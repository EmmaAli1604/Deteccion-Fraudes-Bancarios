import pandas as pd
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.preprocessing import RobustScaler
import xgboost as xgb
from sklearn.ensemble import IsolationForest
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.model_selection import train_test_split

def split_data(df: pd.DataFrame, target_column: str):
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test

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

def evaluate_clustering_model(X_test: pd.DataFrame, model):
    cluster_labels = model.predict(X_test)
    
    sample_size = min(10000, len(X_test))
    
    score_silueta = silhouette_score(X_test, cluster_labels, sample_size=sample_size, random_state=42)
    db_index = davies_bouldin_score(X_test, cluster_labels)
    inercia_test = model.inertia_ 
    
    print("=== EVALUACIÓN GEOMÉTRICA EN DATOS DE PRUEBA ===")
    print(f"Coeficiente de Silueta (Test): {score_silueta:.4f}")
    print(f"Índice Davies-Bouldin (Test): {db_index:.4f}")
    print(f"Inercia (Test): {inercia_test:.4f}")

    metrics = {
        'silhouette': score_silueta,
        'davies_bouldin': db_index,
        'inertia': inercia_test
    }
    
    return cluster_labels, metrics

def test_clustering_model(X_test: pd.DataFrame, model, umbral_anomalia):
    cluster_labels = model.predict(X_test)
    
    distancias = model.transform(X_test)
    distancias_al_centro = distancias.min(axis=1)
    
    es_anomalia = distancias_al_centro > umbral_anomalia
    
    resultados = pd.DataFrame({
        'cluster_asignado': cluster_labels,
        'distancia': distancias_al_centro,
        'es_anomalia': es_anomalia
    }, index=X_test.index)
    
    return resultados

# Modelo de Detección de Anomalías
def train_anomaly_detector(X_train: pd.DataFrame, parameters: dict):
    """Entrena Isolation Forest para encontrar transacciones que rompen la norma."""
    model = IsolationForest(**parameters)
    model.fit(X_train) 
    return model