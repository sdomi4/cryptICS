###########################################
#   Example for a new plugin with needed  #
#   class / methods for plugin discovery  #
###########################################

# To export API endpoints
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from Crypto.Random import get_random_bytes
from Crypto.Random.random import randrange

from backend.util_internal.aes import aes_encrypt, aes_decrypt
from backend.util_internal.conversions import str_to_binary, hex_to_binary
from backend.util_internal.conversions import binary_to_blocks, hex_to_blocks

class EncryptRequest(BaseModel):
    mode: str
    data: str
    key: str
    size: int

class FaultPostRequest(BaseModel):
    key: str
    ciphertext: dict
    fault_indexes: dict
    iv: str
    nonce: str

class FaultPostResponse(BaseModel):
    cleartext: dict

class EncryptResponse(BaseModel):
    mode: str
    key: str
    data: dict

class CipherResponse(BaseModel):
    ciphers: list[str]

class ConfusionDiffusionResponse(BaseModel):
    cleartext: list[str]
    key: str
    ciphertext: list[str]
    diffusion: dict
    confusion: dict

class FaultGetResponse(BaseModel):
    cleartext: list[str]
    key: str
    iv: str
    nonce: str
    ciphertext: dict

# All logic should be contained in the Plugin class, for plugin discovery/import
class Plugin():

    # Plugin metadata
    name = "plugins.blockciphers"
    # Full names (e.g. "plugins.diff") of all dependencies in a list
    dependencies = []
    # API endpoints contained in the plugin
    # should contain the URI and relevant tags so they can be discovered / loaded by the frontend
    # tags determine where the URLs might be loaded in the frontend
    #
    # predefined tags:
    # - homepage: the starting point, dynamically added to the front page (with the extra field "description" for the text on the home page)
    # - navbar: the subpages of the module, dynamically added to the navbar
    #
    # tags can be added as needed for the subpages
    endpoints = [
        {
            "uri": "/plugins/blockciphers",
            "tag": "homepage",
            "description": {
                "de": "Blockchiffren",
                "en": "Block Ciphers"
            }
        }
    ]

    # Instantiate router instance, all plugins are prefixed with at least /plugins
    router = APIRouter(
        prefix="/plugins"
    )

    # method called during plugin discovery to register API endpoints
    # return None if no endpoints should be registered
    def register(self):
        # return None
        return self.router
    
    @router.get("/blockciphers/ciphers", response_model=CipherResponse)
    def run():
        return {"ciphers": ["AES128", "AES192", "AES256"]}
    
    @router.post("/blockciphers/encrypt", response_model=EncryptResponse)
    def run(encrypt_request: EncryptRequest):
        if encrypt_request.key == "random":
            encrypt_request.key = None
        if encrypt_request.data == "random":
            encrypt_request.data = get_random_bytes(encrypt_request.size)
        encrypt_response = aes_encrypt(encrypt_request.data, encrypt_request.mode, encrypt_request.key)
        if encrypt_response is None:
            raise HTTPException(status_code=400, detail="Invalid mode")
        
        print(encrypt_response)

        # convert plaintext/ciphertext to blocks of binary data
        plaintext = binary_to_blocks(str_to_binary(encrypt_request.data), 128)
        ciphertext = binary_to_blocks(hex_to_binary(encrypt_response["ciphertext"]), 128)

        return {
            "mode": encrypt_request.mode,
            "key": encrypt_response["key"],
            "data": {
                "plaintext": plaintext,
                "ciphertext": ciphertext
            }
        }
    
    @router.get("/blockciphers/confusion-diffusion", response_model=ConfusionDiffusionResponse)
    def run():
        random_input = get_random_bytes(32)
        random_key = get_random_bytes(16)

        # key with 1 random bit changed
        confusion_key = bytearray(random_key)
        confusion_key[randrange(0, 15)] ^= 1 << randrange(0, 7)

        diffusion_input = bytearray(random_input)
        diffusion_input[randrange(0, 15)] ^= 1 << randrange(0, 7)

        encrypt_response = aes_encrypt(random_input, "ECB", random_key)
        confusion_response = aes_encrypt(random_input, "ECB", bytes(confusion_key))
        diffusion_repsonse = aes_encrypt(bytes(diffusion_input), "ECB", random_key)

        return {
            "cleartext": binary_to_blocks(hex_to_binary(random_input.hex()), 128),
            "key": random_key.hex(),
            "ciphertext": binary_to_blocks(hex_to_binary(encrypt_response["ciphertext"]), 128),
            "diffusion": {
                "cleartext": binary_to_blocks(hex_to_binary(diffusion_input.hex()), 128),
                "ciphertext": binary_to_blocks(hex_to_binary(diffusion_repsonse["ciphertext"]), 128)
            },
            "confusion": {
                "key": confusion_key.hex(),
                "ciphertext": binary_to_blocks(hex_to_binary(confusion_response["ciphertext"]), 128)
            }
        }
    
    @router.post("/blockciphers/faults", response_model=FaultPostResponse)
    def run(fault_request: FaultPostRequest):
        print(fault_request.fault_indexes)
        ecb_ciphertext = fault_request.ciphertext["ECB"]
        cbc_ciphertext = fault_request.ciphertext["CBC"]
        ctr_ciphertext = fault_request.ciphertext["CTR"]
        ofb_ciphertext = fault_request.ciphertext["OFB"]
        cfb_ciphertext = fault_request.ciphertext["CFB"]

        # flip a bit at specified indexes
        for block in fault_request.fault_indexes:
            print("checking block", block)
            print(fault_request.fault_indexes[block])
            for index in fault_request.fault_indexes[block]:
                # this unholy garbage took me like 2 hours
                # there might be a less cursed way but i'm too cooked to care
                # takes the hex number (string) at the specified index, casts it to be a hex number, then casts it to binary, flips the last bit of the nibble, then casts it back to hex
                ecb_ciphertext[int(block)] = ecb_ciphertext[int(block)][:int(index)] + format(int(bin(int(ecb_ciphertext[int(block)][int(index)], 16)), 2)^1, 'x') + ecb_ciphertext[int(block)][int(index)+1:]
                cbc_ciphertext[int(block)] = cbc_ciphertext[int(block)][:int(index)] + format(int(bin(int(cbc_ciphertext[int(block)][int(index)], 16)), 2)^1, 'x') + cbc_ciphertext[int(block)][int(index)+1:]
                ctr_ciphertext[int(block)] = ctr_ciphertext[int(block)][:int(index)] + format(int(bin(int(ctr_ciphertext[int(block)][int(index)], 16)), 2)^1, 'x') + ctr_ciphertext[int(block)][int(index)+1:]
                ofb_ciphertext[int(block)] = ofb_ciphertext[int(block)][:int(index)] + format(int(bin(int(ofb_ciphertext[int(block)][int(index)], 16)), 2)^1, 'x') + ofb_ciphertext[int(block)][int(index)+1:]
                cfb_ciphertext[int(block)] = cfb_ciphertext[int(block)][:int(index)] + format(int(bin(int(cfb_ciphertext[int(block)][int(index)], 16)), 2)^1, 'x') + cfb_ciphertext[int(block)][int(index)+1:]

        ecb_ciphertext= ''.join(ecb_ciphertext)
        cbc_ciphertext= ''.join(cbc_ciphertext)
        ctr_ciphertext= ''.join(ctr_ciphertext)
        ofb_ciphertext= ''.join(ofb_ciphertext)
        cfb_ciphertext= ''.join(cfb_ciphertext)

        # decrypt the faulty ciphertext with all modes
        decrypt_ecb = aes_decrypt(bytes.fromhex(ecb_ciphertext), "ECB", fault_request.key)
        decrypt_cbc = aes_decrypt(bytes.fromhex(cbc_ciphertext), "CBC", fault_request.key, iv=fault_request.iv)
        decrypt_ctr = aes_decrypt(bytes.fromhex(ctr_ciphertext), "CTR", fault_request.key, nonce=fault_request.nonce)
        decrypt_ofb = aes_decrypt(bytes.fromhex(ofb_ciphertext), "OFB", fault_request.key, iv=fault_request.iv)
        decrypt_cfb = aes_decrypt(bytes.fromhex(cfb_ciphertext), "CFB", fault_request.key, iv=fault_request.iv)

        return {
            "cleartext": {
                "ECB": hex_to_blocks(decrypt_ecb, 128),
                "CBC": hex_to_blocks(decrypt_cbc, 128),
                "CTR": hex_to_blocks(decrypt_ctr, 128),
                "OFB": hex_to_blocks(decrypt_ofb, 128),
                "CFB": hex_to_blocks(decrypt_cfb, 128)
            }
        }

    
    @router.get("/blockciphers/faults", response_model=FaultGetResponse)
    def run():
        # encrypt random data, 4 blocks to show error propagation properly
        random_input = get_random_bytes(64)
        random_key = get_random_bytes(16)
        iv = get_random_bytes(16)
        nonce = get_random_bytes(8)

        ecb_response = aes_encrypt(random_input, "ECB", random_key)
        cbc_response = aes_encrypt(random_input, "CBC", random_key, iv=iv)
        ctr_response = aes_encrypt(random_input, "CTR", random_key, nonce=nonce)
        ofb_response = aes_encrypt(random_input, "OFB", random_key, iv=iv)
        cfb_response = aes_encrypt(random_input, "CFB", random_key, iv=iv)

        return {
            "cleartext": hex_to_blocks(random_input.hex(), 128),
            "key": random_key.hex(),
            "ciphertext": {
                "ECB": hex_to_blocks(ecb_response["ciphertext"], 128),
                "CBC": hex_to_blocks(cbc_response["ciphertext"], 128),
                "CTR": hex_to_blocks(ctr_response["ciphertext"], 128),
                "OFB": hex_to_blocks(ofb_response["ciphertext"], 128),
                "CFB": hex_to_blocks(cfb_response["ciphertext"], 128)
            },
            "iv": iv.hex(),
            "nonce": nonce.hex()
        }