# 📊 WRDS Tech Stock Analyzer

## 1. Objective

This project aims to help retail investors evaluate major tech stocks using **data-driven financial analysis**.

It answers the question:

**Which tech stock provides the best balance of return and risk?**

---

## 2. Target Users

- Beginner investors  
- Business and finance students  
- Users comparing large tech companies  

---

## 3. Data Sources

### Primary Source (Academic)
- WRDS (Wharton Research Data Services)
- CRSP Database
- Data accessed: April 2026

### Secondary Source
- Local fallback dataset (CSV)

---

## 4. Methodology

The project uses financial metrics commonly applied in academic research:

- **Annualized Return**
- **Volatility (Risk)**
- **Sharpe Ratio (Risk-adjusted return)**

A ranking-based scoring model is used to generate investment recommendations.

---

## 5. Features

- 📊 WRDS-based financial analysis  
- 🔄 Real-time WRDS connection (if available)  
- 🛟 Automatic fallback to CSV data  
- 👤 Investor profile (Conservative / Balanced / Aggressive)  
- 📈 Interactive visualization (Plotly)  
- 💡 Automated investment recommendation  

---

## 6. How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
