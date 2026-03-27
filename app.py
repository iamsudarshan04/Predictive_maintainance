from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ---------------------------------------------------
# DEBUG: show Railway filesystem (VERY IMPORTANT)
# ---------------------------------------------------
print("Current working directory:", os.getcwd())
print("Root files:", os.listdir())

if os.path.exists("models"):
    print("Models folder files:", os.listdir("models"))
else:
    print("❌ Models folder not found")

# ---------------------------------------------------
# Load model artifacts safely
# ---------------------------------------------------
model = None
feature_columns = None

try:
    model = joblib.load("models/xgb_rul_model.pkl")
    feature_columns = joblib.load("models/feature_columns.pkl")
    print("✅ Model and feature columns loaded successfully")
except Exception as e:
    print("❌ Error loading model:", e)

# ---------------------------------------------------
# FastAPI app
# ---------------------------------------------------
app = FastAPI(title="Turbofan Engine RUL Prediction API")

# Serve frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve frontend homepage
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

# ---------------------------------------------------
# Input schema
# ---------------------------------------------------
class EngineInput(BaseModel):
    sensor_7: float
    sensor_12: float
    sensor_14: float
    sensor_20: float
    sensor_21: float
    op_setting_1: float
    op_setting_2: float
    op_setting_3: float

# ---------------------------------------------------
# Risk logic
# ---------------------------------------------------
def get_risk_level(rul: float) -> str:
    if rul > 100:
        return "Low Risk"
    elif rul > 40:
        return "Medium Risk"
    else:
        return "High Risk"

# ---------------------------------------------------
# Prediction endpoint
# ---------------------------------------------------
@app.post("/predict")
def predict_rul(data: EngineInput):

    if model is None:
        return {
            "error": "Model not loaded on server. Check deployment logs."
        }

    input_array = np.array([
        data.sensor_7,
        data.sensor_12,
        data.sensor_14,
        data.sensor_20,
        data.sensor_21,
        data.op_setting_1,
        data.op_setting_2,
        data.op_setting_3
    ]).reshape(1, -1)

    predicted_rul = float(model.predict(input_array)[0])
    risk = get_risk_level(predicted_rul)

    return {
        "predicted_rul": round(predicted_rul, 2),
        "risk_level": risk
    }
