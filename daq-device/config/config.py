"""
=================================================================
DAQ 장치 설정 (v3)
=================================================================
통신 PC와 센서 PC 사이의 중개자 역할
"""

# RS232 통신 설정 (통신 PC와 연결)
RS232_PORT = 'COM4'
RS232_BAUDRATE = 115200

# RS485 통신 설정 (센서 PC와 연결)
RS485_PORT = 'COM5'
RS485_BAUDRATE = 9600

# 타임아웃
RS232_TIMEOUT = 5
RS485_TIMEOUT = 2

# 로그 설정
LOG_DIR = 'logs'
LOG_LEVEL = 'DEBUG'  # DEBUG, INFO, WARNING, ERROR
