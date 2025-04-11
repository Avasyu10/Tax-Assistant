import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tempfile
import sounddevice as sd
import speech_recognition as sr
from gtts import gTTS

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

    # Initialize variables
    total_short_term_stocks = 0
    total_long_term_stocks = 0
    total_crypto_gains = 0

    for i in range(num_trades):
        st.sidebar.markdown(f"**Trade {i+1}**")
        asset_type = st.sidebar.selectbox(f"Asset Type - Trade {i+1}", ["Stocks", "Crypto"], key=f"type_{i}")
        buy_price = st.sidebar.number_input(f"Buy Price (₹) - Trade {i+1}", min_value=0.0, step=0.1, key=f"buy_{i}")
        sell_price = st.sidebar.number_input(f"Sell Price (₹) - Trade {i+1}", min_value=0.0, step=0.1, key=f"sell_{i}")
        quantity = st.sidebar.number_input(f"Quantity - Trade {i+1}", min_value=1, step=1, key=f"qty_{i}")
        holding_period = st.sidebar.number_input(f"Holding Period (Days) - Trade {i+1}", min_value=1, step=1, key=f"hold_{i}")
elif st.session_state.mode == "hra_calculator":
    basic_salary = st.sidebar.number_input("Basic Salary (₹)", min_value=0, step=1000)
    hra_received = st.sidebar.number_input("HRA Received (₹)", min_value=0, step=1000)
    rent_paid = st.sidebar.number_input("Rent Paid (₹)", min_value=0, step=1000)
    metro_city = st.sidebar.selectbox("City Type", ["Metro", "Non-Metro"])
    metro_city_bool = True if metro_city == "Metro" else False
elif st.session_state.mode == "loan_calculator":
    loan_amount = st.sidebar.number_input("Loan Amount (₹)", min_value=10000, step=10000)
    annual_rate = st.sidebar.number_input("Annual Interest Rate (%)", min_value=1.0, step=0.1)
    tenure_years = st.sidebar.number_input("Loan Tenure (Years)", min_value=1, step=1)

        
# Title
st.title("💼 Smart Tax Assistant")
st.markdown("### Simplify Your Tax Calculation & Deductions")
st.markdown("---")
st.markdown("## 📰 **Latest Tax News Updates**")

response = requests.get(f"{BASE_URL}/tax_news")

if response.status_code == 200:
    news_data = response.json().get("news", [])
    if news_data:
        for news in news_data:
            title = news["DESCRIPTION"].split(":")[0]
            body = news["DESCRIPTION"].split(":", 1)[-1]
            with st.expander(f" {title}"):
                st.markdown(f"**📝 Description:** {body}")
                st.markdown(f"📅 **Date (GMT):** {news['DATE(GMT)']}")
                st.markdown(f"🏢 **Publisher:** {news['PUBLISHER']}")
    else:
        st.info("🚫 No tax news found at the moment.")
else:
    st.error("⚠️ Failed to fetch tax news. Please try again later.")
st.markdown("---")


# Mode Switching Buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Switch to Capital Gains Tax"):
        st.session_state.mode = "capital_gains"
        st.rerun()

with col2:
    if st.button("🧾 Switch to General Tax"):
        st.session_state.mode = "general_tax"
        st.rerun()

with col3:
    if st.button("🏠 Switch to HRA Calculator"):
        st.session_state.mode = "hra_calculator"
        st.rerun()

with col4:
    if st.button("🏡 Switch to Loan EMI Calculator"):
        st.session_state.mode = "loan_calculator"
        st.rerun()

# HRA Calculation Section

