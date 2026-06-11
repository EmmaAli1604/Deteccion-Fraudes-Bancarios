import json
import os
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    auc,
    classification_report
)

from data.data_loader import DataLoader
from data.preprocessor import FraudPreprocessor

from models.random_forest_model import (
    RandomForestFraudModel
)

from train import ModelTrainer


RANDOM_STATE = 42

os.makedirs("data/models", exist_ok=True)
os.makedirs("data/reports", exist_ok=True)

# =====================================================
# CARGA DE DATOS
# =====================================================

loader = DataLoader(
    "../../data/01_raw/TransactionsData.csv"
)

data = loader.load()

print("Carga de Datos completa.")
# =====================================================
# VARIABLES
# =====================================================

X = data.drop(
    columns=[
        "isFraud",
        "nameOrig",
        "nameDest",
        "isFlaggedFraud"
    ]
)

y = data["isFraud"]

# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=RANDOM_STATE
)

print("Division de Variables para entrenamiento Completa.")

# =====================================================
# PREPROCESAMIENTO
# =====================================================

preprocessor = FraudPreprocessor().build()

print("Preprocesamiento Completo")

# =====================================================
# MODELO
# =====================================================

model = RandomForestFraudModel(
    preprocessor
)

# =====================================================
# GRID SEARCH
# =====================================================

trainer = ModelTrainer(model)

search = trainer.tune(
    X_train,
    y_train
)

print("\n===== MEJORES HIPERPARÁMETROS =====")
print(search.best_params_)

print("Entrenamiento Completo")

# =====================================================
# PREDICCIONES
# =====================================================

best_model = search.best_estimator_

y_pred = best_model.predict(X_test)

y_prob = best_model.predict_proba(X_test)[:, 1]

print("Predicciones completadas.")

# =====================================================
# MÉTRICAS
# =====================================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

fpr, tpr, _ = roc_curve(
    y_test,
    y_prob
)

roc_auc = auc(
    fpr,
    tpr
)

# =====================================================
# MOSTRAR RESULTADOS
# =====================================================

print("\n===== MÉTRICAS =====")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"AUC      : {roc_auc:.4f}")

print("\n===== REPORTE DE CLASIFICACIÓN =====")

print(
    classification_report(
        y_test,
        y_pred
    )
)

# =====================================================
# GUARDAR MÉTRICAS
# =====================================================

metrics = {
    "accuracy": float(accuracy),
    "precision": float(precision),
    "recall": float(recall),
    "f1": float(f1),
    "auc": float(roc_auc),
    "best_params": search.best_params_
}

with open(
    "data/models/metrics.json",
    "w"
) as f:

    json.dump(
        metrics,
        f,
        indent=4
    )
print("Se han guardado las Métricas.")
# =====================================================
# MATRIZ DE CONFUSIÓN
# =====================================================

cm = confusion_matrix(
    y_test,
    y_pred
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm
)

disp.plot()

plt.savefig(
    "data/reports/confusion_matrix.png",
    bbox_inches="tight"
)

plt.close()

# =====================================================
# CURVA ROC
# =====================================================

plt.figure(figsize=(8, 6))

plt.plot(
    fpr,
    tpr,
    label=f"AUC = {roc_auc:.4f}"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()

plt.savefig(
    "data/reports/roc_curve.png",
    bbox_inches="tight"
)

plt.close()

# =====================================================
# GUARDAR MODELO
# =====================================================

joblib.dump(
    best_model,
    "data/models/fraud_detector.joblib"
)

print("\nModelo guardado correctamente.")
print("Métricas guardadas en data/models/metrics.json")
print("Gráficas guardadas en data/reports/")