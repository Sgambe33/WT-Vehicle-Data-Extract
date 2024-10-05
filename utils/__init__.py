import copy
import re
from math import floor
from numbers import Number

from classes.Aerodynamics import Aerodynamics
from classes.Ammo import Ammo
from classes.BallisticComputer import BallisticComputer
from classes.CustomizablePreset import CustomizablePreset
from classes.Engine import Engine
from classes.Modification import Modification
from classes.NightVisionDevice import NightVisionDevice
from classes.Preset import Preset
from classes.Pylon import Pylon
from classes.Vehicle import Vehicle
from classes.Weapon import Weapon
from utils.constants import *
from utils.custom_logging import *
from utils.simple_functions import *
from utils.update_localization import ALL_WEAPONS, ALL_AMMOS, ALL_EXPLOSIVES, ALL_AMMO_TYPES


def get_vehicle_fetch_url(vehicle_name: str, unit_type_uri="/units/tankmodels"):
    """Get epi endpoint of a specific vehicle

    Args:
        vehicle_name (str): Name of vehicle
        unit_type_uri (str, optional): URI of the vehicle"s type. Defaults to "tankmodels".

    Returns:
        str: api endpoint
    """
    return f"{URL_VROMFS}gamedata{unit_type_uri}/{vehicle_name.lower()}.blkx"


def get_guns_url(gun_path: str):
    """Get epi endpoint of a specific gun

    Args:
        gun_path (str): gun"s path found in Vehicle Data
    Returns:
        str: api endpoint
    """
    return f"{URL_VROMFS}{gun_path.lower()}x"


def create_vehicle(v_name: str, v_fetch_path: str) -> Vehicle | None:
    """Create an Vehicle Object

    Args:
        v_name (str): Vehicle"s name
        v_fetch_path (str): Vehicle"s endpoint
    Returns:
        dict: Vehicle Object
    """
    details: dict = myFetch(get_vehicle_fetch_url(v_name, v_fetch_path), True)

    data: Vehicle = create_vehicle_data(v_name, details, v_fetch_path, None)
    if data is None:
        return None

    data.has_customizable_weapons = True if "WeaponSlots" in details.keys() else False
    data.weapons = create_weapons(v_name, details, data.has_customizable_weapons)
    data.presets = create_presets(details, data.has_customizable_weapons, len(data.weapons) > 0)
    data.customizable_presets = create_customizable_presets(details, len(data.weapons) > 0) if data.has_customizable_weapons else None
    return data


