from pydantic import BaseModel
from enum import Enum
from typing import Union, get_type_hints

from models.Pot import Pot

class NonSensorType(str, Enum):
    fan = "fan"
    
class NonSensor(BaseModel):
    type: NonSensorType
    status: Union[None, bool] = None
    class Config:  
        use_enum_values = True

class NonSensors(BaseModel):
    fan: NonSensor = NonSensor(type=NonSensorType.fan)

class NonSensorHttpReq(BaseModel):
    id: get_type_hints(Pot)["potId"] # Or Pot.__annotations__["potId"]
    status: get_type_hints(NonSensor)["status"]