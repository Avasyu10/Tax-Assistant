import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import joblib
import os

# Load dataset from CSV
csv_file = "audit_risk_data.csv"

if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    # Default dataset if CSV is missing
    data = np.array([
        [50000, 5000, 0],
        [70000, 30000, 1],
        [90000, 10000, 0],
        [120000, 60000, 1],
        [150000, 70000, 1],
        [200000, 80000, 1],
        [250000, 50000, 1],
        [300000, 100000, 1],
        [350000, 150000, 1],
        [400000, 200000, 1],
    ])
    df = pd.DataFrame(data, columns=["Income", "Deductions", "Audit_Risk"])

# Extract features and labels
X = df[["Income", "Deductions"]].values
y = df["Audit_Risk"].values

# Train the model
model = GradientBoostingClassifier()
model.fit(X, y)

# Save the model
joblib.dump(model, "audit_risk.pkl")

# Function to predict audit risk
def predict_audit_risk(income, deductions):
    model = joblib.load("audit_risk.pkl")
    risk = model.predict([[income, deductions]])[0]
    return "High Risk" if risk == 1 else "Low Risk"

# Example usage
if __name__ == "__main__":
    test_income = 180000
    test_deductions = 75000
    print(f"Audit Risk: {predict_audit_risk(test_income, test_deductions)}")
