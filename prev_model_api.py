from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI(title="AI Fraud Detection API")

# Load the trained XGBoost model when the server starts
try:
    with open('fraud_xgboost_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("🧠 XGBoost Model Loaded Successfully!")
except FileNotFoundError:
    print("❌ Model file not found. Did you run train_model.py?")
    model = None

class TransactionData(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    time_since_last_txn: float

@app.post("/predict")
def predict_fraud(data: TransactionData):
    if model is None:
        return {"error": "Model not loaded"}

    # 1. Format the incoming data exactly how the model expects it
    input_data = pd.DataFrame([{
        'TransactionAmount': data.amount,
        'Time_Since_Last': data.time_since_last_txn
    }])

    # 2. Ask the XGBoost model for a prediction
    # model.predict returns an array like [1] for Fraud or [0] for Normal
    prediction = int(model.predict(input_data)[0])
    
    # 3. Ask for the probability (e.g., "I am 92% sure this is fraud")
    probability = float(model.predict_proba(input_data)[0][1])

    is_fraud = True if prediction == 1 else False

    if is_fraud:
        print(f"🚨 ML FRAUD ALERT! TXN: {data.transaction_id} | Confidence: {probability:.2%}")
    else:
        print(f"✅ ML Normal TXN: {data.transaction_id} | Confidence: {(1-probability):.2%}")

    return {
        "transaction_id": data.transaction_id,
        "prediction": "Fraud" if is_fraud else "Normal",
        "fraud_probability": probability
    }