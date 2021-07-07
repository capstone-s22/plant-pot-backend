from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Union, List
from enum import Enum

from models.Sensor import Sensors
from models.PlantGrowth import PlantGrowth
from models.Reward import Reward
from models.Quiz import Quiz
from models.CheckIn import CheckIn

class Seed(str, Enum):
    xiao_bai_cai = "xiao bai cai"
    class Config:  
        use_enum_values = True

class PetType(str, Enum):
    penguin = "penguin"
    cat = "cat"
    beaver = "beaver"
    class Config:  
        use_enum_values = True

class NewSessionInput(BaseModel):
    petName: Union[None, str] = None
    petType: Union[None, PetType] = None
    seed: Union[None, Seed] = None
    hat: Union[None, str] = None
    unlockedHats: List[str] = []
    potId: str

#TODO: integrate sensor type as key in sensors
class Session(BaseModel):
    sessionStartTime: datetime = datetime.utcnow()
    sessionEndTime: Union[None, datetime] = None
    reward: Reward = Reward()
    quiz: Quiz = Quiz()
    checkIn: CheckIn = CheckIn()
    sensors: Sensors = Sensors()
    plantGrowth: PlantGrowth = PlantGrowth()
    newSessInput: NewSessionInput