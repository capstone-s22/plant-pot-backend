from pydantic import BaseModel

class Reward(BaseModel):
    coins: int = 80
    leaves: int = 40
    alertCoinsSound: bool = False
    alertLeavesSound: bool = False
