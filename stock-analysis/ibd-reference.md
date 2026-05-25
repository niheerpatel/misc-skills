# IBD Reference: Ratings, CAN SLIM, Patterns, and Sell Rules

Quick reference for the IBD Leaderboard framework used in the `stock-analysis` skill.

---

## IBD Composite Ratings

### Composite Rating
Combines EPS Rating, RS Rating, SMR Rating, Acc/Dist Rating, and other proprietary factors into a single 1–99 score.
- **99** = top 1% of all stocks
- **≥ 90** = Leaderboard-quality threshold
- **< 80** = avoid for new buys

### EPS Rating
Measures earnings growth vs. all other stocks over the last 2–5 years, weighted toward recent quarters.
- **≥ 80** = strong; top 20% of all stocks
- Ideal: acceleration (latest quarter growth > prior quarter growth)
- Watch for: EPS estimates rising; analyst consensus upgrades

### RS (Relative Strength) Rating
Measures price performance vs. all other stocks over the last 52 weeks (with heavier weighting on recent 3 months).
- **≥ 80** = outperforming 80% of all stocks
- **RS Line** = stock price ÷ S&P 500; a rising RS line means the stock is beating the market
- Best setups: RS Line at or making new highs *before* price breaks out (early signal)

### SMR Rating (Sales + Margins + Return on Equity)
Composite of revenue growth, pre-tax margin, and ROE. Graded A–E.
- **A** = top 20% — strong growth, high margins, excellent returns
- **B** = above average
- **C** = average; acceptable if other ratings are very strong
- **D or E** = weak; avoid

### Accumulation/Distribution Rating
Measures institutional buying vs. selling over the last 13 weeks. Graded A–E.
- **A** = heavy institutional buying
- **B** = moderate buying
- **C** = neutral (buying and selling in balance)
- **D** = moderate selling
- **E** = heavy institutional selling; avoid

---

## CAN SLIM Criteria

| Letter | Criterion | Key Thresholds |
|--------|-----------|---------------|
| **C** | Current Quarterly EPS | Growth ≥ 25% vs. same quarter prior year; acceleration preferred |
| **A** | Annual EPS Growth | ≥ 25% per year for last 3 years; ROE ≥ 17%; debt manageable |
| **N** | New (product, high, management) | New product/service with large addressable market; stock at or near 52-wk high |
| **S** | Supply & Demand | Float matters: smaller float = more volatile moves; volume surge on breakout (≥ 40% above average); dry low-volume pullbacks in base |
| **L** | Leader in its Sector | RS Rating ≥ 80; RS Line at highs; #1 or #2 stock in its industry group |
| **I** | Institutional Sponsorship | Increasing number and quality of fund holders (Fidelity, T. Rowe, etc.); Acc/Dist A–C |
| **M** | Market Direction | Follow the market — buy only in confirmed uptrends; sit in cash during corrections |

---

## Base Patterns

### Cup with Handle
- **Shape**: U-shaped decline followed by a short drift-down handle
- **Duration**: 7–65 weeks total; handle ≥ 1 week
- **Depth**: Cup corrects 15–35% (deeper in bear markets); handle corrects < 15% and stays in upper half of the cup
- **Buy point**: Highest price in the handle + $0.10
- **Volume on breakout**: Should be ≥ 40–50% above average

### Double Bottom
- **Shape**: Two lows of roughly equal price forming a W
- **Duration**: ≥ 7 weeks
- **Depth**: Each low corrects 15–35%; second low can undercut first slightly (shakeout)
- **Buy point**: Middle peak of the W + $0.10
- **Volume**: Heavy on second bounce off the low is bullish

### Flat Base
- **Shape**: Tight, sideways consolidation
- **Duration**: ≥ 5 weeks
- **Depth**: Corrects < 15% from high to low
- **Buy point**: Prior high + $0.10
- **Volume**: Low volume throughout the base (institutions not selling); high volume on breakout

### Ascending Base
- **Shape**: Three pullbacks, each pulling back 10–20%, each low higher than the last
- **Duration**: 9–16 weeks
- **Context**: Often forms during a choppy market
- **Buy point**: Highest price before the third pullback + $0.10

### High Tight Flag
- **Shape**: Stock doubles or nearly doubles in 4–8 weeks, then pulls back 10–25% in 3–5 weeks
- **Rarity**: Very rare; usually marks leading stocks in strong bull markets
- **Buy point**: Top of the flag + $0.10
- **Risk**: Volatile; use half position size

---

## Sell Rules

### Defensive Sells (Limit Losses)
- **7–8% loss rule**: Sell immediately if price falls 7–8% below your buy point. No exceptions.
- **Base failure**: If stock breaks out, pulls back into the base and closes below the buy point on high volume → sell
- **Breaks 50-day MA on heavy volume**: Institutional selling; exit if it can't recover in 1–2 days

### Offensive Sells (Lock in Gains)
- **20–25% profit target**: Take profits when up 20–25% from the buy point (most gains come in this range before a pullback or consolidation)
- **Exception — 3-weeks-tight rule**: If a stock rises 20% in 1–3 weeks from breakout, hold for at least 8 weeks — it may be a big winner
- **Climax run**: 3+ weeks up in a row with widening price spreads on the heaviest weekly volume of the run → sell into strength

### Late-Stage Failure Signals
- Stock forms a 4th or 5th base (late-stage bases have higher failure rates)
- RS Line makes a new low while price is still near highs (distribution)
- Reversal: stock breaks out to a new high, then closes down on the highest volume in weeks
- Gap down on earnings on heavy volume → sell immediately

---

## Position Sizing Notes

- **Standard**: Never risk more than 1–2% of portfolio on any single trade (position size × stop distance ≤ 1–2% of portfolio)
- **Uptrend**: Full position at breakout if all signals align
- **Uptrend Under Pressure**: Half position; give less room for error
- **Rally Attempt**: No new positions until a follow-through day (FTD) confirms the uptrend (market index up ≥ 1.25% on higher volume than prior day, on day 4 or later of the rally attempt)
