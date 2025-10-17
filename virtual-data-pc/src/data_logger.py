"""
=================================================================
파일명: virtual-sensor-pc/src/data_logger.py
설명: 가상 센서 PC 데이터 로깅 모듈
작성자: 개발팀
작성일: 2025-10-17
=================================================================
수신한 요청과 전송한 응답을 CSV 파일에 기록합니다.
센서 데이터도 함께 기록하여 추적 가능하게 합니다.
=================================================================
"""

import csv
import os
from datetime import datetime
from pathlib import Path

class DataLogger:
    """
    가상 센서 데이터를 CSV 파일에 기록하는 클래스
    """
    
    def __init__(self, log_dir='logs'):
        """
        데이터 로거 초기화
        
        Args:
            log_dir: 로그 파일을 저장할 디렉토리
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # 파일명에 날짜 포함
        today = datetime.now().strftime("%Y%m%d")
        
        # CSV 파일 경로
        self.request_log_file = self.log_dir / f"request_log_{today}.csv"
        self.sensor_data_log_file = self.log_dir / f"sensor_data_log_{today}.csv"
        
        # CSV 파일 초기화
        self._initialize_csv()
        
        print(f"[DataLogger] 로그 파일 생성:")
        print(f"  - 요청 로그: {self.request_log_file}")
        print(f"  - 센서 데이터 로그: {self.sensor_data_log_file}")
    
    def _initialize_csv(self):
        """CSV 파일 초기화 (헤더 작성)"""
        # 요청 로그 헤더
        if not self.request_log_file.exists() or self.request_log_file.stat().st_size == 0:
            with open(self.request_log_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Request_ID',           # 요청 ID
                    'Receive_Time',         # 수신 시간
                    'Send_Time',            # 응답 송신 시간
                    'Processing_Time_ms',   # 처리 시간 (밀리초)
                    'Message_Received',     # 수신한 메시지
                    'Message_Sent',         # 송신한 메시지
                ])
        
        # 센서 데이터 로그 헤더
        if not self.sensor_data_log_file.exists() or self.sensor_data_log_file.stat().st_size == 0:
            with open(self.sensor_data_log_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Request_ID',       # 요청 ID
                    'Timestamp',        # 생성 시간
                    'Temperature',      # 온도
                    'Humidity',         # 습도
                    'Pressure',         # 압력
                    'Voltage'           # 전압
                ])
    
    def log_transaction(self, request_id, receive_time, send_time, 
                       message_received, message_sent, sensor_data):
        """
        트랜잭션을 로그에 기록
        
        Args:
            request_id: 요청 ID
            receive_time: 수신 시간 (datetime)
            send_time: 송신 시간 (datetime)
            message_received: 수신한 메시지
            message_sent: 송신한 메시지
            sensor_data: 센서 데이터 딕셔너리
        """
        # 처리 시간 계산
        processing_time_ms = (send_time - receive_time).total_seconds() * 1000
        
        # 요청 로그 기록
        with open(self.request_log_file, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                request_id,
                receive_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                send_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                f"{processing_time_ms:.2f}",
                message_received,
                message_sent
            ])
        
        # 센서 데이터 로그 기록
        with open(self.sensor_data_log_file, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                request_id,
                send_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                sensor_data.get('temperature', ''),
                sensor_data.get('humidity', ''),
                sensor_data.get('pressure', ''),
                sensor_data.get('voltage', '')
            ])
    
    def get_statistics(self):
        """로그 통계 반환"""
        if not self.request_log_file.exists():
            return {'total': 0, 'avg_processing_time': 0.0}
        
        total = 0
        processing_times = []
        
        with open(self.request_log_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += 1
                try:
                    processing_times.append(float(row['Processing_Time_ms']))
                except:
                    pass
        
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0.0
        
        return {
            'total': total,
            'avg_processing_time': avg_processing_time,
            'min_processing_time': min(processing_times) if processing_times else 0.0,
            'max_processing_time': max(processing_times) if processing_times else 0.0
        }
    
    def close(self):
        """로거 종료"""
        print(f"[DataLogger] 로그 기록 완료")