def create_vehicle_data(v_name: str, v_details: dict, v_fetch_path, vehicle_type: str | None) -> Vehicle | None:
    """Create all vehicle"s data

    Args:
        v_name (str): vehicle"s name
        v_details (dict): vehicle"s fetched details
        v_fetch_path (_type_): vehicle"s fetch endpoint
        vehicle_type (str | None): #! [UNUSED]

    Returns:
        dict: VehicleData Object
    """
    vehicle_wiki = value_from_dict(v_details, "wiki", value_from_dict(v_details, "Wiki"))
    vehicle_data = value_from_dict(WPCOST, v_name)
    vehicle_tags = value_from_dict(value_from_dict(UNIT_TAGS, v_name), "Shop")
    vehicle_phys = value_from_dict(v_details, "VehiclePhys", value_from_dict(v_details, "ShipPhys"))

    if v_name not in WPCOST or (vehicle_type is not None and value_from_dict(vehicle_data, "unitMoveType") != vehicle_type):
        cLogger.error(
            f'{v_name=} is not in WPCOST {vehicle_type=} WPCOST_TYPE={value_from_dict(vehicle_data, "unitMoveType")}')
        return None

    vehicle: Vehicle = Vehicle()
    country = value_from_dict(vehicle_data, "country")
    country = country.replace("country_", "").lower() if country is not None else country
    vehicle.country = country
    vehicle.identifier = v_name

    tags: dict = value_from_dict(value_from_dict(UNIT_TAGS, v_name), "tags")
    types = [x.replace("type_", "").lower() for x in tags.keys() if (x != "boat" or x != "ship") and x.startswith("type_")]
    for vehicle_type in types:
        if vehicle_type in SEA_TYPES2:
            vehicle.vehicle_type = vehicle_type
            break
        elif vehicle_type in AIR_TYPES2:
            vehicle.vehicle_type = vehicle_type
            break
        elif vehicle_type in GROUND_TYPES2:
            vehicle.vehicle_type = vehicle_type
            break
    types = [t for t in types if t not in [vehicle.vehicle_type]]
    vehicle.vehicle_sub_types = types

    vehicle.event = value_from_dict(vehicle_data, "event", None)
    vehicle.release_date = value_from_dict(value_from_dict(UNIT_TAGS, v_name), "releaseDate", None)
    if vehicle.release_date is not None: vehicle.release_date = vehicle.release_date.replace(" 00:00:00", "")
    vehicle.version = getVersion()

    vehicle.era = value_from_dict(vehicle_data, "rank")
    vehicle.arcade_br = BATTLE_RATINGS[value_from_dict(vehicle_data, "economiceraArcade", value_from_dict(vehicle_data, "economicRankArcade", 1.0))]
    vehicle.realistic_br = BATTLE_RATINGS[value_from_dict(vehicle_data, "economiceraHistorical", value_from_dict(vehicle_data, "economicRankHistorical", 1.0))]
    vehicle.simulator_br = BATTLE_RATINGS[value_from_dict(vehicle_data, "economiceraSimulation", value_from_dict(vehicle_data, "economicRankSimulation", 1.0))]
    economic_rank_tank_historical = value_from_dict(vehicle_data, "economicRankTankHistorical")
    vehicle.realistic_ground_br = BATTLE_RATINGS[economic_rank_tank_historical] if economic_rank_tank_historical is not None else vehicle.realistic_br
    economic_rank_simulation = value_from_dict(vehicle_data, "economiceraSimulation", value_from_dict(vehicle_data, "economicRankSimulation", 1.0))
    vehicle.simulator_ground_br = BATTLE_RATINGS[economic_rank_simulation] if economic_rank_simulation is not None else vehicle.simulator_br

    vehicle.value = value_from_dict(vehicle_data, "value", 0)
    vehicle.req_exp = value_from_dict(vehicle_data, "reqExp", 0)
    vehicle.is_premium = True if value_from_dict(vehicle_data, "costGold") is not None else False

    vehicle.squadron_vehicle = is_squadron_vehicle(SHOP, vehicle.identifier, vehicle.country, vehicle.vehicle_type)
    vehicle.on_marketplace = is_vehicle_on_marketplace(SHOP, vehicle.identifier, vehicle.country, vehicle.vehicle_type)
    vehicle.is_pack = False if (vehicle.on_marketplace or vehicle.squadron_vehicle or not vehicle.is_premium) else is_pack(SHOP, vehicle.identifier, vehicle.country, vehicle.vehicle_type)
    vehicle.ge_cost = value_from_dict(vehicle_data, "costGold", 0)
    vehicle.crew_total_count = value_from_dict(vehicle_data, "crewTotalCount", 0)
    vehicle.hull_armor = get_armor_thickness(v_details, vehicle_tags, "hull")
    vehicle.turret_armor = get_armor_thickness(v_details, vehicle_tags, "turret")

    vehicle_phys_mass = value_from_dict(vehicle_phys, "Mass", value_from_dict(vehicle_phys, "mass"))
    empty_mass = value_from_dict(vehicle_phys_mass, "Empty", 0.0)
    fuel_mass = value_from_dict(vehicle_phys_mass, "Fuel", 0.0)
    vehicle_wiki_general = value_from_dict(vehicle_wiki, "general", value_from_dict(vehicle_wiki, "General"))
    normal_weight = value_from_dict(vehicle_wiki_general, "normalWeight", 0.0)
    vehicle.mass = empty_mass + fuel_mass + normal_weight

    vehicle.train1_cost = value_from_dict(vehicle_data, "trainCost", 0)
    vehicle.train2_cost = value_from_dict(vehicle_data, "train2Cost", 0)
    vehicle.train3_cost_gold = value_from_dict(vehicle_data, "train3Cost_gold", 0)
    vehicle.train3_cost_exp = value_from_dict(vehicle_data, "train3Cost_exp", 0)
    vehicle.sl_mul_arcade = value_from_dict(vehicle_data, "rewardMulArcade", 0.0)
    vehicle.sl_mul_realistic = value_from_dict(vehicle_data, "rewardMulHistorical", 0.0)
    vehicle.sl_mul_simulator = value_from_dict(vehicle_data, "rewardMulSimulation", 0.0)
    vehicle.exp_mul = value_from_dict(vehicle_data, "expMul", 0.0)
    vehicle.repair_time_arcade = value_from_dict(vehicle_data, "repairTimeHrsArcade", 0)
    vehicle.repair_time_realistic = value_from_dict(vehicle_data, "repairTimeHrsHistorical", 0)
    vehicle.repair_time_simulator = value_from_dict(vehicle_data, "repairTimeHrsSimulation", 0)
    vehicle.repair_time_no_crew_arcade = value_from_dict(vehicle_data, "repairTimeHrsNoCrewArcade", 0)
    vehicle.repair_time_no_crew_realistic = value_from_dict(vehicle_data, "repairTimeHrsNoCrewHistorical", 0)
    vehicle.repair_time_no_crew_simulator = value_from_dict(vehicle_data, "repairTimeHrsNoCrewSimulation", 0)
    vehicle.repair_cost_arcade = value_from_dict(vehicle_data, "repairCostArcade", 0)
    vehicle.repair_cost_realistic = value_from_dict(vehicle_data, "repairCostHistorical", 0)
    vehicle.repair_cost_simulator = value_from_dict(vehicle_data, "repairCostSimulation", 0)
    vehicle.repair_cost_per_min_arcade = value_from_dict(vehicle_data, "repairCostPerMinArcade", 0)
    vehicle.repair_cost_per_min_realistic = value_from_dict(vehicle_data, "repairCostPerMinHistorical", 0)
    vehicle.repair_cost_per_min_simulator = value_from_dict(vehicle_data, "repairCostPerMinSimulation", 0)
    vehicle.repair_cost_full_upgraded_arcade = value_from_dict(vehicle_data, "repairCostFullUpgradedArcade", 0)
    vehicle.repair_cost_full_upgraded_realistic = value_from_dict(vehicle_data, "repairCostFullUpgradedHistorical", 0)
    vehicle.repair_cost_full_upgraded_simulator = value_from_dict(vehicle_data, "repairCostFullUpgradedSimulation", 0)
    vehicle.required_vehicle = value_from_dict(vehicle_data, "reqAir", None)

    vehicle.engine = create_vehicle_data_engine(v_fetch_path, vehicle_phys, vehicle_tags)
    vehicle.aerodynamics = create_vehicle_data_aerodynamics(vehicle_wiki, vehicle_tags) if vehicle.vehicle_type in AIR_TYPES else None
    vehicle.modifications = create_vehicle_data_modifications(vehicle_data)
    night_vision_devices = create_vehicle_night_vision(v_details, vehicle.vehicle_type)
    vehicle.ir_devices = night_vision_devices[0]
    vehicle.thermal_devices = night_vision_devices[1]
    vehicle.ballistic_computer = create_vehicle_ballistic_computer(v_details, vehicle.vehicle_type)
    return vehicle


