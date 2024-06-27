###########################################
#   Example for a new plugin with needed  #
#   class / methods for plugin discovery  #
###########################################

# To export API endpoints
from fastapi import APIRouter, HTTPException
from backend.util_internal.hasher import create_hash
from backend.util_internal.conversions import hex_to_binary
from pydantic import BaseModel
import random

class HashRequest(BaseModel):
    algorithm: str
    data: str

class DiffusionRequest(BaseModel):
    algorithm: str
    data: str

class HashGetResponse(BaseModel):
    algorithms: list[str]

class HashPostResponse(BaseModel):
    hash: str

class DiffusionResponse(BaseModel):
    input: str
    hash: str
    hash_binary: str
    modified_hash: str
    modified_hash_binary: str

# All logic should be contained in the Plugin class, for plugin discovery/import
class Plugin():

    # Plugin metadata
    name = "plugins.hashing"
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
        # {
        #     "uri": "/plugins/hashing",
        #     "tag": "homepage",
        #     "description": "Hashing"
        # }
    ]

    
    

    # Instantiate router instance, all plugins are prefixed with at least /plugins
    router = APIRouter(
        prefix="/plugins"
    )

    # method called during plugin discovery to register API endpoints
    # return None if no endpoints should be registered
    def register(self):
        return self.router
    

    
    # Add any API endpoints and logic methods as needed for the plugin
    @router.post("/hash", response_model=HashPostResponse)
    def create_hash(hash_request: HashRequest):
        algorithm = hash_request.algorithm.lower()
        h = create_hash(algorithm=algorithm, data=hash_request.data)
        if h is None:
            raise HTTPException(status_code=404, detail="No such algorithm")
        return {"hash": h}
    
    @router.get("/hash", response_model=HashGetResponse)
    def algorithms():
        hashing_algorithms = ["BLAKE2b", "BLAKE2s", "CMAC", "cSHAKE128", "cSHAKE256", "HMAC", "KangarooTwelve", "keccak", "KMAC128", "KMAC256", "MD2", "MD4", "MD5", "Poly1305", "RIPEMD160", "SHA", "SHA1", "SHA224", "SHA256", "SHA384", "SHA3_224", "SHA3_256", "SHA3_384", "SHA3_512", "SHA512", "SHAKE128", "SHAKE256", "TupleHash128", "TupleHash256"]
        return {"algorithms": hashing_algorithms}