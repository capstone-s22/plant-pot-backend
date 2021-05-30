import time
from datetime import datetime as dt
import json
import base64
import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_CRED = "credentials/plant-pot-firebase-admin.json"

def get_firebase_credentials():
    if os.path.exists(FIREBASE_CRED) and os.path.isfile(FIREBASE_CRED):
        print("Credentials JSON file found")
        return FIREBASE_CRED
    else:
        print("Credentials JSON file not found.")
        encoded_cred = os.getenv('FIREBASE_CRED_ENCODED')
        if encoded_cred != None:
            print("Credentials env var found")

            decoded_cred = json.loads(base64.b64decode(encoded_cred))
            return decoded_cred
        else:
            raise Exception("'FIREBASE_CRED_ENCODED' env var undefined.")

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

def getCurrentTime():
    return dt_float2str(time.time())


pot_id = "ID"
ambient_temp =  "AmbientTemperature"
nutrient_level =  "NutrientLevel"
green_point_score =  "GreenPointScore"
water_level =  "WaterLevel"
is_plant_healthy =  "IsPlantHealthy"
pot_registered_time = "PotRegisteredTime"
to_ring = "ToRing"

def create_new_pot_schema(id):
    new_pot_schema = {
            pot_id: id,
            ambient_temp: False, 
            nutrient_level: {},
            green_point_score: {}, 
            water_level: {}, 
            is_plant_healthy: {}, 
            pot_registered_time: getCurrentTime(), 
            to_ring: False, 
        }

    return new_pot_schema

def update_parameter_schema(field, value):
    current_time = getCurrentTime() # NOTE: If Pot sends datetime in the form of integer, then just convert
    parameter_schema = {}
    parameter_schema["{}.{}".format(field, current_time)] = value

    return parameter_schema