import streamlit as st
import requests
import pandas as pd

# Backend Base URL
BASE_URL = "https://ai-tax-assistant.onrender.com"

st.title("💰 AI-Powered Tax Assistant")
st.markdown("### Simplify Your Tax Calculation & Deductions")
st.markdown("---")

# Sidebar for Inputs
st.sidebar.header("🔢 Enter Your Financial Details")
income = st.sidebar.number_input("Income", min_value=0, step=1000)
investments = st.sidebar.number_input("Investments (PPF, ELSS, NPS, etc.)", min_value=0, step=1000)
medical_expenses = st.sidebar.number_input("Medical Expenses", min_value=0, step=1000)
loan_interest = st.sidebar.number_input("Loan Interest Paid", min_value=0, step=1000)
dependents = st.sidebar.number_input("Number of Dependents", min_value=0, step=1)

st.markdown("## 📝 Generate Tax Document Checklist")
employment_type = st.selectbox("Select Your Employment Type", ["Salaried", "Self-Employed", "Freelancer", "Business Owner"])
has_investments = st.checkbox("Do you have tax-saving investments?")
has_loans = st.checkbox("Do you have any loans?")
has_business_income = st.checkbox("Do you have business income?")

if st.button("📄 Generate Checklist"):
    response = requests.post(f"{BASE_URL}/generate_checklist", json={
        "employment_type": employment_type,
        "has_investments": has_investments,
        "has_loans": has_loans,
        "has_business_income": has_business_income
    })
    checklist = response.json()["checklist"]
    st.write("### Your Tax Document Checklist:")
    for item in checklist:
        st.write(f"- {item}")

st.markdown("---")

# Tax Calculation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 Calculate Tax"):
        response = requests.post(f"{BASE_URL}/calculate_tax", json={"income": income})
        st.success(f"### Estimated Tax: {response.json()['estimated_tax']}")

with col2:
    if st.button("📉 Predict Deduction"):
        response = requests.post(f"{BASE_URL}/predict_deduction", json={
            "income": income,
            "investments": investments,
            "medical_expenses": medical_expenses,
            "loan_interest": loan_interest,
            "dependents": dependents
        })
        st.success(f"### Predicted Deduction: {response.json()['predicted_deduction']}")

with col3:
    if st.button("⚠️ Check Audit Risk"):
        response = requests.post(f"{BASE_URL}/predict_audit_risk", json={
            "income": income,
            "deductions": investments + medical_expenses + loan_interest
        })
        st.warning(f"### Audit Risk Level: {response.json()['audit_risk']}")

st.markdown("---")

# Tax Breakdown & Investment Advisor
st.markdown("## 📊 Tax Breakdown & Investment Advisor")
if st.button("📜 Get Tax Breakdown & Advice"):
    response = requests.post(f"{BASE_URL}/tax_breakdown", json={
        "income": income,
        "investments": investments,
        "medical_expenses": medical_expenses,
        "loan_interest": loan_interest,
        "dependents": dependents
    })
    result = response.json()
    breakdown = result["breakdown"]
    savings = result["potential_savings"]
    recommendations = result["recommendations"]
    
    df = pd.DataFrame(list(breakdown.items()), columns=["Category", "Amount"])
    st.bar_chart(df.set_index("Category"))
    
    st.write(f"💰 **Potential Tax Savings:** {savings}")
    
    st.write("### 📌 Investment Recommendations:")
    for rec in recommendations:
        st.write(f"- {rec}")

st.markdown("---")

# AI Tax Chatbot
st.markdown("## 🤖 Ask the AI Tax Chatbot")
question = st.text_input("Enter your tax-related question:")
if st.button("💬 Get Advice"):
    response = requests.post(f"{BASE_URL}/chatbot", json={"question": question})
    st.info(f"### Chatbot Response: {response.json()['answer']}")

st.markdown("---")

