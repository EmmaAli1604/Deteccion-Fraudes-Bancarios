import pandas as pd

from predictor import FraudPredictor

predictor = FraudPredictor(
    "../data/models/fraud_detector.joblib"
)

"""transaction = pd.DataFrame([
    {
        "step":120,
        "type":"TRANSFER",
        "amount":500000,
        "oldbalanceOrg":800000,
        "newbalanceOrig":300000,
        "oldbalanceDest":10000,
        "newbalanceDest":510000
    }
])"""

transaction = pd.DataFrame([
    {
        "step": 400,
        "type": "TRANSFER",
        "amount": 2000000,
        "oldbalanceOrg": 2000000,
        "newbalanceOrig": 0,
        "oldbalanceDest": 0,
        "newbalanceDest": 0
    }
])

prediction, probability = predictor.predict(
    transaction
)

print(f"{prediction == 0 and 'No es Fraude' or 'Fraude'}")
print(f"Probabilidad de Fraude:{probability:.2f}")