from langchain.agents import create_agent
from langchain_core.tools import tool
from services.llm_factory import get_llm
from tools.weather_tools import get_weather

@tool
def run_weather_agent(user_message: str) -> str:
    """
    Викликає агента прогнозу погоди.
    Використовуй, коли потрібно дізнатись погоду для конкретної локації та дати,
    або оцінити, чи погодні умови сприятливі для певної активності (прогулянка,
    відпочинок на терасі, пікнік тощо).
    Args:
        user_message: запит користувача своїми словами, з координатами/локацією і датою
    """

    agent = create_agent(
        model=get_llm(),
        tools=[get_weather],
    )

    response = agent.invoke({"messages": user_message})["messages"][-1].content
    return response