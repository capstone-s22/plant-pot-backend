from pydantic import BaseModel
from datetime import datetime
from typing import Union

class CheckIn(BaseModel):
    showCheckIn: bool = False
    checkInStreak: int = 0
    checkInLastDate: Union[None, datetime] = None