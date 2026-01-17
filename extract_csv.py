# pip install yfinance pandas

import yfinance as yf
from datetime import datetime, timedelta

def get_inputs():
    symbol = input("Enter stock symbol (e.g., TECHM.NS, AAPL, RELIANCE.NS): ").strip().upper()
    if not symbol:
        raise ValueError("Stock symbol cannot be empty.")

    years_str = input("Enter number of years (e.g., 1, 3, 5): ").strip()
    try:
        years = float(years_str)
        if years <= 0:
            raise ValueError
    except Exception:
        raise ValueError("Years must be a positive number (e.g., 1, 3, 5).")

    return symbol, years

def download_to_csv(symbol: str, years: float):
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=int(years * 365.25))  # timedelta-based

    # yfinance treats end as exclusive; +1 day helps include the latest daily bar
    df = yf.download(
        symbol,
        start=start_dt.strftime("%Y-%m-%d"),
        end=(end_dt + timedelta(days=1)).strftime("%Y-%m-%d"),
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        raise RuntimeError(f"No data returned for '{symbol}'. Check the symbol and try again.")

    df = df.reset_index()  # keep Date as a column for Excel
    safe_symbol = symbol.replace("^", "").replace("/", "_").replace("\\", "_")
    outfile = f"{safe_symbol}_{years:g}y.csv"
    df.to_csv(outfile, index=False)
    print(f"Saved {len(df)} rows to: {outfile}")

if __name__ == "__main__":
    symbol, years = get_inputs()
    download_to_csv(symbol, years)
