from multiprocessing import Process
from os import path
import time
from db.inserter import update_db
from utils import *
from utils.constants import *
from utils.update_localization import generate_locales
from utils.updater import update_dataset, update_images, updates_available
from dotenv import load_dotenv

load_dotenv("/utils/.env")


def get_vehicle_by_country(country, fetch_uri, file_in_path, vehicle_type="VEHICLE", verbose=False):
    all_vehicles = getJson(path.join(".", "nations", country, file_in_path))

    if all_vehicles is None:
        if verbose: cLogger.warning(f'{vehicle_type.upper()} doesn\'t have a file called {file_in_path}')
        return
    out_file = path.join(".", "nations", country, f"{country}Final{vehicle_type}s.json")

    final_vehicles = []
    for index, vehicle in enumerate(all_vehicles):
        if verbose: cLogger.info(f'{index:2} -> {country.upper()}  {vehicle_type.upper()}  {vehicle}') 
        try:
            vehicle = create_vehicle(vehicle, fetch_uri)
            if vehicle is None:
                continue
            final_vehicles.append(vehicle)
        except Exception as e:
            e.with_traceback()
            cLogger.error(f'Error creating {vehicle_type} {vehicle} -> {e.with_traceback()}')
            continue

    with open(out_file, 'w') as f:
        json.dump([o.toJson() for o in final_vehicles], f, indent=2)


def process_country(nation, verbose):
    get_vehicle_by_country(nation, VEHICLE_FETCH_URI['ground'], f'country_{nation}_ground.json', 'Tank', verbose)
    get_vehicle_by_country(nation, VEHICLE_FETCH_URI['sea'], f'country_{nation}_sea.json', 'Ship', verbose)
    get_vehicle_by_country(nation, VEHICLE_FETCH_URI['air'], f'country_{nation}_air.json', 'Aircraft', verbose)


def main(verbose: bool = False, use_multiprocessing: bool = True):
    if use_multiprocessing:
        processes = []
        for nation in COUNTRIES:
            p = Process(target=process_country, args=(nation, verbose))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
    else:
        for nation in COUNTRIES:
            process_country(nation, verbose)

if __name__ == '__main__':
    # if not updates_available():
    #     cLogger.info("No updates available")
    #     exit(0)
    # else:
        cLogger.info("Updates available")
        update_dataset()
        main(verbose=True, use_multiprocessing=True)
        #update_db()
        #update_images()
        #generate_locales("./locales")