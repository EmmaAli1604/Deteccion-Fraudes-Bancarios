import json
import joblib
import pandas as pd
import streamlit as st

# -----------------------------
# Configuración
# -----------------------------

st.set_page_config(
    page_title="Detección de Fraudes Bancarios",
    layout="wide"
)

# -----------------------------
# Cargar modelo
# -----------------------------

@st.cache_resource
def load_model():

    return joblib.load(
        "../data/models/fraud_detector.joblib"
    )

model = load_model()

# -----------------------------
# Cargar métricas
# -----------------------------

@st.cache_data
def load_metrics():

    with open(
        "../data/models/metrics.json",
        "r"
    ) as f:

        return json.load(f)

metrics = load_metrics()

# -----------------------------
# Título
# -----------------------------

st.title(
    "Sistema de Detección de Fraudes Bancarios"
)

st.markdown(
    """
    Dashboard para monitoreo y predicción
    de transacciones fraudulentas.
    """
)

# -----------------------------
# Métricas del modelo
# -----------------------------

st.header(
    "Desempeño del Modelo"
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Accuracy",
    f"{metrics['accuracy']:.4f}"
)

col2.metric(
    "Precision",
    f"{metrics['precision']:.4f}"
)

col3.metric(
    "Recall",
    f"{metrics['recall']:.4f}"
)

col4.metric(
    "F1 Score",
    f"{metrics['f1']:.4f}"
)

col5.metric(
    "AUC",
    f"{metrics['auc']:.4f}"
)

# -----------------------------
# Predicción
# -----------------------------

st.header(
    "Predicción en Tiempo Real"
)

step = st.number_input(
    "Step",
    value=100
)

tipo = st.selectbox(
    "Tipo de Transacción",
    [
        "CASH_IN",
        "CASH_OUT",
        "DEBIT",
        "PAYMENT",
        "TRANSFER"
    ]
)

amount = st.number_input(
    "Monto",
    value=1000.0
)

oldbalanceOrg = st.number_input(
    "Saldo inicial origen",
    value=5000.0
)

newbalanceOrig = st.number_input(
    "Saldo final origen",
    value=4000.0
)

oldbalanceDest = st.number_input(
    "Saldo inicial destino",
    value=1000.0
)

newbalanceDest = st.number_input(
    "Saldo final destino",
    value=2000.0
)

# -----------------------------
# Botón
# -----------------------------

if st.button(
    "Analizar Transacción"
):

    transaction = pd.DataFrame([
        {
            "step": step,
            "type": tipo,
            "amount": amount,
            "oldbalanceOrg": oldbalanceOrg,
            "newbalanceOrig": newbalanceOrig,
            "oldbalanceDest": oldbalanceDest,
            "newbalanceDest": newbalanceDest
        }
    ])

    prediction = model.predict(
        transaction
    )[0]

    probability = model.predict_proba(
        transaction
    )[0][1]

    st.subheader(
        "Resultado"
    )

    if prediction == 1:

        st.error(
            f"⚠️ Fraude detectado "
            f"({probability:.2%})"
        )

    else:

        st.success(
            f"✅ Transacción legítima "
            f"({1-probability:.2%})"
        )

    st.progress(
        float(probability)
    )