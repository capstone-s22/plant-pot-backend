from pydantic import BaseModel
from datetime import datetime
from typing import Union, List
from enum import Enum

from models.Plant import Plants
from models.Reward import Reward
from models.Quiz import Quiz
from models.CheckIn import CheckIn
from models.Sensor import Sensors

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
        
class Session(BaseModel):
    sessionId: int = 1
    sessionStartTime: datetime = datetime.utcnow()
    sessionEndTime: Union[None, datetime] = None
    reward: Reward = Reward()
    quiz: Quiz = Quiz()
    checkIn: CheckIn = CheckIn()
    sensors: Sensors = Sensors()
    # Union doesn't work for Union[Dict[RingColour, None], Dict[RingColour, Plant]]
    plants: Plants = Plants()
    newSessInput: NewSessionInput
    class Config:  
        use_enum_values = True