from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
    FunctionTransformer
)
from sklearn.pipeline import Pipeline
import numpy as np

class FraudPreprocessor:

    def __init__(self):

        self.numeric_features = [
            "step",
            "amount",
            "oldbalanceOrg",
            "newbalanceOrig",
            "oldbalanceDest",
            "newbalanceDest"
        ]

        self.categorical_features = [
            "type"
        ]

    def build(self):

        numeric_pipeline = Pipeline([
            (
                "log",
                FunctionTransformer(
                    np.log1p,
                    validate=False
                )
            ),
            (
                "scaler",
                StandardScaler()
            )
        ])

        return ColumnTransformer([
            (
                "num",
                numeric_pipeline,
                self.numeric_features
            ),
            (
                "cat",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                self.categorical_features
            )
        ])