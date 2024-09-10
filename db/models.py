from peewee import *
import os
#from playhouse.sqlite_ext import JSONField
from playhouse.postgres_ext import JSONField

# db = SqliteDatabase('testing.sqlite3', pragmas={
#     'journal_mode': 'wal',
#     'cache_size': -1024 * 64})

db = PostgresqlDatabase('vehiclesdb', user=os.environ.get("XATA_USER", "<unknown"), password=os.environ.get("XATA_API_KEY", "<unknown"), host='eu-central-1.sql.xata.sh', port=5432)

class BaseModel(Model):
    class Meta:
        database = db


class Vehicle(BaseModel):
    identifier = TextField(primary_key=True)
    country = TextField()
    vehicle_type = TextField()
    vehicle_sub_types = JSONField(null=True, default=[])
    event = TextField(null=True)
    release_date = TextField(null=True)
    version = TextField()
    era = IntegerField()
    arcade_br = FloatField()
    realistic_br = FloatField()
    realistic_ground_br = FloatField()
    simulator_br = FloatField()
    simulator_ground_br = FloatField()
    value = IntegerField()
    req_exp = IntegerField()
    is_premium = BooleanField(default=False)
    is_pack = BooleanField(default=False)
    on_marketplace = BooleanField(default=False)
    squadron_vehicle = BooleanField(default=False)
    ge_cost = IntegerField()
    crew_total_count = IntegerField()
    visibility = IntegerField()
    hull_armor = JSONField(null=True, default=[])
    turret_armor = JSONField(null=True, default=[])
    mass = FloatField()
    train1_cost = IntegerField()
    train2_cost = IntegerField()
    train3_cost_gold = IntegerField()
    train3_cost_exp = IntegerField()
    sl_mul_arcade = FloatField()
    sl_mul_realistic = FloatField()
    sl_mul_simulator = FloatField()
    exp_mul = FloatField()
    repair_time_arcade = FloatField()
    repair_time_realistic = FloatField()
    repair_time_simulator = FloatField()
    repair_time_no_crew_arcade = FloatField()
    repair_time_no_crew_realistic = FloatField()
    repair_time_no_crew_simulator = FloatField()
    repair_cost_arcade = IntegerField()
    repair_cost_realistic = IntegerField()
    repair_cost_simulator = IntegerField()
    repair_cost_per_min_arcade = IntegerField()
    repair_cost_per_min_realistic = IntegerField()
    repair_cost_per_min_simulator = IntegerField()
    repair_cost_full_upgraded_arcade = IntegerField()
    repair_cost_full_upgraded_realistic = IntegerField()
    repair_cost_full_upgraded_simulator = IntegerField()
    required_vehicle = TextField(null=True)
    engine = JSONField(null=True, default={})
    modifications = JSONField(null=True, default={})
    ir_devices = JSONField(null=True, default={})
    thermal_devices = JSONField(null=True, default={})
    ballistic_computer = JSONField(null=True, default={})
    aerodynamics = JSONField(null=True, default={})
    has_customizable_weapons = BooleanField()
    weapons = JSONField(null=True, default=[])
    presets = JSONField(null=True, default=[])
    customizable_presets = JSONField(null=True, default=False)
    
    class Meta:
        database = db
        db_table = 'vehicle'


class VehicleOld(BaseModel):
    identifier = TextField()
    country = TextField()
    vehicle_type = TextField()
    vehicle_sub_types = JSONField(null=True, default=[])
    event = TextField(null=True)
    release_date = TextField(null=True)
    version = TextField()
    era = IntegerField()
    arcade_br = FloatField()
    realistic_br = FloatField()
    realistic_ground_br = FloatField()
    simulator_br = FloatField()
    simulator_ground_br = FloatField()
    value = IntegerField()
    req_exp = IntegerField()
    is_premium = BooleanField(default=False)
    is_pack = BooleanField(default=False)
    on_marketplace = BooleanField(default=False)
    squadron_vehicle = BooleanField(default=False)
    ge_cost = IntegerField()
    crew_total_count = IntegerField()
    visibility = IntegerField()
    hull_armor = JSONField(null=True, default=[])
    turret_armor = JSONField(null=True, default=[])
    mass = FloatField()
    train1_cost = IntegerField()
    train2_cost = IntegerField()
    train3_cost_gold = IntegerField()
    train3_cost_exp = IntegerField()
    sl_mul_arcade = FloatField()
    sl_mul_realistic = FloatField()
    sl_mul_simulator = FloatField()
    exp_mul = FloatField()
    repair_time_arcade = FloatField()
    repair_time_realistic = FloatField()
    repair_time_simulator = FloatField()
    repair_time_no_crew_arcade = FloatField()
    repair_time_no_crew_realistic = FloatField()
    repair_time_no_crew_simulator = FloatField()
    repair_cost_arcade = IntegerField()
    repair_cost_realistic = IntegerField()
    repair_cost_simulator = IntegerField()
    repair_cost_per_min_arcade = IntegerField()
    repair_cost_per_min_realistic = IntegerField()
    repair_cost_per_min_simulator = IntegerField()
    repair_cost_full_upgraded_arcade = IntegerField()
    repair_cost_full_upgraded_realistic = IntegerField()
    repair_cost_full_upgraded_simulator = IntegerField()
    required_vehicle = TextField(null=True)
    engine = JSONField(null=True, default={})
    modifications = JSONField(null=True, default={})
    ir_devices = JSONField(null=True, default={})
    thermal_devices = JSONField(null=True, default={})
    ballistic_computer = JSONField(null=True, default={})
    aerodynamics = JSONField(null=True, default={})
    has_customizable_weapons = BooleanField()
    weapons = JSONField(null=True, default=[])
    presets = JSONField(null=True, default=[])
    customizable_presets = JSONField(null=True, default=False)

    class Meta:
        database = db
        db_table = 'vehicleold'
        primary_key = CompositeKey('identifier', 'version')