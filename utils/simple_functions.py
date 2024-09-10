import json
import os


def myFetch(path, isLocal=False):
    if not isLocal:
        pass
    with open(path, 'r') as f:
        return json.load(f)


def dictHasKeyInsensitive(dictionary: dict[any], keyName: str):
    allKeys = [i.lower() for i in dictionary.keys()]
    return keyName.lower() in allKeys


def dictKeysToList(d: dict):
    return [i for i in d.keys()]


def dictValuesToList(d: dict):
    return [i for i in d.values()]


def printList(l):
    for i in l:
        print(i)


def getJson(path):
    data = None
    if os.path.exists(path):
        with open(path, 'r', encoding="UTF-8") as f:
            data = json.load(f)
    return data


def getVersion():
    with open(os.getenv("DATAMINE_LOCATION") + "/aces.vromfs.bin_u/version", 'r') as f:
        return f.read()


def value_from_dict(dictionary: dict, key: str, fall_back_value: any = None):
    """Get value from a dictionary

    Args:
        dictionary (dict[any]): Dictionary
        key (str): Key to search
        fall_back_value (any, optional): Fallback value if the key not exists in dict. Defaults to None.

    Returns:
        Any: Any
    """
    if dictionary is None or key is None: return fall_back_value
    return dictionary[key] if key in dictionary else fall_back_value


def proper_round(num):
    abs_value = abs(num)
    if abs_value - int(abs_value) >= 0.5:
        return int(num) + 1 if num > 0 else int(num) - 1
    return int(num)


def traverse_shop(shop, lookup_key: str = None, lookup_attribute: str = "marketplaceItemdefId") -> bool:
    if isinstance(shop, list):
        for techtree in shop:
            if traverse_shop(techtree, lookup_key, lookup_attribute):
                return True
    elif isinstance(shop, dict):
        for key in shop:
            if key != "image" and key != "reqAir":
                if "_group" not in key:
                    try:
                        if key == lookup_key and value_from_dict(shop[key], lookup_attribute) is not None:
                            return True
                    except KeyError:
                        pass
                if "_group" in key:
                    if traverse_shop(shop[key], lookup_key, lookup_attribute):
                        return True
    return False


def get_type_key(vehicle_type):
    type_key_mapping = {
        'fighter': 'aviation',
        'assault': 'aviation',
        'bomber': 'aviation',
        'attack_helicopter': 'helicopters',
        'utility_helicopter': 'helicopters',

        'tank': 'army',
        'light_tank': 'army',
        'medium_tank': 'army',
        'heavy_tank': 'army',
        'tank_destroyer': 'army',
        'spaa': 'army',
        'lbv': 'army',
        'mbv': 'army',
        'hbv': 'army',
        'exoskeleton': 'army',

        'ship': 'ships',
        'light_cruiser': 'ships',
        'frigate': 'ships',
        'heavy_cruiser': 'ships',
        'battlecruiser': 'ships',
        'destroyer': 'ships',
        'submarine': 'ships',
        'battleship': 'ships'
    }
    type_key_mapping.update({ground_type: 'army' for ground_type in ['light_tank', 'medium_tank', 'heavy_tank', 'tank_destroyer', 'spaa']})

    return type_key_mapping.get(vehicle_type, 'boats')


def is_vehicle_on_marketplace(shop, identifier, country, vehicle_type) -> bool:
    country_key = "country_" + country
    type_key = get_type_key(vehicle_type)
    return traverse_shop(shop[country_key][type_key]["range"], identifier)


def is_squadron_vehicle(shop, identifier, country, vehicle_type) -> bool:
    country_key = "country_" + country
    type_key = get_type_key(vehicle_type)
    return traverse_shop(shop[country_key][type_key]["range"], identifier, "isClanVehicle")


def is_pack(shop, identifier, country, vehicle_type) -> bool:
    country_key = "country_" + country
    type_key = get_type_key(vehicle_type)
    return traverse_shop(shop[country_key][type_key]["range"], identifier, "gift")
