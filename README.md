# 💼 Smart Tax Assistant

An AI-Powered Web Tool for Intelligent Financial and Tax Guidance

---

## 🔍 Objective

To build a smart, user-friendly web assistant that simplifies the Indian tax process through intelligent predictions, real-time insights, and automation. The system is designed for individuals, freelancers, and small business owners who want a better understanding of taxes and financial planning.

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python-based UI framework)  
- **Backend**: Flask (Python)  
- **Libraries**: `pandas`, `requests`, `json`, `datetime`, `matplotlib`, `gtts`, `speech_recognition`, `tempfile`, `os`  
- **AI/ML**: Rule-based and machine learning models for deduction prediction, audit risk, and investment suggestions  
- **External APIs**:  
  - [NewsData.io](https://newsdata.io) – For tax and business news updates  
  - Hugging Face Qwen LLM – Used for the chatbot module  

---

## 📁 Backend Modules & API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/upload_transactions` | Accepts CSV of bank/UPI transactions and analyzes monthly patterns |
| `/tax_news` | Fetches 6 recent tax-related news articles with hourly caching |
| `/predict_deduction` | Predicts eligible deductions based on income, expenses, and dependents |
| `/calculate_tax` | Calculates income tax based on Indian tax slabs |
| `/predict_audit_risk` | Determines likelihood of a tax audit using income and deduction ratio |
| `/chatbot` | Provides conversational tax advice via Hugging Face model |
| `/generate_checklist` | Generates a list of required documents for tax filing based on user profile |
| `/calculate_capital_gains` | Calculates tax liabilities on stocks and crypto based on trade data |
| `/calculate_hra` | Computes House Rent Allowance exemptions per income and rent |
| `/calculate_loan` | Calculates EMI and tax deductions on home/education loans |
| `/tax_breakdown` | Returns a category-wise tax breakdown and potential investment suggestions |

---

## 🧠 AI & Intelligent Modules

- **Deduction Estimator**: Uses logic and ML to predict deductions under 80C, 80D, 24B, etc.  
- **Audit Risk Analyzer**: Flags high deduction-to-income scenarios for audit awareness  
- **Investment Advisor**: Recommends optimal savings options like ELSS, PPF, and NPS based on income, existing savings, and tax goals  
- **Tax Chatbot**: Natural language chatbot that answers tax FAQs in real-time using Hugging Face’s Qwen model  

---

## 📌 Key Features

- **Income & Expense Analyzer**: Upload a UPI/bank CSV file and get categorized summaries of income, expenses, and savings  
- **Tax Estimator**: Automatically calculates your estimated tax based on Indian income tax rules  
- **Deduction Predictor**: Advises you on eligible deductions based on your income, investments, and family structure  
- **Audit Risk Predictor**: Highlights if you are at higher risk of being flagged for a tax audit  
- **Capital Gains Calculator**: Compute tax on short-term and long-term stock or crypto trades  
- **Loan & HRA Calculators**: Simulate EMI payments and HRA benefits based on your salary and rent details  
- **Document Checklist Generator**: Provides a checklist of required tax-filing documents based on user profile  
- **Real-time News Updates**: Displays Indian tax and finance news, refreshed every hour using caching  
- **Voice-Powered Chatbot**: Users can speak or type questions to get automated voice and text responses using TTS/STT  

---

## 🌍 Potential Impact

- **For Individuals**: Simplifies tax filing, boosts awareness of savings and deduction opportunities  
- **For Students & Freelancers**: Teaches basic tax knowledge and offers filing tools for part-time income  
- **For Small Business Owners**: Helps estimate capital gains, audit risk, and guides them in claimable deductions  
- **For Low-Income or Rural Users**: Features like voice-based interaction, UPI CSV uploads, and visual breakdowns help users with limited literacy or tech experience  
- **Financial Advisors**: Can use this system as a support tool for quick predictions and advisory services  

---

## 🚀 Future Enhancements

- **Regional Language Support**: Add voice and text translation for Hindi, Bengali, Tamil, etc., using speech APIs  
- **PDF Bank Statement Parsing**: Automatically extract data from scanned PDFs using OCR and CV techniques  
- **User Authentication and History**: Let users save past tax estimations and track financial growth over years  
- **Mobile-Friendly UI**: Optimize the Streamlit layout for smartphones and low-bandwidth devices  
- **SMS Alerts or WhatsApp Notifications**: Push reminders or tax-saving tips to registered users  
- **Voice-Only Mode**: Enable a fully speech-driven mode for accessibility in low-literacy populations  
- **Tax Filing Integration**: Link to India’s income tax filing portal or provide ITR-form previews  
- **Interactive Budget Planner**: Suggest optimal spending and investment plans based on monthly income  

---

## 📦 Deployment Details

- **Frontend**: Streamlit Cloud
- **Backend**: Flask app with multiple endpoints, hosted on Render or local server  
- **News Updates**: Cached every hour using NewsData.io API  
- **Voice Module**: Uses `gTTS` for speaking out responses and optional `streamlit-audio-recorder` for voice input  


