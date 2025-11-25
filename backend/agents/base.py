from langchain_openai import ChatOpenAI
from core.settings import settings

def llm_json(temp=0.2):
    return ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=temp,
        openai_api_key=settings.OPENAI_API_KEY,
        response_format={"type": "json_object"}
    )
