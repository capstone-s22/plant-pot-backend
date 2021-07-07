from enum import Enum
from typing import Dict

from pydantic.main import BaseModel

class PlantGrowthStage(str, Enum):
    seed = "seed"
    sprouting = "sprouting"
    seedling = "seedling"
    vegetative = "vegetative"
    harvest = "harvest"
    class Config:  
        use_enum_values = True


class PotRingColour(str, Enum):
    blue = "blue"
    red = "red"
    peach = "peach"
    purple = "purple"
    class Config:  
        use_enum_values = True

class PlantGrowth(BaseModel):
    plantGrowth: Dict[PotRingColour, PlantGrowthStage] = {
        PotRingColour.red: PlantGrowthStage.seed,
        PotRingColour.peach: PlantGrowthStage.seed,
        PotRingColour.purple: PlantGrowthStage.seed,
        PotRingColour.blue: PlantGrowthStage.seed
        }