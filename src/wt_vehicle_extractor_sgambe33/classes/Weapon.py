from pydantic import BaseModel, Field
from typing import Optional, Set
from src.wt_vehicle_extractor_sgambe33.classes.Ammo import Ammo


class Weapon(BaseModel):
    name: Optional[str] = None
    weapon_type: Optional[str] = None
    count: int = 1
    icon: Optional[str] = None
    ammos: Set[Ammo] = Field(default_factory=set)

    __hash__ = object.__hash__

    def __str__(self):
        return (f"Weapon: {self.name}, {self.weapon_type}, {self.count}, " +
                "\n" + "\n".join([f"\t{str(i)}" for i in self.ammos]))

    def toJson(self):
        return self.model_dump_json()
