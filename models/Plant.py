from pydantic import BaseModel
from typing import Dict, List
from models.Sensor import Sensor, SensorType
from enum import Enum

class GrowthStage(str, Enum):
    seed = "seed"
    sprouting = "sprouting"
    seedling = "seedling"
    vegetative = "vegetative"
    harvest = "harvest"
    class Config:  
        use_enum_values = True

class RingColour(str, Enum):
    blue = "blue"
    red = "red"
    peach = "peach"
    purple = "purple"
    class Config:  
        use_enum_values = True

class Plant(BaseModel):
    ringColour: RingColour
    growthStage: GrowthStage = GrowthStage.seed