def get_armor_thickness(v_details: dict, vehicle_tags: dict, part: str) -> list[int]:
    """Get vehicle"s armor thickness

    Args:
        v_details (dict): vehicle"s fetched details
        vehicle_tags (_type_): vehicle"s fetched unittags
        part (str): part of the vehicle (hull or turret)

    Returns:
        list[int]: list of armor thicknesses [front, side, back]
    """
    armor = [0, 0, 0]
    # Method 1: look for armor thickness in the vehicle tags
    if part == "hull":
        armor = value_from_dict(vehicle_tags, "armorThicknessHull", [0, 0, 0])
    elif part == "turret":
        armor = value_from_dict(vehicle_tags, "armorThicknessTurret", [0, 0, 0])
    if armor != [0, 0, 0]: return armor

    # Method 2: fallback if method 1 fails
    damage_parts = value_from_dict(v_details, "DamageParts")
    if damage_parts is None: return armor
    damage_part = value_from_dict(damage_parts, part)
    if damage_part is None: return armor
    if part == "hull":
        armor = [
            value_from_dict(value_from_dict(damage_part, "body_front_dm"), "armorThickness", 0),
            value_from_dict(value_from_dict(damage_part, "body_side_dm"), "armorThickness", 0),
            value_from_dict(value_from_dict(damage_part, "body_back_dm"), "armorThickness", 0)
        ]
    elif part == "turret":
        armor = [
            value_from_dict(value_from_dict(damage_part, "turret_front_dm"), "armorThickness", 0),
            value_from_dict(value_from_dict(damage_part, "turret_side_dm"), "armorThickness", 0),
            value_from_dict(value_from_dict(damage_part, "turret_back_dm"), "armorThickness", 0)
        ]
    return armor


