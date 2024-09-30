import numpy as np
import pandas as pd

from typing import Dict
from dive_agent.DatabaseManager import DatabaseManager
from dive_agent.LLMManager import LLMManager
from dive_agent.Analyses import correlation


class AnalysisAgent:
    def __init__(self):
        self.llm_manager = LLMManager()
        self.db_manager = DatabaseManager()

        self.analysis_tools = {"correlation": correlation.BASE_DESCRIPTION}

    def get_analysis_tools(self) -> Dict[str, str]:

        return self.analysis_tools
