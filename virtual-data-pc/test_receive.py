"""
=================================================================
파일명: virtual-sensor-pc/test_receive.py
설명: RS485 통신 수신 및 응답 테스트 프로그램
작성일: 2025-10-17
=================================================================
"""

import serial
import time
import random
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
    SENSOR_TYPES,
    SENSOR_RANGES,
    DATA_GENERATION_DELAY_MS
)


# =================================================================
# 시리얼 포트 초기화 함수
# =================================================================
def init_serial():
    """
    시리얼 포트 열고 & 초기화 함수
    config.py 설정값 사용
    
    Returns:
        serial.Serial: 초기화된 시리얼 포트 객체
        None: 포트 열기 실패 반환 됨.
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
            print(f" ====== 시리얼 포트 {RS485_PORT} 열기 성공 ====== ")
            print(f"  - Baudrate: {BAUDRATE}")
            print(f"  - Timeout: {TIMEOUT}초")
            print(f"  - Parity: {PARITY}, Stopbits: {STOPBITS}")
            print(f"  - 지원 센서: {', '.join(SENSOR_TYPES)}")
            return ser
        else:
            print(f"✗ 시리얼 포트 {RS485_PORT} 열기 실패")
            return None
            
    except serial.SerialException as e:
        print(f" ****** 시리얼 포트 오류 ****** ")
        print(f" ====== {e} ====== ")
        print(f" config/config.py에서 RS485_PORT를 확인 ")
        return None


# =================================================================
# 가상 센서 데이터 생성 함수
# =================================================================
def generate_sensor_data():
    """
    가상 센서 데이터 생성 함수
    config.py 내 SENSOR_RANGES 설정값 사용
    
    Returns:
        dict: 센서 데이터 (온도, 습도, 압력, 전압 등)
    """
    
    # 센서 데이터 생성 지연 시뮬레이션
    time.sleep(DATA_GENERATION_DELAY_MS / 1000.0)
    
    # 각 센서의 범위 내에서 랜덤 값 생성
    sensor_data = {}
    
    for sensor_type in SENSOR_TYPES:
        if sensor_type in SENSOR_RANGES:
            range_info = SENSOR_RANGES[sensor_type]
            value = random.uniform(range_info['min'], range_info['max'])
            sensor_data[sensor_type] = round(value, 2)
    
    return sensor_data


# =================================================================
# 데이터 수신 함수
# =================================================================
def receive_data(ser):
    """
    RS485로부터 데이터를 수신하는 함수
    
    Args:
        ser: 시리얼 포트 객체
    
    Returns:
        str: 수신한 메세지 (없으면 None 반환)
    """
    
    try:
        # 수신 버퍼에 데이터가 있는지 확인
        if ser.in_waiting > 0:
            
            # 개행 문자(\n)까지 읽음
            data_bytes = ser.readline()
            
            # 바이트를 문자열로 변환
            message = data_bytes.decode('utf-8').strip()
            
            print(f"<- 수신: '{message}' ({len(data_bytes)} bytes)")
            
            return message
        
        else:
            return None
    
    except Exception as e:
        print(f" ****** 수신 오류 ******")
        print(f" ====== {e} ======= ")
        return None


# =================================================================
# 응답 전송 함수
# =================================================================
def send_response(ser, original_message, sensor_data):
    """
    수신한 메세지에 대한 응답 전송 함수
    
    Args:
        ser: 시리얼 포트 객체
        original_message: 수신 원본 메세지
        sensor_data: 센서 데이터 딕셔너리
        
    Returns:
        bool: 전공 성공 여부 (False / True)
    """
    
    try:
        # 응답 메세지 생성 -- 원본 + 센서 데이터
        data_parts = []
        
        for key, value in sensor_data.items():
            unit = SENSOR_RANGES[key]['unit'] if key in SENSOR_RANGES else ''
            data_parts.append(f"{key.upper()} : {value}{unit}")
            
        sensor_str = "_".join(data_parts)
        response = f"RESPONSE_{original_message}_{sensor_str}"
        
        # 문자열을 바이트로 변환하여 전송
        data_bytes = (response + '\n').encode('utf-8')
        
        
        # 데이터 전송
        bytes_written = ser.write(data_bytes)
        
        # 데이터 전송 완료까지 대기
        ser.flush()
        
        print(f"-> 응답: ({bytes_written} bytes)")
        print(f" ***** 센서 데이터: *****")
        
        for key, value in sensor_data.items():
            unit = SENSOR_RANGES[key]['unit'] if key in SENSOR_RANGES else ''
            print(f"    - {key}: {value}{unit}     ")
        
        
        return True
    
    except Exception as e:
        print(f" ****** 응답 전송 오류 *******")
        print(f" ====== {e} ====== ")
        return False


# =================================================================
# 메인 서버 루프
# =================================================================
def main():
    """
    메인 실행 함수 - 통신 테스트
    """
    print("=" * 30)
    print("DAQ 통신 테스트 프로그램 (송신 PC)")
    print("=" * 30)
    

    # 시리얼 포트 초기화
    ser = init_serial()
    
    if ser in None:
        print(" ====== \n 프로그램 종료 ====== ")
        return 
    
    print(" \n 요청 대기 중... (Ctrl + C로 종료) ")
    print("=" * 30)
    
    test_count = 0
    request_count = 0       # 요청 처리 횟수 카운터
    
    try:
        while True:
            
            # 1. 데이터 수신 대기
            message = receive_data(ser)
            
            if message:
                request_count += 1
                timeStamp = datetime.now().strftime("%Y-%m-%d | %H:%M:%S.%f")[:-3]
                
                print(f" \n [요청 #{request_count}] {timeStamp} ")
                print(f" 요청 수신 됨 ")
                
                
                # 2. 가상 센서 데이터 생성
                sensor_data = generate_sensor_data()
                
                # 3. 응답 전송
                if send_response(ser, message, sensor_data):
                    print(f" ====== 응답 전송 완료 ====== ")
                    
                else:
                    print(f" ====== 응답 전송 실패 ====== ")
                
                print(f" ****** 총 처리 횟수: {request_count} ****** ")
            
            # CPU 사용률로 인한 대기
            time.sleep(0.1)     # 0.1초 대기
    
    except KeyboardInterrupt:
        # Ctrl+C로 종료 시
        print("\n\n" + "="*60)
        print("서버 종료")
        print("="*60)
        print(f"총 처리 요청 수: {request_count}")
        
    finally:
        # 프로그램 종료 시 포트 닫기
        if ser and ser.is_open:
            ser.close()
            print(f" ****** \n Serial Port {RS485_PORT} 닫음. ****** ")


# =================================================================
# 프로그램 시작점
# =================================================================
if __name__ == "__main__":
    main()