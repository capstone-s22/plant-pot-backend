import time
from datetime import datetime as dt

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

# TODO: change to simpler method: https://stackoverflow.com/questions/19825330/python-how-to-convert-ctime-to-m-d-y-hms
def dt_float2str(timeDate: float):
    if type(timeDate) == float:
        timeDate = dt.strptime(
            time.ctime(int(timeDate)), "%a %b %d %H:%M:%S %Y"
        ).strftime("%d/%m/%Y %H:%M:%S")

    return timeDate


def dt_str2float(dt_string):
    # TODO: validate datetime string format
    # Sample string value: '04/11/2020 16:30:35'
    if dt_string != "":
        dt_float = dt.strptime(dt_string, "%d/%m/%Y %H:%M:%S").timestamp()
        return dt_float
    else:
        return dt_string

def getCurrentTimeStr():
    return dt_float2str(time.time())

def getCurrentTime():
    return int(time.time())

pot_id = "ID"
ambient_temp =  "Temperature"
nutrient_level =  "NutrientLevel"
green_point_score =  "GreenPointScore"
water_level =  "WaterLevel"
is_plant_healthy =  "IsPlantHealthy"
pot_registered_time = "PotRegisteredTime"
to_ring = "ToRing"

def create_new_pot_schema(id):
    new_pot_schema = {
            pot_id: id,
            ambient_temp: None, 
            nutrient_level: None,
            green_point_score: None, 
            water_level: None, 
            is_plant_healthy: None, 
            pot_registered_time: getCurrentTime(), 
            to_ring: False, 
        }

    return new_pot_schema

def update_parameter_schema(param_name, param_value):
    parameter_schema = {}
    parameter_schema["{}".format(param_name)] = param_value

    return parameter_schema

def append_parameter_schema(param_name, param_value):
    current_time = getCurrentTime() # NOTE: If Pot sends datetime in the form of integer, then just convert
    parameter_schema = {}
    parameter_schema["{}.{}".format(param_name, current_time)] = param_value

    return parameter_schema

