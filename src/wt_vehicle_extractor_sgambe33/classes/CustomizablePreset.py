from pydantic import BaseModel, Field
from typing import List
from src.wt_vehicle_extractor_sgambe33.classes.Pylon import Pylon


class CustomizablePreset(BaseModel):
    max_load: int = 0
    max_load_left_wing: int = 0
    max_load_right_wing: int = 0
    max_disbalance: int = 0
    pylons: List[Pylon] = Field(default_factory=list)

    def __str__(self):
        return f"Custom preset: {self.max_load}, {self.max_load_left_wing}, {self.max_load_right_wing}, {self.max_disbalance}, {self.pylons}"

    def toJson(self):
        return self.model_dump_json()
