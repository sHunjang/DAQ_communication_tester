"""
=================================================================
파일명: communication-pc/src/excel_exporter.py
설명: 엑셀 리포트 생성 모듈
작성자: 개발팀
작성일: 2025-10-17
=================================================================
통신 로그를 분석하여 엑셀 리포트를 생성합니다.
통신 PC와 가상 센서 PC의 로그를 비교하여 데이터 정합성을 검증합니다.
=================================================================
"""

import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference
from pathlib import Path
from datetime import datetime

class ExcelExporter:
    """
    엑셀 리포트를 생성하는 클래스
    """
    
    def __init__(self, comm_log_file, sensor_log_file=None, output_dir='output'):
        """
        엑셀 내보내기 초기화
        
        Args:
            comm_log_file: 통신 PC 로그 파일 경로
            sensor_log_file: 가상 센서 PC 로그 파일 경로 (선택)
            output_dir: 출력 디렉토리
        """
        self.comm_log_file = Path(comm_log_file)
        self.sensor_log_file = Path(sensor_log_file) if sensor_log_file else None
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 워크북 생성
        self.wb = openpyxl.Workbook()
        
        # 기본 시트 제거
        if 'Sheet' in self.wb.sheetnames:
            self.wb.remove(self.wb['Sheet'])
        
        print(f"[ExcelExporter] 초기화 완료")
    
    def _set_header_style(self, ws, row=1):
        """
        헤더 행에 스타일 적용
        
        Args:
            ws: 워크시트
            row: 헤더 행 번호
        """
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        for cell in ws[row]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')
    
    def create_call_log_sheet(self):
        """
        통신 PC 호출 로그 시트 생성
        """
        ws = self.wb.create_sheet("통신 로그")
        
        # CSV 데이터 읽기 및 쓰기
        with open(self.comm_log_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for row_idx, row in enumerate(reader, 1):
                for col_idx, value in enumerate(row, 1):
                    cell = ws.cell(row=row_idx, column=col_idx, value=value)
                    
                    # Success 열 색상 지정
                    if row_idx > 1 and col_idx == 5:  # Success 열
                        if value == 'True':
                            cell.fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
                        else:
                            cell.fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
        
        # 헤더 스타일 적용
        self._set_header_style(ws)
        
        # 열 너비 자동 조정
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        print(f"[ExcelExporter] '통신 로그' 시트 생성 완료")
    
    def create_statistics_sheet(self, calculator):
        """
        통계 요약 시트 생성
        
        Args:
            calculator: ReliabilityCalculator 객체
        """
        ws = self.wb.create_sheet("통계 요약")
        
        # 리포트 데이터 가져오기
        report = calculator.get_full_report()
        
        # 1. 제목
        ws['A1'] = '통신 신뢰도 분석 리포트'
        ws['A1'].font = Font(size=16, bold=True)
        ws.merge_cells('A1:D1')
        
        ws['A2'] = f'생성일시: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        ws.merge_cells('A2:D2')
        
        # 2. 성공률 요약
        row = 4
        ws[f'A{row}'] = '[통신 성공률]'
        ws[f'A{row}'].font = Font(bold=True, size=12)
        ws.merge_cells(f'A{row}:D{row}')
        
        row += 1
        sr = report['success_rate']
        data = [
            ['항목', '값'],
            ['총 요청 수', sr['total']],
            ['성공', f"{sr['success']} ({sr['success_rate']:.2f}%)"],
            ['실패', f"{sr['failure']} ({100-sr['success_rate']:.2f}%)"],
        ]
        
        for data_row in data:
            for col_idx, value in enumerate(data_row, 1):
                ws.cell(row=row, column=col_idx, value=value)
            row += 1
        
        # 헤더 스타일
        self._set_header_style(ws, row=5)
        
        # 3. 응답 시간 통계
        row += 1
        ws[f'A{row}'] = '[응답 시간 통계]'
        ws[f'A{row}'].font = Font(bold=True, size=12)
        ws.merge_cells(f'A{row}:D{row}')
        
        row += 1
        rt = report['response_time_stats']
        data = [
            ['항목', '값 (ms)'],
            ['평균', f"{rt['average']:.2f}"],
            ['최소', f"{rt['min']:.2f}"],
            ['최대', f"{rt['max']:.2f}"],
            ['중앙값', f"{rt['median']:.2f}"],
            ['표준편차', f"{rt['std_dev']:.2f}"],
        ]
        
        for data_row in data:
            for col_idx, value in enumerate(data_row, 1):
                ws.cell(row=row, column=col_idx, value=value)
            row += 1
        
        # 헤더 스타일
        header_row = row - len(data)
        self._set_header_style(ws, row=header_row)
        
        # 4. 에러 패턴
        row += 1
        ws[f'A{row}'] = '[에러 패턴]'
        ws[f'A{row}'].font = Font(bold=True, size=12)
        ws.merge_cells(f'A{row}:D{row}')
        
        row += 1
        errors = report['error_patterns']
        if errors:
            data = [['에러 유형', '발생 횟수']]
            for error_type, count in errors.items():
                data.append([error_type, count])
            
            for data_row in data:
                for col_idx, value in enumerate(data_row, 1):
                    ws.cell(row=row, column=col_idx, value=value)
                row += 1
            
            header_row = row - len(data)
            self._set_header_style(ws, row=header_row)
        else:
            ws[f'A{row}'] = '에러 없음'
            row += 1
        
        # 열 너비 조정
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 30
        
        print(f"[ExcelExporter] '통계 요약' 시트 생성 완료")
    
    def create_response_time_chart(self):
        """
        응답 시간 그래프 시트 생성
        """
        ws = self.wb.create_sheet("응답 시간 그래프")
        
        # 통신 로그에서 응답 시간 데이터 추출
        response_times = []
        with open(self.comm_log_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Success'] == 'True':
                    try:
                        response_times.append(float(row['Response_Time_ms']))
                    except:
                        pass
        
        # 데이터를 시트에 기록
        ws['A1'] = '요청 번호'
        ws['B1'] = '응답 시간 (ms)'
        self._set_header_style(ws)
        
        for idx, time in enumerate(response_times, 1):
            ws[f'A{idx+1}'] = idx
            ws[f'B{idx+1}'] = time
        
        # 차트 생성
        chart = LineChart()
        chart.title = "응답 시간 추이"
        chart.y_axis.title = "응답 시간 (ms)"
        chart.x_axis.title = "요청 번호"
        
        data = Reference(ws, min_col=2, min_row=1, max_row=len(response_times)+1)
        cats = Reference(ws, min_col=1, min_row=2, max_row=len(response_times)+1)
        
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)
        
        ws.add_chart(chart, "D2")
        
        print(f"[ExcelExporter] '응답 시간 그래프' 시트 생성 완료")
    
    def save(self, filename=None):
        """
        엑셀 파일 저장
        
        Args:
            filename: 파일명 (없으면 자동 생성)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reliability_report_{timestamp}.xlsx"
        
        output_path = self.output_dir / filename
        self.wb.save(output_path)
        
        print(f"[ExcelExporter] 엑셀 파일 저장 완료: {output_path}")
        return output_path


# =================================================================
# 테스트 코드
# =================================================================
if __name__ == "__main__":
    from reliability_calculator import ReliabilityCalculator
    from datetime import datetime
    
    print("ExcelExporter 모듈 테스트\n")
    
    # 로그 파일 경로
    today = datetime.now().strftime("%Y%m%d")
    comm_log = f"../logs/call_log_{today}.csv"
    
    if not Path(comm_log).exists():
        print(f"로그 파일을 찾을 수 없습니다: {comm_log}")
        print("먼저 test_send_mock.py를 실행하여 로그를 생성하세요.")
        exit(1)
    
    # 신뢰도 계산
    calculator = ReliabilityCalculator(comm_log)
    
    # 엑셀 생성
    exporter = ExcelExporter(comm_log, output_dir='../output')
    exporter.create_call_log_sheet()
    exporter.create_statistics_sheet(calculator)
    exporter.create_response_time_chart()
    
    # 저장
    output_file = exporter.save()
    
    print(f"\n엑셀 파일을 열어서 확인하세요: {output_file}")
