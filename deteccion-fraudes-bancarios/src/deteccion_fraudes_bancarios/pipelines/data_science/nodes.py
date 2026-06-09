import pandas as pd
from sklearn.preprocessing import RobustScaler
import xgboost as xgb
from sklearn.ensemble import IsolationForest
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.datasets import make_moons


def scale_data(X: pd.DataFrame):
    columnas_a_eliminar = ['nameOrig', 'nameDest', 'isFlaggedFraud'] 
    df = X.drop(columns=columnas_a_eliminar, errors='ignore')

    df = pd.get_dummies(df, columns=['type'], drop_first=True)

    df = df.astype(np.float32)

    scaler = RobustScaler() 
    X_scaled = scaler.fit_transform(df)
    return X_scaled

#  Modelo Supervisado (XGBoost)
def train_xgboost(X_train: pd.DataFrame, y_train: pd.Series, parameters: dict):
    """Entrena el modelo XGBoost para predecir la etiqueta de fraude."""
    model = xgb.XGBClassifier(**parameters)
    model.fit(X_train, y_train)
    return model

# Modelo de Clusterización 
def train_clustering_model(X_train: pd.DataFrame, parameters: dict):
    kmeans = MiniBatchKMeans(n_clusters=5, batch_size=10000, random_state=42)
    model = kmeans.fit_predict(X_train)
    
    return model

# Modelo de Detección de Anomalías
def train_anomaly_detector(X_train: pd.DataFrame, parameters: dict):
    """Entrena Isolation Forest para encontrar transacciones que rompen la norma."""
    model = IsolationForest(**parameters)
    model.fit(X_train) 
    return model