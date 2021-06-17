from pydantic import BaseModel, validator
from enum import Enum
import uuid 
import time as time
from typing import get_type_hints, List, Optional, Dict, Union
from typing_extensions import TypedDict

from models.Pot import Pot, PotId
from models.Session import Session, NewSessionInput
from models.Sensor import Sensor, SensorType, SensorIndicatorRange
from models.GreenPointValues import GreenPointValues
from models.Reward import Reward
from models.Quiz import Quiz, QuizDifficulty
from models.CheckIn import CheckIn
from models.Tutorial import Tutorial

'''
Pot to Backend JSON messages
'''

def validate_model(data):
    print((data))
    return Message.parse_obj(data)

class Action(str, Enum):
    create = "create"
    read = "read"
    update = "update"
    append = "append"
    delete = "delete"

    class Config:  
        use_enum_values = True

class PotDataStr(str, Enum):
    pot = "pot"
    class Config:  
        use_enum_values = True

class PotDataBool(str, Enum):
    checkIn = "checkIn"
    class Config:  
        use_enum_values = True

class PotDataInt(str, Enum):
    sensorTemperature = "sensors.temperature"
    sensorNutrientLevel = "sensors.nutrientLevel"
    sensorWaterLevel = "sensors.waterLevel"
    class Config:  
        use_enum_values = True

# TODO: Make better suit for different types of messages
class PotDataDictStr(TypedDict):
    field: PotDataStr
    value: Union[None, str]

class PotDataDictBool(TypedDict):
    field: PotDataBool
    value: Union[None, bool]

class PotDataDictInt(TypedDict):
    field: PotDataInt
    value: Union[None, int]

class Message(BaseModel):
    action: Action
    potId: get_type_hints(Pot)["potId"] # Or Pot.__annotations__["potId"]
    data: List[Union[PotDataDictStr, PotDataDictInt, PotDataDictBool]]





    