"""
=================================================================
파일명: data_logger.py  
설명: 통신 PC용 데이터 로거
작성일: 2025-10-24
=================================================================
DAQ 통신 내역과 센서 데이터를 CSV 파일로 기록합니다.

로그 파일:
1. call_log_YYYYMMDD.csv: 통신 요청/응답 기록
2. error_log_YYYYMMDD.txt: 에러 발생 기록
3. sensor_data_YYYYMMDD.csv: 센서 데이터 기록

주요 기능:
- 날짜별 로그 파일 자동 생성
- CSV 형식으로 구조화된 데이터 저장
- 통계 정보 제공 (성공률, 평균 응답 시간 등)
=================================================================
"""

import os
import csv
from datetime import datetime
from pathlib import Path


class DataLogger:
    """
    통신 PC용 데이터 로거 클래스
    
    통신 내역과 센서 데이터를 날짜별 CSV 파일로 기록합니다.
    """
    
    def __init__(self, log_dir='logs'):
        """
        로거 초기화
        
        Args:
            log_dir (str): 로그 파일을 저장할 디렉토리
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)  # 디렉토리 생성
        
        # 현재 날짜 (YYYYMMDD 형식)
        today = datetime.now().strftime("%Y%m%d")
        
        # 로그 파일 경로 설정
        self.call_log_file = self.log_dir / f"call_log_{today}.csv"
        self.error_log_file = self.log_dir / f"error_log_{today}.txt"
        self.sensor_log_file = self.log_dir / f"sensor_data_{today}.csv"
        
        # 통계 정보 초기화
        self.stats = {
            'total': 0,
            'success': 0,
            'failure': 0,
            'timeout': 0,
            'response_times': []  # 응답 시간 목록 (ms)
        }
        
        # CSV 파일 초기화 (헤더 작성)
        self._init_call_log()
        self._init_sensor_log()
        
        print(f"[Logger] 로그 디렉토리: {self.log_dir.absolute()}")
        print(f"[Logger] 통신 로그: {self.call_log_file.name}")
        print(f"[Logger] 에러 로그: {self.error_log_file.name}")
        print(f"[Logger] 센서 데이터: {self.sensor_log_file.name}")
    
    def _init_call_log(self):
        """
        통신 로그 CSV 파일 초기화 (헤더 작성)
        """
        # 파일이 없거나 비어있으면 헤더 작성
        if not self.call_log_file.exists() or self.call_log_file.stat().st_size == 0:
            with open(self.call_log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'ID',           # 요청 번호
                    '송신시간',      # 요청 전송 시간
                    '수신시간',      # 응답 수신 시간
                    '응답시간(ms)',  # 응답 시간 (밀리초)
                    'MSG_Type',     # 메시지 타입 (0x01, 0x07 등)
                    '센서명',        # 센서 이름
                    '상태',          # 성공/실패/타임아웃
                    '비고'           # 에러 메시지 등
                ])
    
    def _init_sensor_log(self):
        """
        센서 데이터 로그 CSV 파일 초기화 (헤더 작성)
        """
        if not self.sensor_log_file.exists() or self.sensor_log_file.stat().st_size == 0:
            with open(self.sensor_log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    '시간',
                    'MSG_Type',
                    '센서명',
                    '측정항목',
                    '값',
                    '단위',
                    '상태'
                ])
    
    def log_request(self, request_id, send_time, msg_type_name):
        """
        요청 전송 기록
        
        Args:
            request_id (int): 요청 번호
            send_time (datetime): 전송 시간
            msg_type_name (str): 메시지 타입 이름
        """
        self.stats['total'] += 1
        
        # 임시로 저장 (응답 수신 시 업데이트)
        self._pending_request = {
            'id': request_id,
            'send_time': send_time,
            'msg_type_name': msg_type_name
        }
    
    def log_response(self, request_id, receive_time, msg_type_name, success=True, note=''):
        """
        응답 수신 기록
        
        Args:
            request_id (int): 요청 번호
            receive_time (datetime): 수신 시간
            msg_type_name (str): 메시지 타입 이름
            success (bool): 성공 여부
            note (str): 비고 (에러 메시지 등)
        """
        if hasattr(self, '_pending_request'):
            send_time = self._pending_request['send_time']
            
            # 응답 시간 계산 (밀리초)
            response_time_ms = (receive_time - send_time).total_seconds() * 1000
            self.stats['response_times'].append(response_time_ms)
            
            # 통계 업데이트
            if success:
                self.stats['success'] += 1
                status = '성공'
            else:
                self.stats['failure'] += 1
                status = '실패'
            
            # CSV에 기록
            with open(self.call_log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    request_id,
                    send_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    receive_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    f"{response_time_ms:.2f}",
                    self._pending_request.get('msg_type_name', msg_type_name),
                    msg_type_name,
                    status,
                    note
                ])
    
    def log_timeout(self, request_id, timeout_time):
        """
        타임아웃 기록
        
        Args:
            request_id (int): 요청 번호
            timeout_time (datetime): 타임아웃 발생 시간
        """
        self.stats['timeout'] += 1
        self.stats['failure'] += 1
        
        if hasattr(self, '_pending_request'):
            send_time = self._pending_request['send_time']
            msg_type_name = self._pending_request['msg_type_name']
            
            with open(self.call_log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    request_id,
                    send_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    timeout_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    '',
                    msg_type_name,
                    msg_type_name,
                    '타임아웃',
                    '응답 없음'
                ])
    
    def log_sensor_data(self, timestamp, msg_type, sensor_name, parsed_data):
        """
        센서 데이터 기록
        
        Args:
            timestamp (datetime): 측정 시간
            msg_type (int): 메시지 타입
            sensor_name (str): 센서 이름
            parsed_data (dict): 파싱된 센서 데이터
        """
        time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        with open(self.sensor_log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # 단상 전력량계
            if 'voltage' in parsed_data:
                writer.writerow([
                    time_str, f"0x{msg_type:02X}", sensor_name,
                    '전압', parsed_data['voltage']['value'], 
                    parsed_data['voltage']['unit'],
                    parsed_data['voltage']['status']
                ])
                writer.writerow([
                    time_str, f"0x{msg_type:02X}", sensor_name,
                    '전류', parsed_data['current']['value'],
                    parsed_data['current']['unit'],
                    parsed_data['current']['status']
                ])
                writer.writerow([
                    time_str, f"0x{msg_type:02X}", sensor_name,
                    '전력', parsed_data['power']['value'],
                    parsed_data['power']['unit'],
                    parsed_data['power']['status']
                ])
                writer.writerow([
                    time_str, f"0x{msg_type:02X}", sensor_name,
                    '전력량', parsed_data['energy']['value'],
                    parsed_data['energy']['unit'],
                    parsed_data['energy']['status']
                ])
            
            # 온습도 센서
            elif 'temperature' in parsed_data:
                writer.writerow([
                    time_str, f"0x{msg_type:02X}", sensor_name,
                    '온도', parsed_data['temperature']['value'],
                    parsed_data['temperature']['unit'], 'OK'
                ])
                writer.writerow([
                    time_str, f"0x{msg_type:02X}", sensor_name,
                    '습도', parsed_data['humidity']['value'],
                    parsed_data['humidity']['unit'], 'OK'
                ])
            
            # CO2 센서
            elif 'co2' in parsed_data:
                writer.writerow([
                    time_str, f"0x{msg_type:02X}", sensor_name,
                    'CO2', parsed_data['co2']['value'],
                    parsed_data['co2']['unit'], 'OK'
                ])
    
    def log_error(self, error_message):
        """
        에러 로그 기록
        
        Args:
            error_message (str): 에러 메시지
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        with open(self.error_log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {error_message}\n")
    
    def get_statistics(self):
        """
        통계 정보 반환
        
        Returns:
            dict: 통계 정보
                {
                    'total': 총 요청 수,
                    'success': 성공 수,
                    'failure': 실패 수,
                    'timeout': 타임아웃 수,
                    'success_rate': 성공률 (%),
                    'avg_response_time': 평균 응답 시간 (ms),
                    'min_response_time': 최소 응답 시간 (ms),
                    'max_response_time': 최대 응답 시간 (ms)
                }
        """
        stats = self.stats.copy()
        
        # 성공률 계산
        if stats['total'] > 0:
            stats['success_rate'] = (stats['success'] / stats['total']) * 100
        else:
            stats['success_rate'] = 0
        
        # 응답 시간 통계
        if stats['response_times']:
            stats['avg_response_time'] = sum(stats['response_times']) / len(stats['response_times'])
            stats['min_response_time'] = min(stats['response_times'])
            stats['max_response_time'] = max(stats['response_times'])
        else:
            stats['avg_response_time'] = 0
            stats['min_response_time'] = 0
            stats['max_response_time'] = 0
        
        return stats
    
    def close(self):
        """
        로거 종료 (통계 출력)
        """
        stats = self.get_statistics()
        
        print(f"\n[Logger] 통계 요약:")
        print(f"  총 요청: {stats['total']}")
        print(f"  성공: {stats['success']}")
        print(f"  실패: {stats['failure']}")
        print(f"  타임아웃: {stats['timeout']}")
        print(f"  성공률: {stats['success_rate']:.2f}%")
        
        if stats['avg_response_time'] > 0:
            print(f"  평균 응답 시간: {stats['avg_response_time']:.2f}ms")
            print(f"  최소 응답 시간: {stats['min_response_time']:.2f}ms")
            print(f"  최대 응답 시간: {stats['max_response_time']:.2f}ms")


# =================================================================
# 테스트 코드
# =================================================================
if __name__ == "__main__":
    import time
    
    print("="*70)
    print("데이터 로거 테스트")
    print("="*70)
    
    # 로거 초기화
    logger = DataLogger(log_dir='test_logs')
    
    # 테스트 1: 성공 케이스
    print("\n[테스트 1] 성공 케이스 기록")
    request_id = 1
    send_time = datetime.now()
    
    logger.log_request(request_id, send_time, "단상 전력량계")
    
    time.sleep(0.05)  # 50ms 대기
    receive_time = datetime.now()
    
    logger.log_response(request_id, receive_time, "단상 전력량계", success=True)
    
    # 센서 데이터 기록
    sensor_data = {
        'voltage': {'value': 221.2, 'unit': 'V', 'status': 'OK'},
        'current': {'value': 12.34, 'unit': 'A', 'status': 'OK'},
        'power': {'value': 12.345, 'unit': 'kW', 'status': 'OK'},
        'energy': {'value': 12345, 'unit': 'kWh', 'status': 'OK'}
    }
    logger.log_sensor_data(receive_time, 0x01, "단상 전력량계", sensor_data)
    
    print("✓ 성공 케이스 기록 완료")
    
    # 테스트 2: 타임아웃 케이스
    print("\n[테스트 2] 타임아웃 케이스 기록")
    request_id = 2
    send_time = datetime.now()
    
    logger.log_request(request_id, send_time, "온습도 센서")
    
    time.sleep(0.1)
    timeout_time = datetime.now()
    
    logger.log_timeout(request_id, timeout_time)
    print("✓ 타임아웃 케이스 기록 완료")
    
    # 테스트 3: 에러 기록
    print("\n[테스트 3] 에러 로그 기록")
    logger.log_error("CRC 불일치 오류 발생")
    logger.log_error("프레임 파싱 오류")
    print("✓ 에러 로그 기록 완료")
    
    # 통계 출력
    print("\n[테스트 4] 통계 정보")
    logger.close()
    
    print("\n" + "="*70)
    print("✓ 모든 테스트 완료")
    print(f"생성된 파일:")
    print(f"  - {logger.call_log_file}")
    print(f"  - {logger.error_log_file}")
    print(f"  - {logger.sensor_log_file}")
    print("="*70)
