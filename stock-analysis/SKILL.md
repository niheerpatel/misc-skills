---
name: stock-analysis
description: "Analyze a single stock against IBD Leaderboard criteria (CAN SLIM). Fetches live Finviz data and recent news, accepts IBD ratings from the user, then produces a scored checklist and a buy/hold/sell decision with specific entry, stop-loss, and profit target."
argument-hint: "Ticker symbol (e.g. NVDA)"
---

# IBD Stock Analysis

Evaluate a stock against IBD Leaderboard standards using live Finviz data, recent news, and IBD ratings supplied by the user. Output is a CAN SLIM scorecard, chart pattern assessment, and a clear trade decision with price levels.

## When to Use

- Before entering a new position — confirm the stock meets Leaderboard-quality criteria
- During a market uptrend when reviewing your watchlist for actionable setups
- To stress-test a conviction trade against IBD's evidence-based framework
- When exiting a position and you want a structured hold/sell assessment

## Procedure

### Step 1: Market Context

Ask the user: **"What is the current IBD Market Pulse?"**

Accepted values: `Confirmed Uptrend` | `Uptrend Under Pressure` | `Rally Attempt` | `Market in Correction`

- **Confirmed Uptrend** → proceed with full analysis; new buys are valid
- **Uptrend Under Pressure** → proceed with caution; tighten stop-losses, reduce position size
- **Rally Attempt** → analysis only; no new buys until a follow-through day is confirmed
- **Market in Correction** → stop here. No new buys. If user is already in a position, go to Step 7 (sell rules only).

### Step 2: IBD Ratings Input

Prompt the user to open IBD Stock Checkup at:
`https://research.investors.com/stock-checkup/nasdaq-[TICKER].aspx`

Ask them to provide:

| Rating | Target Threshold | User Input |
|--------|-----------------|------------|
| Composite Rating | ≥ 90 | |
| EPS Rating | ≥ 80 | |
| RS (Relative Strength) Rating | ≥ 80 | |
| SMR Rating | A or B | |
| Accumulation/Distribution Rating | A, B, or C | |
| On IBD Leaderboard? | Yes / No | |
| On IBD 50? | Yes / No | |

Also ask: **"Is the RS Line at or near a 52-week high?"** (visible on IBD charts — look for the RS Line in blue breaking to new highs ahead of or with price.)

### Step 3: Fetch Finviz Data

Run:
```
python stock-analysis/scripts/fetch_finviz.py [TICKER]
```

This returns structured data including:
- Current price, 52-week high/low, % below 52-week high
- 50-day and 200-day moving averages
- Current volume vs. 50-day average volume (relative volume)
- P/E ratio, EPS (ttm), EPS growth Q/Q, Sales growth Q/Q, ROE, Debt/Equity
- Institutional ownership %

If the script fails, manually pull data from `https://finviz.com/quote.ashx?t=[TICKER]`.

### Step 4: Fetch Recent News

Run:
```
python stock-analysis/scripts/fetch_news.py [TICKER]
```

Review the last 30 days of headlines. Flag any of the following as a **catalyst** (supports the N in CAN SLIM):
- Earnings beat (especially acceleration — growth rate higher than prior quarter)
- New product launch or major partnership
- Analyst upgrade or price target raise
- Insider buying
- Industry tailwind (regulatory approval, sector rotation)

Flag the following as **risks**:
- Earnings miss or guidance cut
- Analyst downgrade
- Insider selling (especially large blocks)
- Regulatory or legal headwinds
- Sector rotation away from the stock's industry

### Step 5: CAN SLIM Scorecard

Score each criterion as **Pass**, **Partial**, or **Fail** using the data collected in Steps 2–4. Add a one-line note for each.

