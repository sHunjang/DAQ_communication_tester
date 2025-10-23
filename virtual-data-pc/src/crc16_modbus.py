"""
=================================================================
파일명: virtual-data-pc/src/crc16_modbus.py
설명: Modbus RTU CRC16 계산 모듈
=================================================================
"""

def calculate_crc16_modbus(data):
    """
    Modbus RTU CRC16 계산
    
    Args:
        data: 바이트 데이터
    
    Returns:
        int: CRC16 값
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
    CRC16 검증
    
    Args:
        data_with_crc: CRC16이 포함된 데이터
    
    Returns:
        bool: 유효하면 True
    """
    if len(data_with_crc) < 3:
        return False
    
    data = data_with_crc[:-2]
    received_crc = int.from_bytes(data_with_crc[-2:], byteorder='little')
    calculated_crc = calculate_crc16_modbus(data)
    
    return calculated_crc == received_crc

def append_crc16(data):
    """데이터에 CRC16 추가"""
    crc = calculate_crc16_modbus(data)
    return data + crc.to_bytes(2, byteorder='little')
