"""
=================================================================
파일명: communication-pc/test_daq_protocol.py
설명: DAQ 프로토콜 통신 테스트 (통신 PC 측)
작성자: 개발팀
작성일: 2025-10-23
=================================================================
DAQ 장치와 실제 프로토콜로 통신하는 테스트 프로그램입니다.
Mock Serial 또는 실제 RS232로 전환 가능합니다.
=================================================================
"""

import time
from datetime import datetime

# Config 설정 불러오기
from config.config import (
    USE_MOCK_SERIAL,
    RS232_PORT,
    BAUDRATE,
    BYTESIZE,
    PARITY,
    STOPBITS,
    TIMEOUT,
    INTER_REQUEST_DELAY,
    TARGET_RELIABILITY,
    LOG_DIR,
    SIMULATION_SENSORS
)

# 로거 및 프로토콜 모듈
from src.data_logger import DataLogger
from src.daq_protocol import DAQProtocol, MessageType
from src.data_parser import DataParser

# =================================================================
# Serial 클래스 선택 (Mock 또는 Real)
# =================================================================
if USE_MOCK_SERIAL:
    from mock_serial import MockSerial as Serial, cleanup_mock_files
    print("[시스템] Mock Serial 모드 (가상 테스트)")
else:
    import serial as pyserial
    Serial = pyserial.Serial
    cleanup_mock_files = None
    print("[시스템] 실제 RS232 모드")

# =================================================================
# 시리얼 포트 초기화 함수
# =================================================================
def init_serial():
    """시리얼 포트 초기화"""
    try:
        ser = Serial(
            port=RS232_PORT,
            baudrate=BAUDRATE,
            bytesize=BYTESIZE,
            parity=PARITY,
            stopbits=STOPBITS,
            timeout=TIMEOUT
        )
        
        if ser.is_open:
            mode = "Mock 가상" if USE_MOCK_SERIAL else "실제 RS232"
            print(f"✓ 시리얼 포트 {RS232_PORT} 열기 성공 ({mode})")
            print(f"  - Baudrate: {BAUDRATE}bps")
            print(f"  - Timeout: {TIMEOUT}초")
            return ser
        else:
            print(f"✗ 시리얼 포트 {RS232_PORT} 열기 실패")
            return None
            
    except Exception as e:
        print(f"✗ 시리얼 포트 오류: {e}")
        return None

# =================================================================
# DAQ 요청 전송 함수
# =================================================================
def send_daq_request(ser, msg_type, logger, request_id):
    """
    DAQ에 데이터 요청 전송
    
    참고: 실제로는 요청 프레임이 없을 수 있음
    이 예제에서는 단순히 MSG Type만 전송
    
    Args:
        ser: 시리얼 포트 객체
        msg_type: MessageType
        logger: DataLogger
        request_id: 요청 ID
    
    Returns:
        datetime: 송신 시간
    """
    try:
        send_time = datetime.now()
        
        # 간단한 요청 메시지 (1 byte: MSG Type)
        # 실제 DAQ는 자동으로 데이터를 보낼 수도 있음
        request_data = bytes([msg_type])
        ser.write(request_data)
        ser.flush()
        
        # 로그에 요청 기록
        msg_type_name = {
            MessageType.SINGLE_PHASE: "단상",
            MessageType.TEMP_HUMIDITY: "온습도",
            MessageType.CO2_SENSOR: "CO2"
        }.get(msg_type, f"0x{msg_type:02X}")
        
        logger.log_request(request_id, send_time, f"REQ_{msg_type_name}")
        
        print(f"→ 요청 송신: MSG Type 0x{msg_type:02X} ({msg_type_name})")
        return send_time
        
    except Exception as e:
        print(f"✗ 송신 오류: {e}")
        logger.log_error(f"송신 오류: {e}")
        return None

