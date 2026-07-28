import requests
import config
from langchain_core.tools import tool

@tool
def get_weather(lat: float, lon: float, date: str):
    """
    Отримує прогноз погоди на конкретну дату для заданих координат.
    Args:
        lat: широта локації
        lon: довгота локації
        date: дата у форматі YYYY-MM-DD, наприклад '2026-08-01'
    """

    url = config.OPEN_METEO_URL
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,windspeed_10m_max",
        "timezone": "auto",
        "start_date": date,
        "end_date": date,
    }
    response = requests.get(url, params=params)
    return simplify_weather(response.json())

def simplify_weather(raw_response: dict) -> dict:
    daily = raw_response["daily"]
    return {
        "date": daily["time"][0],
        "temp_max": daily["temperature_2m_max"][0],
        "temp_min": daily["temperature_2m_min"][0],
        "rain_probability_percent": daily["precipitation_probability_max"][0],
        "wind_speed_kmh": daily["windspeed_10m_max"][0],
    }