| # | Criterion | What to Check | Score | Note |
|---|-----------|--------------|-------|------|
| C | Current Quarterly Earnings | EPS growth Q/Q ≥ 25%; EPS Rating ≥ 80 | | |
| A | Annual Earnings Growth | 3-year EPS CAGR ≥ 25%; ROE ≥ 17%; Debt/Eq manageable | | |
| N | New Catalyst | New product, new high, recent positive news catalyst | | |
| S | Supply & Demand | High relative volume on up days; dry volume in base; price holding MAs | | |
| L | Leader in its Group | RS Rating ≥ 80; RS Line at 52-wk high; top 1-2 in sector | | |
| I | Institutional Sponsorship | Acc/Dist A–C; increasing inst. ownership; quality fund holders | | |
| M | Market Direction | IBD Market Pulse (from Step 1) | | |

**Scoring summary**: Count Passes. 7/7 = highest conviction; 5-6/7 = actionable with normal risk; < 5/7 = wait or pass.

### Step 6: Chart Pattern and Buy Point

Using price, 52-week range, and moving average data from Step 3, identify:

**Base type:**
- **Cup with Handle** — U-shaped base 7–65 weeks; handle forms in upper half of base; buy point = handle high + $0.10
- **Double Bottom** — Two lows of roughly equal depth forming a W; buy point = middle peak + $0.10
- **Flat Base** — Tight sideways consolidation ≥ 5 weeks, corrects < 15%; buy point = prior high + $0.10
- **Ascending Base** — Three higher pullbacks each correcting 10–20%; buy point = third pullback high + $0.10
- **No base / extended** — Price > 5% above any identifiable buy point; do not chase

**Assess the entry:**
- Is the stock within **5% of its buy point**? → Actionable
- Is the stock **5–10% above buy point**? → Risky; note it as extended
- Is the stock **> 10% above buy point**? → Do not buy; add to watchlist for next base

**Risk gauge:**
- Distance from current price to 50-day MA (how far can it fall before breaking support?)
- Is the stock finding support at its 10-week MA on pullbacks? (constructive)
- Has the stock undercut its 50-day MA on high volume? (bearish)

### Step 7: Trade Decision

Based on Steps 1–6:

| Decision | Conditions |
|----------|-----------|
| **BUY** | Market in uptrend; CAN SLIM ≥ 5 Pass; within 5% of buy point; volume confirming |
| **WATCH** | Strong setup but extended > 5%, or market in rally attempt awaiting follow-through |
| **HOLD** | Already in position; stock holding above 50-day MA; no sell signals triggered |
| **SELL — Defensive** | Price drops 7–8% below your buy point (hard stop, no exceptions) |
| **SELL — Offensive** | Price up 20–25% from buy point (lock in gains before a potential pullback) |
| **SELL — Late signal** | Breaks 50-day MA on volume; climax run (3 wide-spread weeks up on heaviest volume of base) |

**Output price levels** (always include all three):
- **Entry**: buy point price (or current price if already in position)
- **Stop-loss**: entry price × 0.92 (8% below entry)
- **Profit target**: entry price × 1.20 to 1.25 (20–25% gain)

## Output Format

```
# Stock Analysis: [TICKER] — [Date]

## Market Context
IBD Market Pulse: [status]

## IBD Ratings
| Rating | Value | Pass? |
|--------|-------|-------|
| Composite | | |
| EPS | | |
| RS | | |
| SMR | | |
| Acc/Dist | | |
| Leaderboard | | |

## Finviz Snapshot
[Key metrics from fetch_finviz.py output]

## News & Catalysts
[Bulleted list of notable headlines with dates]

## CAN SLIM Scorecard
[Table from Step 5 — filled in]
**Total: X/7 Pass**

## Chart Pattern
Base type: [type]
Buy point: $[price]
Current price: $[price] ([X]% [above/below] buy point)
Status: [Actionable / Extended / No clear base]

## Trade Decision
**[BUY / WATCH / HOLD / SELL]**

Entry: $[price]
Stop-loss: $[price] ([X]% below entry)
20% target: $[price]
25% target: $[price]

Rationale: [2–3 sentences: what makes this compelling or why to wait]

## Key Risks
[Bulleted list of 2–3 risks to monitor]
```
