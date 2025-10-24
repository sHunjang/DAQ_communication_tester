"""가상 센서 PC 설정"""

USE_MOCK_SERIAL = True
RS232_PORT = 'COM4'
BAUDRATE = 115200
BYTESIZE = 8
PARITY = 'N'
STOPBITS = 1
TIMEOUT = 1
LOG_DIR = 'logs'

SENSOR_DATA_RANGES = {
    'single_phase': {
        'voltage': {'min': 210.0, 'max': 230.0},
        'current': {'min': 5.0, 'max': 20.0},
        'power': {'min': 1.0, 'max': 5.0},
        'energy': {'min': 0, 'max': 99999}
    },
    'temp_humidity': {
        'temperature': {'min': 15.0, 'max': 35.0},
        'humidity': {'min': 30.0, 'max': 80.0}
    },
    'co2': {'ppm': {'min': 400, 'max': 1500}}
}

SIMULATION_SENSORS = [0x01, 0x07, 0x06]
