"""
=================================================================
파일명: gui_main.py
설명: PyQt5 GUI - DAQ 통신 신뢰도 측정 시스템
작성일: 2025-10-24
=================================================================
전문적인 GUI 인터페이스:
- 실시간 통신 모니터링
- 센서 데이터 시각화
- 신뢰도 통계 대시보드
- 로그 뷰어
- Excel 리포트 생성
=================================================================
"""

import sys
import time
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLabel, QPushButton, QComboBox, QTextEdit, QProgressBar,
    QCheckBox, QSpinBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QTabWidget, QMessageBox, QStatusBar
)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QFont, QColor, QPalette
import pyqtgraph as pg

# 프로젝트 모듈 import
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from config.config import (
    USE_MOCK_SERIAL,
    RS232_PORT,
    BAUDRATE,
    SIMULATION_SENSORS,
    LOG_DIR,
    OUTPUT_DIR
)

from src.daq_protocol import DAQProtocol
from src.data_parser import DataParser
from src.data_logger import DataLogger
from src.reliability_calculator import ReliabilityCalculator
from src.excel_exporter import ExcelExporter
from mock_serial import MockSerial, cleanup_mock_files


# =================================================================
# 통신 스레드 (백그라운드 실행)
# =================================================================
class CommunicationThread(QThread):
    """
    백그라운드에서 DAQ 통신을 수행하는 스레드
    
    GUI를 멈추지 않고 연속적으로 통신을 수행합니다.
    """
    
    # 시그널 정의 (스레드 → GUI 데이터 전달)
    status_update = pyqtSignal(str)  # 상태 메시지
    test_complete = pyqtSignal(dict)  # 테스트 완료 데이터
    log_message = pyqtSignal(str, str)  # 로그 메시지 (레벨, 메시지)
    
    def __init__(self, port, baudrate, sensors, delay=1.0):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.sensors = sensors
        self.delay = delay
        
        self.running = False
        self.paused = False
        
        # 모듈 초기화
        self.protocol = DAQProtocol()
        self.parser = DataParser()
        self.logger = DataLogger(log_dir=LOG_DIR)
        self.calculator = ReliabilityCalculator(target_reliability=99.0)
        
        self.test_count = 0
        self.sensor_index = 0
    
    def run(self):
        """스레드 메인 루프"""
        self.running = True
        self.log_message.emit("INFO", "통신 스레드 시작")
        
        # Mock Serial 초기화
        try:
            cleanup_mock_files()
            time.sleep(0.5)
            
            self.ser = MockSerial(port=self.port, baudrate=self.baudrate, timeout=5)
            self.log_message.emit("SUCCESS", f"포트 {self.port} 연결 성공")
            
        except Exception as e:
            self.log_message.emit("ERROR", f"포트 연결 실패: {e}")
            self.running = False
            return
        
        # 통신 루프
        while self.running:
            if self.paused:
                time.sleep(0.1)
                continue
            
            try:
                self._perform_test()
                time.sleep(self.delay)
                
            except Exception as e:
                self.log_message.emit("ERROR", f"테스트 오류: {e}")
        
        # 종료 처리
        self.ser.close()
        self.logger.close()
        self.log_message.emit("INFO", "통신 스레드 종료")
    
    def _perform_test(self):
        """단일 테스트 수행"""
        self.test_count += 1
        msg_type = self.sensors[self.sensor_index]
        self.sensor_index = (self.sensor_index + 1) % len(self.sensors)
        
        sensor_name = self.protocol.get_msg_type_name(msg_type)
        
        # 상태 업데이트
        self.status_update.emit(f"테스트 #{self.test_count} - {sensor_name}")
        
        # 요청 전송
        send_time = datetime.now()
        self.logger.log_request(self.test_count, send_time, sensor_name)
        self.ser.write(bytes([msg_type]))
        
        # 응답 수신
        start_time = time.time()
        frame_buffer = bytearray()
        stx_found = False
        
        while time.time() - start_time < 5:
            if self.ser.in_waiting > 0:
                byte = self.ser.read(1)
                
                if not stx_found:
                    if byte[0] == 0x02:
                        stx_found = True
                        frame_buffer.append(byte[0])
                else:
                    frame_buffer.append(byte[0])
                    if byte[0] == 0x03:
                        break
            else:
                time.sleep(0.01)
        
        # 타임아웃 체크
        if not stx_found or len(frame_buffer) < 7:
            timeout_time = datetime.now()
            self.logger.log_timeout(self.test_count, timeout_time)
            self.calculator.add_timeout(sensor_name)
            
            self.log_message.emit("WARNING", f"테스트 #{self.test_count} 타임아웃")
            
            self.test_complete.emit({
                'test_id': self.test_count,
                'sensor': sensor_name,
                'success': False,
                'error': '타임아웃'
            })
            return
        
        # 프레임 파싱
        frame = bytes(frame_buffer)
        receive_time = datetime.now()
        response_time_ms = (receive_time - send_time).total_seconds() * 1000
        
        result = self.protocol.parse_frame(frame)
        
        if not result['valid']:
            self.logger.log_response(self.test_count, receive_time, sensor_name,
                                    success=False, note=result['error'])
            self.calculator.add_test_result(sensor_name, success=False)
            
            self.log_message.emit("ERROR", f"테스트 #{self.test_count} 파싱 오류: {result['error']}")
            
            self.test_complete.emit({
                'test_id': self.test_count,
                'sensor': sensor_name,
                'success': False,
                'error': result['error']
            })
            return
        
        # 데이터 파싱
        parsed_data = self.parser.parse(result['msg_type'], result['data'])
        
        if 'error' in parsed_data:
            self.logger.log_response(self.test_count, receive_time, sensor_name,
                                    success=False, note=parsed_data['error'])
            self.calculator.add_test_result(sensor_name, success=False)
            
            self.log_message.emit("ERROR", f"테스트 #{self.test_count} 데이터 오류")
            
            self.test_complete.emit({
                'test_id': self.test_count,
                'sensor': sensor_name,
                'success': False,
                'error': parsed_data['error']
            })
            return
        
        # 성공 처리
        self.logger.log_response(self.test_count, receive_time, sensor_name, success=True)
        self.logger.log_sensor_data(receive_time, result['msg_type'], sensor_name, parsed_data)
        self.calculator.add_test_result(sensor_name, success=True, response_time_ms=response_time_ms)
        
        self.log_message.emit("SUCCESS", f"테스트 #{self.test_count} 성공 ({response_time_ms:.0f}ms)")
        
        # GUI로 데이터 전송
        self.test_complete.emit({
            'test_id': self.test_count,
            'sensor': sensor_name,
            'success': True,
            'response_time': response_time_ms,
            'data': parsed_data,
            'reliability': self.calculator.get_overall_reliability(),
            'avg_response': self.calculator.get_response_time_stats()['avg']
        })
    
    def stop(self):
        """스레드 중지"""
        self.running = False
    
    def pause(self):
        """일시 정지"""
        self.paused = True
    
    def resume(self):
        """재개"""
        self.paused = False
    
    def get_statistics(self):
        """통계 정보 반환"""
        return self.calculator.get_summary_report()


