from pydantic import BaseModel
from enum import Enum
from typing import Union, Dict

class SensorType(str, Enum):
    temperature = "temperature"
    nutrient_level = "nutrientLevel"
    water_level = "waterLevel"
    class Config:  
        use_enum_values = True

class SensorIndicatorRange(str, Enum):
    null = "null"
    low = "low"
    medium = "medium"
    high = "high"
    class Config:  
        use_enum_values = True

class Sensor(BaseModel):
    type: SensorType
    value: Union[None, float] = None
    indicator: Union[None, SensorIndicatorRange] = None
    toAlert: bool = False