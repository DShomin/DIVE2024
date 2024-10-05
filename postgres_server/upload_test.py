import pandas as pd
from sqlalchemy import create_engine


# 데이터베이스 연결
ENGINE_URL = "postgresql://postgres:divepassword@localhost:5432/dive2024"
engine = create_engine(ENGINE_URL)


def get_top_n_rows(table_name, n):
    sql_query = f"""
    SELECT * FROM {table_name} LIMIT {n}
    """
    df = pd.read_sql(sql_query, engine)
    return df


# top 30 rows of lotte_mart
df = get_top_n_rows("lotte_mart", 30)
print(df.head())

# top 30 rows of samsung
df = get_top_n_rows("samsung", 30)
print(df.head())

# top 30 rows of lotte_cs
df = get_top_n_rows("lotte_cs", 30)
print(df.head())

df = get_top_n_rows("survey", 30)
print(df.head())
