"""
=================================================================
파일명: crc16_modbus.py
설명: Modbus RTU 프로토콜용 CRC16 체크섬 계산 모듈
작성일: 2025-10-24
=================================================================
Modbus RTU 통신에서 사용하는 CRC16 체크섬을 계산하고 검증합니다.

CRC16-Modbus 규격:
- 다항식: 0xA001 (reversed polynomial)
- 초기값: 0xFFFF
- Little-endian 바이트 순서

주요 기능:
1. CRC16 계산: calculate_crc16_modbus()
2. CRC16 검증: verify_crc16()
3. CRC16 추가: append_crc16()

사용 예시:
    # 1. CRC 계산
    data = b'\x01\x03\x00\x00\x00\x0A'
    crc = calculate_crc16_modbus(data)
    
    # 2. 데이터에 CRC 추가
    data_with_crc = append_crc16(data)
    
    # 3. CRC 검증
    is_valid = verify_crc16(data_with_crc)
=================================================================
"""

def calculate_crc16_modbus(data):
    """
    Modbus RTU CRC16 체크섬 계산
    
    CRC16-Modbus는 데이터 전송 중 오류를 검출하기 위한 체크섬 알고리즘입니다.
    송신측과 수신측이 같은 데이터에 대해 같은 CRC 값을 계산해야 통신이 정상입니다.
    
    알고리즘 동작:
    1. CRC 레지스터를 0xFFFF로 초기화
    2. 데이터의 각 바이트에 대해:
       a. CRC 레지스터와 바이트를 XOR
       b. 8번 반복:
          - LSB(최하위 비트)가 1이면: 오른쪽 시프트 후 0xA001과 XOR
          - LSB가 0이면: 오른쪽 시프트만 수행
    3. 최종 CRC 레지스터 값 반환
    
    Args:
        data (bytes): CRC를 계산할 바이트 데이터
    
    Returns:
        int: 16비트 CRC 값 (0x0000 ~ 0xFFFF)
    
    Example:
        >>> data = b'\x01\x03\x00\x00\x00\x0A'
        >>> crc = calculate_crc16_modbus(data)
        >>> print(f"CRC: 0x{crc:04X}")
        CRC: 0xC5CD
    """
    # CRC 레지스터 초기화 (Modbus RTU 규격)
    crc = 0xFFFF
    
    # 데이터의 각 바이트에 대해 CRC 계산
    for byte in data:
        # 현재 바이트와 CRC 레지스터의 하위 8비트를 XOR
        crc ^= byte
        
        # 8번 비트 시프트 수행
        for _ in range(8):
            # LSB(최하위 비트) 확인
            if crc & 0x0001:
                # LSB가 1이면: 오른쪽 시프트 후 다항식과 XOR
                crc = (crc >> 1) ^ 0xA001
            else:
                # LSB가 0이면: 오른쪽 시프트만
                crc >>= 1
    
    return crc

def verify_crc16(data_with_crc):
    """
    CRC16이 포함된 데이터의 유효성 검증
    
    수신한 데이터의 마지막 2바이트가 올바른 CRC 값인지 확인합니다.
    데이터가 전송 중에 손상되지 않았는지 검증하는 데 사용됩니다.
    
    검증 과정:
    1. 데이터와 CRC를 분리 (마지막 2바이트가 CRC)
    2. 데이터 부분에 대해 CRC 재계산
    3. 재계산한 CRC와 수신한 CRC 비교
    
    Args:
        data_with_crc (bytes): CRC16이 포함된 전체 데이터
                              (마지막 2바이트가 CRC, Little-endian)
    
    Returns:
        bool: CRC가 유효하면 True, 그렇지 않으면 False
    
    Example:
        >>> # 올바른 CRC를 가진 데이터
        >>> frame = b'\x01\x03\x00\x00\x00\x0A\xCD\xC5'
        >>> is_valid = verify_crc16(frame)
        >>> print(f"유효성: {is_valid}")
        유효성: True
        
        >>> # 잘못된 CRC를 가진 데이터
        >>> bad_frame = b'\x01\x03\x00\x00\x00\x0A\x00\x00'
        >>> is_valid = verify_crc16(bad_frame)
        >>> print(f"유효성: {is_valid}")
        유효성: False
    """
    # 최소 길이 확인 (데이터 1바이트 + CRC 2바이트 = 최소 3바이트)
    if len(data_with_crc) < 3:
        return False
    
    # 데이터와 CRC 분리
    data = data_with_crc[:-2]  # 마지막 2바이트 제외
    received_crc = int.from_bytes(data_with_crc[-2:], byteorder='little')
    
    # 데이터 부분에 대해 CRC 재계산
    calculated_crc = calculate_crc16_modbus(data)
    
    # 계산한 CRC와 수신한 CRC 비교
    return calculated_crc == received_crc

