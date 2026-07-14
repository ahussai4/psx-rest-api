from __future__ import annotations

from datetime import date
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup


PSX_HISTORICAL_URL = "https://dps.psx.com.pk/historical"


def clean_number(value: str):
    """
    Convert text numbers from PSX into Python numbers.

    Examples:
        "1,234"     -> 1234
        "133.50"    -> 133.50
        "-"         -> None
    """
    if value is None:
        return None

    value = str(value).strip().replace(",", "")

    if value == "" or value == "-":
        return None

    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return None


def fetch_historical_data(
    symbol: str,
    start: Optional[date] = None,
    end: Optional[date] = None,
) -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a PSX symbol.

    OHLCV means:
        Open, High, Low, Close, Volume.
    """

    symbol = symbol.upper().strip()

    response = requests.post(
        PSX_HISTORICAL_URL,
        data={"symbol": symbol},
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")

    if table is None:
        return pd.DataFrame(
            columns=["date", "open", "high", "low", "close", "volume"]
        )

    rows = []

    for tr in table.find_all("tr"):
        cells = [cell.get_text(strip=True) for cell in tr.find_all(["td", "th"])]

        if len(cells) < 6:
            continue

        if "date" in cells[0].lower():
            continue

        rows.append(cells[:6])

    if not rows:
        return pd.DataFrame(
            columns=["date", "open", "high", "low", "close", "volume"]
        )

    df = pd.DataFrame(
        rows,
        columns=["date", "open", "high", "low", "close", "volume"],
    )

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    for column in ["open", "high", "low", "close", "volume"]:
        df[column] = df[column].apply(clean_number)

    df = df.dropna(subset=["date", "close"])

    for column in ["open", "high", "low", "close"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").astype("Int64")

    if start is not None:
        df = df[df["date"] >= pd.Timestamp(start)]

    if end is not None:
        df = df[df["date"] <= pd.Timestamp(end)]

    df = df.sort_values("date")
    df = df.drop_duplicates(subset=["date"], keep="last")
    df = df.reset_index(drop=True)

    return df