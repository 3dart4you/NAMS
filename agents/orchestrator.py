from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from services.llm_factory import get_llm
from agents.places_agent import run_places_agent
from agents.weather_agent import run_weather_agent
from datetime import date

SYSTEM_PROMPT = f"""Ти — оркестратор туристичного помічника.
Твоя задача — розуміти запит користувача і викликати відповідних субагентів
для отримання інформації (погода, місця, житло тощо).

Сьогоднішня дата: {date.today().isoformat()}.Коли користувач каже "завтра", "вихідні" тощо — сам порахуй конкретну дату
у форматі YYYY-MM-DD і передавай її субагентам явно.

Важливо: якщо рекомендуєш місця для відпочинку на відкритому повітрі
(тераси, парки, прогулянки), обов'язково перевір погоду для цієї локації
через weather agent, і попередь користувача, якщо погодні умови не сприятливі."""

MAX_ITERATIONS = 5

def run_orchestrator(user_message: str) -> str:
    llm = get_llm()
    tools_list = [run_places_agent, run_weather_agent]
    llm_with_tools = llm.bind_tools(tools_list)
    tools_by_name = {item.name: item for item in tools_list}

    messages = [
        SystemMessage(SYSTEM_PROMPT),
        HumanMessage(user_message)
    ]

    for _ in range(MAX_ITERATIONS):
        ai_response = llm_with_tools.invoke(messages)
        messages.append(ai_response)

        if not ai_response.tool_calls:
            return ai_response.content

        for tool_call in ai_response.tool_calls:
            tool_obj = tools_by_name.get(tool_call["name"])
            if tool_obj:
                result = tool_obj.invoke(tool_call["args"])
                print(f"--- РЕЗУЛЬТАТ {tool_call['name']} ---")
                print(result)
                print("---")
                messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))

    return "Не вдалося отримати остаточну відповідь, спробуйте переформулювати запит."