import binascii


def bytearray_to_blocks(data: bytearray, block_size: int) -> list:
        return [data[i:i+block_size] for i in range(0, len(data), block_size)]

def hex_to_binary(hex_data: str) -> str:
    return "{0:08b}".format(int(hex_data, 16))

def str_to_binary(data: str) -> str:
    return ''.join(format(ord(i), '08b') for i in data)

def str_to_hex(data: str) -> str:
    return binascii.hexlify(bytes(data, encoding="utf8"))

def binary_to_hex(binary_data: str) -> str:
    return hex(int(binary_data, 2))[2:]