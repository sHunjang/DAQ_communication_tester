"""
=================================================================
파일명: daq_simulator.py
설명: DAQ 장치 시뮬레이터
작성일: 2025-10-24
=================================================================
실제 DAQ 장치의 동작을 시뮬레이션합니다.
랜덤한 센서 데이터를 생성하여 프로토콜 프레임으로 변환합니다.

주요 기능:
1. 센서 데이터 랜덤 생성
2. DAQ 프로토콜 프레임 생성
3. 시리얼 번호 자동 증가

지원 센서:
- 단상 전력량계
- 온습도 센서
- CO2 센서
=================================================================
"""

import struct
import random
from datetime import datetime

# 모듈 import (상대/절대 경로 자동 처리)
try:
    from .daq_protocol import DAQProtocol, MessageType
    from .data_parser import DataParser
except ImportError:
    from daq_protocol import DAQProtocol, MessageType
    from data_parser import DataParser


class DAQSimulator:
    """
    DAQ 장치를 시뮬레이션하는 클래스
    
    설정된 범위 내에서 랜덤한 센서 값을 생성하고,
    DAQ 프로토콜에 맞는 프레임으로 변환합니다.
    """
    
    def __init__(self, sensor_ranges):
        """
        시뮬레이터 초기화
        
        Args:
            sensor_ranges (dict): 각 센서의 최소/최대 값 범위
                {
                    'single_phase': {
                        'voltage': {'min': 210.0, 'max': 230.0},
                        ...
                    },
                    ...
                }
        """
        self.protocol = DAQProtocol()
        self.parser = DataParser()
        self.sensor_ranges = sensor_ranges
        self.serial_no = 0  # 시리얼 번호 (0~255 순환)
        
        print("[DAQSimulator] 초기화 완료")
    
    def generate_single_phase_data(self):
        """
        단상 전력량계 센서 데이터 생성
        
        설정된 범위 내에서 전압, 전류, 전력, 전력량을 랜덤 생성합니다.
        
        Returns:
            bytes: 10 bytes 센서 데이터
        """
        ranges = self.sensor_ranges['single_phase']
        
        # 랜덤 값 생성
        voltage = random.uniform(ranges['voltage']['min'], ranges['voltage']['max'])
        current = random.uniform(ranges['current']['min'], ranges['current']['max'])
        power = random.uniform(ranges['power']['min'], ranges['power']['max'])
        energy = random.randint(ranges['energy']['min'], ranges['energy']['max'])
        
        # 정수로 변환 (소수점 처리)
        voltage_raw = int(voltage * 10)    # 221.2V → 2212
        current_raw = int(current * 100)   # 12.34A → 1234
        power_raw = int(power * 1000)      # 12.345kW → 12345
        
        # 바이너리 패킹 (Big-endian)
        data = struct.pack('>HHHI', voltage_raw, current_raw, power_raw, energy)
        
        return data
    
    def generate_temp_humidity_data(self):
        """
        온습도 센서 데이터 생성
        
        온도는 음수도 가능 (signed short 사용)
        
        Returns:
            bytes: 4 bytes 센서 데이터
        """
        ranges = self.sensor_ranges['temp_humidity']
        
        temperature = random.uniform(ranges['temperature']['min'], ranges['temperature']['max'])
        humidity = random.uniform(ranges['humidity']['min'], ranges['humidity']['max'])
        
        # 정수로 변환
        temp_raw = int(temperature * 10)      # 25.3℃ → 253
        humidity_raw = int(humidity * 10)     # 65.5% → 655
        
        # 바이너리 패킹 (온도는 signed, 습도는 unsigned)
        data = struct.pack('>hH', temp_raw, humidity_raw)
        
        return data
    
    def generate_co2_data(self):
        """
        CO2 센서 데이터 생성
        
        Returns:
            bytes: 2 bytes 센서 데이터
        """
        ranges = self.sensor_ranges['co2']
        
        co2_ppm = random.randint(ranges['ppm']['min'], ranges['ppm']['max'])
        
        data = struct.pack('>H', co2_ppm)
        
        return data
    
    def generate_sensor_data(self, msg_type):
        """
        MSG Type에 따라 센서 데이터 생성
        
        Args:
            msg_type (int or MessageType): 메시지 타입
        
        Returns:
            bytes: 생성된 센서 데이터 (MSG Type에 따라 크기 다름)
        """
        if isinstance(msg_type, MessageType):
            msg_type = msg_type.value
        
        # MSG Type별 데이터 생성 함수 매핑
        generators = {
            MessageType.SINGLE_PHASE: self.generate_single_phase_data,
            MessageType.TEMP_HUMIDITY: self.generate_temp_humidity_data,
            MessageType.CO2_SENSOR: self.generate_co2_data
        }
        
        generator = generators.get(msg_type)
        if generator:
            return generator()
        else:
            # 지원하지 않는 센서 타입
            print(f"[DAQSimulator] 경고: MSG Type 0x{msg_type:02X}는 지원하지 않습니다")
            return b''
    
    def create_response_frame(self, msg_type):
        """
        응답 프레임 생성
        
        센서 데이터를 생성하고 DAQ 프로토콜 프레임으로 변환합니다.
        시리얼 번호는 자동으로 증가합니다.
        
        Args:
            msg_type (int or MessageType): 메시지 타입
        
        Returns:
            bytes: 완성된 응답 프레임 (STX~ETX)
        """
        # 센서 데이터 생성
        data = self.generate_sensor_data(msg_type)
        
        if not data:
            return None
        
        # DAQ 프로토콜 프레임 생성
        frame = self.protocol.create_frame(msg_type, self.serial_no, data)
        
        # 시리얼 번호 증가 (0~255 순환)
        self.serial_no = (self.serial_no + 1) % 256
        
        return frame
    
    def get_sensor_reading(self, msg_type):
        """
        센서 데이터를 생성하고 파싱하여 반환 (로깅용)
        
        Args:
            msg_type (int or MessageType): 메시지 타입
        
        Returns:
            dict: 파싱된 센서 데이터
        """
        data = self.generate_sensor_data(msg_type)
        if data:
            return self.parser.parse(msg_type, data)
        return None


