from classes import Ammo


class Weapon:
    def __init__(self):
        self.name: str | None = None
        self.weapon_type: str | None = None
        self.count: int = 1
        self.ammos: list[Ammo] = []

    def __str__(self):
        return f"Weapon: {self.name}, {self.weapon_type}, {self.count}," + "\n" + "\n".join([f"\t{str(i)}" for i in self.ammos])

    def toJson(self):
        return {
            "name": self.name,
            "weapon_type": self.weapon_type,
            "count": self.count,
            "ammos": [i.toJson() for i in self.ammos]
        }
