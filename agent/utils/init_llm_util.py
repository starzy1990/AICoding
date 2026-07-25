from langchain.chat_models import init_chat_model
from utils.env_util import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, QWEN_API_KEY, QWEN_BASE_URL


deepseek_llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)

qwen_llm = init_chat_model(
    model="quwen-plus",
    model_provider="openai",
    api_key=QWEN_API_KEY
)