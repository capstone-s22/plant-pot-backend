from pydantic import BaseModel
from typing import Optional
from enum import Enum

from pydantic.decorator import validate_arguments

class SensorType(str, Enum):
    temperature = "temperature"
    nutrient_level = "nutrientLevel"
    water_level = "waterLevel"

class SensorIndicatorRange(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Sensor(BaseModel):
    type: SensorType
    value: float
    indicator: SensorIndicatorRange
    toAlert: bool

class GreenPointValues(BaseModel):
    red: float
    blue: float
    yellow: float
    green: float

class Reward(BaseModel):
    coins: int
    leaves: int
    coinReward: int
    leavesReward: int

class Quiz(BaseModel):
    showQuiz: bool
    quizDifficulty: bool
    quizNumber: int 
    quizTooltipDone: bool
class CheckIn(BaseModel):
    checkIn: bool
    checkInStreak: int
    checkInLastDate: int
    checkInToopTipDone: bool


class NewPot(BaseModel):
    id: str

class HealthMetricUpdate(BaseModel):
    id: str
    parameter: str
    value: float

class HealthMetric(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# user = HealthMetricUpdate(id='123', parameter='12', value='one')

