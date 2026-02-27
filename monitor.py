import pandas as pd
import yfinance as yf
from colorama import Fore, Style, init

init(autoreset=True)

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"]


def colorize(text: str, price: float, open_: float) -> str:
    if price > open_:
        return Fore.GREEN + text + Style.RESET_ALL
    elif price < open_:
        return Fore.RED + text + Style.RESET_ALL
    return text


def get_prices(tickers: list[str]) -> list[dict]:
    rows = []
    for ticker in tickers:
        info = yf.Ticker(ticker).fast_info
        price = info["last_price"]
        open_ = info["open"]
        change = price - open_
        change_pct = (change / open_) * 100
        arrow = "+" if change >= 0 else "-"

        rows.append({
            "Ticker": colorize(ticker, price, open_),
            "Price":  colorize(f"${price:.2f}", price, open_),
            "Change": colorize(f"[{arrow}] {change:+.2f} ({change_pct:+.2f}%)", price, open_),
            "Open":   f"${open_:.2f}",
            "High":   f"${info['day_high']:.2f}",
            "Low":    f"${info['day_low']:.2f}",
            "Volume": f"{info['last_volume']:,}",
        })
    return rows


if __name__ == "__main__":
    print("\nMarket Monitor\n" + "=" * 65)
    rows = get_prices(TICKERS)
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))
    print()
