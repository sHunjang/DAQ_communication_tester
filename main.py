import sys
import datetime
import random
import serial
import serial.tools.list_ports

from PySide6.QtCore import QThread, Signal, Slot, QObject
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QGroupBox, QTextEdit
)

# ===== 통신 기본 설정 =====
PACKET_LEN = {0x0C: 17, 0x20: 37, 0x22: 39}

store = {
    0:  {'V': 2200, 'A': 100, 'kW': 20000, 'kWh': 12345},
    34: {'V1': 3810, 'V2': 3810, 'V3': 3810,
         'A1': 1100, 'A2': 1100, 'A3': 1100,
         'kW1': 21000, 'kW2': 21000, 'kW3': 21000, 'kWh': 123456},
    48: {'V12': 38000, 'V23': 38000, 'V31': 38000,
         'A1': 1000, 'A2': 1000, 'A3': 1000, 'NA': 0,
         'kW1': 20000, 'kW2': 20000, 'kW3': 20000, 'kWh': 100000},
}

def fmt_voltage(val: int) -> str:
    return f"{val / 10:.1f} V"

def fmt_current(val: int) -> str:
    return f"{val / 100:.2f} A"

def fmt_power(val: int) -> str:
    return f"{val / 1000:.3f} kW"


def decode_kwh_4bytes(w_hi: int, w_lo: int) -> int:
    """
    4바이트 전력량 데이터를 32비트 정수 kWh로 디코딩.
    
    가정:
      - w_hi: 상위 WORD (High word)
      - w_lo: 하위 WORD (Low word)
      - 전체 32bit 값이 0 ~ 9,999,999 범위의 정수 kWh.
    """
    # Hi WORD가 상위 16비트, Lo WORD가 하위 16비트
    return (w_hi << 16) | w_lo


def fmt_energy(val: int) -> str:
    return f"{val} kWh"

def debug_kwh_range(label: str, kwh1: int, kwh2: int, kwh3: int):
    print(f"{label} kWh1={kwh1}, kWh2={kwh2}, kWh3={kwh3}")
    for i, v in enumerate([kwh1, kwh2, kwh3], start=1):
        if not (0 <= v <= 9_999_999):
            print(f"  -> kWh{i} OUT OF RANGE: {v}")

def debug_1p2w_energy(self, msg: bytes):
    data = msg[2:-3]
    b8, b9, b10, b11 = data[8], data[9], data[10], data[11]
    print("1P2W kWh bytes:", b8, b9, b10, b11)
    kwh_4 = (b8 << 24) | (b9 << 16) | (b10 << 8) | b11
    print("1P2W kWh 4B:", kwh_4)

def crc16_modbus(data: bytes) -> int:
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

class ComThread(QThread):
    received_msg = Signal(bytes)
    log = Signal(str)

    def __init__(self):
        super().__init__()
        self.ser = serial.Serial()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            try:
                if not self.ser or not self.ser.is_open:
                    break
                b = self.ser.read(1)
                if not b or b[0] != 0x02:
                    continue
                t = self.ser.read(1)
                if not t:
                    continue
                msg_type = t[0]
                packet_len = PACKET_LEN.get(msg_type, 17)
                remaining = packet_len - 2
                rest = self.ser.read(remaining)
                if len(rest) != remaining:
                    continue
                packet = bytes([0x02, msg_type]) + rest
                if packet[-1] != 0x03:
                    continue
                self.received_msg.emit(packet)
            except Exception as e:
                if self.running:
                    self.log.emit(f"Thread error: {e}")
                continue

    def stop(self):
        self.running = False

class SerialHandler(QObject):
    log = Signal(str)

    def __init__(self):
        super().__init__()
        self.ser = None

    def get_port_list(self):
        return sorted([p.device for p in serial.tools.list_ports.comports()])

    def open(self, com_name, baud=9600):
        self.ser = serial.Serial(com_name, baud, timeout=1)
        self.log.emit('COM OPEN')
        return self.ser

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.log.emit('COM CLOSE')