def create_vehicle_data_engine(v_fetch_path: str, vehicle_phys: dict, vehicle_tags: dict) -> Engine:
    """Create vehicle"s engine data

    Args:
        vehicle_tags:
        vehicle_phys (dict): vehicle"s fetched physics
        v_fetch_path (str): vehicle"s fetch endpoint
    Returns:
        dict: VehicleEngine Object
    """
    final_engine: Engine = Engine()

    if "ships" in v_fetch_path:
        engine = value_from_dict(vehicle_phys, "engines")
        max_speed = value_from_dict(engine, "maxSpeed", 0)
        max_rev_speed = value_from_dict(engine, "maxRevSpeed", value_from_dict(engine, "maxReverseSpeed", 0))
        final_engine.max_speed_rb_sb = floor(max_speed * 3.6 if type(max_speed) is float else max_speed[0] * 3.6)
        final_engine.max_reverse_speed_rb_sb = floor(max_rev_speed * 3.6 if isinstance(max_rev_speed, Number) else max_rev_speed[0] * 3.6)
        final_engine.max_speed_ab = proper_round(final_engine.max_speed_rb_sb * ENGINE_SPEED_AB_MUL_SHIP)
        final_engine.max_reverse_speed_ab = proper_round(final_engine.max_reverse_speed_rb_sb * ENGINE_SPEED_AB_MUL_SHIP)

    elif "flightmodels" in v_fetch_path:
        final_engine.max_speed_rb_sb = floor(value_from_dict(vehicle_tags, "maxSpeed", 0) * 3.6)
        final_engine.max_speed_ab = proper_round(final_engine.max_speed_rb_sb * ENGINE_SPEED_AB_MUL_AIR)

    elif "tankmodels" in v_fetch_path:
        engine = value_from_dict(vehicle_phys, "engine")
        mechanics = value_from_dict(vehicle_phys, "mechanics", value_from_dict(vehicle_phys, "Mechanics"))
        drive_gear_radius = value_from_dict(mechanics, "driveGearRadius", 0)
        main_gear_ratio = value_from_dict(mechanics, "mainGearRatio", 0)
        side_gear_ratio = value_from_dict(mechanics, "sideGearRatio", 0)
        gears = value_from_dict(value_from_dict(mechanics, "gearRatios"), "ratio")
        final_engine.max_rpm = value_from_dict(engine, "maxRPM", 0)
        final_engine.min_rpm = value_from_dict(engine, "minRPM", 0)
        final_engine.horse_power_rb_sb = int(value_from_dict(engine, "horsePowers", 0))
        final_engine.horse_power_ab = proper_round(final_engine.horse_power_rb_sb * ENGINE_HP_AB_MUL_TANK)

        try:
            final_engine.max_speed_rb_sb = floor(((final_engine.max_rpm * drive_gear_radius) / (main_gear_ratio * side_gear_ratio * gears[-1])) * 0.12 * 3.14)
            final_engine.max_reverse_speed_rb_sb = floor(((final_engine.max_rpm * drive_gear_radius) / (main_gear_ratio * side_gear_ratio * gears[0])) * 0.12 * 3.14)
        except Exception:
            cLogger.error(f"Error while creating engine for {v_fetch_path}")
            final_engine.max_speed_rb_sb = 0
            final_engine.max_reverse_speed_rb_sb = 0

        final_engine.max_speed_ab = int(proper_round(final_engine.max_speed_rb_sb * ENGINE_SPEED_AB_MUL_TANK))
        final_engine.max_reverse_speed_ab = int(proper_round(final_engine.max_reverse_speed_rb_sb * ENGINE_SPEED_AB_MUL_TANK))
    return final_engine


def create_vehicle_data_aerodynamics(vehicle_wiki: dict, vehicle_tags: dict) -> Aerodynamics:
    """Create vehicle"s aerodynamics data (aircrafts only)
    Args:
        vehicle_wiki:
        vehicle_tags:
    Returns:
        dict: Aerodynamics class
    """
    wiki = value_from_dict(vehicle_wiki, "general", value_from_dict(vehicle_wiki, "General"))
    aerodynamics: Aerodynamics = Aerodynamics()
    aerodynamics.length = value_from_dict(wiki, "length", 0)
    aerodynamics.wingspan = value_from_dict(wiki, "wingspan", 0)
    aerodynamics.wing_area = value_from_dict(wiki, "wingArea", 0)
    aerodynamics.empty_weight = value_from_dict(wiki, "emptyWeight", 0)
    aerodynamics.max_takeoff_weight = value_from_dict(wiki, "maxTakeoffWeight", 0)
    aerodynamics.max_altitude = value_from_dict(vehicle_tags, "maxAltitude", 0)
    aerodynamics.turn_time = value_from_dict(vehicle_tags, "turnTime", 0)
    aerodynamics.runway_length_required = value_from_dict(vehicle_tags, "airfieldLen", 0)
    aerodynamics.max_speed_at_altitude = value_from_dict(vehicle_tags, "maxSpeedAlt", 0)

    return aerodynamics


def create_vehicle_data_modifications(vehicle_wpcost: dict) -> set[Modification]:
    modifications: dict = vehicle_wpcost["modifications"]
    final_modifications = set()
    for mod_name in modifications.keys():
        mod = modifications[mod_name]
        if value_from_dict(mod, "tier", 0) == 0:
            continue
        modification: Modification = Modification()
        modification.name = mod_name
        modification.tier = value_from_dict(mod, "tier", 0)
        modification.req_exp = value_from_dict(mod, "reqExp", 0)
        modification.ge_cost = value_from_dict(mod, "costGold", 0) if value_from_dict(mod, "openCostGold") is None else value_from_dict(mod, "openCostGold", 0)
        modification.required_modification = value_from_dict(mod, "reqModification")
        modification.value = value_from_dict(mod, "value", 0)
        modification.repair_coeff = value_from_dict(mod, "repairCostCoef", 0)
        mod_dict = value_from_dict(MODIFICATIONS, modification.name)
        if mod_dict is not None:
            modification.icon = value_from_dict(mod_dict, "image")
            modification.mod_class = value_from_dict(mod_dict, "modClass")
            if modification.icon is not None:
                modification.icon = modification.icon.replace("#ui/gameuiskin#", "modifications/")
                modification.icon += ".png"
        final_modifications.add(modification)
    return final_modifications


