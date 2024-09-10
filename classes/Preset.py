from classes import Weapon


class Preset:
    def __init__(self):
        self.name: str = None
        self.weapons: list[Weapon] = []

    def __str__(self):
        return f"Preset: {self.name}, {self.weapons}"

    def toJson(self):
        return {
            "name": self.name,
            "weapons": [weapon.toJson() for weapon in self.weapons]
        }
