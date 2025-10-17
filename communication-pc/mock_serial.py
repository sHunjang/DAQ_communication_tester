"""
=================================================================
파일명: mock_serial.py (수정 버전 - 절대 경로)
설명: 파일 기반 RS485 시리얼 포트 Mock 클래스
작성자: 개발팀
작성일: 2025-10-17
수정일: 2025-10-17 (절대 경로 사용)
=================================================================
독립된 Python 프로세스 간 통신을 위해 파일 시스템을 사용합니다.
시스템 임시 폴더를 사용하여 어느 위치에서 실행해도 통신 가능합니다.
실제 시리얼 포트처럼 동작하지만 하드웨어가 필요없습니다.
=================================================================
"""

import os
import time
import threading
import tempfile
from collections import deque
from pathlib import Path

class MockSerial:
    """
    pyserial.Serial 클래스를 모의하는 Mock 객체
    파일 시스템을 이용하여 독립 프로세스 간 통신을 시뮬레이션합니다.
    """
    
    def __init__(self, port=None, baudrate=9600, bytesize=8, 
                 parity='N', stopbits=1, timeout=1):
        """
        Mock 시리얼 포트 초기화
        
        Args:
            port: 포트 이름 (예: 'COM3', 'COM4')
            baudrate: 통신 속도
            bytesize: 데이터 비트
            parity: 패리티 체크
            stopbits: 정지 비트
            timeout: 읽기 타임아웃 (초)
        """
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self._is_open = True
        
        # 내부 버퍼 (수신 데이터 저장)
        self._read_buffer = deque()
        
        # 포트 쌍 매핑 (COM3 <-> COM4 연결)
        self._port_pairs = {
            'COM3': 'COM4',
            'COM4': 'COM3',
            'COM1': 'COM2',
            'COM2': 'COM1',
        }
        
        # =================================================================
        # 통신 파일 경로 설정 (시스템 임시 폴더 사용 - 절대 경로)
        # =================================================================
        temp_dir = Path(tempfile.gettempdir())
        self._comm_dir = temp_dir / 'mock_serial_comm'
        self._comm_dir.mkdir(exist_ok=True)
        
        print(f"[MockSerial] 통신 폴더: {self._comm_dir}")
        
        # 내가 읽을 파일 (상대방이 쓰는 파일)
        self._read_file = self._comm_dir / f"{port}_rx.dat"
        
        # 내가 쓸 파일 (상대방이 읽는 파일)
        if port in self._port_pairs:
            paired_port = self._port_pairs[port]
            self._write_file = self._comm_dir / f"{paired_port}_rx.dat"
        else:
            self._write_file = None
        
        # 파일 초기화 (내가 읽을 파일만 초기화)
        if self._read_file.exists():
            self._read_file.unlink()  # 기존 파일 삭제
        self._read_file.touch()  # 빈 파일 생성
        
        # 마지막으로 읽은 파일 위치 저장
        self._last_read_pos = 0
        
        # 파일 모니터링 스레드 시작
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_file, daemon=True)
        self._monitor_thread.start()
        
        print(f"[MockSerial] 포트 {port} 초기화 완료")
        print(f"[MockSerial] 연결된 포트: {self._port_pairs.get(port, 'None')}")
        print(f"[MockSerial] 읽기 파일: {self._read_file}")
        print(f"[MockSerial] 쓰기 파일: {self._write_file}")
    
    @property
    def is_open(self):
        """포트가 열려있는지 확인"""
        return self._is_open
    
    def write(self, data):
        """
        데이터를 쌍으로 연결된 포트로 전송
        실제로는 상대방의 수신 파일에 기록합니다.
        
        Args:
            data: 전송할 바이트 데이터
            
        Returns:
            int: 전송한 바이트 수
        """
        if not self._is_open:
            raise Exception("포트가 닫혀있습니다")
        
        if not self._write_file:
            print(f"[MockSerial] 경고: {self.port}에 연결된 쌍 포트가 없습니다")
            return len(data)
        
        # 전송 지연 시뮬레이션 (실제 RS485의 전송 시간)
        # 9600 baud = 960 bytes/sec ≈ 0.001초/byte
        transmission_delay = len(data) / (self.baudrate / 10)
        time.sleep(transmission_delay)
        
        # 상대방의 수신 파일에 데이터 추가 (append mode)
        try:
            with open(self._write_file, 'ab') as f:
                f.write(data)
                f.flush()  # 즉시 디스크에 기록
                os.fsync(f.fileno())  # 운영체제 레벨에서도 강제 flush
            
            paired_port = self._port_pairs.get(self.port, 'Unknown')
            print(f"[MockSerial] {self.port} -> {paired_port}: {len(data)} bytes 전송")
            
        except Exception as e:
            print(f"[MockSerial] 쓰기 오류: {e}")
        
        return len(data)
    
    def read(self, size=1):
        """
        지정된 크기만큼 데이터를 읽기
        
        Args:
            size: 읽을 바이트 수
            
        Returns:
            bytes: 읽은 데이터
        """
        if not self._is_open:
            raise Exception("포트가 닫혀있습니다")
        
        # 버퍼에서 데이터 읽기
        result = bytearray()
        for _ in range(min(size, len(self._read_buffer))):
            result.append(self._read_buffer.popleft())
        
        return bytes(result)
    
    def readline(self):
        """
        개행 문자(\n)까지 데이터를 읽기
        
        Returns:
            bytes: 읽은 데이터 (개행 문자 포함)
        """
        if not self._is_open:
            raise Exception("포트가 닫혀있습니다")
        
        start_time = time.time()
        result = bytearray()
        
        while True:
            # 타임아웃 체크
            if time.time() - start_time > self.timeout:
                break
            
            # 버퍼에 데이터가 있으면 읽기
            if self._read_buffer:
                byte = self._read_buffer.popleft()
                result.append(byte)
                
                # 개행 문자를 만나면 종료
                if byte == ord('\n'):
                    break
            else:
                # 버퍼가 비어있으면 잠시 대기
                time.sleep(0.01)
        
        return bytes(result)
    
    @property
    def in_waiting(self):
        """
        읽을 수 있는 데이터의 바이트 수 반환
        
        Returns:
            int: 버퍼에 있는 바이트 수
        """
        return len(self._read_buffer)
    
    def flush(self):
        """출력 버퍼를 비움 (전송 완료 대기)"""
        # Mock에서는 즉시 전송되므로 별도 처리 불필요
        pass
    
    def close(self):
        """포트를 닫음"""
        self._is_open = False
        self._monitoring = False
        
        # 모니터링 스레드 종료 대기
        if self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=1)
        
        print(f"[MockSerial] 포트 {self.port} 닫기 완료")
    
    def _monitor_file(self):
        """
        파일을 주기적으로 모니터링하여 새 데이터를 버퍼로 읽어오는 스레드
        (내부 메서드 - 백그라운드에서 자동 실행)
        """
        while self._monitoring:
            try:
                # 파일이 존재하고 크기가 증가했는지 확인
                if self._read_file.exists():
                    file_size = self._read_file.stat().st_size
                    
                    # 새로운 데이터가 있으면 읽기
                    if file_size > self._last_read_pos:
                        with open(self._read_file, 'rb') as f:
                            # 마지막으로 읽은 위치로 이동
                            f.seek(self._last_read_pos)
                            
                            # 새로운 데이터 읽기
                            new_data = f.read()
                            
                            # 버퍼에 추가
                            for byte in new_data:
                                self._read_buffer.append(byte)
                            
                            # 읽은 위치 업데이트
                            self._last_read_pos = file_size
                            
                            if len(new_data) > 0:
                                print(f"[MockSerial] {self.port} 버퍼에 {len(new_data)} bytes 추가됨")
                
            except Exception as e:
                if self._monitoring:  # 종료 중이 아닐 때만 에러 출력
                    print(f"[MockSerial] 모니터링 오류: {e}")
            
            # CPU 사용률 낮추기
            time.sleep(0.05)  # 50ms마다 체크
    
    def __repr__(self):
        """객체의 문자열 표현"""
        return (f"MockSerial(port='{self.port}', baudrate={self.baudrate}, "
                f"is_open={self._is_open})")
    
    def __del__(self):
        """객체 소멸자 - 리소스 정리"""
        if hasattr(self, '_monitoring'):
            self._monitoring = False
        if hasattr(self, '_is_open') and self._is_open:
            try:
                self.close()
            except:
                pass


