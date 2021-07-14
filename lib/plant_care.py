from models.Sensor import SensorType
import aiohttp
from attr import field
import os
from typing import Dict, Union
from datetime import datetime

from models.Plant import Plant, RingColour, GrowthStage
from models.Pot import Pot
from models.Sensor import Sensor

CV_SERVER_URL_PREFIX = os.getenv('CV_SERVER_URL_PREFIX')
# CV_SERVER_URL_PREFIX = "http://localhost:3002/cv"

#TODO: Add more rules to ensure users dont cheat and iterate the harvest rewards
async def cv_inference(pot_id, encoded_img_data):
    if CV_SERVER_URL_PREFIX == None:
        raise Exception("CV_SERVER_URL_PREFIX not set")
    data = { "potId": pot_id, "encoded_data": encoded_img_data }
    async with aiohttp.request(method='GET', url=CV_SERVER_URL_PREFIX, json=data) as resp:
        assert resp.status == 200
        response = await resp.json()
        for ring_colour in response:
            try:
                Plant.parse_obj(response[ring_colour]) # Validate data with model
            except Exception as e:
                raise Exception("CV server's response validation error")
        return response

def is_seed(dt2: datetime, dt1: datetime):
    return (dt2 - dt1).days == 0 # Day 1

def is_sprouting(growth_stage: GrowthStage, dt2: datetime, dt1: datetime):
    # Day 2 onwards until leaves can be seen in seedling stage onwards
    return ((dt2 - dt1).days >= 1 
            and (growth_stage == GrowthStage.seed or growth_stage == GrowthStage.sprouting))
            

# NOTE: Function to revise plant growth stages based on hardcoded features (not entirely relying on CV output)
def revise_plants_status(current_pot: Pot, new_plants_status):
    revised_plants_status = {}
    for ring_colour in new_plants_status:
        plant = Plant.parse_obj(new_plants_status[ring_colour])

        # NOTE: After harvest, slot will be empty so None. For UT, no new seeds after harvest, so keep it at None
        # TODO: Ideally to remove this once UI allows users to indicate to plant new seed
        if current_pot.session.plants[ring_colour] == None:
            plant = None

        # TODO: Future work: start time of seed planting based on user indication in app, not session start time
        # NOTE: Add replace(tzinfo=None) to avoid error "can't subtract offset-naive and offset-aware datetimes"
        elif is_seed(datetime.utcnow(), current_pot.session.sessionStartTime.replace(tzinfo=None)):
            plant.growthStage = GrowthStage.seed

        elif is_sprouting(plant.growthStage, datetime.utcnow(), current_pot.session.sessionStartTime.replace(tzinfo=None)):
            plant.growthStage = GrowthStage.sprouting
        
        else:
            pass

        revised_plants_status[ring_colour] = plant.dict() if plant != None else plant
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

def harvest_ready(new_plants_status):
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
def get_harvests_completed(current_pot: Pot, new_plants_status):
    harvest_count = 0
    after_harvest_plants_status = {}
    new_plants_objs: Union[Dict[RingColour, None], Dict[RingColour, Plant]] = {}
    old_plants_objs: Union[Dict[RingColour, None], Dict[RingColour, Plant]] = current_pot.session.plants
    for ring_colour in new_plants_status:
        if new_plants_status[ring_colour] == None:
            new_plants_objs[ring_colour] = None
        else:
            new_plants_objs[ring_colour] = Plant.parse_obj(new_plants_status[ring_colour])

    for ring_colour in RingColour:
        old_plant = old_plants_objs[ring_colour.value]
        new_plant = new_plants_objs[ring_colour.value]
        if old_plant != None and new_plant != None and is_harvested(old_plant, new_plant):
            # After harvest, slot will be empty so None
            new_plant = None
            harvest_count += 1
        after_harvest_plants_status[ring_colour] = new_plant.dict() if new_plant != None else new_plant

    return harvest_count, after_harvest_plants_status

def is_water_level_unhealthy(water_level_value: int):
    return water_level_value == 0

def is_nutrient_level_unhealthy(nutrient_level_value: float):
    return nutrient_level_value < 800.0 or nutrient_level_value > 2000.0

def is_temperature_unhealthy(temp_value: float):
    return temp_value < 24.5

def is_sensor_remedy_needed(sensor_type: SensorType, sensor_value):
    if sensor_type == SensorType.nutrient_level:
        return is_nutrient_level_unhealthy(sensor_value)
    elif sensor_type == SensorType.water_level:
        return is_water_level_unhealthy(sensor_value)
    elif sensor_type == SensorType.temperature:
        return is_temperature_unhealthy(sensor_value)
    else:
        return None
    
def is_remedy_performed(sensor_type: SensorType, last_pot_obj: Pot):
    last_sensor_alert_status = last_pot_obj.session.sensors[sensor_type].toAlert
    return last_sensor_alert_status # sensor value remedied, hence alert from True to False