import os
import psycopg2
import pandas as pd
import sqlalchemy


class DatabaseManager:
    def __init__(self):
        self.connect = self.db_connection()

    def db_connection(self):
        try:
            return psycopg2.connect(
                database="dive2024",
                user="postgres",
                password="divepassword",
                host="host.docker.internal",  # localhost
                port=5432,
            )
        except Exception as e:
            print(e)
            print("Connecting to local database")
            return psycopg2.connect(
                database="dive2024",
                user="postgres",
                password="divepassword",
                host="localhost",  # localhost
                port=5432,
            )

    def get_table_names(self):
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        with self.connect.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def get_table_description(self):
        """
        lotte_mart and lotte_cs dataframe description
        stdt : 구매 년월 <거래 발생 년월>
        channel : 구매 채널 <마트, 편의점 2개 채널 존재>
        ch_region : 점포 위치 <소비자의 거래 발생 지역>
        bcode1 : 구매 상품 대분류코드 <>
        bname1 : 구매 상품 대분류명 <소비자의 구매 상품 대분류> (bcode1와 bname1 1:1 매칭)
        count : 구매 건수 <몇개 구매했는지 의미하는 것으로 추정>
        money : 구매 금액 <몇원 구매했는지 의미하는 것으로 추정>
        ppl : 구매자 수 <몇명 구매했는지 의미하는 것으로 추정>
        age : 구매자 연령대 <1대 이하 : 10, 20대 이하 : 20 ... 60 : 60대 이상>
        region : 거주지 지역 <구매자의 거주지 지역>
        ---
        samsung dataframe description
        사용처의 제한은 없으나 삼성카드를 사용한 거래만 추출하였음
        CRI_YM : 기준연월 <거래 발생 년월>
        MRC_ADR : 가맹점소재지 <거래 발생 지역>
        GENDER : 성별
        AGE_GR : 연령대 <각 코드가 어디 연령대를 의미하는지 문의 필요함>
        JOB_GR : 직업군 <소비자의 직업군>
        CATEGORY_M_NM : 중분류 업종명 <가맹점 거래 발생 업종>
        CATEGORY_L_NM : 대분류 업종명 <가맹점 거래 발생 업종>
        MAIN_CSM_AREA : 소비자 주요 카드 사용 지역 <소비자 여행인지 아닌지 판단 가능할 것으로 보임>
        """
        return {
            "lotte_mart": """
            This table contains data about purchases made at Lotte Mart stores.
            The table has the following columns:
            - stdt: Purchase date (year and month)
            - channel: Purchase channel (likely either '마트' or '편의점')
            - ch_region: Store location (likely the consumer's location where the purchase was made)
            - bcode1: Purchase product category code (likely a code for the product category)
            - bname1: Purchase product category name (likely the name of the product category)
            - count: Purchase quantity (likely the number of items purchased)
            - money: Purchase amount (likely the amount of money spent on the purchase)
            - ppl: Number of consumers (likely the number of consumers who made the purchase)
            - age: Age group (likely the age group of the consumer)
            - region: Consumer's main card usage area (likely the main area where the consumer uses their card)
            """,
            "lotte_cs": """
            This table contains data about purchases made at convenience stores.
            The table has the following columns:
            - stdt: Purchase date (year and month)
            - channel: Purchase channel (likely either '마트' or '편의점')
            - ch_region: Store location (likely the consumer's location where the purchase was made)
            - bcode1: Purchase product category code (likely a code for the product category)
            - bname1: Purchase product category name (likely the name of the product category)
            - count: Purchase quantity (likely the number of items purchased)
            - money: Purchase amount (likely the amount of money spent on the purchase)
            - ppl: Number of consumers (likely the number of consumers who made the purchase)
            - age: Age group (likely the age group of the consumer)
            - region: Consumer's main card usage area (likely the main area where the consumer uses their card)
            """,
            "samsung": """
            This table contains data about transactions made with Samsung cards.
            The table has the following columns:
            - CRI_YM: Transaction date (year and month)
            - MRC_ADR: Transaction location (likely the consumer's location where the transaction was made)
            - GENDER: Gender (likely the gender of the consumer)
            - AGE_GR: Age group (likely the age group of the consumer)
            - JOB_GR: Job group (likely the job group of the consumer)
            - CATEGORY_M_NM: Medium category name (likely the name of the medium category of the transaction)
            - CATEGORY_L_NM: Large category name (likely the name of the large category of the transaction)
            - MAIN_CSM_AREA: Consumer's main card usage area (likely the main area where the consumer uses their card)
            """,
        }

    def get_table_schema(self):

        table_names = [table[0] for table in self.get_table_names()]
        results = {}
        for table_name in table_names:
            sql = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';"
            results[table_name] = self.execute_query(sql)
        return results

    def execute_query(self, query):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                return results
        except Exception as e:
            raise Exception(f"Error executing query: {e}")

    def execute_query_as_df(self, query):
        db_info = self.connect.info.dsn_parameters
        engine = sqlalchemy.create_engine(
            f"postgresql://{db_info['user']}:divepassword@{db_info['host']}:{db_info['port']}/dive2024"
        )
        return pd.read_sql_query(query, engine)


if __name__ == "__main__":
    db = DatabaseManager()

    # print(db.get_table_schema())
    df = db.execute_query_as_df("SELECT * FROM lotte_mart limit 10;")
    print(df)
