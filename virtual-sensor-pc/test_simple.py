"""
=================================================================
파일명: test_simple.py
설명: DAQ 시뮬레이터 간단 테스트 (가상 센서 PC)
작성일: 2025-10-24
=================================================================
Mock Serial을 이용하여 DAQ 장치 역할을 수행합니다.
통신 PC로부터 요청을 받으면 센서 데이터를 생성하여 응답합니다.

실행 순서:
1. 이 프로그램을 먼저 실행 (서버 역할)
2. communication-pc의 test_simple.py 실행 (클라이언트 역할)
=================================================================
"""

import time
import sys
from pathlib import Path
from datetime import datetime

# 경로 설정
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Config 및 모듈 import
from config.config import (
    USE_MOCK_SERIAL,
    RS232_PORT,
    BAUDRATE,
    SENSOR_DATA_RANGES
)

from src.daq_simulator import DAQSimulator
from src.daq_protocol import DAQProtocol
from mock_serial import MockSerial

# =================================================================
# 메인 프로그램
# =================================================================
def main():
    print("="*70)
    print("DAQ 시뮬레이터 간단 테스트 (가상 센서 PC)")
    print("="*70)
    print(f"포트: {RS232_PORT}")
    print(f"속도: {BAUDRATE}bps")
    print(f"모드: {'Mock Serial' if USE_MOCK_SERIAL else '실제 RS232'}")
    print("-"*70)
    
    # 시뮬레이터 초기화
    simulator = DAQSimulator(SENSOR_DATA_RANGES)
    protocol = DAQProtocol()
    
    # Mock Serial 포트 열기
    try:
        ser = MockSerial(port=RS232_PORT, baudrate=BAUDRATE, timeout=1)
        print(f"✓ 포트 {RS232_PORT} 열기 성공")
    except Exception as e:
        print(f"✗ 포트 열기 실패: {e}")
        return
    
    print("\n요청 대기 중... (Ctrl+C로 종료)")
    print("=" * 70)
    
    request_count = 0
    
    try:
        while True:
            # 요청 수신 대기 (1 byte: MSG Type)
            if ser.in_waiting > 0:
                request = ser.read(1)
                msg_type = request[0]
                request_count += 1
                
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(f"\n[{timestamp}] 요청 #{request_count}")
                print(f"← MSG Type: 0x{msg_type:02X} ({protocol.get_msg_type_name(msg_type)})")
                
                # 응답 프레임 생성
                frame = simulator.create_response_frame(msg_type)
                
                if frame:
                    # 프레임 전송
                    ser.write(frame)
                    print(f"→ 응답 전송: {len(frame)} bytes")
                    print(f"   프레임: {frame.hex(' ').upper()[:60]}...")
                    
                    # 센서 값 출력
                    sensor_data = simulator.get_sensor_reading(msg_type)
                    if sensor_data and 'voltage' in sensor_data:
                        print(f"   센서: {sensor_data['voltage']['value']:.1f}V, "
                              f"{sensor_data['current']['value']:.2f}A, "
                              f"{sensor_data['power']['value']:.3f}kW")
                    elif sensor_data and 'temperature' in sensor_data:
                        print(f"   센서: {sensor_data['temperature']['value']:.1f}℃, "
                              f"{sensor_data['humidity']['value']:.1f}%")
                    elif sensor_data and 'co2' in sensor_data:
                        print(f"   센서: {sensor_data['co2']['value']} ppm")
                else:
                    print(f"✗ 지원하지 않는 MSG Type")
            
            time.sleep(0.01)  # CPU 사용률 낮추기
            
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("프로그램 종료")
        print("="*70)
        print(f"총 처리 요청: {request_count}회")
    
    finally:
        ser.close()
        print("포트 닫기 완료")

if __name__ == "__main__":
    main()
