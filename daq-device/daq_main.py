"""
=================================================================
DAQ 장치 메인 프로그램 (v3)
=================================================================
"""

import time
import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from config.config import (
    RS232_PORT, RS232_BAUDRATE, RS232_TIMEOUT,
    RS485_PORT, RS485_BAUDRATE, RS485_TIMEOUT
)
from src.daq_relay import DAQRelay
from mock_serial import MockSerial, cleanup_mock_files


def main():
    print("="*70)
    print("DAQ 중개 장치 (v3)")
    print("="*70)
    print(f"RS232 (통신 PC): {RS232_PORT} @ {RS232_BAUDRATE}bps")
    print(f"RS485 (센서 PC): {RS485_PORT} @ {RS485_BAUDRATE}bps")
    print("-"*70)
    
    # Mock Serial 초기화
    cleanup_mock_files()
    time.sleep(0.5)
    
    # DAQ 중개자 초기화
    relay = DAQRelay()
    
    # 포트 열기
    try:
        # RS232: 통신 PC와 연결
        rs232_ser = MockSerial(port=RS232_PORT, baudrate=RS232_BAUDRATE, 
                               timeout=RS232_TIMEOUT)
        print(f"✓ RS232 포트 {RS232_PORT} 열기 성공")
        
        # RS485: 센서 PC와 연결
        rs485_ser = MockSerial(port=RS485_PORT, baudrate=RS485_BAUDRATE, 
                               timeout=RS485_TIMEOUT)
        print(f"✓ RS485 포트 {RS485_PORT} 열기 성공")
        
    except Exception as e:
        print(f"✗ 포트 열기 실패: {e}")
        return
    
    print("\n통신 PC로부터 요청 대기 중... (Ctrl+C로 종료)")
    print("="*70)
    
    try:
        while True:
            # 통신 PC로부터 요청 수신 (1 byte: MSG Type)
            if rs232_ser.in_waiting > 0:
                request = rs232_ser.read(1)
                msg_type = request[0]
                
                # 중개 처리
                success = relay.relay_request(rs232_ser, rs485_ser, msg_type)
                
                if success:
                    print("✓ 중개 성공")
                else:
                    print("✗ 중개 실패")
            
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("DAQ 장치 종료")
        print("="*70)
        
        stats = relay.get_statistics()
        print(f"총 중개: {stats['total_relays']}회")
        print("="*70)
    
    finally:
        rs232_ser.close()
        rs485_ser.close()
        print("포트 닫기 완료")


if __name__ == "__main__":
    main()
