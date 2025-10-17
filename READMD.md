# DAQ 통신 신뢰도 측정 시스템

RS485 통신을 통한 DAQ와 가상 센서 간 통신 신뢰도 측정 및 분석 시스템

## 📋 프로젝트 개요

이 프로젝트는 DAQ(Data Acquisition) 시스템과 가상 센서 간의 RS485 통신 신뢰도를 측정하고 분석하는 도구입니다. 실제 하드웨어 없이도 Mock Serial을 통해 개발 및 테스트가 가능하며, 설정 변경만으로 실제 RS485 하드웨어로 전환할 수 있습니다.

### 주요 기능

- ✅ RS485 유선 통신 시뮬레이션 및 실제 통신 지원
- ✅ Mock Serial 모드 (하드웨어 불필요)
- ✅ 실시간 호출/응답 데이터 로깅 (CSV)
- ✅ 통신 신뢰도 자동 계산 (목표: 99% 이상)
- ✅ 엑셀 리포트 자동 생성 (통계, 그래프 포함)
- ✅ 가상 센서 데이터 생성 (온도, 습도, 압력, 전압)
- ✅ 에러 패턴 분석 및 응답 시간 통계

## 🗂️ 프로젝트 구조

DaqTester/
├── communication-pc/ # 통신 PC 프로그램
│ ├── config/
init.py
│ │ └── config.py # 통신 설정 (Mock/Real 전환)
│ ├── src/
init.py
│ │ ├── data_logger.py # 데이터 로깅
│ │ ├── reliability_calculator.py # 신뢰도 계산
│ │ └── excel_exporter.py # 엑셀 리포트 생성
│ ├── logs/ # 로그 파일 저장
│ ├── output/ # 엑셀 리포트 저장
│ ├── mock_serial.py # Mock Serial 클래스
│ ├── test_send.py # 송신 테스트 (자동 전환)
│ ├── test_send_mock.py # 송신 테스트 (Mock 전용)
│ ├── environment.yml # Conda 환경 설정
│ └── README.md
│
├── virtual-sensor-pc/ # 가상 센서 PC 프로그램
│ ├── config/
init.py
│ │ └── config.py # 센서 설정
│ ├── src/
init.py
│ │ └── data_logger.py # 센서 데이터 로깅
│ ├── logs/ # 로그 파일 저장
│ ├── mock_serial.py # Mock Serial 클래스
│ ├── test_receive.py # 수신 테스트 (자동 전환)
│ ├── test_receive_mock.py # 수신 테스트 (Mock 전용)
│ ├── environment.yml # Conda 환경 설정
│ └── README.md
│
├── .gitignore
└── README.md


## 🚀 빠른 시작

### 1. 환경 설정

#### Miniconda 환경 생성

#### 통신 PC 환경
- cd communication-pc
- conda env create -f environment.yml
- conda activate daq-comm-pc

#### 가상 센서 PC 환경 (새 터미널)
- cd virtual-sensor-pc
- conda env create -f environment.yml
- conda activate daq-sensor-pc


### 2. Mock Serial 테스트 (하드웨어 불필요)
터미널 1: 가상 센서 PC (먼저 실행)
cd virtual-sensor-pc
conda activate daq-sensor-pc
python test_receive_mock.py

터미널 2: 통신 PC (나중에 실행)
cd communication-pc
conda activate daq-comm-pc
python test_send_mock.py

### 3. 실제 RS485 하드웨어 사용

#### 설정 변경
communication-pc/config/config.py
virtual-sensor-pc/config/config.py
USE_MOCK_SERIAL = False # Mock → Real 전환

실제 포트 번호 설정
REAL_PORT_COMM = 'COM3' # 실제 포트로 변경
REAL_PORT_SENSOR = 'COM4' # 실제 포트로 변경

#### 실행
포트 확인
python -m serial.tools.list_ports

테스트 실행 (Mock과 동일한 방법)
터미널 1
cd virtual-sensor-pc
python test_receive.py

터미널 2
cd communication-pc
python test_send.py

## 📊 결과 분석

### 로그 파일 확인

#### 통신 PC 로그
communication-pc/logs/
├── call_log_YYYYMMDD.csv # 호출/응답 로그
└── error_log_YYYYMMDD.txt # 에러 로그

#### 가상 센서 PC 로그
virtual-sensor-pc/logs/
├── request_log_YYYYMMDD.csv # 요청 처리 로그
└── sensor_data_log_YYYYMMDD.csv # 센서 데이터 로그


### 신뢰도 계산

cd communication-pc/src
python reliability_calculator.

### 엑셀 리포트 생성

cd communication-pc/src
python excel_exporter.py

**생성된 파일**: `communication-pc/output/reliability_report_YYYYMMDD_HHMMSS.xlsx`

엑셀 파일 시트:
- **통신 로그**: 전체 통신 기록 (성공/실패 색상 구분)
- **통계 요약**: 성공률, 응답 시간 통계, 에러 패턴
- **응답 시간 그래프**: 시간에 따른 응답 시간 추이

## ⚙️ 설정

### 주요 설정 항목 (config/config.py)
실행 모드
USE_MOCK_SERIAL = True # Mock/Real 전환

통신 설정
BAUDRATE = 9600 # 통신 속도
TIMEOUT = 5 # 응답 대기 시간 (초)
INTER_REQUEST_DELAY = 1.0 # 요청 간 지연 (초)

테스트 설정
TEST_CYCLES = 10000 # 총 테스트 횟수
TARGET_RELIABILITY = 99.0 # 목표 신뢰도 (%)

센서 범위 (가상 센서 PC)
SENSOR_RANGES = {
'temperature': {'min': 23.0, 'max': 27.0, 'unit': '℃'},
'humidity': {'min': 55.0, 'max': 65.0, 'unit': '%'},
'pressure': {'min': 1003.0, 'max': 1023.0, 'unit': 'hPa'},
'voltage': {'min': 3.2, 'max': 3.4, 'unit': 'V'}
}

## 🔧 기술 스택

- **언어**: Python 3.10.18
- **환경 관리**: Miniconda
- **시리얼 통신**: pyserial
- **데이터 처리**: pandas, numpy
- **엑셀 생성**: openpyxl
- **버전 관리**: Git

## 📈 성능 지표

측정 항목:
- 통신 성공률 (%)
- 평균/최소/최대 응답 시간 (ms)
- 타임아웃 발생 횟수
- 에러 유형별 발생 횟수
- 시간대별 성공률

목표:
- **신뢰도 99% 이상**
- 평균 응답 시간 < 1000ms

## 🐛 문제 해결

### Mock Serial 통신 안 됨
- 두 프로그램이 같은 시스템 임시 폴더를 사용하는지 확인
- 가상 센서 PC를 먼저 실행했는지 확인
- `mock_serial_comm` 폴더 권한 확인

### 실제 RS485 포트 인식 안 됨
포트 확인
python -m serial.tools.list_ports

장치 관리자에서 COM 포트 확인 (Windows)
제어판 > 장치 관리자 > 포트(COM & LPT)

### pyserial 설치 오류
가상환경 활성화 확인
conda activate daq-comm-pc

재설치
pip uninstall pyserial
pip install pyserial

**최종 업데이트**: 2025-10-17