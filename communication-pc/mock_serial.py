"""
=================================================================
파일명: mock_serial.py
설명: 파일 기반 가상 시리얼 포트 구현
작성일: 2025-10-24
=================================================================
RS485/RS232 하드웨어 없이 통신을 시뮬레이션하기 위한 Mock 클래스
파일 시스템을 이용하여 독립된 프로세스 간 통신을 구현

주요 기능:
- pyserial.Serial과 동일한 API 제공
- 파일 기반 프로세스 간 통신
- COM3 ↔ COM4 포트 쌍 자동 매핑
- 실제 전송 지연 시뮬레이션 (9600bps 기준)

사용 예시:
    ser = MockSerial(port='COM3', baudrate=9600, timeout=1)
    ser.write(b'Hello')
    data = ser.read(10)
    ser.close()
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
    pyserial.Serial 클래스를 모방하는 가상 시리얼 포트
    
    실제 시리얼 포트와 동일한 인터페이스를 제공하면서,
    파일 시스템을 이용하여 독립된 프로세스 간 통신을 구현
    """
    
    def __init__(self, port=None, baudrate=9600, bytesize=8, 
                 parity='N', stopbits=1, timeout=1):
        """
        Mock 시리얼 포트 초기화
        
        Args:
            port (str): 포트 이름 (예: 'COM3', 'COM4')
            baudrate (int): 통신 속도 (bps) - 전송 지연 계산에 사용
            bytesize (int): 데이터 비트 수
            parity (str): 패리티 체크 ('N': None, 'E': Even, 'O': Odd)
            stopbits (int): 정지 비트 수
            timeout (float): 읽기 타임아웃 (초 단위)
        """
        # 시리얼 포트 기본 속성 저장
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self._is_open = True
        
        # 수신 데이터를 저장하는 내부 버퍼 (FIFO 큐)
        self._read_buffer = deque()
        
        # 포트 쌍 매핑 정의
        # COM3로 보낸 데이터는 COM4가 받고, COM4로 보낸 데이터는 COM3가 받음
        self._port_pairs = {
            'COM3': 'COM4',  # 통신 PC ↔ DAQ
            'COM4': 'COM3',
            'COM5': 'COM6',  # DAQ ↔ 센서 PC
            'COM6': 'COM5',
        }
        
        # =================================================================
        # 통신 파일 경로 설정 (시스템 임시 폴더 사용)
        # =================================================================
        # 어느 위치에서 실행하든 같은 폴더를 사용하도록 절대 경로 지정
        temp_dir = Path(tempfile.gettempdir())  # Windows: C:\Users\...\AppData\Local\Temp
        self._comm_dir = temp_dir / 'mock_serial_comm'
        self._comm_dir.mkdir(exist_ok=True)  # 폴더가 없으면 생성
        
        print(f"[MockSerial] 통신 폴더: {self._comm_dir}")
        
        # 내가 읽을 파일 = 상대방이 쓰는 파일
        # 예: COM3이 읽을 파일 = COM3_rx.dat (COM4가 여기에 씀)
        self._read_file = self._comm_dir / f"{port}_rx.dat"
        
        # 내가 쓸 파일 = 상대방이 읽는 파일
        # 예: COM3이 쓸 파일 = COM4_rx.dat (COM4가 여기서 읽음)
        if port in self._port_pairs:
            paired_port = self._port_pairs[port]
            self._write_file = self._comm_dir / f"{paired_port}_rx.dat"
        else:
            self._write_file = None
            print(f"[MockSerial] 경고: {port}에 대응하는 쌍 포트가 없습니다")
        
        # 읽기 파일 초기화 (기존 데이터 제거)
        if self._read_file.exists():
            self._read_file.unlink()  # 파일 삭제
        self._read_file.touch()  # 빈 파일 생성
        
        # 파일을 마지막으로 읽은 위치 (바이트 오프셋)
        self._last_read_pos = 0
        
        # 파일 모니터링 스레드 시작
        # 백그라운드에서 계속 파일을 감시하다가 새 데이터가 있으면 버퍼에 추가
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_file, daemon=True)
        self._monitor_thread.start()
        
        # 초기화 완료 메시지
        print(f"[MockSerial] 포트 {port} 초기화 완료")
        print(f"[MockSerial] 연결된 포트: {self._port_pairs.get(port, 'None')}")
        print(f"[MockSerial] 읽기 파일: {self._read_file.name}")
        print(f"[MockSerial] 쓰기 파일: {self._write_file.name if self._write_file else 'None'}")
    
    @property
    def is_open(self):
        """
        포트가 열려있는지 확인
        
        Returns:
            bool: 열려있으면 True, 닫혀있으면 False
        """
        return self._is_open
    
    def write(self, data):
        """
        데이터를 쌍 포트로 전송 (실제로는 상대방의 읽기 파일에 기록)
        
        Args:
            data (bytes): 전송할 바이트 데이터
            
        Returns:
            int: 전송한 바이트 수
            
        Raises:
            Exception: 포트가 닫혀있으면 예외 발생
        """
        # 포트가 닫혀있으면 에러
        if not self._is_open:
            raise Exception("포트가 닫혀있습니다")
        
        # 쌍 포트가 없으면 경고만 하고 진행
        if not self._write_file:
            print(f"[MockSerial] 경고: {self.port}에 연결된 쌍 포트가 없습니다")
            return len(data)
        
        # =================================================================
        # 실제 시리얼 통신의 전송 지연 시뮬레이션
        # =================================================================
        # 9600 baud = 초당 960 바이트 전송 가능 (1 바이트당 약 0.001초)
        # 115200 baud = 초당 11520 바이트 전송 가능
        transmission_delay = len(data) / (self.baudrate / 10)
        time.sleep(transmission_delay)
        
        # 상대방의 읽기 파일에 데이터 추가 (append mode)
        try:
            with open(self._write_file, 'ab') as f:
                f.write(data)
                f.flush()  # 버퍼를 즉시 디스크에 쓰기
                os.fsync(f.fileno())  # 운영체제 레벨에서도 강제 flush
            
            # 전송 완료 메시지
            paired_port = self._port_pairs.get(self.port, 'Unknown')
            print(f"[MockSerial] {self.port} -> {paired_port}: {len(data)} bytes 전송")
            
        except Exception as e:
            print(f"[MockSerial] 쓰기 오류: {e}")
        
        return len(data)
    
    def read(self, size=1):
        """
        지정된 크기만큼 데이터 읽기
        
        Args:
            size (int): 읽을 바이트 수
            
        Returns:
            bytes: 읽은 데이터 (버퍼에 데이터가 부족하면 읽을 수 있는 만큼만 반환)
        """
        if not self._is_open:
            raise Exception("포트가 닫혀있습니다")
        
        # 내부 버퍼에서 데이터 꺼내기
        result = bytearray()
        for _ in range(min(size, len(self._read_buffer))):
            result.append(self._read_buffer.popleft())
        
        return bytes(result)
    
    def readline(self):
        """
        개행 문자(\n)까지 데이터 읽기
        
        타임아웃 시간 내에 개행 문자를 만나면 그때까지의 데이터를 반환하고,
        타임아웃이 되면 그때까지 읽은 데이터를 반환
        
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
                
                # 개행 문자(\n = 0x0A)를 만나면 종료
                if byte == ord('\n'):
                    break
            else:
                # 버퍼가 비어있으면 잠시 대기 (CPU 과사용 방지)
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
        """
        출력 버퍼 비우기 (전송 완료 대기)
        
        Mock Serial에서는 write()가 즉시 완료되므로 별도 처리 불필요
        """
        pass
    
    def close(self):
        """
        포트 닫기 및 리소스 정리
        """
        self._is_open = False
        self._monitoring = False
        
        # 모니터링 스레드 종료 대기
        if self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=1)
        
        print(f"[MockSerial] 포트 {self.port} 닫기 완료")
    
    def _monitor_file(self):
        """
        백그라운드 스레드: 파일을 주기적으로 감시하여 새 데이터를 버퍼로 읽어옴
        
        이 함수는 백그라운드 스레드에서 자동으로 실행되며,
        상대방이 파일에 데이터를 쓰면 자동으로 감지하여 읽기 버퍼에 추가
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
                            
                            # 버퍼에 추가 (바이트 단위로)
                            for byte in new_data:
                                self._read_buffer.append(byte)
                            
                            # 읽은 위치 업데이트
                            self._last_read_pos = file_size
                            
                            # 디버그 메시지
                            if len(new_data) > 0:
                                print(f"[MockSerial] {self.port} 버퍼에 {len(new_data)} bytes 추가됨")
                
            except Exception as e:
                # 종료 중이 아닐 때만 에러 출력
                if self._monitoring:
                    print(f"[MockSerial] 모니터링 오류: {e}")
            
            # CPU 사용률 낮추기 (50ms마다 체크)
            time.sleep(0.05)
    
    def __repr__(self):
        """객체의 문자열 표현"""
        return (f"MockSerial(port='{self.port}', baudrate={self.baudrate}, "
                f"is_open={self._is_open})")
    
    def __del__(self):
        """
        객체 소멸자 - 프로그램 종료 시 자동으로 리소스 정리
        """
        if hasattr(self, '_monitoring'):
            self._monitoring = False
        if hasattr(self, '_is_open') and self._is_open:
            try:
                self.close()
            except:
                pass


# =================================================================
# 유틸리티 함수
# =================================================================

def cleanup_mock_files():
    """
    Mock Serial 통신에 사용된 임시 파일들을 모두 삭제
    
    프로그램 시작 전이나 종료 후 호출하면 이전 테스트의 잔여 파일을 정리할 수 있음
    """
    temp_dir = Path(tempfile.gettempdir())
    comm_dir = temp_dir / 'mock_serial_comm'
    
    print(f"[MockSerial] 정리 대상 폴더: {comm_dir}")
    
    if comm_dir.exists():
        # .dat 파일들 삭제
        for file in comm_dir.glob('*.dat'):
            try:
                file.unlink()
                print(f"[MockSerial] 파일 삭제: {file.name}")
            except Exception as e:
                print(f"[MockSerial] 파일 삭제 실패: {file.name}, {e}")
        
        # 빈 디렉토리 삭제 시도
        try:
            comm_dir.rmdir()
            print(f"[MockSerial] 디렉토리 삭제 완료")
        except Exception as e:
            pass  # 디렉토리가 비어있지 않으면 무시
