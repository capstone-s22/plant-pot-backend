from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Union, List
from enum import Enum

from models.Plant import RingColour, Plant
from models.Reward import Reward
from models.Quiz import Quiz
from models.CheckIn import CheckIn
from models.Sensor import Sensor, SensorType

class Seed(str, Enum):
    chinese_cabbage = "chinese cabbage"

class PetType(str, Enum):
    penguin = "penguin"
    cat = "cat"
    beaver = "beaver"

class NewSessionInput(BaseModel):
    petName: Union[None, str] = None
    petType: Union[None, PetType] = None
    seed: Union[None, Seed] = None
    hat: Union[None, str] = None
    unlockedHats: List[str] = []
    potId: str
    class Config:  
        use_enum_values = True
        
#TODO: integrate sensor type as key in sensors
class Session(BaseModel):
    sessionId: int = 1
    sessionStartTime: datetime = datetime.utcnow()
    sessionEndTime: Union[None, datetime] = None
    reward: Reward = Reward()
    quiz: Quiz = Quiz()
    checkIn: CheckIn = CheckIn()
    sensors: Dict[SensorType, Sensor] = {
        SensorType.temperature: Sensor(type=SensorType.temperature),
        SensorType.nutrient_level: Sensor(type=SensorType.nutrient_level),
        SensorType.water_level: Sensor(type=SensorType.water_level)
        }
    # None means empty slot
    plants: Union[Dict[RingColour, None], Dict[RingColour, Plant]] = {
        RingColour.red: Plant(ringColour=RingColour.red),
        RingColour.peach: Plant(ringColour=RingColour.peach),
        RingColour.purple: Plant(ringColour=RingColour.purple),
        RingColour.blue: Plant(ringColour=RingColour.blue)
        }
    newSessInput: NewSessionInput
    class Config:  
        use_enum_values = True