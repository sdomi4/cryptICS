from fastapi import APIRouter
from pydantic import BaseModel
from Crypto.Util.Padding import pad, unpad

class PaddingRequest(BaseModel):
    blocks: list[bytes]
    blocksize: int
    # available modes: "pkcs7", "iso7816", "x923", "none"
    mode: str

class PaddingResponse(BaseModel):
    blocks: list[bytes]

class BlockSplitRequest(BaseModel):
    data: bytes
    blocksize: int

class BlockSplitResponse(BaseModel):
    blocks: list[bytes]

class Plugin():
    name = "plugins.padding"
    dependencies = ["plugins.data_conversion"]
    endpoints = {
        "pad" : {
            "uri": "/plugins/pad",
            "tags": ["block_ciphers", "utility", "padding"]
        },
        "unpad": {
            "uri": "/plugins/unpad",
            "tags": ["block_ciphers", "utility", "padding"]
        },
        "split": {
            "uri": "/plugins/split",
            "tags": ["block_ciphers", "utility", "padding"]
        }
    }

    router = APIRouter(
        prefix="/plugins"
    )

    def register(self):
        print("Registering padding API endpoints...")
        return self.router
    
    @router.post("/split", response_model=BlockSplitResponse)
    def split_blocks(block_request: BlockSplitRequest):
        data = block_request.data
        blocks = [data[i:i+block_request.blocksize] for i in range(0, len(data), block_request.blocksize)]
        return {"blocks": blocks}
    
    @router.post("/pad", response_model=PaddingResponse)
    def pad(padding_request: PaddingRequest):
        blocks = padding_request.blocks
        if padding_request.mode == "none":
            return blocks
        blocks[-1] = pad(blocks[-1], padding_request.blocksize, padding_request.mode)
        return {"blocks": blocks}
    
    @router.post("/unpad", response_model=PaddingResponse)
    def unpad(padding_request: PaddingRequest):
        blocks = padding_request.blocks
        if padding_request.mode == "none":
            return blocks
        blocks[-1] = unpad(blocks[-1], padding_request.blocksize, padding_request.mode)
        return {"blocks": blocks}