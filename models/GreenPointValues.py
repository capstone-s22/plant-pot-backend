from pydantic import BaseModel
from typing import Union

class GreenPointValues(BaseModel):
    red: Union[float, None] = None
    blue: Union[float, None] = None
    yellow: Union[float, None] = None
    green: Union[float, None] = None
