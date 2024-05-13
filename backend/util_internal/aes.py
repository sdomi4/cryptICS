from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def aes_encrypt(data: str, mode: str):
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
    data = data.encode()
    if padding_needed:
        data = pad(data, 16)
    
    key = get_random_bytes(16)
    cipher = AES.new(key, cipher_mode)

    ciphertext = cipher.encrypt(data)

    return {
        "key": key.hex(),
        "ciphertext": ciphertext.hex()
    }