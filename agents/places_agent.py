from langchain.agents import create_agent
from services.llm_factory import get_llm
from tools.places_tools import search_place
from langchain_core.tools import tool

@tool
def run_places_agent (user_message: str) -> str:
    """
    Викликає агента пошуку місць — кафе, ресторанів, парків тощо.
    Використовуй, коли користувач хоче знайти конкретне місце для відвідування,
    з'їсти щось, погуляти, чи цікавиться певними локаціями.
    Args:
        user_message: запит користувача своїми словами, з усім потрібним контекстом
            (місто/координати, тип місця, вподобання)
    """

    agent = create_agent(
        model=get_llm(),
        tools=[search_place]
    )

    response = agent.invoke({"messages": user_message})["messages"][-1].content
    return response
