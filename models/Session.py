from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Union
from enum import Enum

from models.Sensor import Sensor, SensorType
from models.GreenPointValues import GreenPointValues
from models.Reward import Reward
from models.Quiz import Quiz
from models.CheckIn import CheckIn
from models.Tutorial import Tutorial

class Seed(str, Enum):
    xiao_bai_cai = "xiao bai cai"
    class Config:  
        use_enum_values = True

class PetType(str, Enum):
    dog = "dog"
    cat = "cat"
    class Config:  
        use_enum_values = True

class NewSessionInput(BaseModel):
    petName: Union[None, str] = None
    petType: Union[None, PetType] = None
    seed: Union[None, Seed] = None
    hat: Union[None, str] = None
    potId: str


#TODO: integrate sensor type as key in sensors
class Session(BaseModel):
    session_id: Union[None, str] = "1"
    sessionStartTime: datetime = datetime.utcnow()
    sessionEndTime: Union[None, datetime] = None
    greenPointValues: GreenPointValues= GreenPointValues()
    reward: Reward = Reward()
    quiz: Quiz = Quiz()
    checkIn: CheckIn = CheckIn()
    tutorial: Tutorial = Tutorial()
    sensors: Dict[SensorType, Sensor] = {
        SensorType.temperature: Sensor(type=SensorType.temperature),
        SensorType.nutrient_level: Sensor(type=SensorType.nutrient_level),
        SensorType.water_level: Sensor(type=SensorType.water_level)
        }
    newSessInput: NewSessionInput

