from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import pandas as pd
import os
import joblib

router = APIRouter()

# Load trained model and scaler
BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "..", "random_forest_model.pkl")
scaler_path = os.path.join(BASE_DIR, "..", "scaler.pkl")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

class AdInput(BaseModel):
    ad_name: str
    frequency: float
    impressions: int
    full_plays: int
    thumbstop_rate: float
    roas: float
    amount_spent: float
    ctr: float
    impressions_to_full_play_rate: float
    spend: float

@router.post("/predict")
def predict_ad_performance(inputs: List[AdInput]):
    predictions = []

    for ad in inputs:
        row = {
            "frequency": ad.frequency,
            "impressions": ad.impressions,
            "full_plays": ad.full_plays,
            "thumbstop_rate": ad.thumbstop_rate,
            "roas": ad.roas,
            "amount_spent": ad.amount_spent,
            "impressions_to_full_play": ad.impressions_to_full_play_rate,
        }

        X = pd.DataFrame([row])
        X_scaled = scaler.transform(X)
        probs = model.predict_proba(X_scaled)[0]

        if len(probs) == 2:
            fatigue_prob = round(probs[1], 4)
            winner_prob = round(probs[0], 4)
        else:
            only_class = model.classes_[0]
            if only_class == 1:
                fatigue_prob = 1.0
                winner_prob = 0.0
            else:
                fatigue_prob = 0.0
                winner_prob = 1.0

        recommendation = "increase budget by 10%" if fatigue_prob < 0.3 else "reduce budget or refresh creative"

        predictions.append({
            "ad_name": ad.ad_name,
            "fatigue_probability": fatigue_prob,
            "winner_probability": winner_prob,
            "recommendation": recommendation
        })

    return {"predictions": predictions}
