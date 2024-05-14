from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def aes_encrypt(data: str, mode: str, key: str = None):
    padding_needed = False
    match mode:
        case "ECB":
            cipher_mode = AES.MODE_ECB
            padding_needed = True
        case "CBC":
            cipher_mode = AES.MODE_CBC
            padding_needed = True
        case "CTR":
            cipher_mode = AES.MODE_CTR
        case "OFB":
            cipher_mode = AES.MODE_OFB
        case "CFB":
            cipher_mode = AES.MODE_CFB
        case _:
            return None
    if not isinstance(data, bytes):
        data = data.encode()
    if padding_needed and len(data) % 16 != 0:
        data = pad(data, 16)
    
    if key is None:
        key = get_random_bytes(16)
    cipher = AES.new(key, cipher_mode)

    ciphertext = cipher.encrypt(data)

    return {
        "key": key.hex(),
        "ciphertext": ciphertext.hex()
    }