"""
=================================================================
파일명: communication-pc/src/data_parser.py
설명: DAQ 센서 데이터 파싱 모듈
작성자: 개발팀
작성일: 2025-10-23
=================================================================
각 센서 타입별로 바이너리 데이터를 파싱하여 실제 값으로 변환합니다.
- 소수점 처리
- 2의 보수 처리 (음수 온도)
- Overflow/Error 값 처리
=================================================================
"""

import struct
from daq_protocol import MessageType

class DataParser:
    """
    DAQ 센서 데이터 파싱 클래스
    """
    
    # 특수 값 정의
    OVERFLOW = 0xFFF1
    COMM_ERROR = 0xFFFE
    
    def __init__(self):
        """파서 초기화"""
        pass
    
    def parse(self, msg_type, data):
        """
        MSG Type에 따라 적절한 파서 호출
        
        Args:
            msg_type: MessageType enum 또는 int
            data: 바이너리 데이터 (bytes)
        
        Returns:
            dict: 파싱된 데이터 딕셔너리
        
        Example:
            >>> parser = DataParser()
            >>> data = bytes.fromhex('08A4 04D2 3039 00003039')
            >>> result = parser.parse(MessageType.SINGLE_PHASE, data)
            >>> print(result)
        """
        if isinstance(msg_type, MessageType):
            msg_type = msg_type.value
        
        # MSG Type별 파서 매핑
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
        
        parser_func = parsers.get(msg_type)
        if parser_func:
            return parser_func(data)
        else:
            return {'error': f'알 수 없는 MSG Type: 0x{msg_type:02X}'}
    
    def _check_special_value(self, value):
        """
        특수 값(Overflow, Error) 확인
        
        Args:
            value: 확인할 값 (int)
        
        Returns:
            tuple: (is_special, status_string)
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
        
        데이터 구조 (10 bytes):
        - 전압 (2 bytes): 소수점 1자리 (0.1V)
        - 전류 (2 bytes): 소수점 2자리 (0.01A)
        - 유효전력 (2 bytes): 소수점 3자리 (0.001kW)
        - 전력량 (4 bytes): 정수 (1kWh)
        
        Args:
            data: 10 bytes 데이터
        
        Returns:
            dict: 파싱된 데이터
        """
        if len(data) != 10:
            return {'error': f'데이터 크기 오류 (예상: 10 bytes, 실제: {len(data)} bytes)'}
        
        # 데이터 언팩
        voltage_raw, current_raw, power_raw, energy = struct.unpack('>HHHI', data)
        
        # 특수 값 확인
        voltage_status = self._check_special_value(voltage_raw)
        current_status = self._check_special_value(current_raw)
        power_status = self._check_special_value(power_raw)
        
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
        3상3선 전력량계 데이터 파싱
        
        데이터 구조 (30 bytes):
        - L1/L2/L3 전압 (각 2 bytes): 소수점 1자리
        - L1/L2/L3 전류 (각 2 bytes): 소수점 2자리
        - L1/L2/L3 유효전력 (각 2 bytes): 소수점 3자리
        - L1/L2/L3 전력량 (각 4 bytes): 정수
        """
        if len(data) != 30:
            return {'error': f'데이터 크기 오류 (예상: 30 bytes, 실제: {len(data)} bytes)'}
        
        # 데이터 언팩
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
        3상4선 전력량계 데이터 파싱
        
        데이터 구조 (32 bytes):
        - L1/L2/L3 전압 (각 2 bytes)
        - L1/L2/L3/N 전류 (각 2 bytes)
        - L1/L2/L3 유효전력 (각 2 bytes)
        - L1/L2/L3 전력량 (각 4 bytes)
        """
        if len(data) != 32:
            return {'error': f'데이터 크기 오류 (예상: 32 bytes, 실제: {len(data)} bytes)'}
        
        # 데이터 언팩
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
        """
        유량 센서 데이터 파싱
        
        데이터 구조 (8 bytes):
        - 순간 유량 (4 bytes): 소수점 2자리 (0.01L/min)
        - 누적 유량 (4 bytes): 소수점 2자리 (0.01L)
        """
        if len(data) != 8:
            return {'error': f'데이터 크기 오류'}
        
        flow_rate, total_flow = struct.unpack('>II', data)
        
        return {
            'flow_rate': {
                'value': flow_rate / 100.0,
                'unit': 'L/min'
            },
            'total_flow': {
                'value': total_flow / 100.0,
                'unit': 'L'
            }
        }
    
    def parse_water_meter(self, data):
        """
        수도 계량기 데이터 파싱
        
        데이터 구조 (4 bytes):
        - 사용량 (4 bytes): 소수점 2자리 (0.01L)
        """
        if len(data) != 4:
            return {'error': f'데이터 크기 오류'}
        
        usage = struct.unpack('>I', data)[0]
        
        return {
            'water_usage': {
                'value': usage / 100.0,
                'unit': 'L'
            }
        }
    
    def parse_co2_sensor(self, data):
        """
        CO2 센서 데이터 파싱
        
        데이터 구조 (2 bytes):
        - CO2 농도 (2 bytes): 정수 (1ppm)
        """
        if len(data) != 2:
            return {'error': f'데이터 크기 오류'}
        
        co2_ppm = struct.unpack('>H', data)[0]
        
        return {
            'co2': {
                'value': co2_ppm,
                'unit': 'ppm'
            }
        }
    
    def parse_temp_humidity(self, data):
        """
        온습도 센서 데이터 파싱
        
        데이터 구조 (4 bytes):
        - 온도 (2 bytes): 소수점 1자리, 2의 보수 (signed)
        - 습도 (2 bytes): 소수점 1자리
        """
        if len(data) != 4:
            return {'error': f'데이터 크기 오류'}
        
        # 온도는 signed short (2의 보수)
        temp_raw = struct.unpack('>h', data[0:2])[0]
        humidity_raw = struct.unpack('>H', data[2:4])[0]
        
        return {
            'temperature': {
                'value': temp_raw / 10.0,
                'unit': '℃'
            },
            'humidity': {
                'value': humidity_raw / 10.0,
                'unit': '%'
            }
        }
    
    def parse_solar_sensor(self, data):
        """
        일사량 센서 데이터 파싱
        
        데이터 구조 (2 bytes):
        - 일사량 (2 bytes): 정수 (1W/m²)
        """
        if len(data) != 2:
            return {'error': f'데이터 크기 오류'}
        
        solar = struct.unpack('>H', data)[0]
        
        return {
            'solar': {
                'value': solar,
                'unit': 'W/m²'
            }
        }
    
    def parse_dc_motor(self, data):
        """
        DC 모터 감시 데이터 파싱
        
        데이터 구조 (1 byte):
        - 상태 (1 byte): 비트 플래그
          bit 0: 모터 ON/OFF
          bit 1: 방향 (정/역)
          bit 2-7: Reserved
        """
        if len(data) != 1:
            return {'error': f'데이터 크기 오류'}
        
        status = data[0]
        
        return {
            'motor_on': bool(status & 0x01),
            'direction': 'Forward' if (status & 0x02) == 0 else 'Reverse',
            'raw_status': f'0x{status:02X}'
        }
    
    def format_output(self, parsed_data):
        """
        파싱된 데이터를 읽기 쉬운 형식으로 출력
        
        Args:
            parsed_data: parse() 함수의 결과
        
        Returns:
            str: 포맷된 문자열
        """
        if 'error' in parsed_data:
            return f"에러: {parsed_data['error']}"
        
        lines = []
        
        def format_value(item):
            if isinstance(item, dict):
                if 'value' in item:
                    value = item['value']
                    unit = item.get('unit', '')
                    status = item.get('status', 'OK')
                    
                    if status != 'OK':
                        return f"{status}"
                    elif value is None:
                        return "N/A"
                    else:
                        return f"{value:.3f} {unit}"
                else:
                    # 중첩된 딕셔너리 처리
                    sub_lines = []
                    for key, val in item.items():
                        sub_lines.append(f"  {key}: {format_value(val)}")
                    return "\n".join(sub_lines)
            else:
                return str(item)
        
        for key, value in parsed_data.items():
            lines.append(f"{key}:")
            lines.append(format_value(value))
        
        return "\n".join(lines)


