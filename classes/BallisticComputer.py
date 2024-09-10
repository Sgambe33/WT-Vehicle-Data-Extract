class BallisticComputer:
    def __init__(self):
        self.has_gun_ccip:bool=False
        self.has_turret_ccip:bool=False
        self.has_bombs_ccip:bool=False
        self.has_rocket_ccip:bool=False
        
        self.has_gun_ccrp:bool=False
        self.has_turret_ccrp:bool=False
        self.has_bombs_ccrp:bool=False
        self.has_rocket_ccrp:bool=False
        
    def __str__(self) -> str:
        return f"gun_ccip: {self.has_gun_ccip}, turret_ccip: {self.has_turret_ccip}, bombs_ccip: {self.has_bombs_ccip}, rocket_ccip: {self.has_rocket_ccip}, gun_ccrp: {self.has_gun_ccrp}, turret_ccrp: {self.has_turret_ccrp}, bombs_ccrp: {self.has_bombs_ccrp}, rocket_ccrp: {self.has_rocket_ccrp}"
    
    def is_all_false(self) -> bool:
        return not any([self.has_gun_ccip, self.has_turret_ccip, self.has_bombs_ccip, self.has_rocket_ccip, self.has_gun_ccrp, self.has_turret_ccrp, self.has_bombs_ccrp, self.has_rocket_ccrp])

    def toJson(self):
        return {
            "gun_ccip": self.has_gun_ccip,
            "turret_ccip": self.has_turret_ccip,
            "bombs_ccip": self.has_bombs_ccip,
            "rocket_ccip": self.has_rocket_ccip,
            "gun_ccrp": self.has_gun_ccrp,
            "turret_ccrp": self.has_turret_ccrp,
            "bombs_ccrp": self.has_bombs_ccrp,
            "rocket_ccrp": self.has_rocket_ccrp,
        }