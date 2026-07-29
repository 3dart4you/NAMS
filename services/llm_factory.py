from langchain.chat_models import init_chat_model
import config


def get_llm():
    return init_chat_model(
        base_url=config.LLM_BASE_URL,
        model=config.LLM_MODEL,
        model_provider="openai",
        api_key="not_needed",
    )