import os

from dotenv import load_dotenv

from utils.simple_functions import getJson

load_dotenv()


def read_game_version(version_path: str):
    with open(version_path, 'r') as f:
        return f.read()


WPCOST = getJson(os.getenv("DATAMINE_LOCATION") + "/char.vromfs.bin_u/config/wpcost.blkx")
UNIT_TAGS = getJson(os.getenv("DATAMINE_LOCATION") + "/char.vromfs.bin_u/config/unittags.blkx")
LANG_UNITS = (os.getenv("DATAMINE_LOCATION") + "/lang.vromfs.bin_u/lang/units.csv")
LANG_WEAPONS = (os.getenv("DATAMINE_LOCATION") + "/lang.vromfs.bin_u/lang/units_weaponry.csv")
URL_VROMFS = (os.getenv("DATAMINE_LOCATION") + "/aces.vromfs.bin_u/")
SHOP = getJson(os.getenv("DATAMINE_LOCATION") + "/char.vromfs.bin_u/config/shop.blkx")
MODIFICATIONS: dict = getJson(os.getenv("DATAMINE_LOCATION") + "/char.vromfs.bin_u/config/modifications.blkx")["modifications"]

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

BATTLE_RATINGS = [1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0, 4.3, 4.7, 5.0, 5.3, 5.7, 6.0, 6.3, 6.7, 7.0, 7.3, 7.7, 8.0, 8.3, 8.7, 9.0, 9.3, 9.7, 10.0, 10.3, 10.7, 11.0, 11.3, 11.7, 12.0, 12.3, 12.7, 13.0, 13.3, 13.7]

GROUND_TYPES: set[str] = {'light_tank', 'medium_tank', 'heavy_tank', 'tank_destroyer', 'spaa'}
AIR_TYPES: set[str] = {'fighter', 'assault', 'bomber', 'helicopter'}
SEA_TYPES: set[str] = {'destroyer', 'submarine_chaser', 'cruiser', 'battleship', 'gun_boat', 'torpedo_boat', 'torpedo_gun_boat', 'naval_ferry_barge'}

AIR_TYPES2: set[str] = {"attack_helicopter", "utility_helicopter", "fighter", "assault", "bomber"}
GROUND_TYPES2: set[str] = {"tank", "light_tank", "medium_tank", "heavy_tank", "tank_destroyer", "spaa", "lbv", "mbv", "hbv", "exoskeleton"}
SEA_TYPES2: set[str] = {"ship", "destroyer", "light_cruiser", "boat", "heavy_boat", "barge", "frigate", "heavy_cruiser", "battlecruiser", "battleship", "submarine"}

AIR_CLASSES = ["exp_fighter", "exp_bomber", "exp_assault", "exp_helicopter"]
GROUND_CLASSES = ["exp_tank", "exp_tank_destroyer", "exp_SPAA", "exp_heavy_tank"]
SEA_CLASSES = ["exp_cruiser", "exp_destroyer", "exp_gun_boat", "exp_torpedo_boat", "exp_submarine_chaser", "exp_torpedo_gun_boat", "exp_naval_ferry_barge"]
