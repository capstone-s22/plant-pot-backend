from pydantic import BaseModel

class Reward(BaseModel):
    coins: int
    leaves: int
    coinsReward: int
    leavesReward: int
    alertCoinSound: bool
    alertLeavesSound: bool
