from langgraph.graph import StateGraph, END, START
from trend_agent.TrendAgent import TrendAgent
from trend_agent.TrendState import InputState, OutputState


class WorkflowManager:
    def __init__(self):
        self.trend_agent = TrendAgent()

    def create_workflow(self) -> StateGraph:
        workflow = StateGraph(input=InputState, output=OutputState)

        # Add nodes to the graph
        workflow.add_node("trendagent_executor", self.trend_agent.trendagent_executor)

        workflow.add_edge(START, "trendagent_executor")
        workflow.add_edge("trendagent_executor", END)

        return workflow

    def returnGraph(self):
        return self.create_workflow().compile()

    def run_trend_agent(self, question: str):
        return self.trend_agent.trendagent_executor(question)


from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":
    app = WorkflowManager().returnGraph()
    result = app.invoke(
        {"question": "전포와 광안리의 검색 트랜드 차이를 확인하고 싶다."}
    )
    print("result: ", result)
