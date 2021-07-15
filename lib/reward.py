from models.Reward import RewardIncrement
from models.Plant import Plant, Plants
from models.CheckIn import CheckIn

C = 10

def get_harvest_reward(harvest_count: int):
    leaves_reward = harvest_count*50
    coins_reward = harvest_count*100
    plant_care_reward = RewardIncrement(
        coinsRewardIncrement=coins_reward,
        leavesRewardIncrement=leaves_reward
    )

    return plant_care_reward.dict()
    

def get_check_in_reward(plants: Plants, check_in_info: dict):
    leaves_reward = 0
    coins_reward = 0
    for plant_tuple in plants:
        # NOTE: Iterating through plants: Plants give you ('peach', Plant(...)) as a tuple
        # TODO: Perhaps find a more refined way to do this
        plant: Plant = plant_tuple[1]
        leaves_reward += (plant.plantSize*(plant.plantHealth + 1))/10 + C

    check_in_obj = CheckIn.parse_obj(check_in_info)
    if check_in_obj.checkInStreak % 5 == 0:
        coins_reward = 20*(check_in_obj.checkInStreak//5)

    check_in_reward = RewardIncrement(
        leavesRewardIncrement=leaves_reward,
        coinsRewardIncrement=coins_reward
    )

    return check_in_reward.dict()

def get_plant_care_reward():
    leaves_reward = 20
    coins_reward = 20
    plant_care_reward = RewardIncrement(
        coinsRewardIncrement=coins_reward,
        leavesRewardIncrement=leaves_reward
    )

    return plant_care_reward.dict()

def get_reward_sounds(reward_increments):
    reward_increment_obj: RewardIncrement = RewardIncrement.parse_obj(reward_increments)
    return reward_increment_obj.coinsRewardIncrement > 0.0 or reward_increment_obj.leavesRewardIncrement > 0.0


# plants = {'red': Plant(ringColour='red', growthStage='sprouting', plantHealth=0.5, plantSize=2.0), 'peach': Plant(ringColour='peach', growthStage='sprouting', plantHealth=0.5, plantSize=2.0), 'blue': Plant(ringColour='blue', growthStage='sprouting', plantHealth=0.5, plantSize=2.0), 'purple': Plant(ringColour='purple', growthStage='sprouting', plantHealth=0.5, plantSize=2.0)}
