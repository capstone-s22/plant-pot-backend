from pydantic import BaseModel, validator
from enum import Enum
import uuid 
import time as time
from typing import get_type_hints, List, Optional, Dict, Union
from typing_extensions import TypedDict

from models.Pot import Pot

'''
Pot to Backend JSON messages
'''

async def validate_model(data):
    return MessageFromPot.parse_obj(data)

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
    image = "image"
    class Config:  
        use_enum_values = True

class PotDataBool(str, Enum):
    checkIn = "checkIn"
    class Config:  
        use_enum_values = True

class PotDataFloat(str, Enum):
    sensorTemperature = "temperature"
    sensorNutrientLevel = "nutrientLevel"
    sensorWaterLevel = "waterLevel"
    class Config:  
        use_enum_values = True

# TODO: Make better suit for different types of messages
class PotDataDictStr(TypedDict):
    field: PotDataStr
    value: Union[None, str]

class PotDataDictBool(TypedDict):
    field: PotDataBool
    value: Union[None, bool]

class PotDataDictFloat(TypedDict):
    field: PotDataFloat
    value: Union[None, float]

class MessageFromPot(BaseModel):
    action: Action
    potId: get_type_hints(Pot)["potId"] # Or Pot.__annotations__["potId"]
    data: List[Union[PotDataDictStr, PotDataDictFloat, PotDataDictBool]]





    