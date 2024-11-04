from pydantic import BaseModel
from typing import Optional


class NightVisionDevice(BaseModel):
    commander_device: Optional[str] = None
    driver_device: Optional[str] = None
    pilot_device: Optional[str] = None
    sight_device: Optional[str] = None
    targeting_pod_device: Optional[str] = None
    gunner_device: Optional[str] = None

    def __str__(self) -> str:
        return (f"NightVisionDevice(commander_device={self.commander_device}, driver_device={self.driver_device}, "
                f"pilot_device={self.pilot_device}, sight_device={self.sight_device}, "
                f"targeting_pod_device={self.targeting_pod_device}, gunner_device={self.gunner_device})")

    def is_all_null(self) -> bool:
        return all(value is None for value in self.__dict__.values())

    def toJson(self):
        return self.model_dump_json()
