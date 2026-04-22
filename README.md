# Interactive Stock Analysis Tool for AAPL, MSFT, AMZN, TSLA

## 1. Project Title
**Interactive Stock Analysis Tool (AAPL, MSFT, AMZN, TSLA)**

## 2. Project Overview
This project is an interactive data analysis tool designed to explore historical stock performance of Apple (AAPL), Microsoft (MSFT), Amazon (AMZN), and Tesla (TSLA) from 2020 to 2025.

- **Problem:** Users often need a simple and visual way to analyze and compare multiple stock trends, returns, correlations, and portfolio performance.
- **Target Users:** Individual investors, finance students, and analysts interested in technology stocks.
- **Tool Capabilities:**
  - Visualize adjusted close prices and daily returns
  - Compute and display 50-day moving averages
  - Show correlation heatmaps between selected stocks
  - Simulate an equal-weight portfolio cumulative return
  - Allow interactive stock selection and time range filtering
  - Download filtered dataset as CSV

## 3. Dataset Description
- **Source:** WRDS CRSP Daily Stock Data
- **Tickers:** AAPL, MSFT, AMZN, TSLA
- **Data Retrieval Date:** Latest download on 2026-04-22
- **Key Variables:**
  - `date`: Trading date
  - `ticker`: Stock symbol
  - `prc`: Daily stock price
  - `vol`: Trading volume
  - `Adj Close`: Adjusted close price (computed)
  - `Daily Return`: Percentage daily change (computed)
- **Data Size:** CSV file uploaded in `data/stock_data_sample.csv` (~small sample <25MB)
- **Note:** Full WRDS data requires access; uploaded CSV ensures reproducibility with relative paths.

## 4. How to Run Locally (Mac Compatible)
1. Clone the repository:
```bash
git clone https://github.com/zhangbingbing77/acc102.git
cd acc102
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app locally:
```bash
streamlit run app.py
```

- Python Version: 3.9+ recommended
- The app is fully local and uses relative paths (`data/stock_data_sample.csv`).
- Streamlit Cloud deployment is NOT used, which complies with Track 4 requirements.

## 5. Project Structure
```
acc102/
├─ app.py                 # Streamlit interactive tool
├─ ACC102_Financial_Analysis.ipynb      # Data cleaning and analysis workflow
├─ data/
│  └─ stock_data_sample.csv          # Sample stock data
├─ requirements.txt       # Python dependencies
├─ README.md              # Project documentation
└─ .gitignore
```

## 6. Features
- Multi-stock selection (AAPL, MSFT, AMZN, TSLA)
- Adjustable date range filter (2020–2025)
- Interactive line charts for adjusted close prices
- Optional 50-day moving average overlay
- Daily return line chart visualization
- Correlation heatmap of selected stocks
- Equal-weight portfolio cumulative return chart
- Download filtered dataset as CSV

## 7. Methodology & Analysis Process
- Data Cleaning: Convert date column to datetime, ensure positive prices, forward-fill missing values
- Feature Engineering: Compute Adj Close and Daily Return, calculate 50-day moving average
- Pandas/Numpy Operations: Filtering by ticker and date range, groupby operations, cumulative product for portfolio return
- Visualization:
  - Plotly interactive line charts for price and return trends
  - Seaborn-style correlation heatmap
- Interactivity: Streamlit widgets for stock selection, date range, toggle options for moving averages, correlation, and portfolio

## 8. Results & Insights
- Price Trends: AAPL and MSFT show steady growth; TSLA is highly volatile
- Daily Returns: Most returns center around zero; TSLA and AMZN show occasional extreme changes
- Correlation: High correlation between AAPL and MSFT; moderate correlations for AMZN and TSLA
- Portfolio Performance: Equal-weight portfolio smooths individual stock volatility and provides a diversified return perspective
- Business Value: Users can visually compare multiple stocks, understand correlations, and simulate simple portfolios for decision-making

## 9. Limitations & Future Improvements
- Analysis only includes price and return data; fundamental or macroeconomic factors are not considered
- Portfolio simulation is simplified; no transaction costs or risk adjustments included
- Data sample in the repository is limited; full WRDS dataset required for extended analysis
- Future improvements: Add interactive technical indicators, multiple portfolio strategies, and predictive analytics

## 10. Compliance Notes
- All file paths are relative paths, no hard-coded absolute local paths
- All code, comments and documentation are written in English
- Project follows Track 4 Interactive Data Analysis Tool requirements
- Local Streamlit execution only, no Streamlit Cloud deployment
- Sample data uploaded for reproducibility, full data source stated as WRDS CRSP
```
