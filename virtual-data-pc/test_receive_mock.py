"""
=================================================================
파일명: virtual-sensor-pc/test_receive_mock.py
설명: Mock Serial을 사용한 RS485 수신 및 응답 테스트 (로깅 추가)
작성자: 개발팀
작성일: 2025-10-17
수정일: 2025-10-17 (로깅 기능 추가)
=================================================================
"""

import time
import random
from datetime import datetime

# Mock Serial 클래스 import
from mock_serial import MockSerial as Serial

# 로거 import
from src.data_logger import DataLogger

# config.py에서 설정값 불러오기
from config.config import (
    RS485_PORT,
    BAUDRATE,
    BYTESIZE,
    PARITY,
    STOPBITS,
    TIMEOUT,
    SENSOR_TYPES,
    SENSOR_RANGES,
    DATA_GENERATION_DELAY_MS,
    LOG_DIR
)

# =================================================================
# 시리얼 포트 초기화 함수
# =================================================================
def init_serial():
    """Mock 시리얼 포트를 열고 초기화"""
    try:
        ser = Serial(
            port=RS485_PORT,
            baudrate=BAUDRATE,
            bytesize=BYTESIZE,
            parity=PARITY,
            stopbits=STOPBITS,
            timeout=TIMEOUT
        )
        
        if ser.is_open:
            print(f"✓ Mock 시리얼 포트 {RS485_PORT} 열기 성공")
            print(f"  - Baudrate: {BAUDRATE}")
            print(f"  - Timeout: {TIMEOUT}초")
            print(f"  - 지원 센서: {', '.join(SENSOR_TYPES)}")
            print(f"  - 모드: 가상 테스트 모드")
            return ser
        else:
            print(f"✗ Mock 시리얼 포트 {RS485_PORT} 열기 실패")
            return None
            
    except Exception as e:
        print(f"✗ 시리얼 포트 오류: {e}")
        return None

# =================================================================
# 가상 센서 데이터 생성 함수
# =================================================================
def generate_sensor_data():
    """가상 센서 데이터를 생성"""
    # 센서 데이터 생성 지연 시뮬레이션
    time.sleep(DATA_GENERATION_DELAY_MS / 1000.0)
    
    sensor_data = {}
    for sensor_type in SENSOR_TYPES:
        if sensor_type in SENSOR_RANGES:
            range_info = SENSOR_RANGES[sensor_type]
            value = random.uniform(range_info['min'], range_info['max'])
            sensor_data[sensor_type] = round(value, 2)
    
    return sensor_data

# =================================================================
# Request ID 추출 함수
# =================================================================
def extract_request_id(message):
    """
    메시지에서 Request ID를 추출
    예: "TEST_1_2025-10-17 15:30:00.123" -> 1
    """
    try:
        parts = message.split('_')
        if len(parts) >= 2:
            return int(parts[1])
    except:
        pass
    return None

# =================================================================
# 데이터 수신 함수
# =================================================================
def receive_data(ser):
    """RS485로부터 데이터를 수신"""
    try:
        if ser.in_waiting > 0:
            receive_time = datetime.now()
            data_bytes = ser.readline()
            message = data_bytes.decode('utf-8').strip()
            
            print(f"← 수신: '{message}' ({len(data_bytes)} bytes)")
            return message, receive_time
        else:
            return None, None
            
    except Exception as e:
        print(f"✗ 수신 오류: {e}")
        return None, None

# =================================================================
# 응답 전송 함수
# =================================================================
def send_response(ser, original_message, sensor_data, logger, request_id, receive_time):
    """
    수신한 메시지에 대한 응답을 전송하고 로그에 기록
    """
    try:
        send_time = datetime.now()
        
        data_parts = []
        for key, value in sensor_data.items():
            unit = SENSOR_RANGES[key]['unit'] if key in SENSOR_RANGES else ''
            data_parts.append(f"{key.upper()}:{value}{unit}")
        
        sensor_str = "_".join(data_parts)
        response = f"RESPONSE_{original_message}_{sensor_str}"
        
        data_bytes = (response + '\n').encode('utf-8')
        bytes_written = ser.write(data_bytes)
        ser.flush()
        
        # 로그에 트랜잭션 기록
        logger.log_transaction(
            request_id=request_id,
            receive_time=receive_time,
            send_time=send_time,
            message_received=original_message,
            message_sent=response,
            sensor_data=sensor_data
        )
        
        print(f"→ 응답: ({bytes_written} bytes)")
        print(f"  센서 데이터:")
        for key, value in sensor_data.items():
            unit = SENSOR_RANGES[key]['unit'] if key in SENSOR_RANGES else ''
            print(f"    - {key}: {value}{unit}")
        
        return True
        
    except Exception as e:
        print(f"✗ 응답 전송 오류: {e}")
        return False

# =================================================================
# 메인 서버 루프
# =================================================================
def main():
    """메인 실행 함수 - 서버 대기 루프"""
    print("="*60)
    print("RS485 Mock 통신 테스트 (수신측 - 가상 센서)")
    print("="*60)
    print(f"⚠ 주의: 이것은 가상 테스트입니다.")
    print(f"⚠ 실제 RS485 하드웨어는 필요하지 않습니다.")
    print("-"*60)
    
    # 데이터 로거 초기화
    logger = DataLogger(log_dir=LOG_DIR)
    
    # 시리얼 포트 초기화
    ser = init_serial()
    if ser is None:
        print("\n프로그램을 종료합니다.")
        return
    
    print("\n요청 대기 중... (Ctrl+C로 종료)")
    print("※ 이 프로그램을 먼저 실행한 후 통신 PC 프로그램을 실행하세요!")
    print("-"*60)
    
    request_count = 0
    
    try:
        while True:
            # 1. 데이터 수신 대기
            message, receive_time = receive_data(ser)
            
            if message:
                request_count += 1
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                
                # Request ID 추출
                request_id = extract_request_id(message)
                if request_id is None:
                    request_id = request_count
                
                print(f"\n[요청 #{request_count}] {timestamp}")
                print(f"✓ 요청 수신 성공")
                
                # 2. 가상 센서 데이터 생성
                sensor_data = generate_sensor_data()
                
                # 3. 응답 전송 (로깅 포함)
                if send_response(ser, message, sensor_data, logger, request_id, receive_time):
                    print(f"✓ 응답 전송 완료")
                else:
                    print(f"✗ 응답 전송 실패")
                
                print(f"  총 처리 횟수: {request_count}")
            
            # CPU 사용률 낮추기 위한 짧은 대기
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("서버 종료")
        print("="*60)
        print(f"총 처리 요청 수: {request_count}")
        
        # 로거 통계 출력
        print("\n" + "-"*60)
        print("로그 통계:")
        stats = logger.get_statistics()
        print(f"  총 처리: {stats['total']}")
        print(f"  평균 처리 시간: {stats['avg_processing_time']:.2f}ms")
        print(f"  최소 처리 시간: {stats['min_processing_time']:.2f}ms")
        print(f"  최대 처리 시간: {stats['max_processing_time']:.2f}ms")
        
    finally:
        # 리소스 정리
        logger.close()
        
        if ser and ser.is_open:
            ser.close()
            print(f"\nMock 시리얼 포트 {RS485_PORT} 닫기 완료")

if __name__ == "__main__":
    main()
