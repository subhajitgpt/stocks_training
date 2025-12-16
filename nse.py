#!/usr/bin/env python3
"""
Hybrid NSE + ADR Stock Data Fetcher (Interactive Version)

- Asks for SYMBOL in console
- Fetches NSE data via nsepython
- Fetches ADR data via yfinance
- Saves outputs into ./data/ folder as CSV
- Last 8 years of OHLCV

Author: Subhajit + ChatGPT
"""

import pandas as pd
from datetime import date, timedelta
import os
import sys

# ---------- USER INPUT ----------
SYMBOL = input("Enter NSE Symbol (e.g., INFY, TCS, RELIANCE): ").strip().upper()
ADR_TICKER = SYMBOL  # assuming ADR uses same base symbol
YEARS_BACK = 3

# ---------- DATA FOLDER ----------
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# ---------- DATE RANGE ----------
end_date = date.today()
start_date = end_date - timedelta(days=365 * YEARS_BACK)

print(f"\nFetching {SYMBOL} data from {start_date} to {end_date}...\n")

# ---------- 1. NSE FETCH ----------
def fetch_nse_history(symbol: str, start: date, end: date) -> pd.DataFrame:
    try:
        from nsepython import equity_history
    except ImportError:
        print("ERROR: nsepython missing → pip install nsepython")
        return pd.DataFrame()

    start_str = start.strftime("%d-%m-%Y")
    end_str = end.strftime("%d-%m-%Y")

    print(f"[NSE] Downloading {symbol}...")

    try:
        data = equity_history(
            symbol=symbol,
            series="EQ",
            start_date=start_str,
            end_date=end_str
        )

        if data.empty:
            print("[NSE] No data returned.")
            return pd.DataFrame()

        col_map = {
            "CH_TIMESTAMP": "Date",
            "TIMESTAMP": "Date",
            "CH_OPENING_PRICE": "Open",
            "CH_TRADE_HIGH_PRICE": "High",
            "CH_TRADE_LOW_PRICE": "Low",
            "CH_CLOSING_PRICE": "Close",
            "CH_TOT_TRADED_QTY": "Volume"
        }

        data = data.rename(columns={k: v for k, v in col_map.items() if k in data.columns})
        data["Date"] = pd.to_datetime(data["Date"])
        data = data.sort_values("Date").set_index("Date")

        data = data[["Open", "High", "Low", "Close", "Volume"]].apply(pd.to_numeric, errors="coerce")

        print(f"[NSE] Rows fetched: {len(data)}")
        return data

    except Exception as e:
        print(f"[NSE] ERROR: {e}")
        return pd.DataFrame()


# ---------- 2. ADR FETCH ----------
def fetch_adr_history(ticker: str, start: date, end: date) -> pd.DataFrame:
    try:
        import yfinance as yf
    except ImportError:
        print("ERROR: yfinance missing → pip install yfinance")
        return pd.DataFrame()

    print(f"[ADR] Downloading {ticker} ADR...")

    try:
        df = yf.download(ticker, start=start, end=end, progress=False)
        if df.empty:
            print("[ADR] No data returned.")
            return pd.DataFrame()

        df = df[["Open", "High", "Low", "Close", "Volume"]]
        df.index = pd.to_datetime(df.index)
        df = df.apply(pd.to_numeric, errors="coerce")

        print(f"[ADR] Rows fetched: {len(df)}")
        return df

    except Exception as e:
        print(f"[ADR] ERROR: {e}")
        return pd.DataFrame()


# ---------- 3. RUN ----------
nse_df = fetch_nse_history(SYMBOL, start_date, end_date)
adr_df = fetch_adr_history(ADR_TICKER, start_date, end_date)

# ---------- 4. ALIGN & SAVE ----------
if not nse_df.empty:
    if not adr_df.empty:
        common_start = max(nse_df.index.min(), adr_df.index.min())
        common_end = min(nse_df.index.max(), adr_df.index.max())
        nse_df = nse_df.loc[common_start:common_end]

    nse_file = f"{DATA_FOLDER}/{SYMBOL}_nse_ohlcv.csv"
    nse_df.to_csv(nse_file)
    print(f"[NSE] Saved → {nse_file}")

if not adr_df.empty:
    if not nse_df.empty:
        common_start = max(nse_df.index.min(), adr_df.index.min())
        common_end = min(nse_df.index.max(), adr_df.index.max())
        adr_df = adr_df.loc[common_start:common_end]

    adr_file = f"{DATA_FOLDER}/{SYMBOL}_adr_ohlcv.csv"
    adr_df.to_csv(adr_file)
    print(f"[ADR] Saved → {adr_file}")

print("\n✅ DONE: Files are now inside the /data folder")
