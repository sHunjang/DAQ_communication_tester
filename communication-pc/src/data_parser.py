"""
=================================================================
파일명: data_parser.py
설명: DAQ 센서 데이터 파싱 모듈
작성일: 2025-10-24
=================================================================
각 센서 타입별로 바이너리 데이터를 실제 값으로 변환합니다.

주요 기능:
1. MSG Type에 따른 자동 파싱
2. 소수점 처리 (예: 2212 → 221.2V)
3. 2의 보수 처리 (음수 온도)
4. Overflow/Error 값 처리 (0xFFF1, 0xFFFE)

지원 센서:
- 단상 전력량계: 전압, 전류, 전력, 전력량
- 3상3선/4선 전력량계: 각 상별 전압, 전류, 전력, 전력량
- 유량 센서: 순간 유량, 누적 유량
- 수도 계량기: 사용량
- CO2 센서: CO2 농도
- 온습도 센서: 온도(음수 가능), 습도
- 일사량 센서: 일사량
- DC 모터: 동작 상태

사용 예시:
    parser = DataParser()
    data = bytes.fromhex('08A4 04D2 3039 00003039')
    result = parser.parse(MessageType.SINGLE_PHASE, data)
    print(f"전압: {result['voltage']['value']:.1f}V")
=================================================================
"""

import struct

# DAQ 프로토콜 import (상대/절대 경로 자동 처리)
try:
    from .daq_protocol import MessageType
except ImportError:
    from daq_protocol import MessageType