def create_vehicle_night_vision(v_details: dict, vehicle_type: str) -> tuple[NightVisionDevice, NightVisionDevice] | tuple[None, None]:
    """Create vehicle"s night vision devices
    
    Args:
        v_details (dict): vehicle"s fetched details
        vehicle_type (str): vehicle"s type
    Returns:
        tuple[NightVisionDevice, NightVisionDevice]: (IR, Thermal) Night Vision Devices
    """

    modifications: dict = value_from_dict(v_details, "modifications")

    night_vision_modification = None
    if vehicle_type in SEA_TYPES2:
        return None, None
    elif vehicle_type in AIR_TYPES2:
        if modifications is None or "heli_night_vision_system" not in modifications.keys():
            return None, None
        night_vision_modification = value_from_dict(modifications, "heli_night_vision_system")
    elif vehicle_type in GROUND_TYPES2:
        if modifications is None or "night_vision_system" not in modifications.keys():
            return None, None
        night_vision_modification = value_from_dict(modifications, "night_vision_system")

    if night_vision_modification is not None:
        effects = value_from_dict(night_vision_modification, "effects")
        night_vision_devices = value_from_dict(effects, "nightVision")
    else:
        night_vision_devices = value_from_dict(v_details, "night_vision")
    ir_devices = NightVisionDevice()
    thermal_devices = NightVisionDevice()

    device_mapping = {
        "gunnerThermal": (thermal_devices, "gunner_device", THERMAL_VISION_GENERATIONS),
        "pilotThermal": (thermal_devices, "pilot_device", THERMAL_VISION_GENERATIONS),
        "sightTPodThermal": (thermal_devices, "targeting_pod_device", THERMAL_VISION_GENERATIONS),
        "sightThermal": (thermal_devices, "sight_device", THERMAL_VISION_GENERATIONS),
        "driverThermal": (thermal_devices, "driver_device", THERMAL_VISION_GENERATIONS),
        "commanderViewThermal": (thermal_devices, "commander_device", THERMAL_VISION_GENERATIONS),
        "gunnerIr": (ir_devices, "gunner_device", IR_VISION_GENERATIONS),
        "pilotIr": (ir_devices, "pilot_device", IR_VISION_GENERATIONS),
        "sightTPodIr": (ir_devices, "targeting_pod_device", IR_VISION_GENERATIONS),
        "sightIr": (ir_devices, "sight_device", IR_VISION_GENERATIONS),
        "driverIr": (ir_devices, "driver_device", IR_VISION_GENERATIONS),
        "commanderViewIr": (ir_devices, "commander_device", IR_VISION_GENERATIONS),
    }

    for device in night_vision_devices:
        if device in device_mapping:
            device_obj, attribute, generation_dict = device_mapping[device]
            resolution = tuple(value_from_dict(night_vision_devices.get(device), "resolution"))
            setattr(device_obj, attribute, generation_dict.get(resolution))

    if ir_devices.is_all_null() and thermal_devices.is_all_null():
        return None, None
    if ir_devices.is_all_null():
        ir_devices = None
    if thermal_devices.is_all_null():
        thermal_devices = None

    return ir_devices, thermal_devices


def create_vehicle_ballistic_computer(v_details: dict, vehicle_type: str) -> BallisticComputer | None:
    """Create vehicle"s ballistic computer

    Args:
        v_details (dict): vehicle"s fetched details
        vehicle_type (str): vehicle"s type

    Returns:
        BallisticComputer|None: Ballistic Computer Object
    """
    if vehicle_type in SEA_TYPES or vehicle_type in GROUND_TYPES:
        return None
    else:
        ballistic_computer = BallisticComputer()
        ballistic_computer.has_gun_ccip = bool(value_from_dict(v_details, "haveCCIPForGun", False))
        ballistic_computer.has_turret_ccip = bool(value_from_dict(v_details, "haveCCIPForTurret", False))
        ballistic_computer.has_bombs_ccip = bool(value_from_dict(v_details, "haveCCIPForBombs", False))
        ballistic_computer.has_rocket_ccip = bool(value_from_dict(v_details, "haveCCIPForRocket", False))
        ballistic_computer.has_gun_ccrp = bool(value_from_dict(v_details, "haveCCRPForGun", False))
        ballistic_computer.has_turret_ccrp = bool(value_from_dict(v_details, "haveCCRPForTurret", False))
        ballistic_computer.has_bombs_ccrp = bool(value_from_dict(v_details, "haveCCRPForBombs", False))
        ballistic_computer.has_rocket_ccrp = bool(value_from_dict(v_details, "haveCCRPForRocket", False))

        if ballistic_computer.is_all_false():
            return None

        return ballistic_computer


