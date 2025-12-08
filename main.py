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
# STX(1) + TYPE(1) + DATA + CRC(2) + ETX(1)
# DATA 길이는 프로토콜 문서 기준
PACKET_LEN = {
    0x0C: 17,   # 1P2W : DATA 12 bytes
    0x20: 37,   # 3P3W : DATA 32 bytes
    0x22: 39    # 3P4W : DATA 34 bytes
}

store = {
    0:  {'V': 2200, 'A': 100, 'kW': 20000, 'kWh': 12345},
    34: {'V1': 3810, 'V2': 3810, 'V3': 3810,
         'A1': 1100, 'A2': 1100, 'A3': 1100,
         'kW1': 21000, 'kW2': 21000, 'kW3': 21000,
         'kWh1': 123456, 'kWh2': 123456, 'kWh3':123456},
    48: {'V12': 38000, 'V23': 38000, 'V31': 38000,
         'A1': 1000, 'A2': 1000, 'A3': 1000, 'NA': 0,
         'kW1': 20000, 'kW2': 20000, 'kW3': 20000,
         'kWh1': 123456, 'kWh2': 123456, 'kWh3':123456},
}


def fmt_voltage(val: int) -> str:
    # 프로토콜: 전압[V] 소수점 1자리(/10)
    return f"{val / 10:.1f} V"


def fmt_current(val: int) -> str:
    # 프로토콜: 전류[A] 소수점 2자리(/100)
    return f"{val / 100:.2f} A"


def fmt_power(val: int) -> str:
    # 프로토콜: 유효전력[kW] 소수점 3자리(/1000)
    return f"{val / 1000:.3f} kW"


def decode_kwh_4bytes(w_hi: int, w_lo: int) -> int:
    """
    4바이트 전력량 데이터를 32비트 정수 kWh로 디코딩.
    - w_hi: 상위 WORD (High word)
    - w_lo: 하위 WORD (Low word)
    """
    return (w_hi << 16) | w_lo


def fmt_energy(val: int) -> str:
    # 프로토콜: 전력량[kWh] 정수값 (0 ~ 9,999,999)
    return f"{val} kWh"


