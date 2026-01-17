# Stock Training - Time Series Analysis Tool

A browser-based time series analysis application for stock market data using Pyodide (Python in the browser). Analyze stock trends, volatility, and perform technical analysis without any backend setup.

## Features

- 📊 **Interactive Charts**: Price trends, volatility analysis, moving averages
- 📈 **Technical Analysis**: 50-day and 200-day moving averages, return calculations
- 📁 **CSV Upload**: Upload your own stock data files
- 🌐 **No Backend Required**: Runs entirely in the browser using Pyodide
- 🤖 **AI Assistant Panel**: Get insights and ask questions about your data

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
