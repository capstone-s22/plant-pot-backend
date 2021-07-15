from pydantic import BaseModel
from typing import Optional
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

class Plants(BaseModel):
    # Optional means Union[Plant, None], None means empty slot
    blue: Optional[Plant] = Plant(ringColour=RingColour.blue)
    red: Optional[Plant] = Plant(ringColour=RingColour.red)
    peach: Optional[Plant] = Plant(ringColour=RingColour.peach)
    purple: Optional[Plant] = Plant(ringColour=RingColour.purple)
