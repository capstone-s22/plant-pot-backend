from pydantic import BaseModel, validator
from enum import Enum
import uuid 
import time as time
from typing import get_type_hints, List, Optional, Dict, Union

from models.Pot import Pot
from models.Sensor import SensorType
from models.NonSensor import NonSensorType

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
    showHarvest = "showHarvest"
    alertTempSensor = "showTemperature"
    alertNLSensor = "showNutrientLevel"
    alertWLSensor = "showWaterLevel"
    ringHappySound = "ringHappySound"
    ringSadSound = "ringSadSound"

class PotSendDataStr(str, Enum):
    health_check = "health check"
    acknowledgment = "ack"
    error = "error"
    image = "image"

class PotSendDataDictBool(BaseModel):
    field: Union[PotSendDataBool, NonSensorType]
    value: Union[None, bool]

class PotSendDataDictStr(BaseModel):
    field: Union[PotSendDataStr, SensorType]
    value: Union[None, str]

class MessageToPot(BaseModel):
    action: Action = Action.update
    potId: get_type_hints(Pot)["potId"] # Or Pot.__annotations__["potId"]
    data: List[Union[PotSendDataDictStr, PotSendDataDictBool]]
    class Config:  
        use_enum_values = True

def getPotSendDataBoolSensor(sensor_type: SensorType):
    if sensor_type == sensor_type.temperature:
        return PotSendDataBool.alertTempSensor
    elif sensor_type == sensor_type.nutrient_level:
        return PotSendDataBool.alertNLSensor
    elif sensor_type == sensor_type.water_level:
        return PotSendDataBool.alertWLSensor
    else:
        raise Exception("Invalid Sensor Type") 