from pydantic import BaseModel
from typing import List, Union, Dict
from uuid import UUID

from models.Pot import Pot, PotId

class User(BaseModel):
    # name: Union[str, None] = None
    id: str
    pots: Dict[PotId, Pot]

