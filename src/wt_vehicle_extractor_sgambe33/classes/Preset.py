from pydantic import BaseModel, Field
from typing import List, Optional, Set
from src.wt_vehicle_extractor_sgambe33.classes.Weapon import Weapon


class Preset(BaseModel):
    name: Optional[str] = None
    weapons: Set[Weapon] = Field(default_factory=set)

    def __str__(self):
        return f"Preset: {self.name}, {self.weapons}"

    def toJson(self):
        return self.model_dump_json()
