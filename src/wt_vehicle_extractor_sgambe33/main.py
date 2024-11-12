import time
import traceback
from os import path
#from db.inserter import update_db
from utils import *
from utils.constants import *
 #from utils.update_localization import generate_locales
from utils.updater import update_dataset, update_images
from dotenv import load_dotenv
from threading import Thread

load_dotenv(".env")


def get_vehicle_by_country(country, fetch_uri, file_in_path, vehicle_type="VEHICLE", verbose=False):
    all_vehicles = my_fetch(path.join("./generatedAssets/nations", country, file_in_path))

    if all_vehicles is None:
        if verbose: cLogger.warning(f'{vehicle_type.upper()} doesn\'t have a file called {file_in_path}')
        return
    out_file = path.join("./generatedAssets/nations", country, f"{country}Final{vehicle_type}s.json")

    final_vehicles = []
    for index, vehicle in enumerate(all_vehicles):
        if verbose: cLogger.info(f'{index:2} -> {country.upper()}  {vehicle_type.upper()}  {vehicle}')
        try:
            vehicle = create_vehicle(vehicle, fetch_uri)
            if vehicle is None:
                continue
            final_vehicles.append(vehicle)
        except Exception as e:
            cLogger.error(f'Error creating {vehicle_type} {vehicle} -> {e}')
            return

    with open(out_file, 'wb') as f:
        f.write(orjson.dumps([o.toJson() for o in final_vehicles], option=orjson.OPT_INDENT_2))


def process_country(nation, verbose):
    get_vehicle_by_country(nation, VEHICLE_FETCH_URI['ground'], f'country_{nation}_ground.json', 'Tank', verbose)
    get_vehicle_by_country(nation, VEHICLE_FETCH_URI['sea'], f'country_{nation}_sea.json', 'Ship', verbose)
    get_vehicle_by_country(nation, VEHICLE_FETCH_URI['air'], f'country_{nation}_air.json', 'Aircraft', verbose)


def main(verbose: bool = False, use_multithreading: bool = True):
    if use_multithreading:
        threads = []
        for nation in COUNTRIES:
            t = Thread(target=process_country, args=(nation, verbose))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    else:
        for nation in COUNTRIES:
            process_country(nation, verbose)


if __name__ == '__main__':
    update_dataset()
    # TODO: Fix localization for weaponry when using multiprocessing
    start_time = time.time()
    main(verbose=True, use_multithreading=True)
    print(f"--- {time.time() - start_time} seconds ---")
    #update_db()
    #update_images()
    #generate_locales()
