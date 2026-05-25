#!/usr/bin/env python3
"""
Fetch recent news headlines for a ticker from Finviz.
Usage: python3 fetch_news.py TICKER
Output: numbered list with date, signal tag, and headline to stdout
"""

import sys
import re
import ssl
import urllib.request

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

RISK_KEYWORDS = [
    "miss", "misses", "cut", "cuts", "downgrade", "downgrades",
    "lawsuit", "probe", "investigation", "fine", "recall", "warning",
    "loss", "losses", "decline", "drop", "fell", "fall", "short sell",
    "insider sell", "revenue miss", "guidance cut", "layoff", "layoffs",
]

CATALYST_KEYWORDS = [
    "beat", "beats", "upgrade", "upgrades", "raise", "raises", "raised",
    "record", "new high", "partnership", "contract", "approval", "approved",
    "launch", "launches", "acquisition", "buyback", "dividend", "breakout",
    "insider buy", "outperform", "strong", "surge", "jumps", "record high",
    "earnings beat", "revenue beat", "price target raised",
]

SOURCE_RE = re.compile(r"trackAndOpenNews\(event,\s*'([^']*)',\s*'([^']*)'")
DATE_RE = re.compile(r"<td[^>]*width=\"130\"[^>]*>\s*(.*?)\s*</td>", re.DOTALL)
HEADLINE_RE = re.compile(r'<a class="tab-link-news"[^>]*>\s*(.*?)\s*</a>', re.DOTALL)


def classify(headline: str) -> str:
    h = headline.lower()
    is_catalyst = any(kw in h for kw in CATALYST_KEYWORDS)
    is_risk = any(kw in h for kw in RISK_KEYWORDS)
    if is_catalyst and not is_risk:
        return "CATALYST"
    if is_risk and not is_catalyst:
        return "RISK"
    return ""


def fetch(ticker: str) -> list[dict]:
    url = f"https://finviz.com/quote.ashx?t={ticker.upper()}&ty=c&p=d&b=1"
    req = urllib.request.Request(url, headers=HEADERS)
    ctx = ssl.create_default_context(cafile=_SSL_CAFILE)
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
    with opener.open(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    # Extract only the news table section for speed
    news_start = html.find('id="news-table"')
    news_end = html.find("</table>", news_start)
    if news_start == -1:
        return []
    news_html = html[news_start:news_end]

    results = []
    last_date = "today"

    for row in re.split(r"<tr\b", news_html):
        src_m = SOURCE_RE.search(row)
        if not src_m:
            continue
        source = src_m.group(1).strip()

        date_m = DATE_RE.search(row)
        if date_m:
            date_raw = re.sub(r"\s+", " ", date_m.group(1)).strip()
            # Finviz format: "May-22-26 07:27PM" (new day) or "10:30AM" (same day)
            if re.search(r"[A-Z][a-z]+-\d{2}-\d{2}", date_raw):
                last_date = date_raw.split()[0]

        hl_m = HEADLINE_RE.search(row)
        if not hl_m:
            continue
        headline = re.sub(r"<[^>]+>", "", hl_m.group(1))
        headline = re.sub(r"\s+", " ", headline).strip()
        headline = headline.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'")
        if not headline:
            continue

        results.append({
            "date": last_date,
            "headline": headline,
            "source": source,
            "signal": classify(headline),
        })

    return results[:40]


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_news.py TICKER", file=sys.stderr)
        sys.exit(1)

    ticker = sys.argv[1].upper()
    try:
        items = fetch(ticker)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not items:
        print(f"No news found for {ticker}.")
        sys.exit(0)

    print(f"\n=== Recent News: {ticker} ===\n")
    for i, item in enumerate(items, 1):
        tag = f"[{item['signal']}]" if item["signal"] else ""
        print(f"{i:2}. {item['date']:<14} {tag:<12} {item['headline']}")

    catalysts = [x for x in items if x["signal"] == "CATALYST"]
    risks = [x for x in items if x["signal"] == "RISK"]

    print(f"\n--- Summary ---")
    print(f"Catalysts: {len(catalysts)}  |  Risks: {len(risks)}  |  Neutral: {len(items) - len(catalysts) - len(risks)}")

    if catalysts:
        print("\nTop catalysts:")
        for x in catalysts[:5]:
            print(f"  + {x['date']}: {x['headline']}")

    if risks:
        print("\nTop risks:")
        for x in risks[:5]:
            print(f"  - {x['date']}: {x['headline']}")


if __name__ == "__main__":
    main()
