from models.Sensor import SensorType, Sensor, Sensors, SensorIndicatorRange
import aiohttp
from attr import field
import os
from datetime import datetime

from models.Plant import Plant, GrowthStage, Plants
from models.Pot import Pot
from models.Sensor import Sensor
from lib.custom_logger import logger

CV_SERVER_URL_PREFIX = os.getenv('CV_SERVER_URL_PREFIX')
# CV_SERVER_URL_PREFIX = "http://localhost:3002/cv"

#TODO: Add more rules to ensure users dont cheat and iterate the harvest rewards
async def cv_inference(pot_id, encoded_img_data):
    if CV_SERVER_URL_PREFIX == None:
        raise Exception("CV_SERVER_URL_PREFIX not set")
    data = { "potId": pot_id, "encoded_data": encoded_img_data }
    async with aiohttp.request(method='GET', url=CV_SERVER_URL_PREFIX, json=data) as resp:
        if resp.status == 200:
            response = await resp.json()
            
            for ring_colour in response:
                try:
                    Plant.parse_obj(response[ring_colour]) # Validate data with model
                except Exception as e:
                    raise Exception("CV server's response validation error")
            return response
        else:
            response = await resp.json()
            logger.error("Respose status={}, response={}".format(resp.status, response))
            raise Exception("Something went wrong in CV Server")

def is_seed(dt2: datetime, dt1: datetime):
    return (dt2 - dt1).days == 0 # Day 1

def is_sprouting(growth_stage: GrowthStage, dt2: datetime, dt1: datetime):
    # Day 2 onwards until leaves can be seen in seedling stage onwards
    return ((dt2 - dt1).days >= 1 
            and (growth_stage == GrowthStage.seed or growth_stage == GrowthStage.sprouting))
            

# NOTE: Function to revise plant growth stages based on hardcoded features (not entirely relying on CV output)
def revise_plants_status(current_pot: Pot, new_plants_status: dict):
    revised_plants_status = {}
    new_plants_objs: Plants = Plants.parse_obj(new_plants_status)
    old_plants_objs: Plants = current_pot.session.plants

    # Fields are ordered https://pydantic-docs.helpmanual.io/usage/models/#field-ordering
    for old_plant_tuple, new_plant_tuple in zip(old_plants_objs, new_plants_objs):
        old_plant: Plant = old_plant_tuple[1]
        new_plant: Plant = new_plant_tuple[1]
        ring_colour = old_plant.ringColour

        # NOTE: After harvest, slot will be empty so None. For UT, no new seeds after harvest, so keep it at None
        # TODO: Ideally to remove this once UI allows users to indicate to plant new seed
        if old_plant.growthStage == None:
            new_plant = Plant(growthStage=None, ringColour=new_plant.ringColour)

        # TODO: Future work: start time of seed planting based on user indication in app, not session start time
        # NOTE: Add replace(tzinfo=None) to avoid error "can't subtract offset-naive and offset-aware datetimes"
        
        # NOTE: Temporarily removing them for UT 
        # elif is_seed(datetime.utcnow(), current_pot.session.sessionStartTime.replace(tzinfo=None)):
        #     new_plant.growthStage = GrowthStage.seed

        # NOTE: Temporarily removing them for UT 
        # elif is_sprouting(new_plant.growthStage, datetime.utcnow(), current_pot.session.sessionStartTime.replace(tzinfo=None)):
        #     new_plant.growthStage = GrowthStage.sprouting
        
        else:
            logger.info("No revision to plants status needed")

        revised_plants_status[ring_colour] = new_plant.dict()
    return revised_plants_status

def to_show_trim(new_plants_status):
    after_check_trim_status = {}
    for ring_colour in new_plants_status:
        if new_plants_status[ring_colour] == None:
            plant = None
        else:
            plant = Plant.parse_obj(new_plants_status[ring_colour])
            if plant.yellowness.value > 0.3:
                plant.yellowness.toShowTrim = True
        after_check_trim_status[ring_colour] = plant.dict() if plant != None else plant
            
    return after_check_trim_status

def harvest_ready(new_plants_status: dict):
    for ring_colour in new_plants_status:
        plant = Plant.parse_obj(new_plants_status[ring_colour])
        if plant.growthStage ==  GrowthStage.harvest:
            # As long as there is harvest stage for any plant inform
            return True
    return False

def is_harvested(old_plant_obj: Plant, new_plant_obj: Plant):
    # NOTE: since currently seed and sprout hard to be differentiated
    return (old_plant_obj.growthStage == GrowthStage.harvest 
            and (new_plant_obj.growthStage == GrowthStage.seed or new_plant_obj.growthStage == GrowthStage.sprouting)) 

#TODO: Make a function for converting from new_plants_status to dictionary of plants and back and forth
def get_harvests_completed(current_pot: Pot, new_plants_status: dict):
    harvest_count = 0
    after_harvest_plants_status = {}
    new_plants_objs: Plants = Plants.parse_obj(new_plants_status)
    old_plants_objs: Plants = current_pot.session.plants

    # Fields are ordered https://pydantic-docs.helpmanual.io/usage/models/#field-ordering
    for old_plant_tuple, new_plant_tuple in zip(old_plants_objs, new_plants_objs):
        old_plant: Plant = old_plant_tuple[1]
        new_plant: Plant = new_plant_tuple[1]
        ring_colour = old_plant.ringColour

        if is_harvested(old_plant, new_plant):
            # NOTE: After harvest, slot will be empty so None, since CV can't differentiate null, seed and sprout
            new_plant = Plant(growthStage=None, ringColour=new_plant.ringColour)
            harvest_count += 1
        after_harvest_plants_status[ring_colour] = new_plant.dict()

    return harvest_count, after_harvest_plants_status

def is_water_level_unhealthy(water_level_value: int):
    if water_level_value == 0:
        return True, SensorIndicatorRange.low
    else:
        return False, SensorIndicatorRange.medium

def is_nutrient_level_unhealthy(nutrient_level_value: float):
    if nutrient_level_value < 1.0:
        return True, SensorIndicatorRange.low
    else:
        return False, SensorIndicatorRange.medium

def is_temperature_unhealthy(temp_value: float):

    if temp_value < 20.0:
        return True, SensorIndicatorRange.low
    elif temp_value > 31.0:
        return True, SensorIndicatorRange.high
    else:
        return False, SensorIndicatorRange.medium

def is_sensor_remedy_needed(sensor_type: SensorType, sensor_value): 
    if sensor_type == SensorType.nutrient_level:
        return is_nutrient_level_unhealthy(sensor_value)
    elif sensor_type == SensorType.water_level:
        return is_water_level_unhealthy(sensor_value)
    elif sensor_type == SensorType.temperature:
        return is_temperature_unhealthy(sensor_value)
    else:
        return None, None
    
def is_remedy_performed(sensor_type: SensorType, last_pot_obj: Pot):
    last_sensor_alert_status = None
    last_sensors_obj: Sensors = last_pot_obj.session.sensors
    # TODO: Cuurrently have to loop through all sensors to find the sensor type. Improve this if possible
    for sensor_tuple in last_sensors_obj:
        sensor: Sensor = sensor_tuple[1]
        if sensor.type == sensor_type:
            last_sensor_alert_status = sensor.toAlert

    # TODO: Remove this once sensortype is checked in MessageFromPot
    if last_sensor_alert_status == None:
        raise Exception("Sensor type invalid")

    return last_sensor_alert_status # sensor value remedied, hence alert from True to False