# =================================================================
# DAQ 응답 수신 함수
# =================================================================
def receive_daq_response(ser, protocol, parser, logger, request_id):
    """
    DAQ로부터 응답 프레임 수신 및 파싱
    
    Args:
        ser: 시리얼 포트 객체
        protocol: DAQProtocol 객체
        parser: DataParser 객체
        logger: DataLogger
        request_id: 요청 ID
    
    Returns:
        dict: 파싱된 데이터 또는 None
    """
    try:
        receive_time = datetime.now()
        
        # 프레임 수신 (최대 256 bytes)
        # STX를 기다림
        stx_found = False
        frame_buffer = bytearray()
        
        start_time = time.time()
        while time.time() - start_time < TIMEOUT:
            if ser.in_waiting > 0:
                byte = ser.read(1)
                
                if not stx_found:
                    if byte[0] == 0x02:  # STX
                        stx_found = True
                        frame_buffer.append(byte[0])
                else:
                    frame_buffer.append(byte[0])
                    
                    # ETX를 찾으면 프레임 완성
                    if byte[0] == 0x03:  # ETX
                        break
            else:
                time.sleep(0.01)
        
        if not stx_found or len(frame_buffer) < 7:
            # 타임아웃
            timeout_time = datetime.now()
            logger.log_timeout(request_id, timeout_time)
            print(f"✗ 타임아웃: {TIMEOUT}초 동안 응답 없음")
            return None
        
        frame = bytes(frame_buffer)
        print(f"← 수신: {len(frame)} bytes")
        print(f"   HEX: {frame.hex(' ').upper()}")
        
        # 프레임 파싱
        result = protocol.parse_frame(frame)
        
        if not result['valid']:
            print(f"✗ 프레임 파싱 오류: {result['error']}")
            logger.log_error(f"프레임 파싱 오류: {result['error']}")
            return None
        
        # 데이터 파싱
        parsed_data = parser.parse(result['msg_type'], result['data'])
        
        if 'error' in parsed_data:
            print(f"✗ 데이터 파싱 오류: {parsed_data['error']}")
            logger.log_error(f"데이터 파싱 오류: {parsed_data['error']}")
            return None
        
        # 로그에 응답 기록
        msg_type_name = protocol.get_msg_type_name(result['msg_type'])
        logger.log_response(request_id, receive_time, msg_type_name, success=True)
        
        print(f"✓ 수신 성공: {msg_type_name}")
        
        return {
            'msg_type': result['msg_type'],
            'serial_no': result['serial_no'],
            'data': parsed_data
        }
        
    except Exception as e:
        print(f"✗ 수신 오류: {e}")
        logger.log_error(f"수신 오류: {e}")
        return None

# =================================================================
# 데이터 출력 함수
# =================================================================
def print_sensor_data(parsed_data, msg_type):
    """파싱된 센서 데이터 출력"""
    
    if msg_type == MessageType.SINGLE_PHASE:
        print(f"   전압: {parsed_data['voltage']['value']:.1f} {parsed_data['voltage']['unit']}")
        print(f"   전류: {parsed_data['current']['value']:.2f} {parsed_data['current']['unit']}")
        print(f"   전력: {parsed_data['power']['value']:.3f} {parsed_data['power']['unit']}")
        print(f"   전력량: {parsed_data['energy']['value']} {parsed_data['energy']['unit']}")
    
    elif msg_type == MessageType.TEMP_HUMIDITY:
        print(f"   온도: {parsed_data['temperature']['value']:.1f} {parsed_data['temperature']['unit']}")
        print(f"   습도: {parsed_data['humidity']['value']:.1f} {parsed_data['humidity']['unit']}")
    
    elif msg_type == MessageType.CO2_SENSOR:
        print(f"   CO2: {parsed_data['co2']['value']} {parsed_data['co2']['unit']}")

