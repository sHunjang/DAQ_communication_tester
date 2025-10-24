"""DAQ 통신 PC 설정"""

# 실행 모드
USE_MOCK_SERIAL = True  # True: Mock, False: 실제 RS232

# 통신 설정
RS232_PORT = 'COM3'
BAUDRATE = 115200
BYTESIZE = 8
PARITY = 'N'
STOPBITS = 1
TIMEOUT = 5

# 테스트 설정
INTER_REQUEST_DELAY = 1.0
TARGET_RELIABILITY = 99.0

# 경로 설정
LOG_DIR = 'logs'
OUTPUT_DIR = 'output'

# 시뮬레이션할 센서
SIMULATION_SENSORS = [0x01, 0x07, 0x06]  # 단상, 온습도, CO2
