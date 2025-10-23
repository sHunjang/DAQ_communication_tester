"""
=================================================================
파일명: communication-pc/src/daq_protocol.py
설명: DAQ 통신 프로토콜 구현
작성자: 개발팀
작성일: 2025-10-23
=================================================================
DAQ 장치와 PC 간 통신 프로토콜을 구현합니다.
프레임 구조: [STX][Length][Serial No][MSG Type][Data][CRC16][ETX]
=================================================================
"""

import struct
from enum import IntEnum
from crc16_modbus import calculate_crc16_modbus, verify_crc16

class MessageType(IntEnum):
    """DAQ 메시지 타입 정의"""
    SINGLE_PHASE = 0x01      # 단상 전력량계 (12 bytes)
    THREE_PHASE_3W = 0x02    # 3상3선 전력량계 (32 bytes)
    THREE_PHASE_4W = 0x03    # 3상4선 전력량계 (34 bytes)
    FLOW_SENSOR = 0x04       # 유량 센서 (10 bytes)
    WATER_METER = 0x05       # 수도 계량기 (6 bytes)
    CO2_SENSOR = 0x06        # CO2 센서 (4 bytes)
    TEMP_HUMIDITY = 0x07     # 온습도 센서 (6 bytes)
    SOLAR_SENSOR = 0x08      # 일사량 센서 (4 bytes)
    DC_MOTOR = 0x09          # DC 모터 감시 (3 bytes)

