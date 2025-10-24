"""
=================================================================
파일명: test_with_logging.py
설명: 로깅 기능이 추가된 DAQ 통신 테스트
작성일: 2025-10-24
=================================================================
"""

import time
import sys
from pathlib import Path
from datetime import datetime

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from config.config import (
    USE_MOCK_SERIAL,
    RS232_PORT,
    BAUDRATE,
    INTER_REQUEST_DELAY,
    SIMULATION_SENSORS
)

from src.daq_protocol import DAQProtocol
from src.data_parser import DataParser
from src.data_logger import DataLogger  # ← 로거 추가
from mock_serial import MockSerial, cleanup_mock_files

def main():
    print("="*70)
    print("DAQ 통신 테스트 (로깅 기능 포함)")
    print("="*70)
    print(f"포트: {RS232_PORT}")
    print(f"속도: {BAUDRATE}bps")
    print("-"*70)
    
    # 이전 통신 파일 정리
    if USE_MOCK_SERIAL:
        cleanup_mock_files()
        time.sleep(0.5)
    
    # 초기화
    protocol = DAQProtocol()
    parser = DataParser()
    logger = DataLogger(log_dir='logs')  # ← 로거 초기화
    
    # Mock Serial 포트 열기
    try:
        ser = MockSerial(port=RS232_PORT, baudrate=BAUDRATE, timeout=5)
        print(f"✓ 포트 {RS232_PORT} 열기 성공")
    except Exception as e:
        print(f"✗ 포트 열기 실패: {e}")
        logger.log_error(f"포트 열기 실패: {e}")
        return
    
    print("\n준비 대기 중...")
    time.sleep(2)
    
    print("테스트 시작! (Ctrl+C로 종료)")
    print("="*70)
    
    test_count = 0
    sensor_index = 0
    
    try:
        while True:
            test_count += 1
            msg_type = SIMULATION_SENSORS[sensor_index]
            sensor_index = (sensor_index + 1) % len(SIMULATION_SENSORS)
            
            timestamp = datetime.now()
            sensor_name = protocol.get_msg_type_name(msg_type)
            
            print(f"\n[{timestamp.strftime('%H:%M:%S.%f')[:-3]}] 테스트 #{test_count}")
            print(f"센서: 0x{msg_type:02X} ({sensor_name})")
            
            # 1. 요청 전송
            send_time = datetime.now()
            logger.log_request(test_count, send_time, sensor_name)  # ← 로그 기록
            
            ser.write(bytes([msg_type]))
            print(f"→ 요청 전송")
            
            # 2. 응답 수신
            start_time = time.time()
            frame_buffer = bytearray()
            stx_found = False
            
            while time.time() - start_time < 5:
                if ser.in_waiting > 0:
                    byte = ser.read(1)
                    
                    if not stx_found:
                        if byte[0] == 0x02:
                            stx_found = True
                            frame_buffer.append(byte[0])
                    else:
                        frame_buffer.append(byte[0])
                        if byte[0] == 0x03:
                            break
                else:
                    time.sleep(0.01)
            
            # 3. 타임아웃 체크
            if not stx_found or len(frame_buffer) < 7:
                timeout_time = datetime.now()
                logger.log_timeout(test_count, timeout_time)  # ← 타임아웃 로그
                logger.log_error(f"테스트 #{test_count}: 타임아웃")
                print(f"✗ 타임아웃")
                time.sleep(INTER_REQUEST_DELAY)
                continue
            
            frame = bytes(frame_buffer)
            receive_time = datetime.now()
            print(f"← 응답 수신: {len(frame)} bytes")
            
            # 4. 프레임 파싱
            result = protocol.parse_frame(frame)
            
            if not result['valid']:
                logger.log_response(test_count, receive_time, sensor_name, 
                                  success=False, note=result['error'])  # ← 실패 로그
                logger.log_error(f"테스트 #{test_count}: {result['error']}")
                print(f"✗ 파싱 오류: {result['error']}")
                time.sleep(INTER_REQUEST_DELAY)
                continue
            
            # 5. 데이터 파싱
            parsed_data = parser.parse(result['msg_type'], result['data'])
            
            if 'error' in parsed_data:
                logger.log_response(test_count, receive_time, sensor_name,
                                  success=False, note=parsed_data['error'])
                logger.log_error(f"테스트 #{test_count}: {parsed_data['error']}")
                print(f"✗ 데이터 오류: {parsed_data['error']}")
                time.sleep(INTER_REQUEST_DELAY)
                continue
            
            # 6. 성공 로그 기록
            logger.log_response(test_count, receive_time, sensor_name, success=True)  # ← 성공 로그
            logger.log_sensor_data(receive_time, result['msg_type'], 
                                  sensor_name, parsed_data)  # ← 센서 데이터 로그
            
            print(f"✓ 통신 성공")
            
            # 센서 값 출력
            if 'voltage' in parsed_data:
                print(f"   전압: {parsed_data['voltage']['value']:.1f}V")
                print(f"   전류: {parsed_data['current']['value']:.2f}A")
                print(f"   전력: {parsed_data['power']['value']:.3f}kW")
            elif 'temperature' in parsed_data:
                print(f"   온도: {parsed_data['temperature']['value']:.1f}℃")
                print(f"   습도: {parsed_data['humidity']['value']:.1f}%")
            elif 'co2' in parsed_data:
                print(f"   CO2: {parsed_data['co2']['value']} ppm")
            
            # 통계 출력
            stats = logger.get_statistics()
            success_rate = stats['success_rate']
            print(f"   통계: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
            
            time.sleep(INTER_REQUEST_DELAY)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("테스트 종료")
        print("="*70)
        
        # 최종 통계 출력
        stats = logger.get_statistics()
        print(f"총 테스트: {stats['total']}회")
        print(f"성공: {stats['success']}회")
        print(f"실패: {stats['failure']}회")
        print(f"타임아웃: {stats['timeout']}회")
        print(f"성공률: {stats['success_rate']:.2f}%")
        
        if stats['avg_response_time'] > 0:
            print(f"\n응답 시간:")
            print(f"  평균: {stats['avg_response_time']:.2f}ms")
            print(f"  최소: {stats['min_response_time']:.2f}ms")
            print(f"  최대: {stats['max_response_time']:.2f}ms")
    
    finally:
        logger.close()  # ← 로거 종료 (최종 통계 출력)
        ser.close()
        print("\n포트 닫기 완료")

if __name__ == "__main__":
    main()
