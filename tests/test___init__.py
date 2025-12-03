from util import decrypt_bytes


def test_decrypt_bytes():
    buf = [1,2,3,4,5,6,7,8]
    crc = 12345
    output = decrypt_bytes(bytes(buf), crc)
    print(output)