"""
=================================================================
파일명: test_simple.py
설명: DAQ 통신 간단 테스트 (통신 PC)
작성일: 2025-10-24
=================================================================
Mock Serial을 이용하여 DAQ 장치와 통신합니다.
주기적으로 센서 데이터를 요청하고 응답을 파싱하여 출력합니다.

실행 순서:
1. virtual-sensor-pc의 test_simple.py를 먼저 실행
2. 이 프로그램을 실행
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
    INTER_REQUEST_DELAY,
    SIMULATION_SENSORS
)

from src.daq_protocol import DAQProtocol
from src.data_parser import DataParser
from mock_serial import MockSerial, cleanup_mock_files

# =================================================================
# 메인 프로그램
# =================================================================
def main():
    print("="*70)
    print("DAQ 통신 간단 테스트 (통신 PC)")
    print("="*70)
    print(f"포트: {RS232_PORT}")
    print(f"속도: {BAUDRATE}bps")
    print(f"모드: {'Mock Serial' if USE_MOCK_SERIAL else '실제 RS232'}")
    print(f"테스트 센서: {[f'0x{s:02X}' for s in SIMULATION_SENSORS]}")
    print("-"*70)
    
    # 이전 통신 파일 정리
    if USE_MOCK_SERIAL:
        cleanup_mock_files()
        time.sleep(0.5)
    
    # 프로토콜 및 파서 초기화
    protocol = DAQProtocol()
    parser = DataParser()
    
    # Mock Serial 포트 열기
    try:
        ser = MockSerial(port=RS232_PORT, baudrate=BAUDRATE, timeout=5)
        print(f"✓ 포트 {RS232_PORT} 열기 성공")
    except Exception as e:
        print(f"✗ 포트 열기 실패: {e}")
        return
    
    print("\n준비 대기 중...")
    time.sleep(2)
    
    print("테스트 시작! (Ctrl+C로 종료)")
    print("="*70)
    
    test_count = 0
    success_count = 0
    sensor_index = 0
    
    try:
        while True:
            test_count += 1
            
            # 순환하면서 센서 타입 선택
            msg_type = SIMULATION_SENSORS[sensor_index]
            sensor_index = (sensor_index + 1) % len(SIMULATION_SENSORS)
            
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"\n[{timestamp}] 테스트 #{test_count}")
            print(f"센서: 0x{msg_type:02X} ({protocol.get_msg_type_name(msg_type)})")
            
            # 1. 요청 전송 (1 byte: MSG Type)
            ser.write(bytes([msg_type]))
            print(f"→ 요청 전송")
            
            # 2. 응답 수신 대기
            start_time = time.time()
            frame_buffer = bytearray()
            stx_found = False
            
            while time.time() - start_time < 5:  # 5초 타임아웃
                if ser.in_waiting > 0:
                    byte = ser.read(1)
                    
                    if not stx_found:
                        if byte[0] == 0x02:  # STX
                            stx_found = True
                            frame_buffer.append(byte[0])
                    else:
                        frame_buffer.append(byte[0])
                        if byte[0] == 0x03:  # ETX
                            break
                else:
                    time.sleep(0.01)
            
            if not stx_found or len(frame_buffer) < 7:
                print(f"✗ 타임아웃 (응답 없음)")
                continue
            
            frame = bytes(frame_buffer)
            print(f"← 응답 수신: {len(frame)} bytes")
            
            # 3. 프레임 파싱
            result = protocol.parse_frame(frame)
            
            if not result['valid']:
                print(f"✗ 파싱 오류: {result['error']}")
                continue
            
            # 4. 데이터 파싱
            parsed_data = parser.parse(result['msg_type'], result['data'])
            
            if 'error' in parsed_data:
                print(f"✗ 데이터 오류: {parsed_data['error']}")
                continue
            
            # 5. 센서 값 출력
            success_count += 1
            print(f"✓ 통신 성공")
            
            if 'voltage' in parsed_data:
                print(f"   전압: {parsed_data['voltage']['value']:.1f}V")
                print(f"   전류: {parsed_data['current']['value']:.2f}A")
                print(f"   전력: {parsed_data['power']['value']:.3f}kW")
            elif 'temperature' in parsed_data:
                print(f"   온도: {parsed_data['temperature']['value']:.1f}℃")
                print(f"   습도: {parsed_data['humidity']['value']:.1f}%")
            elif 'co2' in parsed_data:
                print(f"   CO2: {parsed_data['co2']['value']} ppm")
            
            # 6. 통계
            success_rate = (success_count / test_count) * 100
            print(f"   통계: {success_count}/{test_count} ({success_rate:.1f}%)")
            
            # 다음 테스트 전 대기
            time.sleep(INTER_REQUEST_DELAY)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("테스트 종료")
        print("="*70)
        print(f"총 테스트: {test_count}회")
        print(f"성공: {success_count}회")
        print(f"실패: {test_count - success_count}회")
        if test_count > 0:
            print(f"성공률: {(success_count/test_count)*100:.2f}%")
    
    finally:
        ser.close()
        print("\n포트 닫기 완료")

if __name__ == "__main__":
    main()
