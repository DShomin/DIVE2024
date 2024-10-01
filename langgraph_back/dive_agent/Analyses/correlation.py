import numpy as np
import pandas as pd
import scipy.stats as ss
from sklearn.preprocessing import LabelEncoder

from typing import Dict, Any, Union, List
from typing_extensions import TypedDict
from abc import ABC, abstractmethod


BASE_DESCRIPTION = (
    "This analysis is used to analyze the correlation between multiple variables."
)


class BaseCorrelationAnalysis(ABC):
    def __init__(
        self,
        input_data: Union[pd.DataFrame, np.ndarray] = pd.DataFrame(
            [[1, 2, 3], [4, 5, 6]]
        ),
    ):
        self.input_data = self._validate_and_convert_input(input_data)

    @staticmethod
    def _validate_and_convert_input(
        input_data: Union[pd.DataFrame, np.ndarray]
    ) -> pd.DataFrame:
        if not isinstance(input_data, (pd.DataFrame, np.ndarray)):
            raise ValueError(
                "The input data must be a pandas DataFrame or numpy array."
            )

        if input_data.shape[1] < 2:
            raise ValueError("The input data must have at least two columns.")

        return (
            pd.DataFrame(input_data)
            if isinstance(input_data, np.ndarray)
            else input_data
        )

    def get_base_description(self) -> str:
        return BASE_DESCRIPTION

    @abstractmethod
    def get_specific_description(self) -> str:
        pass

    @abstractmethod
    def get_input_requirements(self) -> str:
        pass

    @abstractmethod
    def check_input_schema(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def execute_analysis(self) -> Dict[str, Any]:
        pass


class NormalCorrelationAnalysis(BaseCorrelationAnalysis):
    def __init__(
        self,
        input_data: Union[pd.DataFrame, np.ndarray] = pd.DataFrame(
            [[1, 2, 3], [4, 5, 6]]
        ),
        argument: Dict[str, Any] = {},
    ):
        super().__init__(input_data)
        self.argument = argument

    def get_specific_description(self) -> str:
        return "This analysis is used to analyze the correlation between continuous variables. Pearson, Kendall, Spearman methods can be used."

    def get_input_requirements(self) -> str:
        return "This analysis requires multiple continuous variables as input. (e.g. age, height, weight, etc.)"

    def check_input_schema(self) -> Dict[str, Any]:
        if not self.input_data.dtypes.apply(
            lambda x: np.issubdtype(x, np.number)
        ).all():
            return {"error": "The input data must be numeric data."}
        return {}

    def get_argument_explanation(self) -> Dict[str, Any]:
        return {
            "method": {
                "requirement": False,
                "explanation": "Correlation method",
                "type": str,
                "available_value": [
                    {
                        "pearson": "Measure the linear relationship between two continuous variables."
                    },
                    {
                        "kendall": "Measure the ordinal association between two variables based on rank agreement."
                    },
                    {
                        "spearman": "Measure the monotonic relationship between two variables."
                    },
                ],
            }
        }

    def get_available_argument(self) -> List[str]:
        return list(self.get_argument_explanation().keys())

    def check_update_argument_schema(self) -> Dict[str, Any]:
        argument_explanation = self.get_argument_explanation()
        available_argument = self.get_available_argument()

        self.argument = {
            k: v for k, v in self.argument.items() if k in available_argument
        }

        required_arguments = [
            k for k, v in argument_explanation.items() if v["requirement"]
        ]

        if (
            set(self.argument.keys()) != set(required_arguments)
            and len(required_arguments) != 0
        ):
            return {"error": f"Required arguments are {', '.join(required_arguments)}."}

        for key, value in self.argument.items():
            if value not in [
                list(v.keys())[0] for v in argument_explanation[key]["available_value"]
            ]:
                return {
                    "error": f"Possible values for {key} are {', '.join([list(v.keys())[0] for v in argument_explanation[key]['available_value']])}."
                }

        return {}

    def execute_analysis(self) -> Dict[str, Any]:
        error = self.check_update_argument_schema()
        if error:
            return error
        result = {}
        corr = self.input_data.corr(**self.argument)
        for col in corr.columns:
            for row in corr.index:
                result[f"{col} and {row}"] = float(corr.loc[row, col])

        return {
            "result": result,
            "result_description": """
            This is the correlation matrix between the variables.
            The value is between -1 and 1. If the value is close to 1, it means that the two variables are positively correlated.
            If the value is close to -1, it means that the two variables are negatively correlated.
            If the value is close to 0, it means that the two variables are not correlated.
            """,
        }


class CramerCorrelationAnalysis(BaseCorrelationAnalysis):
    def __init__(
        self,
        input_data: Union[pd.DataFrame, np.ndarray] = pd.DataFrame(
            [[1, 2, 3], [4, 5, 6]]
        ),
        argument: Dict[str, Any] = {},
    ):
        super().__init__(input_data)

    def get_specific_description(self) -> str:
        return "This analysis uses Cramer's V method to analyze the correlation between categorical variables."

    def get_input_requirements(self) -> str:
        return "This analysis requires multiple categorical variables as input. (e.g. gender, race, etc.)"

    def check_input_schema(self) -> Dict[str, Any]:
        if self.input_data.dtypes.apply(lambda x: np.issubdtype(x, np.number)).any():
            return {"error": "The input data must be categorical data."}

        return {}

    def get_argument_explanation(self) -> Dict[str, Any]:
        return {}

    def cramer_v(self, col_1, col_2):
        confusion_matrix = pd.crosstab(col_1, col_2).values
        chi2 = ss.chi2_contingency(confusion_matrix)[0]
        n = confusion_matrix.sum()
        phi2 = chi2 / n
        r, k = confusion_matrix.shape
        phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
        phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
        rcorr = r - ((r - 1) ** 2) / (n - 1)
        kcorr = k - ((k - 1) ** 2) / (n - 1)
        return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

    def execute_analysis(self) -> Dict[str, Any]:

        result = {}
        column_names = self.input_data.columns.tolist()
        for col_1 in column_names:
            for col_2 in column_names:
                result[f"{col_1} and {col_2}"] = float(
                    self.cramer_v(self.input_data[col_1], self.input_data[col_2])
                )

        return {
            "result": result,
            "result_discription": """This is the correlation matrix between the categorical variables. 
            The value is between 0 and 1. if the value is close to 1, it means that the two variables are strongly correlated.
            if the value is close to 0, it means that the two variables are not correlated.
            """,
        }


class PointBiserialCorrelationAnalysis(BaseCorrelationAnalysis):
    def __init__(
        self,
        input_data: Union[pd.DataFrame, np.ndarray] = pd.DataFrame(
            [[1, 2, 3], [4, 5, 6]]
        ),
        argument: Dict[str, Any] = {},
    ):
        super().__init__(input_data)
        self.argument = argument
        self.binary_columns = []

    def get_specific_description(self) -> str:
        return "This analysis uses Point-Biserial correlation coefficient to analyze the correlation between binary and continuous variables."

    def get_input_requirements(self) -> str:
        return "This analysis requires at least one binary variable and one continuous variable as input."

    def check_input_schema(self) -> Dict[str, Any]:
        binary_column_exists = False
        for column in self.input_data.columns:
            if (
                self.input_data[column].nunique() == 2
                and self.input_data[column].dtype == pd.CategoricalDtype
            ):
                binary_column_exists = True
                le = LabelEncoder()
                le.fit(self.input_data[column])
                self.input_data[column] = le.transform(self.input_data[column])
                self.binary_columns.append(column)
            elif self.input_data[column].nunique() == 2:
                self.binary_columns.append(column)
                binary_column_exists = True
            elif self.input_data[column].nunique() < 3:
                binary_column_exists = False
                break

        if not binary_column_exists:
            return {"error": "At least one binary variable is required."}

        return {}

    def get_argument_explanation(self) -> Dict[str, Any]:
        return {}

    def execute_analysis(self) -> Dict[str, Any]:
        binary_columns = self.binary_columns
        continuous_columns = self.input_data.iloc[
            :,
            self.input_data.dtypes.apply(lambda x: np.issubdtype(x, np.number)).values,
        ].columns
        result = {}

        for binary_column in binary_columns:
            for continuous_column in continuous_columns:
                r, p = ss.pointbiserialr(
                    self.input_data[binary_column].values,
                    self.input_data[continuous_column].values,
                )
                result[f"{binary_column} and {continuous_column} r"] = float(r)
                result[f"{binary_column} and {continuous_column} p"] = float(p)

        return {
            "result": result,
            "result_discription": """
            p: Indicates whether the relationship between two variables is statistically significant.
            r: Indicates the strength and direction of the linear relationship between two variables.
            
            If the p-value is less than 0.05 and the r-value is large: There is a strong correlation between the variables, and the relationship is statistically significant.
            If the p-value is greater than 0.05 and the r-value is small: There is little or no correlation, and the relationship is not statistically significant.
            """,
        }


TOOL_LIST = [
    NormalCorrelationAnalysis,
    CramerCorrelationAnalysis,
    PointBiserialCorrelationAnalysis,
]


if __name__ == "__main__":
    data = pd.DataFrame(
        {
            # "gender": ["male", "female", "male", "female", "male"],
            "age": [20, 30, 40, 50, 60],
            "height": [170, 160, 175, 165, 180],
        }
    )
    print("--------------------------------")

    # 1. NormalCorrelationAnalysis
    analysis = NormalCorrelationAnalysis(data, {"method": "pearson"})
    result = analysis.check_input_schema()
    if "error" in result.keys():
        print(result["error"])
    else:
        result = analysis.execute_analysis()
        print(result)
    print("--------------------------------")
    # 2. CramerCorrelationAnalysis
    data = pd.DataFrame(
        {
            "gender": ["male", "female", "male", "female", "male", "trans"],
            # "age": [20, 30, 40, 50, 60],
            # "height": [170, 160, 175, 165, 180],
            "test": [True, False, True, False, False, False],
        }
    )
    analysis = CramerCorrelationAnalysis(data)
    result = analysis.check_input_schema()
    if "error" in result.keys():
        print(result["error"])
    else:
        result = analysis.execute_analysis()
        print(result)
    print("--------------------------------")
    # 3. PointBiserialCorrelationAnalysis
    data = pd.DataFrame(
        {
            "gender": ["male", "female", "male", "female", "male"],
            "age": [20, 30, 40, 50, 60],
            "height": [170, 160, 175, 165, 180],
        }
    )
    analysis = PointBiserialCorrelationAnalysis(data)
    result = analysis.check_input_schema()
    if "error" in result.keys():
        print(result["error"])
    else:
        result = analysis.execute_analysis()
        print(result)
