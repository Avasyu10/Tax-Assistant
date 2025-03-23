from flask import Flask, request, jsonify
from ocr_extractor import extract_expenses
from tax_deduction import predict_deduction
from tax_calculator import calculate_tax
from audit_risk import predict_audit_risk
from chatbot import get_tax_advice
from checklist_generator import generate_checklist
from tax_breakdown import calculate_tax_breakdown
from investment_advisor import get_investment_recommendations
from capital_gains import calculate_capital_gains

app = Flask(__name__)

# API Endpoint: Upload receipt image for OCR
@app.route("/upload_receipt", methods=["POST"])
def upload_receipt():
    file = request.files["file"]
    file_path = f"uploads/{file.filename}"
    file.save(file_path)
    expenses = extract_expenses(file_path)
    return jsonify({"expenses": expenses})

# API Endpoint: Predict tax deductions
@app.route("/predict_deduction", methods=["POST"])
def deduction():
    data = request.json

    # Extract values, defaulting to 0 if not provided
    income = data.get("income", 0)
    investments = data.get("investments", 0)
    medical_expenses = data.get("medical_expenses", 0)
    loan_interest = data.get("loan_interest", 0)
    dependents = data.get("dependents", 0)

    # Predict deduction
    deduction = predict_deduction(income, investments, medical_expenses, loan_interest, dependents)

    return jsonify({"predicted_deduction": deduction})


# API Endpoint: Calculate estimated tax
@app.route("/calculate_tax", methods=["POST"])
def tax():
    data = request.json
    income = data["income"]
    estimated_tax = calculate_tax(income)
    return jsonify({"estimated_tax": estimated_tax})

# API Endpoint: Predict audit risk
@app.route("/predict_audit_risk", methods=["POST"])
def audit_risk():
    data = request.json
    income = data["income"]
    deductions = data["deductions"]
    risk = predict_audit_risk(income, deductions)
    return jsonify({"audit_risk": "High" if risk == 1 else "Low"})

# API Endpoint: NLP Chatbot for tax queries
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    question = data["question"]
    answer = get_tax_advice(question)
    return jsonify({"answer": answer})

# API Endpoint: Tax Document Checklist Generator
@app.route("/generate_checklist", methods=["POST"])
def generate():
    data = request.json
    emp_type = data.get("employment_type")
    has_investments = data.get("has_investments", False)
    has_loans = data.get("has_loans", False)
    has_business_income = data.get("has_business_income", False)

    checklist = generate_checklist(emp_type, has_investments, has_loans, has_business_income)
    return jsonify({"checklist": checklist})

# API Endpoint: Capital Gains Tax Calculation
@app.route("/calculate_capital_gains", methods=["POST"])
def capital_gains():
    data = request.json

    # Extract values, defaulting to 0 if not provided
    num_trades = data.get("num_trades", 0)
    asset_type = data.get("asset_type", "")
    buy_price = float(data.get("buy_price", 0))
    sell_price = float(data.get("sell_price", 0))
    quantity = int(data.get("quantity", 0))
    holding_period = int(data.get("holding_period", 0))

    # Calculate capital gains
    result = calculate_capital_gains(asset_type, buy_price, sell_price, quantity, holding_period)
    
    return jsonify(result)


# API Endpoint: Tax Breakdown & Investment Recommendations
@app.route("/tax_breakdown", methods=["POST"])
def tax_breakdown():
    data = request.json
    income = data["income"]
    investments = data["investments"]
    medical_expenses = data["medical_expenses"]
    loan_interest = data["loan_interest"]
    dependents = data["dependents"]

    # Get tax breakdown & savings
    breakdown, potential_savings = calculate_tax_breakdown(income, investments, medical_expenses, loan_interest, dependents)

    # Get investment recommendations
    recommendations = get_investment_recommendations(investments, medical_expenses, loan_interest, dependents)

    return jsonify({
        "breakdown": breakdown,
        "potential_savings": potential_savings,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
