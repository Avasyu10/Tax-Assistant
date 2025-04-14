# 💼 Smart Tax Assistant

An **AI-Powered Web Tool** for Financial and Tax Guidance

---

## 🔍 Objective

To develop a web-based tax assistant that helps users manage their personal finances by offering:

- ✅ Intelligent tax predictions  
- ✅ Audit risk assessments  
- ✅ Capital gains calculations  
- ✅ Investment suggestions  
- ✅ Real-time tax news updates  

Users can upload their financial data, interact with AI, and receive actionable insights for taxation.

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python-based UI)  
- **Backend**: Flask (Python)  
- **Libraries**: `pandas`, `requests`, `json`, `datetime`, `matplotlib.pyplot`, `speech_recognition`, `gtts`, `streamlit`, `os`  
- **AI/ML Models**: Used for deduction prediction, audit risk estimation, and investment advice  
- **APIs**:  
  - [NewsData.io](https://newsdata.io) for real-time news  
  - Custom REST APIs for tax functionalities  

---

## 📁 Backend Modules & API Endpoints

| Endpoint | Description |
|---------|-------------|
| `/upload_transactions` | Upload and parse CSV bank transactions |
| `/tax_news` | Fetch 6 recent tax news articles (cached hourly) |
| `/predict_deduction` | Estimate tax deductions based on income/investments |
| `/calculate_tax` | Calculate estimated tax liability |
| `/predict_audit_risk` | Predict risk of being audited |
| `/chatbot` | NLP-powered chatbot for tax Q&A |
| `/generate_checklist` | Generate a document checklist based on user profile |
| `/calculate_capital_gains` | Compute capital gains/losses and tax |
| `/calculate_hra` | Calculate HRA exemptions |
| `/calculate_loan` | Estimate loan EMI |
| `/tax_breakdown` | Returns tax breakdown and investment suggestions |

---

## 🧠 AI Functionalities

- **Deduction Prediction Model**: Trained on income and investment trends  
- **Audit Risk Estimation**: Flags suspicious deduction-to-income ratios  
- **Investment Advisor**: Recommends ELSS, PPF, NPS based on goals  
- **Chatbot**: Hugging Face-based LLM (Qwen) that answers tax questions  

---

## 🎯 Key Features

- 📁 Upload and analyze bank statements  
- 📊 Get real-time deduction predictions  
- 💰 Estimate taxes, capital gains, HRA and loan EMI  
- 📈 Personalized investment advice  
- ⚠️ Predict audit risk levels  
- 📄 Generate tax-filing checklists  
- 📰 Real-time tax news every hour  
- 🤖 Voice-enabled AI chatbot for tax FAQs  

---

## 📈 Potential Impact

- **Individuals**: Educates and empowers them to plan taxes smarter  
- **Freelancers/SMBs**: Eases tax filing and compliance  
- **Financial Advisors**: Acts as a smart backend for client help  

---

## 📎 Future Enhancements

- 🔗 UPI-based transaction tracking  
- 📑 PDF parsing of bank statements  
- 🧾 OCR for scanning physical receipts  
- 🔐 User authentication & history tracking  
- 🌐 Regional language chatbot support  
- 📊 More visual dashboards and graphs  

---

## 👨‍💻 Deployment

- **Backend**: Flask (hosted on Render or localhost)  
- **Frontend**: Streamlit (wide layout enabled)  
- **News API**: Cached every 1 hour using NewsData.io  
- **Speech**: Uses `gTTS` for response and `streamlit audio recorder` for input  

---