class MainWindow(QMainWindow):
    
    def clear_log(self):
        if hasattr(self, "log_view"):
            self.log_view.clear()
            
    def __init__(self):
        super().__init__()

        self.device_counters = {}
        self.comm_handler = SerialHandler()
        self.worker = ComThread()
        self.worker.received_msg.connect(self.received_msg_slot)
        self.worker.log.connect(self.log_msg)
        self.comm_handler.log.connect(self.log_msg)

        # ===== UI =====
        central = QWidget()
        root = QVBoxLayout(central)

        # 상단: Port / Baud / Open / Close
        top = QHBoxLayout()
        root.addLayout(top)

        self.port_combo = QComboBox()
        self.port_combo.addItems(self.comm_handler.get_port_list())
        top.addWidget(QLabel("Port:"))
        top.addWidget(self.port_combo)

        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["9600", "19200", "38400"])
        self.baud_combo.setCurrentText("9600")
        top.addWidget(QLabel("Baud:"))
        top.addWidget(self.baud_combo)

        self.open_btn = QPushButton("Open")
        self.close_btn = QPushButton("Close")
        self.close_btn.setEnabled(False)
        top.addWidget(self.open_btn)
        top.addWidget(self.close_btn)
        top.addStretch(1)

        # 1P2W
        self.table_1p2w = QTableWidget()
        self.table_1p2w.setRowCount(4)
        self.table_1p2w.setColumnCount(2)
        self.table_1p2w.setHorizontalHeaderLabels(["Item", "Value"])
        self._init_1p2w_table()

        gb1 = QGroupBox("1P2W (단상)")
        gb1_layout = QVBoxLayout(gb1)
        gb1_layout.addWidget(self.table_1p2w)
        root.addWidget(gb1)

        # 3P3W
        self.table_3p3w = QTableWidget()
        self.table_3p3w.setRowCount(4)
        self.table_3p3w.setColumnCount(3)
        self.table_3p3w.setHorizontalHeaderLabels(["L1", "L2", "L3"])
        self._init_3p3w_table()

        gb2 = QGroupBox("3P3W (3상3선)")
        gb2_layout = QVBoxLayout(gb2)
        gb2_layout.addWidget(self.table_3p3w)
        root.addWidget(gb2)

        # 3P4W
        self.table_3p4w = QTableWidget()
        self.table_3p4w.setRowCount(4)
        self.table_3p4w.setColumnCount(4)
        self.table_3p4w.setHorizontalHeaderLabels(["L1", "L2", "L3", "N"])
        self._init_3p4w_table()

        gb3 = QGroupBox("3P4W (3상4선)")
        gb3_layout = QVBoxLayout(gb3)
        gb3_layout.addWidget(self.table_3p4w)
        root.addWidget(gb3)

        self.setCentralWidget(central)
        self.setWindowTitle("Power Monitor - 1P2W / 3P3W / 3P4W")

        # 버튼 연결
        self.open_btn.clicked.connect(self.com_open)
        self.close_btn.clicked.connect(self.com_close)
        
        root.addWidget(gb3)
        
        # ===== Log 영역 =====
        log_layout = QHBoxLayout()
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)

        self.log_clear_btn = QPushButton("Log Clear")
        self.log_clear_btn.clicked.connect(self.clear_log)

        log_layout.addWidget(self.log_view)
        log_layout.addWidget(self.log_clear_btn)

        root.addLayout(log_layout)

        self.setCentralWidget(central)

    # ===== 테이블 유틸 =====
    def _set_item(self, table, row, col, text):
        item = table.item(row, col)
        if item is None:
            item = QTableWidgetItem()
            table.setItem(row, col, item)
        item.setText(str(text))

    def _init_1p2w_table(self):
        labels = ["전압[V]", "전류[A]", "유효전력[kW]", "전력량[kWh]"]
        for r, name in enumerate(labels):
            self._set_item(self.table_1p2w, r, 0, name)
            self._set_item(self.table_1p2w, r, 1, "-")

    def _init_3p3w_table(self):
        row_labels = ["전압[V]", "전류[A]", "유효전력[kW]", "전력량[kWh]"]
        for r, name in enumerate(row_labels):
            self.table_3p3w.setVerticalHeaderItem(r, QTableWidgetItem(name))
            for c in range(4):
                self._set_item(self.table_3p3w, r, c, "-")

    def _init_3p4w_table(self):
        row_labels = ["전압[V]", "전류[A]", "유효전력[kW]", "전력량[kWh]"]
        for r, name in enumerate(row_labels):
            self.table_3p4w.setVerticalHeaderItem(r, QTableWidgetItem(name))
            for c in range(5):
                self._set_item(self.table_3p4w, r, c, "-")

    # ===== 디버그: 에너지 후보 4바이트 =====
    def debug_energy_candidates(self, msg: bytes, label: str):
        data = msg[2:-3]
        if len(data) < 16:
            return
        cand = data[-16:]  # CRC 앞 16바이트를 kWh 후보라고 가정
        e1_big = int.from_bytes(cand[0:4], "big")
        e2_big = int.from_bytes(cand[4:8], "big")
        e3_big = int.from_bytes(cand[8:12], "big")
        et_big = int.from_bytes(cand[12:16], "big")
        e1_lit = int.from_bytes(cand[0:4], "little")
        e2_lit = int.from_bytes(cand[4:8], "little")
        e3_lit = int.from_bytes(cand[8:12], "little")
        et_lit = int.from_bytes(cand[12:16], "little")
        print(f"{label} kWh cand BIG : {e1_big}, {e2_big}, {e3_big}, {et_big}")
        print(f"{label} kWh cand LIT : {e1_lit}, {e2_lit}, {e3_lit}, {et_lit}")
    
    def debug_1p2w_energy(self, msg: bytes):
        data = msg[2:-3]
        if len(data) < 12:
            return
        b8, b9, b10, b11 = data[8], data[9], data[10], data[11]
        kwh_4 = (b8 << 24) | (b9 << 16) | (b10 << 8) | b11
        print(f"1P2W kWh bytes: {b8:02X} {b9:02X} {b10:02X} {b11:02X}, int={kwh_4}")

    # ===== 로그 =====
    @Slot(str)
    def log_msg(self, msg: str):
        # 타임스탬프 붙이기
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"

        # 콘솔 출력(원하면 유지)
        print(line)

        # UI 로그창에 추가
        if hasattr(self, "log_view"):
            self.log_view.append(line)

    # ===== COM 제어 =====
    def com_open(self):
        try:
            port = self.port_combo.currentText()
            baud = int(self.baud_combo.currentText())
            self.worker.ser = self.comm_handler.open(port, baud)
            self.worker.start()
            self.open_btn.setEnabled(False)
            self.close_btn.setEnabled(True)
        except Exception as e:
            self.log_msg(f"Open Error: {e}")

    def com_close(self):
        try:
            self.worker.stop()
            if self.worker.isRunning():
                self.worker.wait(2000)
            self.comm_handler.close()
            self.open_btn.setEnabled(True)
            self.close_btn.setEnabled(False)
        except Exception as e:
            self.log_msg(f"Close Error: {e}")

    # ===== RX 처리 =====
    @Slot(bytes)
    def received_msg_slot(self, msg: bytes):
        try:
            if len(msg) < 5 or msg[0] != 0x02 or msg[-1] != 0x03:
                return
            print('RX:', ' '.join(f'{b:02x}' for b in msg))
            self.log_msg('RX: ' + ' '.join(f'{b:02x}' for b in msg))

            msg_type = msg[1]
            crc_data = msg[1:-3]
            crc_rcv = int.from_bytes(msg[-3:-1], 'little')
            crc_calc = crc16_modbus(crc_data)
            if crc_calc != crc_rcv:
                return

            if msg_type == 0x0C:
                self.update_1p2w(msg)
            elif msg_type == 0x20:
                self.debug_energy_candidates(msg, "3P3W")
                self.update_3p3w(msg)
            elif msg_type == 0x22:
                self.debug_energy_candidates(msg, "3P4W")
                self.update_3p4w(msg)

            # device_id = {0x0C: 0, 0x20: 34, 0x22: 48}.get(msg_type, 0)
            # self.generate_response(device_id, msg_type)

        except Exception as e:
            self.log_msg(f"RX Error: {e}")

    # ===== 각 상별 UI 업데이트 =====
    def update_1p2w(self, msg: bytes):
        self.debug_1p2w_energy(msg)
        data = msg[2:-3]
        if len(data) < 12:
            return
        V   = (data[2] << 8) | data[3]
        A   = (data[4] << 8) | data[5]
        kW  = (data[6] << 8) | data[7]
        kWh = (data[8] << 24) | (data[9] << 16) | (data[10] << 8) | data[11]

        self._set_item(self.table_1p2w, 0, 1, fmt_voltage(V))
        self._set_item(self.table_1p2w, 1, 1, fmt_current(A))
        self._set_item(self.table_1p2w, 2, 1, fmt_power(kW))
        self._set_item(self.table_1p2w, 3, 1, fmt_energy(kWh))

    def update_3p3w(self, msg: bytes):
        """
        3상3선(3P3W) 프레임을 파싱하여 UI 테이블을 업데이트.
        
        프레임 구조 (총 37바이트):
        [STX(1)][TYPE(1)][DATA(32)][CRC(2)][ETX(1)]
        
        DATA 영역 (32바이트 = 16 WORD):
        - WORD 0~2:   전압 V1, V2, V3 (각 2바이트)
        - WORD 3~5:   전류 A1, A2, A3
        - WORD 6~8:   유효전력 kW1, kW2, kW3
        - WORD 9~10:  전력량 L1 (4바이트)
        - WORD 11~12: 전력량 L2 (4바이트)
        - WORD 13~14: 전력량 L3 (4바이트)
        
        스케일:
        - 전압: 소수점 1자리 (/10)
        - 전류: 소수점 2자리 (/100)
        - 전력: 소수점 3자리 (/1000)
        - 전력량: 정수 (0~9,999,999)
        """
        # STX, TYPE, CRC, ETX 제거 → 순수 DATA 영역만 추출
        data = msg[2:-3]
        
        # DATA를 2바이트(WORD) 단위로 분리하여 리스트로 만듦
        vals = []
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                # big-endian: [상위바이트][하위바이트]
                vals.append((data[i] << 8) | data[i + 1])
        
        # 최소 15개 WORD 필요 (전압3 + 전류3 + 전력3 + 전력량6)
        if len(vals) < 15:
            return
        
        # === 각 파라미터 추출 ===
        # 전압 (WORD 0~2)
        V1, V2, V3 = vals[0], vals[1], vals[2]
        
        # 전류 (WORD 3~5)
        A1, A2, A3 = vals[3], vals[4], vals[5]
        
        # 유효전력 (WORD 6~8)
        kW1, kW2, kW3 = vals[6], vals[7], vals[8]
        
        # 전력량 (각 4바이트 = 2 WORD씩)
        # vals[9~10] = L1 전력량, vals[11~12] = L2, vals[13~14] = L3
        kWh1 = vals[9]
        kWh2 = vals[11]
        kWh3 = vals[13]
        
        # === UI 테이블 업데이트 ===
        # Row 0: 전압 (V)
        self._set_item(self.table_3p3w, 0, 0, fmt_voltage(V1))   # L1
        self._set_item(self.table_3p3w, 0, 1, fmt_voltage(V2))   # L2
        self._set_item(self.table_3p3w, 0, 2, fmt_voltage(V3))   # L3
        
        # Row 1: 전류 (A)
        self._set_item(self.table_3p3w, 1, 0, fmt_current(A1))
        self._set_item(self.table_3p3w, 1, 1, fmt_current(A2))
        self._set_item(self.table_3p3w, 1, 2, fmt_current(A3))
        
        # Row 2: 유효전력 (kW)
        self._set_item(self.table_3p3w, 2, 0, fmt_power(kW1))
        self._set_item(self.table_3p3w, 2, 1, fmt_power(kW2))
        self._set_item(self.table_3p3w, 2, 2, fmt_power(kW3))
        
        # Row 3: 전력량 (kWh) - 각 상별 + 합계
        self._set_item(self.table_3p3w, 3, 0, fmt_energy(kWh1))  # L1
        self._set_item(self.table_3p3w, 3, 1, fmt_energy(kWh2))  # L2
        self._set_item(self.table_3p3w, 3, 2, fmt_energy(kWh3))  # L3
        # debug_kwh_range("3P4W", kWh1, kWh2, kWh3)
        # self._set_item(self.table_3p3w, 3, 3, fmt_energy(kWh1 + kWh2 + kWh3))  # Sum


    def update_3p4w(self, msg: bytes):
        """
        3상4선(3P4W) 프레임을 파싱하여 UI 테이블을 업데이트.
        
        프레임 구조 (총 39바이트):
        [STX(1)][TYPE(1)][DATA(34)][CRC(2)][ETX(1)]
        
        DATA 영역 (34바이트 = 17 WORD):
        - WORD 0~2:   전압 V12, V23, V31 (선간전압, 각 2바이트)
        - WORD 3~6:   전류 A1, A2, A3, N (중성선 포함 4개)
        - WORD 7~9:   유효전력 kW1, kW2, kW3
        - WORD 10~11: 전력량 L1 (4바이트)
        - WORD 12~13: 전력량 L2 (4바이트)
        - WORD 14~15: 전력량 L3 (4바이트)
        
        3P3W와의 차이점:
        - 전압: 상전압이 아닌 선간전압 (V12, V23, V31)
        - 전류: 중성선(N) 전류 추가 (총 4개)
        """
        # STX, TYPE, CRC, ETX 제거 → 순수 DATA 영역만 추출
        data = msg[2:-3]
        
        # DATA를 2바이트(WORD) 단위로 분리
        vals = []
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                vals.append((data[i] << 8) | data[i + 1])
        
        # 최소 16개 WORD 필요
        if len(vals) < 16:
            return
        
        # === 각 파라미터 추출 ===
        # 전압 (WORD 0~2) - 선간전압
        V12, V23, V31 = vals[0], vals[1], vals[2]
        
        # 전류 (WORD 3~6) - L1, L2, L3, 중성선(N)
        A1, A2, A3, N = vals[3], vals[4], vals[5], vals[6]
        
        # 유효전력 (WORD 7~9)
        kW1, kW2, kW3 = vals[7], vals[8], vals[9]
        
        # 전력량 (각 4바이트 = 2 WORD씩)
        # vals[10~11] = L1, vals[12~13] = L2, vals[14~15] = L3
        kWh1 = vals[10]
        kWh2 = vals[12]
        kWh3 = vals[14]
        
        # === UI 테이블 업데이트 ===
        # Row 0: 전압 (V) - 선간전압
        self._set_item(self.table_3p4w, 0, 0, fmt_voltage(V12))   # L1-L2
        self._set_item(self.table_3p4w, 0, 1, fmt_voltage(V23))   # L2-L3
        self._set_item(self.table_3p4w, 0, 2, fmt_voltage(V31))   # L3-L1
        
        # Row 1: 전류 (A) - 중성선 포함
        self._set_item(self.table_3p4w, 1, 0, fmt_current(A1))    # L1
        self._set_item(self.table_3p4w, 1, 1, fmt_current(A2))    # L2
        self._set_item(self.table_3p4w, 1, 2, fmt_current(A3))    # L3
        self._set_item(self.table_3p4w, 1, 3, fmt_current(N))     # Neutral
        
        # Row 2: 유효전력 (kW)
        self._set_item(self.table_3p4w, 2, 0, fmt_power(kW1))
        self._set_item(self.table_3p4w, 2, 1, fmt_power(kW2))
        self._set_item(self.table_3p4w, 2, 2, fmt_power(kW3))
        
        # Row 3: 전력량 (kWh) - 각 상별 + 합계
        self._set_item(self.table_3p4w, 3, 0, fmt_energy(kWh1))   # L1
        self._set_item(self.table_3p4w, 3, 1, fmt_energy(kWh2))   # L2
        self._set_item(self.table_3p4w, 3, 2, fmt_energy(kWh3))   # L3
        # self._set_item(self.table_3p4w, 3, 4, fmt_energy(kWh1 + kWh2 + kWh3))  # Sum



    # ===== TX 응답 =====
    def genete_response(self, device_id: int, msg_type: int):
        try:
            dev_data = store.get(device_id, store[0])
            rand_val = random.randrange(0, 10) * 100

            if device_id not in self.device_counters:
                self.device_counters[device_id] = 0
            self.device_counters[device_id] += 1

            response_data = []

            if msg_type == 0x0C:
                V = (dev_data['V'] + rand_val) & 0xFFFF
                A = (dev_data['A'] + rand_val) & 0xFFFF
                kW = (dev_data['kW'] + rand_val) & 0xFFFF
                kWh = (dev_data['kWh'] + self.device_counters[device_id]) & 0xFFFFFFFF
                response_data.extend([
                    V >> 8, V & 0xFF,
                    A >> 8, A & 0xFF,
                    kW >> 8, kW & 0xFF,
                    (kWh >> 24) & 0xFF,
                    (kWh >> 16) & 0xFF,
                    (kWh >> 8) & 0xFF,
                    kWh & 0xFF
                ])

            elif msg_type == 0x20:
                for key in ['V1','V2','V3','A1','A2','A3','kW1','kW2','kW3']:
                    val = (dev_data.get(key, 0) + rand_val) & 0xFFFF
                    response_data.extend([val >> 8, val & 0xFF])
                kWh = (dev_data['kWh'] + self.device_counters[device_id]) & 0xFFFFFFFF
                response_data.extend([
                    (kWh >> 24) & 0xFF,
                    (kWh >> 16) & 0xFF,
                    (kWh >> 8) & 0xFF,
                    kWh & 0xFF,
                    0,0,0,0,0,0,0,0
                ])

            elif msg_type == 0x22:
                for key in ['V12','V23','V31','A1','A2','A3','NA','kW1','kW2','kW3']:
                    val = (dev_data.get(key, 0) + rand_val) & 0xFFFF
                    response_data.extend([val >> 8, val & 0xFF])
                kWh = (dev_data['kWh'] + self.device_counters[device_id]) & 0xFFFFFFFF
                response_data.extend([
                    (kWh >> 24) & 0xFF,
                    (kWh >> 16) & 0xFF,
                    (kWh >> 8) & 0xFF,
                    kWh & 0xFF,
                    0,0,0,0,0,0,0,0
                ])

            tx_crc_data = [msg_type] + response_data
            crc_tx = crc16_modbus(bytes(tx_crc_data))
            full_resp = [0x02] + tx_crc_data + [crc_tx & 0xFF, (crc_tx >> 8) & 0xFF, 0x03]

            self.check_and_write(full_resp)

        except Exception as e:
            self.log_msg(f"Gen Error: {e}")

    def check_and_write(self, send_msg):
        try:
            if not self.worker.ser or not self.worker.ser.is_open:
                return
            safe_msg = [int(x) & 0xFF for x in send_msg]
            self.worker.ser.write(bytes(safe_msg))
        except Exception as e:
            if "not open" not in str(e):
                self.log_msg(f"TX Error: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
