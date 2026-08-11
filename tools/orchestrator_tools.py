import requests
from langchain_core.tools import tool
import config
from services.db import ChatDatabase
from typing import Optional

db = ChatDatabase()

@tool()
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

@tool()
def get_content(
    keyword: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> list[dict]:
    """
    Search the user's previous conversation history.

    Use this tool when the user asks about something that may have
    been mentioned in an earlier conversation.

    Examples:
    - "Про що ми говорили про Львів?"
    - "Коли я планував поїздку до Львова?"
    - "Чи згадував я раніше Париж?"
    - "Що я казав 10 травня?"
    - "Коли я збирався гуляти у Львові?"

    SEARCH STRATEGY:
    1. If the user mentions a specific place, person, topic, or object,
       use it as the keyword.
    2. If the user does not specify a date, leave date_from and date_to
       as null.
    3. Do NOT invent dates.
    4. If the first search does not provide enough information,
       perform another search using a different relevant keyword.
    5. The search is a text search. It does not understand semantic
       meaning by itself. After receiving the results, analyze the
       returned messages and determine which ones answer the user's
       question.
    6. Pay attention to created_at when determining when something
       happened or was planned.
    7. Use session_id to understand which messages belong to the same
       conversation.

    IMPORTANT:
    - keyword is optional.
    - date_from is optional.
    - date_to is optional.
    - Passing null/None for dates is valid.
    - Dates must use YYYY-MM-DD format.

    Args:
        keyword:
            Word or phrase to search for in previous messages.
            Example: "Львів", "Париж", "поїздка".
            Use null if searching only by date.

        date_from:
            Start date in YYYY-MM-DD format.
            Use null if no start date was specified.

        date_to:
            End date in YYYY-MM-DD format.
            Use null if no end date was specified.
    """

    return db.search_messages(
        keyword=keyword,
        date_from=date_from,
        date_to=date_to,
        limit=50,
    )