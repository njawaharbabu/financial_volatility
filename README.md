# Financial Market Volatility Analysis

## Objective
To analyze fluctuations in financial markets using stock datasets, calculate volatility metrics, and visualize trends to assess market stability.

## Features
- **Interactive Dashboard**: Built with Streamlit for real-time analysis.
- **Dynamic Data Fetching**: Uses Yahoo Finance API (`yfinance`) for up-to-date market data.
- **Volatility Metrics**: Calculates Rolling Standard Deviation and Annualized Volatility.
- **Visual Insights**: Interactive charts for price trends, volatility clustering, and return distributions.

## How to Run
1. Navigate to the project directory:
   ```powershell
   cd financial_volatility
   ```
2. Run the Streamlit app:
   ```powershell
   streamlit run dashboard.py
   ```

## Dependencies
- `yfinance`: For fetching stock market data.
- `pandas`: For data manipulation.
- `plotly`: For interactive visualizations.
- `streamlit`: For the web-based dashboard.
