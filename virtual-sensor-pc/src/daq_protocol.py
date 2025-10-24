"""
=================================================================
파일명: daq_protocol.py
설명: DAQ 장치 통신 프로토콜 구현
작성일: 2025-10-24
=================================================================
PC와 DAQ 장치 간 통신 프로토콜을 정의하고 구현합니다.

프레임 구조:
[STX] [Length] [Serial No] [MSG Type] [Data] [CRC16] [ETX]
 1B     1B        1B          1B        N B    2B      1B

- STX: 0x02 (Start of Text)
- Length: Serial No + MSG Type + Data의 총 바이트 수
- Serial No: 시리얼 번호 (0~255)
- MSG Type: 메시지 타입 (센서 종류)
- Data: 센서별 데이터 (크기는 MSG Type에 따라 다름)
- CRC16: Modbus CRC16 (Length~Data에 대해 계산)
- ETX: 0x03 (End of Text)

MSG Type 정의:
0x01: 단상 전력량계 (10 bytes)
0x02: 3상3선 전력량계 (30 bytes)
0x03: 3상4선 전력량계 (32 bytes)
0x04: 유량 센서 (8 bytes)
0x05: 수도 계량기 (4 bytes)
0x06: CO2 센서 (2 bytes)
0x07: 온습도 센서 (4 bytes)
0x08: 일사량 센서 (2 bytes)
0x09: DC 모터 감시 (1 byte)
=================================================================
"""

import struct
from enum import IntEnum

# CRC16 모듈 import (상대/절대 경로 자동 처리)
try:
    from .crc16_modbus import calculate_crc16_modbus, verify_crc16
except ImportError:
    from crc16_modbus import calculate_crc16_modbus, verify_crc16


# =================================================================
# 메시지 타입 정의 (Enum)
# =================================================================
class MessageType(IntEnum):
    """
    DAQ 프로토콜에서 사용하는 메시지 타입 정의
    
    각 센서 종류마다 고유한 ID를 가지며, 이 ID에 따라 데이터 구조가 결정됩니다.
    """
    SINGLE_PHASE = 0x01      # 단상 전력량계
    THREE_PHASE_3W = 0x02    # 3상3선 전력량계
    THREE_PHASE_4W = 0x03    # 3상4선 전력량계
    FLOW_SENSOR = 0x04       # 유량 센서
    WATER_METER = 0x05       # 수도 계량기
    CO2_SENSOR = 0x06        # CO2 센서
    TEMP_HUMIDITY = 0x07     # 온습도 센서
    SOLAR_SENSOR = 0x08      # 일사량 센서
    DC_MOTOR = 0x09          # DC 모터 감시


