from pydantic import BaseModel

class Reward(BaseModel):
    coins: int
    leaves: int
    coinReward: int
    leavesReward: int