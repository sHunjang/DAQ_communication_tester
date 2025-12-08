# Modbus Power Monitor (1P2W / 3P3W / 3P4W)

병원 전력 계측 보드를 대상으로, Modbus 통신으로 수집한 데이터를
GUI(Pyside6)로 모니터링하는 도구.  
단상 1P2W와 3상 3선/4선(3P3W / 3P4W)의 전압, 전류, 유효전력, 전력량(kWh)을
실시간으로 표시하고, 통신 로그를 타임스탬프와 함께 확인

---

## Features

- 시리얼(Modbus RTU) 기반 실시간 데이터 수집
- 1P2W / 3P3W / 3P4W 계측값 분리 표시
  - 전압 [V]
  - 전류 [A]
  - 유효전력 [kW]
  - 전력량 [kWh]
- 상별 전력량(kWh) 표시
  - 1P2W: 4바이트 누적 kWh
  - 3P3W/3P4W: 각 상별 kWh(보드 정의에 맞게 WORD 단위 파싱)
- 통신 로그 뷰
  - 수신 패킷(RX) 및 에러 메시지 타임스탬프 출력
  - Log Clear 버튼으로 로그 삭제 가능

---

## Tech Stack

- Language: Python 3.10
- GUI: PySide6 (Qt for Python)
- Serial Communication: pyserial
- OS: Windows 기준 개발/테스트

---

## Installation

```bash
pip install PySide6 pyserial
```

---

## Usage

1. 계측 보드와 PC를 시리얼(USB-Serial 등)로 연결
2. `main.py` 실행

```bash
python main.py
```

3. 프로그램 상단에서:
   - `Port`: 연결된 COM 포트 선택 (예: COM3, COM10)
   - `Baud`: 통신 속도 선택 (기본 9600)
   - `Open` 버튼 클릭 → 통신 시작
   - `Close` 버튼 클릭 → 통신 종료

4. 화면 구성
   - 1P2W: 단상 전압/전류/유효전력/전력량
   - 3P3W: 3상3선 L1/L2/L3별 전압, 전류, 유효전력, 전력량
   - 3P4W: 3상4선 L1/L2/L3/N별 전류 및 상별 전력량
   - Log 영역: 하단에서 타임스탬프와 함께 RX 로그/에러 확인
     - `Log Clear` 버튼으로 기록 삭제

---

## Protocol Overview

- 시작/종료
  - STX: `0x02` - {02}
  - ETX: `0x03` - {03}
- CRC:
  - CRC16 Modbus (초기값 0xFFFF, 다항식 0xA001)
  - 프레임 중 `[TYPE ... DATA ...]` 구간에 대해 계산
  - 프레임 내에서는 Little Endian(Lo, Hi) 순서로 전송

- 메시지 타입 및 길이

| Type | 의미        | 전체 길이(byte) | DATA 길이 |
|------|-------------|-----------------|-----------|
| 0x0C | 1P2W 단상   | 17              | 12        |
| 0x20 | 3P3W 3상3선 | 37              | 32        |
| 0x22 | 3P4W 3상4선 | 39              | 34        |

- DATA 필드 예시 (요약)

  - 1P2W (0x0C)
    - V: 2B
    - A: 2B
    - kW: 2B
    - kWh: 4B (32bit 정수)

  - 3P3W (0x20)
    - V1,V2,V3: 각 2B
    - A1,A2,A3: 각 2B
    - kW1,kW2,kW3: 각 2B
    - kWh1,kWh2,kWh3: 각 2B(WORD) 사용  
      (4바이트 필드 중 하위 WORD만 실제 kWh로 사용)

  - 3P4W (0x22)
    - V12,V23,V31: 각 2B
    - A1,A2,A3,N: 각 2B
    - kW1,kW2,kW3: 각 2B
    - kWh1,kWh2,kWh3: 각 2B(WORD) 사용

※ 실제 WORD 인덱스는 장비 프로토콜 문서를 기준으로 매핑되었습니다.

---

## UI Details

- 전압: 정수값 / 10 → `XXX.X V`
- 전류: 정수값 / 100 → `XX.XX A`
- 유효전력: 정수값 / 1000 → `XX.XXX kW`
- 전력량:
  - 1P2W: 32bit 정수 kWh
  - 3P3W/3P4W: WORD 단위 정수 kWh

---

## Logging

- 로그 포맷 예:
```bash
[2025-03-17 15:48:30] COM OPEN
[2025-03-17 15:48:31] RX: 02 20 00 02 0e db ...
[2025-03-17 15:48:32] RX Error: CRC mismatch ...
[2025-03-17 15:52:10] COM CLOSE
```

- 화면 하단 `Log` 영역에 누적 표시
- `Log Clear` 버튼 클릭 시 현재 로그 모두 삭제

---

## Project Structure (예시)

```bash
Modbus_Communication_lab/
├── main.py # 메인 GUI + 통신 로직
├── requirements.txt # 의존성 목록 (선택)
└── README.md
```

---

## TODO / 개선 아이디어

- Modbus RTU 외 TCP 지원
- 로그 파일로 저장 옵션 추가
- 알람/이벤트(전압/전류 임계값 초과) 표시
- 다국어 지원 (한/영 전환)

---