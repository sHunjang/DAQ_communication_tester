# DAQ 통신 신뢰도 측정 시스템

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

RS485/RS232 통신을 통한 DAQ(Data Acquisition) 장치 신뢰도 자동 측정 시스템

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [시스템 구성](#시스템-구성)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [폴더 구조](#폴더-구조)
- [DAQ 프로토콜](#daq-프로토콜)
- [생성되는 파일](#생성되는-파일)
- [문제 해결](#문제-해결)

## 🎯 프로젝트 개요

이 프로젝트는 DAQ 장치와 PC 간 통신의 신뢰도를 자동으로 측정하고 분석하는 시스템입니다.

**개발 배경**:
- DAQ 장치의 통신 안정성 검증 필요
- 목표 신뢰도 99% 이상 달성 확인
- 실시간 센서 데이터 수집 및 분석

**활용 분야**:
- 전력량계 통신 검증
- 환경 센서 모니터링
- IoT 장치 신뢰도 테스트

## ✨ 주요 기능

### 1. 통신 테스트
- ✅ RS232/RS485 하드웨어 통신 지원
- ✅ Mock Serial을 통한 가상 테스트
- ✅ DAQ 바이너리 프로토콜 구현
- ✅ CRC16 Modbus 체크섬 검증
- ✅ 자동 재시도 및 타임아웃 처리

### 2. 데이터 로깅
- 📊 통신 로그 (call_log_YYYYMMDD.csv)
- 📊 센서 데이터 로그 (sensor_data_YYYYMMDD.csv)
- 📊 에러 로그 (error_log_YYYYMMDD.txt)

### 3. 신뢰도 분석
- 📈 전체 성공률 계산
- 📈 센서별 신뢰도 통계
- 📈 응답 시간 분석 (평균/최소/최대)
- 📈 MTBF (Mean Time Between Failures) 계산
- 📈 안정성 등급 평가 (S/A/B/C/D/F)

### 4. 리포트 생성
- 📑 Excel 자동 리포트 (.xlsx)
- 📑 Summary, CallLog, SensorData, Charts 시트
- 📑 차트 및 그래프 자동 생성

### 5. 지원 센서
| 센서 타입 | MSG Type | 데이터 크기 |
|----------|----------|-----------|
| 단상 전력량계 | 0x01 | 10 bytes |
| 3상3선 전력량계 | 0x02 | 30 bytes |
| 3상4선 전력량계 | 0x03 | 32 bytes |
| 유량 센서 | 0x04 | 8 bytes |
| 수도 계량기 | 0x05 | 4 bytes |
| CO2 센서 | 0x06 | 2 bytes |
| 온습도 센서 | 0x07 | 4 bytes |
| 일사량 센서 | 0x08 | 2 bytes |
| DC 모터 감시 | 0x09 | 1 byte |

## 🏗️ 시스템 구성

[통신 PC] ←→ RS232/RS485 ←→ [DAQ 장치] ←→ [센서들]

- **통신 PC (communication-pc)**: 데이터 수집, 로깅, 분석
- **가상 센서 PC (virtual-sensor-pc)**: DAQ 장치 시뮬레이터
- **Mock Serial**: 하드웨어 없이 통신 테스트

## 🛠️ 설치 방법

### 1. 필수 요구사항
- Python 3.10 이상
- Miniconda 또는 Anaconda
- Windows 10/11 (권장)

## 📡 DAQ 프로토콜

### 프레임 구조
[STX] [Length] [Serial No] [MSG Type] [Data] [CRC16] [ETX]
1B 1B 1B 1B N B 2B 1B

- **STX**: 0x02 (시작)
- **Length**: Payload 크기
- **Serial No**: 0~255 순환
- **MSG Type**: 센서 타입 (0x01~0x09)
- **Data**: 센서 데이터
- **CRC16**: Modbus CRC (Little-endian)
- **ETX**: 0x03 (종료)

### 예시: 단상 전력량계

02 0C 00 01 08A4 04D2 3039 00003039 E3EF 03
│ │ │ │ └─────────┬─────────┘ │ │
│ │ │ │ Data (10B) CRC ETX
│ │ │ └─ MSG Type (0x01)
│ │ └─ Serial No (0)
│ └─ Length (12)
└─ STX

파싱:

전압: 0x08A4 = 2212 → 221.2V

전류: 0x04D2 = 1234 → 12.34A

전력: 0x3039 = 12345 → 12.345kW

전력량: 0x00003039 = 12345kWh