import filecmp
import os
import json
import shutil
from tqdm import tqdm
from dotenv import load_dotenv
from utils import cLogger
from utils.simple_functions import value_from_dict
from utils.constants import MODIFICATIONS, COUNTRIES, AIR_CLASSES, GROUND_CLASSES, SEA_CLASSES

load_dotenv()


def update_dataset():
    """
    Update the dataset by processing the `wpcost.blkx` file.

    This function reads the `wpcost.blkx` file and then iterates
    over the countries to create JSON files for air, ground, and sea units.

    Returns:
        None
    """
    with open(os.getenv("DATAMINE_LOCATION") + "/char.vromfs.bin_u/config/wpcost.blkx", "r", encoding="UTF-8") as f:
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


def update_images() -> None:
    """
    Update images by moving them from source directories to destination directories.

    This function iterates over a predefined set of source directories and moves images
    to corresponding destination directories. It checks if the images already exist in
    the destination and only copies them if they do not exist or are different.

    Directories:
        - "/atlases.vromfs.bin_u/units": "./assets/techtrees/"
        - "/tex.vromfs.bin_u/tanks": "./assets/images/"
        - "/tex.vromfs.bin_u/ships": "./assets/images/"
        - "/tex.vromfs.bin_u/aircrafts": "./assets/images/"
        - "/atlases.vromfs.bin_u/gameuiskin": "./assets/modifications/"

    Returns:
        None
    """
    directories = {
        "/atlases.vromfs.bin_u/units": "./assets/techtrees/",
        "/tex.vromfs.bin_u/tanks": "./assets/images/",
        "/tex.vromfs.bin_u/ships": "./assets/images/",
        "/tex.vromfs.bin_u/aircrafts": "./assets/images/",
        "/atlases.vromfs.bin_u/gameuiskin": "./assets/modifications/"
    }

    for source_dir, dest_dir in directories.items():
        cLogger.info(f"Moving images from {source_dir} to {dest_dir} if necessary")
        path = os.getenv("DATAMINE_LOCATION") + source_dir
        files = os.listdir(path)
        os.makedirs(dest_dir, exist_ok=True)
        for file in tqdm(files):
            if source_dir == "/atlases.vromfs.bin_u/gameuiskin" and not valid_mod_icon(file.replace(".png", "")):
                continue
            source = os.path.join(path, file)
            destination = os.path.join(os.path.abspath(dest_dir), file)
            if not os.path.exists(destination) or not filecmp.cmp(source, destination):
                shutil.copy(source, destination)


def valid_mod_icon(file: str) -> bool:
    """Check if the icon is valid for a modification.

    Returns:
        bool: True if the icon is valid, False otherwise.
    """
    for mod in MODIFICATIONS:
        icon = value_from_dict(MODIFICATIONS[mod], "image")
        if icon is not None and file in icon:
            return True
    return False
