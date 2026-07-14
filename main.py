from __future__ import annotations

from datetime import date
from io import StringIO
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse

from psx_client import fetch_historical_data, fetch_symbols


app = FastAPI(
    title="PSX REST API",
    description="A simple REST API for Pakistan Stock Exchange data",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "PSX REST API is running",
        "available_endpoints": [
            "/",
            "/health",
            "/symbols",
            "/info/{symbol}",
            "/latest/{symbol}",
            "/historical/{symbol}",
            "/download/{symbol}",
        ],
        "examples": [
            "/health",
            "/symbols",
            "/symbols?limit=10",
            "/info/HBL",
            "/latest/HBL",
            "/historical/HBL",
            "/historical/HBL?limit=5",
            "/historical/HBL?limit=5&order=asc",
            "/historical/HBL?limit=5&order=desc",
            "/download/HBL",
            "/download/HBL?start=2021-01-01&end=2026-07-13",
        ],
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "API is healthy",
    }


@app.get("/symbols")
def get_symbols(
    limit: Optional[int] = Query(default=None, ge=1, le=5000),
):
    try:
        symbols = fetch_symbols()
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not fetch symbols from PSX: {exc}",
        )

    total_count = len(symbols)

    if limit is not None:
        symbols = symbols[:limit]

    return {
        "total_count": total_count,
        "returned_count": len(symbols),
        "data": symbols,
    }


@app.get("/info/{symbol}")
def get_symbol_info(symbol: str):
    symbol = symbol.upper().strip()

    try:
        symbols = fetch_symbols()
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not fetch symbols from PSX: {exc}",
        )

    for item in symbols:
        if item["symbol"] == symbol:
            return item

    raise HTTPException(
        status_code=404,
        detail=f"No symbol information found for '{symbol}'.",
    )


@app.get("/latest/{symbol}")
def get_latest_data(symbol: str):
    try:
        df = fetch_historical_data(symbol=symbol)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not fetch data from PSX: {exc}",
        )

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No historical data found for symbol '{symbol.upper()}'.",
        )

    df = df.sort_values("date", ascending=False)

    latest_row = df.iloc[0].copy()
    latest_row["date"] = latest_row["date"].strftime("%Y-%m-%d")

    return {
        "symbol": symbol.upper(),
        "data": latest_row.to_dict(),
    }


@app.get("/historical/{symbol}")
def get_historical_data(
    symbol: str,
    start: Optional[date] = Query(default=None),
    end: Optional[date] = Query(default=None),
    limit: Optional[int] = Query(default=None, ge=1, le=5000),
    order: str = Query(default="asc"),
):
    order = order.lower().strip()

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="order must be either 'asc' or 'desc'",
        )

    if start is not None and end is not None and start > end:
        raise HTTPException(
            status_code=400,
            detail="start date cannot be after end date",
        )

    try:
        df = fetch_historical_data(
            symbol=symbol,
            start=start,
            end=end,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not fetch data from PSX: {exc}",
        )

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No historical data found for symbol '{symbol.upper()}'.",
        )

    total_count = len(df)

    if order == "desc":
        df = df.sort_values("date", ascending=False)
    else:
        df = df.sort_values("date", ascending=True)

    if limit is not None:
        df = df.head(limit)

    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    return {
        "symbol": symbol.upper(),
        "total_count": total_count,
        "returned_count": len(df),
        "order": order,
        "start": df["date"].iloc[-1] if order == "desc" else df["date"].iloc[0],
        "end": df["date"].iloc[0] if order == "desc" else df["date"].iloc[-1],
        "data": df.to_dict(orient="records"),
    }


@app.get("/download/{symbol}")
def download_historical_data(
    symbol: str,
    start: Optional[date] = Query(default=None),
    end: Optional[date] = Query(default=None),
):
    if start is not None and end is not None and start > end:
        raise HTTPException(
            status_code=400,
            detail="start date cannot be after end date",
        )

    try:
        df = fetch_historical_data(
            symbol=symbol,
            start=start,
            end=end,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not fetch data from PSX: {exc}",
        )

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No historical data found for symbol '{symbol.upper()}'.",
        )

    df = df.sort_values("date", ascending=True)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    filename = f"{symbol.upper()}_historical_data.csv"

    return StreamingResponse(
        iter([csv_buffer.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )