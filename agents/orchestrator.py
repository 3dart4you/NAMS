from langchain.agents import create_agent
from services.llm_factory import get_llm
from agents.places_agent import run_places_agent
from agents.weather_agent import run_weather_agent
from datetime import date
from tools.orchestrator_tools import geolocation

SYSTEM_PROMPT = f"""Ти — оркестратор туристичного помічника.
Сьогоднішня дата: {date.today().isoformat()}.

Якщо користувач дає назву міста/локації словами (а не координатами) —
СПОЧАТКУ виклич {geolocation}, щоб отримати lat/lon, і тільки
ПОТІМ передавай ці координати субагентам погоди та пошуку місць.
Не питай користувача про координати самостійно — завжди намагайся
отримати їх через geolocation.

Коли користувач каже "завтра", "вихідні" тощо — сам порахуй конкретну дату
у форматі YYYY-MM-DD і передавай її субагентам.

Якщо рекомендуєш місця для відпочинку на відкритому повітрі
(тераси, парки, прогулянки), обов'язково перевір погоду для цієї локації."""

def run_orchestrator(user_message: str) -> str:
    agent = create_agent(
        model=get_llm(),
        tools=[run_places_agent, run_weather_agent, geolocation],
        system_prompt=SYSTEM_PROMPT
    )

    for message_chunk, metadata in agent.stream({"messages": [user_message]}, stream_mode="messages"):
        if metadata.get("langgraph_node") == "model" and message_chunk.content:
            print(message_chunk.content, end="", flush=True)
    print()

    return "DONE"