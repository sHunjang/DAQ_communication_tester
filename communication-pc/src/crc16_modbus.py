"""
=================================================================
파일명: communication-pc/src/crc16_modbus.py
설명: Modbus RTU CRC16 계산 모듈
작성자: 개발팀
작성일: 2025-10-23
=================================================================
Modbus RTU 프로토콜에서 사용하는 CRC16 체크섬을 계산합니다.
다항식: 0xA001 (reversed polynomial)
초기값: 0xFFFF
=================================================================
"""

def calculate_crc16_modbus(data):
    """
    Modbus RTU CRC16 계산
    
    Args:
        data: 바이트 데이터 (bytes 또는 bytearray)
    
    Returns:
        int: CRC16 값 (16bit)
    
    Example:
        >>> data = b'\x02\x0C\x00\x01\x08\xA4\x04\xD2\x30\x39\x00\x00\x30\x39'
        >>> crc = calculate_crc16_modbus(data)
        >>> print(f"CRC16: 0x{crc:04X}")
    """
    crc = 0xFFFF
    
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    
    return crc

def verify_crc16(data_with_crc):
    """
    CRC16이 포함된 데이터의 유효성 검증
    
    Args:
        data_with_crc: CRC16이 포함된 전체 데이터 (마지막 2바이트가 CRC)
    
    Returns:
        bool: 유효하면 True, 아니면 False
    
    Example:
        >>> frame = b'\x02\x0C\x00\x01\x08\xA4\x04\xD2\x30\x39\x00\x00\x30\x39\xAB\xEC'
        >>> is_valid = verify_crc16(frame[1:-1])  # STX, ETX 제외
        >>> print(f"Valid: {is_valid}")
    """
    if len(data_with_crc) < 3:
        return False
    
    # 데이터와 CRC 분리
    data = data_with_crc[:-2]
    received_crc = int.from_bytes(data_with_crc[-2:], byteorder='little')
    
    # CRC 계산
    calculated_crc = calculate_crc16_modbus(data)
    
    return calculated_crc == received_crc

def append_crc16(data):
    """
    데이터에 CRC16을 추가
    
    Args:
        data: 원본 데이터 (bytes)
    
    Returns:
        bytes: CRC16이 추가된 데이터 (Little-endian)
    """
    crc = calculate_crc16_modbus(data)
    return data + crc.to_bytes(2, byteorder='little')


# =================================================================
# 테스트 코드
# =================================================================
if __name__ == "__main__":
    print("CRC16 Modbus 계산기 테스트\n")
    
    # 테스트 케이스 1: 단상 전력량계 프레임 (문서 예시)
    print("=" * 60)
    print("테스트 1: 단상 전력량계 프레임")
    print("=" * 60)
    
    # STX와 ETX를 제외한 데이터
    data = bytes.fromhex('0C 00 01 08A4 04D2 3039 00003039')
    print(f"데이터: {data.hex(' ').upper()}")
    
    crc = calculate_crc16_modbus(data)
    print(f"계산된 CRC16: 0x{crc:04X}")
    print(f"Little-endian: {crc.to_bytes(2, 'little').hex(' ').upper()}")
    
    # 전체 프레임 (예상 CRC: 0xABEC)
    expected_crc = 0xABEC
    print(f"예상 CRC16: 0x{expected_crc:04X}")
    print(f"일치 여부: {'✓' if crc == expected_crc else '✗'}")
    
    # 테스트 케이스 2: CRC 검증
    print("\n" + "=" * 60)
    print("테스트 2: CRC 검증")
    print("=" * 60)
    
    # 전체 프레임 (STX, ETX 제외)
    full_data = data + crc.to_bytes(2, 'little')
    print(f"전체 데이터: {full_data.hex(' ').upper()}")
    
    is_valid = verify_crc16(full_data)
    print(f"검증 결과: {'✓ 유효함' if is_valid else '✗ 유효하지 않음'}")
    
    # 테스트 케이스 3: 잘못된 CRC
    print("\n" + "=" * 60)
    print("테스트 3: 잘못된 CRC 검증")
    print("=" * 60)
    
    wrong_data = data + bytes([0x00, 0x00])  # 잘못된 CRC
    print(f"잘못된 데이터: {wrong_data.hex(' ').upper()}")
    
    is_valid = verify_crc16(wrong_data)
    print(f"검증 결과: {'✓ 유효함' if is_valid else '✗ 유효하지 않음 (예상된 결과)'}")
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)
