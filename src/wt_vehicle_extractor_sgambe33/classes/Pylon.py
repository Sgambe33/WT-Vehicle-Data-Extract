from pydantic import BaseModel, Field
from typing import List, Set
from src.wt_vehicle_extractor_sgambe33.classes.Weapon import Weapon


class Pylon(BaseModel):
    index: int = 1
    used_for_disbalance: bool = True
    selectable_weapons: Set[Weapon] = Field(default_factory=set)

    def __str__(self):
        return f"Pylon: {self.index}, {self.used_for_disbalance}, {self.selectable_weapons}"

    def toJson(self):
        return self.model_dump_json()
