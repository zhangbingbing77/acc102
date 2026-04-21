# 📊 Tech Stock Decision Assistant

## 1. Objective
This project aims to help retail investors compare major tech stocks and make better investment decisions based on data.

## 2. Target Users
- Beginner investors  
- Business students  
- Individuals comparing tech companies (AAPL, MSFT, GOOGL, etc.)

## 3. Features
- 📈 Stock price trend visualization  
- 📊 Financial metrics comparison  
- 🧮 Investment scoring system (growth, profitability, risk)  
- 👤 User preference (Conservative / Balanced / Aggressive)  
- 💡 Automated investment recommendation  

## 4. Data Source
- Yahoo Finance (via yfinance)  
- Data retrieved in April 2026  

## 5. Methodology
- CAGR (Compound Annual Growth Rate) for growth  
- ROE & Net Margin for profitability  
- Debt-to-Equity for risk  
- Ranking-based scoring model  

## 6. How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
