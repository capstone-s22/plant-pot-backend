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


class HealthMetricUpdate(BaseModel):
    id: str
    parameter: str
    value: float

class Sensors(BaseModel):
    sensorCoinsReward: int = 0
    sensorLeavesReward: int = 0
    sensors: Dict[SensorType, Sensor] = {
        SensorType.temperature: Sensor(type=SensorType.temperature),
        SensorType.nutrient_level: Sensor(type=SensorType.nutrient_level),
        SensorType.water_level: Sensor(type=SensorType.water_level)
        }