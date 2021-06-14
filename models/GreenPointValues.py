from pydantic import BaseModel
from typing import Union

class GreenPointValues(BaseModel):
    red: Union[float, None]
    blue: Union[float, None]
    yellow: Union[float, None]
    green: Union[float, None]
