from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# does not perform any padding, use aes_encrypt_unaligned for that
# this is mostly for neat demonstrations with known length data
def aes_encrypt(data: str, mode: str, key: str = None):
    padding_needed = False
    match mode:
        case "ECB":
            cipher_mode = AES.MODE_ECB
        case "CBC":
            cipher_mode = AES.MODE_CBC
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
    
    if key is None:
        key = get_random_bytes(16)
    cipher = AES.new(key, cipher_mode)

    ciphertext = cipher.encrypt(data)

    return {
        "key": key.hex(),
        "ciphertext": ciphertext.hex()
    }

def aes_encrypt_unaligned(data: str, mode: str, key: str = None, padding: str = "PKCS7"):
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
    if padding_needed:
        data = pad(data, 16, padding)
    
    if key is None:
        key = get_random_bytes(16)
    cipher = AES.new(key, cipher_mode)

    ciphertext = cipher.encrypt(data)

    return {
        "key": key.hex(),
        "ciphertext": ciphertext.hex()
    }

# does not perform any unpadding, use aes_decrypt_unaligned for that
def aes_decrypt(data: str, mode: str, key: str):
    padded = False
    match mode:
        case "ECB":
            cipher_mode = AES.MODE_ECB
        case "CBC":
            cipher_mode = AES.MODE_CBC
        case "CTR":
            cipher_mode = AES.MODE_CTR
        case "OFB":
            cipher_mode = AES.MODE_OFB
        case "CFB":
            cipher_mode = AES.MODE_CFB
        case _:
            return None
    if not isinstance(data, bytes):
        data = bytes.fromhex(data)

    if not isinstance(key, bytes):
        key = bytes.fromhex(key)
    
    cipher = AES.new(key, cipher_mode)
    data = cipher.decrypt(data)
    return data.hex()

def aes_decrypt_unaligned(data: str, mode: str, key: str, padding: str = "PKCS7"):
    padded = False
    match mode:
        case "ECB":
            cipher_mode = AES.MODE_ECB
            padded = True
        case "CBC":
            cipher_mode = AES.MODE_CBC
            padded = True
        case "CTR":
            cipher_mode = AES.MODE_CTR
        case "OFB":
            cipher_mode = AES.MODE_OFB
        case "CFB":
            cipher_mode = AES.MODE_CFB
        case _:
            return None
    if not isinstance(data, bytes):
        data = bytes.fromhex(data)

    if not isinstance(key, bytes):
        key = bytes.fromhex(key)
    
    cipher = AES.new(key, cipher_mode)
    data = cipher.decrypt(data)
    if padded:
        data = unpad(data, 16)
    return data.hex()