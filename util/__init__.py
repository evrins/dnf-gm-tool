import time


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        result = func(*args, **kwargs)
        end = time.perf_counter_ns()
        print(f'{func.__name__} took {(end - start) / 1_000_000.0:.4f} ms to run.')
        return result

    return wrapper


def decrypt_bytes(input_bytes: bytes, crc):
    """对原始字节流进行初步预处理"""
    key = 0x81A79011
    xor = crc ^ key
    int_num = len(input_bytes) // 4
    key_all = xor.to_bytes(4, 'little') * int_num
    value_xored_all = int.from_bytes(key_all, 'little') ^ int.from_bytes(
        input_bytes, 'little'
    )
    mask_1 = 0b00000000_00000000_00000000_00111111
    mask_2 = 0b11111111_11111111_11111111_11000000
    mask_1_all = int.from_bytes(mask_1.to_bytes(4, 'little') * int_num, 'little')
    mask_2_all = int.from_bytes(mask_2.to_bytes(4, 'little') * int_num, 'little')
    value_1 = value_xored_all & mask_1_all
    value_2 = value_xored_all & mask_2_all
    value = value_1 << 26 | value_2 >> 6
    return value.to_bytes(4 * int_num, 'little')


def decode_string_to_utf8(s: str) -> str:
    s1 = s.encode('latin1', 'replace')
    s2 = s.encode('cp1252', 'replace')
    s3 = b''
    for i in range(len(s1)):
        if s1[i : i + 1] == b'?':
            s3 += s2[i : i + 1]
        else:
            s3 += s1[i : i + 1]
    return s3.decode(errors='replace')
