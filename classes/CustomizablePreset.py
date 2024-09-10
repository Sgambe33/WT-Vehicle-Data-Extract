from classes import Pylon


class CustomizablePreset:
    def __init__(self):
        self.max_load: int = 0
        self.max_load_left_wing: int = 0
        self.max_load_right_wing: int = 0
        self.max_disbalance: int = 0
        self.pylons: list[Pylon] = []

    def __str__(self):
        return f"Custom preset: {self.max_load}, {self.max_load_left_wing}, {self.max_load_right_wing}, {self.max_disbalance}, {self.pylons}"

    def toJson(self):
        return {
            "max_load": self.max_load,
            "max_load_left_wing": self.max_load_left_wing,
            "max_load_right_wing": self.max_load_right_wing,
            "max_disbalance": self.max_disbalance,
            "pylons": [pylon.toJson() for pylon in self.pylons]
        }
