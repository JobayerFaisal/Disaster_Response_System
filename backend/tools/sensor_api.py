import random

def get_weather_sensor():
    return {
        "rainfall_mm": random.randint(80, 200),
        "wind_kmh": random.randint(10, 60),
        "humidity": random.randint(70, 98)
    }


def get_river_sensor():
    return {
        "water_level_m": round(random.uniform(4.5, 7.0), 2),
        "rise_rate_cm_hr": round(random.uniform(5, 20), 2),
        "flow_speed": round(random.uniform(1.2, 3.2), 2)
    }
