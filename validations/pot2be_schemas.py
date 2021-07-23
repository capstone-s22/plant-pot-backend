from pydantic import BaseModel, validator
from enum import Enum
import uuid 
import time as time
from typing import get_type_hints, List, Optional, Dict, Union

from models.Pot import Pot
from models.Sensor import SensorType
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

class PotDataStr(str, Enum):
    pot = "pot"
    image = "image"

class PotDataBool(str, Enum):
    checkIn = "checkIn"

# class PotDataFloat(str, Enum):
#     others = "others"

# TODO: Make better suit for different types of messages
class PotDataDictStr(BaseModel):
    field: PotDataStr
    value: Union[None, str]

class PotDataDictBool(BaseModel):
    field: PotDataBool
    value: Union[None, bool]

class PotDataDictFloat(BaseModel):
    field: SensorType
    value: Union[None, float]

class MessageFromPot(BaseModel):
    action: Action
    potId: get_type_hints(Pot)["potId"] # Or Pot.__annotations__["potId"]
    data: List[Union[PotDataDictStr, PotDataDictFloat, PotDataDictBool]]
    class Config:  
        use_enum_values = True