from pytrends.request import TrendReq
import pandas as pd
import plotly.express as px

from typing import List, Union, Annotated, Dict
from langchain_core.prompts import ChatPromptTemplate

from trend_agent.LLMManager import LLMManager
from trend_agent.TrendTools import (
    get_trends_by_keyword,
    get_today_trends,
    get_history_trends,
)

from serpapi import GoogleSearch
import os


class TrendAgent:
    def __init__(self):

        self.llm_manager = LLMManager()

    def trendagent_executor(self, question: str):

        tools = [
            get_trends_by_keyword,
            get_today_trends,
            get_history_trends,
        ]
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a specialized assistant designed to search and retrieve trending data using the Google Trends API. Your primary function is to help users discover current and past trends based on specific queries. You have access to tools that allow you to perform the following tasks:

1.	Track Current Trends: Retrieve and display real-time trending topics based on specific regions, categories, or keywords provided by the user.
2.	Search Historical Trends: Look up and display past trends using search terms, time ranges, and geographical filters. If a timeframe is not provided, you will infer or set it to a recent time period.
3.	Discover Relevant Trends: Identify and return trends that are likely to be of interest to the user based on their input.

Your goal is to help the user explore and find relevant trending topics or historical trend data. Always present the information in a clear and concise manner, and ensure that the data retrieved is relevant to the user’s requests. If no data is available, inform the user politely and suggest alternative search options.
You have to summarize the result.
""",
                ),
                (
                    "human",
                    """
                Quetion: {question}
                
                {agent_scratchpad}""",
                ),
            ]
        )
        result = self.llm_manager.execute_tool_agent(
            tools,
            prompt,
            question=question,
        )
        return {"result": result}
