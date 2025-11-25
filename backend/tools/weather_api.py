# placeholder
import os
import requests
from core.settings import settings
from tools.sensor_api import get_weather_sensor


def get_weather(mode: str = "simulated"):
    """
    Fetches weather data from:
    - Simulated sensors (default)
    - Real OpenWeatherMap API (if enabled)
    
    Returns dictionary:
    {
        "rainfall_mm": int,
        "humidity": int,
        "wind_kmh": int
    }
    """

    if mode == "simulated":
        return get_weather_sensor()

    # -------- REAL API MODE --------
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise Exception("Missing OPENWEATHER_API_KEY in environment")

    lat = 23.8103
    lon = 90.4125

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )

    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()

        rainfall = data.get("rain", {}).get("1h", 0)
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        return {
            "rainfall_mm": int(rainfall),
            "humidity": int(humidity),
            "wind_kmh": int(wind),
        }

    except Exception as e:
        print("Weather API failed:", e)
        return get_weather_sensor()  # fallback
