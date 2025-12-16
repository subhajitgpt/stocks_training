from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple

import yfinance as yf

DATE_FMT = "%Y-%m-%d"


def parse_date(value: str) -> datetime.date:
    try:
        return datetime.strptime(value, DATE_FMT).date()
    except ValueError as exc:  # pragma: no cover - argparse surfaces this cleanly
        raise argparse.ArgumentTypeError(f"Expected YYYY-MM-DD date, got '{value}'") from exc


def resolve_dates(
    start: datetime.date | None,
    end: datetime.date | None,
    days_back: int,
) -> Tuple[datetime.date, datetime.date]:
    if days_back <= 0:
        raise ValueError("days_back must be positive")

    today = datetime.today().date()
    resolved_end = end or today

    if start and end and start > end:
        raise ValueError("start date must be on or before end date")

    if start and not end:
        resolved_start = start
        resolved_end = start + timedelta(days=days_back)
    elif not start:
        resolved_start = resolved_end - timedelta(days=days_back)
    else:
        resolved_start = start

    if resolved_start > resolved_end:
        raise ValueError("Computed start date is after end date")

    return resolved_start, resolved_end


def download_index_history(
    symbol: str,
    start: datetime.date,
    end: datetime.date,
    output_path: Path,
) -> Path:
    # Ensure consistent ISO formatting for yfinance queries.
    data = yf.download(symbol, start=start.isoformat(), end=end.isoformat(), progress=False)

    if data.empty:
        raise RuntimeError(
            f"No historical data returned for {symbol} between {start.isoformat()} and {end.isoformat()}"
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download an index's historical prices from yfinance and persist as CSV."
    )
    parser.add_argument("symbol", help="Index ticker symbol, e.g. ^GSPC or ^DJI")
    parser.add_argument(
        "--start",
        type=parse_date,
        help="Explicit start date in YYYY-MM-DD format (default: end - days-back)",
    )
    parser.add_argument(
        "--end",
        type=parse_date,
        help="Explicit end date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--days-back",
        type=int,
        default=365,
        help="Number of trailing days to fetch when start or end are omitted (default: 365)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data") / "index_history.csv",
        help="CSV output path (default: data/index_history.csv)",
    )

    args = parser.parse_args()

    try:
        start_date, end_date = resolve_dates(args.start, args.end, args.__dict__["days_back"])
    except ValueError as exc:
        parser.error(str(exc))

    output_path = args.output

    try:
        saved_path = download_index_history(args.symbol, start_date, end_date, output_path)
    except Exception as exc:  # pragma: no cover - CLI path
        parser.error(str(exc))

    print(
        f"Saved {args.symbol} data from {start_date.isoformat()} to {end_date.isoformat()} at {saved_path}"
    )


if __name__ == "__main__":
    main()
