# 💰 AI Personal Finance Advisor

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-FF4B4B?style=for-the-badge)](https://priyanshu-finance-advisor.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Gemini-AI-F9AB00?style=for-the-badge&logo=google&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)

**An AI-powered personal finance dashboard with expense tracking, ML-based anomaly detection, budget prediction, and a Gemini AI financial advisor — all in one app.**

🚀 **[Live Demo](https://priyanshu-finance-advisor.streamlit.app)**

---

## 🧠 About the Project

This project is a **full-stack personal finance web app** built with a focus on **Machine Learning** and **Generative AI** for intelligent financial insights.

> 💡 Built with Python, Machine Learning & Generative AI

The app combines multiple techniques — **Isolation Forest for anomaly detection**, **trend-based budget prediction**, and **Google Gemini 1.5 Flash** for real-time AI financial advice — to deliver a complete personal finance management experience.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 AI Financial Advisor | Natural language Q&A powered by Google Gemini 1.5 Flash |
| 🚨 Anomaly Detection | Isolation Forest ML algorithm to flag unusual transactions |
| 📊 Budget Predictor | Predicts next month's expenses from historical data |
| 💳 Expense Tracker | Add & visualize transactions with interactive Plotly charts |
| 🎨 Custom Dashboard | Metric cards, pie charts, bar graphs & line charts |
| 🔒 Secure API Handling | API keys via `.env` & Streamlit Secrets — never exposed |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Streamlit | Web UI framework |
| Google Gemini API | AI-powered financial advisor |
| Scikit-learn | Anomaly detection (Isolation Forest) |
| Plotly | Interactive data visualizations |
| Pandas | Data processing & analysis |
| NumPy | Numerical computations |
| python-dotenv | Environment variable management |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Google Gemini API key — [Get it here](https://makersuite.google.com/app/apikey)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Priyanshuu2008/personal-finance-advisor.git
cd personal-finance-advisor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file and add your API key
echo GEMINI_API_KEY=your_api_key_here > .env

# 4. Run the app
streamlit run app.py
```

App will open at `http://localhost:8501`

---

## 📁 Project Structure

```
personal-finance-advisor/
├── app.py                        # Main Streamlit application
├── requirements.txt              # Python dependencies
├── .env                          # API keys (not committed)
├── .gitignore
├── .streamlit/
│   └── config.toml               # Streamlit theme & config
├── assets/
│   └── dashboard.png             # App screenshot
└── data/
    ├── personal_transactions.csv # Transaction data
    └── Budget.csv                # Budget data
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

For Streamlit Cloud deployment, add this under **Settings → Secrets**:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

---

## 📌 Key Highlights

- 🔮 **Generative AI** — Real-time financial advice using Gemini 1.5 Flash
- 🧠 **Unsupervised ML** — Anomaly detection without any labeled data
- 📈 **Data Visualization** — Interactive charts with Plotly
- ☁️ **Cloud Deployed** — Live on Streamlit Cloud, accessible anywhere
- 🔐 **Secure** — API keys never committed to version control

---

## 🙋‍♂️ Author

**Priyanshu Tiwari**
- GitHub: [@Priyanshuu2008](https://github.com/Priyanshuu2008)
- LinkedIn: [priyanshuu20](https://www.linkedin.com/in/priyanshuu20/)
- Live App: [priyanshu-finance-advisor.streamlit.app](https://priyanshu-finance-advisor.streamlit.app)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
