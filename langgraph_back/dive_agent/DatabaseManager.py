import os
import psycopg2


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
        survay_desc_dict = {
            "SQ1": "What is your gender?",
            "SQ2": "What is your age?",
            "SQ4": "Where do you currently reside?",
            "AQ1": "How satisfied are you with your current residence {SQ4}?",
            "AQ2": "Do you plan to continue living in {SQ4} in the future?",
            "AQ3_1": "If you were to move to a different area, what is the first factor you would consider?",
            "AQ3_2": "If you were to move to a different area, what is the second factor you would consider?",
            "AQ3_3": "If you were to move to a different area, what is the third factor you would consider?",
            "AQ4": "Which area would you most like to live in?",
            "BQ1": "What comes to mind when you think of 'Busan'? Please write down the images that come to mind.",
            "BQ2": "Please select all the words that come to mind when you think of 'Busan'. Please select at least 5 words. The words are separated by ','.",
            "BQ3": "How many times have you visited Busan in the last 2 years?",
            "BQ4_1": "Busan accommodation satisfaction",
            "BQ4_2": "Busan tourist attraction satisfaction",
            "BQ4_3": "Busan natural landscape satisfaction",
            "BQ4_4": "Busan leisure and cultural activities satisfaction",
            "BQ4_5": "Busan cafe and restaurant satisfaction",
            "BQ4_6": "Busan sports and leisure activities satisfaction",
            "BQ4_7": "Busan transportation convenience satisfaction",
            "BQ4_8": "Busan shopping satisfaction",
            "BQ4_9": "Busan local residents' kindness",
            "BQ4_10": "Busan overall satisfaction",
            "BQ5": "What do you think after visiting Busan?",
            "BQ6": "How many more times do you plan to visit Busan in the future?",
            "BQ7_1": "What was the first thing you liked about Busan?",
            "BQ7_2": "What was the second thing you liked about Busan?",
            "BQ7_3": "What was the third thing you liked about Busan?",
            "BQ8": "What kind of festival did you visit in Busan? If you have experienced several festivals, please select only one festival that you visited most recently.",
            "BQ9": "When you enjoyed the festival in Busan, who did you enjoy the festival with?",
            "BQ10_1": "How satisfied were you with the {BQ8} in Busan? Event program",
            "BQ10_2": "How satisfied were you with the {BQ8} in Busan? Surrounding control and safety/security",
            "BQ10_3": "How satisfied were you with the {BQ8} in Busan? Transportation environment (accessibility, parking, etc.)",
            "BQ10_4": "How satisfied were you with the {BQ8} in Busan? Convenience/rest facilities",
            "BQ10_5": "How satisfied were you with the {BQ8} in Busan? Surrounding environment (cleanliness, hygiene, etc.)",
            "BQ10_6": "How satisfied were you with the {BQ8} in Busan? Cost of living/price level",
            "BQ10_7": "How satisfied were you with the {BQ8} in Busan? Overall satisfaction",
            "BQ11": "How did your image of Busan change after visiting {BQ8}?",
            "BQ12": "How likely are you to visit Busan again to enjoy {BQ8}?",
            "CQ1": "Have you ever experienced a workation in Busan?",
            "CQ3_1_merged": "What is the reason you experienced a workation in Seoul? (The value is included in the list.)",
            "CQ3_2_merged": "What is the reason you experienced a workation in Busan? (The value is included in the list.)",
            "CQ3_3_merged": "What is the reason you experienced a workation in Incheon? (The value is included in the list.)",
            "CQ3_4_merged": "What is the reason you experienced a workation in Daegu? (The value is included in the list.)",
            "CQ3_5_merged": "What is the reason you experienced a workation in Daejeon? (The value is included in the list.)",
            "CQ3_6_merged": "What is the reason you experienced a workation in Gwangju? (The value is included in the list.)",
            "CQ3_7_merged": "What is the reason you experienced a workation in Ulsan? (The value is included in the list.)",
            "CQ3_8_merged": "What is the reason you experienced a workation in Gyeonggi-do? (The value is included in the list.)",
            "CQ3_9_merged": "What is the reason you experienced a workation in Chungcheongbuk-do? (The value is included in the list.)",
            "CQ3_10_merged": "What is the reason you experienced a workation in Chungcheongnam-do? (The value is included in the list.)",
            "CQ3_11_merged": "What is the reason you experienced a workation in Jeollabuk-do? (The value is included in the list.)",
            "CQ3_12_merged": "What is the reason you experienced a workation in Jeollanam-do? (The value is included in the list.)",
            "CQ3_13_merged": "What is the reason you experienced a workation in Gyeongsangbuk-do? (The value is included in the list.)",
            "CQ3_14_merged": "What is the reason you experienced a workation in Gyeongsangnam-do? (The value is included in the list.)",
            "CQ3_15_merged": "What is the reason you experienced a workation in Gangwon-do? (The value is included in the list.)",
            "CQ3_16_merged": "What is the reason you experienced a workation in Sejong Special Self-Governing City? (The value is included in the list.)",
            "CQ3_17_merged": "What is the reason you experienced a workation in Jeju Special Self-Governing Province? (The value is included in the list.)",
            "CQ4": "Do you plan to experience a workation in the future?",
            "CQ5_1": "What is the first factor you consider when you experience a workation?",
            "CQ5_2": "What is the second factor you consider when you experience a workation?",
            "CQ5_3": "What is the third factor you consider when you experience a workation?",
            "CQ6": "How likely are you to experience a workation in Busan?",
        }
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
            "survey": """
            This table contains survey data on the perception of Busan and migration to Busan. 
            - SQ1: "What is your gender?",
            - SQ2: "What is your age?",
            - SQ4: "Where do you currently reside?",
            - AQ1: "How satisfied are you with your current residence {SQ4}?",
            - AQ2: "Do you plan to continue living in {SQ4} in the future?",
            - AQ3_1: "If you were to move to a different area, what is the first factor you would consider?",
            - AQ3_2: "If you were to move to a different area, what is the second factor you would consider?",
            - AQ3_3: "If you were to move to a different area, what is the third factor you would consider?",
            - AQ4: "Which area would you most like to live in?",
            - BQ1: "What comes to mind when you think of 'Busan'? Please write down the images that come to mind.",
            - BQ2: "Please select all the words that come to mind when you think of 'Busan'. Please select at least 5 words. The words are separated by ','.",
            - BQ3: "How many times have you visited Busan in the last 2 years?",
            - BQ4_1: "Busan accommodation satisfaction",
            - BQ4_2: "Busan tourist attraction satisfaction",
            - BQ4_3: "Busan natural landscape satisfaction",
            - BQ4_4: "Busan leisure and cultural activities satisfaction",
            - BQ4_5: "Busan cafe and restaurant satisfaction",
            - BQ4_6: "Busan sports and leisure activities satisfaction",
            - BQ4_7: "Busan transportation convenience satisfaction",
            - BQ4_8: "Busan shopping satisfaction",
            - BQ4_9: "Busan local residents' kindness",
            - BQ4_10: "Busan overall satisfaction",
            - BQ5: "What do you think after visiting Busan?",
            - BQ6: "How many more times do you plan to visit Busan in the future?",
            - BQ7_1: "What was the first thing you liked about Busan?",
            - BQ7_2: "What was the second thing you liked about Busan?",
            - BQ7_3: "What was the third thing you liked about Busan?",
            - BQ8: "What kind of festival did you visit in Busan? If you have experienced several festivals, please select only one festival that you visited most recently.",
            - BQ9: "When you enjoyed the festival in Busan, who did you enjoy the festival with?",
            - BQ10_1: "How satisfied were you with the {BQ8} in Busan? Event program",
            - BQ10_2: "How satisfied were you with the {BQ8} in Busan? Surrounding control and safety/security",
            - BQ10_3: "How satisfied were you with the {BQ8} in Busan? Transportation environment (accessibility, parking, etc.)",
            - BQ10_4: "How satisfied were you with the {BQ8} in Busan? Convenience/rest facilities",
            - BQ10_5: "How satisfied were you with the {BQ8} in Busan? Surrounding environment (cleanliness, hygiene, etc.)",
            - BQ10_6: "How satisfied were you with the {BQ8} in Busan? Cost of living/price level",
            - BQ10_7: "How satisfied were you with the {BQ8} in Busan? Overall satisfaction",
            - BQ11: "How did your image of Busan change after visiting {BQ8}?",
            - BQ12: "How likely are you to visit Busan again to enjoy {BQ8}?",
            - CQ1: "Have you ever experienced a workation in Busan?",
            - CQ3_1_merged: "What is the reason you experienced a workation in Seoul? (The value is included in the list.)",
            - CQ3_2_merged: "What is the reason you experienced a workation in Busan? (The value is included in the list.)",
            - CQ3_3_merged: "What is the reason you experienced a workation in Incheon? (The value is included in the list.)",
            - CQ3_4_merged: "What is the reason you experienced a workation in Daegu? (The value is included in the list.)",
            - CQ3_5_merged: "What is the reason you experienced a workation in Daejeon? (The value is included in the list.)",
            - CQ3_6_merged: "What is the reason you experienced a workation in Gwangju? (The value is included in the list.)",
            - CQ3_7_merged: "What is the reason you experienced a workation in Ulsan? (The value is included in the list.)",
            - CQ3_8_merged: "What is the reason you experienced a workation in Gyeonggi-do? (The value is included in the list.)",
            - CQ3_9_merged: "What is the reason you experienced a workation in Chungcheongbuk-do? (The value is included in the list.)",
            - CQ3_10_merged: "What is the reason you experienced a workation in Chungcheongnam-do? (The value is included in the list.)",
            - CQ3_11_merged: "What is the reason you experienced a workation in Jeollabuk-do? (The value is included in the list.)",
            - CQ3_12_merged: "What is the reason you experienced a workation in Jeollanam-do? (The value is included in the list.)",
            - CQ3_13_merged: "What is the reason you experienced a workation in Gyeongsangbuk-do? (The value is included in the list.)",
            - CQ3_14_merged: "What is the reason you experienced a workation in Gyeongsangnam-do? (The value is included in the list.)",
            - CQ3_15_merged: "What is the reason you experienced a workation in Gangwon-do? (The value is included in the list.)",
            - CQ3_16_merged: "What is the reason you experienced a workation in Sejong Special Self-Governing City? (The value is included in the list.)",
            - CQ3_17_merged: "What is the reason you experienced a workation in Jeju Special Self-Governing Province? (The value is included in the list.)",
            - CQ4: "Do you plan to experience a workation in the future?",
            - CQ5_1: "What is the first factor you consider when you experience a workation?",
            - CQ5_2: "What is the second factor you consider when you experience a workation?",
            - CQ5_3: "What is the third factor you consider when you experience a workation?",
            - CQ6: "How likely are you to experience a workation in Busan?",
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


if __name__ == "__main__":
    db = DatabaseManager()

    print(db.get_table_schema())
