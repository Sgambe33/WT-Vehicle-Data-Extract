import os

from dotenv import load_dotenv

from utils.simple_functions import getJson

load_dotenv()


def read_game_version(version_path: str):
    with open(version_path, 'r') as f:
        return f.read()


WPCOST = getJson("War-Thunder-Datamine" + "/char.vromfs.bin_u/config/wpcost.blkx")
UNIT_TAGS = getJson("War-Thunder-Datamine" + "/char.vromfs.bin_u/config/unittags.blkx")
LANG_UNITS = ("War-Thunder-Datamine" + "/lang.vromfs.bin_u/lang/units.csv")
LANG_WEAPONS = ("War-Thunder-Datamine" + "/lang.vromfs.bin_u/lang/units_weaponry.csv")
URL_VROMFS = ("War-Thunder-Datamine" + "/aces.vromfs.bin_u/")
SHOP = getJson("War-Thunder-Datamine" + "/char.vromfs.bin_u/config/shop.blkx")
MODIFICATIONS: dict = getJson("War-Thunder-Datamine" + "/char.vromfs.bin_u/config/modifications.blkx")["modifications"]

COUNTRIES = ["britain", "china", "france", "germany", "israel", "italy", "japan", "sweden", "usa", "ussr"]

VEHICLE_FETCH_URI = {
    'ground': '/units/tankmodels',
    'sea': '/units/ships',
    'air': '/flightmodels',
}

ENGINE_HP_AB_MUL_TANK = 1.908
ENGINE_SPEED_AB_MUL_TANK = 1.101
ENGINE_SPEED_AB_MUL_SHIP = 1.222
ENGINE_SPEED_AB_MUL_AIR = 1.037


CANNON_TYPE = 'bullet'
ROCKET_TYPE = 'rocketGun'
TORPEDO_TYPE = 'torpedoGun'
BOMB_TYPE = 'bombGun'
BOOSTER_TYPE = 'boosterGun'
CONTAINER_TYPE = 'container'
EXTFUELTANK_TYPE = 'fuelTankGun'

CANNON_NAME = 'cannon'
ROCKET_NAME = 'rocket'
TORPEDO_NAME = 'torpedo'
BOMB_NAME = 'bomb'
BOOSTER_NAME = 'payload'
CONTAINER_NAME = 'container'
EXTFUELTANK_NAME = 'payload'

THERMAL_VISION_GENERATIONS: dict = {
    (500, 300): "GEN1",
    (800, 600): "GEN2",
    (1024, 768): "GEN2+",
    (1200, 800): "GEN3",
    (1920, 1080): "GEN3+",
}

IR_VISION_GENERATIONS: dict = {
    (800, 600): "GEN1",
    (1024, 768): "GEN2",
    (1200, 800): "GEN2+",
    (1600, 1200): "GEN3",
    (1920, 1080): "GEN3+",
}

WATCHED_PATHS_BLKX = [
    "aces.vromfs.bin_u/gamedata/flightmodels",
    "aces.vromfs.bin_u/gamedata/units/tankmodels",
    "aces.vromfs.bin_u/gamedata/units/ships",
    "aces.vromfs.bin_u/gamedata/sensors",
    "char.vromfs.bin_u/config/wpcost.blkx",
    "char.vromfs.bin_u/config/unittags.blkx",
    "char.vromfs.bin_u/config/modifications.blkx"
]

WATCHED_PATHS_IMGS = [
    "tex.vromfs.bin_u/aircrafts",
    "tex.vromfs.bin_u/ships",
    "tex.vromfs.bin_u/tanks",
    "atlases.vromfs.bin_u/units"
]

BATTLE_RATINGS = {
    0: 1.0,
    1: 1.3,
    2: 1.7,
    3: 2.0,
    4: 2.3,
    5: 2.7,
    6: 3.0,
    7: 3.3,
    8: 3.7,
    9: 4.0,
    10: 4.3,
    11: 4.7,
    12: 5.0,
    13: 5.3,
    14: 5.7,
    15: 6.0,
    16: 6.3,
    17: 6.7,
    18: 7.0,
    19: 7.3,
    20: 7.7,
    21: 8.0,
    22: 8.3,
    23: 8.7,
    24: 9.0,
    25: 9.3,
    26: 9.7,
    27: 10.0,
    28: 10.3,
    29: 10.7,
    30: 11.0,
    31: 11.3,
    32: 11.7,
    33: 12.0,
    34: 12.3,
    35: 12.7,
    36: 13.0,
    37: 13.3,
    38: 13.7,
}

GROUND_TYPES: set[str] = {'light_tank', 'medium_tank', 'heavy_tank', 'tank_destroyer', 'spaa'}
AIR_TYPES: set[str] = {'fighter', 'assault', 'bomber', 'helicopter'}
# SEA_TYPES: set[str] = {'destroyer', 'submarine_chaser', 'cruiser', 'battleship', 'gun_boat', 'torpedo_boat', 'torpedo_gun_boat', 'naval_ferry_barge'}

# GROUND_TYPES: dict = {"light_tank":"┪",
#                      "medium_tank":"┬",
#                      "heavy_tank":"┨",
#                      "spaa":"┰",
#                      "tank_destroyer":"┴",
#                      "suit":"╅"
#                      }
# AIR_TYPES: dict = {"attack_helicopter", "utility_helicopter", "assault", "bomber", "heavy_bomber", "fighter", "fighter_assault", "ufo"}
SEA_TYPES: dict = {"gun_boat": "␉", "heavy_gun_boat": "␊", "heavy_boat": "␊", "naval_ferry_barge": "␋", "destroyer": "␌", "cruiser": "␏", "light_cruiser": "␎", "battlecruiser": "␐", "heavy_cruiser": "␐", "battleship": "␑", "submarine": "␒"}

AIR_TYPES2: set[str] = {"attack_helicopter", "utility_helicopter","fighter", "assault", "bomber"}
GROUND_TYPES2: set[str] =  {"tank", "light_tank", "medium_tank", "heavy_tank", "tank_destroyer", "spaa", "lbv", "mbv", "hbv", "exoskeleton"}
SEA_TYPES2: set[str] = {"ship", "destroyer", "light_cruiser", "boat", "heavy_boat", "barge", "frigate","heavy_cruiser", "battlecruiser", "battleship", "submarine"}  
