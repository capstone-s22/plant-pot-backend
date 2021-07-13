from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Union, get_type_hints
from uuid import UUID
from models.Session import Session

#TODO: Integrate sessionID in sessions key
class PotId(BaseModel):
    id: str

class Pot(BaseModel):
    potId: Union[None, str]
    # user_id: str
    potRegisteredTime: datetime = datetime.utcnow()
    session: Session
    connected: bool = True

class PotHttpReq(BaseModel):
    id: get_type_hints(Pot)["potId"] # Or Pot.__annotations__["potId"]