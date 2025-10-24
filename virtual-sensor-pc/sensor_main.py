"""
=================================================================
센서 PC 메인 프로그램 (v3)
=================================================================
"""

import time
import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from config.config import RS485_PORT, BAUDRATE, SENSOR_RANGES
from src.sensor_simulator import SensorSimulator
from mock_serial import MockSerial, cleanup_mock_files


def main():
    print("="*70)
    print("센서 PC 시뮬레이터 (v3)")
    print("="*70)
    print(f"RS485 포트: {RS485_PORT}")
    print("-"*70)
    
    # Mock Serial 초기화
    cleanup_mock_files()
    time.sleep(0.5)
    
    # 센서 시뮬레이터 초기화
    simulator = SensorSimulator(SENSOR_RANGES)
    
    # 포트 열기
    try:
        ser = MockSerial(port=RS485_PORT, baudrate=BAUDRATE, timeout=1)
        print(f"✓ 포트 {RS485_PORT} 열기 성공")
    except Exception as e:
        print(f"✗ 포트 열기 실패: {e}")
        return
    
    print("\nDAQ로부터 요청 대기 중... (Ctrl+C로 종료)")
    print("="*70)
    
    request_count = 0
    
    try:
        while True:
            # DAQ로부터 요청 수신 (2 bytes: MSG Type + Device ID)
            if ser.in_waiting >= 2:
                request = ser.read(2)
                msg_type = request[0]
                device_id = request[1]
                
                request_count += 1
                
                timestamp = time.strftime("%H:%M:%S")
                print(f"\n[{timestamp}] 요청 #{request_count}")
                print(f"← MSG Type: 0x{msg_type:02X}, Device ID: {device_id}")
                
                # 센서 데이터 생성
                sensor_data = simulator.generate_sensor_data(msg_type)
                
                if sensor_data:
                    # DAQ로 응답 (Raw 데이터만)
                    ser.write(sensor_data)
                    print(f"→ 응답 전송: {len(sensor_data)} bytes")
                else:
                    print(f"✗ 지원하지 않는 센서 타입")
            
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("센서 PC 종료")
        print(f"총 처리: {request_count}회")
        print("="*70)
    
    finally:
        ser.close()


if __name__ == "__main__":
    main()
