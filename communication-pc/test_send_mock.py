"""
=================================================================
파일명: communication-pc/test_send_mock.py
설명: Mock Serial을 사용한 RS485 송신 테스트 (로깅 기능 추가)
작성자: 개발팀
작성일: 2025-10-17
수정일: 2025-10-17 (로깅 기능 추가)
=================================================================
"""

import time
from datetime import datetime

# Mock Serial 클래스 import
from mock_serial import MockSerial as Serial, cleanup_mock_files

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
    INTER_REQUEST_DELAY,
    TARGET_RELIABILITY,
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
            print(f"  - 모드: 가상 테스트 모드 (실제 하드웨어 불필요)")
            return ser
        else:
            print(f"✗ Mock 시리얼 포트 {RS485_PORT} 열기 실패")
            return None
            
    except Exception as e:
        print(f"✗ 시리얼 포트 오류: {e}")
        return None

# =================================================================
# 데이터 송신 함수
# =================================================================
def send_data(ser, message, logger, request_id):
    """
    데이터를 RS485로 전송하고 로그에 기록
    
    Args:
        ser: 시리얼 포트 객체
        message: 전송할 메시지
        logger: DataLogger 객체
        request_id: 요청 ID
    
    Returns:
        datetime: 송신 시간
    """
    try:
        send_time = datetime.now()
        data_bytes = (message + '\n').encode('utf-8')
        bytes_written = ser.write(data_bytes)
        ser.flush()
        
        # 로그에 요청 기록
        logger.log_request(request_id, send_time, message)
        
        print(f"→ 송신: '{message}' ({bytes_written} bytes)")
        return send_time
        
    except Exception as e:
        print(f"✗ 송신 오류: {e}")
        logger.log_error(f"송신 오류: {e}")
        return None

# =================================================================
# 데이터 수신 함수
# =================================================================
def receive_data(ser, logger, request_id):
    """
    RS485로부터 응답 데이터를 수신하고 로그에 기록
    
    Args:
        ser: 시리얼 포트 객체
        logger: DataLogger 객체
        request_id: 요청 ID
    
    Returns:
        str: 수신한 메시지 (없으면 None)
    """
    try:
        receive_time = datetime.now()
        
        if ser.in_waiting > 0:
            data_bytes = ser.readline()
            message = data_bytes.decode('utf-8').strip()
            
            # 로그에 응답 기록
            logger.log_response(request_id, receive_time, message, success=True)
            
            print(f"← 수신: '{message}' ({len(data_bytes)} bytes)")
            return message
        else:
            # 타임아웃
            timeout_time = datetime.now()
            logger.log_timeout(request_id, timeout_time)
            
            print(f"✗ 타임아웃: {TIMEOUT}초 동안 응답 없음")
            return None
            
    except Exception as e:
        print(f"✗ 수신 오류: {e}")
        logger.log_error(f"수신 오류: {e}")
        return None

# =================================================================
# 메인 테스트 루프
# =================================================================
def main():
    """메인 실행 함수"""
    print("="*60)
    print("RS485 Mock 통신 테스트 프로그램 (송신측)")
    print("="*60)
    print(f"⚠ 주의: 이것은 가상 테스트입니다.")
    print(f"⚠ 실제 RS485 하드웨어는 필요하지 않습니다.")
    print(f"⚠ 가상 센서 PC의 test_receive_mock.py도 실행하세요.")
    print(f"목표 신뢰도: {TARGET_RELIABILITY}%")
    print("-"*60)
    
    # 통신 파일 정리
    print("이전 통신 파일 정리")
    cleanup_mock_files()
    time.sleep(0.5)
    
    # 데이터 로거 초기화
    logger = DataLogger(log_dir=LOG_DIR)
    
    # 시리얼 포트 초기화
    ser = init_serial()
    if ser is None:
        print("\n프로그램을 종료합니다.")
        return
    
    print("\n테스트 시작 (Ctrl+C로 종료)")
    print("※ 가상 센서 PC 프로그램이 먼저 실행되어야 합니다!")
    print("-"*60)
    
    # 가상 센서 PC 실행 대기
    print("\n가상 센서 PC 준비 대기 중...")
    time.sleep(2)
    print("테스트 시작!\n")
    
    test_count = 0
    success_count = 0
    
    try:
        while True:
            test_count += 1
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            message = f"TEST_{test_count}_{timestamp}"
            
            print(f"\n[테스트 #{test_count}] {timestamp}")
            
            # 1. 데이터 송신 (로깅 포함)
            send_time = send_data(ser, message, logger, test_count)
            
            if send_time:
                # 2. 응답 대기 및 수신 (로깅 포함)
                response = receive_data(ser, logger, test_count)
                
                # 3. 응답 확인
                if response:
                    success_count += 1
                    print(f"✓ 통신 성공")
                    
                    if message in response:
                        print(f"✓ 데이터 일치 확인")
                    else:
                        print(f"⚠ 데이터 불일치")
                        logger.log_error(f"데이터 불일치: {message} != {response}")
                else:
                    print(f"✗ 통신 실패 (응답 없음)")
            
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
        print(f"  평균 응답 시간: {stats['avg_response_time']:.2f}ms")
        print(f"  최소 응답 시간: {stats['min_response_time']:.2f}ms")
        print(f"  최대 응답 시간: {stats['max_response_time']:.2f}ms")
        
    finally:
        # 리소스 정리
        logger.close()
        
        if ser and ser.is_open:
            ser.close()
            print(f"\nMock 시리얼 포트 {RS485_PORT} 닫기 완료")

if __name__ == "__main__":
    main()
