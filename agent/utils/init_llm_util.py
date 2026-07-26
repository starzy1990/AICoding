from langchain.chat_models import init_chat_model
from agent.utils.env_util import get_env_var


deepseek_llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=get_env_var("DEEPSEEK_API_KEY"),
    base_url=get_env_var("DEEPSEEK_BASE_URL"),
)

qwen_llm = init_chat_model(
    model="quwen-plus",
    model_provider="openai",
    api_key=get_env_var("QWEN_API_KEY"),
)