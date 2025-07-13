from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import numpy as np
from joblib import load

router = APIRouter()

# Load trained model and scaler
model = load("random_forest_model.pkl")
scaler = load("scaler.pkl")

# Define request schema
class AdMetrics(BaseModel):
    frequency: float
    impressions: int
    full_plays: int
    thumbstop_rate: float
    roas: float
    amount_spent: float

@router.post("/predict-ad-performance")
def predict_ad_performance(ad: AdMetrics):
    # Derived feature
    impressions_to_full_play = ad.full_plays / ad.impressions if ad.impressions > 0 else 0

    # Ensure correct input order
    X = np.array([
        ad.frequency,
        ad.impressions,
        ad.full_plays,
        ad.thumbstop_rate,
        ad.roas,
        ad.amount_spent,
        impressions_to_full_play
    ]).reshape(1, -1)

    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)[0]
    proba = model.predict_proba(X_scaled)[0]

    fatigue_prob = round(1 - proba[1], 3)
    winner_prob = round(proba[1], 3)

    recommendation = "🟢 Increase budget by 20%" if winner_prob > 0.7 else (
        "🟡 Keep budget stable" if 0.4 < winner_prob <= 0.7 else "🔴 Decrease budget by 30% or pause"
    )

    return {
        "prediction": "winner" if prediction == 1 else "not_winner",
        "winner_probability": winner_prob,
        "fatigue_probability": fatigue_prob,
        "budget_recommendation": recommendation
    }
