from pydantic import BaseModel

class RewardSound(BaseModel):
    alertCoinsSound: bool = False
    alertLeavesSound: bool = False

class RewardIncrement(BaseModel):
    coinsRewardIncrement: int = 0
    leavesRewardIncrement: int = 0

#TODO: Nested rewards based on the classes above: Link up with Ben on this
class Reward(BaseModel):
    coins: int = 80
    leaves: int = 40
    rewardSound: RewardSound = RewardSound()
    checkInReward: RewardIncrement = RewardIncrement()
    plantCareReward: RewardIncrement = RewardIncrement()
    harvestReward: RewardIncrement = RewardIncrement()