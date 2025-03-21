import streamlit as st
import requests
import pandas as pd

# Backend Base URL
BASE_URL = "https://ai-tax-assistant.onrender.com"

st.title("💰 AI-Powered Tax Assistant")
st.markdown("### Simplify Your Tax Calculation & Deductions ")

st.markdown("---")

# User Inputs
income = st.number_input("### Enter Your Income", min_value=0, step=1000)
investments = st.number_input("### Investments (PPF, ELSS, NPS, etc.)", min_value=0, step=1000)
medical_expenses = st.number_input("### Medical Expenses", min_value=0, step=1000)
loan_interest = st.number_input("### Loan Interest Paid", min_value=0, step=1000)
dependents = st.number_input("### Number of Dependents", min_value=0, step=1)

st.markdown("---")

# Employment Type Selection
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
        st.write("- " + item)

st.markdown("---")

# Tax Calculation Button
if st.button("📊 Calculate Tax"):
    response = requests.post(f"{BASE_URL}/calculate_tax", json={"income": income})
    st.write("### Estimated Tax:", response.json()["estimated_tax"])

st.markdown("---")

# Tax Deduction Prediction Button
if st.button("📉 Predict Deduction"):
    response = requests.post(f"{BASE_URL}/predict_deduction", json={
        "income": income,
        "investments": investments,
        "medical_expenses": medical_expenses,
        "loan_interest": loan_interest,
        "dependents": dependents
    })
    st.write("### Predicted Deduction:", response.json()["predicted_deduction"])

st.markdown("---")

# Audit Risk Assessment Button
if st.button("⚠️ Check Audit Risk"):
    response = requests.post(f"{BASE_URL}/predict_audit_risk", json={
        "income": income,
        "deductions": investments + medical_expenses + loan_interest
    })
    st.write("### Audit Risk Level:", response.json()["audit_risk"])

st.markdown("---")

# **New Feature: Tax Breakdown & Investment Recommendations with Bar Chart**
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

    st.write("### 📊 Tax Breakdown:")
    for key, value in breakdown.items():
        st.write(f"**{key}:** {value}")

    # Convert breakdown data to a DataFrame for visualization
    df = pd.DataFrame(list(breakdown.items()), columns=["Category", "Amount"])
    
    # Display bar chart
    st.bar_chart(df.set_index("Category"))

    st.write(f"💰 **Potential Tax Savings:** {savings}")

    st.write("### 📌 Investment Recommendations:")
    for rec in recommendations:
        st.write("- " + rec)

st.markdown("---")

# Tax Chatbot for Advice
st.markdown("## 🤖 Ask the AI Tax Chatbot")
question = st.text_input("Enter your tax-related question:")
if st.button("💬 Get Advice"):
    response = requests.post(f"{BASE_URL}/chatbot", json={"question": question})
    st.write("### Chatbot Response:", response.json()["answer"])

st.markdown("---")

