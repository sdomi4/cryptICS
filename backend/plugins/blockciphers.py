###########################################
#   Example for a new plugin with needed  #
#   class / methods for plugin discovery  #
###########################################

# To export API endpoints
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.util_internal.aes import aes_encrypt
from backend.util_internal.conversions import str_to_binary, hex_to_binary
from backend.util_internal.conversions import binary_to_blocks

class EncryptRequest(BaseModel):
    mode: str
    data: str

class EncryptResponse(BaseModel):
    mode: str
    key: str
    data: dict

class CipherResponse(BaseModel):
    ciphers: list[str]

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
            "description": "Block Ciphers"
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
        encrypt_response = aes_encrypt(encrypt_request.data, encrypt_request.mode)
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