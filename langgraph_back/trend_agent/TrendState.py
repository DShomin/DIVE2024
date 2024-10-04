from typing import List, Any, Annotated, Dict, Optional
from typing_extensions import TypedDict
import operator
import pandas as pd


class InputState(TypedDict):
    question: str
    # agent_scratchpad: str


class OutputState(TypedDict):
    interest_over_time: pd.DataFrame
    interest_by_region: pd.DataFrame
    trending_searches: Dict[str, Any]
    top_charts: Dict[str, Any]
    result: Dict[str, Any]
