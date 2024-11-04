from pydantic import BaseModel, Field
from typing import List, Optional, Set

from src.wt_vehicle_extractor_sgambe33.classes.Aerodynamics import Aerodynamics
from src.wt_vehicle_extractor_sgambe33.classes.Engine import Engine
from src.wt_vehicle_extractor_sgambe33.classes.Modification import Modification
from src.wt_vehicle_extractor_sgambe33.classes.NightVisionDevice import NightVisionDevice
from src.wt_vehicle_extractor_sgambe33.classes.Preset import Preset
from src.wt_vehicle_extractor_sgambe33.classes.Weapon import Weapon


from src.wt_vehicle_extractor_sgambe33.classes.BallisticComputer import BallisticComputer
from src.wt_vehicle_extractor_sgambe33.classes.CustomizablePreset import CustomizablePreset


class Vehicle(BaseModel):
    country: Optional[str] = None
    identifier: Optional[str] = None
    vehicle_type: Optional[str] = None
    vehicle_sub_types: List[str] = Field(default_factory=list)
    event: Optional[str] = None
    release_date: Optional[str] = None
    version: Optional[str] = None
    era: int = 0
    arcade_br: float = 1.0
    realistic_br: float = 1.0
    realistic_ground_br: float = 1.0
    simulator_br: float = 1.0
    simulator_ground_br: float = 1.0
    value: int = 0
    req_exp: int = 0
    is_premium: bool = False
    is_pack: bool = False
    on_marketplace: bool = False
    squadron_vehicle: bool = False
    ge_cost: int = 0
    crew_total_count: int = 0
    visibility: int = 0
    hull_armor: List[int] = Field(default_factory=list)
    turret_armor: List[int] = Field(default_factory=list)
    mass: float = 0.0
    train1_cost: int = 0
    train2_cost: int = 0
    train3_cost_gold: int = 0
    train3_cost_exp: int = 0
    sl_mul_arcade: float = 0.0
    sl_mul_realistic: float = 0.0
    sl_mul_simulator: float = 0.0
    exp_mul: float = 0.0
    repair_time_arcade: float = 0.0
    repair_time_realistic: float = 0.0
    repair_time_simulator: float = 0.0
    repair_time_no_crew_arcade: float = 0.0
    repair_time_no_crew_realistic: float = 0.0
    repair_time_no_crew_simulator: float = 0.0
    repair_cost_arcade: int = 0
    repair_cost_realistic: int = 0
    repair_cost_simulator: int = 0
    repair_cost_per_min_arcade: int = 0
    repair_cost_per_min_realistic: int = 0
    repair_cost_per_min_simulator: int = 0
    repair_cost_full_upgraded_arcade: int = 0
    repair_cost_full_upgraded_realistic: int = 0
    repair_cost_full_upgraded_simulator: int = 0
    required_vehicle: Optional[str] = None
    engine: Optional[Engine] = None
    modifications: Set[Modification] = Field(default_factory=set)
    ir_devices: Optional[NightVisionDevice] = None
    thermal_devices: Optional[NightVisionDevice] = None
    ballistic_computer: Optional[BallisticComputer] = None
    aerodynamics: Optional[Aerodynamics] = None
    has_customizable_weapons: bool = False
    weapons: Set[Weapon] = Field(default_factory=set)
    presets: List[Preset] = Field(default_factory=list)
    customizable_presets: Optional[CustomizablePreset] = None

    def toJson(self):
        return self.model_dump(mode='json')
