import difflib
from fastapi import APIRouter
from pydantic import BaseModel

class DiffResponse(BaseModel):
    differences: list

class DiffRequest(BaseModel):
    input1: str
    input2: str

class Plugin():
    name = "plugins.diff"
    dependencies = None
    endpoints = []

    router = APIRouter(
        prefix="/plugins"
    )

    def register(self):
        print("Registering Diff API endpoint")
        return self.router

    @router.post("/diff", response_model=DiffResponse)    
    def run(diff_request: DiffRequest) -> list:
        diff =  list(difflib.ndiff(diff_request.input1, diff_request.input2))
        return {"differences": diff}