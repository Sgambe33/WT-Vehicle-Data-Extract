import filecmp
import os
import json
import shutil
import paramiko as pk
import requests
from tqdm import tqdm
from dotenv import load_dotenv
from scp import SCPClient

from utils import cLogger
from utils.simple_functions import value_from_dict
from utils.constants import MODIFICATIONS
from datetime import datetime, timedelta


load_dotenv()
COUNTRIES = ["ussr", "usa", "china", "japan", "italy",
             "germany", "israel", "sweden", "britain", "france"]
AIR_CLASSES = ["exp_fighter", "exp_bomber", "exp_assault", "exp_helicopter"]
GROUND_CLASSES = ["exp_tank", "exp_tank_destroyer",
                  "exp_SPAA", "exp_heavy_tank"]
SEA_CLASSES = ["exp_cruiser", "exp_destroyer", "exp_gun_boat", "exp_torpedo_boat",
               "exp_submarine_chaser", "exp_torpedo_gun_boat", "exp_naval_ferry_barge"]


def update_dataset():
    with open("War-Thunder-Datamine" + "/char.vromfs.bin_u/config/wpcost.blkx", "r", encoding="UTF-8") as f:
        wpcost = json.load(f)

    del wpcost["economicRankMax"]

    for n in tqdm(COUNTRIES):
        air_list = []
        ground_list = []
        sea_list = []
        country_dir = os.path.abspath("./nations/" + n)

        if not os.path.exists(country_dir):
            os.makedirs(country_dir)

        air_path = os.path.abspath(
            "./nations/" + n + "/country_" + n + "_air.json")
        ground_path = os.path.abspath(
            "./nations/" + n + "/country_" + n + "_ground.json")
        sea_path = os.path.abspath(
            "./nations/" + n + "/country_" + n + "_sea.json")

        for i in wpcost:

            if wpcost[i]["unitClass"] in AIR_CLASSES and wpcost[i]["country"] == "country_" + n:
                air_list.append(i)
            elif wpcost[i]["unitClass"] in GROUND_CLASSES and wpcost[i]["country"] == "country_" + n:
                ground_list.append(i)
            elif wpcost[i]["unitClass"] in SEA_CLASSES and wpcost[i]["country"] == "country_" + n:
                sea_list.append(i)

        if len(air_list) != 0:
            with open(air_path, "w") as f:
                json.dump(air_list, f, indent=3)

        if len(ground_list) != 0:
            with open(ground_path, "w") as f:
                json.dump(ground_list, f, indent=3)

        if len(sea_list) != 0:
            with open(sea_path, "w") as f:
                json.dump(sea_list, f, indent=3)


def update_images():
    directories = {
        "/atlases.vromfs.bin_u/units": "./assets/techtrees/",
        "/tex.vromfs.bin_u/tanks": "./assets/images/",
        "/tex.vromfs.bin_u/ships": "./assets/images/",
        "/tex.vromfs.bin_u/aircrafts": "./assets/images/",
        "/atlases.vromfs.bin_u/gameuiskin": "./assets/modifications/"
    }

    for dir, dest in directories.items():
        cLogger.info(f"Updating {dir} to {dest}")
        path = "War-Thunder-Datamine" + dir
        files = os.listdir(path)
        for file in tqdm(files):
            if dir == "/atlases.vromfs.bin_u/gameuiskin" and not valid_mod_icon(file.replace(".png", "")):
                continue
            source = os.path.join(path, file)
            destination = os.path.join(os.path.abspath(dest), file)
            if not os.path.exists(destination) or not filecmp.cmp(source, destination):
                shutil.copy(source, destination)


def valid_mod_icon(file: str):
    """Check if the icon is valid for a modification.

    Returns:
        bool: True if the icon is valid, False otherwise.
    """
    for mod in MODIFICATIONS:
        icon = value_from_dict(MODIFICATIONS[mod], "image")
        if icon is not None and file in icon:
            return True
    return False
