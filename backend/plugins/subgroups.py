import operator
import backend.util_internal.group_theory as gt
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

class SubGroupRequest(BaseModel):
    elements: list[int]
    operation: str
    mod: int

class SubGroupResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    is_group: bool
    why_not_group: list
    subgroups: list[dict]

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
            return subgroups
        
        subgroups["is_group"] = True
        for subgroup in group.find_subgroups():
            table = subgroup.generate_multiplication_table()
            subgroups["subgroups"].append(
                {
                    subgroup.get_order(): table
                }
            )
        return subgroups