class DAQProtocol:
    """
    DAQ 통신 프로토콜 클래스
    """
    
    # 프레임 구분자
    STX = 0x02  # Start of Text
    ETX = 0x03  # End of Text
    
    # 데이터 크기 정의 (MSG Type별)
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
        DAQ 프레임 생성
        
        Args:
            msg_type: MessageType enum 또는 int (0x01~0x09)
            serial_no: 시리얼 번호 (0~255)
            data: 센서 데이터 (bytes)
        
        Returns:
            bytes: 완성된 프레임 [STX][Length][Serial No][MSG Type][Data][CRC16][ETX]
        
        Raises:
            ValueError: 데이터 크기가 잘못된 경우
        
        Example:
            >>> protocol = DAQProtocol()
            >>> # 단상 전력량계: 전압 221.2V, 전류 12.34A, 전력 12.345kW, 전력량 12345kWh
            >>> data = struct.pack('>HHHHI', 2212, 1234, 12345, 0, 12345)
            >>> frame = protocol.create_frame(MessageType.SINGLE_PHASE, 0, data)
            >>> print(frame.hex(' ').upper())
        """
        # MSG Type을 int로 변환
        if isinstance(msg_type, MessageType):
            msg_type_int = msg_type.value
        else:
            msg_type_int = msg_type
        
        # 데이터 크기 검증
        expected_size = self.DATA_SIZE.get(msg_type_int)
        if expected_size and len(data) != expected_size:
            raise ValueError(
                f"MSG Type 0x{msg_type_int:02X}의 데이터 크기는 {expected_size} bytes여야 합니다. "
                f"(받은 크기: {len(data)} bytes)"
            )
        
        # Length 계산 (Serial No + MSG Type + Data)
        length = 1 + 1 + len(data)
        
        # 헤더 생성: [STX][Length][Serial No][MSG Type]
        header = struct.pack('BBBB', self.STX, length, serial_no, msg_type_int)
        
        # CRC 계산 대상: [Length][Serial No][MSG Type][Data]
        crc_data = struct.pack('BBB', length, serial_no, msg_type_int) + data
        crc = calculate_crc16_modbus(crc_data)
        
        # 전체 프레임 조립
        frame = header + data + struct.pack('<H', crc) + struct.pack('B', self.ETX)
        
        return frame
    
    def parse_frame(self, frame):
        """
        DAQ 프레임 파싱
        
        Args:
            frame: 수신한 프레임 데이터 (bytes)
        
        Returns:
            dict: 파싱된 데이터
                {
                    'valid': bool,
                    'serial_no': int,
                    'msg_type': int,
                    'data': bytes,
                    'error': str (에러 발생 시)
                }
        
        Example:
            >>> protocol = DAQProtocol()
            >>> frame = bytes.fromhex('02 0C 00 01 08A4 04D2 3039 00003039 ABEC 03')
            >>> result = protocol.parse_frame(frame)
            >>> print(f"Valid: {result['valid']}, MSG Type: 0x{result['msg_type']:02X}")
        """
        result = {
            'valid': False,
            'serial_no': 0,
            'msg_type': 0,
            'data': b'',
            'error': ''
        }
        
        # 최소 프레임 크기 확인 (STX + Length + Serial No + MSG Type + CRC16 + ETX = 7 bytes)
        if len(frame) < 7:
            result['error'] = f"프레임 크기가 너무 작습니다 ({len(frame)} bytes)"
            return result
        
        # STX 확인
        if frame[0] != self.STX:
            result['error'] = f"STX가 잘못되었습니다 (0x{frame[0]:02X})"
            return result
        
        # ETX 확인
        if frame[-1] != self.ETX:
            result['error'] = f"ETX가 잘못되었습니다 (0x{frame[-1]:02X})"
            return result
        
        # 헤더 파싱
        length = frame[1]
        serial_no = frame[2]
        msg_type = frame[3]
        
        # 프레임 크기 검증
        expected_frame_size = 1 + 1 + length + 2 + 1  # STX + Length + Payload + CRC16 + ETX
        if len(frame) != expected_frame_size:
            result['error'] = (
                f"프레임 크기가 일치하지 않습니다 "
                f"(예상: {expected_frame_size}, 실제: {len(frame)})"
            )
            return result
        
        # CRC 검증 (STX와 ETX 제외)
        crc_data = frame[1:-3]  # Length부터 Data까지
        received_crc = struct.unpack('<H', frame[-3:-1])[0]
        calculated_crc = calculate_crc16_modbus(crc_data)
        
        if received_crc != calculated_crc:
            result['error'] = (
                f"CRC 불일치 "
                f"(수신: 0x{received_crc:04X}, 계산: 0x{calculated_crc:04X})"
            )
            return result
        
        # 데이터 추출
        data = frame[4:-3]
        
        result['valid'] = True
        result['serial_no'] = serial_no
        result['msg_type'] = msg_type
        result['data'] = data
        
        return result
    
    def get_msg_type_name(self, msg_type):
        """
        MSG Type 코드를 이름으로 변환
        
        Args:
            msg_type: MSG Type 코드 (int)
        
        Returns:
            str: MSG Type 이름
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
    print("DAQ 프로토콜 테스트\n")
    
    protocol = DAQProtocol()
    
    # 테스트 1: 단상 전력량계 프레임 생성
    print("=" * 60)
    print("테스트 1: 단상 전력량계 프레임 생성")
    print("=" * 60)
    
    # 데이터: 전압 221.2V, 전류 12.34A, 전력 12.345kW, 전력량 12345kWh
    voltage = 2212    # 221.2V * 10
    current = 1234    # 12.34A * 100
    power = 12345     # 12.345kW * 1000
    energy = 12345    # 12345kWh
    
    data = struct.pack('>HHHI', voltage, current, power, energy)
    print(f"입력 데이터:")
    print(f"  전압: {voltage/10:.1f}V")
    print(f"  전류: {current/100:.2f}A")
    print(f"  전력: {power/1000:.3f}kW")
    print(f"  전력량: {energy}kWh")
    
    frame = protocol.create_frame(MessageType.SINGLE_PHASE, 0, data)
    print(f"\n생성된 프레임:")
    print(f"  HEX: {frame.hex(' ').upper()}")
    print(f"  크기: {len(frame)} bytes")
    
    # 테스트 2: 프레임 파싱
    print("\n" + "=" * 60)
    print("테스트 2: 프레임 파싱")
    print("=" * 60)
    
    result = protocol.parse_frame(frame)
    print(f"파싱 결과:")
    print(f"  유효성: {'✓' if result['valid'] else '✗'}")
    print(f"  Serial No: {result['serial_no']}")
    print(f"  MSG Type: 0x{result['msg_type']:02X} ({protocol.get_msg_type_name(result['msg_type'])})")
    print(f"  데이터: {result['data'].hex(' ').upper()}")
    
    if result['error']:
        print(f"  에러: {result['error']}")
    
    # 테스트 3: 온습도 센서 프레임
    print("\n" + "=" * 60)
    print("테스트 3: 온습도 센서 프레임")
    print("=" * 60)
    
    # 온도: -12.3℃ (2의 보수), 습도: 99.9%
    temperature = -123  # -12.3℃ * 10
    humidity = 999      # 99.9% * 10
    
    data = struct.pack('>hH', temperature, humidity)
    print(f"입력 데이터:")
    print(f"  온도: {temperature/10:.1f}℃")
    print(f"  습도: {humidity/10:.1f}%")
    
    frame = protocol.create_frame(MessageType.TEMP_HUMIDITY, 5, data)
    print(f"\n생성된 프레임:")
    print(f"  HEX: {frame.hex(' ').upper()}")
    
    result = protocol.parse_frame(frame)
    print(f"\n파싱 결과:")
    print(f"  유효성: {'✓' if result['valid'] else '✗'}")
    print(f"  MSG Type: {protocol.get_msg_type_name(result['msg_type'])}")
    
    # 테스트 4: 잘못된 CRC
    print("\n" + "=" * 60)
    print("테스트 4: 잘못된 CRC 검증")
    print("=" * 60)
    
    bad_frame = bytearray(frame)
    bad_frame[-3] = 0x00  # CRC 변조
    
    result = protocol.parse_frame(bytes(bad_frame))
    print(f"파싱 결과:")
    print(f"  유효성: {'✓' if result['valid'] else '✗ (예상된 결과)'}")
    print(f"  에러: {result['error']}")
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)