# =================================================================
# 편의 함수: Serial 클래스를 MockSerial로 대체
# =================================================================
def get_serial_class(use_mock=True):
    """
    실제 Serial 또는 MockSerial 클래스를 반환
    
    Args:
        use_mock: True면 MockSerial, False면 실제 serial.Serial 반환
        
    Returns:
        Serial 클래스
    """
    if use_mock:
        return MockSerial
    else:
        import serial
        return serial.Serial


# =================================================================
# 유틸리티: 통신 파일 정리
# =================================================================
def cleanup_mock_files():
    """
    Mock Serial 통신에 사용된 임시 파일들을 모두 삭제합니다.
    프로그램 시작 전이나 종료 후 호출하면 좋습니다.
    """
    temp_dir = Path(tempfile.gettempdir())
    comm_dir = temp_dir / 'mock_serial_comm'
    
    print(f"[MockSerial] 정리 대상 폴더: {comm_dir}")
    
    if comm_dir.exists():
        for file in comm_dir.glob('*.dat'):
            try:
                file.unlink()
                print(f"[MockSerial] 파일 삭제: {file.name}")
            except Exception as e:
                print(f"[MockSerial] 파일 삭제 실패: {file.name}, {e}")
        
        try:
            comm_dir.rmdir()
            print(f"[MockSerial] 디렉토리 삭제 완료")
        except Exception as e:
            pass  # 디렉토리가 비어있지 않으면 무시


# =================================================================
# 테스트 코드 (이 파일을 직접 실행할 때만 동작)
# =================================================================
if __name__ == "__main__":
    print("="*60)
    print("Mock Serial 모듈 단독 테스트")
    print("="*60)
    
    # 이전 파일 정리
    cleanup_mock_files()
    time.sleep(0.5)
    
    # COM3 포트 생성
    print("\n1. COM3 포트 생성 테스트")
    ser = MockSerial(port='COM3', baudrate=9600, timeout=2)
    print(f"생성된 포트: {ser}")
    
    time.sleep(1)
    
    # 데이터 전송 테스트
    print("\n2. 데이터 전송 테스트")
    test_data = b"Hello Mock Serial\n"
    bytes_written = ser.write(test_data)
    print(f"전송 완료: {bytes_written} bytes")
    
    time.sleep(1)
    
    # 포트 닫기
    print("\n3. 포트 닫기 테스트")
    ser.close()
    
    time.sleep(1)
    
    # 파일 정리
    print("\n4. 파일 정리 테스트")
    cleanup_mock_files()
    
    print("\n" + "="*60)
    print("테스트 완료!")
    print("="*60)
