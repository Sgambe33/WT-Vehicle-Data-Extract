import copy
import json
import os
from tqdm import tqdm
import pandas as pd
from dotenv import load_dotenv
from db.models import Vehicle
from utils import cLogger

load_dotenv()

DATAMINE_LOCATION = os.getenv("DATAMINE_LOCATION")
UNITS_LANG = open(os.path.join(os.getenv("DATAMINE_LOCATION"), "lang.vromfs.bin_u/lang/units.csv"), 'r', encoding="UTF-8")

LOCALIZATION_TEMPLATE = {
    "vehicles": {},
    "modifications": {},
    "weapons": {},
    "ammos": {},
    "ammo_types": {},
    "explosives": {}
}

languages = {
    "Belarusian": "be",
    "Czech": "cs",
    "German": "de",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "Hungarian": "hu",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Serbian": "sr",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Vietnamese": "vi",
    "Chinese": "zh"
}

language_data = {lang: copy.deepcopy(LOCALIZATION_TEMPLATE) for lang in languages}

ALL_WEAPONS: set[str] = set()
ALL_AMMOS: set[str] = set()
ALL_AMMO_TYPES: set[str] = set()
ALL_EXPLOSIVES: set[str] = set()

UNITS_LANG_CSV = pd.read_csv(UNITS_LANG, delimiter=";", encoding="UTF-8")
UNITS_LANG_CSV.set_index("<ID|readonly|noverify>", inplace=True)

MODIFICATIONS_LANG_CSV = pd.read_csv(os.path.join(DATAMINE_LOCATION, "lang.vromfs.bin_u/lang/units_modifications.csv"), delimiter=";", encoding="utf-8")
MODIFICATIONS_LANG_CSV.set_index("<ID|readonly|noverify>", inplace=True)

WEAPONRY_LANG_CSV = pd.read_csv(os.path.join(DATAMINE_LOCATION, "lang.vromfs.bin_u/lang/units_weaponry.csv"), delimiter=";", encoding="utf-8")
WEAPONRY_LANG_CSV.set_index("<ID|readonly|noverify>", inplace=True)


def get_localized_identifier(identifier, lang, suffix):
    localized_identifier = UNITS_LANG_CSV.loc[identifier + suffix]
    return localized_identifier[f"<{lang.capitalize()}>"]


def get_localized_modification(modification, lang, suffix):
    try:
        localized_modification = MODIFICATIONS_LANG_CSV.loc["modification/" + modification + suffix]
    except KeyError:
        return None
    return localized_modification[f"<{lang.capitalize()}>"]


def get_localized_weaponry(key, lang, suffix):
    try:
        localized_weapon = WEAPONRY_LANG_CSV.loc[key + suffix]
    except KeyError:
        return None
    return localized_weapon[f"<{lang.capitalize()}>"]


def sanitize_language_data():
    for lang in languages:
        vehicles = language_data[lang]["vehicles"]
        for key, value in vehicles.items():
            vehicles[key] = value.replace("\u00a0", " ")


def generate_locales():
    destination_path = "./generatedAssets/locales"
    vehicles_identifiers = [v.identifier for v in Vehicle.select(Vehicle.identifier)]
    vehicles_modifications = [v.modifications for v in Vehicle.select(Vehicle.modifications)]
    vehicles_modifications_names = set()
    for mods in vehicles_modifications:
        for mod in mods:
            vehicles_modifications_names.add(mod["name"])

    cLogger.info("Localizing vehicles")
    for identifier in tqdm(vehicles_identifiers):
        real_id = identifier
        if "football" in identifier:
            real_id = "us_m551"
        for lang in languages:
            try:
                language_data[lang]["vehicles"][real_id.lower() + "_short"] = get_localized_identifier(real_id, lang, "_shop")
                language_data[lang]["vehicles"][real_id.lower() + "_extended"] = get_localized_identifier(real_id, lang, "_0")
            except KeyError:
                pass

    cLogger.info("Localizing modifications")
    for mod in tqdm(vehicles_modifications_names):
        for lang in languages:
            try:
                localized_mod = get_localized_modification(mod, lang, "")
                localized_mod_desc = get_localized_modification(mod, lang, "/desc")
                if localized_mod and localized_mod_desc:
                    language_data[lang]["modifications"][mod.lower() + ""] = localized_mod
                    language_data[lang]["modifications"][mod.lower() + "_desc"] = localized_mod_desc
            except KeyError:
                pass

    cLogger.info("Localizing weapons")
    for weapon in ALL_WEAPONS:
        for lang in languages:
            try:
                weapon_name = get_localized_weaponry(f"weapons/{weapon}", lang, "")
                if weapon_name:
                    language_data[lang]["weapons"][weapon.lower()] = weapon_name
            except KeyError:
                pass

    cLogger.info("Localizing ammos")
    for ammo in tqdm(ALL_AMMOS):
        for lang in languages:
            try:
                ammo_name = get_localized_weaponry(ammo, lang, "")
                if ammo_name:
                    language_data[lang]["ammos"][ammo.lower()] = ammo_name
            except KeyError:
                pass

    cLogger.info("Localizing explosives")
    for explosive in tqdm(ALL_EXPLOSIVES):
        for lang in languages:
            try:
                explosive_name = get_localized_weaponry(f"explosiveType/{explosive}", lang, "")
                if explosive_name:
                    language_data[lang]["explosives"][explosive.lower()] = explosive_name
            except KeyError:
                pass

    cLogger.info("Localizing ammo types")
    for ammo_type in tqdm(ALL_AMMO_TYPES):
        for lang in languages:
            try:
                ammo_type_name = get_localized_weaponry(ammo_type, lang, "/name")
                ammo_type_name_short = get_localized_weaponry(ammo_type, lang, "/name/short")
                if ammo_type_name:
                    language_data[lang]["ammo_types"][ammo_type.lower()] = ammo_type_name
                    language_data[lang]["ammo_types"][ammo_type.lower() + "_short"] = ammo_type_name_short

            except KeyError:
                pass

    sanitize_language_data()

    os.makedirs(destination_path, exist_ok=True)
    for lang, iso_code in languages.items():
        file_path = os.path.join(destination_path, f"{iso_code}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding="UTF-8") as f:
                existing_data = json.load(f)
            existing_data.update(language_data[lang])
            data_to_write = existing_data
        else:
            data_to_write = language_data[lang]
        with open(file_path, 'w', encoding="UTF-8") as f:
            json.dump(data_to_write, f, indent=3, ensure_ascii=False)
