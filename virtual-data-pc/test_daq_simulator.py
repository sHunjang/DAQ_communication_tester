"""
=================================================================
파일명: virtual-sensor-pc/src/daq_simulator.py
설명: DAQ 장치 시뮬레이터
작성자: 개발팀
작성일: 2025-10-23
=================================================================
"""

import struct
import random
from datetime import datetime


from src.daq_protocol import DAQProtocol, MessageType
from src.data_parser import DataParser

class DAQSimulator:
    """DAQ 장치 시뮬레이터 클래스"""
    
    def __init__(self, sensor_ranges):
        """시뮬레이터 초기화"""
        self.protocol = DAQProtocol()
        self.parser = DataParser()
        self.sensor_ranges = sensor_ranges
        self.serial_no = 0
        print("[DAQSimulator] 초기화 완료")
    
    def generate_single_phase_data(self):
        """단상 전력량계 데이터 생성"""
        ranges = self.sensor_ranges['single_phase']
        
        voltage = random.uniform(ranges['voltage']['min'], ranges['voltage']['max'])
        current = random.uniform(ranges['current']['min'], ranges['current']['max'])
        power = random.uniform(ranges['power']['min'], ranges['power']['max'])
        energy = random.randint(ranges['energy']['min'], ranges['energy']['max'])
        
        voltage_raw = int(voltage * 10)
        current_raw = int(current * 100)
        power_raw = int(power * 1000)
        
        data = struct.pack('>HHHI', voltage_raw, current_raw, power_raw, energy)
        return data
    
    def generate_temp_humidity_data(self):
        """온습도 센서 데이터 생성"""
        ranges = self.sensor_ranges['temp_humidity']
        
        temperature = random.uniform(ranges['temperature']['min'], ranges['temperature']['max'])
        humidity = random.uniform(ranges['humidity']['min'], ranges['humidity']['max'])
        
        temp_raw = int(temperature * 10)
        humidity_raw = int(humidity * 10)
        
        data = struct.pack('>hH', temp_raw, humidity_raw)
        return data
    
    def generate_co2_data(self):
        """CO2 센서 데이터 생성"""
        ranges = self.sensor_ranges['co2']
        co2_ppm = random.randint(ranges['ppm']['min'], ranges['ppm']['max'])
        data = struct.pack('>H', co2_ppm)
        return data
    
    def generate_sensor_data(self, msg_type):
        """MSG Type에 따라 센서 데이터 생성"""
        if isinstance(msg_type, MessageType):
            msg_type = msg_type.value
        
        generators = {
            MessageType.SINGLE_PHASE: self.generate_single_phase_data,
            MessageType.TEMP_HUMIDITY: self.generate_temp_humidity_data,
            MessageType.CO2_SENSOR: self.generate_co2_data
        }
        
        generator = generators.get(msg_type)
        return generator() if generator else b''
    
    def create_response_frame(self, msg_type):
        """응답 프레임 생성"""
        data = self.generate_sensor_data(msg_type)
        if not data:
            return None
        
        frame = self.protocol.create_frame(msg_type, self.serial_no, data)
        self.serial_no = (self.serial_no + 1) % 256
        return frame
    
    def get_sensor_reading(self, msg_type):
        """센서 데이터를 생성하고 파싱하여 반환"""
        data = self.generate_sensor_data(msg_type)
        return self.parser.parse(msg_type, data) if data else None
