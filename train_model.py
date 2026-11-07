
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Generate reproducible synthetic transaction data
rng = np.random.default_rng(42)
n = 3000

data = pd.DataFrame({
    "amount": rng.uniform(100, 500000, n),
    "hour": rng.integers(0, 24, n),
    "failed_logins": rng.integers(0, 10, n),
    "new_device": rng.integers(0, 2, n)
})

# Synthetic fraud labels based on predefined rules
data["fraud"] = (
    (data["amount"] > 200000) |
    (data["failed_logins"] >= 5) |
    ((data["new_device"] == 1) & (data["amount"] > 100000))
).astype(int)

features = ["amount", "hour", "failed_logins", "new_device"]

X = data[features]
y = data["fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("BankGuard AI Model Evaluation")
print(classification_report(y_test, predictions))

joblib.dump(model, "fraud_model.pkl")

print("Model saved successfully: fraud_model.pkl")
