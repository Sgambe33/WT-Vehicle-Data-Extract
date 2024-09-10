import copy
import json
import os
from tqdm import tqdm
import pandas as pd
from dotenv import load_dotenv
from db.models import Vehicle

load_dotenv()

DATAMINE_LOCATION = os.getenv("DATAMINE_LOCATION")
UNITS_LANG = open(os.path.join("War-Thunder-Datamine", "lang.vromfs.bin_u/lang/units.csv"), 'r', encoding='utf-8')

LOCALIZATION_TEMPLATE = {
    "vehicles": {},
    "modifications": {},
    "presets": {},
    "weaponry": {}
}



languages = {
    'Belarusian': 'be',
    'Czech': 'cs',
    'German': 'de',
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'Hungarian': 'hu',
    'Italian': 'it',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Serbian': 'sr',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Vietnamese': 'vi',
    'Chinese': 'zh'
}

language_data = {lang: copy.deepcopy(LOCALIZATION_TEMPLATE) for lang in languages}

UNITS_LANG_CSV = pd.read_csv(UNITS_LANG, delimiter=';', encoding='utf-8')
UNITS_LANG_CSV.set_index('<ID|readonly|noverify>', inplace=True)

MODIFICATIONS_LANG_CSV = pd.read_csv(os.path.join("War-Thunder-Datamine", "lang.vromfs.bin_u/lang/units_modifications.csv"), delimiter=';', encoding='utf-8')
MODIFICATIONS_LANG_CSV.set_index('<ID|readonly|noverify>', inplace=True)

WEAPONRY_LANG_CSV = pd.read_csv(os.path.join("War-Thunder-Datamine", "lang.vromfs.bin_u/lang/units_weaponry.csv"), delimiter=';', encoding='utf-8')
WEAPONRY_LANG_CSV.set_index('<ID|readonly|noverify>', inplace=True)

def get_localized_identifier(identifier, lang, suffix):
    localized_identifier = UNITS_LANG_CSV.loc[identifier + suffix]
    return localized_identifier[f'<{lang.capitalize()}>']


def get_localized_modification(modification, lang, suffix):
    try:
        localized_modification = MODIFICATIONS_LANG_CSV.loc["modification/"+modification + suffix]
    except KeyError:
        return None
    return localized_modification[f'<{lang.capitalize()}>']


def sanitize_language_data():
    for lang in languages:
        vehicles = language_data[lang]["vehicles"]
        for key, value in vehicles.items():
            vehicles[key] = value.replace('\u00a0', ' ')


def generate_locales(destination_path):
    # Get all vehicles identifiers
    vehicles_identifiers = [v.identifier for v in Vehicle.select(Vehicle.identifier)]
    vehicles_modifications = [v.modifications for v in Vehicle.select(Vehicle.modifications)]
    vehicles_modifications_names = set()
    for mods in vehicles_modifications:
        for mod in mods:
            vehicles_modifications_names.add(mod['name'])    
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
            
    sanitize_language_data()

    os.makedirs(destination_path, exist_ok=True)
    for lang, iso_code in languages.items():
        file_path = os.path.join(destination_path, f"{iso_code}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding='utf-8') as f:
                existing_data = json.load(f)
            existing_data.update(language_data[lang])
            data_to_write = existing_data
        else:
            data_to_write = language_data[lang]
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(data_to_write, f, indent=3, ensure_ascii=False)
   