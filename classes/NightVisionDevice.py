class NightVisionDevice:
    def __init__(self):
        #For tanks
        self.commander_device: str = None
        self.driver_device: str = None

        #For air units
        self.pilot_device: str = None
        self.sight_device: str = None
        self.targeting_pod_device: str = None

        #Common
        self.gunner_device: str = None

    def __str__(self) -> str:
        return f"NigthVisionDevice(commander_device={self.commander_device}, driver_device={self.driver_device}, pilot_device={self.pilot_device}, sight_device={self.sight_device}, targeting_pod_device={self.targeting_pod_device}, gunner_device={self.gunner_device})"

    def is_all_null(self) -> bool:
        return all(value is None for value in self.__dict__.values())

    def toJson(self):
        return {
            "commander_device": self.commander_device,
            "driver_device": self.driver_device,
            "pilot_device": self.pilot_device,
            "sight_device": self.sight_device,
            "targeting_pod_device": self.targeting_pod_device,
            "gunner_device": self.gunner_device
        }
