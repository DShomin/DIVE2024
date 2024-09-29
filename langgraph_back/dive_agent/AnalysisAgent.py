import numpy as np
import pandas as pd

from dive_agent.DatabaseManager import DatabaseManager
from dive_agent.LLMManager import LLMManager


class AnalysisAgent:
    def __init__(self):
        self.llm_manager = LLMManager()
        self.db_manager = DatabaseManager()
