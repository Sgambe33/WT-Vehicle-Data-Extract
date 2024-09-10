from classes import Engine, NightVisionDevice, Weapon, Preset, Modification, Aerodynamics
from classes.BallisticComputer import BallisticComputer
from classes.CustomizablePreset import CustomizablePreset


class Vehicle:
    def __init__(self):
        self.country: str = None
        self.identifier: str = None
        self.vehicle_type: str = None
        self.vehicle_sub_types: list[str] = []
        self.event: str = None
        self.release_date: str = None
        self.version: str = None
        self.era: int = 0
        self.arcade_br: float = 1.0
        self.realistic_br: float = 1.0
        self.realistic_ground_br: float = 1.0
        self.simulator_br: float = 1.0
        self.simulator_ground_br: float = 1.0
        self.value: int = 0
        self.req_exp: int = 0
        self.is_premium: bool = False
        self.is_pack: bool = False
        self.on_marketplace: bool = False
        self.squadron_vehicle: bool = False
        self.ge_cost: int = 0
        self.crew_total_count: int = 0
        self.visibility: int  = 0
        self.hull_armor: list[int] = []
        self.turret_armor: list[int] = []
        self.mass: int = 0.0
        self.train1_cost: int = 0
        self.train2_cost: int = 0
        self.train3_cost_gold: int = 0
        self.train3_cost_exp: int = 0
        self.sl_mul_arcade: float = 0.0
        self.sl_mul_realistic: float = 0.0  
        self.sl_mul_simulator: float
        self.exp_mul: float = 0.0
        self.repair_time_arcade: float = 0.0
        self.repair_time_realistic: float = 0.0
        self.repair_time_simulator: float = 0.0
        self.repair_time_no_crew_arcade: float = 0.0
        self.repair_time_no_crew_realistic: float = 0.0
        self.repair_time_no_crew_simulator: float = 0.0
        self.repair_cost_arcade: int = 0
        self.repair_cost_realistic: int = 0
        self.repair_cost_simulator: int = 0
        self.repair_cost_per_min_arcade: int = 0
        self.repair_cost_per_min_realistic: int = 0
        self.repair_cost_per_min_simulator: int = 0
        self.repair_cost_full_upgraded_arcade: int = 0
        self.repair_cost_full_upgraded_realistic: int = 0
        self.repair_cost_full_upgraded_simulator: int = 0
        self.required_vehicle: str = None
        self.engine: Engine = None
        self.modifications: list[Modification] = []
        self.ir_devices: NightVisionDevice = None
        self.thermal_devices: NightVisionDevice = None
        self.ballistic_computer: BallisticComputer = None
        self.aerodynamics: Aerodynamics = None
        self.weapons: list[Weapon] = []
        self.has_customizable_weapons: bool = False
        self.presets: list[Preset] = []
        self.customizable_presets: CustomizablePreset = None

    def toJson(self):
        return {
            "country": self.country,
            "identifier": self.identifier,
            "vehicle_type": self.vehicle_type,
            "vehicle_sub_types": self.vehicle_sub_types,
            "event": self.event,
            "release_date": self.release_date,
            "version": self.version,
            "era": self.era,
            "arcade_br": self.arcade_br,
            "realistic_br": self.realistic_br,
            "realistic_ground_br": self.realistic_ground_br,
            "simulator_br": self.simulator_br,
            "simulator_ground_br": self.simulator_ground_br,
            "value": self.value,
            "req_exp": self.req_exp,
            "is_premium": self.is_premium,
            "is_pack": self.is_pack,
            "on_marketplace": self.on_marketplace,
            "squadron_vehicle": self.squadron_vehicle,
            "ge_cost": self.ge_cost,
            "crew_total_count": self.crew_total_count,
            "visibility": self.visibility,
            "hull_armor": self.hull_armor,
            "turret_armor": self.turret_armor,
            "mass": self.mass,
            "train1_cost": self.train1_cost,
            "train2_cost": self.train2_cost,
            "train3_cost_gold": self.train3_cost_gold,
            "train3_cost_exp": self.train3_cost_exp,
            "sl_mul_arcade": self.sl_mul_arcade,
            "sl_mul_realistic": self.sl_mul_realistic,
            "sl_mul_simulator": self.sl_mul_simulator,
            "exp_mul": self.exp_mul,
            "repair_time_arcade": self.repair_time_arcade,
            "repair_time_realistic": self.repair_time_realistic,
            "repair_time_simulator": self.repair_time_simulator,
            "repair_time_no_crew_arcade": self.repair_time_no_crew_arcade,
            "repair_time_no_crew_realistic": self.repair_time_no_crew_realistic,
            "repair_time_no_crew_simulator": self.repair_time_no_crew_simulator,
            "repair_cost_arcade": self.repair_cost_arcade,
            "repair_cost_realistic": self.repair_cost_realistic,
            "repair_cost_simulator": self.repair_cost_simulator,
            "repair_cost_per_min_arcade": self.repair_cost_per_min_arcade,
            "repair_cost_per_min_realistic": self.repair_cost_per_min_realistic,
            "repair_cost_per_min_simulator": self.repair_cost_per_min_simulator,
            "repair_cost_full_upgraded_arcade": self.repair_cost_full_upgraded_arcade,
            "repair_cost_full_upgraded_realistic": self.repair_cost_full_upgraded_realistic,
            "repair_cost_full_upgraded_simulator": self.repair_cost_full_upgraded_simulator,
            "required_vehicle": self.required_vehicle,
            "engine": self.engine.toJson(),
            "modifications": [] if self.modifications is None else [i.toJson() for i in self.modifications],
            "ir_devices": self.ir_devices.toJson() if self.ir_devices is not None else {},
            "thermal_devices": self.thermal_devices.toJson() if self.thermal_devices is not None else {},
            "ballistic_computer": self.ballistic_computer.toJson() if self.ballistic_computer is not None else {},
            "aerodynamics": self.aerodynamics.toJson() if self.aerodynamics is not None else {},
            "has_customizable_weapons": self.has_customizable_weapons,
            "weapons": [] if self.weapons is None else [i.toJson() for i in self.weapons],
            "presets": [] if self.presets is None else [i.toJson() for i in self.presets],
            "customizable_presets": [] if self.customizable_presets is None else self.customizable_presets.toJson()
        }
