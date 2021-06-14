from pydantic import BaseModel
from typing import Union

class Activity(BaseModel):
    showActivity: bool
    type: Union[None, int]

