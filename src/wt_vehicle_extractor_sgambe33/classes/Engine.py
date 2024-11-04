from pydantic import BaseModel


class Engine(BaseModel):
    horse_power_ab: int = 0
    horse_power_rb_sb: int = 0
    max_rpm: int = 0
    min_rpm: int = 0
    max_speed_ab: int = 0
    max_reverse_speed_ab: int = 0
    max_speed_rb_sb: int = 0
    max_reverse_speed_rb_sb: int = 0

    def __str__(self):
        return (f"Engine: {self.horse_power_ab} HP (AB), {self.horse_power_rb_sb} HP (RB/SB), "
                f"{self.max_rpm} RPM, {self.min_rpm} RPM, {self.max_speed_ab} km/h (AB), "
                f"{self.max_reverse_speed_ab} km/h (AB), {self.max_speed_rb_sb} km/h (RB/SB), "
                f"{self.max_reverse_speed_rb_sb} km/h (RB/SB)")

    def toJson(self):
        return self.model_dump_json()
