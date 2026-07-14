# PSX REST API

A simple REST API for fetching Pakistan Stock Exchange historical data.

This project is built with FastAPI.

## Features

- Fetch historical OHLCV data for PSX symbols
- List available PSX symbols
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
├── README.md
└── .gitignore
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn main:app --reload
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

## Endpoints

### Home

```text
GET /
```

Example:

```text
http://127.0.0.1:8000/
```

### Health Check

```text
GET /health
```

Example:

```text
http://127.0.0.1:8000/health
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
http://127.0.0.1:8000/symbols
```

With limit:

```text
http://127.0.0.1:8000/symbols?limit=10
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

### Historical Data

```text
GET /historical/{symbol}
```

Example:

```text
http://127.0.0.1:8000/historical/HBL
```

With filters:

```text
http://127.0.0.1:8000/historical/HBL?start=2021-01-01&end=2026-07-13&limit=5&order=desc
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

## Notes

This project is for educational and research purposes.

Data availability depends on the PSX data source.