def create_weapons(v_name: str, v_details: dict, customizable: bool = False):
    """Create Gun Object
    Args:
        v_name:
        v_details:
        customizable:
    Returns:
        Gun Object
    """
    final_weapons: set[Weapon] = set()
    final_presets: set[Preset] = set()

    if customizable:
        if value_from_dict(v_details, "commonWeapons") == {}: return final_weapons
        default_weapons = value_from_dict(value_from_dict(v_details, "WeaponSlots"), "WeaponSlot", [])
        if len(default_weapons) == 0: return final_weapons
        if type(value_from_dict(default_weapons, "WeaponPreset", [])) is list:
            for gun in value_from_dict(default_weapons, "WeaponPreset", []):
                preset: Preset = Preset()
                preset.name = gun["name"]

                if isinstance(value_from_dict(gun, "Weapon"), list):
                    for gun_part in value_from_dict(gun, "Weapon"):
                        if "dummy" not in gun_part["blk"]:
                            preset.weapons.append(create_weapon_details(gun_part["blk"]))

                # TODO: This is a temporary fix, figure out an elegant solution
                final_presets.add(copy.deepcopy(preset))
                preset.weapons.clear()

        # For when vehicles can mount only one weapon (F4U-4)
        elif isinstance(value_from_dict(default_weapons, "WeaponPreset", []), dict):
            preset = Preset()
            preset.name = value_from_dict(default_weapons, "WeaponPreset", [])["name"]
            if isinstance(value_from_dict(default_weapons, "WeaponPreset", [])["Weapon"], list):
                for gun in value_from_dict(default_weapons, "WeaponPreset", [])["Weapon"]:
                    if "dummy" not in gun["blk"]:
                        preset.weapons.append(create_weapon_details(gun["blk"]))

            preset.weapons = group_and_increment(preset.weapons, "name")
            final_presets.add(copy.deepcopy(preset))
            preset.weapons.clear()
        return final_presets
    else:
        # TODO: Could add support for depression/elevation
        vehicle_file_weapons = value_from_dict(value_from_dict(v_details, "commonWeapons"), "Weapon", [])
        vehicle_file_weapons = [vehicle_file_weapons] if isinstance(vehicle_file_weapons, dict) else vehicle_file_weapons

        for weapon in vehicle_file_weapons:
            weapon_path: str = value_from_dict(weapon, "blk")
            if weapon_path is None:
                cLogger.warning(f"{v_name} weapon weapon_path not exist")
                continue
            weapon_path = weapon_path if weapon_path.endswith(".blk") else f"{weapon_path}.blk"
            if weapon_path.endswith("dummy_weapon.blk"):
                continue

            weapon_details: Weapon = create_weapon_details(weapon_path)
            final_weapons.add(weapon_details)

        final_weapons = group_and_increment(final_weapons, "name")
        return final_weapons


# TODO: Is count really necessary here? Perhaps yes, see customizable presets creation
def create_weapon_details(weapon_path: str, count: int = 1):
    """Create Weapon Object

    Args:
        count:
        weapon_path (str): Weapon"s weapon_path
    Returns:
        Weapon Object
    """
    if not weapon_path.endswith(".blk"):
        weapon_path += ".blk"

    weapon_blkx: dict = myFetch(get_guns_url(weapon_path), True)

    name_regex = re.findall(r".*\/(.*).blk", weapon_path)

    weapon_type = value_from_dict(weapon_blkx, "weaponType")

    is_rocket: bool = value_from_dict(weapon_blkx, ROCKET_NAME) or dictHasKeyInsensitive(weapon_blkx, ROCKET_TYPE) or value_from_dict(weapon_blkx, ROCKET_TYPE)
    is_cannon: bool = value_from_dict(weapon_blkx, CANNON_NAME) or dictHasKeyInsensitive(weapon_blkx, CANNON_TYPE) or value_from_dict(weapon_blkx, CANNON_TYPE) or weapon_type == -1 or weapon_type == 1 or weapon_type == 3
    is_torpedo: bool = value_from_dict(weapon_blkx, TORPEDO_NAME) or dictHasKeyInsensitive(weapon_blkx, TORPEDO_TYPE) or value_from_dict(weapon_blkx, TORPEDO_TYPE) or weapon_type == 1
    is_bomb: bool = value_from_dict(weapon_blkx, BOMB_NAME) or dictHasKeyInsensitive(weapon_blkx, BOMB_TYPE) or value_from_dict(weapon_blkx, BOMB_TYPE)
    is_booster: bool = value_from_dict(weapon_blkx, BOOSTER_NAME) or dictHasKeyInsensitive(weapon_blkx, BOOSTER_TYPE) or value_from_dict(weapon_blkx, BOOSTER_TYPE)
    is_container: bool = value_from_dict(weapon_blkx, CONTAINER_NAME) or dictHasKeyInsensitive(weapon_blkx, CONTAINER_TYPE) or value_from_dict(weapon_blkx, CONTAINER_TYPE)
    is_extfueltank: bool = value_from_dict(weapon_blkx, EXTFUELTANK_NAME) or dictHasKeyInsensitive(weapon_blkx, EXTFUELTANK_TYPE) or value_from_dict(weapon_blkx, EXTFUELTANK_TYPE)

    valid = weapon_type is not None or is_rocket or is_torpedo or is_cannon or is_bomb or is_booster or is_container or is_extfueltank
    if not valid:
        cLogger.error(f"""The weapon {name_regex[0]} -  type is missing {get_guns_url(weapon_path)} weapon_type={weapon_type}\tis_rocket={is_rocket}\tis_cannon={is_cannon}\tis_torpedo={is_torpedo}\tIS_BOMB={is_bomb}\tis_container={is_container}""")
        return

    final_ammos: set[Ammo] = set()

    all_weapons_keys = dictKeysToList(weapon_blkx)
    if is_cannon:
        final_ammos = get_ammos_by_weapon("bullet", weapon_blkx, all_weapons_keys)
    elif is_rocket:
        final_ammos = get_ammos_by_weapon("rocket", weapon_blkx, all_weapons_keys)
    elif is_torpedo:
        final_ammos = get_ammos_by_weapon("torpedo", weapon_blkx, all_weapons_keys)
    elif is_bomb:
        final_ammos = get_ammos_by_weapon("bomb", weapon_blkx, all_weapons_keys)
    elif is_booster:
        final_ammos = get_ammos_by_weapon("payload", weapon_blkx, all_weapons_keys)
    elif is_container:
        return create_weapon_details(weapon_blkx["blk"], weapon_blkx["bullets"])

    elif is_extfueltank:
        final_ammos = get_ammos_by_weapon("payload", weapon_blkx, all_weapons_keys)

    weapon: Weapon = Weapon()
    weapon.name = name_regex[0]
    weapon.weapon_type = CANNON_NAME if is_cannon else ROCKET_NAME if is_rocket else TORPEDO_NAME if is_torpedo else BOMB_NAME if is_bomb else BOOSTER_NAME if is_booster else CONTAINER_NAME
    weapon.count = count

    weapon.ammos = final_ammos
    ALL_WEAPONS.add(weapon.name)

    return weapon


