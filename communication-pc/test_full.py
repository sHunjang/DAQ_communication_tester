"""
=================================================================
파일명: test_full.py
설명: DAQ 통신 신뢰도 측정 - 최종 통합 버전
작성일: 2025-10-24
=================================================================
전체 기능을 통합한 완전판:
1. Mock Serial 통신
2. DAQ 프로토콜 통신
3. 데이터 로깅 (CSV)
4. 신뢰도 계산
5. Excel 리포트 자동 생성

실행 순서:
1. virtual-sensor-pc/test_simple.py 먼저 실행
2. 이 프로그램 실행
3. 종료 시 자동으로 Excel 리포트 생성
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
    SIMULATION_SENSORS,
    LOG_DIR,
    OUTPUT_DIR
)

from src.daq_protocol import DAQProtocol
from src.data_parser import DataParser
from src.data_logger import DataLogger
from src.reliability_calculator import ReliabilityCalculator
from src.excel_exporter import ExcelExporter
from mock_serial import MockSerial, cleanup_mock_files


def main():
    print("="*70)
    print("DAQ 통신 신뢰도 측정 시스템 v1.0")
    print("="*70)
    print(f"포트: {RS232_PORT}")
    print(f"속도: {BAUDRATE}bps")
    print(f"모드: {'Mock Serial' if USE_MOCK_SERIAL else '실제 RS232'}")
    print(f"센서: {[f'0x{s:02X}' for s in SIMULATION_SENSORS]}")
    print("-"*70)
    
    # 이전 통신 파일 정리
    if USE_MOCK_SERIAL:
        print("Mock Serial 초기화 중...")
        cleanup_mock_files()
        time.sleep(0.5)
    
    # 모듈 초기화
    protocol = DAQProtocol()
    parser = DataParser()
    logger = DataLogger(log_dir=LOG_DIR)
    calculator = ReliabilityCalculator(target_reliability=99.0)
    
    print("✓ 모든 모듈 초기화 완료")
    
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
            logger.log_request(test_count, send_time, sensor_name)
            
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
                
                # 로깅
                logger.log_timeout(test_count, timeout_time)
                logger.log_error(f"테스트 #{test_count}: 타임아웃 ({sensor_name})")
                
                # 신뢰도 계산
                calculator.add_timeout(sensor_name)
                
                print(f"✗ 타임아웃")
                time.sleep(INTER_REQUEST_DELAY)
                continue
            
            frame = bytes(frame_buffer)
            receive_time = datetime.now()
            response_time_ms = (receive_time - send_time).total_seconds() * 1000
            
            print(f"← 응답 수신: {len(frame)} bytes ({response_time_ms:.2f}ms)")
            
            # 4. 프레임 파싱
            result = protocol.parse_frame(frame)
            
            if not result['valid']:
                # 로깅
                logger.log_response(test_count, receive_time, sensor_name, 
                                  success=False, note=result['error'])
                logger.log_error(f"테스트 #{test_count}: {result['error']}")
                
                # 신뢰도 계산
                calculator.add_test_result(sensor_name, success=False)
                
                print(f"✗ 파싱 오류: {result['error']}")
                time.sleep(INTER_REQUEST_DELAY)
                continue
            
            # 5. 데이터 파싱
            parsed_data = parser.parse(result['msg_type'], result['data'])
            
            if 'error' in parsed_data:
                # 로깅
                logger.log_response(test_count, receive_time, sensor_name,
                                  success=False, note=parsed_data['error'])
                logger.log_error(f"테스트 #{test_count}: {parsed_data['error']}")
                
                # 신뢰도 계산
                calculator.add_test_result(sensor_name, success=False)
                
                print(f"✗ 데이터 오류: {parsed_data['error']}")
                time.sleep(INTER_REQUEST_DELAY)
                continue
            
            # 6. 성공 처리
            # 로깅
            logger.log_response(test_count, receive_time, sensor_name, success=True)
            logger.log_sensor_data(receive_time, result['msg_type'], 
                                  sensor_name, parsed_data)
            
            # 신뢰도 계산
            calculator.add_test_result(sensor_name, success=True, 
                                      response_time_ms=response_time_ms)
            
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
            
            # 실시간 통계
            reliability = calculator.get_overall_reliability()
            response_stats = calculator.get_response_time_stats()
            
            print(f"   통계: 신뢰도 {reliability:.1f}% | "
                  f"평균응답 {response_stats['avg']:.0f}ms")
            
            time.sleep(INTER_REQUEST_DELAY)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("테스트 종료")
        print("="*70)
        
        # 최종 통계 출력
        calculator.print_summary()
        
    finally:
        # 리소스 정리
        logger.close()
        ser.close()
        
        # Excel 리포트 생성
        print("\n" + "="*70)
        print("Excel 리포트 생성 중...")
        print("="*70)
        
        try:
            # 로그 파일 경로
            log_dir = Path(LOG_DIR)
            today = datetime.now().strftime("%Y%m%d")
            call_log_file = log_dir / f"call_log_{today}.csv"
            sensor_log_file = log_dir / f"sensor_data_{today}.csv"
            
            # 신뢰도 리포트 가져오기
            reliability_report = calculator.get_summary_report()
            
            # Excel 생성
            exporter = ExcelExporter(output_dir=OUTPUT_DIR)
            output_file = exporter.create_report(
                call_log_file, 
                sensor_log_file, 
                reliability_report
            )
            
            print(f"\n✓ Excel 리포트 생성 완료!")
            print(f"파일: {output_file.absolute()}")
            
            # 파일 자동 열기 (Windows)
            try:
                import os
                os.startfile(output_file)
            except:
                pass
                
        except Exception as e:
            print(f"✗ Excel 생성 실패: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n포트 닫기 완료")
        print("="*70)


if __name__ == "__main__":
    main()
