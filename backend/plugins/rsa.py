###########################################
#   Example for a new plugin with needed  #
#   class / methods for plugin discovery  #
###########################################

# To export API endpoints
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from base64 import b64encode, b64decode

from backend.util_internal.rsa import rsa_encrypt_unpadded, rsa_decrypt_unpadded, get_key

class UnpaddedEncryptRequest(BaseModel):
    data: int

class UnpaddedDecryptRequest(BaseModel):
    data: int

class UnpaddedDecryptResponse(BaseModel):
    decrypted_data: int

class UnpaddedEncryptResponse(BaseModel):
    encrypted_data: int
    key: dict

class HomomorphicResponse(BaseModel):
    initial_data: int
    encrypted_data: str
    modifier: int
    modified_data: str
    homomorphic_data: str
    decrypted_data: int
    key: dict

# All logic should be contained in the Plugin class, for plugin discovery/import
class Plugin():

    # Plugin metadata
    name = "plugins.rsa"
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
            "uri": "/plugins/rsa",
            "tag": "homepage",
            "description": "RSA"
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
    
    @router.post("/rsa/unpadded/encrypt", response_model=UnpaddedEncryptResponse)
    def run(unpadded_encrypt_request: UnpaddedEncryptRequest):
        key = get_key()
        n = key['n']
        e = key['e']
        d = key['d']
        data = unpadded_encrypt_request.data
        encrypted_data = rsa_encrypt_unpadded(data, e, n)
        return {
            "encrypted_data": encrypted_data,
            "key": {
                "n": n,
                "e": e,
                "d": d
            }
            }
    
    @router.post("/rsa/unpadded/decrypt", response_model=UnpaddedDecryptResponse)
    def run(unpadded_decrypt_request: UnpaddedDecryptRequest):
        key = get_key()
        n = key['n']
        e = key['e']
        d = key['d']
        data = unpadded_decrypt_request.data
        decrypted_data = rsa_decrypt_unpadded(data, n, d)
        return {
            "decrypted_data": decrypted_data,
        }
    
    @router.get("/rsa/homomorphic", response_model=HomomorphicResponse)
    def run():
        key = get_key()
        n = key['n']
        e = key['e']
        d = key['d']
        p = key['p']
        q = key['q']

        initial_data = 42
        encrypted_data = rsa_encrypt_unpadded(initial_data, e, n)
        
        modifier = 2
        modified_data = rsa_encrypt_unpadded(modifier, e, n)

        homomorphic_data = (encrypted_data * modified_data) % n

        decrypted_data = rsa_decrypt_unpadded(homomorphic_data, n, d)

        return {
            "initial_data": initial_data,
            "encrypted_data": hex(encrypted_data),
            "modifier": modifier,
            "modified_data": hex(modified_data),
            "homomorphic_data": hex(homomorphic_data),
            "decrypted_data": decrypted_data,
            "key": {
                "n": hex(n),
                "e": e,
                "d": hex(d),
                "p": p,
                "q": q
            }
        }