# Loan EMI Calculation
if st.session_state.mode == "loan_calculator":
    st.markdown("---")
    st.markdown("## 🏡 Loan EMI Calculator")
    
     # ℹ️ About EMI & Tax Benefits
    with st.expander("ℹ️ Understanding EMI, Tax Benefits & Loan Rules in India"):
        st.write("""
        - **EMI (Equated Monthly Installment)** is a fixed monthly payment towards your loan.
        - EMI consists of **Principal + Interest**, with higher interest payments in the early months.
        - **Tax Benefits in India**:
          - 🏠 **Home Loan**:
            - Up to ₹2,00,000 deduction on interest under **Section 24(b)** (Self-occupied property).
            - Principal repayment eligible under **Section 80C** (Max ₹1,50,000).
          - 🎓 **Education Loan**:
            - **Unlimited deduction** on interest under **Section 80E** (Valid for 8 years).
          - 🚗 **Car Loan**: No tax benefits for personal cars, but deduction available for business use.
        - **EMI Calculation Formula**:  
          - EMI = **[P × r × (1+r)^n] / [(1+r)^n - 1]**  
          - Where **P** = Loan Amount, **r** = Monthly Interest Rate, **n** = Loan Tenure (Months)
        """)

    if st.button("📉 Calculate EMI"):
        response = requests.post(f"{BASE_URL}/calculate_loan", json={
            "loan_amount": loan_amount,
            "annual_rate": annual_rate,
            "tenure_years": tenure_years
        })
        result = response.json()

        if "error" in result:
            st.error(result["error"])
        else:
            st.success(f"### EMI Details")
            st.write(f"**Monthly EMI**: ₹{result['emi']}")
            st.write(f"**Total Interest Paid**: ₹{result['total_interest']}")
            st.write(f"**Total Payment (Principal + Interest)**: ₹{result['total_payment']}")
            st.write(f"**Eligible Tax Deduction on Interest**: ₹{result['tax_deduction']}")

            # Plot Graph - Principal & Interest Over Time
            st.markdown("### Loan Amortization Schedule")
            df = pd.DataFrame(result["amortization"])

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df["Month"], df["Principal"], label="Principal Paid", color="blue")
            ax.plot(df["Month"], df["Interest"], label="Interest Paid", color="red")
            ax.fill_between(df["Month"], df["Principal"], df["Interest"], color="gray", alpha=0.2)
            ax.set_xlabel("Months")
            ax.set_ylabel("Amount (₹)")
            ax.set_title("Principal & Interest Breakdown Over Time")
            ax.legend()
            st.pyplot(fig)

st.markdown("---")

if st.session_state.mode == "hra_calculator":
    
    st.markdown("## 🏠 HRA Exemption Calculator")
    st.write("House Rent Allowance (HRA) is an important tax benefit for salaried employees who live in rented accommodation. The exempted portion of HRA is calculated based on the following three conditions, and the least of these is exempted from tax:")
    st.write("1. **50% of Basic Salary for Metro Cities (40% for Non-Metro Cities)**")
    st.write("2. **Actual HRA Received from Employer**")
    st.write("3. **Rent Paid minus 10% of Basic Salary**")
    
    if st.button("🏠 Calculate HRA Exemption"):
        st.markdown("---")
        response = requests.post(f"{BASE_URL}/calculate_hra", json={
            "basic_salary": basic_salary,
            "hra_received": hra_received,
            "rent_paid": rent_paid,
            "metro_city": metro_city_bool
        })
        result = response.json()
        st.write(f"### **HRA Exemption Details**")
        st.write(f"**Exempted HRA**: ₹{result['hra_exempted']}")
        st.write(f"**Taxable HRA**: ₹{result['hra_taxable']}")
        
        st.write("#### Explanation:")
        st.write(f"- **50% of Basic Salary (Metro) / 40% (Non-Metro)**: ₹{result['metro_or_non_metro_limit']}")
        st.write(f"- **Actual HRA Received**: ₹{hra_received}")
        st.write(f"- **Rent Paid - 10% of Basic Salary**: ₹{result['rent_minus_10_percent']}")
        st.write("The lowest of these values is taken as the exempted HRA, and the remaining portion is taxable.")
    st.markdown("---")

