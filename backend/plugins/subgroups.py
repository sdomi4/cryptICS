import operator
import backend.util_internal.group_theory as gt
from backend.util_internal.euler_phi import euler_phi
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

class SubGroupRequest(BaseModel):
    elements: list[int]
    operation: str
    mod: int

class SubGroupResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    elements: list[int]
    operation: str
    mod: int
    is_group: bool
    why_not_group: list
    subgroups: list[dict]
    table: dict
    exponenttable: dict
    roworders: dict
    possibleprimitives: int
    possiblesubgroups: list[int]

class Plugin():
    name = "plugins.subgroups"
    dependencies = None
    endpoints = [
        {
            "uri": "/plugins/subgroups",
            "tag": "homepage",
            "description": "Group Theory"
        },
        {
            "uri": "/plugins/subgroups/learn",
            "tag": "navbar",
            "description": "Learn"
        },
        {
            "uri": "/plugins/subgroups/practice",
            "tag": "navbar",
            "description": "Practice"
        },
        {
            "uri": "/plugins/subgroups/calculate",
            "tag": "navbar",
            "description": "Calculate"
        }
    ]

    router = APIRouter(
        prefix="/plugins/groups"
    )

    def register(self):
        print("Registering Subgroup API endpoints...")
        return self.router
    
    @router.post("/subgroups", response_model=SubGroupResponse)
    def run(group_request: SubGroupRequest):
        ops = {
            "add": operator.add,
            "sub": operator.sub,
            "mul": operator.mul,
            "div": operator.floordiv,
            "exp": operator.pow
        } 
        group = gt.Group(set(group_request.elements), ops[group_request.operation], group_request.mod)
        subgroups = {
            "is_group": False,
            "why_not_group": [],
            "subgroups": []
        }
        if not group.is_group():
            subgroups["why_not_group"] = group.why_not_group
            subgroups["elements"] = group_request.elements
            subgroups["operation"] = group_request.operation
            subgroups["mod"] = group_request.mod
            subgroups["table"] = {}
            subgroups["exponenttable"] = {}
            subgroups["roworders"] = {}
            subgroups["possibleprimitives"] = 0
            subgroups["possiblesubgroups"] = []
            return subgroups
        
        subgroups["is_group"] = True
        for subgroup in group.find_subgroups():
            table = subgroup.generate_multiplication_table()
            subgroups["subgroups"].append(
                {
                    subgroup.get_order(): table
                }
            )
        subgroups["elements"] = group_request.elements
        subgroups["operation"] = group_request.operation
        subgroups["mod"] = group_request.mod
        subgroups["table"] = group.generate_multiplication_table()
        subgroups["exponenttable"] = group.generate_exponential_table()
        subgroups["roworders"] = group.get_row_orders(subgroups["exponenttable"])
        subgroups["possibleprimitives"] = euler_phi(group.get_order())
        subgroups["possiblesubgroups"] = group.get_possible_subgroups()
        return subgroups