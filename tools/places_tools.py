import requests
import config
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_core.tools import tool

@tool
def search_place(lat: float, lon: float, category: str, radius: int = 1000) -> list[dict]:
    """
    Шукає місця (кафе, парки, ресторани тощо) поблизу заданих координат.
    Args:
        lat: широта центру пошуку
        lon: довгота центру пошуку
        category: категорія місця, наприклад 'catering.cafe', 'leisure.park', 'catering.restaurant'
        radius: радіус пошуку в метрах, за замовчуванням 2000
    """

    geoapify_key = os.getenv("GEOAPIFY_KEY")
    geoapify_url = config.GEOAPIFY_BASE_URL
    params = {
        "categories": category,
        "filter": f"circle:{lon},{lat},{radius}",
        "limit": 10,
        "apiKey": geoapify_key
    }
    response = requests.get(geoapify_url, params=params)
    return simplify_place(response.json())

def simplify_place(raw_response: dict) -> list[dict]:
    simplified = []
    for feature in raw_response.get("features", []):
        props = feature["properties"]
        simplified.append({
            "name": props.get("name", "Без назви"),
            "address": props.get("formatted"),
            "categories": props.get("categories", []),
            "opening_hours": props.get("opening_hours"),
            "lat": props["lat"],
            "lon": props["lon"],
        })
    return simplified