def debug_kwh_range(label: str, kwh1: int, kwh2: int, kwh3: int):
    print(f"{label} kWh1={kwh1}, kWh2={kwh2}, kWh3={kwh3}")
    for i, v in enumerate([kwh1, kwh2, kwh3], start=1):
        if not (0 <= v <= 9_999_999):
            print(f"  -> kWh{i} OUT OF RANGE: {v}")


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

                # STX 읽기
                b = self.ser.read(1)
                if not b or b[0] != 0x02:
                    continue

                # TYPE (0x0C / 0x20 / 0x22 ...)
                t = self.ser.read(1)
                if not t:
                    continue
                msg_type = t[0]

                # 나머지 패킷 길이는 타입별로 고정
                packet_len = PACKET_LEN.get(msg_type, 17)
                remaining = packet_len - 2  # 이미 STX, TYPE 2바이트 읽음
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
        self.log.emit(datetime.datetime.now().strftime("[%H:%M:%S]") + ' COM OPEN')
        return self.ser

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.log.emit(datetime.datetime.now().strftime("[%H:%M:%S]") + ' COM CLOSE')


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
        self.baud_combo.addItems(["9600", "19200", "38400", "115200"])
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
        self.setWindowTitle("Power Monitor - 1P2W / 3P3W / 3P4W")

        # 버튼 연결
        self.open_btn.clicked.connect(self.com_open)
        self.close_btn.clicked.connect(self.com_close)

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
            for c in range(self.table_3p3w.columnCount()):  # L1, L2, L3
                self._set_item(self.table_3p3w, r, c, "-")

    def _init_3p4w_table(self):
        row_labels = ["전압[V]", "전류[A]", "유효전력[kW]", "전력량[kWh]"]
        for r, name in enumerate(row_labels):
            self.table_3p4w.setVerticalHeaderItem(r, QTableWidgetItem(name))
            for c in range(self.table_3p4w.columnCount()):  # L1, L2, L3, N
                self._set_item(self.table_3p4w, r, c, "-")

    # ===== 로그 =====
    @Slot(str)
    def log_msg(self, msg: str):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
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

            # CRC 검사 (TYPE부터 CRC 직전까지)
            crc_data = msg[1:-3]
            crc_rcv = int.from_bytes(msg[-3:-1], 'little')
            crc_calc = crc16_modbus(crc_data)
            if crc_calc != crc_rcv:
                self.log_msg("CRC mismatch")
                return

            if msg_type == 0x0C:
                self.update_1p2w(msg)
            elif msg_type == 0x20:
                self.update_3p3w(msg)
            elif msg_type == 0x22:
                self.update_3p4w(msg)

        except Exception as e:
            self.log_msg(f"RX Error: {e}")

    # ===== 각 상별 UI 업데이트 =====
    def update_1p2w(self, msg: bytes):
        """
        1P2W (단상) 프레임 파싱.
        데이터 구조 (총 12 bytes, msg[2:-3]):
          [0]  일련번호
          [1]  장치 번호
          [2-3]  전압 V
          [4-5]  전류 A
          [6-7]  유효전력 kW
          [8-11] 전력량 kWh (4바이트)
        """
        data = msg[2:-3]
        if len(data) < 12:
            return

        # seq = data[0]
        # dev_id = data[1]

        V = (data[2] << 8) | data[3]
        A = (data[4] << 8) | data[5]
        kW = (data[6] << 8) | data[7]
        kWh = int.from_bytes(data[8:12], "big")

        self._set_item(self.table_1p2w, 0, 1, fmt_voltage(V))
        self._set_item(self.table_1p2w, 1, 1, fmt_current(A))
        self._set_item(self.table_1p2w, 2, 1, fmt_power(kW))
        self._set_item(self.table_1p2w, 3, 1, fmt_energy(kWh))

    def update_3p3w(self, msg: bytes):
        """
        3상3선(3P3W) 프레임 파싱.
        데이터 구조 (총 32 bytes, msg[2:-3]):
          [0]    일련번호
          [1]    장치 번호
          [2-3]  V1
          [4-5]  V2
          [6-7]  V3
          [8-9]  A1
          [10-11] A2
          [12-13] A3
          [14-15] kW1
          [16-17] kW2
          [18-19] kW3
          [20-23] kWh1 (4B)
          [24-27] kWh2 (4B)
          [28-31] kWh3 (4B)
        """
        data = msg[2:-3]
        if len(data) < 32:
            return

        def u16(offset):
            return (data[offset] << 8) | data[offset + 1]

        V1 = u16(2)
        V2 = u16(4)
        V3 = u16(6)

        A1 = u16(8)
        A2 = u16(10)
        A3 = u16(12)

        kW1 = u16(14)
        kW2 = u16(16)
        kW3 = u16(18)

        # 전력량 4바이트 (상위 WORD + 하위 WORD)
        kWh1 = int.from_bytes(data[20:24], "big")
        kWh2 = int.from_bytes(data[24:28], "big")
        kWh3 = int.from_bytes(data[28:32], "big")

        # debug_kwh_range("3P3W", kWh1, kWh2, kWh3)

        # Row 0: 전압
        self._set_item(self.table_3p3w, 0, 0, fmt_voltage(V1))
        self._set_item(self.table_3p3w, 0, 1, fmt_voltage(V2))
        self._set_item(self.table_3p3w, 0, 2, fmt_voltage(V3))

        # Row 1: 전류
        self._set_item(self.table_3p3w, 1, 0, fmt_current(A1))
        self._set_item(self.table_3p3w, 1, 1, fmt_current(A2))
        self._set_item(self.table_3p3w, 1, 2, fmt_current(A3))

        # Row 2: 유효전력
        self._set_item(self.table_3p3w, 2, 0, fmt_power(kW1))
        self._set_item(self.table_3p3w, 2, 1, fmt_power(kW2))
        self._set_item(self.table_3p3w, 2, 2, fmt_power(kW3))

        # Row 3: 전력량
        self._set_item(self.table_3p3w, 3, 0, fmt_energy(kWh1))
        self._set_item(self.table_3p3w, 3, 1, fmt_energy(kWh2))
        self._set_item(self.table_3p3w, 3, 2, fmt_energy(kWh3))

    def update_3p4w(self, msg: bytes):
        """
        3상4선(3P4W) 프레임 파싱.
        데이터 구조 (총 34 bytes, msg[2:-3]):
          [0]    일련번호
          [1]    장치 번호
          [2-3]  V12
          [4-5]  V23
          [6-7]  V31
          [8-9]  A1
          [10-11] A2
          [12-13] A3
          [14-15] N (중성선)
          [16-17] kW1
          [18-19] kW2
          [20-21] kW3
          [22-25] kWh1 (4B)
          [26-29] kWh2 (4B)
          [30-33] kWh3 (4B)
        """
        data = msg[2:-3]
        if len(data) < 34:
            return

        def u16(offset):
            return (data[offset] << 8) | data[offset + 1]

        V12 = u16(2)
        V23 = u16(4)
        V31 = u16(6)

        A1 = u16(8)
        A2 = u16(10)
        A3 = u16(12)
        N = u16(14)

        kW1 = u16(16)
        kW2 = u16(18)
        kW3 = u16(20)

        kWh1 = int.from_bytes(data[22:26], "big")
        kWh2 = int.from_bytes(data[26:30], "big")
        kWh3 = int.from_bytes(data[30:34], "big")

        # debug_kwh_range("3P4W", kWh1, kWh2, kWh3)

        # Row 0: 전압 (선간전압)
        self._set_item(self.table_3p4w, 0, 0, fmt_voltage(V12))
        self._set_item(self.table_3p4w, 0, 1, fmt_voltage(V23))
        self._set_item(self.table_3p4w, 0, 2, fmt_voltage(V31))
        self._set_item(self.table_3p4w, 0, 3, "-")  # N에는 전압 없음

        # Row 1: 전류 (L1/L2/L3/N)
        self._set_item(self.table_3p4w, 1, 0, fmt_current(A1))
        self._set_item(self.table_3p4w, 1, 1, fmt_current(A2))
        self._set_item(self.table_3p4w, 1, 2, fmt_current(A3))
        self._set_item(self.table_3p4w, 1, 3, fmt_current(N))

        # Row 2: 유효전력
        self._set_item(self.table_3p4w, 2, 0, fmt_power(kW1))
        self._set_item(self.table_3p4w, 2, 1, fmt_power(kW2))
        self._set_item(self.table_3p4w, 2, 2, fmt_power(kW3))
        self._set_item(self.table_3p4w, 2, 3, "-")

        # Row 3: 전력량 (각 상별)
        self._set_item(self.table_3p4w, 3, 0, fmt_energy(kWh1))
        self._set_item(self.table_3p4w, 3, 1, fmt_energy(kWh2))
        self._set_item(self.table_3p4w, 3, 2, fmt_energy(kWh3))
        self._set_item(self.table_3p4w, 3, 3, "-")

    # ===== (옵션) 시뮬레이션용 응답 생성 =====
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
                    0x00,              # 일련번호
                    0x01,              # 장치 번호
                    V >> 8, V & 0xFF,
                    A >> 8, A & 0xFF,
                    kW >> 8, kW & 0xFF,
                    (kWh >> 24) & 0xFF,
                    (kWh >> 16) & 0xFF,
                    (kWh >> 8) & 0xFF,
                    kWh & 0xFF
                ])

            elif msg_type == 0x20:
                response_data.extend([0x00, 0x02])  # 일련번호, 장치 번호

                # V/A/kW는 그대로
                for key in ['V1', 'V2', 'V3', 'A1', 'A2', 'A3', 'kW1', 'kW2', 'kW3']:
                    val = (dev_data.get(key, 0) + rand_val) & 0xFFFF
                    response_data.extend([val >> 8, val & 0xFF])

                # --- 여기부터 전력량(kWh1, kWh2, kWh3) 개별 처리 ---
                cnt = self.device_counters[device_id]

                kWh1 = (dev_data.get('kWh1', 0) + cnt) & 0xFFFFFFFF
                kWh2 = (dev_data.get('kWh2', 0) + cnt) & 0xFFFFFFFF
                kWh3 = (dev_data.get('kWh3', 0) + cnt) & 0xFFFFFFFF

                for kWh in (kWh1, kWh2, kWh3):
                    response_data.extend([
                        (kWh >> 24) & 0xFF,
                        (kWh >> 16) & 0xFF,
                        (kWh >> 8) & 0xFF,
                        kWh & 0xFF
                    ])

            elif msg_type == 0x22:
                response_data.extend([0x00, 0x03])  # 일련번호, 장치 번호

                # V/A/N/kW는 그대로
                for key in ['V12', 'V23', 'V31', 'A1', 'A2', 'A3', 'NA', 'kW1', 'kW2', 'kW3']:
                    val = (dev_data.get(key, 0) + rand_val) & 0xFFFF
                    response_data.extend([val >> 8, val & 0xFF])

                # --- 전력량(kWh1, kWh2, kWh3) 개별 처리 ---
                cnt = self.device_counters[device_id]

                kWh1 = (dev_data.get('kWh1', 0) + cnt) & 0xFFFFFFFF
                kWh2 = (dev_data.get('kWh2', 0) + cnt) & 0xFFFFFFFF
                kWh3 = (dev_data.get('kWh3', 0) + cnt) & 0xFFFFFFFF

                for kWh in (kWh1, kWh2, kWh3):
                    response_data.extend([
                        (kWh >> 24) & 0xFF,
                        (kWh >> 16) & 0xFF,
                        (kWh >> 8) & 0xFF,
                        kWh & 0xFF
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
