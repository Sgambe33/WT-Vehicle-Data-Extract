class Aerodynamics:
    def __init__(self, ):
        self.length: float = 0.0
        self.wingspan: float = 0.0
        self.wing_area: float = 0.0
        self.empty_weight: int = 0
        self.max_takeoff_weight: int = 0
        self.max_altitude: int = 0
        self.turn_time: int = 0
        self.runway_length_required: int = 0
        self.max_speed_at_altitude: int = 0

    def __str__(self):
        return f"Aerodynamics: {self.length} m, {self.wingspan} m, {self.wing_area} m^2, {self.empty_weight} kg, {self.max_takeoff_weight} kg, {self.max_altitude} m, {self.turn_time} s, {self.runway_length_required} m, {self.max_speed_at_altitude} km/h"

    def toJson(self):
        return {
            "length": self.length,
            "wingspan": self.wingspan,
            "wing_area": self.wing_area,
            "empty_weight": self.empty_weight,
            "max_takeoff_weight": self.max_takeoff_weight,
            "max_altitude": self.max_altitude,
            "turn_time": self.turn_time,
            "runway_length_required": self.runway_length_required,
            "max_speed_at_altitude": self.max_speed_at_altitude
        }
