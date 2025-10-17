"""
=================================================================
파일명: communication-pc/src/data_logger.py
설명: 통신 PC 데이터 로깅 모듈
작성자: 개발팀
작성일: 2025-10-17
=================================================================
모든 호출과 응답을 CSV 파일에 기록합니다.
나중에 엑셀로 분석하고 신뢰도를 계산하는데 사용됩니다.
=================================================================
"""

import csv
import os
from datetime import datetime
from pathlib import Path

class DataLogger:
    """
    통신 데이터를 CSV 파일에 기록하는 클래스
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
        self.call_log_file = self.log_dir / f"call_log_{today}.csv"
        self.error_log_file = self.log_dir / f"error_log_{today}.txt"
        
        # CSV 파일 초기화 (헤더 작성)
        self._initialize_csv()
        
        print(f"[DataLogger] 로그 파일 생성:")
        print(f"  - 호출 로그: {self.call_log_file}")
        print(f"  - 에러 로그: {self.error_log_file}")
    
    def _initialize_csv(self):
        """
        CSV 파일 초기화 (헤더 작성)
        파일이 없으면 생성하고 헤더를 작성합니다.
        """
        # 파일이 없거나 비어있으면 헤더 작성
        if not self.call_log_file.exists() or self.call_log_file.stat().st_size == 0:
            with open(self.call_log_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                # 헤더 작성
                writer.writerow([
                    'Request_ID',           # 요청 ID
                    'Send_Time',            # 송신 시간
                    'Receive_Time',         # 수신 시간
                    'Response_Time_ms',     # 응답 시간 (밀리초)
                    'Success',              # 성공 여부 (True/False)
                    'Message_Sent',         # 송신한 메시지
                    'Message_Received',     # 수신한 메시지
                    'Error_Message'         # 에러 메시지 (있으면)
                ])
    
    def log_request(self, request_id, send_time, message_sent):
        """
        요청 송신을 로그에 기록
        
        Args:
            request_id: 요청 고유 ID
            send_time: 송신 시간 (datetime 객체)
            message_sent: 송신한 메시지
        """
        # 임시로 메모리에 저장 (응답 받을 때까지 대기)
        if not hasattr(self, '_pending_requests'):
            self._pending_requests = {}
        
        self._pending_requests[request_id] = {
            'send_time': send_time,
            'message_sent': message_sent
        }
    
    def log_response(self, request_id, receive_time, message_received, success=True, error_message=''):
        """
        응답 수신을 로그에 기록
        
        Args:
            request_id: 요청 고유 ID
            receive_time: 수신 시간 (datetime 객체)
            message_received: 수신한 메시지
            success: 성공 여부
            error_message: 에러 메시지 (실패 시)
        """
        if not hasattr(self, '_pending_requests'):
            self._pending_requests = {}
        
        # 대기 중인 요청 정보 가져오기
        if request_id in self._pending_requests:
            request_info = self._pending_requests[request_id]
            send_time = request_info['send_time']
            message_sent = request_info['message_sent']
            
            # 응답 시간 계산 (밀리초)
            response_time_ms = (receive_time - send_time).total_seconds() * 1000
            
            # CSV에 기록
            with open(self.call_log_file, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    request_id,
                    send_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    receive_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    f"{response_time_ms:.2f}",
                    success,
                    message_sent,
                    message_received,
                    error_message
                ])
            
            # 대기 목록에서 제거
            del self._pending_requests[request_id]
        else:
            # 요청 없이 응답만 온 경우 (비정상)
            self.log_error(f"응답만 수신됨: Request ID {request_id}")
    
    def log_timeout(self, request_id, timeout_time):
        """
        타임아웃 발생을 로그에 기록
        
        Args:
            request_id: 요청 고유 ID
            timeout_time: 타임아웃 발생 시간
        """
        if not hasattr(self, '_pending_requests'):
            self._pending_requests = {}
        
        if request_id in self._pending_requests:
            request_info = self._pending_requests[request_id]
            send_time = request_info['send_time']
            message_sent = request_info['message_sent']
            
            # 응답 시간 계산
            response_time_ms = (timeout_time - send_time).total_seconds() * 1000
            
            # CSV에 기록
            with open(self.call_log_file, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    request_id,
                    send_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    timeout_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    f"{response_time_ms:.2f}",
                    False,  # 실패
                    message_sent,
                    '',  # 수신 메시지 없음
                    'Timeout'
                ])
            
            # 대기 목록에서 제거
            del self._pending_requests[request_id]
    
    def log_error(self, error_message):
        """
        에러 메시지를 텍스트 파일에 기록
        
        Args:
            error_message: 에러 메시지
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        with open(self.error_log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {error_message}\n")
    
    def get_statistics(self):
        """
        현재까지 기록된 로그의 통계를 반환
        
        Returns:
            dict: 통계 정보 (총 요청 수, 성공 수, 실패 수, 평균 응답 시간 등)
        """
        if not self.call_log_file.exists():
            return {
                'total': 0,
                'success': 0,
                'failure': 0,
                'success_rate': 0.0,
                'avg_response_time': 0.0
            }
        
        total = 0
        success = 0
        failure = 0
        response_times = []
        
        with open(self.call_log_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += 1
                if row['Success'] == 'True':
                    success += 1
                    # 응답 시간 수집
                    try:
                        response_times.append(float(row['Response_Time_ms']))
                    except:
                        pass
                else:
                    failure += 1
        
        # 통계 계산
        success_rate = (success / total * 100) if total > 0 else 0.0
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0.0
        
        return {
            'total': total,
            'success': success,
            'failure': failure,
            'success_rate': success_rate,
            'avg_response_time': avg_response_time,
            'min_response_time': min(response_times) if response_times else 0.0,
            'max_response_time': max(response_times) if response_times else 0.0
        }
    
    def close(self):
        """로거 종료 (리소스 정리)"""
        # 대기 중인 요청들을 타임아웃으로 처리
        if hasattr(self, '_pending_requests'):
            current_time = datetime.now()
            for request_id in list(self._pending_requests.keys()):
                self.log_timeout(request_id, current_time)
        
        print(f"[DataLogger] 로그 기록 완료")


# =================================================================
# 테스트 코드
# =================================================================
if __name__ == "__main__":
    print("DataLogger 모듈 테스트\n")
    
    # 로거 생성
    logger = DataLogger(log_dir='test_logs')
    
    # 테스트 데이터 기록
    from datetime import datetime, timedelta
    
    # 성공 케이스
    req_id = 1
    send_time = datetime.now()
    logger.log_request(req_id, send_time, "TEST_1")
    
    recv_time = send_time + timedelta(milliseconds=150)
    logger.log_response(req_id, recv_time, "RESPONSE_TEST_1", success=True)
    
    # 타임아웃 케이스
    req_id = 2
    send_time = datetime.now()
    logger.log_request(req_id, send_time, "TEST_2")
    
    timeout_time = send_time + timedelta(seconds=5)
    logger.log_timeout(req_id, timeout_time)
    
    # 통계 출력
    stats = logger.get_statistics()
    print("\n통계:")
    print(f"  총 요청: {stats['total']}")
    print(f"  성공: {stats['success']}")
    print(f"  실패: {stats['failure']}")
    print(f"  성공률: {stats['success_rate']:.2f}%")
    print(f"  평균 응답 시간: {stats['avg_response_time']:.2f}ms")
    
    logger.close()
    
    print(f"\n로그 파일 확인: test_logs/")
