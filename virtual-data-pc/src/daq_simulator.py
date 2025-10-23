"""
=================================================================
파일명: virtual-sensor-pc/src/daq_simulator.py
설명: DAQ 장치 시뮬레이터
작성자: 개발팀
작성일: 2025-10-23
=================================================================
실제 DAQ 장치의 동작을 시뮬레이션합니다.
PC로부터 요청을 받으면 가상 센서 데이터를 생성하여 응답합니다.
=================================================================
"""

import struct
import random
from datetime import datetime
from daq_protocol import DAQProtocol, MessageType
from data_parser import DataParser

class DAQSimulator:
    """
    DAQ 장치 시뮬레이터 클래스
    """
    
    def __init__(self, sensor_ranges):
        """
        시뮬레이터 초기화
        
        Args:
            sensor_ranges: 센서 데이터 범위 (config의 SENSOR_DATA_RANGES)
        """
        self.protocol = DAQProtocol()
        self.parser = DataParser()
        self.sensor_ranges = sensor_ranges
        self.serial_no = 0
        
        print("[DAQSimulator] 초기화 완료")
    
    def generate_single_phase_data(self):
        """
        단상 전력량계 데이터 생성
        
        Returns:
            bytes: 단상 전력량계 데이터 (10 bytes)
        """
        ranges = self.sensor_ranges['single_phase']
        
        voltage = random.uniform(ranges['voltage']['min'], ranges['voltage']['max'])
        current = random.uniform(ranges['current']['min'], ranges['current']['max'])
        power = random.uniform(ranges['power']['min'], ranges['power']['max'])
        energy = random.randint(ranges['energy']['min'], ranges['energy']['max'])
        
        # 정수로 변환 (소수점 처리)
        voltage_raw = int(voltage * 10)
        current_raw = int(current * 100)
        power_raw = int(power * 1000)
        
        data = struct.pack('>HHHI', voltage_raw, current_raw, power_raw, energy)
        
        return data
    
    def generate_temp_humidity_data(self):
        """
        온습도 센서 데이터 생성
        
        Returns:
            bytes: 온습도 데이터 (4 bytes)
        """
        ranges = self.sensor_ranges['temp_humidity']
        
        temperature = random.uniform(ranges['temperature']['min'], ranges['temperature']['max'])
        humidity = random.uniform(ranges['humidity']['min'], ranges['humidity']['max'])
        
        # 정수로 변환
        temp_raw = int(temperature * 10)
        humidity_raw = int(humidity * 10)
        
        data = struct.pack('>hH', temp_raw, humidity_raw)
        
        return data
    
    def generate_co2_data(self):
        """
        CO2 센서 데이터 생성
        
        Returns:
            bytes: CO2 데이터 (2 bytes)
        """
        ranges = self.sensor_ranges['co2']
        
        co2_ppm = random.randint(ranges['ppm']['min'], ranges['ppm']['max'])
        
        data = struct.pack('>H', co2_ppm)
        
        return data
    
    def generate_sensor_data(self, msg_type):
        """
        MSG Type에 따라 센서 데이터 생성
        
        Args:
            msg_type: MessageType enum 또는 int
        
        Returns:
            bytes: 생성된 센서 데이터
        """
        if isinstance(msg_type, MessageType):
            msg_type = msg_type.value
        
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
            return b''
    
    def create_response_frame(self, msg_type):
        """
        응답 프레임 생성
        
        Args:
            msg_type: MessageType enum 또는 int
        
        Returns:
            bytes: 완성된 응답 프레임
        """
        # 센서 데이터 생성
        data = self.generate_sensor_data(msg_type)
        
        if not data:
            return None
        
        # 프레임 생성
        frame = self.protocol.create_frame(msg_type, self.serial_no, data)
        
        # Serial No 증가
        self.serial_no = (self.serial_no + 1) % 256
        
        return frame
    
    def get_sensor_reading(self, msg_type):
        """
        센서 데이터를 생성하고 파싱하여 반환 (로깅용)
        
        Args:
            msg_type: MessageType enum 또는 int
        
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
    print("DAQ 시뮬레이터 테스트\n")
    
    # Config에서 센서 범위 가져오기 (여기서는 직접 정의)
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
    parser = DataParser()
    
    # 테스트 1: 단상 전력량계
    print("=" * 60)
    print("테스트 1: 단상 전력량계 프레임 생성")
    print("=" * 60)
    
    frame = simulator.create_response_frame(MessageType.SINGLE_PHASE)
    print(f"생성된 프레임: {frame.hex(' ').upper()}")
    
    # 프레임 파싱
    protocol = DAQProtocol()
    result = protocol.parse_frame(frame)
    
    if result['valid']:
        parsed = parser.parse(result['msg_type'], result['data'])
        print(f"\n파싱 결과:")
        print(f"  전압: {parsed['voltage']['value']:.1f} {parsed['voltage']['unit']}")
        print(f"  전류: {parsed['current']['value']:.2f} {parsed['current']['unit']}")
        print(f"  전력: {parsed['power']['value']:.3f} {parsed['power']['unit']}")
        print(f"  전력량: {parsed['energy']['value']} {parsed['energy']['unit']}")
    
    # 테스트 2: 온습도 센서
    print("\n" + "=" * 60)
    print("테스트 2: 온습도 센서 프레임 생성")
    print("=" * 60)
    
    for i in range(3):
        frame = simulator.create_response_frame(MessageType.TEMP_HUMIDITY)
        result = protocol.parse_frame(frame)
        
        if result['valid']:
            parsed = parser.parse(result['msg_type'], result['data'])
            print(f"  [{i+1}] 온도: {parsed['temperature']['value']:.1f}℃, "
                  f"습도: {parsed['humidity']['value']:.1f}%")
    
    # 테스트 3: CO2 센서
    print("\n" + "=" * 60)
    print("테스트 3: CO2 센서 프레임 생성")
    print("=" * 60)
    
    for i in range(3):
        frame = simulator.create_response_frame(MessageType.CO2_SENSOR)
        result = protocol.parse_frame(frame)
        
        if result['valid']:
            parsed = parser.parse(result['msg_type'], result['data'])
            print(f"  [{i+1}] CO2: {parsed['co2']['value']} {parsed['co2']['unit']}")
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)
