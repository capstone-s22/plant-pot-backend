
def is_water_level_healthy(water_level_value: int):
    return "Healthy" if water_level_value == 1 else "Unhealthy"

def is_nutrient_level_healthy(nutrient_level_value: float):
    if nutrient_level_value <800.0:
        return "Too little nutrients"
    elif nutrient_level_value > 2000.0:
        return "Too much nutrients"
    else:
        return "Healthy"

def is_temperature_healthy(temp_value: float):
    return "Healthy" if temp_value > 24.5 else "Unhealthy"