# =================================================================
# DAQ 프로토콜 클래스
# =================================================================
class DAQProtocol:
    """
    DAQ 통신 프로토콜을 처리하는 클래스
    
    주요 기능:
    1. 프레임 생성 (create_frame)
    2. 프레임 파싱 (parse_frame)
    3. MSG Type 이름 변환 (get_msg_type_name)
    """
    
    # =================================================================
    # 프로토콜 상수 정의
    # =================================================================
    STX = 0x02  # Start of Text
    ETX = 0x03  # End of Text
    
    # MSG Type별 데이터 크기 정의 (바이트 단위)
    DATA_SIZE = {
        MessageType.SINGLE_PHASE: 10,      # 전압2+전류2+전력2+전력량4 = 10
        MessageType.THREE_PHASE_3W: 30,    # 전압6+전류6+전력6+전력량12 = 30
        MessageType.THREE_PHASE_4W: 32,    # 전압6+전류8+전력6+전력량12 = 32
        MessageType.FLOW_SENSOR: 8,        # 유량4+누적유량4 = 8
        MessageType.WATER_METER: 4,        # 사용량4 = 4
        MessageType.CO2_SENSOR: 2,         # CO2농도2 = 2
        MessageType.TEMP_HUMIDITY: 4,      # 온도2+습도2 = 4
        MessageType.SOLAR_SENSOR: 2,       # 일사량2 = 2
        MessageType.DC_MOTOR: 1            # 상태1 = 1
    }
    
    def __init__(self):
        """프로토콜 초기화"""
        pass
    
    def create_frame(self, msg_type, serial_no, data):
        """
        DAQ 프로토콜 프레임 생성
        
        전송할 센서 데이터를 DAQ 프로토콜 규격에 맞는 프레임으로 변환합니다.
        CRC16 체크섬을 자동으로 계산하여 추가합니다.
        
        프레임 생성 과정:
        1. MSG Type과 데이터 크기 검증
        2. 헤더 생성 [STX][Length][Serial No][MSG Type]
        3. CRC16 계산 대상 추출 [Length][Serial No][MSG Type][Data]
        4. CRC16 계산 및 추가
        5. ETX 추가하여 최종 프레임 완성
        
        Args:
            msg_type (int or MessageType): 메시지 타입 (0x01~0x09)
            serial_no (int): 시리얼 번호 (0~255)
            data (bytes): 센서 데이터 (MSG Type에 따라 크기가 다름)
        
        Returns:
            bytes: 완성된 프레임
            
        Raises:
            ValueError: 데이터 크기가 MSG Type에 맞지 않을 때
        
        Example:
            >>> protocol = DAQProtocol()
            >>> # 단상 전력량계: 전압 221.2V, 전류 12.34A, 전력 12.345kW, 전력량 12345kWh
            >>> data = struct.pack('>HHHI', 2212, 1234, 12345, 12345)
            >>> frame = protocol.create_frame(MessageType.SINGLE_PHASE, 0, data)
            >>> print(frame.hex(' ').upper())
            02 0C 00 01 08 A4 04 D2 30 39 00 00 30 39 E3 EF 03
        """
        # MSG Type을 int로 변환 (Enum이든 int든 처리)
        if isinstance(msg_type, MessageType):
            msg_type_int = msg_type.value
        else:
            msg_type_int = msg_type
        
        # =================================================================
        # 데이터 크기 검증
        # =================================================================
        expected_size = self.DATA_SIZE.get(msg_type_int)
        if expected_size and len(data) != expected_size:
            raise ValueError(
                f"MSG Type 0x{msg_type_int:02X}의 데이터 크기는 {expected_size} bytes여야 합니다. "
                f"(실제: {len(data)} bytes)"
            )
        
        # =================================================================
        # Length 계산
        # =================================================================
        # Length = Serial No(1) + MSG Type(1) + Data(N)
        length = 1 + 1 + len(data)
        
        # =================================================================
        # 프레임 생성
        # =================================================================
        # 1. 헤더 생성: [STX][Length][Serial No][MSG Type]
        header = struct.pack('BBBB', self.STX, length, serial_no, msg_type_int)
        
        # 2. CRC 계산 대상: [Length][Serial No][MSG Type][Data]
        crc_data = struct.pack('BBB', length, serial_no, msg_type_int) + data
        
        # 3. CRC16 계산 (Modbus)
        crc = calculate_crc16_modbus(crc_data)
        
        # 4. 전체 프레임 조립
        # [STX][Length][Serial No][MSG Type][Data][CRC16-Low][CRC16-High][ETX]
        frame = header + data + struct.pack('<H', crc) + struct.pack('B', self.ETX)
        
        return frame
    
    def parse_frame(self, frame):
        """
        수신한 프레임을 파싱하여 데이터 추출
        
        수신한 바이트 데이터에서 헤더, 데이터, CRC를 분리하고 검증합니다.
        
        파싱 과정:
        1. 프레임 최소 크기 확인 (7 bytes 이상)
        2. STX 확인 (0x02)
        3. ETX 확인 (0x03)
        4. Length 기반 프레임 크기 검증
        5. CRC16 검증
        6. 데이터 추출 및 반환
        
        Args:
            frame (bytes): 수신한 전체 프레임
        
        Returns:
            dict: 파싱 결과
                {
                    'valid': bool,          # 프레임 유효성
                    'serial_no': int,       # 시리얼 번호
                    'msg_type': int,        # 메시지 타입
                    'data': bytes,          # 센서 데이터
                    'error': str            # 에러 메시지 (valid=False일 때)
                }
        
        Example:
            >>> protocol = DAQProtocol()
            >>> frame = bytes.fromhex('02 0C 00 01 08A4 04D2 3039 00003039 E3EF 03')
            >>> result = protocol.parse_frame(frame)
            >>> print(f"유효성: {result['valid']}")
            >>> print(f"MSG Type: 0x{result['msg_type']:02X}")
            >>> print(f"데이터: {result['data'].hex(' ').upper()}")
        """
        # 파싱 결과를 담을 딕셔너리 초기화
        result = {
            'valid': False,
            'serial_no': 0,
            'msg_type': 0,
            'data': b'',
            'error': ''
        }
        
        # =================================================================
        # 1. 프레임 최소 크기 확인
        # =================================================================
        # 최소 프레임 = STX(1) + Length(1) + Serial(1) + MSG(1) + CRC(2) + ETX(1) = 7 bytes
        if len(frame) < 7:
            result['error'] = f"프레임이 너무 작습니다 (최소 7 bytes, 실제 {len(frame)} bytes)"
            return result
        
        # =================================================================
        # 2. STX 확인 (프레임 시작)
        # =================================================================
        if frame[0] != self.STX:
            result['error'] = f"STX가 잘못되었습니다 (예상: 0x02, 실제: 0x{frame[0]:02X})"
            return result
        
        # =================================================================
        # 3. ETX 확인 (프레임 끝)
        # =================================================================
        if frame[-1] != self.ETX:
            result['error'] = f"ETX가 잘못되었습니다 (예상: 0x03, 실제: 0x{frame[-1]:02X})"
            return result
        
        # =================================================================
        # 4. 헤더 파싱
        # =================================================================
        length = frame[1]      # Payload 크기 (Serial No + MSG Type + Data)
        serial_no = frame[2]   # 시리얼 번호
        msg_type = frame[3]    # 메시지 타입
        
        # =================================================================
        # 5. 프레임 크기 검증
        # =================================================================
        # 예상 크기 = STX(1) + Length(1) + Payload(length) + CRC(2) + ETX(1)
        expected_frame_size = 1 + 1 + length + 2 + 1
        if len(frame) != expected_frame_size:
            result['error'] = (
                f"프레임 크기 불일치 "
                f"(예상: {expected_frame_size} bytes, 실제: {len(frame)} bytes)"
            )
            return result
        
        # =================================================================
        # 6. CRC16 검증
        # =================================================================
        # CRC 계산 대상: [Length][Serial No][MSG Type][Data]
        crc_data = frame[1:-3]  # STX 제외, CRC+ETX 제외
        
        # 수신한 CRC (Little-endian)
        received_crc = struct.unpack('<H', frame[-3:-1])[0]
        
        # CRC 재계산
        calculated_crc = calculate_crc16_modbus(crc_data)
        
        # CRC 비교
        if received_crc != calculated_crc:
            result['error'] = (
                f"CRC 불일치 "
                f"(수신: 0x{received_crc:04X}, 계산: 0x{calculated_crc:04X})"
            )
            return result
        
        # =================================================================
        # 7. 데이터 추출
        # =================================================================
        # Data 위치: [STX][Length][Serial][MSG Type][Data...][CRC][ETX]
        #              0     1       2       3        4~-4     -3~-1
        data = frame[4:-3]
        
        # =================================================================
        # 8. 결과 반환
        # =================================================================
        result['valid'] = True
        result['serial_no'] = serial_no
        result['msg_type'] = msg_type
        result['data'] = data
        
        return result
    
    def get_msg_type_name(self, msg_type):
        """
        MSG Type 코드를 한글 이름으로 변환
        
        Args:
            msg_type (int): MSG Type 코드 (0x01~0x09)
        
        Returns:
            str: MSG Type 이름 (예: "단상 전력량계")
        
        Example:
            >>> protocol = DAQProtocol()
            >>> name = protocol.get_msg_type_name(0x01)
            >>> print(name)
            단상 전력량계
        """
        msg_type_names = {
            MessageType.SINGLE_PHASE: "단상 전력량계",
            MessageType.THREE_PHASE_3W: "3상3선 전력량계",
            MessageType.THREE_PHASE_4W: "3상4선 전력량계",
            MessageType.FLOW_SENSOR: "유량 센서",
            MessageType.WATER_METER: "수도 계량기",
            MessageType.CO2_SENSOR: "CO2 센서",
            MessageType.TEMP_HUMIDITY: "온습도 센서",
            MessageType.SOLAR_SENSOR: "일사량 센서",
            MessageType.DC_MOTOR: "DC 모터 감시"
        }
        
        return msg_type_names.get(msg_type, f"알 수 없음 (0x{msg_type:02X})")


