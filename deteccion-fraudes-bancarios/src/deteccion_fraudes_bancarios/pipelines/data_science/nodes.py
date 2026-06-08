import pandas as pd
import xgboost as xgb
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans

#  Modelo Supervisado (XGBoost)
def train_xgboost(X_train: pd.DataFrame, y_train: pd.Series, parameters: dict):
    """Entrena el modelo XGBoost para predecir la etiqueta de fraude."""
    model = xgb.XGBClassifier(**parameters)
    model.fit(X_train, y_train)
    return model

# Modelo de Clusterización 
def train_clustering_model(X_train: pd.DataFrame, parameters: dict):
    """Entrena K-Means para agrupar comportamientos similares."""
    model = KMeans(**parameters)
    model.fit(X_train)
    return model

# Modelo de Detección de Anomalías
def train_anomaly_detector(X_train: pd.DataFrame, parameters: dict):
    """Entrena Isolation Forest para encontrar transacciones que rompen la norma."""
    model = IsolationForest(**parameters)
    model.fit(X_train) 
    return model