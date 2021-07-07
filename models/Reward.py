from pydantic import BaseModel

class Reward(BaseModel):
    coins: int = 80
    leaves: int = 40
    alertCoinsSound: bool = False
    alertLeavesSound: bool = False
    checkInCoinsReward: int = 0
    checkInLeavesReward: int = 0
    plantCareCoinsReward: int = 0
    plantCareLeavesReward: int = 0