# Capital Gains Tax Section
if st.session_state.mode == "capital_gains":
    st.markdown("## 📈 Crypto & Stock Capital Gains Tax Calculator")
    
    if st.button("📊 Calculate Capital Gains Tax"):
        response = requests.post(f"{BASE_URL}/calculate_capital_gains", json={
                "num_trades": num_trades,
                "asset_type": asset_type,
                "buy_price": buy_price,
                "sell_price": sell_price,
                "quantity": quantity,
                "holding_period": holding_period
        })
        result = response.json()
        
        st.write(f"###  **Capital Gains Summary**")
        st.write(f"**Short-Term Capital Gains (Stocks)**: ₹{result['short_term_gains_stocks']}")
        st.write(f"**Long-Term Capital Gains (Stocks)**: ₹{result['long_term_gains_stocks']}")
        st.write(f"**Crypto Gains**: ₹{result['crypto_gains']}")

        st.write("---")
        st.write(f"###  **Tax Breakdown**")
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
# Expense Split Section

st.markdown("## ⚖️ Income & Expense Balance")

# Button to enable expense entry
if "enter_expenses" not in st.session_state:
    st.session_state.enter_expenses = False

if st.button("➕ Enter Expenses"):
    st.session_state.enter_expenses = True

# Expense entry fields (visible after button click)
if st.session_state.enter_expenses:
    st.markdown("### 📌 Enter Your Expenses")
    st.markdown("Enter salary and your expenses below.")

    
    salary = st.number_input("Salary", min_value=0, step=10000)
    rent = st.number_input("🏠 Rent", min_value=0, step=1000)
    groceries = st.number_input("🛒 Groceries", min_value=0, step=500)
    utilities = st.number_input("💡 Utilities", min_value=0, step=500)
    transportation = st.number_input("🚗 Transportation", min_value=0, step=500)
    entertainment = st.number_input("🎭 Entertainment", min_value=0, step=500)
    other_expenses = st.number_input("📑 Other Expenses", min_value=0, step=500)

    total_expenses = rent + groceries + utilities + transportation + entertainment + other_expenses
    remaining_income = salary - total_expenses

    # Button to finalize and show results
    if st.button("📊 Split & Analyze"):
        st.success(f"### Total Expenses: ₹{total_expenses}")
        st.info(f"### Remaining Income: ₹{remaining_income}")

        if remaining_income < 0:
            st.error("⚠️ Warning: Expenses exceed income! Consider adjusting your budget.")

        # Pie Chart Visualization
        st.markdown("## 📊 Expense Breakdown")
        labels = ["Rent", "Groceries", "Utilities", "Transportation", "Entertainment", "Other"]
        values = [rent, groceries, utilities, transportation, entertainment, other_expenses]
        colors = ["red", "green", "blue", "orange", "purple", "gray"]
        
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')  # Ensures pie is a circle
        
        
        st.pyplot(fig)
        
        # Recommendations Based on Spending
        st.markdown("## Smart Financial Recommendations")
        recs = []
        if rent > (0.3 * salary):
            recs.append("📌 Consider reducing rent or finding a more affordable option (should ideally be <30% of income).")
        if groceries > (0.2 * salary):
            recs.append("📌 Look for discounts, meal planning, or alternative grocery options to cut costs.")
        if utilities > (0.1 * salary):
            recs.append("📌 Try to save on electricity and water bills by using energy-efficient appliances.")
        if transportation > (0.15 * salary):
            recs.append("📌 Consider carpooling or using public transport to cut transportation costs.")
        if entertainment > (0.1 * salary):
            recs.append("📌 Consider budgeting entertainment expenses to free up more savings.")
        if other_expenses > (0.1 * salary):
            recs.append("📌 Review miscellaneous expenses to find potential savings opportunities.")
        if remaining_income > 0:
            recs.append("📌 Consider investing a portion of your remaining income for better financial growth.")
        elif remaining_income < 0:
            recs.append("📌 Your expenses exceed income! Re-evaluate your spending habits.")

        for r in recs:
            st.write(r)
st.markdown("---")



st.markdown("## 🔗 UPI-Based Financial Summary")
st.markdown("Upload your UPI transaction statement (CSV format) to categorize your income and expenses.")