# =================================================================
# 데이터 파서 클래스
# =================================================================
class DataParser:
    """
    DAQ 센서 데이터를 파싱하는 클래스
    
    바이너리 데이터를 실제 물리량으로 변환하며,
    각 센서 타입에 맞는 소수점 처리와 단위 변환을 수행합니다.
    """
    
    # =================================================================
    # 특수 값 정의 (에러 상태 표시)
    # =================================================================
    OVERFLOW = 0xFFF1    # 측정 범위 초과
    COMM_ERROR = 0xFFFE  # 통신 오류
    
    def __init__(self):
        """파서 초기화"""
        pass
    
    def parse(self, msg_type, data):
        """
        MSG Type에 따라 적절한 파서 자동 호출
        
        Args:
            msg_type (int or MessageType): 메시지 타입
            data (bytes): 바이너리 센서 데이터
        
        Returns:
            dict: 파싱된 데이터 (센서별로 구조가 다름)
        
        Example:
            >>> parser = DataParser()
            >>> data = bytes.fromhex('08A4 04D2 3039 00003039')
            >>> result = parser.parse(MessageType.SINGLE_PHASE, data)
            >>> print(result['voltage']['value'])
            221.2
        """
        # MessageType Enum을 int로 변환
        if isinstance(msg_type, MessageType):
            msg_type = msg_type.value
        
        # MSG Type별 파서 매핑 테이블
        parsers = {
            MessageType.SINGLE_PHASE: self.parse_single_phase,
            MessageType.THREE_PHASE_3W: self.parse_three_phase_3w,
            MessageType.THREE_PHASE_4W: self.parse_three_phase_4w,
            MessageType.FLOW_SENSOR: self.parse_flow_sensor,
            MessageType.WATER_METER: self.parse_water_meter,
            MessageType.CO2_SENSOR: self.parse_co2_sensor,
            MessageType.TEMP_HUMIDITY: self.parse_temp_humidity,
            MessageType.SOLAR_SENSOR: self.parse_solar_sensor,
            MessageType.DC_MOTOR: self.parse_dc_motor
        }
        
        # 해당 파서 함수 호출
        parser_func = parsers.get(msg_type)
        if parser_func:
            return parser_func(data)
        else:
            return {'error': f'알 수 없는 MSG Type: 0x{msg_type:02X}'}
    
    def _check_special_value(self, value):
        """
        Overflow 또는 통신 오류 값 확인
        
        센서에서 측정 범위를 초과하거나 통신 오류가 발생하면
        특수한 값(0xFFF1, 0xFFFE)을 전송합니다.
        
        Args:
            value (int): 확인할 값
        
        Returns:
            tuple: (is_special, status_string)
                - is_special: True면 특수값, False면 정상값
                - status_string: "OVERFLOW", "COMM_ERROR", "OK"
        """
        if value == self.OVERFLOW:
            return True, "OVERFLOW"
        elif value == self.COMM_ERROR:
            return True, "COMM_ERROR"
        else:
            return False, "OK"
    
    def parse_single_phase(self, data):
        """
        단상 전력량계 데이터 파싱
        
        데이터 구조 (10 bytes, Big-endian):
        - 전압 (2B): unsigned short, 소수점 1자리 (0.1V 단위)
        - 전류 (2B): unsigned short, 소수점 2자리 (0.01A 단위)
        - 유효전력 (2B): unsigned short, 소수점 3자리 (0.001kW 단위)
        - 전력량 (4B): unsigned int, 정수 (1kWh 단위)
        
        Args:
            data (bytes): 10 bytes 데이터
        
        Returns:
            dict: 파싱된 데이터
                {
                    'voltage': {'value': float, 'unit': 'V', 'status': 'OK'},
                    'current': {'value': float, 'unit': 'A', 'status': 'OK'},
                    'power': {'value': float, 'unit': 'kW', 'status': 'OK'},
                    'energy': {'value': int, 'unit': 'kWh', 'status': 'OK'}
                }
        """
        # 데이터 크기 검증
        if len(data) != 10:
            return {'error': f'데이터 크기 오류 (예상: 10 bytes, 실제: {len(data)} bytes)'}
        
        # 바이너리 데이터 언팩 (Big-endian)
        # H: unsigned short (2 bytes)
        # I: unsigned int (4 bytes)
        voltage_raw, current_raw, power_raw, energy = struct.unpack('>HHHI', data)
        
        # 특수 값 확인 (Overflow, 통신 오류 등)
        voltage_status = self._check_special_value(voltage_raw)
        current_status = self._check_special_value(current_raw)
        power_status = self._check_special_value(power_raw)
        
        # 결과 딕셔너리 생성
        result = {
            'voltage': {
                'value': voltage_raw / 10.0 if not voltage_status[0] else None,
                'unit': 'V',
                'status': voltage_status[1]
            },
            'current': {
                'value': current_raw / 100.0 if not current_status[0] else None,
                'unit': 'A',
                'status': current_status[1]
            },
            'power': {
                'value': power_raw / 1000.0 if not power_status[0] else None,
                'unit': 'kW',
                'status': power_status[1]
            },
            'energy': {
                'value': energy,
                'unit': 'kWh',
                'status': 'OK'
            }
        }
        
        return result
    
    def parse_three_phase_3w(self, data):
        """
        3상3선 전력량계 데이터 파싱 (30 bytes)
        
        3개 상(L1, L2, L3)의 전압, 전류, 전력, 전력량을 포함합니다.
        """
        if len(data) != 30:
            return {'error': f'데이터 크기 오류'}
        
        # 언팩: 전압3개(6B) + 전류3개(6B) + 전력3개(6B) + 전력량3개(12B)
        values = struct.unpack('>HHHHHHHHHIII', data)
        
        result = {
            'L1': {
                'voltage': {'value': values[0] / 10.0, 'unit': 'V'},
                'current': {'value': values[3] / 100.0, 'unit': 'A'},
                'power': {'value': values[6] / 1000.0, 'unit': 'kW'},
                'energy': {'value': values[9], 'unit': 'kWh'}
            },
            'L2': {
                'voltage': {'value': values[1] / 10.0, 'unit': 'V'},
                'current': {'value': values[4] / 100.0, 'unit': 'A'},
                'power': {'value': values[7] / 1000.0, 'unit': 'kW'},
                'energy': {'value': values[10], 'unit': 'kWh'}
            },
            'L3': {
                'voltage': {'value': values[2] / 10.0, 'unit': 'V'},
                'current': {'value': values[5] / 100.0, 'unit': 'A'},
                'power': {'value': values[8] / 1000.0, 'unit': 'kW'},
                'energy': {'value': values[11], 'unit': 'kWh'}
            }
        }
        
        return result
    
    def parse_three_phase_4w(self, data):
        """
        3상4선 전력량계 데이터 파싱 (32 bytes)
        
        3상3선 + 중성선(N) 전류 포함
        """
        if len(data) != 32:
            return {'error': f'데이터 크기 오류'}
        
        # 전압3개 + 전류4개(L1,L2,L3,N) + 전력3개 + 전력량3개
        values = struct.unpack('>HHHHHHHHHHIII', data)
        
        result = {
            'L1': {
                'voltage': {'value': values[0] / 10.0, 'unit': 'V'},
                'current': {'value': values[3] / 100.0, 'unit': 'A'},
                'power': {'value': values[7] / 1000.0, 'unit': 'kW'},
                'energy': {'value': values[10], 'unit': 'kWh'}
            },
            'L2': {
                'voltage': {'value': values[1] / 10.0, 'unit': 'V'},
                'current': {'value': values[4] / 100.0, 'unit': 'A'},
                'power': {'value': values[8] / 1000.0, 'unit': 'kW'},
                'energy': {'value': values[11], 'unit': 'kWh'}
            },
            'L3': {
                'voltage': {'value': values[2] / 10.0, 'unit': 'V'},
                'current': {'value': values[5] / 100.0, 'unit': 'A'},
                'power': {'value': values[9] / 1000.0, 'unit': 'kW'},
                'energy': {'value': values[12], 'unit': 'kWh'}
            },
            'N': {
                'current': {'value': values[6] / 100.0, 'unit': 'A'}
            }
        }
        
        return result
    
    def parse_flow_sensor(self, data):
        """유량 센서 데이터 파싱 (8 bytes)"""
        if len(data) != 8:
            return {'error': f'데이터 크기 오류'}
        
        flow_rate, total_flow = struct.unpack('>II', data)
        
        return {
            'flow_rate': {'value': flow_rate / 100.0, 'unit': 'L/min'},
            'total_flow': {'value': total_flow / 100.0, 'unit': 'L'}
        }
    
    def parse_water_meter(self, data):
        """수도 계량기 데이터 파싱 (4 bytes)"""
        if len(data) != 4:
            return {'error': f'데이터 크기 오류'}
        
        usage = struct.unpack('>I', data)[0]
        
        return {
            'water_usage': {'value': usage / 100.0, 'unit': 'L'}
        }
    
    def parse_co2_sensor(self, data):
        """CO2 센서 데이터 파싱 (2 bytes)"""
        if len(data) != 2:
            return {'error': f'데이터 크기 오류'}
        
        co2_ppm = struct.unpack('>H', data)[0]
        
        return {
            'co2': {'value': co2_ppm, 'unit': 'ppm'}
        }
    
    def parse_temp_humidity(self, data):
        """
        온습도 센서 데이터 파싱 (4 bytes)
        
        특이사항:
        - 온도는 signed short (2의 보수) → 음수 표현 가능
        - 습도는 unsigned short
        
        예:
        - 온도 0xFF85 = -123 → -12.3℃
        - 습도 0x03E7 = 999 → 99.9%
        """
        if len(data) != 4:
            return {'error': f'데이터 크기 오류'}
        
        # h: signed short (2의 보수, -32768~32767)
        # H: unsigned short (0~65535)
        temp_raw = struct.unpack('>h', data[0:2])[0]  # signed
        humidity_raw = struct.unpack('>H', data[2:4])[0]  # unsigned
        
        return {
            'temperature': {'value': temp_raw / 10.0, 'unit': '℃'},
            'humidity': {'value': humidity_raw / 10.0, 'unit': '%'}
        }
    
    def parse_solar_sensor(self, data):
        """일사량 센서 데이터 파싱 (2 bytes)"""
        if len(data) != 2:
            return {'error': f'데이터 크기 오류'}
        
        solar = struct.unpack('>H', data)[0]
        
        return {
            'solar': {'value': solar, 'unit': 'W/m²'}
        }
    
    def parse_dc_motor(self, data):
        """
        DC 모터 감시 데이터 파싱 (1 byte)
        
        상태 비트:
        - bit 0: 모터 ON/OFF
        - bit 1: 방향 (0: Forward, 1: Reverse)
        - bit 2-7: Reserved
        """
        if len(data) != 1:
            return {'error': f'데이터 크기 오류'}
        
        status = data[0]
        
        return {
            'motor_on': bool(status & 0x01),
            'direction': 'Forward' if (status & 0x02) == 0 else 'Reverse',
            'raw_status': f'0x{status:02X}'
        }


