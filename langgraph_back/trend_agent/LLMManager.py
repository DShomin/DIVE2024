from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
)


class LLMManager:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def invoke(self, prompt: ChatPromptTemplate, **kwargs) -> str:
        messages = prompt.format_messages(**kwargs)
        response = self.llm.invoke(messages)
        return response.content

    def execute_tool_agent(self, tools: list, prompt: ChatPromptTemplate, **kwargs):
        agent = create_tool_calling_agent(self.llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent, tools=tools, return_intermediate_steps=True, verbose=True
        )
        result = agent_executor.invoke(kwargs)

        return result
