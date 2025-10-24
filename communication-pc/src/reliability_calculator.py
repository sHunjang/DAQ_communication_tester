"""
=================================================================
파일명: reliability_calculator.py
설명: 통신 신뢰도 계산 모듈
작성일: 2025-10-24
=================================================================
DAQ 통신 신뢰도를 계산하고 분석합니다.

신뢰도 지표:
1. 전체 성공률 (%)
2. 센서별 성공률 (%)
3. 평균/최소/최대 응답 시간
4. MTBF (Mean Time Between Failures)
5. 안정성 등급 평가

목표 신뢰도: 99% 이상
=================================================================
"""

from collections import defaultdict
from datetime import timedelta


class ReliabilityCalculator:
    """
    통신 신뢰도 계산 클래스
    """
    
    def __init__(self, target_reliability=99.0):
        """
        신뢰도 계산기 초기화
        
        Args:
            target_reliability (float): 목표 신뢰도 (%)
        """
        self.target_reliability = target_reliability
        
        # 전체 통계
        self.total_tests = 0
        self.total_success = 0
        self.total_failures = 0
        self.total_timeouts = 0
        
        # 센서별 통계
        self.sensor_stats = defaultdict(lambda: {
            'total': 0,
            'success': 0,
            'failure': 0,
            'timeout': 0
        })
        
        # 응답 시간 통계
        self.response_times = []
        self.sensor_response_times = defaultdict(list)
        
        # 연속 실패 추적
        self.consecutive_failures = 0
        self.max_consecutive_failures = 0
        
        # 실패 간격 (MTBF 계산용)
        self.failure_intervals = []
        self.last_failure_index = 0
    
    def add_test_result(self, sensor_name, success, response_time_ms=None):
        """
        테스트 결과 추가
        
        Args:
            sensor_name (str): 센서 이름
            success (bool): 성공 여부
            response_time_ms (float): 응답 시간 (ms), 실패 시 None
        """
        self.total_tests += 1
        
        # 센서별 통계 업데이트
        self.sensor_stats[sensor_name]['total'] += 1
        
        if success:
            self.total_success += 1
            self.sensor_stats[sensor_name]['success'] += 1
            self.consecutive_failures = 0
            
            if response_time_ms is not None:
                self.response_times.append(response_time_ms)
                self.sensor_response_times[sensor_name].append(response_time_ms)
        else:
            self.total_failures += 1
            self.sensor_stats[sensor_name]['failure'] += 1
            self.consecutive_failures += 1
            
            # 최대 연속 실패 갱신
            if self.consecutive_failures > self.max_consecutive_failures:
                self.max_consecutive_failures = self.consecutive_failures
            
            # MTBF 계산을 위한 실패 간격 기록
            interval = self.total_tests - self.last_failure_index
            if self.last_failure_index > 0:
                self.failure_intervals.append(interval)
            self.last_failure_index = self.total_tests
    
    def add_timeout(self, sensor_name):
        """
        타임아웃 기록
        
        Args:
            sensor_name (str): 센서 이름
        """
        self.add_test_result(sensor_name, success=False)
        self.total_timeouts += 1
        self.sensor_stats[sensor_name]['timeout'] += 1
    
    def get_overall_reliability(self):
        """
        전체 신뢰도 계산
        
        Returns:
            float: 전체 성공률 (%)
        """
        if self.total_tests == 0:
            return 0.0
        return (self.total_success / self.total_tests) * 100
    
    def get_sensor_reliability(self, sensor_name):
        """
        센서별 신뢰도 계산
        
        Args:
            sensor_name (str): 센서 이름
        
        Returns:
            float: 센서 성공률 (%)
        """
        stats = self.sensor_stats[sensor_name]
        if stats['total'] == 0:
            return 0.0
        return (stats['success'] / stats['total']) * 100
    
    def get_response_time_stats(self):
        """
        전체 응답 시간 통계
        
        Returns:
            dict: 평균, 최소, 최대, 표준편차
        """
        if not self.response_times:
            return {
                'avg': 0,
                'min': 0,
                'max': 0,
                'std': 0,
                'count': 0
            }
        
        import statistics
        
        return {
            'avg': statistics.mean(self.response_times),
            'min': min(self.response_times),
            'max': max(self.response_times),
            'std': statistics.stdev(self.response_times) if len(self.response_times) > 1 else 0,
            'count': len(self.response_times)
        }
    
    def get_sensor_response_time_stats(self, sensor_name):
        """
        센서별 응답 시간 통계
        
        Args:
            sensor_name (str): 센서 이름
        
        Returns:
            dict: 평균, 최소, 최대
        """
        times = self.sensor_response_times[sensor_name]
        
        if not times:
            return {'avg': 0, 'min': 0, 'max': 0, 'count': 0}
        
        import statistics
        
        return {
            'avg': statistics.mean(times),
            'min': min(times),
            'max': max(times),
            'count': len(times)
        }
    
    def get_mtbf(self):
        """
        MTBF (Mean Time Between Failures) 계산
        
        Returns:
            float: 평균 실패 간격 (테스트 횟수)
        """
        if not self.failure_intervals:
            return float('inf')
        
        import statistics
        return statistics.mean(self.failure_intervals)
    
    def get_stability_grade(self):
        """
        안정성 등급 평가
        
        Returns:
            str: 등급 (S, A, B, C, D, F)
        """
        reliability = self.get_overall_reliability()
        
        if reliability >= 99.9:
            return 'S'
        elif reliability >= 99.0:
            return 'A'
        elif reliability >= 95.0:
            return 'B'
        elif reliability >= 90.0:
            return 'C'
        elif reliability >= 80.0:
            return 'D'
        else:
            return 'F'
    
    def meets_target(self):
        """
        목표 신뢰도 달성 여부
        
        Returns:
            bool: 달성 여부
        """
        return self.get_overall_reliability() >= self.target_reliability
    
    def get_summary_report(self):
        """
        요약 리포트 생성
        
        Returns:
            dict: 전체 통계 정보
        """
        reliability = self.get_overall_reliability()
        response_stats = self.get_response_time_stats()
        mtbf = self.get_mtbf()
        grade = self.get_stability_grade()
        
        report = {
            'overall': {
                'total_tests': self.total_tests,
                'success': self.total_success,
                'failure': self.total_failures,
                'timeout': self.total_timeouts,
                'reliability': reliability,
                'meets_target': self.meets_target(),
                'target': self.target_reliability,
                'grade': grade
            },
            'response_time': {
                'avg': response_stats['avg'],
                'min': response_stats['min'],
                'max': response_stats['max'],
                'std': response_stats['std']
            },
            'failure_analysis': {
                'consecutive_max': self.max_consecutive_failures,
                'mtbf': mtbf if mtbf != float('inf') else 'N/A'
            },
            'sensors': {}
        }
        
        # 센서별 통계 추가
        for sensor_name, stats in self.sensor_stats.items():
            sensor_reliability = self.get_sensor_reliability(sensor_name)
            sensor_response = self.get_sensor_response_time_stats(sensor_name)
            
            report['sensors'][sensor_name] = {
                'total': stats['total'],
                'success': stats['success'],
                'failure': stats['failure'],
                'timeout': stats['timeout'],
                'reliability': sensor_reliability,
                'avg_response_time': sensor_response['avg']
            }
        
        return report
    
    def print_summary(self):
        """요약 리포트 출력"""
        report = self.get_summary_report()
        
        print("="*70)
        print("신뢰도 측정 결과")
        print("="*70)
        
        # 전체 통계
        overall = report['overall']
        print(f"\n[전체 통계]")
        print(f"  총 테스트: {overall['total_tests']}회")
        print(f"  성공: {overall['success']}회")
        print(f"  실패: {overall['failure']}회")
        print(f"  타임아웃: {overall['timeout']}회")
        print(f"  신뢰도: {overall['reliability']:.2f}%")
        print(f"  목표: {overall['target']:.2f}%")
        print(f"  달성 여부: {'✓ 달성' if overall['meets_target'] else '✗ 미달성'}")
        print(f"  안정성 등급: {overall['grade']}")
        
        # 응답 시간
        resp = report['response_time']
        if resp['avg'] > 0:
            print(f"\n[응답 시간]")
            print(f"  평균: {resp['avg']:.2f}ms")
            print(f"  최소: {resp['min']:.2f}ms")
            print(f"  최대: {resp['max']:.2f}ms")
            print(f"  표준편차: {resp['std']:.2f}ms")
        
        # 실패 분석
        fail = report['failure_analysis']
        print(f"\n[실패 분석]")
        print(f"  최대 연속 실패: {fail['consecutive_max']}회")
        print(f"  MTBF: {fail['mtbf']}")
        
        # 센서별 통계
        print(f"\n[센서별 통계]")
        for sensor_name, sensor_data in report['sensors'].items():
            print(f"  {sensor_name}:")
            print(f"    신뢰도: {sensor_data['reliability']:.2f}% "
                  f"({sensor_data['success']}/{sensor_data['total']})")
            if sensor_data['avg_response_time'] > 0:
                print(f"    평균 응답: {sensor_data['avg_response_time']:.2f}ms")


# =================================================================
# 테스트 코드
# =================================================================
if __name__ == "__main__":
    print("신뢰도 계산기 테스트\n")
    
    calc = ReliabilityCalculator(target_reliability=99.0)
    
    # 시뮬레이션: 100회 테스트
    import random
    
    sensors = ["단상 전력량계", "온습도 센서", "CO2 센서"]
    
    for i in range(100):
        sensor = random.choice(sensors)
        
        # 98% 성공률 시뮬레이션
        success = random.random() < 0.98
        
        if success:
            response_time = random.uniform(100, 200)
            calc.add_test_result(sensor, True, response_time)
        else:
            calc.add_test_result(sensor, False)
    
    # 리포트 출력
    calc.print_summary()
