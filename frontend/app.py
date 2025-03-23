import streamlit as st
import requests
import pandas as pd

# Backend Base URL
BASE_URL = "https://ai-tax-assistant.onrender.com"

# Sidebar: Dynamic Input Fields
st.sidebar.header("📑 Enter Your Financial Details")

# Define session state for mode switching
if "mode" not in st.session_state:
    st.session_state.mode = "general_tax"

# Sidebar Inputs (Default: General Tax Inputs)
if st.session_state.mode == "general_tax":
    income = st.sidebar.number_input("Income", min_value=0, step=1000)
    investments = st.sidebar.number_input("Investments (PPF, ELSS, NPS, etc.)", min_value=0, step=1000)
    medical_expenses = st.sidebar.number_input("Medical Expenses", min_value=0, step=1000)
    loan_interest = st.sidebar.number_input("Loan Interest Paid", min_value=0, step=1000)
    dependents = st.sidebar.number_input("Number of Dependents", min_value=0, step=1)
elif st.session_state.mode == "capital_gains":
    num_trades = st.sidebar.number_input("Number of Trades", min_value=1, step=1, value=1)
    trades = []
    for i in range(num_trades):
        st.sidebar.markdown(f"**Trade {i+1}**")
        asset_type = st.sidebar.selectbox(f"Asset Type - Trade {i+1}", ["Stocks", "Crypto"], key=f"type_{i}")
        buy_price = st.sidebar.number_input(f"Buy Price (₹) - Trade {i+1}", min_value=0.0, step=0.1, key=f"buy_{i}")
        sell_price = st.sidebar.number_input(f"Sell Price (₹) - Trade {i+1}", min_value=0.0, step=0.1, key=f"sell_{i}")
        quantity = st.sidebar.number_input(f"Quantity - Trade {i+1}", min_value=1, step=1, key=f"qty_{i}")
        holding_period = st.sidebar.number_input(f"Holding Period (Days) - Trade {i+1}", min_value=1, step=1, key=f"hold_{i}")

        trades.append({
            "asset_type": asset_type,
            "buy_price": buy_price,
            "sell_price": sell_price,
            "quantity": quantity,
            "holding_period": holding_period
        })

# Title
st.title("💼 Smart Tax Assistant")
st.markdown("### Simplify Your Tax Calculation & Deductions")
st.markdown("---")

# Mode Switching Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("📊 Switch to Capital Gains Tax"):
        st.session_state.mode = "capital_gains"
        st.experimental_rerun()
with col2:
    if st.button("🧾 Switch to General Tax Calculator"):
        st.session_state.mode = "general_tax"
        st.rerun()
st.markdown("---")
# Capital Gains Tax Section
if st.session_state.mode == "capital_gains":
    st.markdown("## 📈 Crypto & Stock Capital Gains Tax Calculator")
    
    if st.button("📊 Calculate Capital Gains Tax"):
        response = requests.post(f"{BASE_URL}/calculate_capital_gains", json={"trades": trades})
        result = response.json()
        
        st.write(f"### 📊 **Capital Gains Summary**")
        st.write(f"**Short-Term Capital Gains (Stocks)**: ₹{result['short_term_gains_stocks']}")
        st.write(f"**Long-Term Capital Gains (Stocks)**: ₹{result['long_term_gains_stocks']}")
        st.write(f"**Crypto Gains**: ₹{result['crypto_gains']}")

        st.write("---")
        st.write(f"### 💰 **Tax Breakdown**")
        st.write(f"📌 **STCG Tax on Stocks (15%)**: ₹{result['stcg_stocks_tax']}")
        st.write(f"📌 **LTCG Tax on Stocks (10% after ₹1,00,000 exemption)**: ₹{result['ltcg_stocks_tax']}")
        st.write(f"📌 **Crypto Tax (30%)**: ₹{result['crypto_tax']}")

    st.markdown("---")

# General Tax Calculation Section
if st.session_state.mode == "general_tax":
    st.markdown("## 📊 Tax Calculation & Deductions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Calculate Tax"):
            response = requests.post(f"{BASE_URL}/calculate_tax", json={"income": income})
            st.success(f"### Estimated Tax: ₹{response.json()['estimated_tax']}")

    with col2:
        if st.button("📉 Predict Deduction"):
            response = requests.post(f"{BASE_URL}/predict_deduction", json={
                "income": income,
                "investments": investments,
                "medical_expenses": medical_expenses,
                "loan_interest": loan_interest,
                "dependents": dependents
            })
            st.success(f"### Predicted Deduction: ₹{response.json()['predicted_deduction']}")

    with col3:
        if st.button("⚠️ Check Audit Risk"):
            response = requests.post(f"{BASE_URL}/predict_audit_risk", json={
                "income": income,
                "deductions": investments + medical_expenses + loan_interest
            })
            st.warning(f"### Audit Risk Level: {response.json()['audit_risk']}")

    st.markdown("---")

# Tax Document Checklist
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

    st.write(f"💰 **Potential Tax Savings:** ₹{savings}")

    st.write("### 📌 Investment Recommendations:")
    for rec in recommendations:
        st.write(f"- {rec}")

st.markdown("---")

# Important Tax Tips Section
st.markdown("## 📌 Important Points to Keep in Mind While Filing Taxes")
st.markdown(
    """
    <div style="font-size:16px;">
    -  <b>Keep Track of Your Income & Deductions</b>: Ensure all income sources and eligible deductions are accounted for.<br>
    -  <b>Choose the Right Tax Regime</b>: Compare the old and new tax regimes to see which is beneficial.<br>
    -  <b>Save Tax Through Investments</b>: Consider tax-saving schemes like PPF, ELSS, and NPS.<br>
    -  <b>Medical & Insurance Benefits</b>: Claim deductions for medical expenses and insurance premiums.<br>
    -  <b>Loan Interest Deduction</b>: Home and education loan interest can help reduce taxable income.<br>
    -  <b>Dependent Tax Benefits</b>: Expenses on dependents, including parents and children, may be eligible for deductions.<br>
    -  <b>HRA & Rent Allowance</b>: If living in a rented house, claim HRA benefits.<br>
    -  <b>Be Honest in Your Tax Filing</b>: Over-claiming deductions can increase audit risk.<br>
    -  <b>Check Form 16 & Other Documents</b>: Verify all documents before filing.<br>
    -  <b>File Before the Deadline</b>: Avoid penalties by filing on time.<br>
    -  <b>Utilize 80C Deductions Wisely</b>: Invest in tax-saving instruments to reduce liability.<br>
    -  <b>Report All Income Sources</b>: Ensure part-time jobs, freelancing, or investments are included in your filing.<br>
    </div>
    """, unsafe_allow_html=True
)

st.markdown("---")


# AI Tax Chatbot
st.markdown("## 🤖 Ask the AI Tax Chatbot")
question = st.text_input("Enter your tax-related question:")
if st.button("💬 Get Advice"):
    response = requests.post(f"{BASE_URL}/chatbot", json={"question": question})
    st.info(f"### Chatbot Response: {response.json()['answer']}")

st.markdown("---")



