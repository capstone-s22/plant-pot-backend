from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Union
from enum import Enum

from models.Sensor import Sensor
from models.GreenPointValues import GreenPointValues
from models.Reward import Reward
from models.Quiz import Quiz
from models.CheckIn import CheckIn
from models.Activity import Activity

class Seed(str, Enum):
    xiao_bai_cai = "xiao bai cai"

class PetType(str, Enum):
    dog = "dog"
    cat = "cat"

class NewSessionInput(BaseModel):
    petName: Union[None, str]
    petType: Union[None, PetType]
    seed: Union[None, Seed]
    potId: str
    
    class Config:  
        use_enum_values = True


#TODO: integrate sensor type as key in sensors
class Session(BaseModel):
    session_id: Union[None, str]
    sessionStartTime: datetime
    sessionEndTime: Union[None, datetime]
    newSessInput: NewSessionInput
    sensors: Dict[str, Sensor]
    greenPointValues: GreenPointValues
    reward: Reward
    quiz: Quiz
    checkIn: CheckIn
    activity: Activity
    
    class Config:  
        use_enum_values = True

# class UpdateSession(BaseModel):
