"""
=================================================================
파일명: communication-pc/test_send.py
설명: RS485 통신 송신 테스트 프로그램
작성일: 2025-10-17
=================================================================
이 프로그램은 RS485를 통해 데이터를 전송하고 응답을 확인.
가상 센서 PC와 통신이 정상적으로 이루어지는지 테스트용
=================================================================
"""

import serial
import time
from datetime import datetime

# =================================================================
# config.py에서 설정값 불러오기
# =================================================================
from config.config import (
    RS485_PORT,
    BAUDRATE,
    BYTESIZE,
    PARITY,
    STOPBITS,
    TIMEOUT,
    INTER_REQUEST_DELAY,
    TARGET_RELIABILITY
)

# =================================================================
# 시리얼 포트 초기화 함수
# =================================================================
def init_serial():
    """
    시리얼 포트 OPEN & 초기화 함수
    config.py 설정값 사용
    
    Returns:
        serial.Serial: 초기화된 시리얼 포트 객체
        None: 포트 열기 실패 시
    """
    try:
        ser = serial.Serial(
            port=RS485_PORT,      # config.py에서 불러온 포트
            baudrate=BAUDRATE,    # config.py에서 불러온 속도
            bytesize=BYTESIZE,    # config.py에서 불러온 데이터 비트
            parity=PARITY,        # config.py에서 불러온 패리티
            stopbits=STOPBITS,    # config.py에서 불러온 정지 비트
            timeout=TIMEOUT       # config.py에서 불러온 타임아웃
        )

        if ser.is_open:
            print(f"✓ 시리얼 포트 {RS485_PORT} 열기 성공")
            print(f"  - Baudrate: {BAUDRATE}")
            print(f"  - Timeout: {TIMEOUT}초")
            print(f"  - Parity: {PARITY}, Stopbits: {STOPBITS}")
            return ser
        else:
            print(f"✗ 시리얼 포트 {RS485_PORT} 열기 실패")
            return None
            
    except serial.SerialException as e:
        print(f" ***** 시리얼 포트 오류: {e} *****")
        print(f" ====== config/config.py에서 RS485_PORT를 확인. ====== ")
        return None
    

# =================================================================
# 데이터 송신 함수
# =================================================================
def send_data(ser, message):
    """
    RS485로 데이터 전송 함수
    
    Args:
        ser: 시리얼 포트 객체
        message: 전송할 메세지 (문자열로 설정함.)
    
    Returns:
        bool: 전송 성공 여부 (False / True)
    """

    try:
        # 문자열을 바이트로 변환하여 전송
        data_bytes = (message + '\n').encode('utf-8')
        
        # 데이터 전송
        bytes_written = ser.write(data_bytes)
        
        # 전송 완료까지 대기 (버퍼 비워둠)
        ser.flush()
        
        print(f"-> 송신: '{message}' ({bytes_written} bytes)")
        return True
    
    except Exception as e:
        print(f" ***** 송신 오류 ***** ")
        print(f" ===== {e} =====")
        return False

# =================================================================
# 데이터 수신 함수
# =================================================================
def receive_data(ser) :
    """
    RS485 응답 데이터 수신 함수
    
    Args:
        ser: 시리얼 포트 객체
    
    Returns:
        str: 수신한 메세지 (없으면 None 반환)
    """
    
    try:
        # 수신할 버퍼에 데이터가 있는지 확인
        if ser.in_waiting > 0:
            # 개행 문자(\n)까지 읽어야 함
            data_bytes = ser.readline()
            
            # 바이트를 문자열로 변환
            message = data_bytes.decode('utf-8').strip()
            
            print(f"<- 수신: '{message}' ({len(data_bytes)} bytes)")
            return message
    
        else:
            # 타임아웃: 데이터가 없는 경우
            print(f" ***** 타임 아웃: {TIMEOUT}초 동안 응답 없음 ***** ")
            return None
    
    except Exception as e:
        print(f" ***** 수신 오류 ***** ")
        print(f" ===== {e} =====")
        return None


# =================================================================
# 메인 테스트 루프
# =================================================================
def main():
    """
    메인 실행 함수 - 통신 테스트
    """
    print("=" * 30)
    print("DAQ 통신 테스트 프로그램 (송신 PC)")
    print("=" * 30)
    
    print(f"설정값은 config/config.py에서 관리")
    print(f"목표 신뢰도: {TARGET_RELIABILITY}%")
    print("-" * 30)
    
    # Serial Port 초기화
    ser = init_serial()
    
    if ser is None:
        print("시리얼 포트 없어서 프로그램 종료.")
        return
    
    print(" ====== \n 테스트 시작 (Ctrl + C 로 종료하면 됨.) ====== ")
    
    test_count = 0      # Test 횟수 카운터
    success_count = 0      # 성공 횟수 카운터
    
    try:
        while True:
            test_count += 1
            
            # 현재 시간 메세지에 포함
            timeStamp = datetime.now().strftime("%Y-%m-%d | %H:%M:%S.%f")[:-3]
            message = f"TEST_{test_count}_{timeStamp}"
            
            print(f" \n[테스트 #{test_count}] | {timeStamp}")
            
            # 1. Data 통신
            if send_data(ser, message) :
                
                # 2. 응답 대기 및 수신
                response = receive_data(ser)
                
                # 3. 응답 확인
                if response:
                    success_count += 1
                    print(f" ====== 통신 성공 ====== ")

                    # 송신한 메세지와 수신한 메세지 비교
                    if message in response:
                        print(f" 데이터 일치 확인 ")
                    else:
                        print(f" 데이터 일치 X ")
                
                else:
                    print(f" ****** 통신 실패(응답 X) ****** ")
            
            # 4. 통계 출력
            success_rate = (success_count / test_count) * 100
            print(f" ====== 통계 : {success_count} / {test_count} 성공 ({success_rate:.1f}%)")
            
            
            # 목표 신뢰도와 비교
            if success_rate >= TARGET_RELIABILITY:
                print(f" ****** 신뢰도 {TARGET_RELIABILITY}% 이상임. ******")
            else:
                print(f" 신뢰도 {TARGET_RELIABILITY}%에 충족하지 못함.")
            
            
            # 5. 다음 테으스 전 대기 (config.py의 설정값 사용)
            time.sleep(INTER_REQUEST_DELAY)
    
    except KeyboardInterrupt:
        # Ctrl+C로 종료 시
        print("\n\n" + "="*60)
        print("테스트 종료")
        print("="*60)
        print(f"총 테스트 횟수: {test_count}")
        print(f"성공 횟수: {success_count}")
        print(f"실패 횟수: {test_count - success_count}")
        final_rate = (success_count/test_count)*100 if test_count > 0 else 0
        print(f"최종 성공률: {final_rate:.2f}%")
        
        
        # 목표 달성 여부
        if final_rate >= TARGET_RELIABILITY:
            print(f" ****** 목표 신뢰도 {TARGET_RELIABILITY}% 이상임. ******")
        else:
            print(f" 신뢰도 {TARGET_RELIABILITY}%에 충족하지 못함.")
    
    finally:
        # 프로그램 종료 시 포트 닫음
        if ser and ser.is_open:
            ser.close()
            print(f" \n====== 시리얼 포트 {RS485_PORT} 닫음. ====== ")


# =================================================================
# 프로그램 시작점
# =================================================================
if __name__ == "__main__" :
    main()