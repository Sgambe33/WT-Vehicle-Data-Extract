import hashlib

from pydantic import BaseModel
from typing import Optional


class Ammo(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    caliber: float = 0.0
    mass: float = 0.0
    speed: float = 0.0
    max_distance: float = 0.0
    explosive_type: Optional[str] = None
    explosive_mass: float = 0.0

    def __str__(self):
        return f"Ammo: {self.name} {self.type} {self.caliber}mm, {self.mass}kg, {self.speed}m/s, {self.max_distance}m, {self.explosive_type} {self.explosive_mass}kg"

    def toJson(self):
        return self.model_dump_json()

    def __eq__(self, other):
        if isinstance(other, Ammo):
            return self.name == other.name
        return False

    def __hash__(self):
        return int(hashlib.sha256(self.model_dump_json().encode("utf-8")).hexdigest(), 16) % 10 ** 8
