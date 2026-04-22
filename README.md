# Interactive Stock Analysis Tool for AAPL, MSFT, AMZN, TSLA

## Student Information
- **Name:** Bingbing Zhang 
- **Student ID:** 2469540
- **Module:** ACC102 
- **Track4**: Interactive Data Analysis Tool 

## 1. Project Title
**Interactive Stock Analysis Tool (AAPL, MSFT, AMZN, TSLA)**

## 2. Project Overview
This project is an interactive data analysis tool designed to explore historical stock performance of Apple (AAPL), Microsoft (MSFT), Amazon (AMZN), and Tesla (TSLA) from 2020 to 2025.  

- **Problem:** Users need a simple and visual way to analyze and compare multiple stock trends, returns, correlations, and portfolio performance.  
- **Target Users:** Individual investors, finance students, and analysts interested in technology stocks.  
- **Tool Capabilities:**  
  - Visualize adjusted close prices and daily returns  
  - Compute and display 50-day moving averages  
  - Show correlation heatmaps between selected stocks  
  - Simulate an equal-weight portfolio cumulative return  
  - Allow interactive stock selection and time range filtering  
  - Download filtered dataset as CSV  

## 3. Dataset Description
- **Data File:** `data/stock_data.csv` (full dataset, uploaded to GitHub)  
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
- **Data Size:** Full dataset uploaded (~<25MB each or merged)  
- **Note:** The CSV is complete, ensuring reproducibility; no external download required.

## 4. How to Run
1. Clone the repository:
```bash
git clone <your-repo-url>
cd StockAnalysis

	2.	Install dependencies:

pip install -r requirements.txt

	3.	Run the Streamlit app:

streamlit run app.py

	•	Python Version: 3.9+ recommended
	•	The app is fully local and uses relative paths (data/stock_data.csv).

5. Project Structure

StockAnalysis/
├─ app.py                 # Streamlit interactive tool
├─ notebooks/
│  └─ analysis.ipynb      # Data cleaning and analysis workflow
├─ data/
│  └─ stock_data.csv      # Full stock dataset
├─ requirements.txt       # Python dependencies
├─ README.md              # Project documentation
└─ videos/
    └─ demo.mp4           # Demonstration video

6. Features
	•	Multi-stock selection (AAPL, MSFT, AMZN, TSLA)
	•	Adjustable date range filter (2020–2025)
	•	Interactive line charts for adjusted close prices
	•	Optional 50-day moving average overlay
	•	Daily return line chart visualization
	•	Correlation heatmap of selected stocks
	•	Equal-weight portfolio cumulative return chart
	•	Download filtered dataset as CSV

7. Key Analysis
	•	Data Cleaning: Convert date column to datetime, ensure positive prices, forward-fill missing values
	•	Feature Engineering: Compute Adj Close and Daily Return, calculate 50-day moving average
	•	Pandas/Numpy Operations: Filtering by ticker and date range, groupby operations, cumulative product for portfolio return
	•	Visualization:
	•	Matplotlib for line charts
	•	Seaborn for correlation heatmap
	•	Interactivity: Streamlit widgets for stock selection, date range, toggle options for moving averages, correlation, and portfolio

8. Results & Insights
	•	Price Trends: AAPL and MSFT show steady growth; TSLA is highly volatile
	•	Daily Returns: Most returns center around zero; TSLA and AMZN show occasional extreme changes
	•	Correlation: High correlation between AAPL and MSFT; moderate correlations for AMZN and TSLA
	•	Portfolio Performance: Equal-weight portfolio smooths individual stock volatility and provides a diversified return perspective
	•	Business Value: Users can visually compare multiple stocks, understand correlations, and simulate simple portfolios for decision-making

9. Limitations & Improvements
	•	Analysis only includes price and return data; fundamental or macroeconomic factors are not considered
	•	Portfolio simulation is simplified; no transaction costs or risk adjustments included
	•	Future improvements: Add interactive technical indicators, multiple portfolio strategies, and predictive analytics
如果你愿意，我可以帮你接着写 **高分反思报告模板（500–800 词）**，包含 AI 使用披露、局限性说明和改进建议，直接可提交。  

你希望我帮你写吗？
