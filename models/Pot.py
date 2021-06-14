from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Union
from uuid import UUID
 
from models.Session import Session

#TODO: Integrate sessionID in sessions key
class PotId(BaseModel):
    id: str

class Pot(BaseModel):
    potId: Union[None, str]
    # user_id: str
    potRegisteredTime: datetime
    sessions: Dict[str, Session]

class NewPot(BaseModel):
    id: str