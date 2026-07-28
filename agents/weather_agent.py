from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from services.llm_factory import get_llm
from tools.weather_tools import get_weather

MAX_ITERATIONS = 5

@tool
def run_weather_agent(user_message: str) -> str:
    """
    Викликає агента прогнозу погоди.
    Використовуй, коли потрібно дізнатись погоду для конкретної локації і дати,
    або оцінити, чи погодні умови сприятливі для певної активності (прогулянка,
    відпочинок на терасі, пікнік тощо).
    Args:
        user_message: запит користувача своїми словами, з координатами/локацією і датою
    """
    llm = get_llm()
    tools_list = [get_weather]
    llm_with_tools = llm.bind_tools(tools_list)
    tools_by_name = {item.name: item for item in tools_list}

    messages = [HumanMessage(user_message)]

    for _ in range(MAX_ITERATIONS):
        ai_response = llm_with_tools.invoke(messages)
        messages.append(ai_response)

        if not ai_response.tool_calls:
            return ai_response.content

    for tool_call in ai_response.tool_calls:
        tool_obj = tools_by_name.get(tool_call["name"])
        if tool_obj:
            result = tool_obj.invoke(tool_call["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))

    final_response = llm_with_tools.invoke(messages)
    return final_response.content