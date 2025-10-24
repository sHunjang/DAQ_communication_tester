"""
=================================================================
파일명: sensor_simulator.py
설명: 순수 센서 시뮬레이터 (v3)
작성일: 2025-10-24
=================================================================
DAQ로부터 요청을 받으면 Raw 센서 데이터만 생성합니다.
프로토콜 프레임 생성은 DAQ가 담당합니다.
"""

import struct
import random
from datetime import datetime


class SensorSimulator:
    """
    순수 센서 데이터 생성기
    
    DAQ 프로토콜을 모르고, Raw 데이터만 생성합니다.
    """
    
    def __init__(self, sensor_ranges):
        self.ranges = sensor_ranges
        print(f"[Sensor] 센서 시뮬레이터 초기화")
    
    def generate_sensor_data(self, msg_type):
        """
        MSG Type에 따라 Raw 센서 데이터 생성
        
        Args:
            msg_type (int): 센서 타입 (0x01, 0x07, 0x06)
        
        Returns:
            bytes: Raw 센서 데이터
        """
        if msg_type == 0x01:
            return self._generate_single_phase()
        elif msg_type == 0x07:
            return self._generate_temp_humidity()
        elif msg_type == 0x06:
            return self._generate_co2()
        else:
            return b''
    
    def _generate_single_phase(self):
        """단상 전력량계 데이터 (10 bytes)"""
        ranges = self.ranges[0x01]
        
        voltage = random.uniform(ranges['voltage']['min'], ranges['voltage']['max'])
        current = random.uniform(ranges['current']['min'], ranges['current']['max'])
        power = random.uniform(ranges['power']['min'], ranges['power']['max'])
        energy = random.randint(ranges['energy']['min'], ranges['energy']['max'])
        
        # 정수로 변환
        voltage_raw = int(voltage * 10)
        current_raw = int(current * 100)
        power_raw = int(power * 1000)
        
        # Big-endian 패킹
        data = struct.pack('>HHHI', voltage_raw, current_raw, power_raw, energy)
        
        print(f"[Sensor] 단상: {voltage:.1f}V, {current:.2f}A, {power:.3f}kW")
        return data
    
    def _generate_temp_humidity(self):
        """온습도 센서 데이터 (4 bytes)"""
        ranges = self.ranges[0x07]
        
        temperature = random.uniform(ranges['temperature']['min'], ranges['temperature']['max'])
        humidity = random.uniform(ranges['humidity']['min'], ranges['humidity']['max'])
        
        temp_raw = int(temperature * 10)
        humidity_raw = int(humidity * 10)
        
        data = struct.pack('>hH', temp_raw, humidity_raw)
        
        print(f"[Sensor] 온습도: {temperature:.1f}℃, {humidity:.1f}%")
        return data
    
    def _generate_co2(self):
        """CO2 센서 데이터 (2 bytes)"""
        ranges = self.ranges[0x06]
        
        co2_ppm = random.randint(ranges['ppm']['min'], ranges['ppm']['max'])
        
        data = struct.pack('>H', co2_ppm)
        
        print(f"[Sensor] CO2: {co2_ppm} ppm")
        return data
