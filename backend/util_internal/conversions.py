import binascii

def hex_to_blocks(hex_data: str, block_size: int) -> list[str]:
    # typecast to int, expect user to be smart enough to provide reasonable block size
    n = int(block_size / 4)
    return [hex_data[i:i+n] for i in range(0, len(hex_data), n)]
    

def binary_to_blocks(binary_data: str, block_size: int) -> list[str]:
    return [binary_data[i:i+block_size] for i in range(0, len(binary_data), block_size)]

def hex_to_binary(hex_data: str) -> str:
    binary = "{0:08b}".format(int(hex_data, 16))
    # check if leading zeroes were lost
    if len(binary) < len(hex_data) * 4:
        binary = "0" * (len(hex_data) * 4 - len(binary)) + binary
    return binary

def str_to_binary(data: str) -> str:
    return ''.join(format(ord(i), '08b') for i in data)

def str_to_hex(data: str) -> str:
    return binascii.hexlify(bytes(data, encoding="utf8"))

def binary_to_hex(binary_data: str) -> str:
    return hex(int(binary_data, 2))[2:]

def binary_to_bytes(binary_data: str) -> bytes:
    hex_data = binary_to_hex(binary_data)
    return bytes.fromhex(hex_data)