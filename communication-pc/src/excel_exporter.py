"""
=================================================================
파일명: excel_exporter.py
설명: Excel 신뢰도 리포트 자동 생성
작성일: 2025-10-24
=================================================================
CSV 로그 파일을 분석하여 Excel 신뢰도 리포트를 자동 생성합니다.

생성되는 시트:
1. Summary: 전체 요약
2. CallLog: 통신 로그
3. SensorData: 센서 데이터
4. Charts: 차트 및 그래프

필요 라이브러리:
- openpyxl (pip install openpyxl)
=================================================================
"""

import csv
from datetime import datetime
from pathlib import Path

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.chart import BarChart, LineChart, PieChart, Reference
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False
    print("[경고] openpyxl이 설치되지 않았습니다.")
    print("설치 방법: pip install openpyxl")


class ExcelExporter:
    """
    Excel 신뢰도 리포트 생성 클래스
    """
    
    def __init__(self, output_dir='output'):
        """
        엑셀 익스포터 초기화
        
        Args:
            output_dir (str): 출력 디렉토리
        """
        if not OPENPYXL_AVAILABLE:
            raise ImportError("openpyxl 라이브러리가 필요합니다")
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 스타일 정의
        self.header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        self.header_font = Font(bold=True, color="FFFFFF")
        self.success_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        self.failure_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
        self.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    
    def create_report(self, call_log_file, sensor_log_file, reliability_report):
        """
        Excel 리포트 생성
        
        Args:
            call_log_file (Path): 통신 로그 CSV 파일
            sensor_log_file (Path): 센서 데이터 CSV 파일
            reliability_report (dict): 신뢰도 리포트 딕셔너리
        
        Returns:
            Path: 생성된 Excel 파일 경로
        """
        # 워크북 생성
        wb = Workbook()
        
        # 기본 시트 제거
        if 'Sheet' in wb.sheetnames:
            wb.remove(wb['Sheet'])
        
        # 1. Summary 시트
        print("[Excel] Summary 시트 생성 중...")
        self._create_summary_sheet(wb, reliability_report)
        
        # 2. CallLog 시트
        print("[Excel] CallLog 시트 생성 중...")
        self._create_call_log_sheet(wb, call_log_file)
        
        # 3. SensorData 시트
        print("[Excel] SensorData 시트 생성 중...")
        self._create_sensor_data_sheet(wb, sensor_log_file)
        
        # 4. Charts 시트
        print("[Excel] Charts 시트 생성 중...")
        self._create_charts_sheet(wb, reliability_report)
        
        # 파일 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"reliability_report_{timestamp}.xlsx"
        
        wb.save(output_file)
        print(f"[Excel] 리포트 생성 완료: {output_file}")
        
        return output_file
    
    def _create_summary_sheet(self, wb, report):
        """Summary 시트 생성"""
        ws = wb.create_sheet("Summary", 0)
        
        # 제목
        ws['A1'] = "DAQ 통신 신뢰도 측정 리포트"
        ws['A1'].font = Font(size=16, bold=True)
        ws.merge_cells('A1:D1')
        
        ws['A2'] = f"생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ws.merge_cells('A2:D2')
        
        # 전체 통계
        row = 4
        ws[f'A{row}'] = "전체 통계"
        ws[f'A{row}'].font = Font(size=14, bold=True)
        
        overall = report['overall']
        
        stats_data = [
            ['항목', '값', '비고', ''],
            ['총 테스트', overall['total_tests'], '회', ''],
            ['성공', overall['success'], '회', ''],
            ['실패', overall['failure'], '회', ''],
            ['타임아웃', overall['timeout'], '회', ''],
            ['신뢰도', f"{overall['reliability']:.2f}", '%', ''],
            ['목표 신뢰도', f"{overall['target']:.2f}", '%', ''],
            ['달성 여부', '달성' if overall['meets_target'] else '미달성', '', ''],
            ['안정성 등급', overall['grade'], '', '']
        ]
        
        row += 1
        for r_idx, row_data in enumerate(stats_data, start=row):
            for c_idx, value in enumerate(row_data, start=1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)
                cell.border = self.border
                
                if r_idx == row:  # 헤더
                    cell.fill = self.header_fill
                    cell.font = self.header_font
                elif c_idx == 2 and r_idx > row:  # 값 열
                    cell.alignment = Alignment(horizontal='right')
        
        # 응답 시간 통계
        row = row + len(stats_data) + 2
        ws[f'A{row}'] = "응답 시간 통계"
        ws[f'A{row}'].font = Font(size=14, bold=True)
        
        resp = report['response_time']
        resp_data = [
            ['항목', '값', '단위', ''],
            ['평균', f"{resp['avg']:.2f}", 'ms', ''],
            ['최소', f"{resp['min']:.2f}", 'ms', ''],
            ['최대', f"{resp['max']:.2f}", 'ms', ''],
            ['표준편차', f"{resp['std']:.2f}", 'ms', '']
        ]
        
        row += 1
        for r_idx, row_data in enumerate(resp_data, start=row):
            for c_idx, value in enumerate(row_data, start=1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)
                cell.border = self.border
                
                if r_idx == row:
                    cell.fill = self.header_fill
                    cell.font = self.header_font
                elif c_idx == 2 and r_idx > row:
                    cell.alignment = Alignment(horizontal='right')
        
        # 센서별 통계
        row = row + len(resp_data) + 2
        ws[f'A{row}'] = "센서별 통계"
        ws[f'A{row}'].font = Font(size=14, bold=True)
        
        sensor_headers = ['센서명', '총', '성공', '실패', '신뢰도(%)', '평균응답(ms)']
        
        row += 1
        for c_idx, header in enumerate(sensor_headers, start=1):
            cell = ws.cell(row=row, column=c_idx, value=header)
            cell.fill = self.header_fill
            cell.font = self.header_font
            cell.border = self.border
        
        for sensor_name, sensor_data in report['sensors'].items():
            row += 1
            sensor_row_data = [
                sensor_name,
                sensor_data['total'],
                sensor_data['success'],
                sensor_data['failure'],
                f"{sensor_data['reliability']:.2f}",
                f"{sensor_data['avg_response_time']:.2f}"
            ]
            
            for c_idx, value in enumerate(sensor_row_data, start=1):
                cell = ws.cell(row=row, column=c_idx, value=value)
                cell.border = self.border
                
                if c_idx in [2, 3, 4, 5, 6]:  # 숫자 열
                    cell.alignment = Alignment(horizontal='right')
        
        # 열 너비 조정
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 15
    
    def _create_call_log_sheet(self, wb, csv_file):
        """CallLog 시트 생성"""
        ws = wb.create_sheet("CallLog")
        
        if not csv_file.exists():
            ws['A1'] = "로그 파일을 찾을 수 없습니다"
            return
        
        # CSV 읽기
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            for r_idx, row in enumerate(reader, start=1):
                for c_idx, value in enumerate(row, start=1):
                    cell = ws.cell(row=r_idx, column=c_idx, value=value)
                    cell.border = self.border
                    
                    if r_idx == 1:  # 헤더
                        cell.fill = self.header_fill
                        cell.font = self.header_font
                    elif r_idx > 1:  # 데이터
                        # 상태에 따라 색상 적용
                        if c_idx == 7:  # 상태 열
                            if value == '성공':
                                cell.fill = self.success_fill
                            elif value in ['실패', '타임아웃']:
                                cell.fill = self.failure_fill
        
        # 열 너비 자동 조정
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 30)
            ws.column_dimensions[column_letter].width = adjusted_width
    
    def _create_sensor_data_sheet(self, wb, csv_file):
        """SensorData 시트 생성"""
        ws = wb.create_sheet("SensorData")
        
        if not csv_file.exists():
            ws['A1'] = "로그 파일을 찾을 수 없습니다"
            return
        
        # CSV 읽기
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            for r_idx, row in enumerate(reader, start=1):
                for c_idx, value in enumerate(row, start=1):
                    cell = ws.cell(row=r_idx, column=c_idx, value=value)
                    cell.border = self.border
                    
                    if r_idx == 1:  # 헤더
                        cell.fill = self.header_fill
                        cell.font = self.header_font
        
        # 열 너비 조정
        ws.column_dimensions['A'].width = 20  # 시간
        ws.column_dimensions['B'].width = 12  # MSG_Type
        ws.column_dimensions['C'].width = 20  # 센서명
        ws.column_dimensions['D'].width = 15  # 측정항목
        ws.column_dimensions['E'].width = 15  # 값
        ws.column_dimensions['F'].width = 10  # 단위
        ws.column_dimensions['G'].width = 10  # 상태
    
    def _create_charts_sheet(self, wb, report):
        """Charts 시트 생성"""
        ws = wb.create_sheet("Charts")
        
        # 제목
        ws['A1'] = "신뢰도 분석 차트"
        ws['A1'].font = Font(size=14, bold=True)
        
        # 센서별 신뢰도 데이터 준비
        row = 3
        ws[f'A{row}'] = "센서명"
        ws[f'B{row}'] = "신뢰도(%)"
        
        for cell in [ws[f'A{row}'], ws[f'B{row}']]:
            cell.fill = self.header_fill
            cell.font = self.header_font
        
        row += 1
        start_row = row
        
        for sensor_name, sensor_data in report['sensors'].items():
            ws[f'A{row}'] = sensor_name
            ws[f'B{row}'] = sensor_data['reliability']
            row += 1
        
        end_row = row - 1
        
        # 막대 차트 생성
        chart = BarChart()
        chart.title = "센서별 신뢰도"
        chart.x_axis.title = "센서"
        chart.y_axis.title = "신뢰도 (%)"
        
        data = Reference(ws, min_col=2, min_row=start_row-1, max_row=end_row)
        categories = Reference(ws, min_col=1, min_row=start_row, max_row=end_row)
        
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(categories)
        
        ws.add_chart(chart, f"D{start_row}")
        
        # 파이 차트 (성공/실패 비율)
        row = end_row + 3
        ws[f'A{row}'] = "구분"
        ws[f'B{row}'] = "횟수"
        
        for cell in [ws[f'A{row}'], ws[f'B{row}']]:
            cell.fill = self.header_fill
            cell.font = self.header_font
        
        overall = report['overall']
        
        row += 1
        pie_start = row
        ws[f'A{row}'] = "성공"
        ws[f'B{row}'] = overall['success']
        
        row += 1
        ws[f'A{row}'] = "실패"
        ws[f'B{row}'] = overall['failure']
        pie_end = row
        
        # 파이 차트
        pie = PieChart()
        pie.title = "전체 성공/실패 비율"
        
        data = Reference(ws, min_col=2, min_row=pie_start-1, max_row=pie_end)
        categories = Reference(ws, min_col=1, min_row=pie_start, max_row=pie_end)
        
        pie.add_data(data, titles_from_data=True)
        pie.set_categories(categories)
        
        ws.add_chart(pie, f"D{pie_start}")


