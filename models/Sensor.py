from pydantic import BaseModel
from enum import Enum
from typing import Union

class SensorType(str, Enum):
    temperature = "temperature"
    nutrient_level = "nutrientLevel"
    water_level = "waterLevel"

class SensorIndicatorRange(str, Enum): #low/high means too low/high (unhealthy), medium means just right (healthy)
    null = None
    low = "low"
    medium = "medium"
    high = "high"
    
class Sensor(BaseModel):
    type: SensorType
    value: Union[None, float] = None
    indicator: Union[None, SensorIndicatorRange] = SensorIndicatorRange.medium
    toAlert: bool = False
    class Config:  
        use_enum_values = True

class Sensors(BaseModel):
    temperature: Sensor = Sensor(type=SensorType.temperature)
    nutrientLevel: Sensor = Sensor(type=SensorType.nutrient_level)
    waterLevel: Sensor = Sensor(type=SensorType.water_level)