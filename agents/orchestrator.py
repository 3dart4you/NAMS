from langchain.agents import create_agent
from services.llm_factory import get_llm
from agents.places_agent import run_places_agent
from agents.weather_agent import run_weather_agent
from datetime import date
from tools.orchestrator_tools import get_geolocation, get_content

SYSTEM_PROMPT = f"""Ти — оркестратор туристичного помічника.

Rules:
- Коли користувач каже "завтра", "вихідні" тощо — використай {date.today().isoformat()} для отримання конкретної дати
у форматі YYYY-MM-DD і передавай її субагентам
- Перед зверненням до субагентів скористайся {get_geolocation} для отримання координат бажаного місця.
Якщо невідомо точної назви місця для визначення погоди достатньо знати координати орієнтовного центру регіону.
- Якщо в повідомленні користувача немає конкретики і він говорить, що хоче прогулятись, відвідати щось чи кудись поїхати
обов'язково перевір погоду для цієї локації через субагента {run_weather_agent}.
 Example:
    user - "Де можна пообідати в районі парка Шевченка?"
    ai_assistant - "На вході в парк є кафе 'Сяйво', в центрі парку можна замовити хотдоги в закладі 'Пузатий Боб', 
                    а березі ставка продається дуже смачне морозиво в 'Смакота'"
- Якщо користувач не прописав жодних вимог до комфорту, ціни, температури тощо збери цю інформацію і дай висновки типу 
'найдешевше буде тут, а найкомфортніше може бути тут якщо любите дивани чи спокійну музику'.
"""

agent = create_agent(
    model=get_llm(),
    tools=[run_places_agent, run_weather_agent, get_geolocation, get_content],
    system_prompt=SYSTEM_PROMPT
)

def run_orchestrator(messages: list[dict]) -> str:
    full_response = ""
    is_first_chunk = True
    status_text = "🤔 NAMS думає..."
    in_thinking = False
    buffer = ""

    for message_chunk, metadata in agent.stream(
        {"messages": messages},
        stream_mode="messages",
    ):
        if metadata.get("langgraph_node") == "model" and message_chunk.content:
            buffer += message_chunk.content

            while True:
                if not in_thinking:
                    start = buffer.find("<think>")
                    if start == -1:
                        clean, buffer = buffer, ""
                    else:
                        clean, buffer = buffer[:start], buffer[start + len("<think>"):]
                        in_thinking = True

                    if clean:
                        if is_first_chunk:
                            print("\r" + " " * len(status_text) + "\r", end="", flush=True)
                            print("NAMS: ", end="", flush=True)
                            is_first_chunk = False
                        print(clean, end="", flush=True)
                        full_response += clean
                else:
                    end = buffer.find("</think>")
                    if end == -1:
                        buffer = ""
                        break
                    else:
                        buffer = buffer[end + len("</think>"):]
                        in_thinking = False
                        continue
                break

    print()
    return full_response