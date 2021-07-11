import aiohttp
from attr import field
import os
from typing import Dict 

from models.Plant import Plant, RingColour, GrowthStage
from models.Pot import Pot

# CV_SERVER_URL_PREFIX = os.getenv('CV_SERVER_URL_PREFIX')
CV_SERVER_URL_PREFIX = "http://127.0.0.1:3002/cv"

#TODO: Add more rules to ensure users dont cheat and iterate the harvest rewards
async def cv_inference(pot_id, encoded_img_data):
    data = { "potId": pot_id, "encoded_data": encoded_img_data }
    async with aiohttp.request(method='GET', url=CV_SERVER_URL_PREFIX, json=data) as resp:
        assert resp.status == 200
        response = await resp.json()
        for ring_colour in response:
            try:
                Plant.parse_obj(response[ring_colour]) # Validate data with model
            except Exception as e:
                return e
        return response
def harvest_ready(new_plants_status):
    for ring_colour in new_plants_status:
        plant = Plant.parse_obj(new_plants_status[ring_colour])
        if plant.growthStage ==  GrowthStage.harvest:
            # As long as there is harvest stage for any plant inform
            return True
    return False

def is_harvested(old_plant_obj: Plant, new_plant_obj: Plant):
    print(old_plant_obj.growthStage, new_plant_obj.growthStage)
    return old_plant_obj.growthStage == GrowthStage.harvest and new_plant_obj.growthStage == GrowthStage.seed

def get_harvests_completed(current_pot: Pot, new_plants_status):
    harvest_count = 0
    new_plants_objs: Dict[RingColour, Plant] = {}
    old_plants_objs: Dict[RingColour, Plant] = current_pot.session.plants
    for ring_colour in new_plants_status:
        new_plants_objs[ring_colour] = Plant.parse_obj(new_plants_status[ring_colour])

    for ring_colour in RingColour:
        if is_harvested(old_plants_objs[ring_colour.value], new_plants_objs[ring_colour.value]):
            harvest_count += 1
    
    return harvest_count

def is_water_level_healthy(water_level_value: int):
    return "Healthy" if water_level_value == 1 else "Unhealthy"

def is_nutrient_level_healthy(nutrient_level_value: float):
    if nutrient_level_value <800.0:
        return "Too little nutrients"
    elif nutrient_level_value > 2000.0:
        return "Too much nutrients"
    else:
        return "Healthy"

def is_temperature_healthy(temp_value: float):
    return "Healthy" if temp_value > 24.5 else "Unhealthy"

