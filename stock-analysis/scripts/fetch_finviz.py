#!/usr/bin/env python3
"""
Fetch key technical and fundamental data for a ticker from Finviz.
Usage: python3 fetch_finviz.py TICKER
Output: JSON to stdout
"""

import sys
import json
import re
import ssl
import urllib.request
from html.parser import HTMLParser

try:
    import certifi
    _SSL_CAFILE = certifi.where()
except ImportError:
    _SSL_CAFILE = None

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

WANTED = {
    "Index", "Market Cap", "P/E", "Forward P/E", "PEG", "P/S", "P/B", "P/C",
    "EPS (ttm)", "EPS next Y", "EPS next Q", "EPS this Y", "EPS Q/Q",
    "Sales Q/Q", "EPS past 5Y", "Sales past 5Y",
    "Income", "Sales", "Book/sh", "Cash/sh",
    "Dividend", "Dividend %", "Employees",
    "Optionable", "Shortable",
    "Recom", "Avg Volume", "Rel Volume", "Price", "Change", "Volume",
    "52W Range", "52W High", "52W Low",
    "RSI (14)", "Volatility",
    "SMA20", "SMA50", "SMA200",
    "Short Float", "Short Ratio", "Short Interest",
    "Insider Own", "Insider Trans", "Inst Own", "Inst Trans",
    "ROA", "ROE", "ROI",
    "Gross M", "Oper M", "Profit M",
    "Perf Week", "Perf Month", "Perf Quarter", "Perf Half Y", "Perf Year", "Perf YTD",
    "Earnings", "Target Price", "ATR (14)", "Beta",
}


class SnapshotParser(HTMLParser):
    """Parse Finviz snapshot table into label→value dict."""

    def __init__(self):
        super().__init__()
        self.data: dict[str, str] = {}
        self._in_snapshot = False
        self._in_label = False
        self._in_value = False
        self._pending_label: str | None = None
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class", "")
        if "snapshot-table2" in cls:
            self._in_snapshot = True
            return
        if not self._in_snapshot:
            return
        if tag == "div":
            if "snapshot-td-label" in cls:
                self._in_label = True
                self._buf = ""
            elif "snapshot-td-content" in cls:
                self._in_value = True
                self._buf = ""

    def handle_endtag(self, tag):
        if not self._in_snapshot:
            return
        if tag == "div":
            if self._in_label:
                self._pending_label = self._buf.strip()
                self._in_label = False
                self._buf = ""
            elif self._in_value:
                if self._pending_label:
                    self.data[self._pending_label] = self._buf.strip()
                    self._pending_label = None
                self._in_value = False
                self._buf = ""

    def handle_data(self, data):
        if self._in_label or self._in_value:
            self._buf += data


def fetch(ticker: str) -> dict:
    url = f"https://finviz.com/quote.ashx?t={ticker.upper()}&ty=c&p=d&b=1"
    req = urllib.request.Request(url, headers=HEADERS)
    ctx = ssl.create_default_context(cafile=_SSL_CAFILE)
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
    with opener.open(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    parser = SnapshotParser()
    parser.feed(html)
    raw = parser.data

    if not raw:
        raise ValueError(
            f"No data parsed for {ticker}. "
            "Finviz may have changed its layout or rate-limited this request."
        )

    result: dict = {"ticker": ticker.upper()}

    # Include only fields relevant to IBD analysis
    for label, value in raw.items():
        if label in WANTED:
            key = label.lower().replace("/", "_").replace(" ", "_").replace("(", "").replace(")", "").replace("%", "pct")
            result[key] = value

    # Derived: % below 52-week high
    try:
        price_str = raw.get("Price", "")
        high_str = raw.get("52W High", "")
        price = float(re.sub(r"[^\d.]", "", price_str))
        high = float(re.sub(r"[^\d.]", "", high_str))
        if price and high:
            result["pct_below_52w_high"] = f"{((high - price) / high * 100):.1f}%"
    except (ValueError, ZeroDivisionError, AttributeError):
        pass

    # Derived: % above/below 50-day MA
    try:
        sma50_str = raw.get("SMA50", "")
        if "%" in sma50_str:
            result["price_vs_sma50"] = sma50_str  # Finviz already gives % above/below
    except AttributeError:
        pass

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_finviz.py TICKER", file=sys.stderr)
        sys.exit(1)

    ticker = sys.argv[1]
    try:
        data = fetch(ticker)
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e), "ticker": ticker.upper()}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
