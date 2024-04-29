###########################################
#   Example for a new plugin with needed  #
#   class / methods for plugin discovery  #
###########################################

# To export API endpoints
from fastapi import APIRouter, HTTPException
import Crypto.Hash
from pydantic import BaseModel

class HashRequest(BaseModel):
    algorithm: str
    data: str

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
        {
            "uri": "/plugins/hashing",
            "tag": "homepage",
            "description": "Hashing"
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
    

    
    # Add any API endpoints and logic methods as needed for the plugin
    @router.post("/hash", response_model=[])
    def run(hash_request: HashRequest):
        algorithm = hash_request.algorithm.lower()
        match algorithm:
            case "blake2b":
                h = Crypto.Hash.BLAKE2b.new()
            case "blake2s":
                h = Crypto.Hash.BLAKE2s.new()
            case "cmac":
                h = Crypto.Hash.CMAC.new()
            case "cshake128":
                h = Crypto.Hash.cSHAKE128.new()
            case "cshake256":
                h = Crypto.Hash.cSHAKE256.new()
            case "hmac":
                h = Crypto.Hash.HMAC.new()
            case "kangarootwelve":
                h = Crypto.Hash.KangarooTwelve.new()
            case "keccak":
                h = Crypto.Hash.keccak.new()
            case "kmac128":
                h = Crypto.Hash.KMAC128.new()
            case "kmac256":
                h = Crypto.Hash.KMAC256.new()
            case "md2":
                h = Crypto.Hash.MD2.new()
            case "md4":
                h = Crypto.Hash.MD4.new()
            case "md5":
                h = Crypto.Hash.MD5.new()
            case "poly1305":
                h = Crypto.Hash.Poly1305.new()
            case "ripemd" | "ripemd160":
                h = Crypto.Hash.RIPEMD160.new()
            case "sha":
                h = Crypto.Hash.SHA.new()
            case "sha1":
                h = Crypto.Hash.SHA1.new()
            case "sha224":
                h = Crypto.Hash.SHA224.new()
            case "sha256":
                h = Crypto.Hash.SHA256.new()
            case "sha384":
                h = Crypto.Hash.SHA384.new()
            case "sha3_224":
                h = Crypto.Hash.SHA3_224.new()
            case "sha3_256":
                h = Crypto.Hash.SHA3_256.new()
            case "sha3_384":
                h = Crypto.Hash.SHA3_384.new()
            case "sha3_512":
                h = Crypto.Hash.SHA3_512.new()
            case "sha512":
                h = Crypto.Hash.SHA512.new()
            case "shake128":
                h = Crypto.Hash.SHAKE128.new()
            case "shake256":
                h = Crypto.Hash.SHAKE256.new()
            case "tuplehash128":
                h = Crypto.Hash.TupleHash128.new()
            case "tuplehash256":
                h = Crypto.Hash.TupleHash256.new()
            case _:
                raise HTTPException(status_code=404, detail="No such algorithm")
        h.update(hash_request.data.encode())
        return h.hexdigest()
    
    @router.get("/algorithms", response_model=[])
    def run():
        default_hashing_algorithms = ["SHA1", "SHA256", "MD5", "Poly1305"]
        return default_hashing_algorithms
    
    @router.get("/allalgorithms", response_model=[])
    def run():
        hashing_algorithms = ["BLAKE2b", "BLAKE2s", "CMAC", "cSHAKE128", "cSHAKE256", "HMAC", "KangarooTwelve", "keccak", "KMAC128", "KMAC256", "MD2", "MD4", "MD5", "Poly1305", "RIPEMD160", "SHA", "SHA1", "SHA224", "SHA256", "SHA384", "SHA3_224", "SHA3_256", "SHA3_384", "SHA3_512", "SHA512", "SHAKE128", "SHAKE256", "TupleHash128", "TupleHash256"]
        return hashing_algorithms
