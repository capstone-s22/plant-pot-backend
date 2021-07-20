from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Dict, Union, get_type_hints
from uuid import UUID
from models.Session import Session
from models.Sound import Sounds

#TODO: Integrate sessionID in sessions key
class PotId(BaseModel):
    id: str

class Pot(BaseModel):
    potId: Union[None, str]
    # user_id: str
     # NOTE: Can't create default values here as it will stay as constant throughout
    potRegisteredTime: datetime
    session: Session
    connected: bool = True
    sounds: Sounds = Sounds()

class PotHttpReq(BaseModel):
    id: get_type_hints(Pot)["potId"] # Or Pot.__annotations__["potId"]