import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load dataset
df = pd.read_csv("tax_data.csv")

# Features & labels
X = df[['Income', 'Investments', 'Medical_Expenses', 'Loan_Interest', 'Dependents']].values
y = df['Tax_Deduction'].values  # Now predicting deductions instead of tax

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "tax_deduction_model.pkl")

print("Enhanced model trained and saved!")


def predict_deduction(income, investments, medical_expenses, loan_interest, dependents):
    """Predicts tax deduction based on multiple financial factors."""
    model = joblib.load("tax_deduction_model.pkl")  # Load saved model
    return model.predict([[income, investments, medical_expenses, loan_interest, dependents]])[0]  # Predict deduction
