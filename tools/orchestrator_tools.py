import requests
from langchain_core.tools import tool
import config

@tool(parse_docstring=True,)
def get_geolocation(place_name: str) -> dict:
    """Перетворює назву міста/місця на географічні координати (широта, довгота).

    Використовуй цей інструмент ЗАВЖДИ, коли користувач називає локацію словами
    (наприклад, "Франківськ", "центр Львова"), а не координатами напряму.

    Args:
        place_name: назва міста або місця, наприклад 'Івано-Франківськ'

    Returns:
        dict: словник координат lat/lon
    """
    url = config.NOMINATIM_URL
    params = {"q": place_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "NAMS"}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if not data:
        return {"error": f"Не вдалося знайти координати для '{place_name}'"}

    return {
        "lat": float(data[0]["lat"]),
        "lon": float(data[0]["lon"]),
    }