# =================================================================
# 테스트 코드
# =================================================================
if __name__ == "__main__":
    print("="*70)
    print("데이터 파서 테스트")
    print("="*70)
    
    parser = DataParser()
    
    # 테스트 1: 단상 전력량계
    print("\n[테스트 1] 단상 전력량계")
    print("-"*70)
    data = struct.pack('>HHHI', 2212, 1234, 12345, 12345)
    print(f"입력 데이터: {data.hex(' ').upper()}")
    
    result = parser.parse(MessageType.SINGLE_PHASE, data)
    print(f"파싱 결과:")
    print(f"  전압: {result['voltage']['value']:.1f} {result['voltage']['unit']}")
    print(f"  전류: {result['current']['value']:.2f} {result['current']['unit']}")
    print(f"  전력: {result['power']['value']:.3f} {result['power']['unit']}")
    print(f"  전력량: {result['energy']['value']} {result['energy']['unit']}")
    
    # 테스트 2: 온습도 (음수 온도)
    print("\n[테스트 2] 온습도 센서 (음수 온도)")
    print("-"*70)
    data = struct.pack('>hH', -123, 999)
    print(f"입력 데이터: {data.hex(' ').upper()}")
    
    result = parser.parse(MessageType.TEMP_HUMIDITY, data)
    print(f"파싱 결과:")
    print(f"  온도: {result['temperature']['value']:.1f} {result['temperature']['unit']}")
    print(f"  습도: {result['humidity']['value']:.1f} {result['humidity']['unit']}")
    
    # 테스트 3: 온습도 (양수 온도)
    print("\n[테스트 3] 온습도 센서 (양수 온도)")
    print("-"*70)
    data = struct.pack('>hH', 253, 655)
    result = parser.parse(MessageType.TEMP_HUMIDITY, data)
    print(f"  온도: {result['temperature']['value']:.1f}℃")
    print(f"  습도: {result['humidity']['value']:.1f}%")
    
    # 테스트 4: Overflow 처리
    print("\n[테스트 4] Overflow 값 처리")
    print("-"*70)
    data = struct.pack('>HHHI', 0xFFF1, 1234, 12345, 12345)
    result = parser.parse(MessageType.SINGLE_PHASE, data)
    print(f"  전압 상태: {result['voltage']['status']}")
    print(f"  전압 값: {result['voltage']['value']}")
    print(f"  전류: {result['current']['value']:.2f}A")
    
    # 테스트 5: CO2 센서
    print("\n[테스트 5] CO2 센서")
    print("-"*70)
    data = struct.pack('>H', 876)
    result = parser.parse(MessageType.CO2_SENSOR, data)
    print(f"  CO2: {result['co2']['value']} {result['co2']['unit']}")
    
    print("\n" + "="*70)
    print("✓ 모든 테스트 완료")
    print("="*70)
