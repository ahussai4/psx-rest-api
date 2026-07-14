# PSX REST API

A simple REST API for fetching Pakistan Stock Exchange historical data.

This project is built with FastAPI and deployed on Render.

## Live Deployment

The API is publicly available at:

```text
https://psx-rest-api.onrender.com
```

Live examples:

```text
https://psx-rest-api.onrender.com/health
```

```text
https://psx-rest-api.onrender.com/symbols?limit=10
```

```text
https://psx-rest-api.onrender.com/latest/HBL
```

```text
https://psx-rest-api.onrender.com/historical/HBL?limit=5&order=desc
```

```text
https://psx-rest-api.onrender.com/download/HBL
```

## Features

- Fetch historical OHLCV data for PSX symbols
- List available PSX symbols
- Fetch the latest available data for a symbol
- Download historical data as a CSV file
- Filter historical data by start date and end date
- Limit the number of returned rows
- Sort historical data in ascending or descending date order
- Health-check endpoint
- Automatic API documentation with FastAPI

OHLCV means:

- Open
- High
- Low
- Close
- Volume

## Project Structure

```text
psx-rest-api/
├── main.py
├── psx_client.py
├── requirements.txt
├── runtime.txt
├── README.md
├── Procfile
└── .gitignore
```

## Install Dependencies

Create and activate a virtual environment, then install the required packages:

```bash
pip install -r requirements.txt
```

## Run the API Locally

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The API will run locally at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically creates interactive documentation here:

```text
http://127.0.0.1:8000/docs
```

For the deployed API:

```text
https://psx-rest-api.onrender.com/docs
```

## Endpoints

### Home

```text
GET /
```

Example:

```text
https://psx-rest-api.onrender.com/
```

This endpoint returns a basic message and a list of available endpoints.

### Health Check

```text
GET /health
```

Example:

```text
https://psx-rest-api.onrender.com/health
```

Example response:

```json
{
  "status": "ok",
  "message": "API is healthy"
}
```

### Symbols

```text
GET /symbols
```

This endpoint returns available PSX symbols.

Example:

```text
https://psx-rest-api.onrender.com/symbols
```

With limit:

```text
https://psx-rest-api.onrender.com/symbols?limit=10
```

Example response:

```json
{
  "total_count": 1000,
  "returned_count": 10,
  "data": [
    {
      "symbol": "HBL",
      "name": "Habib Bank Limited",
      "sector": "Commercial Banks",
      "is_etf": false,
      "is_debt": false
    }
  ]
}
```

### Latest Data

```text
GET /latest/{symbol}
```

This endpoint returns the most recent available historical row for a PSX symbol.

Example:

```text
https://psx-rest-api.onrender.com/latest/HBL
```

Example response:

```json
{
  "symbol": "HBL",
  "data": {
    "date": "2026-07-13",
    "open": 311.79,
    "high": 315.0,
    "low": 307.99,
    "close": 310.93,
    "volume": 829063
  }
}
```

### Historical Data

```text
GET /historical/{symbol}
```

This endpoint returns historical OHLCV data for a PSX symbol.

Example:

```text
https://psx-rest-api.onrender.com/historical/HBL
```

With filters:

```text
https://psx-rest-api.onrender.com/historical/HBL?start=2021-01-01&end=2026-07-13&limit=5&order=desc
```

## Historical Data Query Parameters

| Parameter | Meaning | Example |
|---|---|---|
| `start` | Start date | `2021-01-01` |
| `end` | End date | `2026-07-13` |
| `limit` | Number of rows to return | `5` |
| `order` | Date order: `asc` or `desc` | `desc` |

## Example Historical Data Response

```json
{
  "symbol": "HBL",
  "total_count": 1366,
  "returned_count": 5,
  "order": "desc",
  "start": "2026-07-07",
  "end": "2026-07-13",
  "data": [
    {
      "date": "2026-07-13",
      "open": 311.79,
      "high": 315.0,
      "low": 307.99,
      "close": 310.93,
      "volume": 829063
    }
  ]
}
```

### CSV Download

```text
GET /download/{symbol}
```

This endpoint downloads historical OHLCV data for a PSX symbol as a CSV file.

Example:

```text
https://psx-rest-api.onrender.com/download/HBL
```

With date filters:

```text
https://psx-rest-api.onrender.com/download/HBL?start=2021-01-01&end=2026-07-13
```

The downloaded file will be named:

```text
HBL_historical_data.csv
```

## CSV Download Query Parameters

| Parameter | Meaning | Example |
|---|---|---|
| `start` | Start date | `2021-01-01` |
| `end` | End date | `2026-07-13` |

## Deployment

This project is deployed on Render.

The start command used for deployment is:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

This command is also stored in the `Procfile`:

```text
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

The Python runtime is pinned in `runtime.txt`:

```text
python-3.12.8
```

## Notes

This project is for educational and research purposes.

Data availability depends on the PSX data source.

Free Render services may sleep after periods of inactivity, so the first request can take a little longer.