# =================================================================
# 테스트 코드
# =================================================================
if __name__ == "__main__":
    print("데이터 파싱 모듈 테스트\n")
    
    parser = DataParser()
    
    # 테스트 1: 단상 전력량계
    print("=" * 60)
    print("테스트 1: 단상 전력량계 파싱")
    print("=" * 60)
    
    # 전압 221.2V, 전류 12.34A, 전력 12.345kW, 전력량 12345kWh
    data = struct.pack('>HHHI', 2212, 1234, 12345, 12345)
    print(f"입력 데이터: {data.hex(' ').upper()}")
    
    result = parser.parse(MessageType.SINGLE_PHASE, data)
    print(f"\n파싱 결과:")
    print(f"  전압: {result['voltage']['value']:.1f} {result['voltage']['unit']}")
    print(f"  전류: {result['current']['value']:.2f} {result['current']['unit']}")
    print(f"  전력: {result['power']['value']:.3f} {result['power']['unit']}")
    print(f"  전력량: {result['energy']['value']} {result['energy']['unit']}")
    
    # 테스트 2: 온습도 센서 (음수 온도)
    print("\n" + "=" * 60)
    print("테스트 2: 온습도 센서 파싱 (음수 온도)")
    print("=" * 60)
    
    # 온도 -12.3℃, 습도 99.9%
    data = struct.pack('>hH', -123, 999)
    print(f"입력 데이터: {data.hex(' ').upper()}")
    
    result = parser.parse(MessageType.TEMP_HUMIDITY, data)
    print(f"\n파싱 결과:")
    print(f"  온도: {result['temperature']['value']:.1f} {result['temperature']['unit']}")
    print(f"  습도: {result['humidity']['value']:.1f} {result['humidity']['unit']}")
    
    # 테스트 3: 온습도 센서 (양수 온도)
    print("\n" + "=" * 60)
    print("테스트 3: 온습도 센서 파싱 (양수 온도)")
    print("=" * 60)
    
    # 온도 25.3℃, 습도 65.5%
    data = struct.pack('>hH', 253, 655)
    print(f"입력 데이터: {data.hex(' ').upper()}")
    
    result = parser.parse(MessageType.TEMP_HUMIDITY, data)
    print(f"\n파싱 결과:")
    print(f"  온도: {result['temperature']['value']:.1f} {result['temperature']['unit']}")
    print(f"  습도: {result['humidity']['value']:.1f} {result['humidity']['unit']}")
    
    # 테스트 4: Overflow 값 처리
    print("\n" + "=" * 60)
    print("테스트 4: Overflow 값 처리")
    print("=" * 60)
    
    # 전압 Overflow, 나머지는 정상
    data = struct.pack('>HHHI', 0xFFF1, 1234, 12345, 12345)
    print(f"입력 데이터: {data.hex(' ').upper()}")
    
    result = parser.parse(MessageType.SINGLE_PHASE, data)
    print(f"\n파싱 결과:")
    print(f"  전압: {result['voltage']['status']}")
    print(f"  전류: {result['current']['value']:.2f} {result['current']['unit']}")
    
    # 테스트 5: DC 모터 상태
    print("\n" + "=" * 60)
    print("테스트 5: DC 모터 상태 파싱")
    print("=" * 60)
    
    # 모터 ON, 정방향
    data = struct.pack('B', 0x01)
    result = parser.parse(MessageType.DC_MOTOR, data)
    print(f"상태 0x01: 모터 {result['motor_on']}, 방향 {result['direction']}")
    
    # 모터 ON, 역방향
    data = struct.pack('B', 0x03)
    result = parser.parse(MessageType.DC_MOTOR, data)
    print(f"상태 0x03: 모터 {result['motor_on']}, 방향 {result['direction']}")
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)