def get_ammos_by_weapon(weapon_type: str, all_weapons: dict[any], all_weapons_keys=[]):
    final_ammos: set[Ammo] = set()
    for key in all_weapons_keys:
        raw_ammo = None
        key_value = value_from_dict(all_weapons, key)

        if (isinstance(key_value, dict) or isinstance(key_value, list)) and key.lower() == weapon_type.lower():
            raw_ammo = key_value
        elif isinstance(key_value, dict) and dictHasKeyInsensitive(key_value, weapon_type):
            raw_ammo = value_from_dict(key_value, weapon_type)

        if not raw_ammo:
            continue

        raw_ammo = raw_ammo if type(raw_ammo) is list else [raw_ammo]
        if len(raw_ammo) == 0:
            pass
        for _ammo in raw_ammo:
            ammo = create_ammo(_ammo)
            final_ammos.add(ammo)

    return final_ammos


def create_ammo(raw_ammo: dict):
    explosive_type = value_from_dict(raw_ammo, "explosiveType")
    explosive_mass = value_from_dict(raw_ammo, "explosiveMass")

    name = value_from_dict(raw_ammo, "bombName", value_from_dict(raw_ammo, "bulletName"))
    _type = value_from_dict(raw_ammo, "bombType", value_from_dict(raw_ammo, "bulletType"))
    mass = value_from_dict(raw_ammo, "mass")
    mass = mass[0] if type(mass) is list else mass
    # ship else generic
    speed = value_from_dict(raw_ammo, "maxSpeedInWater",
                            value_from_dict(raw_ammo, "speed", value_from_dict(raw_ammo, "maxSpeed")))
    caliber = value_from_dict(raw_ammo, "caliber")
    # ship else generic
    max_distance = value_from_dict(raw_ammo, "distToLive", value_from_dict(raw_ammo, "maxDistance"))

    out: Ammo = Ammo()
    out.name = name
    # If type is a list, get the first element
    out.type = _type[0] if type(_type) is list else _type
    out.caliber = caliber
    out.mass = mass
    out.speed = speed
    out.max_distance = max_distance
    out.explosive_type = explosive_type
    out.explosive_mass = explosive_mass

    # For localization
    if out.name is not None:
        ALL_AMMOS.add(out.name)
    if out.explosive_type is not None:
        ALL_EXPLOSIVES.add(explosive_type)
    if out.type is not None:
        ALL_AMMO_TYPES.add(out.type)
    return out


