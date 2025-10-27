"""
=================================================================
파일명: daq_relay.py
설명: DAQ 중개 로직 (v3)
작성일: 2025-10-24
=================================================================
- 통신 PC의 요청을 받아서 센서 PC로 전달
- 센서 PC의 응답을 DAQ 프로토콜로 변환하여 통신 PC에 전달

중개 프로세스:
1. 통신 PC로부터 요청 수신 (1 byte: MSG Type)
2. 센서 PC로 요청 전달 (2 bytes: MSG Type + Device ID)
3. 센서 PC로부터 Raw 데이터 수신
4. DAQ 프로토콜 프레임 생성 (STX, CRC, ETX 추가)
5. 통신 PC로 응답 전송
=================================================================
"""

import struct
import time
from datetime import datetime


class DAQRelay:
    """
    DAQ 중개자 클래스
    
    양쪽 통신을 중개하고 프로토콜을 변환
    """
    
    # DAQ 프로토콜 상수
    STX = 0x02
    ETX = 0x03
    
    # MSG Type별 데이터 크기 (센서 PC로부터 받을 크기)
    SENSOR_DATA_SIZE = {
        0x01: 10,  # 단상 전력량계
        0x07: 4,   # 온습도 센서
        0x06: 2    # CO2 센서
    }
    
    def __init__(self):
        self.serial_no = 0  # 시리얼 번호 (0~255 순환)
        self.relay_count = 0
        
        print("[DAQ] 중개 장치 초기화")
    
    def relay_request(self, rs232_ser, rs485_ser, msg_type):
        """
        요청 중개 처리
        
        Args:
            rs232_ser: RS232 시리얼 객체 (통신 PC)
            rs485_ser: RS485 시리얼 객체 (센서 PC)
            msg_type (int): 메시지 타입
        
        Returns:
            bool: 성공 여부
        """
        self.relay_count += 1
        
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"\n[{timestamp}] 중개 #{self.relay_count}")
        print(f"← 통신 PC: MSG Type 0x{msg_type:02X}")
        
        # 1. 센서 PC로 요청 전송 (MSG Type + Device ID)
        device_id = 0x01  # 임시 Device ID
        sensor_request = bytes([msg_type, device_id])
        
        rs485_ser.write(sensor_request)
        print(f"→ 센서 PC: 요청 전송 (2 bytes)")
        
        # 2. 센서 PC로부터 응답 수신
        expected_size = self.SENSOR_DATA_SIZE.get(msg_type, 0)
        
        if expected_size == 0:
            print(f"✗ 지원하지 않는 MSG Type")
            return False
        
        # 응답 대기 (최대 2초)
        start_time = time.time()
        sensor_data = bytearray()
        
        while len(sensor_data) < expected_size:
            if time.time() - start_time > 2:
                print(f"✗ 센서 PC 타임아웃")
                return False
            
            if rs485_ser.in_waiting > 0:
                sensor_data.extend(rs485_ser.read(rs485_ser.in_waiting))
            else:
                time.sleep(0.01)
        
        # 필요한 크기만큼만 자르기
        sensor_data = bytes(sensor_data[:expected_size])
        
        print(f"← 센서 PC: {len(sensor_data)} bytes 수신")
        print(f"   Raw 데이터: {sensor_data.hex(' ').upper()}")
        
        # 3. DAQ 프로토콜 프레임 생성
        frame = self._create_protocol_frame(msg_type, sensor_data)
        
        print(f"→ 통신 PC: {len(frame)} bytes 전송")
        print(f"   프레임: {frame.hex(' ').upper()}")
        
        # 4. 통신 PC로 전송
        rs232_ser.write(frame)
        
        # 5. 시리얼 번호 증가
        self.serial_no = (self.serial_no + 1) % 256
        
        return True
    
    def _create_protocol_frame(self, msg_type, sensor_data):
        """
        DAQ 프로토콜 프레임 생성
        
        프레임 구조:
        [STX][Length][Serial No][MSG Type][Data][CRC16-Low][CRC16-High][ETX]
        
        Args:
            msg_type (int): 메시지 타입
            sensor_data (bytes): 센서 Raw 데이터
        
        Returns:
            bytes: 완성된 프레임
        """
        # Length 계산 (Serial No + MSG Type + Data)
        length = 1 + 1 + len(sensor_data)
        
        # CRC 계산 대상 생성
        crc_data = struct.pack('BBB', length, self.serial_no, msg_type) + sensor_data
        
        # CRC16 계산
        crc = self._calculate_crc16_modbus(crc_data)
        
        # 프레임 조립
        frame = (
            struct.pack('B', self.STX) +
            struct.pack('BBB', length, self.serial_no, msg_type) +
            sensor_data +
            struct.pack('<H', crc) +  # Little-endian
            struct.pack('B', self.ETX)
        )
        
        return frame
    
    def _calculate_crc16_modbus(self, data):
        """
        Modbus CRC16 계산
        
        Args:
            data (bytes): CRC를 계산할 데이터
        
        Returns:
            int: CRC16 값
        """
        crc = 0xFFFF
        
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        
        return crc
    
    def get_statistics(self):
        """통계 정보 반환"""
        return {
            'total_relays': self.relay_count,
            'current_serial': self.serial_no
        }
