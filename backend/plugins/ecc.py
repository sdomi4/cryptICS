###########################################
#   Example for a new plugin with needed  #
#   class / methods for plugin discovery  #
###########################################

# To export API endpoints
from fastapi import APIRouter, HTTPException

from backend.util_internal.ecc_inspector import random_curve, random_cyclic_curve, ECCInvestigator

from pydantic import BaseModel

class CurveResponse(BaseModel):
    a: int
    b: int
    p: int

class InspectRequest(BaseModel):
    a: int
    b: int
    p: int

class InspectResponse(BaseModel):
    is_elliptic: bool
    all_points: list
    positive_points: list
    primitive_points: list
    order: int
    calculation_info: dict

# All logic should be contained in the Plugin class, for plugin discovery/import
class Plugin():

    # Plugin metadata
    name = "plugins.ecc"

    dependencies = []

    endpoints = [
        {
            "uri": "/plugins/ecc",
            "tag": "homepage",
            "description": {
                "de": "ECC",
                "en": "ECC"
            }
        }
    ]

    # Instantiate router instance, all plugins are prefixed with at least /plugins
    router = APIRouter(
        prefix="/plugins"
    )

    def register(self):
        # return None
        return self.router
    
    # get random elliptic curve for exercise
    @router.get("/ecc/random", response_model=CurveResponse)
    def run():
        a, b, p = random_curve()

        if a is None:
            raise HTTPException(status_code=500, detail="Could not generate random curve")
        print(a, b, p)
        return {
            "a": a,
            "b": b,
            "p": p
        }
    
    @router.get("/ecc/cyclic", response_model=CurveResponse)
    def run():
        a, b, p = random_cyclic_curve()

        if a is None:
            raise HTTPException(status_code=500, detail="Could not generate random cyclic curve")
        
        return {
            "a": a,
            "b": b,
            "p": p
        }
    
    # ECC_Untersucher but with proper maths i guess
    @router.post("/ecc/inspect", response_model=InspectResponse)
    def run(inspect_request: InspectRequest):
        ecc = ECCInvestigator(inspect_request.a, inspect_request.b, inspect_request.p)
        is_elliptic = ecc.is_curve_elliptic()
        if is_elliptic:
            order = ecc.get_order()
            all_points = ecc.get_all_points_on_ec()
            positive_points = ecc.get_positive_points_on_elliptic_curve()
            primitives = ecc.get_primitive_points_on_elliptic_curve()
            primitive_points = primitives[0]
            calculation_info = primitives[1]
        else:
            order = None
            all_points = []
            positive_points = []
            primitive_points = []
            calculation_info = {}

        return {
            "is_elliptic": is_elliptic,
            "all_points": all_points,
            "positive_points": positive_points,
            "primitive_points": primitive_points,
            "order": order,
            "calculation_info": calculation_info
        }