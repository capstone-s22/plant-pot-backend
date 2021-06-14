from pydantic import BaseModel
from enum import Enum
from typing import Union

class SensorType(str, Enum):
    temperature = "temperature"
    nutrient_level = "nutrientLevel"
    water_level = "waterLevel"

class SensorIndicatorRange(str, Enum):
    null = "null"
    low = "low"
    medium = "medium"
    high = "high"

class Sensor(BaseModel):
    type: SensorType
    value: Union[None, float]
    indicator: Union[None, SensorIndicatorRange]
    toAlert: bool

    class Config:  
        use_enum_values = True

class HealthMetricUpdate(BaseModel):
    id: str
    parameter: str
    value: float