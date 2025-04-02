from pytrends.request import TrendReq
from serpapi import GoogleSearch
import pandas as pd
import os

from langchain_core.tools import tool

from typing import List, Union, Annotated, Dict


def init_pytrends():
    pytrends = TrendReq(hl="ko", tz=300, geo="KR")
    return pytrends


def get_perapi_params():
    serpapi_params = {
        "engine": "google_trends",
        "geo": "KR",
        "hl": "ko",
        "api_key": os.getenv("SERPAPI_KEY"),
    }
    return serpapi_params


@tool()
def get_trends_by_keyword(
    keyword: Annotated[Union[str, List[str]], "keyword to get trends data"],
    timeframe: Annotated[str, "timeframe to get trends data"],
    category: Annotated[int, "category to get trends data"],
) -> Dict[str, pd.DataFrame]:
    """
    This is used to obtain the search trend of a keyword in a specific time or a specific category.

    :param keyword: str or list of str, keyword to get trends data if you want to get multiple keywords, you can use list for example "전포, 광안리"
    :param timeframe: str, timeframe to get trends data (e.g. '2024-01-01 2024-01-31')
    :param category: int, category to get trends data
    :return: tuple of Dataframe, Dataframe, Dataframe
    """
    pytrends = init_pytrends()
    if isinstance(keyword, str):
        keyword = [keyword]

    if ", " in keyword:
        keyword = keyword.split(", ")

    try:
        pytrends.build_payload(
            kw_list=keyword,
            timeframe=timeframe,
            geo="KR",
            cat=category,
        )
        interest_over_time = pytrends.interest_over_time()
        interest_by_region = pytrends.interest_by_region(inc_low_vol=True)

        interest_by_region.index.set_names("geoName", inplace=True)
        interest_by_region.reset_index(inplace=True)
        # interest_over_time_fig = px.line(
        #     interest_over_time, y=keyword, title="Search Trend"
        # )
        # interest_over_time_fig.update_layout(hovermode="x unified")
        return {
            "interest_over_time": interest_over_time,
            "interest_by_region": interest_by_region,
        }
    except Exception as e:
        print(e)
        return {}, {}


@tool()
def get_today_trends():
    """
    This is used to obtain today's trends data from Google Trends.
    :return: Dataframe
    """
    pytrends = init_pytrends()
    try:
        return {
            "trending_searches": pytrends.trending_searches(pn="south_korea").to_dict()
        }
    except Exception as e:
        print(e)
        return {}


@tool()
def get_history_trends(date: Annotated[int, "date to get history trends data"]):
    """
    This is used to obtain history trends data from Google Trends.
    :param date: int, date to get history trends data (e.g. 2023)
    It cannot use this year 2024
    :return: Dataframe
    """
    pytrends = init_pytrends()
    if date >= 2024:
        raise ValueError("Cannot use over this year")
    try:
        return {
            "top_charts": pytrends.top_charts(date, hl="ko", tz=300, geo="KR").to_dict()
        }
    except Exception as e:
        print(e)
        return {}


def get_category() -> dict:
    """
    Get category data from Google Trends
    :return: dict
    """
    pytrends = init_pytrends()
    return {"available_categories": pytrends.categories().to_dict()}


def get_suggestions(keyword: str):
    """
    get suggestions from google trends
    """
    pytrends = init_pytrends()
    try:
        return {"suggestions": pytrends.suggestions(keyword).to_dict()}
    except Exception as e:
        print(e)
        return {}


def get_related_topics(keyword: str, date: str):
    """
    serpapi를 사용하여 관련 주제를 가져옵니다.
    """
    serpapi_params = get_perapi_params()
    serpapi_params["q"] = keyword
    serpapi_params["date"] = date
    serpapi_params["data_type"] = "RELATED_TOPICS"

    search = GoogleSearch(serpapi_params)
    try:
        result = search.get_dict()
        related_topics = result["related_topics"]
    except Exception as e:
        print(e)
        return {"top_topics": [], "rising_topics": []}

    top_topics = [
        {
            "title": topic["topic"]["title"],
            "type": topic["topic"]["type"],
            "value": topic["value"],
        }
        for topic in related_topics["top"]
    ]
    rising_topics = [
        {
            "title": topic["topic"]["title"],
            "type": topic["topic"]["type"],
            "value": topic["value"],
        }
        for topic in related_topics["rising"]
    ]
    return {
        "top_topics": top_topics,
        "rising_topics": rising_topics,
    }


def get_related_queries(keyword: str, date: str):
    """
    serpapi를 사용하여 관련 쿼리를 가져옵니다.
    """
    serpapi_params = get_perapi_params()
    serpapi_params["q"] = keyword
    serpapi_params["date"] = date
    serpapi_params["data_type"] = "RELATED_QUERIES"

    search = GoogleSearch(serpapi_params)
    try:
        result = search.get_dict()
        related_queries = result["related_queries"]
    except Exception as e:
        print(e)
        return {"top_queries": [], "rising_queries": []}
    top_queries = [
        {
            "title": query["query"],
            "value": query["value"],
        }
        for query in related_queries["top"]
    ]
    rising_queries = [
        {
            "title": query["query"],
            "value": query["value"],
        }
        for query in related_queries["rising"]
    ]

    return {
        "top_queries": top_queries,
        "rising_queries": rising_queries,
    }