# =================================================================
# 테스트 코드 (수정)
# =================================================================
if __name__ == "__main__":
    import sys
    
    print("Excel 리포트 생성기 테스트\n")
    
    if not OPENPYXL_AVAILABLE:
        print("openpyxl을 먼저 설치하세요: pip install openpyxl")
        exit(1)
    
    # 샘플 신뢰도 리포트
    sample_report = {
        'overall': {
            'total_tests': 100,
            'success': 98,
            'failure': 2,
            'timeout': 0,
            'reliability': 98.0,
            'meets_target': False,
            'target': 99.0,
            'grade': 'B'
        },
        'response_time': {
            'avg': 151.63,
            'min': 100.42,
            'max': 198.93,
            'std': 26.33
        },
        'failure_analysis': {
            'consecutive_max': 1,
            'mtbf': 50
        },
        'sensors': {
            '단상 전력량계': {
                'total': 34,
                'success': 32,
                'failure': 2,
                'timeout': 0,
                'reliability': 94.12,
                'avg_response_time': 155.23
            },
            '온습도 센서': {
                'total': 33,
                'success': 33,
                'failure': 0,
                'timeout': 0,
                'reliability': 100.0,
                'avg_response_time': 148.45
            },
            'CO2 센서': {
                'total': 33,
                'success': 33,
                'failure': 0,
                'timeout': 0,
                'reliability': 100.0,
                'avg_response_time': 151.20
            }
        }
    }
    
    # =================================================================
    # 경로 수정: 절대 경로 사용
    # =================================================================
    # 현재 파일 위치 기준으로 프로젝트 루트 찾기
    current_file = Path(__file__).resolve()
    src_dir = current_file.parent  # communication-pc/src
    comm_pc_dir = src_dir.parent   # communication-pc
    
    log_dir = comm_pc_dir / 'logs'
    output_dir = comm_pc_dir / 'output'
    
    print(f"로그 디렉토리: {log_dir}")
    print(f"출력 디렉토리: {output_dir}")
    
    call_log = log_dir / 'call_log_20251024.csv'
    sensor_log = log_dir / 'sensor_data_20251024.csv'
    
    # 파일 존재 확인
    if not call_log.exists():
        print(f"✗ call_log 파일 없음: {call_log}")
        print("  샘플 데이터로 진행합니다.")
    
    if not sensor_log.exists():
        print(f"✗ sensor_log 파일 없음: {sensor_log}")
        print("  샘플 데이터로 진행합니다.")
    
    # Excel 생성
    exporter = ExcelExporter(output_dir=str(output_dir))
    
    try:
        output_file = exporter.create_report(call_log, sensor_log, sample_report)
        print(f"\n✓ 리포트 생성 완료!")
        print(f"파일 위치: {output_file.absolute()}")
        
        # 파일 열기 (Windows)
        import os
        os.startfile(output_file)
        
    except Exception as e:
        print(f"✗ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
