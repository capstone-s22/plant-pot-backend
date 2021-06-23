

def plant_health(green_point_val, yellow_point_val):
    health = green_point_val/(green_point_val + yellow_point_val)
    return health

def plant_size(green_point_val, yellow_point_val, total_area):
    plant_growth = (green_point_val + yellow_point_val)/total_area
    return plant_growth

def leaves_reward(plant_health, plant_size):
    reward = (plant_size*(plant_health + 1))/10 + 10
    return reward