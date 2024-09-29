from dive_agent.WorkflowManager import WorkflowManager
from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":
    # 연간 총소비량을 직업에서 '02.회사원'와 '01.전문직'을 그래프로 보여줘
    result = WorkflowManager().run_sql_agent(
        "Show the total consumption trend by occupation as a line graph, ordered by year. The occupations are '02.회사원' and '01.전문직'."
    )
    print(result)
