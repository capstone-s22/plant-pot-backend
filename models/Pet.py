from pydantic import BaseModel
from enum import Enum
from typing import Union, List

class PetType(str, Enum):
    dog = "dog"
    cat = "cat"

class Pet(BaseModel):
    name: Union[None, str]
    type: Union[None, PetType]

    class Config:  
        use_enum_values = True