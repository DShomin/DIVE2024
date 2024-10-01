import numpy as np
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from typing import Dict
from dive_agent.DatabaseManager import DatabaseManager
from dive_agent.LLMManager import LLMManager
from dive_agent.Analyses import correlation


class AnalysisAgent:
    def __init__(self):
        self.llm_manager = LLMManager()
        self.db_manager = DatabaseManager()

        self.analysis_tools = {"correlation": correlation.BASE_DESCRIPTION}

    def get_analysis_tools(self) -> str:

        return self.analysis_tools

    def choose_analysis(self, state: dict) -> dict:
        """Choose the appropriate analysis tool based on the user's question"""
        question = state["question"]
        parsed_question = state["parsed_question"]

        if not parsed_question["require_analysis"]:
            return {"relevant_analysis_tools": []}

        analysis_tools = parsed_question["relevant_analysis_tools"]

        tool_description = {}
        for tool in analysis_tools:
            for specific_tool in eval(tool).TOOL_LIST:
                argument = {}
                specific_tool_instance = specific_tool()
                specific_tool_name = specific_tool_instance.__class__.__name__
                specific_tool_description = (
                    specific_tool_instance.get_specific_description()
                )
                tool_description[specific_tool_name] = {
                    "analysis_type": tool,
                    "description": specific_tool_description,
                    "argument": specific_tool_instance.get_argument_explanation(),
                    "input_requirements": specific_tool_instance.get_input_requirements(),
                }

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are an Data scientist. You are given a question and a list of analysis tools that can be used to answer the question.
                    You need to choose the most appropriate analysis tool that can answer the question.
                    You need to return the analysis tool name and the arguments for the analysis tool.
                    
                    Respond in JSON format with the following structure. Only respond with the JSON:
                    {{
                        "selected_analysis": [
                            {{
                                "analysis_type": string,
                                "analysis_name": string,
                                "required_input": string,
                                "arguments": {{
                                    "argument_name": string,
                                    "argument_value": string
                                }}
                            }}
                        ]
                    }}
                    """,
                ),
                (
                    "human",
                    """
                    ===Question: 
                    {question}
                    ===Analysis tools: 
                    {tool_description}
                    
                    """,
                ),
            ]
        )
        output_parser = JsonOutputParser()
        response = self.llm_manager.invoke(
            prompt,
            question=question,
            tool_description=tool_description,
        )
        result = output_parser.parse(response)

        return result

    def execute_analysis(self, state: dict) -> dict:
        """Execute the analysis tool and return the results"""
        sql_query = state["sql_query"]
        input_data = self.db_manager.execute_query_as_df(sql_query)

        analysis = state["analysis"]["selected_analysis"]
        results = {}
        for analysis_tool in analysis:
            analysis_type = analysis_tool["analysis_type"]
            analysis_name = analysis_tool["analysis_name"]
            required_input = analysis_tool["required_input"]
            arguments = analysis_tool["arguments"]
            arguments = {arguments["argument_name"]: arguments["argument_value"]}
            analysis_type = analysis_type + "." + analysis_name
            analysis_tool = eval(analysis_type)
            analysis_tool_instance = analysis_tool(
                input_data=input_data, argument=arguments
            )
            error = analysis_tool_instance.check_input_schema()
            if "error" in error:
                return {"error": error["error"]}
            result = analysis_tool_instance.execute_analysis()
            results[analysis_name] = result

        return {"analysis_results": results}


if __name__ == "__main__":
    analysis_agent = AnalysisAgent()

    # example_state = {
    #     "analysis": {
    #         "selected_analysis": [
    #             {
    #                 "analysis_type": "correlation",
    #                 "analysis_name": "NormalCorrelationAnalysis",
    #                 "required_input": "input_data",
    #                 "arguments": {"method": "pearson"},
    #             }
    #         ]
    #     }
    # }

    # result = analysis_agent.execute_analysis(example_state)
    # print(result)
