from classes import Weapon


class Pylon:
    def __init__(self):
        self.index: int = 1
        self.used_for_disbalance: bool = True
        self.selectable_weapons: list[Weapon] = []

    def __str__(self):
        return f"Pylon: {self.index}, {self.used_for_disbalance}, {self.selectable_weapons}"

    def toJson(self):
        return {
            "index": self.index,
            "used_for_disbalance": self.used_for_disbalance,
            "selectable_weapons": [weapon.toJson() for weapon in self.selectable_weapons]
        }
