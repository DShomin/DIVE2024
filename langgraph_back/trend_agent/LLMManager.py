from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent


class LLMManager:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)

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
