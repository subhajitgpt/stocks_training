# Stock Training - Time Series Analysis Tool

A browser-based time series analysis application for stock market data using Pyodide (Python in the browser). Analyze stock trends, volatility, and perform technical analysis without any backend setup.

## Features

- 📊 **Interactive Charts**: Price trends, volatility analysis, moving averages, RSI
- 📈 **Technical Analysis**: 
  - 50-day and 200-day moving averages
  - RSI (Relative Strength Index) with overbought/oversold levels
  - Return calculations and volatility metrics
- 🤖 **AI-Powered Recommendations**: Automatically generates investment insights using OpenAI GPT-4o
- 📁 **CSV Upload**: Upload your own stock data files
- 🌐 **No Backend Required**: Runs entirely in the browser using Pyodide
- 💬 **AI Assistant Panel**: Get insights and ask questions about your data

## CSV File Requirements

Your CSV file should contain the following columns (column names are automatically normalized):

### Required Columns:
- **Date** (accepts: Date, Timestamp, Time)
- **Close** (accepts: Close, Closing_Price, Adj Close, Adj_Close)

### Optional Columns:
- **Open** (accepts: Open, Opening_Price)
- **High** (accepts: High, High_Price)
- **Low** (accepts: Low, Low_Price)
- **Volume** (accepts: Volume, Vol, Trading_Volume)

### Data Handling:
- ✅ Automatically handles spaces in column names (converts to underscores)
- ✅ Removes commas from numeric values
- ✅ Handles duplicate column names by adding suffixes
- ✅ Removes duplicate columns after mapping (keeps first occurrence)
- ✅ Supports various date formats
- ✅ Strips whitespace from column names

### Example CSV Format:
```csv
Date,Close,Open,High,Low,Volume
17/05/2022,849.8522,875.25,918.95,860,872
18/05/2022,850.9203,876.35,891,874.1,885.55
19/05/2022,816.45,840.85,867,838,867
```

## Getting Started

1. Open `index.html` in a modern web browser
2. Wait for Pyodide to load
3. Upload your CSV file or use the sample data
4. View the generated charts and analysis
5. **Automatic AI Recommendation**: After analysis completes, the AI assistant automatically generates investment recommendations based on:
   - Current price and price trends
   - RSI signals (overbought/oversold conditions)
   - Moving average patterns (Golden/Death Cross)
   - Volatility analysis
   - Overall market sentiment

## n8n World-Events Correlation (Optional)

This project includes an optional integration to n8n that:

- Converts your latest analysis into a JSON payload (including recent daily returns)
- Sends it to an n8n webhook when you click **Invoke n8n**
- Enriches it with world-event signals (war/conflict intensity + oil/energy headlines)
- Returns a structured response that the UI renders as metric cards + news lists + a short summary

### Setup

1. Install and start n8n (any recent version).
2. Import the workflow JSON: `n8n/stock-world-correlation-patched.json`
3. In n8n, activate the workflow.
4. Open `index.html`, run **Analyze** on a CSV, then go to the **🧩 n8n Correlation** tab.
5. Ensure the webhook URL matches your n8n instance (default):

  `http://localhost:5678/webhook/stock-world-correlation`

### What the UI shows

The **🧩 n8n Correlation** tab renders these stock-related values (when available):

- `ticker`, `symbol`, `source_file`
- `current_price`, `price_change_pct`
- `rsi_14`
- `current_volatility_pct`, `avg_volatility_pct`
- `ma_signal`, `ma_50`, `ma_200`
- `recent_stock_return_pct`

And these macro/correlation values:

- `overall_macro_risk`
- `war_news_risk_score`, `oil_risk_score`
- `likely_oil_sensitivity`, `likely_war_sensitivity`
- `effect_on_stock`

It also lists the returned **war** and **oil/energy** news items and prints the workflow’s `summary`.

### Notes

- If you open `index.html` via `file://` and the webhook call fails, serve the folder via a local web server (so the browser origin is not `null`) and/or enable CORS for your n8n instance.

## AI-Powered Analysis

The application includes an intelligent AI assistant that:
- **Automatically analyzes** all technical indicators after each data upload
- **Generates recommendations** considering RSI, moving averages, and volatility
- Provides insights on market sentiment, key signals, and risk assessment
- Can answer follow-up questions about your data
- Supports image upload for chart analysis

## Technical Details

- **Python Environment**: Pyodide v0.24.1
- **Libraries Used**: pandas, matplotlib, numpy
- **Client-Side Processing**: All analysis runs in the browser
- **No Installation Required**: Just open the HTML file

## Files

- `index.html` - Main application file
- `data/` - Sample CSV files for testing
- `generate_csv.py` - Utility to generate sample data
- `encrypt_keys.py` - Key encryption utility

## Browser Compatibility

Works best in modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari

## Notes

- First load may take a few seconds while Pyodide initializes
- Large CSV files (>10,000 rows) may take longer to process
- All processing happens locally in your browser
