"""
=================================================================
파일명: communication-pc/src/reliability_calculator.py
설명: 통신 신뢰도 계산 모듈
작성자: 개발팀
작성일: 2025-10-17
=================================================================
CSV 로그 파일을 분석하여 통신 신뢰도를 계산합니다.
성공률, 응답 시간 통계, 에러 패턴 등을 분석합니다.
=================================================================
"""

import csv
import statistics
from pathlib import Path
from datetime import datetime
from collections import Counter

class ReliabilityCalculator:
    """
    통신 신뢰도를 계산하는 클래스
    """
    
    def __init__(self, log_file):
        """
        신뢰도 계산기 초기화
        
        Args:
            log_file: 분석할 CSV 로그 파일 경로
        """
        self.log_file = Path(log_file)
        
        if not self.log_file.exists():
            raise FileNotFoundError(f"로그 파일을 찾을 수 없습니다: {log_file}")
        
        # 로그 데이터 로드
        self.data = self._load_log_data()
        
        print(f"[ReliabilityCalculator] 로그 파일 로드 완료: {self.log_file.name}")
        print(f"[ReliabilityCalculator] 총 레코드 수: {len(self.data)}")
    
    def _load_log_data(self):
        """
        CSV 로그 파일을 읽어서 데이터 리스트로 변환
        
        Returns:
            list: 로그 데이터 리스트 (각 항목은 딕셔너리)
        """
        data = []
        
        with open(self.log_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 성공 여부를 boolean으로 변환
                row['Success'] = row['Success'] == 'True'
                
                # 응답 시간을 float으로 변환
                try:
                    row['Response_Time_ms'] = float(row['Response_Time_ms'])
                except:
                    row['Response_Time_ms'] = 0.0
                
                data.append(row)
        
        return data
    
    def calculate_success_rate(self):
        """
        통신 성공률 계산
        
        Returns:
            dict: 성공률 정보
        """
        if not self.data:
            return {
                'total': 0,
                'success': 0,
                'failure': 0,
                'success_rate': 0.0
            }
        
        total = len(self.data)
        success = sum(1 for row in self.data if row['Success'])
        failure = total - success
        success_rate = (success / total * 100) if total > 0 else 0.0
        
        return {
            'total': total,
            'success': success,
            'failure': failure,
            'success_rate': success_rate
        }
    
    def calculate_response_time_stats(self):
        """
        응답 시간 통계 계산
        
        Returns:
            dict: 응답 시간 통계 (평균, 최소, 최대, 중앙값, 표준편차)
        """
        # 성공한 요청의 응답 시간만 수집
        response_times = [
            row['Response_Time_ms'] 
            for row in self.data 
            if row['Success'] and row['Response_Time_ms'] > 0
        ]
        
        if not response_times:
            return {
                'count': 0,
                'average': 0.0,
                'min': 0.0,
                'max': 0.0,
                'median': 0.0,
                'std_dev': 0.0
            }
        
        return {
            'count': len(response_times),
            'average': statistics.mean(response_times),
            'min': min(response_times),
            'max': max(response_times),
            'median': statistics.median(response_times),
            'std_dev': statistics.stdev(response_times) if len(response_times) > 1 else 0.0
        }
    
    def analyze_error_patterns(self):
        """
        에러 패턴 분석
        
        Returns:
            dict: 에러 유형별 발생 횟수
        """
        # 실패한 요청의 에러 메시지 수집
        error_messages = [
            row['Error_Message'] 
            for row in self.data 
            if not row['Success'] and row['Error_Message']
        ]
        
        # 에러 유형별 카운트
        error_counter = Counter(error_messages)
        
        return dict(error_counter)
    
    def calculate_time_distribution(self, bins=10):
        """
        응답 시간 분포 계산 (히스토그램용)
        
        Args:
            bins: 구간 개수
            
        Returns:
            dict: 응답 시간 분포 정보
        """
        response_times = [
            row['Response_Time_ms'] 
            for row in self.data 
            if row['Success'] and row['Response_Time_ms'] > 0
        ]
        
        if not response_times:
            return {'bins': [], 'counts': []}
        
        min_time = min(response_times)
        max_time = max(response_times)
        bin_width = (max_time - min_time) / bins if max_time > min_time else 1.0
        
        # 구간 생성
        bin_edges = [min_time + i * bin_width for i in range(bins + 1)]
        bin_counts = [0] * bins
        
        # 각 응답 시간을 해당 구간에 배치
        for time in response_times:
            for i in range(bins):
                if bin_edges[i] <= time < bin_edges[i + 1]:
                    bin_counts[i] += 1
                    break
                elif i == bins - 1 and time == bin_edges[i + 1]:
                    # 최대값은 마지막 구간에 포함
                    bin_counts[i] += 1
                    break
        
        return {
            'bin_edges': bin_edges,
            'bin_counts': bin_counts
        }
    
    def calculate_hourly_stats(self):
        """
        시간대별 통신 성공률 계산
        
        Returns:
            dict: 시간대별 통계
        """
        hourly_data = {}
        
        for row in self.data:
            try:
                # 시간 추출 (HH 형식)
                send_time_str = row['Send_Time']
                hour = send_time_str.split(' ')[1].split(':')[0]
                
                if hour not in hourly_data:
                    hourly_data[hour] = {'total': 0, 'success': 0}
                
                hourly_data[hour]['total'] += 1
                if row['Success']:
                    hourly_data[hour]['success'] += 1
                    
            except:
                continue
        
        # 성공률 계산
        for hour in hourly_data:
            total = hourly_data[hour]['total']
            success = hourly_data[hour]['success']
            hourly_data[hour]['success_rate'] = (success / total * 100) if total > 0 else 0.0
        
        return hourly_data
    
    def get_full_report(self):
        """
        전체 신뢰도 리포트 생성
        
        Returns:
            dict: 전체 분석 결과
        """
        report = {
            'success_rate': self.calculate_success_rate(),
            'response_time_stats': self.calculate_response_time_stats(),
            'error_patterns': self.analyze_error_patterns(),
            'time_distribution': self.calculate_time_distribution(),
            'hourly_stats': self.calculate_hourly_stats()
        }
        
        return report
    
    def print_report(self):
        """전체 리포트를 콘솔에 출력"""
        report = self.get_full_report()
        
        print("\n" + "="*60)
        print("통신 신뢰도 분석 리포트")
        print("="*60)
        
        # 1. 성공률
        print("\n[1] 통신 성공률")
        print("-"*60)
        sr = report['success_rate']
        print(f"  총 요청 수: {sr['total']}")
        print(f"  성공: {sr['success']} ({sr['success_rate']:.2f}%)")
        print(f"  실패: {sr['failure']} ({100-sr['success_rate']:.2f}%)")
        
        # 2. 응답 시간 통계
        print("\n[2] 응답 시간 통계")
        print("-"*60)
        rt = report['response_time_stats']
        print(f"  평균: {rt['average']:.2f}ms")
        print(f"  최소: {rt['min']:.2f}ms")
        print(f"  최대: {rt['max']:.2f}ms")
        print(f"  중앙값: {rt['median']:.2f}ms")
        print(f"  표준편차: {rt['std_dev']:.2f}ms")
        
        # 3. 에러 패턴
        print("\n[3] 에러 패턴")
        print("-"*60)
        errors = report['error_patterns']
        if errors:
            for error_type, count in errors.items():
                print(f"  {error_type}: {count}회")
        else:
            print("  에러 없음")
        
        print("\n" + "="*60)


# =================================================================
# 테스트 코드
# =================================================================
if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    print("ReliabilityCalculator 모듈 테스트\n")
    
    # 로그 파일 경로 확인
    today = datetime.now().strftime("%Y%m%d")
    log_file = f"../logs/call_log_{today}.csv"
    
    if not Path(log_file).exists():
        print(f"로그 파일을 찾을 수 없습니다: {log_file}")
        print("먼저 test_send_mock.py를 실행하여 로그를 생성하세요.")
        sys.exit(1)
    
    # 신뢰도 계산
    calculator = ReliabilityCalculator(log_file)
    
    # 리포트 출력
    calculator.print_report()
