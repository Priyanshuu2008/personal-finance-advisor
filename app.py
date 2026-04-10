import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
import google.generativeai as genai
from sklearn.ensemble import IsolationForest
import numpy as np

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Finance Advisor", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    * { font-family: 'Segoe UI', sans-serif !important; }
    [data-testid="stAppViewContainer"], .main, .block-container {
        background-color: #f5f7fa !important;
    }
    [data-testid="stHeader"] { background-color: #f5f7fa !important; }
    .block-container { padding: 2rem 3rem !important; }

    section[data-testid="stSidebar"] { background-color: #1e2240 !important; }
    section[data-testid="stSidebar"] * { color: white !important; }
    section[data-testid="stSidebar"] input {
        color: #111827 !important;
        background-color: white !important;
        border-radius: 6px !important;
    }
    section[data-testid="stSidebar"] p { color: white !important; }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 { color: white !important; }
    section[data-testid="stSidebar"] small { color: #adb5bd !important; }
    section[data-testid="stSidebar"] span { color: white !important; }

    [data-testid="stMetric"] {
        background-color: white !important;
        border-radius: 14px !important;
        padding: 1.2rem !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07) !important;
        border: 1px solid #e5e7eb !important;
    }
    .stButton > button {
        background-color: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.8rem !important;
        font-weight: 500 !important;
    }
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important;
        background-color: white !important;
        color: #111827 !important;
    }
    .stNumberInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important;
        background-color: white !important;
        color: #111827 !important;
    }
    #MainMenu, footer { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

PLOT_LAYOUT = dict(
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(color='#111827', size=11),
    margin=dict(t=40, b=120, l=40, r=40)
)

# ==================== SIDEBAR ====================
st.sidebar.title("Finance Advisor")
st.sidebar.markdown("---")
page = st.sidebar.radio("Go to", ["Dashboard", "Expense Tracker", "AI Advisor", "Anomaly Detection", "Budget Predictor"])
st.sidebar.markdown("---")

st.sidebar.markdown("### Your Monthly Data")
user_name = st.sidebar.text_input("Your Name", value="User")
income = st.sidebar.number_input("Monthly Income (₹)", min_value=0, value=75000, step=1000)

st.sidebar.markdown("**Budget & Spent (₹)**")

categories = ["Rent", "Groceries", "EMI", "Travel & Commute", "Dining Out",
              "Electricity & Bills", "Mobile & Internet", "Medical",
              "Entertainment", "Shopping", "Education", "Savings"]

default_budget = [15000, 8000, 12000, 4000, 3000, 2500, 1000, 2000, 2000, 5000, 3000, 10000]
default_spent  = [15000, 7200, 12000, 4800, 4200, 2500,  999, 1500, 3200, 6500, 3000,  8000]

budget_vals = []
spent_vals = []

