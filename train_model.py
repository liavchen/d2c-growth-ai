import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from joblib import dump

# Load data
df = pd.read_csv("ads_data.csv")

# Standardize column names
df.columns = df.columns.str.strip()

# Rename for convenience
df = df.rename(columns={
    "custom_derived_metrics:10229368397185749": "full_plays",
    "custom_derived_metrics:122130457322636890": "roas",
    "custom_derived_metrics:122130482612636890": "thumbstop_rate",
    "Amount spent (USD)": "amount_spent",
    "Impressions": "impressions",
    "Frequency": "frequency"
})

# --- Labeling Logic ---
df["impressions_to_full_play"] = df["full_plays"] / df["impressions"]

# Label fatigue ads (low ROAS, high frequency, low thumbstop)
df["label_fatigue"] = (
    (df["roas"] < 1.0) &
    (df["frequency"] > 1.5) &
    (df["thumbstop_rate"] < 0.8)
).astype(int)

# Label winning ads
df["label_winner"] = (
    (df["impressions_to_full_play"] > 0.85) &
    (df["thumbstop_rate"] > 0.8) &
    (df["roas"] > 1.5) &
    (df["amount_spent"] > 100)
).astype(int)

print("Label distribution:\n", df["label_fatigue"].value_counts())


# --- Choose Your Target ---
target = "label_winner"  # or "label_fatigue" based on what you want to predict

# --- Training ---
features = [
    "frequency", "impressions", "full_plays", "thumbstop_rate",
    "roas", "amount_spent", "impressions_to_full_play"
]

X = df[features]
y = df[target]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and scaler
dump(model, "random_forest_model.pkl")
dump(scaler, "scaler.pkl")

print("✅ Model and scaler saved successfully.")
