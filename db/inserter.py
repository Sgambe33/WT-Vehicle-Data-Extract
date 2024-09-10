import json
from deepdiff import DeepDiff
from peewee import DoesNotExist, chunked
from playhouse.shortcuts import model_to_dict
from tqdm import tqdm
from dotenv import load_dotenv

from utils import cLogger
from .models import db, Vehicle, VehicleOld

COUNTRY_LIST = ["britain", "china", "france", "germany", "israel", "italy", "japan", "sweden", "usa", "ussr"]

load_dotenv()

def create_tables():
    db.create_tables([Vehicle, VehicleOld])

def update_db():
    for country in COUNTRY_LIST:
        cLogger.info(f'Updating {country}')
        for vehicle_category in ['Aircrafts', 'Tanks', 'Ships']:
            try:
                with open(f'nations/{country}/{country}Final{vehicle_category}.json', 'r') as file:
                    vehicles_data = json.load(file)
                    new_vehicles = []
                    for vehicle_data in tqdm(vehicles_data):
                        current_version = vehicle_data.pop('version')

                        try:
                            db_vehicle = Vehicle.get(Vehicle.identifier == vehicle_data['identifier'])
                            db_vehicle_dict = model_to_dict(db_vehicle)
                            db_version = db_vehicle_dict.pop('version')

                            diff = DeepDiff(db_vehicle_dict, vehicle_data, ignore_order=True)
                            if len(diff.items()) > 0:

                                if current_version.split('.')[0] >= db_version.split('.')[0] and current_version.split('.')[1] > db_version.split('.')[1]:
                                    # Put old vehicle in VehicleOld table
                                    db_vehicle_dict['version'] = db_version
                                    VehicleOld.create(**db_vehicle_dict)
                                    db_vehicle.delete_instance()

                                    # Save the new vehicle in Vehicle table
                                    vehicle_data["version"] = current_version
                                    new_vehicles.append(vehicle_data)
                                else:
                                    cLogger.info(f'{vehicle_data["identifier"]} version updated: {db_version} --> {current_version}')
                                    for key, value in vehicle_data.items():
                                        setattr(db_vehicle, key, value)
                                    db_vehicle.version = current_version
                                    db_vehicle.save()
                            else:
                                db_vehicle.version = current_version
                                db_vehicle.save()
                        except DoesNotExist:
                            vehicle_data["version"] = current_version
                            new_vehicles.append(vehicle_data)

                    with db.atomic():
                        for vehicles in chunked(new_vehicles, 100):
                            Vehicle.insert_many(vehicles).execute()
            except FileNotFoundError:
                pass