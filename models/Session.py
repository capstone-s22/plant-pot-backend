from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Union
from enum import Enum

from models.Pet import Pet
from models.Sensor import Sensor
from models.GreenPointValues import GreenPointValues
from models.Reward import Reward
from models.Quiz import Quiz
from models.CheckIn import CheckIn
from models.Activity import Activity

class Seed(str, Enum):
    xiao_bai_cai = "xiao bai cai"


#TODO: integrate sensor type as key in sensors
class Session(BaseModel):
    session_id: Union[None, str]
    sessionStartTime: datetime
    sessionEndTime: Union[None, datetime]
    seed: Union[None, Seed]
    pet: Pet
    sensors: Dict[str, Sensor]
    greenPointValues: GreenPointValues
    reward: Reward
    quiz: Quiz
    checkIn: CheckIn
    activity: Activity
    
    class Config:  
        use_enum_values = True

# class UpdateSession(BaseModel):
