from pydantic import BaseModel, validator
from enum import Enum
import uuid 
import time as time
from typing import get_type_hints, List, Optional, Dict
from typing_extensions import TypedDict

from models.Pot import Pot, PotId
from models.Session import Session, NewSessionInput
from models.Sensor import Sensor, SensorType, SensorIndicatorRange
from models.GreenPointValues import GreenPointValues
from models.Reward import Reward
from models.Quiz import Quiz, quizDifficulty
from models.CheckIn import CheckIn
from models.Activity import Activity

'''
Pot to Backend JSONmessages
'''

def validate_model(data):
    print(data)
    return Message.parse_obj(data)

class Action(str, Enum):
    create = "create"
    read = "read"
    update = "update"
    append = "append"
    delete = "delete"

    class Config:  
        use_enum_values = True

class PotData(str, Enum):
    pot = "pot"
    checkIn = "checkIn"
    sensorTemperature = "sensors.temperature"
    sensorNutrientLevel = "sensors.nutrientLevel"
    sensorWaterLevel = "sensors.waterLevel"
    
    class Config:  
        use_enum_values = True

class PotDataDict(TypedDict):
    field: PotData
    value: Optional[str]

class Message(BaseModel):
    action: Action
    potId: get_type_hints(Pot)["potId"] # Or Pot.__annotations__["potId"]
    data: List[PotDataDict]

# class UpdateSensorValue(BaseModel):
#     action: RequestAction
#     potId: get_type_hints(Pot)["potId"] # Or Pot.__annotations__["potId"]
#     sensorType: SensorType
#     value: float





    