from pydantic import BaseModel
from typing import Optional
from enum import Enum


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