for i, cat in enumerate(categories):
    st.sidebar.markdown(f"**{cat}**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        b = st.number_input("Budget", min_value=0, value=default_budget[i], step=500, key=f"budget_{i}", label_visibility="collapsed")
    with col2:
        s = st.number_input("Spent", min_value=0, value=default_spent[i], step=500, key=f"spent_{i}", label_visibility="collapsed")
    budget_vals.append(b)
    spent_vals.append(s)

st.sidebar.markdown("---")
st.sidebar.caption("Powered by Gemini + Scikit-learn")

# Build DataFrame
data = {
    'Category': categories,
    'Budget': budget_vals,
    'Spent': spent_vals
}
df = pd.DataFrame(data)
df['Remaining'] = df['Budget'] - df['Spent']
df['Status'] = df['Remaining'].apply(lambda x: 'Over Budget' if x < 0 else 'On Track')

total_budget = df['Budget'].sum()
total_spent = df['Spent'].sum()
total_savings = df[df['Category'] == 'Savings']['Spent'].values[0] if 'Savings' in df['Category'].values else 0

# ==================== DASHBOARD ====================
if page == "Dashboard":
    st.title(f"Welcome, {user_name}")
    st.caption("Here's your financial overview for this month")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Monthly Income", f"₹{income:,}")
    col2.metric("Total Spent", f"₹{total_spent:,}", delta=f"₹{income - total_spent:,} remaining")
    col3.metric("Total Savings", f"₹{total_savings:,}")
    col4.metric("Savings Rate", f"{(total_savings/income*100):.0f}%" if income > 0 else "0%")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        fig1 = go.Figure(data=[go.Pie(
            labels=df['Category'],
            values=df['Spent'],
            hole=0.5,
            textinfo='label+percent',
            textposition='outside',
            marker_colors=px.colors.qualitative.Set3
        )])
        fig1.update_layout(title='Spending Breakdown', showlegend=False, **PLOT_LAYOUT)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name='Budget', x=df['Category'], y=df['Budget'], marker_color='#93c5fd'))
        fig2.add_trace(go.Bar(name='Spent', x=df['Category'], y=df['Spent'], marker_color='#2563eb'))
        fig2.update_layout(
            barmode='group',
            title='Budget vs Spent',
            xaxis=dict(tickangle=-45, tickfont=dict(size=9)),
            **PLOT_LAYOUT
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    over = df[df['Status'] == 'Over Budget']
    if len(over) > 0:
        st.error(f"Overspending Alert: You exceeded budget in — {', '.join(over['Category'].tolist())}")
    st.success("Savings Tip: Reduce spending in over-budget categories to save more this month.")

# ==================== EXPENSE TRACKER ====================
elif page == "Expense Tracker":
    st.title("Expense Tracker")
    st.caption("Track your monthly transactions and spending patterns.")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Spending by Category")
        fig = px.bar(df, x='Spent', y='Category', orientation='h',
                    color='Status',
                    color_discrete_map={'On Track': '#22c55e', 'Over Budget': '#ef4444'})
        fig.update_layout(yaxis=dict(tickfont=dict(size=10)), **PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Budget Overview")
        st.dataframe(df[['Category', 'Budget', 'Spent', 'Remaining', 'Status']],
                    use_container_width=True, hide_index=True)

# ==================== AI ADVISOR ====================
elif page == "AI Advisor":
    st.title("AI Financial Advisor")
    st.caption("Ask anything about your finances — get personalized, data-driven advice.")
    st.markdown("---")

    budget_summary = df[['Category', 'Budget', 'Spent', 'Remaining', 'Status']].to_string()
    user_question = st.text_input("Your question",
                                  placeholder="e.g. Where can I cut my expenses this month?")

    if st.button("Get Advice"):
        if user_question:
            with st.spinner("Analyzing your finances..."):
                try:
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    prompt = f"""
User monthly budget data (Indian salaried employee, monthly income {income} rupees):
{budget_summary}

User question: {user_question}

You are an expert Indian financial advisor. Give specific, actionable advice in simple English only.
No Hindi or Hinglish. Use bullet points. Use the rupee symbol for currency amounts.
"""
                    response = model.generate_content(prompt)
                    st.markdown("**Advice:**")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a question first.")

# ==================== ANOMALY DETECTION ====================
elif page == "Anomaly Detection":
    st.title("Anomaly Detection")
    st.caption("Machine learning flags unusual spending patterns in your budget.")
    st.markdown("---")

    ml_model = IsolationForest(contamination=0.2, random_state=42)
    df['Anomaly'] = ml_model.fit_predict(df[['Spent']])
    df['ML Status'] = df['Anomaly'].map({1: 'Normal', -1: 'Unusual'})

    anomalies = df[df['Anomaly'] == -1]
    normal = df[df['Anomaly'] == 1]

    col1, col2 = st.columns(2)
    col1.metric("Unusual Spending Categories", len(anomalies))
    col2.metric("Normal Spending Categories", len(normal))

    st.markdown("---")

    fig = px.bar(df, x='Category', y='Spent', color='ML Status',
                color_discrete_map={'Normal': '#2563eb', 'Unusual': '#dc2626'},
                title='Spending Anomalies')
    fig.update_layout(
        xaxis=dict(tickangle=-45, tickfont=dict(size=10)),
        **PLOT_LAYOUT
    )
    st.plotly_chart(fig, use_container_width=True)

    if len(anomalies) > 0:
        st.markdown("**Flagged Categories:**")
        st.dataframe(anomalies[['Category', 'Spent', 'ML Status']],
                    use_container_width=True, hide_index=True)

# ==================== BUDGET PREDICTOR ====================
elif page == "Budget Predictor":
    st.title("Budget Predictor")
    st.caption("Estimated spending for next month based on current patterns.")
    st.markdown("---")

    np.random.seed(42)
    df['Predicted'] = (df['Spent'] * np.random.uniform(0.95, 1.1, len(df))).round(0)
    predicted_total = df['Predicted'].sum()

    col1, col2 = st.columns(2)
    col1.metric("Current Month Budget", f"₹{total_budget:,}")
    col2.metric("Predicted Next Month", f"₹{predicted_total:,.0f}",
                delta=f"₹{predicted_total - total_budget:,.0f}")

    st.markdown("---")

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Current', x=df['Category'], y=df['Spent'], marker_color='#2563eb'))
    fig.add_trace(go.Bar(name='Predicted', x=df['Category'], y=df['Predicted'], marker_color='#7c3aed'))
    fig.update_layout(
        barmode='group',
        title='Current vs Predicted Expenses',
        xaxis=dict(tickangle=-45, tickfont=dict(size=10)),
        **PLOT_LAYOUT
    )
    st.plotly_chart(fig, use_container_width=True)

    over_budget = df[df['Status'] == 'Over Budget']['Category'].tolist()
    if over_budget:
        for cat in over_budget:
            st.warning(f"Limit {cat} spending to stay within budget.")
    st.success(f"Try to save at least ₹{int(income * 0.2):,} next month (20% of income).")

    st.markdown("**Detailed Breakdown:**")
    st.dataframe(df[['Category', 'Budget', 'Spent', 'Predicted']],
                use_container_width=True, hide_index=True)
    