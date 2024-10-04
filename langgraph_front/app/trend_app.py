import streamlit as st
import pandas as pd
import json
from dotenv import load_dotenv

from trend_agent.WorkflowManager import WorkflowManager

import plotly.express as px

load_dotenv()

st.title("LangGraph Backend")

# get user question
user_question = st.text_input("Enter your question:")
# submit button
ask_button = st.button("Ask to Agent")

if ask_button:
    with st.spinner("Working..."):
        result = WorkflowManager().run_trend_agent(user_question)
    result = result["result"]
    answer = result["output"]
    st.write(answer)
    agent_outputs = result["intermediate_steps"]
    for agent_output in agent_outputs:
        if "interest_over_time" in agent_output[1].keys():
            interest_over_time_df = agent_output[1]["interest_over_time"]
            kwords = interest_over_time_df.columns.tolist()
            # remove isPartial
            kwords = [x for x in kwords if x != "isPartial"]
            fig = px.line(
                interest_over_time_df, y=kwords, title=", ".join(kwords) + "Trend"
            )
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig)

        if "interest_by_region" in agent_output[1].keys():
            interest_by_region_df = agent_output[1]["interest_by_region"]
            region_json = json.load(
                open(
                    "/Users/ihomin/Documents/DIVE2024/langgraph_front/app/SIDO_MAP_2022.json"
                )
            )
            kwords = interest_by_region_df.columns.tolist()

            for kword in kwords:
                fig = px.choropleth_mapbox(
                    interest_by_region_df,
                    geojson=region_json,
                    locations="geoName",
                    color=kword,
                    color_continuous_scale="matter",
                    range_color=(0, 100),
                    mapbox_style="carto-positron",
                    featureidkey="properties.CTP_KOR_NM",
                    zoom=5,
                    center={"lat": 37.565, "lon": 126.986},
                    opacity=0.5,
                )
                fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
                st.plotly_chart(fig)

        if "trending_searches" in agent_output[1].keys():
            st.write(agent_output[1]["trending_searches"])
        if "top_charts" in agent_output[1].keys():
            st.write(agent_output["top_charts"])
