class Modification:
    def __init__(self):
        self.name: str = None
        self.tier: int = 0
        self.repair_coeff: float = 0.0
        self.value: int = 0
        self.req_exp: int = 0
        self.ge_cost: int = 0
        self.required_modification: str = None
        self.mod_class: str = None
        self.icon: str = None

    def __str__(self):
        return f"Modification: {self.name}, {self.tier}, {self.repair_coeff}, {self.value}, {self.req_exp}, {self.ge_cost}, {self.required_modification}"

    def toJson(self):
        return {
            "name": self.name,
            "tier": self.tier,
            "repair_coeff": self.repair_coeff,
            "value": self.value,
            "req_exp": self.req_exp,
            "ge_cost": self.ge_cost,
            "required_modification": self.required_modification,
            "mod_class": self.mod_class,
            "icon": self.icon
        }
