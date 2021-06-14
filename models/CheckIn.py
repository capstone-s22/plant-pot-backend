from pydantic import BaseModel
from datetime import datetime
from typing import Union

class CheckIn(BaseModel):
    checkIn: bool
    checkInStreak: int
    checkInLastDate: Union[None, datetime]
    checkInToopTipDone: bool