def append_crc16(data):
    """
    데이터에 CRC16을 계산하여 추가
    
    전송할 데이터의 끝에 CRC16을 자동으로 추가합니다.
    Little-endian 바이트 순서로 추가됩니다.
    
    Args:
        data (bytes): 원본 데이터
    
    Returns:
        bytes: CRC16이 추가된 데이터 (원본 + 2바이트 CRC)
    
    Example:
        >>> data = b'\x01\x03\x00\x00\x00\x0A'
        >>> data_with_crc = append_crc16(data)
        >>> print(data_with_crc.hex(' ').upper())
        01 03 00 00 00 0A CD C5
        #                   ^^^^^ CRC16 (Little-endian)
    """
    # CRC 계산
    crc = calculate_crc16_modbus(data)
    
    # CRC를 Little-endian 2바이트로 변환하여 추가
    # 예: CRC = 0xC5CD -> 바이트로 변환 시 CD C5 (낮은 바이트가 먼저)
    return data + crc.to_bytes(2, byteorder='little')


# =================================================================
# 테스트 코드 (이 파일을 직접 실행할 때만 동작)
# =================================================================
if __name__ == "__main__":
    print("="*70)
    print("CRC16 Modbus 계산기 테스트")
    print("="*70)
    
    # =================================================================
    # 테스트 케이스 1: 표준 Modbus 요청 프레임
    # =================================================================
    print("\n[테스트 1] 표준 Modbus Read Holding Registers 요청")
    print("-"*70)
    
    # Slave ID: 0x01
    # Function Code: 0x03 (Read Holding Registers)
    # Starting Address: 0x0000
    # Quantity: 0x000A (10개 레지스터)
    request = bytes.fromhex('01 03 00 00 00 0A')
    print(f"요청 데이터: {request.hex(' ').upper()}")
    
    # CRC 계산
    crc = calculate_crc16_modbus(request)
    print(f"계산된 CRC: 0x{crc:04X}")
    print(f"Little-endian 바이트: {crc.to_bytes(2, 'little').hex(' ').upper()}")
    
    # 예상 CRC: 0xC5CD (Little-endian: CD C5)
    expected_crc = 0xC5CD
    print(f"예상 CRC: 0x{expected_crc:04X}")
    print(f"결과: {'✓ 일치' if crc == expected_crc else '✗ 불일치'}")
    
    # =================================================================
    # 테스트 케이스 2: CRC 추가 및 검증
    # =================================================================
    print("\n[테스트 2] CRC 추가 및 검증")
    print("-"*70)
    
    # CRC 추가
    frame_with_crc = append_crc16(request)
    print(f"CRC 추가된 프레임: {frame_with_crc.hex(' ').upper()}")
    
    # CRC 검증
    is_valid = verify_crc16(frame_with_crc)
    print(f"CRC 검증: {'✓ 유효' if is_valid else '✗ 유효하지 않음'}")
    
    # =================================================================
    # 테스트 케이스 3: 잘못된 CRC 검출
    # =================================================================
    print("\n[테스트 3] 잘못된 CRC 검출")
    print("-"*70)
    
    # 일부러 잘못된 CRC 생성
    bad_frame = request + bytes([0x00, 0x00])
    print(f"잘못된 프레임: {bad_frame.hex(' ').upper()}")
    
    is_valid = verify_crc16(bad_frame)
    print(f"CRC 검증: {'✗ 유효 (예상 밖)' if is_valid else '✓ 유효하지 않음 (예상된 결과)'}")
    
    # =================================================================
    # 테스트 케이스 4: DAQ 프로토콜 데이터
    # =================================================================
    print("\n[테스트 4] DAQ 프로토콜 단상 전력량계 데이터")
    print("-"*70)
    
    # Length=12, Serial=0, MSG Type=0x01, 
    # 전압=221.2V(0x08A4), 전류=12.34A(0x04D2), 전력=12.345kW(0x3039), 전력량=12345kWh(0x00003039)
    daq_data = bytes.fromhex('0C 00 01 08A4 04D2 3039 00003039')
    print(f"DAQ 데이터: {daq_data.hex(' ').upper()}")
    
    crc = calculate_crc16_modbus(daq_data)
    print(f"계산된 CRC: 0x{crc:04X}")
    print(f"Little-endian: {crc.to_bytes(2, 'little').hex(' ').upper()}")
    
    # 전체 프레임
    full_frame = append_crc16(daq_data)
    print(f"전체 프레임: {full_frame.hex(' ').upper()}")
    
    # 검증
    is_valid = verify_crc16(full_frame)
    print(f"CRC 검증: {'✓ 유효' if is_valid else '✗ 유효하지 않음'}")
    
    # =================================================================
    # 종료
    # =================================================================
    print("\n" + "="*70)
    print("✓ 모든 테스트 완료")
    print("="*70)