# =================================================================
# 테스트 코드
# =================================================================
if __name__ == "__main__":
    print("="*70)
    print("DAQ 프로토콜 테스트")
    print("="*70)
    
    protocol = DAQProtocol()
    
    # =================================================================
    # 테스트 1: 단상 전력량계 프레임 생성
    # =================================================================
    print("\n[테스트 1] 단상 전력량계 프레임 생성")
    print("-"*70)
    
    # 센서 데이터: 전압 221.2V, 전류 12.34A, 전력 12.345kW, 전력량 12345kWh
    voltage = 2212    # 221.2 * 10
    current = 1234    # 12.34 * 100
    power = 12345     # 12.345 * 1000
    energy = 12345    # 12345 kWh
    
    data = struct.pack('>HHHI', voltage, current, power, energy)
    print(f"센서 데이터:")
    print(f"  전압: {voltage/10:.1f}V")
    print(f"  전류: {current/100:.2f}A")
    print(f"  전력: {power/1000:.3f}kW")
    print(f"  전력량: {energy}kWh")
    print(f"데이터 (HEX): {data.hex(' ').upper()}")
    
    frame = protocol.create_frame(MessageType.SINGLE_PHASE, 0, data)
    print(f"\n생성된 프레임:")
    print(f"  HEX: {frame.hex(' ').upper()}")
    print(f"  크기: {len(frame)} bytes")
    
    # =================================================================
    # 테스트 2: 프레임 파싱
    # =================================================================
    print("\n[테스트 2] 프레임 파싱")
    print("-"*70)
    
    result = protocol.parse_frame(frame)
    print(f"파싱 결과:")
    print(f"  유효성: {'✓ 유효' if result['valid'] else '✗ 유효하지 않음'}")
    print(f"  Serial No: {result['serial_no']}")
    print(f"  MSG Type: 0x{result['msg_type']:02X} ({protocol.get_msg_type_name(result['msg_type'])})")
    print(f"  데이터: {result['data'].hex(' ').upper()}")
    
    if result['error']:
        print(f"  에러: {result['error']}")
    
    # =================================================================
    # 테스트 3: 온습도 센서
    # =================================================================
    print("\n[테스트 3] 온습도 센서 프레임")
    print("-"*70)
    
    # 온도: -12.3℃, 습도: 99.9%
    temperature = -123  # -12.3 * 10
    humidity = 999      # 99.9 * 10
    
    data = struct.pack('>hH', temperature, humidity)
    print(f"센서 데이터:")
    print(f"  온도: {temperature/10:.1f}℃")
    print(f"  습도: {humidity/10:.1f}%")
    
    frame = protocol.create_frame(MessageType.TEMP_HUMIDITY, 5, data)
    print(f"\n생성된 프레임: {frame.hex(' ').upper()}")
    
    result = protocol.parse_frame(frame)
    print(f"파싱 유효성: {'✓' if result['valid'] else '✗'}")
    
    # =================================================================
    # 테스트 4: 잘못된 CRC
    # =================================================================
    print("\n[테스트 4] 잘못된 CRC 검출")
    print("-"*70)
    
    bad_frame = bytearray(frame)
    bad_frame[-3] = 0x00  # CRC 변조
    
    result = protocol.parse_frame(bytes(bad_frame))
    print(f"파싱 유효성: {'✗ (예상된 결과)' if not result['valid'] else '✓ (예상 밖)'}")
    print(f"에러 메시지: {result['error']}")
    
    # =================================================================
    # 종료
    # =================================================================
    print("\n" + "="*70)
    print("✓ 모든 테스트 완료")
    print("="*70)