def create_presets(v_details: dict, customizable: bool, has_offensive_weapons: bool):
    final_presets = []
    weapon_presets = value_from_dict(v_details, "weapon_presets")
    presets = value_from_dict(weapon_presets, "preset")

    # Do not touch this, it is to filter out default presets (no preset in-game)
    if type(presets) is dict:
        return []
    if customizable:
        weapon_slots = value_from_dict(v_details, "WeaponSlots")
        weapon_slot: list = value_from_dict(weapon_slots, "WeaponSlot")
        SLOT_HASHMAP = {}
        for slot in weapon_slot:
            SLOT_HASHMAP[slot["index"]] = weapon_slot.index(slot)

        for preset in presets[1:] if has_offensive_weapons else presets:
            final_preset = Preset()
            final_preset.name = preset["name"]
            # Retrieve list of objects with inside: SLOT and PRESET (preset name)
            preset_details = value_from_dict(myFetch(get_guns_url(preset["blk"]), True), "Weapon", [])
            if isinstance(preset_details, dict):
                preset_details = [preset_details]
            for weapon_of_preset in preset_details:
                # Get all the guns from a specific pylon
                pylon_guns = value_from_dict(weapon_slot[SLOT_HASHMAP[weapon_of_preset["slot"]]], "WeaponPreset")

                # TODO: Find an example for this?
                if isinstance(pylon_guns, dict):
                    if type(pylon_guns["Weapon"]) is list:
                        for weapon in pylon_guns["Weapon"]:
                            if "dummy" not in value_from_dict(weapon, "blk", []):
                                final_preset.weapons.append(create_weapon_details(weapon["blk"]))
                    else:
                        if "dummy" not in value_from_dict(pylon_guns["Weapon"], "blk", []):
                            final_preset.weapons.append(create_weapon_details(pylon_guns["Weapon"]["blk"]))
                elif isinstance(pylon_guns, list):
                    for weapon in pylon_guns:
                        # Check if the weapon name is the same as the preset name
                        if weapon["name"] == weapon_of_preset["preset"]:
                            if isinstance(weapon["Weapon"], dict) and ("dummy" not in value_from_dict(weapon["Weapon"], "blk")):
                                final_preset.weapons.append(create_weapon_details(weapon["Weapon"]["blk"]))
                            # TODO: Find an example for this?
                            elif isinstance(weapon["Weapon"], list):
                                for w in weapon["Weapon"]:
                                    if "dummy" not in value_from_dict(w, "blk", []):
                                        final_preset.weapons.append(create_weapon_details(w["blk"]))
                else:
                    cLogger.warning("Error while creating: " + preset["name"])
                    pass
            final_preset.weapons = group_and_increment(final_preset.weapons, "name")
            final_presets.append(copy.deepcopy(final_preset))

    else:
        for preset in presets:

            blk = value_from_dict(preset, "blk")
            preset = myFetch(get_guns_url(blk), True)

            if "_default" not in blk.lower() and "empty" not in blk.lower() and preset.get("Weapon") is not None:
                final_preset = Preset()
                name_regex = re.findall(r".*\/(.*).blk", blk)
                final_preset.name = name_regex[0]
                weapons = value_from_dict(preset, "Weapon")

                # ! Do not touch this
                if type(weapons) is not list:
                    if "dummy" not in value_from_dict(preset["Weapon"], "blk", []):
                        final_preset.weapons.append(create_weapon_details(value_from_dict(preset["Weapon"], "blk")))
                else:
                    for weapon in weapons:
                        if "dummy" not in value_from_dict(preset["Weapon"], "blk", []):
                            final_preset.weapons.append(create_weapon_details(value_from_dict(weapon, "blk")))

                final_preset.weapons = group_and_increment(final_preset.weapons, "name")
                # TODO: This is a temporary fix, figure out an elegant solution.
                final_presets.append(copy.deepcopy(final_preset))

    return final_presets


def create_customizable_presets(v_details: dict, has_offensive_weapons: bool) -> CustomizablePreset:
    weapon_slots = value_from_dict(v_details, "WeaponSlots")

    customizable_preset = CustomizablePreset()
    customizable_preset.max_load = value_from_dict(weapon_slots, "maxloadMass", 0)
    customizable_preset.max_load_left_wing = value_from_dict(weapon_slots, "maxloadMassLeftConsoles", 0)
    customizable_preset.max_load_right_wing = value_from_dict(weapon_slots, "maxloadMassRightConsoles", 0)
    customizable_preset.max_disbalance = value_from_dict(weapon_slots, "maxDisbalance", 0)

    weapon_slot: list = value_from_dict(weapon_slots, "WeaponSlot")

    # TODO: not sure if skipping the first slot is a good idea (see buccaneer s2) or maybe skip only if it does not have tier or order key
    for slot in weapon_slot[1:] if has_offensive_weapons else weapon_slot:

        pylon = Pylon()
        pylon.index = value_from_dict(slot, "index", 1)
        pylon.used_for_disbalance = not value_from_dict(slot, "notUseforDisbalanceCalculation", False)

        available_weapons = value_from_dict(slot, "WeaponPreset", [])

        if isinstance(available_weapons, dict):
            available_weapons = [available_weapons]

        for weapon_object in available_weapons:
            # Get all the guns from a specific pylon
            weapons = value_from_dict(weapon_object, "Weapon")

            if isinstance(weapons, dict):
                weapons = [weapons]

            if weapons is not None:
                for weapon in weapons:
                    # TODO: Perhaps set count to number of ammos? (see bullets)
                    if "dummy_weapon" not in weapon["blk"]:
                        pylon.selectable_weapons.append(create_weapon_details(weapon["blk"]))

        pylon.selectable_weapons = group_and_increment(pylon.selectable_weapons, "name")
        customizable_preset.pylons.append(copy.deepcopy(pylon))

    customizable_preset.pylons.sort(key=lambda x: x.index, reverse=False)
    return customizable_preset


def group_and_increment(set_of_items, property_name):
    item_dict = {}
    for item in set_of_items:
        property_value = getattr(item, property_name)
        if property_value not in item_dict:
            item_dict[property_value] = item
        else:
            item_dict[property_value].count += item.count
    return list(item_dict.values())
