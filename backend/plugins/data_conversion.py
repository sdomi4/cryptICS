###########################################
#   Example for a new plugin with needed  #
#   class / methods for plugin discovery  #
###########################################
from util_internal.conversions import bytearray_to_blocks
# To export API endpoints
from fastapi import APIRouter
from pydantic import BaseModel

class BlockRequest(BaseModel):
    data: str
    encoding: str
    block_size: int

class BlockResponse(BaseModel):
    data: list[bytes]

class BinaryRequest(BaseModel):
    data: list[bytes]

class BinaryResponse(BaseModel):
    binary: str

class BinaryBlockRequest(BaseModel):
    data: list[bytes]

class BinaryBlockResponse(BaseModel):
    data: list[str]

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
    
    def _bytearray_to_blocks(data: bytearray, block_size: int) -> list:
        return [data[i:i+block_size] for i in range(0, len(data), block_size)]
    
    # @router.post("/binaryString", response_model=BinaryResponse)
    # def get_binary_string(binary_request: BinaryRequest):
    #     binary_string = ' '.join(f'{byte:08b}' for byte in binary_request.data)
    #     return binary_string
    
    # @router.post("/blocksToBinary", response_description=BinaryBlockResponse)
    # def blocks_to_binary(binary_block_request: BinaryBlockRequest):
    #     binary_blocks = []
    #     return binary_blocks
    
    # @router.post("/toBlocks", response_model=BlockResponse)
    # def string_to_blocks(block_request: BlockRequest):
    #     data = bytes(block_request.data, block_request.encoding)
    #     blocks = bytearray_to_blocks(data, block_request.block_size)
    #     for block in blocks:
    #         print(block.hex())
    #     return {"data": blocks}