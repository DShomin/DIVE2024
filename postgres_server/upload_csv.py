import pandas as pd

from survey_pre_process import pre_process_survey

from sqlalchemy import create_engine, Integer, Float, String, Date
from sqlalchemy.types import TypeEngine
import os

# 데이터베이스 연결
endpoint_url = "postgresql://postgres:divepassword@localhost:5432/dive2024"
engine = create_engine(endpoint_url)


# CSV 파일 경로 설정
upload_list = [
    # {
    #     "name": "lotte_mart",
    #     "path": "../data/DB/lotte/003_ltmb_mart_data.csv",
    # },
    # {
    #     "name": "lotte_cs",
    #     "path": "../data/DB/lotte/002_ltmb_k7_data.csv",
    # },
    # {
    #     "name": "samsung",
    #     "path": "../data/DB/samsung/DIVE_FINAL_F.csv",
    # },
    {
        "name": "survey",
        "path": "../data/DB/lotte/006_ltmb_lime_data.xlsx",
    },
]


def type_update_df(table_name: str, df: pd.DataFrame) -> pd.DataFrame:
    """Date column type change"""
    if table_name == "lotte_mart" or table_name == "lotte_cs":
        df["stdt"] = pd.to_datetime(df["stdt"], format="%Y%m")
        df["bcode1"] = df["bcode1"].astype("category")
    elif table_name == "samsung":
        df["CRI_YM"] = pd.to_datetime(df["CRI_YM"], format="%Y%m")
        df["GENDER"] = df["GENDER"].astype("category")

    return df


def optimize_df(table_name: str, df: pd.DataFrame) -> pd.DataFrame:
    """Optimize the dataframe for the database"""
    df = df.dropna()

    df = type_update_df(table_name, df)

    # 문자열 컬럼 최적화
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype("category")

    # 숫자형 컬럼 최적화
    for col in df.select_dtypes(include=["int64", "float64"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="integer")

    return df


def get_column_type(col_name: str, dtype: str) -> TypeEngine:
    """컬럼 이름과 데이터 타입에 따라 적절한 SQLAlchemy 타입 반환"""
    if "int" in str(dtype):
        if col_name in ["stdt", "CRI_YM"]:  # 날짜 컬럼
            return Date
        elif df[col_name].max() < 2147483647 and df[col_name].min() > -2147483648:
            return Integer
        else:
            return Float  # bigint 대신 Float 사용
    elif "float" in str(dtype):
        return Float
    else:
        return String(length=255)  # 문자열 길이 제한


for csv_file in upload_list:
    print(f"Uploading {csv_file['name']} to database")
    print(f"Target path: {csv_file['path']}")
    if csv_file["name"] == "survey":
        df = pd.read_excel(csv_file["path"], sheet_name="DATA")
        df = pre_process_survey(df)
    else:
        df = pd.read_csv(csv_file["path"])
        df = optimize_df(csv_file["name"], df)
    dtype = {col: get_column_type(col, df[col].dtype) for col in df.columns}
    df.to_sql(csv_file["name"], engine, if_exists="replace", index=False, dtype=dtype)

print("Upload complete")