uploaded_statement = st.file_uploader("📂 Upload UPI Transaction CSV", type=["csv"])

if uploaded_statement:
    st.success("✅ File Uploaded Successfully!")

    # Read CSV as DataFrame
    df = pd.read_csv(uploaded_statement)

    # Convert DataFrame to JSON format for API
    transactions_json = df.to_dict(orient="records")

    # Send data to backend API for processing
    response = requests.post(f"{BASE_URL}/upload_transactions", json={"transactions": transactions_json})

    if response.status_code == 200:
        result = response.json()
        summary_table = pd.DataFrame(result["summary"])

        st.write("### 📊 Monthly Breakdown")
        st.dataframe(summary_table.style.format({col: "₹{:.2f}" for col in summary_table.select_dtypes(include=[np.number]).columns}))

    else:
        st.error("❌ Failed to analyze transactions. Please check the file format and try again.")

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
# Tax Resources & Guides Section
st.markdown("## 🌐 Important Tax Resources & Guides")
st.markdown("Here are some essential links to help you understand and file your taxes effectively:")
st.markdown("\n")


space1, col1, space2, col2, space3 = st.columns([0.1, 1, 0.1, 1, 0.1])

with col1:
    st.markdown("### 📌 Government Tax Portals")
    st.markdown("- **Income Tax Department:** [Visit Here](https://www.incometaxindia.gov.in/)")
    st.markdown("- **GST Portal:** [Visit Here](https://www.gst.gov.in/)")
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")
    
    
    st.markdown("### 📌 Latest Financial News & Updates")
    st.markdown("- **Union Budget Highlights:** [Read Here](https://www.indiabudget.gov.in/)")
    st.markdown("- **Latest Tax Amendments:** [Check Here](https://cleartax.in/s/income-tax)")
    st.markdown("- **Economic Survey Reports:** [Explore Here](https://www.indiabudget.gov.in/economicsurvey/)")
    


with col2:
    st.markdown("### 📌 Filing & Help Guides")
    st.markdown("- **How to File Income Tax Returns:** [Read Here](https://cleartax.in/s/how-to-efile-itr)")
    st.markdown("- **Documents Required for Filing Taxes:** [View Here](https://cleartax.in/s/documents-required-for-income-tax-return-filing)")
    st.markdown("\n")
    
    
    st.markdown("### 📌 Investment & Tax Saving")
    st.markdown("- **80C Deductions Explained:** [Learn More](https://cleartax.in/s/80c-80-deductions)")
    st.markdown("- **Best Tax-Saving Investments:** [Check Here](https://tax2win.in/guide/tax-saving-investments)")
    st.markdown("- **Capital Gains Tax on Stocks:** [Read Here](https://cleartax.in/s/capital-gains-income)")

st.markdown("---")


st.markdown("## 🤖 Voice-Enabled AI Tax Chatbot")


if "question_from_voice" not in st.session_state:
    st.session_state.question_from_voice = ""


def record_audio(duration=5, samplerate=44100):
    st.info("🎙️ Listening... Speak now!")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    return np.array(audio_data, dtype='int16').flatten()


if st.button("Speak your question 🎙️"):
    recognizer = sr.Recognizer()
    audio_array = record_audio()
    audio = sr.AudioData(audio_array.tobytes(), 44100, 2)

    try:
        spoken_question = recognizer.recognize_google(audio)
        st.session_state.question_from_voice = spoken_question
        st.success(f"You said: {spoken_question}")
    except sr.UnknownValueError:
        st.warning("Sorry, could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")


question = st.text_input("Ask your tax question:", value=st.session_state.question_from_voice)


if st.button("💬 Get Advice") and question.strip():
    response = requests.post(f"{BASE_URL}/chatbot", json={"question": question})
    answer = response.json()["answer"]
    st.success(f"Chatbot: {answer}")

 
    tts = gTTS(answer)
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    st.audio(temp_audio.name, format="audio/mp3")

st.markdown("---")








