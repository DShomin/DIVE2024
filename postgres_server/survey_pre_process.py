import pandas as pd


def map_column(survey_df: pd.DataFrame, column: list, code_dict: dict):
    for col in column:
        survey_df[col] = survey_df[col].map(code_dict)
    return survey_df


def pre_process_survey(survey_df: pd.DataFrame) -> pd.DataFrame:
    region_column = [
        "SQ4",
        "AQ4",
        "CQ2_1",
        "CQ2_2",
        "CQ2_3",
        "CQ2_4",
        "CQ2_5",
        "CQ2_6",
        "CQ2_7",
        "CQ2_8",
        "CQ2_9",
        "CQ2_10",
        "CQ2_11",
        "CQ2_12",
        "CQ2_13",
        "CQ2_14",
        "CQ2_15",
        "CQ2_16",
        "CQ2_17",
    ]

    region_code_dict = {
        1: "서울특별시",
        2: "부산광역시",
        3: "인천광역시",
        4: "대구광역시",
        5: "대전광역시",
        6: "광주광역시",
        7: "울산광역시",
        8: "경기도",
        9: "충청북도",
        10: "충청남도",
        11: "전라북도",
        12: "전라남도",
        13: "경상북도",
        14: "경상남도",
        15: "강원도",
        16: "세종특별자치시",
        17: "제주특별자치도",
    }

    survey_df = map_column(survey_df, region_column, region_code_dict)

    # drop column
    occ_column = ["SQ3_1", "SQ3_2", "SQ3_3", "SQ3_4", "SQ3_9999"]
    survey_df.drop(columns=occ_column, inplace=True)

    #
    current_home_satisfaction_column = ["AQ1"]

    current_home_satisfaction_code_dict = {
        1: "전혀 만족하지 않는다",
        2: "만족하지 않는 편이다",
        3: "보통이다",
        4: "만족하는 편이다",
        5: "매우 만족한다",
    }

    survey_df = map_column(
        survey_df, current_home_satisfaction_column, current_home_satisfaction_code_dict
    )

    wish_move_column = ["AQ2"]
    wish_move_code_dict = {
        1: "전혀 그렇지 않다",
        2: "그렇지 않다",
        3: "보통이다",
        4: "그렇다",
        5: "매우 그렇다",
    }

    survey_df = map_column(survey_df, wish_move_column, wish_move_code_dict)

    moving_reson_column = ["AQ3_1", "AQ3_2", "AQ3_3"]
    moving_reson_code_dict = {
        1: "일자리(취업/창업 등)",
        2: "교통환경(대중교통, 고속도로 인접, 주차 등)",
        3: "주변 상권",
        4: "병·의원 시설",
        5: "교육 시설",
        6: "지역의 지원 정책(이주비 지원, 세금감면 등)",
        7: "연고(출생지, 성장지, 거주지 등)",
        8: "부동산 가격",
    }
    survey_df = map_column(survey_df, moving_reson_column, moving_reson_code_dict)
    busan_opinion_column = [
        "BQ2_1",
        "BQ2_2",
        "BQ2_3",
        "BQ2_4",
        "BQ2_5",
        "BQ2_6",
        "BQ2_7",
        "BQ2_8",
        "BQ2_9",
        "BQ2_10",
        "BQ2_11",
        "BQ2_12",
        "BQ2_13",
        "BQ2_14",
        "BQ2_15",
        "BQ2_16",
        "BQ2_17",
        "BQ2_18",
        "BQ2_19",
        "BQ2_20",
        "BQ2_21",
        "BQ2_22",
        "BQ2_23",
        "BQ2_24",
        "BQ2_25",
        "BQ2_26",
        "BQ2_27",
        "BQ2_28",
        "BQ2_29",
        "BQ2_30",
    ]
    busan_opinion_code_dict = {
        1: "고급스러운/품격있는",
        2: "글로벌한",
        3: "깨끗한/위생적인",
        4: "독특한/차별화된",
        5: "따뜻한",
        6: "맛있는",
        7: "믿을 수 있는/신뢰가 가는",
        8: "복잡한",
        9: "사회에 공헌하는",
        10: "새로운",
        11: "소통하는",
        12: "스마트한",
        13: "아름다운",
        14: "안전한",
        15: "예술적인",
        16: "자유로운",
        17: "재미있는/즐거운",
        18: "전문적인",
        19: "전통적인",
        20: "젊은",
        21: "친근한/친숙한",
        22: "친절한",
        23: "트렌디한",
        24: "포용하는",
        25: "편리한",
        26: "함께하는/상생하는",
        27: "행복한",
        28: "혁신적인/선도하는",
        29: "환경 친화적인",
        30: "활기찬/역동적인",
    }
    # change column as bool type
    survey_df[busan_opinion_column] = survey_df[busan_opinion_column].notnull()
    for col in busan_opinion_column:
        new_ele = busan_opinion_code_dict[int(col.split("_")[1])]
        # if True change to new_ele else empty string
        survey_df[col] = survey_df[col].apply(lambda x: new_ele if x else "")
    survey_df["BQ2"] = (
        survey_df[busan_opinion_column].apply(lambda x: ", ".join(x), axis=1).copy()
    )
    survey_df["BQ2"] = (
        survey_df["BQ2"]
        .apply(lambda x: ", ".join([i for i in x.split(",") if i.strip()]))
        .copy()
    )
    # drop column
    survey_df.drop(columns=busan_opinion_column, inplace=True)

    # parse visit count column
    # BQ3의 값이 없으면 0으로
    survey_df["BQ3"] = survey_df["BQ3"].fillna(0)
    # BQ3_9 삭제
    survey_df.drop(columns=["BQ3_9"], inplace=True)

    # parse satisfaction about travel column
    satisfaction_busan_column = [
        "BQ4_1",
        "BQ4_2",
        "BQ4_3",
        "BQ4_4",
        "BQ4_5",
        "BQ4_6",
        "BQ4_7",
        "BQ4_8",
        "BQ4_9",
        "BQ4_10",
    ]
    satisfaction_busan_column_code = {
        1: "매우 불만족 스러웠다",
        2: "다소 불만족 스러웠다",
        3: "보통이다",
        4: "대체로 만족했다",
        5: "매우 만족했다",
        9: "해당사항 없음",
    }
    survey_df = map_column(
        survey_df, satisfaction_busan_column, satisfaction_busan_column_code
    )
    after_travel_image_change_column = ["BQ5"]
    after_travel_image_change_code_dict = {
        1: "매우 나빠졌다",
        2: "전보다 나빠진 편이다",
        3: "변함없다",
        4: "전보다 좋아진 편이다",
        5: "매우 좋아졌다",
    }
    survey_df = map_column(
        survey_df, after_travel_image_change_column, after_travel_image_change_code_dict
    )

    more_visit_intention_column = ["BQ6"]
    more_visit_intention_code_dict = {
        1: "전혀 그렇지 않다",
        2: "그렇지 않는 편이다",
        3: "보통이다",
        4: "그런 편이다",
        5: "매우 그렇다",
    }
    survey_df = map_column(
        survey_df, more_visit_intention_column, more_visit_intention_code_dict
    )

    satisfaction_travel_column = ["BQ7_1", "BQ7_2", "BQ7_3"]
    satisfaction_travel_column_code = {
        1: "숙박환경(가격, 위치, 숙소 컨디션 등)",
        2: "유명 관광명소",
        3: "근처 자연경관(바다, 산 등)",
        4: "여가·문화활동",
        5: "카페·맛집",
        6: "스포츠·레저활동(서핑, 루지 등)",
        7: "교통 편의성(대중교통, 주차 등)",
        8: "쇼핑",
        9: "지역주민의 친절",
    }
    survey_df = map_column(
        survey_df, satisfaction_travel_column, satisfaction_travel_column_code
    )

    festival_column = ["BQ8"]
    festival_code_dict = {
        1: "특산품/먹거리 축제(커피, 맥주, 수산 등)",
        2: "자연환경/관광 명소 축제(해돋이, 모래 축제 등)",
        3: "지역 영화제",
        4: "음악 축제",
        5: "나이트 페스티벌(드론쇼/불꽃축제/빛 축제 등)",
        6: "워터 페스티벌",
        7: "문화예술 페스티벌(비엔날레 등)",
        9997: "기타",
        9999: "방문해 본 축제 없음",
    }
    survey_df = map_column(survey_df, festival_column, festival_code_dict)

    travel_companion_column = ["BQ9"]
    travel_companion_code_dict = {
        1: "친구",
        2: "가족",
        3: "연인",
        4: "회사동료",
        5: "혼자",
    }
    survey_df = map_column(
        survey_df, travel_companion_column, travel_companion_code_dict
    )

    specific_satisfaction_column = [
        "BQ10_1",
        "BQ10_2",
        "BQ10_3",
        "BQ10_4",
        "BQ10_5",
        "BQ10_6",
        "BQ10_7",
    ]
    specific_satisfaction_column_code_dict = {
        1: "매우 불만족 스러웠다",
        2: "다소 불만족 스러웠다",
        3: "보통이다",
        4: "대체로 만족했다",
        5: "매우 만족했다",
    }
    survey_df = map_column(
        survey_df, specific_satisfaction_column, specific_satisfaction_column_code_dict
    )
    after_travel_image_change_column = ["BQ11"]
    after_travel_image_change_code_dict = {
        1: "매우 나빠졌다",
        2: "전보다 나빠진 편이다",
        3: "변함없다",
        4: "전보다 좋아진 편이다",
        5: "매우 좋아졌다",
    }
    survey_df = map_column(
        survey_df, after_travel_image_change_column, after_travel_image_change_code_dict
    )
    join_festival_intention_column = ["BQ12"]
    join_festival_intention_code_dict = {
        1: "전혀 그렇지 않다",
        2: "그렇지 않는 편이다",
        3: "보통이다",
        4: "그런 편이다",
        5: "매우 그렇다",
    }
    survey_df = map_column(
        survey_df, join_festival_intention_column, join_festival_intention_code_dict
    )
    workcation_experience_column = ["CQ1"]
    workcation_experience_code_dict = {
        1: True,
        2: False,
    }
    survey_df = map_column(
        survey_df, workcation_experience_column, workcation_experience_code_dict
    )

    workcation_choice_reason_col_description = {
        "CQ3_1": "서울특별시",
        "CQ3_2": "부산광역시",
        "CQ3_3": "인천광역시",
        "CQ3_4": "대구광역시",
        "CQ3_5": "대전광역시",
        "CQ3_6": "광주광역시",
        "CQ3_7": "울산광역시",
        "CQ3_8": "경기도",
        "CQ3_9": "충청북도",
        "CQ3_10": "충청남도",
        "CQ3_11": "전라북도",
        "CQ3_12": "전라남도",
        "CQ3_13": "경상북도",
        "CQ3_14": "경상남도",
        "CQ3_15": "강원도",
        "CQ3_16": "세종특별자치시",
        "CQ3_17": "제주특별자치도",
    }

    workcation_choice_reason_col = [
        "CQ3_1_1",
        "CQ3_1_2",
        "CQ3_1_3",
        "CQ3_1_4",
        "CQ3_1_5",
        "CQ3_1_6",
        "CQ3_1_7",
        "CQ3_1_8",
        "CQ3_1_9",
        "CQ3_1_9997",
        "CQ3_1_9997_etc",
        "CQ3_2_1",
        "CQ3_2_2",
        "CQ3_2_3",
        "CQ3_2_4",
        "CQ3_2_5",
        "CQ3_2_6",
        "CQ3_2_7",
        "CQ3_2_8",
        "CQ3_2_9",
        "CQ3_2_9997",
        "CQ3_2_9997_etc",
        "CQ3_3_1",
        "CQ3_3_2",
        "CQ3_3_3",
        "CQ3_3_4",
        "CQ3_3_5",
        "CQ3_3_6",
        "CQ3_3_7",
        "CQ3_3_8",
        "CQ3_3_9",
        "CQ3_3_9997",
        "CQ3_3_9997_etc",
        "CQ3_4_1",
        "CQ3_4_2",
        "CQ3_4_3",
        "CQ3_4_4",
        "CQ3_4_5",
        "CQ3_4_6",
        "CQ3_4_7",
        "CQ3_4_8",
        "CQ3_4_9",
        "CQ3_4_9997",
        "CQ3_4_9997_etc",
        "CQ3_5_1",
        "CQ3_5_2",
        "CQ3_5_3",
        "CQ3_5_4",
        "CQ3_5_5",
        "CQ3_5_6",
        "CQ3_5_7",
        "CQ3_5_8",
        "CQ3_5_9",
        "CQ3_5_9997",
        "CQ3_5_9997_etc",
        "CQ3_6_1",
        "CQ3_6_2",
        "CQ3_6_3",
        "CQ3_6_4",
        "CQ3_6_5",
        "CQ3_6_6",
        "CQ3_6_7",
        "CQ3_6_8",
        "CQ3_6_9",
        "CQ3_6_9997",
        "CQ3_6_9997_etc",
        "CQ3_7_1",
        "CQ3_7_2",
        "CQ3_7_3",
        "CQ3_7_4",
        "CQ3_7_5",
        "CQ3_7_6",
        "CQ3_7_7",
        "CQ3_7_8",
        "CQ3_7_9",
        "CQ3_7_9997",
        "CQ3_7_9997_etc",
        "CQ3_8_1",
        "CQ3_8_2",
        "CQ3_8_3",
        "CQ3_8_4",
        "CQ3_8_5",
        "CQ3_8_6",
        "CQ3_8_7",
        "CQ3_8_8",
        "CQ3_8_9",
        "CQ3_8_9997",
        "CQ3_8_9997_etc",
        "CQ3_9_1",
        "CQ3_9_2",
        "CQ3_9_3",
        "CQ3_9_4",
        "CQ3_9_5",
        "CQ3_9_6",
        "CQ3_9_7",
        "CQ3_9_8",
        "CQ3_9_9",
        "CQ3_9_9997",
        "CQ3_9_9997_etc",
        "CQ3_10_1",
        "CQ3_10_2",
        "CQ3_10_3",
        "CQ3_10_4",
        "CQ3_10_5",
        "CQ3_10_6",
        "CQ3_10_7",
        "CQ3_10_8",
        "CQ3_10_9",
        "CQ3_10_9997",
        "CQ3_10_9997_etc",
        "CQ3_11_1",
        "CQ3_11_2",
        "CQ3_11_3",
        "CQ3_11_4",
        "CQ3_11_5",
        "CQ3_11_6",
        "CQ3_11_7",
        "CQ3_11_8",
        "CQ3_11_9",
        "CQ3_11_9997",
        "CQ3_11_9997_etc",
        "CQ3_12_1",
        "CQ3_12_2",
        "CQ3_12_3",
        "CQ3_12_4",
        "CQ3_12_5",
        "CQ3_12_6",
        "CQ3_12_7",
        "CQ3_12_8",
        "CQ3_12_9",
        "CQ3_12_9997",
        "CQ3_12_9997_etc",
        "CQ3_13_1",
        "CQ3_13_2",
        "CQ3_13_3",
        "CQ3_13_4",
        "CQ3_13_5",
        "CQ3_13_6",
        "CQ3_13_7",
        "CQ3_13_8",
        "CQ3_13_9",
        "CQ3_13_9997",
        "CQ3_13_9997_etc",
        "CQ3_14_1",
        "CQ3_14_2",
        "CQ3_14_3",
        "CQ3_14_4",
        "CQ3_14_5",
        "CQ3_14_6",
        "CQ3_14_7",
        "CQ3_14_8",
        "CQ3_14_9",
        "CQ3_14_9997",
        "CQ3_14_9997_etc",
        "CQ3_15_1",
        "CQ3_15_2",
        "CQ3_15_3",
        "CQ3_15_4",
        "CQ3_15_5",
        "CQ3_15_6",
        "CQ3_15_7",
        "CQ3_15_8",
        "CQ3_15_9",
        "CQ3_15_9997",
        "CQ3_15_9997_etc",
        "CQ3_16_1",
        "CQ3_16_2",
        "CQ3_16_3",
        "CQ3_16_4",
        "CQ3_16_5",
        "CQ3_16_6",
        "CQ3_16_7",
        "CQ3_16_8",
        "CQ3_16_9",
        "CQ3_16_9997",
        "CQ3_16_9997_etc",
        "CQ3_17_1",
        "CQ3_17_2",
        "CQ3_17_3",
        "CQ3_17_4",
        "CQ3_17_5",
        "CQ3_17_6",
        "CQ3_17_7",
        "CQ3_17_8",
        "CQ3_17_9",
        "CQ3_17_9997",
        "CQ3_17_9997_etc",
    ]
    workcation_choice_code = {
        1: "회사에서 지정해 준 지역이라서",
        2: "주변에 관광할 곳이 많아서",
        3: "방문하기에 교통이 편리해서",
        4: "본가/친척/아는 사람이 그 지역에 거주하고 있어서",
        5: "나중에 해당 지역으로 이사/이전 계획이 있어서",
        6: "관광지가 별로 없어 쉬면서 업무에 집중할 수 있어서",
        7: "주변에 맛집이 많아서",
        8: "평소에 여행으로는 잘 가지 않는 지역이라서",
        9: "평소에 자주 가는/좋아하는 지역이라서",
        9997: "기타",
    }
    for col in workcation_choice_reason_col:
        survey_df[col] = survey_df[col].map(workcation_choice_code)

    new_col_list = list()
    for region_code, region_name in workcation_choice_reason_col_description.items():

        survey_df[region_code + "_merged"] = survey_df.apply(
            lambda row: [
                row[col]
                for col in survey_df.columns
                if col.startswith(region_code) and not pd.isna(row[col])
            ],
            axis=1,
        ).copy()
        new_col_list.append(region_code + "_merged")

    # do join string
    # for col in new_col_list:
    #     survey_df[col] = survey_df[col].apply(lambda x: " | ".join(x))

    # drop old columns
    survey_df.drop(columns=workcation_choice_reason_col, inplace=True)
    # parse do you wnat to next time
    next_time_workcation_col = ["CQ4"]
    next_time_workcation_col_code = {
        1: True,
        2: False,
    }
    survey_df = map_column(
        survey_df, next_time_workcation_col, next_time_workcation_col_code
    )
    workcation_important_factor_col = ["CQ5_1", "CQ5_2", "CQ5_3"]
    workcation_important_factor_col_code = {
        1: "숙박환경",
        2: "근무환경",
        3: "근처 자연경관(강, 바다, 산 등)",
        4: "여가·문화활동",
        5: "휴식",
        6: "근처 관광지/여행지",
        7: "카페·맛집 탐방",
        8: "교통 편의성(대중교통, 주차 등)",
        9: "스포츠·레저 활동(서핑, 루지 등)",
        9997: "기타",
    }
    survey_df = map_column(
        survey_df, workcation_important_factor_col, workcation_important_factor_col_code
    )
    workcation_intention_col = ["CQ6"]
    workcation_intention_col_code = {
        1: "전혀 그렇지 않다",
        2: "그렇지 않는 편이다",
        3: "보통이다",
        4: "그런 편이다",
        5: "매우 그렇다",
    }
    survey_df = map_column(
        survey_df, workcation_intention_col, workcation_intention_col_code
    )
    return survey_df