# =================================================================
# 메인 테스트 루프
# =================================================================
def main():
    """메인 실행 함수"""
    print("="*60)
    print("DAQ 프로토콜 통신 테스트 (통신 PC 측)")
    print("="*60)
    
    if USE_MOCK_SERIAL:
        print(f"⚠ Mock Serial 모드")
        print(f"⚠ 가상 센서 PC의 test_daq_simulator.py를 먼저 실행하세요.")
    else:
        print(f"✓ 실제 RS232 모드")
        print(f"✓ DAQ 장치가 {RS232_PORT}에 연결되어 있는지 확인하세요.")
    
    print(f"목표 신뢰도: {TARGET_RELIABILITY}%")
    print("-"*60)
    
    # Mock 모드면 통신 파일 정리
    if USE_MOCK_SERIAL and cleanup_mock_files:
        print("이전 통신 파일 정리")
        cleanup_mock_files()
        time.sleep(0.5)
    
    # 모듈 초기화
    logger = DataLogger(log_dir=LOG_DIR)
    protocol = DAQProtocol()
    parser = DataParser()
    
    # 시리얼 포트 초기화
    ser = init_serial()
    if ser is None:
        print("\n프로그램을 종료합니다.")
        return
    
    print("\n테스트 시작 (Ctrl+C로 종료)")
    print(f"테스트할 센서: {[f'0x{s:02X}' for s in SIMULATION_SENSORS]}")
    print("-"*60)
    
    # 준비 대기
    print("\nDAQ 준비 대기 중...")
    time.sleep(2)
    print("테스트 시작!\n")
    
    test_count = 0
    success_count = 0
    sensor_index = 0
    
    try:
        while True:
            test_count += 1
            
            # 순환하면서 센서 타입 선택
            msg_type = SIMULATION_SENSORS[sensor_index]
            sensor_index = (sensor_index + 1) % len(SIMULATION_SENSORS)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            
            print(f"\n[테스트 #{test_count}] {timestamp}")
            print(f"센서 타입: 0x{msg_type:02X} ({protocol.get_msg_type_name(msg_type)})")
            
            # 1. 요청 전송
            send_time = send_daq_request(ser, msg_type, logger, test_count)
            
            if send_time:
                # 2. 응답 수신 및 파싱
                response = receive_daq_response(ser, protocol, parser, logger, test_count)
                
                # 3. 응답 확인
                if response:
                    success_count += 1
                    print(f"✓ 통신 성공")
                    
                    # 센서 데이터 출력
                    print_sensor_data(response['data'], response['msg_type'])
                else:
                    print(f"✗ 통신 실패 (응답 없음 또는 파싱 오류)")
            
            # 4. 통계 출력
            success_rate = (success_count / test_count) * 100
            print(f"  통계: {success_count}/{test_count} 성공 ({success_rate:.1f}%)")
            
            if success_rate >= TARGET_RELIABILITY:
                print(f"  ✓ 목표 신뢰도 {TARGET_RELIABILITY}% 달성!")
            else:
                print(f"  ⚠ 목표 신뢰도 {TARGET_RELIABILITY}% 미달")
            
            # 5. 다음 테스트 전 대기
            time.sleep(INTER_REQUEST_DELAY)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("테스트 종료")
        print("="*60)
        print(f"총 테스트 횟수: {test_count}")
        print(f"성공 횟수: {success_count}")
        print(f"실패 횟수: {test_count - success_count}")
        final_rate = (success_count/test_count)*100 if test_count > 0 else 0
        print(f"최종 성공률: {final_rate:.2f}%")
        
        if final_rate >= TARGET_RELIABILITY:
            print(f"✓ 목표 신뢰도 {TARGET_RELIABILITY}% 달성!")
        else:
            print(f"✗ 목표 신뢰도 {TARGET_RELIABILITY}% 미달")
        
        # 로거 통계 출력
        print("\n" + "-"*60)
        print("로그 통계:")
        stats = logger.get_statistics()
        print(f"  총 요청: {stats['total']}")
        print(f"  성공: {stats['success']}")
        print(f"  실패: {stats['failure']}")
        if stats['avg_response_time'] > 0:
            print(f"  평균 응답 시간: {stats['avg_response_time']:.2f}ms")
            print(f"  최소 응답 시간: {stats['min_response_time']:.2f}ms")
            print(f"  최대 응답 시간: {stats['max_response_time']:.2f}ms")
        
    finally:
        # 리소스 정리
        logger.close()
        
        if ser and ser.is_open:
            ser.close()
            print(f"\n시리얼 포트 {RS232_PORT} 닫기 완료")

if __name__ == "__main__":
    main()
