from pydantic import BaseModel
from typing import Optional


class Modification(BaseModel):
    name: Optional[str] = None
    tier: int = 0
    repair_coeff: float = 0.0
    value: int = 0
    req_exp: int = 0
    ge_cost: int = 0
    required_modification: Optional[str] = None
    mod_class: Optional[str] = None
    icon: Optional[str] = None

    __hash__ = object.__hash__

    def __str__(self):
        return (f"Modification: {self.name}, {self.tier}, {self.repair_coeff}, {self.value}, "
                f"{self.req_exp}, {self.ge_cost}, {self.required_modification}")

    def toJson(self):
        return self.model_dump_json()
