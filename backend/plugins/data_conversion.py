###########################################
#   Example for a new plugin with needed  #
#   class / methods for plugin discovery  #
###########################################
from util_internal.conversions import bytearray_to_blocks
# To export API endpoints
from fastapi import APIRouter
from pydantic import BaseModel
import binascii

class BinaryRequest(BaseModel):
    data: str

class HexRequest(BaseModel):
    data: str

class BothRequest(BaseModel):
    data: str

# All logic should be contained in the Plugin class, for plugin discovery/import
class Plugin():

    # Plugin metadata
    name = "plugins.data_conversion"
    # Full names (e.g. "plugins.diff") of all dependencies in a list
    dependencies = []
    # API endpoints contained in the plugin
    # should contain the URI and relevant tags so they can be discovered / loaded by the frontend
    # tags are 
    endpoints = {}

    # Instantiate router instance, all plugins are prefixed with at least /plugins
    router = APIRouter(
        prefix="/plugins"
    )

    # method called during plugin discovery to register API endpoints
    # return None if no endpoints should be registered
    def register(self):
        # return None
        return self.router
    


    @router.post("/strToBinary")
    def run(binary_request: BinaryRequest):
        return ''.join(format(ord(i), '08b') for i in binary_request.data)

    @router.post("/hexToBinary")
    def run(hex_request: HexRequest):
        return "{0:08b}".format(int(hex_request.data, 16)) 
    @router.post("/strToBoth")
    def run(both_request: BothRequest):
        binary = ''.join(format(ord(i), '08b') for i in both_request.data)
        response = {
            "binary": binary,
            "hex": binascii.hexlify(bytes(both_request.data, encoding="utf8"))
        } 
        return response