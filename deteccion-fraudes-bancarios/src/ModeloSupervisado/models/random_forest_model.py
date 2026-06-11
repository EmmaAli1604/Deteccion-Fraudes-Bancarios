import joblib

from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

from .base_model import BaseModel

class RandomForestFraudModel(BaseModel):

    def __init__(self, preprocessor):

        self.pipeline = Pipeline([
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                RandomForestClassifier(
                    random_state=42,
                    class_weight="balanced",
                    n_jobs=-1
                )
            )
        ])

    def train(self, X, y):

        self.pipeline.fit(X, y)

    def predict(self, X):

        return self.pipeline.predict(X)

    def predict_proba(self, X):

        return self.pipeline.predict_proba(X)

    def save(self, path):

        joblib.dump(self.pipeline, path)