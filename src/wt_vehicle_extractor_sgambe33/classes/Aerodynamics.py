from pydantic import BaseModel

class Aerodynamics(BaseModel):
    length: float = 0.0
    wingspan: float = 0.0
    wing_area: float = 0.0
    empty_weight: int = 0
    max_takeoff_weight: int = 0
    max_altitude: int = 0
    turn_time: int = 0
    runway_length_required: int = 0
    max_speed_at_altitude: int = 0

    def __str__(self):
        return f"Aerodynamics: {self.length} m, {self.wingspan} m, {self.wing_area} m^2, {self.empty_weight} kg, {self.max_takeoff_weight} kg, {self.max_altitude} m, {self.turn_time} s, {self.runway_length_required} m, {self.max_speed_at_altitude} km/h"

    def toJson(self):
        return self.model_dump_json()