def get_column_description():

    description_dict = {
        "SQ1": "여러분의 성별은 무엇입니까?",
        "SQ2": "여러분의 연령은 어떻게 되십니까?",
        "SQ4": "귀하께서는 현재 어디에 거주하고 계신가요?",
        "AQ1": "귀하께서는 현재 거주하고 계시는 {SQ4}에 대해 전반적으로 얼마나 만족하시나요?",
        "AQ2": "귀하께서는 앞으로도 계속 {SQ4}에서 거주하실 생각이신가요?",
        "AQ3_1": "귀하께서 다른 지역으로 이전/이사를 하게 된다면 다음 중 어떠한 요소를 첫번째로 고려하시나요?",
        "AQ3_2": "귀하께서 다른 지역으로 이전/이사를 하게 된다면 다음 중 어떠한 요소를 두번째로 고려하시나요?",
        "AQ3_3": "귀하께서 다른 지역으로 이전/이사를 하게 된다면 다음 중 어떠한 요소를 세번째로 고려하시나요?",
        "AQ4": "귀하께서 다음 중 가장 살아보고 싶은 지역은 어디인가요?",
        "BQ1": "귀하께서는 ‘부산’하면 어떤 이미지가 떠오르시나요? 떠오르는 이미지를 자유롭게 적어 주시기 바랍니다.",
        "BQ2": "다음 중 귀하께서 ‘부산’하면 생각나는 단어를 모두 선택해 주세요. 최소 5개는 선택해 주세요. ', '를 기준으로 단어가 구분되어 있다.",
        "BQ3": "귀하께서는 최근 2년간 부산에 몇 회 정도 방문하셨나요?",
        "BQ4_1": "부산 숙박환경 만족도",
        "BQ4_2": "부산 관광명소 만족도",
        "BQ4_3": "부산 자연경관 만족도",
        "BQ4_4": "부산 여가·문화활동 만족도",
        "BQ4_5": "부산 카페·맛집 만족도",
        "BQ4_6": "부산 스포츠·레저활동 만족도",
        "BQ4_7": "부산 교통 편의성 만족도",
        "BQ4_8": "부산 쇼핑 만족도",
        "BQ4_9": "부산 지역주민의 친절",
        "BQ4_10": "부산 전반적 만족도",
        "BQ5": "귀하께서는 부산을 방문하신 후 어떻게 생각하십니까?",
        "BQ6": "귀하께서는 앞으로 부산을 몇 번 더 방문하실 생각이신가요?",
        "BQ7_1": "첫번째로 좋았던 부분은 무엇인가요?",
        "BQ7_2": "두번째로 좋았던 부분은 무엇인가요?",
        "BQ7_3": "세번째로 좋았던 부분은 무엇인가요?",
        "BQ8": "귀하께서 부산에서 방문해 보신 축제는 다음 중 어떤 종류였나요? 여러 축제를 방문해 본 경험이 있으시다면 가장 최근 방문한 축제를 한 가지만 선택해 주세요.",
        "BQ9": "귀하께서는 부산에서 방문해 보신 축제{BQ8}를 즐기실 때 어떤 사람과 함께 축제를 즐기셨나요?",
        "BQ10_1": "귀하께서는 방문해 보신 부산의 {BQ8}에 얼마나 만족하셨나요? 행사 프로그램",
        "BQ10_2": "귀하께서는 방문해 보신 부산의 {BQ8}에 얼마나 만족하셨나요? 주변 통제 및 안전/치안",
        "BQ10_3": "귀하께서는 방문해 보신 부산의 {BQ8}에 얼마나 만족하셨나요? 교통환경(접근성, 주차 등)",
        "BQ10_4": "귀하께서는 방문해 보신 부산의 {BQ8}에 얼마나 만족하셨나요? 편의/휴게시설",
        "BQ10_5": "귀하께서는 방문해 보신 부산의 {BQ8}에 얼마나 만족하셨나요? 주변 환경(청결, 위생 등)",
        "BQ10_6": "귀하께서는 방문해 보신 부산의 {BQ8}에 얼마나 만족하셨나요? 물가/상도의",
        "BQ10_7": "귀하께서는 방문해 보신 부산의 {BQ8}에 얼마나 만족하셨나요? 전반적 만족도",
        "BQ11": "귀하께서는 {BQ8} 방문 후 부산에 대한 이미지가 어떻게 변화했나요?",
        "BQ12": "귀하께서는 {BQ8}와 유사한 축제를 즐기러 다음에도 다시 부산을 방문하실 의향이 얼마나 있으신가요?",
        "CQ1": "귀하께서는 부산에서 워케이션 경험을 하신 적이 있으신가요?",
        "CQ3_1_merged": "귀하께서 서울특별시에서 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_2_merged": "귀하께서 부산광역시에서 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_3_merged": "귀하께서 인천광역시에서 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_4_merged": "귀하께서 대구광역시에서 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_5_merged": "귀하께서 대전광역시에서 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_6_merged": "귀하께서 광주광역시에서 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_7_merged": "귀하께서 울산광역시에서 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_8_merged": "귀하께서 경기도에서 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_9_merged": "귀하께서 충청북도에서 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_10_merged": "귀하께서 충청남도에서 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_11_merged": "귀하께서 전라북도에서 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_12_merged": "귀하께서 전라남도에서 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_13_merged": "귀하께서 경상북도에서 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_14_merged": "귀하께서 경상남도 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_15_merged": "귀하께서 강원도 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_16_merged": "귀하께서 세종특별자치시 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ3_17_merged": "귀하께서 제주특별자치도 워케이션을 경험하게 된 이유는 무엇입니까? (값이 list로 해당하는 것이 포함되어 있다.)",
        "CQ4": "귀하께서는 앞으로 워케이션을 경험하실 생각이 있으신가요?",
        "CQ5_1": "귀하께서는 워케이션을 경험하실 때 첫번째로 생각하는 요소는 무엇입니까?",
        "CQ5_2": "귀하께서는 워케이션을 경험하실 때 두번째로 생각하는 요소는 무엇입니까?",
        "CQ5_3": "귀하께서는 워케이션을 경험하실 때 세번째로 생각하는 요소는 무엇입니까?",
        "CQ6": "귀하께서는 워케이션을 부산에서 경험하실 의향이 얼마나 있으신가요?",
    }
    return description_dict
