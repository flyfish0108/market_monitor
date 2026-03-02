# Market Monitor

A command-line tool that fetches and displays live stock prices in a color-coded table, with a separate portfolio tracker for P&L on your holdings.

## Features

- Live price data via Yahoo Finance
- Displays Price, Change, Open, High, Low, and Volume
- Color-coded output: green = up from open, red = down from open

## Setup

```bash
python -m venv venv
venv\Scripts\pip install -r requirements.txt
```

## Market Monitor

Displays live prices for a watchlist of tickers.

```bash
venv\Scripts\python monitor.py
```

Or double-click `run.bat` to open in a new Windows Terminal tab.

Example output:

```
Market Monitor
=================================================================
 Ticker    Price              Change    Open    High     Low      Volume
  AAPL $272.95  [-] -2.00 (-0.73%) $274.95 $276.11 $270.80  32,292,600
  MSFT $401.72  [-] -2.99 (-0.74%) $404.71 $407.49 $398.74  34,283,500
  META $657.01  [+] +6.46 (+0.99%) $650.55 $661.00 $647.50  10,611,800
```

### Adding Stocks

Edit the `TICKERS` list at the top of `monitor.py`:

```python
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "RDDT", "U", "DUOL", "PLTR"]
```

## Portfolio Tracker

Reads your trades from `trades.csv` and shows current holdings with P&L.

### trades.csv format

```
date,ticker,action,shares,price,commission
2024-01-15,AAPL,buy,10,185.50,1.00
2024-02-01,AAPL,sell,5,190.00,1.00
```

- `action`: `buy` or `sell`
- `price`: per-share price (use split-adjusted prices for historical trades)
- `commission`: per-trade commission in dollars

### Running

```bash
venv\Scripts\python portfolio.py
```

Or double-click `portfolio.bat` to open in a new Windows Terminal tab.

Example output:

```
Portfolio Holdings
=====================================================================================
Ticker  Shares  Avg Cost  Current Price  Mkt Value   P&L         P&L%      Today
----------------------------------------------------------------------------------
AAPL    5       $185.60   $264.18        $1,320.90   $+392.90    +42.34%   -43.15
MSFT    5       $390.20   $392.74        $1,963.70   $+12.70     +0.65%    +9.30
NVDA    100     $86.16    $177.19        $17,719.00  $+9,102.80  +105.65%  -406.00

Portfolio Summary
---------------------------------------------
  Total Market Value : $   21,003.60
  Total Cost Basis   : $   11,495.20
  Total P&L          : $+9,508.40  (+82.72%)
  Today's Change     : $-439.85
```

Fully sold positions are automatically excluded. P&L uses weighted average cost basis.
