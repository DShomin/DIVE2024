from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
)


class LLMManager:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # gpt-4o

    def invoke(self, prompt: ChatPromptTemplate, **kwargs) -> str:
        messages = prompt.format_messages(**kwargs)
        response = self.llm.invoke(messages)
        return response.content
