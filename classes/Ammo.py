import hashlib
import json


class Ammo:
    def __init__(self):
        self.name: str | None = None
        self.type: str | None = None
        self.caliber: float = 0.0
        self.mass: float = 0.0
        self.speed: float = 0.0
        self.max_distance: float = 0.0
        self.explosive_type: str | None = None
        self.explosive_mass: float = 0.0

    def __str__(self):
        return f"Ammo: {self.name} {self.type} {self.caliber}mm, {self.mass}kg, {self.speed}m/s, {self.max_distance}m, {self.explosive_type} {self.explosive_mass}kg"

    def toJson(self):
        return {
            "name": self.name,
            "type": self.type,
            "caliber": self.caliber,
            "mass": self.mass,
            "speed": self.speed,
            "max_distance": self.max_distance,
            "explosive_type": self.explosive_type,
            "explosive_mass": self.explosive_mass
        }

    def __eq__(self, other):
        if isinstance(other, Ammo):
            return self.name == other.name
        return False

    def __hash__(self):
        return int(hashlib.sha256(json.dumps(self.toJson()).encode("utf-8")).hexdigest(), 16) % 10 ** 8
