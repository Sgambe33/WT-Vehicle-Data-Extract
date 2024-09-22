class Engine:
    def __init__(self):
        self.horse_power_ab: int = 0
        self.horse_power_rb_sb: int = 0
        self.max_rpm: int = 0
        self.min_rpm: int = 0
        self.max_speed_ab: int = 0
        self.max_reverse_speed_ab: int = 0
        self.max_speed_rb_sb: int = 0
        self.max_reverse_speed_rb_sb: int = 0

    def __str__(self):
        return (f"Engine: {self.horse_power_ab} HP (AB), {self.horse_power_rb_sb} HP (RB/SB), "
                f"{self.max_rpm} RPM, {self.min_rpm} RPM, {self.max_speed_ab} km/h (AB), "
                f"{self.max_reverse_speed_ab} km/h (AB), {self.max_speed_rb_sb} km/h (RB/SB), "
                f"{self.max_reverse_speed_rb_sb} km/h (RB/SB)")

    def toJson(self):
        return {
            "horse_power_ab": self.horse_power_ab,
            "horse_power_rb_sb": self.horse_power_rb_sb,
            "max_rpm": self.max_rpm,
            "min_rpm": self.min_rpm,
            "max_speed_ab": self.max_speed_ab,
            "max_reverse_speed_ab": self.max_reverse_speed_ab,
            "max_speed_rb_sb": self.max_speed_rb_sb,
            "max_reverse_speed_rb_sb": self.max_reverse_speed_rb_sb
        }
