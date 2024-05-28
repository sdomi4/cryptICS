###########################################
#   Example for a new plugin with needed  #
#   class / methods for plugin discovery  #
###########################################

# To export API endpoints
from fastapi import APIRouter, HTTPException
from Crypto.Random import random

from backend.util_internal.ecc_inspector import random_curve, random_cyclic_curve, ECCInvestigator
from backend.util_internal.ecc_exercise import generate_practice_points, check_nonsingularity, check_point_on_curve, inverse_point, hasse_theorem
from sympy import isprime

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
    not_elliptic: str

class ExerciseResponse(BaseModel):
    a: int
    b: int
    p: int
    practice_points: tuple
    m: tuple
    k: tuple
    q: tuple
    inverse_table: list
    nonsingularity: int
    check_point: tuple
    point_P: tuple
    point_T: tuple
    point_U: tuple
    hasse_bounds: tuple
    estimation_number: int

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
        a, b, p, order = random_curve()

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
        order = 0
        all_points = []
        positive_points = []
        primitive_points = []
        calculation_info = {}
        is_elliptic = False

        if isprime(inspect_request.p):
            ecc = ECCInvestigator(inspect_request.a, inspect_request.b, inspect_request.p)
            is_elliptic = ecc.is_curve_elliptic()
            if is_elliptic:
                order = ecc.get_order()
                all_points = ecc.get_all_points_on_ec()
                positive_points = ecc.get_positive_points_on_elliptic_curve()
                primitives = ecc.get_primitive_points_on_elliptic_curve()
                primitive_points = primitives[0]
                calculation_info = primitives[1]
                not_elliptic = "it is, trust"
            else:
                not_elliptic = "singular"
        else:
            not_elliptic = "nonprime"
        return {
            "is_elliptic": is_elliptic,
            "all_points": all_points,
            "positive_points": positive_points,
            "primitive_points": primitive_points,
            "order": order,
            "calculation_info": calculation_info,
            "not_elliptic": not_elliptic
        }
    
    @router.get("/ecc/practice", response_model=ExerciseResponse)
    def run():
        # some randomly generated curves / questions will run into modular inverses that don't exist
        # I could try understanding the math and fixing it, but this way is more my style
        sanitycounter = 0
        while sanitycounter < 1000:
            sanitycounter += 1
            try:
                a, b, p, order = random_curve()
                ecc = ECCInvestigator(a, b, p)
                point_to_check = random.choice(ecc.get_positive_points_on_elliptic_curve())
                point_to_inverse = random.choice(ecc.get_positive_points_on_elliptic_curve())
                practice_points = generate_practice_points(a, b, p)
                nonsingularity = check_nonsingularity(a, b, p)
                check_point = check_point_on_curve(point_to_check[0], point_to_check[1], a, b, p)
                inversed_point = inverse_point(point_to_inverse[0], point_to_inverse[1], p)
                hasse_bounds = hasse_theorem(p)
                hasse_bounds = (int(hasse_bounds[0]), int(hasse_bounds[1]))

            except ZeroDivisionError:
                continue

            return {
                "a": a,
                "b": b,
                "p": p,
                "practice_points": practice_points["practice_points"],
                "m": practice_points["m"],
                "k": practice_points["k"],
                "q": practice_points["q"],
                "inverse_table": practice_points["inverse_table"],
                "nonsingularity": nonsingularity,
                "check_point": check_point,
                "point_P": point_to_check,
                "point_T": point_to_inverse,
                "point_U": inversed_point,
                "estimation_number": random.randint(int(hasse_bounds[0]), int(hasse_bounds[1])),
                "hasse_bounds": hasse_bounds
            }
        raise HTTPException(status_code=500, detail="Spent 1000 tries generating a valid exercise, giving up, just refresh")