# Market Monitor

A command-line tool that fetches and displays live stock prices in a color-coded table.

## Features

- Live price data via Yahoo Finance
- Displays Price, Change, Open, High, Low, and Volume
- Color-coded output: green = up from open, red = down from open

## Setup

```bash
python -m venv venv
venv\Scripts\pip install -r requirements.txt
```

## Usage

```bash
venv\Scripts\python monitor.py
```

Example output:

```
Market Monitor
=================================================================
        Ticker    Price              Change    Open    High     Low      Volume
  AAPL $272.95  [-] -2.00 (-0.73%) $274.95 $276.11 $270.80  32,292,600
  MSFT $401.72  [-] -2.99 (-0.74%) $404.71 $407.49 $398.74  34,283,500
  META $657.01  [+] +6.46 (+0.99%) $650.55 $661.00 $647.50  10,611,800
```

## Adding Stocks

Edit the `TICKERS` list at the top of `monitor.py`:

```python
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"]
```
