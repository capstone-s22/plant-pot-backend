from models.Reward import RewardIncrement, RewardSound
from models.Plant import Plant

C = 10

def get_check_in_reward(plants):
    leaves_reward = 0
    for ring_colour in plants:
        plant: Plant = plants[ring_colour]
        leaves_reward += (plant.plantSize*(plant.plantHealth + 1))/10 + C

    check_in_reward = RewardIncrement(
        leavesRewardIncrement=leaves_reward
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
    reward_sound = RewardSound(
        alertLeavesSound=True if reward_increment_obj.coinsRewardIncrement > 0.0 else False,
        alertCoinsSound=True if reward_increment_obj.leavesRewardIncrement > 0.0 else False
    )

    return reward_sound.dict()


# plants = {'red': Plant(ringColour='red', growthStage='sprouting', plantHealth=0.5, plantSize=2.0), 'peach': Plant(ringColour='peach', growthStage='sprouting', plantHealth=0.5, plantSize=2.0), 'blue': Plant(ringColour='blue', growthStage='sprouting', plantHealth=0.5, plantSize=2.0), 'purple': Plant(ringColour='purple', growthStage='sprouting', plantHealth=0.5, plantSize=2.0)}
# print(get_check_in_reward(plants))
# print(get_plant_care_reward())
