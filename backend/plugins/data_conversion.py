###########################################
#   Example for a new plugin with needed  #
#   class / methods for plugin discovery  #
###########################################

# To export API endpoints
from fastapi import APIRouter
from pydantic import BaseModel
import binascii
import backend.util_internal.conversions as conversions

class BinaryRequest(BaseModel):
    data: str

class BinaryResponse(BaseModel):
    data: str
    binary: str

class HexRequest(BaseModel):
    data: str

class HexResponse(BaseModel):
    data: str
    hex: str

class BothRequest(BaseModel):
    data: str

class BothResponse(BaseModel):
    data: str
    binary: str
    hex: str

class BlockRequest(BaseModel):
    blocks: list[str]

class BlockResponse(BaseModel):
    blocks: list[str]

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
    


    @router.post("/strToBinary", response_model=BinaryResponse)
    def run(binary_request: BinaryRequest):
        binary = conversions.str_to_binary(binary_request.data)
        response = {
            "data": binary_request.data,
            "binary": binary
        }
        return response
    
    @router.post("/hexToBinary", response_model=BinaryResponse)
    def run(hex_request: HexRequest):
        binary = conversions.hex_to_binary(hex_request.data)
        response = {
            "data": hex_request.data,
            "binary": binary
        }
        return response
    
    @router.post("/strToBoth", response_model=BothResponse)
    def run(both_request: BothRequest):
        binary = conversions.str_to_binary(both_request.data)
        response = {
            "binary": binary,
            "hex": binascii.hexlify(bytes(both_request.data, encoding="utf8"))
        } 
        return response
    
    @router.post("/binaryToHexBlocks", response_model=BlockResponse)
    def run(block_request: BlockRequest):
        hex_blocks = []
        for block in block_request.blocks:
            hex_blocks.append(conversions.binary_to_hex(block))
        return {
            "blocks": hex_blocks
        }
    
    @router.post("/hexToBinaryBlocks", response_model=BlockResponse)
    def run(block_request: BlockRequest):
        binary_blocks = []
        for block in block_request.blocks:
            binary_blocks.append(conversions.hex_to_binary(block))
        return {
            "blocks": binary_blocks
        }