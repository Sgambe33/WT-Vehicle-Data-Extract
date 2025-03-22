from wt_vehicle_extractor_sgambe33.classes.Vehicle import Vehicle


def create_vehicle(vehicle_id:str)->Vehicle | None:
    """Create a single vehicle.

    Keyword arguments:
        vehicle_id -- The id of the vehicle you want to extract. If not sure, check the game wiki.
    """
    pass


def create_all_vehicles(multithread:bool, verbose:bool)->list[Vehicle]:
    """Extracts all vehicles from the game.

    Keyword arguments:
        multithread -- If set to true the script will try to create multiple vehicles at the same time to reduce execution time. 
        verbose -- If set to true, progress bars will be displayed along with eventual errors or warnings.
    """
    pass


def extract_all_images(path:str)->None:
    """Extracts all vehicles, techtree, modifications and weapons images.

    Keyword arguments:
        path -- The folder where to put all images organized in folders. 
    """
    pass


def extract_localization(path:str)->None:
    """Extracts vehicles, modifications, guns and ammos localization.

    Keyword arguments:
        path -- The folder where to put the JSON files with localization. 
    """
    pass


def execute_full_extract(use_db: bool, save_diffs: bool)->None:
    """Execute a full extract run.

    Keyword arguments:
        use_db -- If set to false all data will be saved in JSON files. If set to true a sqlite db will be created.
        save_diffs -- If set to true it will override use_db parameter and create a sqlite db to also track vehicle changes between game versions. 
    """
    pass
