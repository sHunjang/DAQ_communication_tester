"""
=================================================================
파일명: test_mock_simple.py
설명: Mock Serial 단순 테스트 (단일 프로그램)
=================================================================
하나의 프로그램 안에서 송신과 수신을 모두 테스트합니다.
"""

import time
import threading
from mock_serial import MockSerial, cleanup_mock_files

def sender_thread():
    """송신 스레드"""
    print("\n[송신 스레드] 시작")
    time.sleep(1)  # 수신 준비 대기
    
    # COM3 포트로 송신
    ser_tx = MockSerial(port='COM3', baudrate=9600, timeout=5)
    
    for i in range(3):
        message = f"TEST_{i+1}\n"
        print(f"\n[송신] 메시지 전송: {message.strip()}")
        ser_tx.write(message.encode('utf-8'))
        time.sleep(1)
    
    ser_tx.close()
    print("\n[송신 스레드] 종료")

def receiver_thread():
    """수신 스레드"""
    print("\n[수신 스레드] 시작")
    
    # COM4 포트로 수신
    ser_rx = MockSerial(port='COM4', baudrate=9600, timeout=2)
    
    for i in range(3):
        print(f"\n[수신] 메시지 대기 중...")
        data = ser_rx.readline()
        
        if data:
            message = data.decode('utf-8').strip()
            print(f"[수신] 메시지 수신: {message}")
            
            # 응답 전송
            response = f"RESPONSE_{message}\n"
            print(f"[수신] 응답 전송: {response.strip()}")
            ser_rx.write(response.encode('utf-8'))
        else:
            print(f"[수신] 타임아웃!")
    
    ser_rx.close()
    print("\n[수신 스레드] 종료")

def main():
    print("="*60)
    print("Mock Serial 단순 테스트")
    print("="*60)
    
    # 이전 파일 정리
    cleanup_mock_files()
    time.sleep(0.5)
    
    # 송신과 수신 스레드 시작
    rx_thread = threading.Thread(target=receiver_thread)
    tx_thread = threading.Thread(target=sender_thread)
    
    rx_thread.start()
    tx_thread.start()
    
    # 스레드 종료 대기
    rx_thread.join()
    tx_thread.join()
    
    print("\n" + "="*60)
    print("테스트 완료")
    print("="*60)
    
    # 파일 정리
    time.sleep(1)
    cleanup_mock_files()

if __name__ == "__main__":
    main()
