import streamlit as st
import pandas as pd
from dotenv import load_dotenv

import plotly.express as px

from dive_agent.WorkflowManager import WorkflowManager

load_dotenv()

st.title("LangGraph Backend")

# get user question
user_question = st.text_input("Enter your question:")
# submit button
ask_button = st.button("Ask to Agent")

if ask_button:
    with st.spinner("Working..."):
        result = WorkflowManager().run_sql_agent(user_question)

    answer = result["answer"]
    visualization_type = result["visualization"]
    print(result["formatted_data_for_visualization"])
    # bar, horizontal_bar, line, pie, scatter, none
    if result["visualization"] != "none":

        visualization_data = result["formatted_data_for_visualization"]
        viz_df = None
        if visualization_type == "bar":
            viz_df = pd.DataFrame()
            for data in visualization_data["values"]:
                new_df = pd.DataFrame(data)
                new_df["labels"] = visualization_data["labels"]
                viz_df = pd.concat([viz_df, new_df])
            if "label" in viz_df.columns:
                fig = px.bar(viz_df, x="labels", y="data", color="label")
            else:
                fig = px.bar(viz_df, x="labels", y="data")
            st.plotly_chart(fig)

        elif visualization_type == "horizontal_bar":
            viz_df = pd.DataFrame()
            for data in visualization_data["values"]:
                new_df = pd.DataFrame(data)
                new_df["labels"] = visualization_data["labels"]
                viz_df = pd.concat([viz_df, new_df])
            if len(visualization_data["values"]) > 1:
                fig = px.bar(
                    viz_df, x="labels", y="data", color="label", orientation="h"
                )
            else:
                fig = px.bar(viz_df, x="labels", y="data", orientation="h")
            st.plotly_chart(fig)

        elif visualization_type == "line":
            viz_df = pd.DataFrame()
            if "yAxisLabel" in visualization_data:
                yAxisLabel = visualization_data["yAxisLabel"]
            else:
                yAxisLabel = None

            if len(visualization_data["yValues"]) == 1:
                viz_df["xValues"] = visualization_data["xValues"]
                y_name = visualization_data["yValues"][0]["label"]
                y_data = visualization_data["yValues"][0]["data"]
                viz_df[y_name] = y_data
                fig = px.line(viz_df, x="xValues", y=y_name)
            else:
                for data in visualization_data["yValues"]:
                    # if list is all None, then skip
                    if all(value is None for value in data["data"]):
                        continue

                    new_dict = {
                        "label": data["label"],
                        "data": data["data"],
                    }
                    new_df = pd.DataFrame(new_dict)
                    new_df["xValues"] = visualization_data["xValues"]
                    viz_df = pd.concat([viz_df, new_df])
                fig = px.line(viz_df, x="label", y="data", color="xValues")

            if yAxisLabel is not None:
                fig.update_layout(
                    yaxis_title=yAxisLabel,
                )
            st.plotly_chart(fig)

        elif visualization_type == "pie":
            viz_df = pd.DataFrame(visualization_data)

            fig = px.pie(viz_df, names="label", values="value")
            st.plotly_chart(fig)
        elif visualization_type == "scatter":
            viz_df = pd.DataFrame(
                [
                    {
                        "x": point["x"],
                        "y": point["y"],
                        "id": point["id"],
                        "gender": series["label"],
                    }
                    for series in visualization_data["series"]
                    for point in series["data"]
                ]
            )
            fig = px.scatter(viz_df)
            st.plotly_chart(fig)

    st.write(answer)

    # if viz_df is not None:
    #     show_table = st.toggle("Show Table", False)
    #     if show_table:
    #         st.write(viz_df)
