import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from analysis_lib import fetch_stock_data, calculate_volatility, get_summary_stats

# Page Config
st.set_page_config(page_title="Financial Volatility Analysis", layout="wide", page_icon="📈")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3e4150;
    }
    h1, h2, h3 {
        color: #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Financial Market Volatility Analysis")
st.markdown("Analyze stock market fluctuations and stability metrics.")

# Sidebar
st.sidebar.header("Configuration")
ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL, ^GSPC, BTC-USD)", value="^GSPC")
period = st.sidebar.selectbox("Select Time Period", options=['1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'], index=3)
window = st.sidebar.slider("Rolling Window (Days)", min_value=5, max_value=60, value=21)

# Fetch and Process Data
with st.spinner(f"Fetching data for {ticker}..."):
    raw_data = fetch_stock_data(ticker, period=period)

if raw_data is not None:
    data = calculate_volatility(raw_data, window=window)
    stats = get_summary_stats(data)

    # Determine Close Column
    close_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'

    # Top Row Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Price", f"${data[close_col].iloc[-1]:.2f}")
    col2.metric("Avg Annual Volatility", f"{stats['Average Annualized Volatility']*100:.2f}%")
    col3.metric("Current Annual Volatility", f"{stats['Current Annualized Volatility']*100:.2f}%")
    col4.metric("Max Daily Return", f"{stats['Max Daily Return']*100:.2f}%")

    # Visualizations
    st.subheader("Market Trends & Volatility Analysis")
    
    # 1. Price and Volatility Chart
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.1, 
                        subplot_titles=(f"{ticker} Adjusted Close Price", "Annualized Volatility (Rolling)"))

    # Price Line
    fig.add_trace(go.Scatter(x=data.index, y=data[close_col], name="Price", line=dict(color='#00d4ff', width=2)), row=1, col=1)
    
    # Volatility Line
    fig.add_trace(go.Scatter(x=data.index, y=data['Annualized_Volatility'], name="Volatility", fill='tozeroy', line=dict(color='#ff4b4b', width=2)), row=2, col=1)

    fig.update_layout(height=700, template="plotly_dark", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # 2. Daily Returns Distribution
    st.subheader("Daily Returns Distribution")
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(x=data['Daily_Return'], nbinsx=50, marker_color='#00d4ff', opacity=0.7))
    fig_hist.update_layout(template="plotly_dark", xaxis_title="Daily Return", yaxis_title="Frequency", height=400)
    st.plotly_chart(fig_hist, use_container_width=True)

    # Insights Section
    st.subheader("Stability Insights")
    stability_score = "High" if stats['Average Annualized Volatility'] < 0.15 else "Moderate" if stats['Average Annualized Volatility'] < 0.30 else "Low"
    
    st.info(f"""
    **Market Analysis for {ticker}:**
    - The average annualized volatility over the selected period is **{stats['Average Annualized Volatility']*100:.2f}%**.
    - The current market stability is considered **{stability_score}**.
    - Volatility peaks often correspond to significant market events or price corrections.
    """)

else:
    st.error(f"Could not find data for ticker: {ticker}. Please check the symbol.")

st.markdown("---")
st.markdown("Created for Financial Market Volatility Analysis Mini Project.")
