from pydantic import BaseModel, validator
from enum import Enum
import uuid 
import time as time
from typing import get_type_hints, List, Optional, Dict, Union
from typing_extensions import TypedDict
from models.Pot import Pot

'''
Backend to Pot JSON messages
'''

async def validate_model(data):
    return MessageToPot.parse_obj(data)

class Action(str, Enum):
    read = "read"
    update = "update"

class PotSendDataBool(str, Enum):
    showCheckIn = "showCheckIn"
    showQuiz = "showQuiz"
    alertTempSensor = "temperature" # Currently unused
    alertNLSensor = "nutrientLevel" # Currently unused
    alertWLSensor = "waterLevel" # Currently unused
    ringHappySound = "ringHappySound"
    ringSadSound = "ringSadSound"

class PotSendDataStr(str, Enum):
    health_check = "health check"
    acknowledgment = "ack"
    error = "error"
    image = "image"
    harvest = "harvest"

class PotSendDataDictBool(TypedDict):
    field: PotSendDataBool
    value: Union[None, bool]

class PotSendDataDictStr(TypedDict):
    field: PotSendDataStr
    value: Union[None, str]

class MessageToPot(BaseModel):
    action: Action = Action.update
    potId: get_type_hints(Pot)["potId"] # Or Pot.__annotations__["potId"]
    data: List[Union[PotSendDataDictStr, PotSendDataDictBool]]
    class Config:  
        use_enum_values = True




    