# =================================================================
# 메인 윈도우 클래스
# =================================================================
class MainWindow(QMainWindow):
    """
    PyQt5 메인 윈도우
    """
    
    def __init__(self):
        super().__init__()
        
        self.comm_thread = None
        self.reliability_history = []  # 신뢰도 추이 기록
        self.response_time_history = []  # 응답시간 추이 기록
        
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("DAQ 통신 신뢰도 측정 시스템 v1.0")
        self.setGeometry(100, 100, 1200, 800)
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 상단: 설정 패널
        main_layout.addWidget(self.create_config_panel())
        
        # 중간: 탭 위젯 (모니터링, 로그, 통계)
        tab_widget = QTabWidget()
        tab_widget.addTab(self.create_monitor_tab(), "실시간 모니터링")
        tab_widget.addTab(self.create_log_tab(), "통신 로그")
        tab_widget.addTab(self.create_stats_tab(), "통계 분석")
        main_layout.addWidget(tab_widget)
        
        # 하단: 상태바
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("준비")
    
    def create_config_panel(self):
        """설정 패널 생성"""
        group = QGroupBox("설정")
        layout = QHBoxLayout()
        
        # 포트 선택
        layout.addWidget(QLabel("포트:"))
        self.port_combo = QComboBox()
        self.port_combo.addItems(['COM3', 'COM4', 'COM5', 'COM6'])
        self.port_combo.setCurrentText(RS232_PORT)
        layout.addWidget(self.port_combo)
        
        # 속도 선택
        layout.addWidget(QLabel("속도:"))
        self.baudrate_combo = QComboBox()
        self.baudrate_combo.addItems(['9600', '19200', '38400', '57600', '115200'])
        self.baudrate_combo.setCurrentText(str(BAUDRATE))
        layout.addWidget(self.baudrate_combo)
        
        # 지연 시간
        layout.addWidget(QLabel("지연(초):"))
        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(0, 10)
        self.delay_spin.setValue(1)
        layout.addWidget(self.delay_spin)
        
        # 센서 선택
        layout.addWidget(QLabel("센서:"))
        self.sensor_checks = {}
        for sensor_id in [0x01, 0x07, 0x06]:
            name = DAQProtocol().get_msg_type_name(sensor_id)
            cb = QCheckBox(name)
            cb.setChecked(sensor_id in SIMULATION_SENSORS)
            self.sensor_checks[sensor_id] = cb
            layout.addWidget(cb)
        
        layout.addStretch()
        
        # 버튼
        self.start_btn = QPushButton("시작")
        self.start_btn.clicked.connect(self.start_test)
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("중지")
        self.stop_btn.clicked.connect(self.stop_test)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        layout.addWidget(self.stop_btn)
        
        self.report_btn = QPushButton("리포트 생성")
        self.report_btn.clicked.connect(self.generate_report)
        self.report_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        layout.addWidget(self.report_btn)
        
        group.setLayout(layout)
        return group
    
    def create_monitor_tab(self):
        """실시간 모니터링 탭"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 상단: 현재 상태
        status_group = QGroupBox("현재 상태")
        status_layout = QVBoxLayout()
        
        self.current_status = QLabel("● 대기 중")
        self.current_status.setStyleSheet("font-size: 16px; color: gray;")
        status_layout.addWidget(self.current_status)
        
        self.current_sensor = QLabel("센서: -")
        self.current_sensor.setStyleSheet("font-size: 14px;")
        status_layout.addWidget(self.current_sensor)
        
        self.sensor_data_label = QLabel("센서 값: -")
        self.sensor_data_label.setStyleSheet("font-size: 14px;")
        status_layout.addWidget(self.sensor_data_label)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # 중간: 통계 표시
        stats_group = QGroupBox("실시간 통계")
        stats_layout = QHBoxLayout()
        
        self.reliability_label = QLabel("신뢰도: -")
        self.reliability_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        stats_layout.addWidget(self.reliability_label)
        
        self.response_label = QLabel("평균응답: -")
        self.response_label.setStyleSheet("font-size: 16px;")
        stats_layout.addWidget(self.response_label)
        
        self.success_label = QLabel("성공: 0/0")
        self.success_label.setStyleSheet("font-size: 16px;")
        stats_layout.addWidget(self.success_label)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # 하단: 신뢰도 차트
        chart_group = QGroupBox("신뢰도 추이")
        chart_layout = QVBoxLayout()
        
        self.reliability_plot = pg.PlotWidget()
        self.reliability_plot.setBackground('w')
        self.reliability_plot.setLabel('left', '신뢰도 (%)')
        self.reliability_plot.setLabel('bottom', '테스트 횟수')
        self.reliability_plot.setYRange(90, 100)
        self.reliability_curve = self.reliability_plot.plot(pen=pg.mkPen('g', width=2))
        
        chart_layout.addWidget(self.reliability_plot)
        chart_group.setLayout(chart_layout)
        layout.addWidget(chart_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_log_tab(self):
        """통신 로그 탭"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("font-family: Consolas; font-size: 10pt;")
        
        layout.addWidget(self.log_text)
        widget.setLayout(layout)
        return widget
    
    def create_stats_tab(self):
        """통계 분석 탭"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 센서별 통계 테이블
        stats_group = QGroupBox("센서별 통계")
        stats_layout = QVBoxLayout()
        
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(6)
        self.stats_table.setHorizontalHeaderLabels([
            '센서명', '총 테스트', '성공', '실패', '신뢰도(%)', '평균응답(ms)'
        ])
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        stats_layout.addWidget(self.stats_table)
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        widget.setLayout(layout)
        return widget
    
    def start_test(self):
        """테스트 시작"""
        # 선택된 센서 확인
        selected_sensors = [sid for sid, cb in self.sensor_checks.items() if cb.isChecked()]
        
        if not selected_sensors:
            QMessageBox.warning(self, "경고", "최소 1개 이상의 센서를 선택하세요.")
            return
        
        # 설정 가져오기
        port = self.port_combo.currentText()
        baudrate = int(self.baudrate_combo.currentText())
        delay = self.delay_spin.value()
        
        # 로그 초기화
        self.log_text.clear()
        self.reliability_history.clear()
        self.response_time_history.clear()
        
        # 통신 스레드 시작
        self.comm_thread = CommunicationThread(port, baudrate, selected_sensors, delay)
        self.comm_thread.status_update.connect(self.update_status)
        self.comm_thread.test_complete.connect(self.handle_test_complete)
        self.comm_thread.log_message.connect(self.add_log)
        self.comm_thread.start()
        
        # UI 업데이트
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.current_status.setText("● 실행 중")
        self.current_status.setStyleSheet("font-size: 16px; color: green;")
        self.statusBar.showMessage("테스트 진행 중...")
        
        self.add_log("INFO", "테스트 시작")
    
    def stop_test(self):
        """테스트 중지"""
        if self.comm_thread:
            self.comm_thread.stop()
            self.comm_thread.wait()
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.current_status.setText("● 중지됨")
        self.current_status.setStyleSheet("font-size: 16px; color: red;")
        self.statusBar.showMessage("테스트 중지")
        
        self.add_log("INFO", "테스트 중지")
        
        # 최종 통계 업데이트
        if self.comm_thread:
            self.update_stats_table()
    
    def update_status(self, message):
        """상태 업데이트"""
        self.current_sensor.setText(message)
        self.statusBar.showMessage(message)
    
    def handle_test_complete(self, data):
        """테스트 완료 처리"""
        if data['success']:
            # 센서 데이터 표시
            sensor_data = data['data']
            text = ""
            
            if 'voltage' in sensor_data:
                text = (f"전압: {sensor_data['voltage']['value']:.1f}V | "
                       f"전류: {sensor_data['current']['value']:.2f}A | "
                       f"전력: {sensor_data['power']['value']:.3f}kW")
            elif 'temperature' in sensor_data:
                text = (f"온도: {sensor_data['temperature']['value']:.1f}℃ | "
                       f"습도: {sensor_data['humidity']['value']:.1f}%")
            elif 'co2' in sensor_data:
                text = f"CO2: {sensor_data['co2']['value']} ppm"
            
            self.sensor_data_label.setText(f"센서 값: {text}")
            
            # 통계 업데이트
            reliability = data['reliability']
            avg_response = data['avg_response']
            
            self.reliability_label.setText(f"신뢰도: {reliability:.1f}%")
            self.reliability_label.setStyleSheet(
                f"font-size: 16px; font-weight: bold; "
                f"color: {'green' if reliability >= 99 else 'orange' if reliability >= 95 else 'red'};"
            )
            
            self.response_label.setText(f"평균응답: {avg_response:.0f}ms")
            
            # 차트 업데이트
            test_id = data['test_id']
            self.reliability_history.append((test_id, reliability))
            
            if len(self.reliability_history) > 100:
                self.reliability_history.pop(0)
            
            x_data = [item[0] for item in self.reliability_history]
            y_data = [item[1] for item in self.reliability_history]
            self.reliability_curve.setData(x_data, y_data)
    
    def add_log(self, level, message):
        """로그 추가"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 레벨에 따른 색상
        colors = {
            'INFO': 'blue',
            'SUCCESS': 'green',
            'WARNING': 'orange',
            'ERROR': 'red'
        }
        
        color = colors.get(level, 'black')
        
        formatted_msg = f'<span style="color: {color};">[{timestamp}] [{level}] {message}</span>'
        self.log_text.append(formatted_msg)
        
        # 자동 스크롤
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def update_stats_table(self):
        """통계 테이블 업데이트"""
        if not self.comm_thread:
            return
        
        report = self.comm_thread.get_statistics()
        sensors = report.get('sensors', {})
        
        self.stats_table.setRowCount(len(sensors))
        
        for row, (sensor_name, sensor_data) in enumerate(sensors.items()):
            self.stats_table.setItem(row, 0, QTableWidgetItem(sensor_name))
            self.stats_table.setItem(row, 1, QTableWidgetItem(str(sensor_data['total'])))
            self.stats_table.setItem(row, 2, QTableWidgetItem(str(sensor_data['success'])))
            self.stats_table.setItem(row, 3, QTableWidgetItem(str(sensor_data['failure'])))
            self.stats_table.setItem(row, 4, QTableWidgetItem(f"{sensor_data['reliability']:.2f}"))
            self.stats_table.setItem(row, 5, QTableWidgetItem(f"{sensor_data['avg_response_time']:.2f}"))
    
    def generate_report(self):
        """Excel 리포트 생성"""
        if not self.comm_thread:
            QMessageBox.warning(self, "경고", "테스트를 먼저 실행하세요.")
            return
        
        try:
            self.add_log("INFO", "Excel 리포트 생성 중...")
            
            # 로그 파일 경로
            log_dir = Path(LOG_DIR)
            today = datetime.now().strftime("%Y%m%d")
            call_log_file = log_dir / f"call_log_{today}.csv"
            sensor_log_file = log_dir / f"sensor_data_{today}.csv"
            
            # 신뢰도 리포트
            reliability_report = self.comm_thread.get_statistics()
            
            # Excel 생성
            exporter = ExcelExporter(output_dir=OUTPUT_DIR)
            output_file = exporter.create_report(
                call_log_file,
                sensor_log_file,
                reliability_report
            )
            
            self.add_log("SUCCESS", f"리포트 생성 완료: {output_file.name}")
            
            QMessageBox.information(self, "완료", f"Excel 리포트가 생성되었습니다.\n{output_file}")
            
            # 파일 열기
            import os
            os.startfile(output_file)
            
        except Exception as e:
            self.add_log("ERROR", f"리포트 생성 실패: {e}")
            QMessageBox.critical(self, "오류", f"리포트 생성 실패:\n{e}")
    
    def closeEvent(self, event):
        """윈도우 닫기 이벤트"""
        if self.comm_thread and self.comm_thread.isRunning():
            reply = QMessageBox.question(
                self, '확인',
                '테스트가 진행 중입니다. 종료하시겠습니까?',
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.comm_thread.stop()
                self.comm_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


# =================================================================
# 메인 실행
# =================================================================
def main():
    app = QApplication(sys.argv)
    
    # 폰트 설정
    font = QFont("맑은 고딕", 10)
    app.setFont(font)
    
    # 메인 윈도우
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
