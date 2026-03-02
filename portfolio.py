import csv
import os
import yfinance as yf
from colorama import Fore, Style, init

init(autoreset=True)

TRADES_FILE = os.path.join(os.path.dirname(__file__), "trades.csv")

HEADERS = ["Ticker", "Shares", "Avg Cost", "Current Price", "Mkt Value", "P&L", "P&L%", "Today"]


def load_holdings(path: str) -> dict:
    """Read trades.csv and compute current holdings with weighted average cost."""
    holdings = {}  # ticker -> {shares, avg_cost}

    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            ticker = row["ticker"].upper()
            action = row["action"].lower()
            shares = float(row["shares"])
            price = float(row["price"])
            commission = float(row["commission"])

            if ticker not in holdings:
                holdings[ticker] = {"shares": 0.0, "avg_cost": 0.0}

            h = holdings[ticker]

            if action == "buy":
                new_shares = h["shares"] + shares
                total_cost = h["avg_cost"] * h["shares"] + price * shares + commission
                h["avg_cost"] = total_cost / new_shares
                h["shares"] = new_shares
            elif action == "sell":
                h["shares"] -= shares

    # Remove fully-sold positions
    return {t: h for t, h in holdings.items() if h["shares"] > 0}


def colorize(text: str, value: float) -> str:
    if value > 0:
        return Fore.GREEN + text + Style.RESET_ALL
    elif value < 0:
        return Fore.RED + text + Style.RESET_ALL
    return text


def print_table(plain_rows: list[list[str]], colored_rows: list[list[str]]) -> None:
    """Print a table with proper alignment, using plain_rows to measure widths."""
    widths = [len(h) for h in HEADERS]
    for row in plain_rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    header = "  ".join(h.ljust(widths[i]) for i, h in enumerate(HEADERS))
    print(header)
    print("-" * len(header))

    for plain, colored in zip(plain_rows, colored_rows):
        parts = []
        for i, (p, c) in enumerate(zip(plain, colored)):
            padding = widths[i] - len(p)
            parts.append(c + " " * padding)
        print("  ".join(parts))


def main():
    holdings = load_holdings(TRADES_FILE)
    if not holdings:
        print("No open positions found in trades.csv.")
        return

    plain_rows = []
    colored_rows = []
    total_market_value = 0.0
    total_cost_basis = 0.0
    total_today_change = 0.0

    for ticker, h in holdings.items():
        info = yf.Ticker(ticker).fast_info
        price = info["last_price"]
        open_ = info["open"]

        shares = h["shares"]
        avg_cost = h["avg_cost"]
        market_value = price * shares
        cost_basis = avg_cost * shares
        pnl = market_value - cost_basis
        pnl_pct = (pnl / cost_basis) * 100 if cost_basis else 0.0
        today_change = (price - open_) * shares

        total_market_value += market_value
        total_cost_basis += cost_basis
        total_today_change += today_change

        p_ticker    = ticker
        p_shares    = f"{shares:.4g}"
        p_avg_cost  = f"${avg_cost:.2f}"
        p_price     = f"${price:.2f}"
        p_mktval    = f"${market_value:,.2f}"
        p_pnl       = f"${pnl:+,.2f}"
        p_pnl_pct   = f"{pnl_pct:+.2f}%"
        p_today     = f"{today_change:+.2f}"

        plain_rows.append([p_ticker, p_shares, p_avg_cost, p_price, p_mktval, p_pnl, p_pnl_pct, p_today])
        colored_rows.append([
            colorize(p_ticker,   pnl),
            p_shares,
            p_avg_cost,
            colorize(p_price,   price - open_),
            p_mktval,
            colorize(p_pnl,     pnl),
            colorize(p_pnl_pct, pnl),
            colorize(p_today,   today_change),
        ])

    total_pnl = total_market_value - total_cost_basis
    total_pnl_pct = (total_pnl / total_cost_basis) * 100 if total_cost_basis else 0.0

    print("\nPortfolio Holdings\n" + "=" * 85)
    print_table(plain_rows, colored_rows)

    pnl_str = f"${total_pnl:+,.2f}  ({total_pnl_pct:+.2f}%)"
    today_str = f"${total_today_change:+,.2f}"

    print("\nPortfolio Summary\n" + "-" * 45)
    print(f"  Total Market Value : ${total_market_value:>12,.2f}")
    print(f"  Total Cost Basis   : ${total_cost_basis:>12,.2f}")
    print(f"  Total P&L          : {colorize(pnl_str, total_pnl)}")
    print(f"  Today's Change     : {colorize(today_str, total_today_change)}")
    print()


if __name__ == "__main__":
    main()
