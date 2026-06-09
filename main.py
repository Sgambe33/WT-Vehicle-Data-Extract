import asyncio
from os import path
from tqdm import tqdm

from db.inserter import update_db
from utils import *
from utils.constants import *
from utils.update_localization import generate_locales
from utils.updater import update_dataset, update_images

MAX_CONCURRENT_REQUESTS = 20
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


def get_file_path(country, filename):
    return path.join(".", "nations", country, filename)


async def process_vehicle_async(vehicle, fetch_uri, vehicle_type, pbar):
    """
    Wraps the blocking create_vehicle call.
    Updates the pbar immediately after the specific task finishes.
    """
    async with semaphore:
        try:
            result = await asyncio.to_thread(create_vehicle, vehicle, fetch_uri)
        except Exception as e:
            cLogger.error(f'Error creating {vehicle_type} {vehicle} -> {e}', exc_info=True)
            result = None
        finally:
            if pbar:
                pbar.update(1)

        return result


async def get_vehicle_by_country_async(country, fetch_uri, file_in_path, vehicle_type, pbar, verbose=False):
    in_file = get_file_path(country, file_in_path)
    if not path.exists(in_file):
        if verbose: cLogger.warning(f'{vehicle_type.upper()} missing file {file_in_path}')
        return

    all_vehicles = getJson(in_file)
    if not all_vehicles:
        return

    # Create tasks for this country/type
    tasks = []
    for vehicle in all_vehicles:
        tasks.append(process_vehicle_async(vehicle, fetch_uri, vehicle_type, pbar))

    # Wait for this specific batch to finish so we can save the file
    results = await asyncio.gather(*tasks)

    final_vehicles = [res for res in results if res is not None]

    out_file = path.join(".", "nations", country, f"{country}Final{vehicle_type}s.json")
    with open(out_file, 'w') as f:
        json.dump([o.toJson() for o in final_vehicles], f, indent=2)


async def process_country_async(nation, pbar, verbose):
    await asyncio.gather(
        get_vehicle_by_country_async(nation, VEHICLE_FETCH_URI['air'], f'country_{nation}_air.json', 'Aircraft', pbar,
                                     verbose),
        get_vehicle_by_country_async(nation, VEHICLE_FETCH_URI['ground'], f'country_{nation}_ground.json', 'Tank', pbar,
                                     verbose),
        get_vehicle_by_country_async(nation, VEHICLE_FETCH_URI['sea'], f'country_{nation}_sea.json', 'Ship', pbar,
                                     verbose)
        )


def count_total_items():
    total = 0
    types = [
        f'country_{{}}_air.json',
        f'country_{{}}_ground.json',
        f'country_{{}}_sea.json'
    ]

    cLogger.info("Counting total vehicles to process...")
    for nation in COUNTRIES:
        for file_template in types:
            fname = get_file_path(nation, file_template.format(nation))
            if path.exists(fname):
                try:
                    with open(fname, 'r') as f:
                        data = json.load(f)
                        if data:
                            total += len(data)
                except:
                    pass
    return total


async def main_async(verbose: bool = False):
    total_vehicles: int = await asyncio.to_thread(count_total_items)
    cLogger.info(f"Starting processing for approximately {total_vehicles} vehicles.")
    with tqdm(total=total_vehicles, unit="vehicle", desc="Processing") as pbar:
        tasks = [process_country_async(nation, pbar, verbose) for nation in COUNTRIES]
        await asyncio.gather(*tasks)

def main(verbose: bool = False):
    asyncio.run(main_async(verbose))


if __name__ == '__main__':
    update_dataset()
    main(verbose=False)

    update_db(verbose=False) # better to not parallelize due to database locking...
    update_images()
    generate_locales("./locales")
