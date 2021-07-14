from pydantic import BaseModel
from typing import Union, Dict 
from models.Sensor import Sensor, SensorType
from enum import Enum

class GrowthStage(str, Enum):
    seed = "seed"
    sprouting = "sprouting"
    seedling = "seedling"
    vegetative = "vegetative"
    harvest = "harvest"

class RingColour(str, Enum):
    blue = "blue"
    red = "red"
    peach = "peach"
    purple = "purple"

class Yellowness(BaseModel):
    value: float = 0.0
    toShowTrim: bool = False
    
    class Config:  
        use_enum_values = True

class Plant(BaseModel):
    ringColour: RingColour
    growthStage: GrowthStage = GrowthStage.seed
    plantHealth: float = 0.0
    plantSize: float = 0.0
    yellowness: Yellowness = Yellowness()

    class Config:  
        use_enum_values = True
