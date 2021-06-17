from pydantic import BaseModel
from typing import Union

class Tutorial(BaseModel):
    showTutorial: bool = False
    type: Union[None, int] = None

