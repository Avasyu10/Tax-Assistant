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
from hra_calculator import calculate_hra
from loan_utils import calculate_emi
from transaction_analyzer import analyze_transactions
import pandas as pd
import requests
import os
import json
from datetime import datetime, timedelta



app = Flask(__name__)

# API Endpoint: Upload Bank Transaction CSV
@app.route("/upload_transactions", methods=["POST"])
def upload_transactions():
    transactions = request.json["transactions"]
    df = pd.DataFrame(transactions)

    summary_table = analyze_transactions(df)

    result_json = summary_table.reset_index().to_dict(orient="records")

    return jsonify({"summary": result_json})

# Real time news
CACHE_FILE = "tax_news_cache.json"

@app.route("/tax_news", methods=["GET"])
def fetch_tax_news():
    try:
        # Check if cache exists
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                cache_data = json.load(f)
                last_fetched = datetime.strptime(cache_data["timestamp"], "%Y-%m-%d %H:%M:%S")
                if datetime.utcnow() - last_fetched < timedelta(days=2):
                    return jsonify({"news": cache_data["news"]})

        # Fetch from API if 2 days passed or cache doesn't exist
        response = requests.get("https://newsdata.io/api/1/news?apikey=pub_78245db189fba9e583135531ddbcf8185efce&q=tax&country=in&language=en&category=business,domestic,education,health,lifestyle")
        data = response.json()

        if "results" not in data or not data["results"]:
            print("API Response had no results:", data)
            return jsonify({"news": [], "message": "No tax news found."})

        news_list = []
        for item in data["results"][:5]:
            raw_date = item.get("pubDate", "")
            try:
                dt = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
                formatted_date = dt.strftime("%d %b %Y\n%I:%M:%S %p")
            except:
                formatted_date = raw_date

            news_list.append({
                "DESCRIPTION": f"{item.get('title', 'No Title')}: {item.get('description', 'No Description')}", "DATE(GMT)": formatted_date, "PUBLISHER": item.get("source_id", "Unknown Source")
            })

        # Cache the response
        with open(CACHE_FILE, "w") as f:
            json.dump({
                "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "news": news_list
            }, f)

        return jsonify({"news": news_list})

    except Exception as e:
        print("Error while fetching news:", str(e))
        return jsonify({"error": "Failed to fetch news. Please try again later."}), 500


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

@app.route("/calculate_hra", methods=["POST"])
def hra_calculator():
    data = request.json

    salary = float(data["basic_salary"])
    hra_received = float(data["hra_received"])
    rent_paid = float(data["rent_paid"])
    metro_city = (data["metro_city"])  # True for Metro, False for Non-Metro

    hra_result = calculate_hra(salary, hra_received, rent_paid, metro_city)

    return jsonify(hra_result)


@app.route("/calculate_loan", methods=["POST"])
def loan_calculator():
    data = request.json
    loan_amount = float(data["loan_amount"])
    annual_rate = float(data["annual_rate"])
    tenure_years = int(data["tenure_years"])

    result = calculate_emi(loan_amount, annual_rate, tenure_years)
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