# =================================================================
# 테스트 코드
# =================================================================
if __name__ == "__main__":
    print("="*70)
    print("DAQ 시뮬레이터 테스트")
    print("="*70)
    
    # 센서 범위 설정
    sensor_ranges = {
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
        'co2': {
            'ppm': {'min': 400, 'max': 1500}
        }
    }
    
    simulator = DAQSimulator(sensor_ranges)
    protocol = DAQProtocol()
    parser = DataParser()
    
    # 테스트 1: 단상 전력량계
    print("\n[테스트 1] 단상 전력량계 3회 생성")
    print("-"*70)
    
    for i in range(3):
        frame = simulator.create_response_frame(MessageType.SINGLE_PHASE)
        print(f"\n프레임 #{i+1}: {frame.hex(' ').upper()}")
        
        # 파싱
        result = protocol.parse_frame(frame)
        if result['valid']:
            parsed = parser.parse(result['msg_type'], result['data'])
            print(f"  전압: {parsed['voltage']['value']:.1f}V")
            print(f"  전류: {parsed['current']['value']:.2f}A")
            print(f"  전력: {parsed['power']['value']:.3f}kW")
    
    # 테스트 2: 온습도 센서
    print("\n[테스트 2] 온습도 센서 3회 생성")
    print("-"*70)
    
    for i in range(3):
        frame = simulator.create_response_frame(MessageType.TEMP_HUMIDITY)
        result = protocol.parse_frame(frame)
        
        if result['valid']:
            parsed = parser.parse(result['msg_type'], result['data'])
            print(f"  [{i+1}] 온도: {parsed['temperature']['value']:.1f}℃, "
                  f"습도: {parsed['humidity']['value']:.1f}%")
    
    # 테스트 3: CO2 센서
    print("\n[테스트 3] CO2 센서 3회 생성")
    print("-"*70)
    
    for i in range(3):
        frame = simulator.create_response_frame(MessageType.CO2_SENSOR)
        result = protocol.parse_frame(frame)
        
        if result['valid']:
            parsed = parser.parse(result['msg_type'], result['data'])
            print(f"  [{i+1}] CO2: {parsed['co2']['value']} ppm")
    
    print("\n" + "="*70)
    print("✓ 모든 테스트 완료")
    print("="*70)
