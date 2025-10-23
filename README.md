## System Overview -- Ganiyu's NBA Betting Intelligence System


# What are we building?
Core Purpose: An automated system that analyzes NBA player props, spreads, and moneylines to identify positive expected value (+EV) betting opportunities by comparing our statistical predictions against sportsbook lines.

System Architecture (breakdown of each component)

## 1. Data Collection Module 
(feeds data to below)

**What it does:** Automatically gathers all the data we need

**Sub-components:**
- **Player Stats Scraper** - Gets game logs, season stats, advanced metrics
- **Team Stats Scraper** - Pace, ratings, recent form
- **Injury Report Scraper** - Daily injury updates
- **Odds Scraper** - Current betting lines from sportsbooks
- **Historical Data Importer** - One-time import of last season's data

**Data Sources We'll Use:**
- NBA Stats API (official, free, reliable)
- Basketball-Reference (backup for historical data)
- The Odds API (betting lines - 500 free requests/month)
- ESPN (injury reports)

**Key Design Decision:**
- We'll run scrapers **daily at a scheduled time** (before games start)
- We'll store raw data first, clean it second (never lose original data)
- We'll implement error handling (what if a website is down?)


## 2. Data Storage (Database)

**What it does:** Stores all collected data in an organized, queryable format

**Why we need a database:**
- You'll accumulate thousands of games, hundreds of players, daily updates
- Need fast queries like "Show me LeBron's last 10 games against Western Conference teams"
- Want historical tracking of our predictions vs. actual results

**Database Choice: SQLite**
- Built into Python (no separate installation)
- Perfect for single-user applications
- Easy to back up (just one file)
- Can always upgrade to PostgreSQL later if needed

**Database Schema (Structure):**

We'll have these main tables:

**Table 1: players**
- player_id (unique identifier)
- player_name
- team
- position
- active (yes/no)

**Table 2: games**
- game_id
- date
- home_team
- away_team
- home_score
- away_score
- pace (possessions)

**Table 3: player_game_stats**
- stat_id
- player_id
- game_id
- minutes
- points
- rebounds
- assists
- steals
- blocks
- field_goals_made/attempted
- three_pointers_made/attempted
- free_throws_made/attempted
- turnovers
- fouls

**Table 4: team_stats**
- team_id
- date
- offensive_rating
- defensive_rating
- pace
- wins/losses

**Table 5: injuries**
- injury_id
- player_id
- date
- status (Out, Doubtful, Questionable, Probable)
- injury_type

**Table 6: betting_lines**
- line_id
- game_id
- sportsbook
- timestamp
- line_type (spread, moneyline, over/under, player_prop)
- player_id (if player prop)
- prop_type (points, rebounds, assists)
- line_value
- odds

**Table 7: predictions**
- prediction_id
- date
- player_id (or game_id for spreads/totals)
- prediction_type
- predicted_value
- confidence_score
- model_version

**Table 8: bet_tracking**
- bet_id
- prediction_id
- bet_amount
- odds
- result (win/loss/push)
- profit_loss
- actual_outcome


## 3. Analysis & Prediction Engine (generates predictions daily)

**What it does:** Takes historical data and generates predictions

This is the **brain** of our system. We'll build this in stages:

### **Stage 1: Simple Statistical Model (Weeks 1-4)**
- Rolling averages (last 5, 10, 15 games)
- Season averages
- Home/away splits
- Opponent adjustments

**Example Logic for Points Prediction:**
```
Base = Player's last 10 game average
Pace Adjustment = (Tonight's opponent pace / League average pace)
Rest Adjustment = (Back-to-back? -5% | 2+ days rest? +2%)
Home/Away = (Home: +2% | Away: -2%)
Opponent Defense = (Top 10 defense? -8% | Bottom 10? +8%)

Predicted Points = Base × Pace × Rest × Home × Opponent
```
### **Stage 2: Machine Learning Model (Weeks 5-8)**
- Train models on historical data
- Features: 50+ variables (recent form, matchups, usage rate, etc.)
- Algorithms: Linear Regression → Random Forest → XGBoost
- Cross-validation to prevent overfitting

### **Stage 3: Advanced Model (Weeks 9-12)**
- Lineup-based predictions (who's on court together)
- Minutes projection (if starter is out, bench player gets more)
- Line movement analysis (track how lines move = sharp money)
- Correlation bets (if Player A goes over, Player B likely goes under)

**Key Design Decision:**
- We'll version our models (v1.0, v1.1, etc.)
- Track which model version made which prediction
- A/B test different models against each other

---

## 4. Odds Comparison Module (identifies +EV bets for us to display on user interface)

**What it does:** Compares our predictions to sportsbook lines and calculates EV

**Process:**
1. Get today's betting lines from multiple sportsbooks
2. Convert odds to implied probability
3. Compare to our predicted probability
4. Calculate expected value
5. Filter for +EV bets above threshold (e.g., +5% edge minimum)
6. Rank by confidence/EV

**Example Output:**
```
TONIGHT'S +EV OPPORTUNITIES:

Player: LeBron James
Prop: Over 25.5 Points
Sportsbook: DraftKings @ -110 (52.4% implied)
Our Model: 62% probability
Edge: +9.6% EV
Kelly Bet Size: 3.2% of bankroll
Confidence: HIGH (based on 150+ similar games)

## 5. User Dashboard/Interface (puts everything in a readable, digestible format for everyone to use and work off of)

**Two Options:**

**Option A: Terminal/Command Line Interface (Simplest)**
- Run a Python script
- See output in terminal
- Good for learning, fast to build

**Option B: Web Dashboard (More Polished)**
- HTML interface you open in browser
- Tables, charts, filters
- Looks professional
- Takes longer to build

**My Recommendation:** Start with Option A, upgrade to B later

**Dashboard Features:**
- Today's Top Picks (sorted by EV)
- Player Deep Dives (click to see all stats, trends, reasoning)
- Model Performance Tracker (our win rate, ROI, CLV)
- Bet History Log
- Line Movement Alerts

## Development Roadmap (Detailed Timeline)

### **Phase 1: Foundation (Weeks 1-2)**
- Set up Python environment
- Build database schema
- Create first data scraper (player stats)
- Import last season's historical data
- Verify data quality

**Deliverable:** Database populated with 2023-24 season data

### **Phase 2: Basic Analytics (Weeks 3-4)**
- Build simple rolling average calculator
- Create basic prediction model (statistical only)
- Test predictions against historical outcomes
- Calculate baseline accuracy

**Deliverable:** Working v1.0 model with known accuracy rate

### **Phase 3: Automation (Weeks 5-6)**
- Build injury scraper
- Build odds scraper
- Create daily update script (run each morning)
- Add EV calculator
- Build simple terminal output

**Deliverable:** Daily automated predictions

### **Phase 4: Machine Learning (Weeks 7-10)**
- Feature engineering (create 50+ predictive variables)
- Train ML models
- Cross-validation and backtesting
- Compare ML vs. statistical model


**Deliverable:** v2.0 ML-powered model

### **Phase 5: Refinement (Weeks 11-14)**
- Add multiple sportsbook comparison
- Build bet tracking system
- Implement bankroll management (Kelly Criterion)
- Create performance dashboard
- Line movement tracking

**Deliverable:** Production-ready betting system

### **Phase 6: Advanced Features (Weeks 15+)**
- Lineup analysis
- Correlation identification
- Live in-game adjustments
- Mobile notifications
- Web dashboard

**Deliverable:** Professional-grade betting tool

---

## Risk Management & Bankroll Strategy

**Critical Component:** Even with a great model, poor bankroll management will bankrupt you.

========================================

Technology Stack Summary
Core Technologies:

Language: Python 3.9+
Database: SQLite3
Data Processing: Pandas, NumPy
Web Scraping: Requests, BeautifulSoup4
Machine Learning: Scikit-learn, XGBoost
Visualization: Matplotlib, Seaborn
Task Scheduling: Windows Task Scheduler (for automation)

Development Tools:

Code Editor: VS Code (free, excellent for Python)
Version Control: Git/GitHub (save your work, track changes)
Testing: Pytest (ensure code works correctly)

========================================

Explanation of the Kelly Criterion Theory for Bettors

Bet Size % = (Your Edge) / (Decimal Odds)
```

Let's use a real example:

### **Example: LeBron James Over 25.5 Points**

**Step 1: Find Your Edge**

The sportsbook offers **-110 odds** on Over 25.5 points.
- This means bet $110 to win $100
- Implied probability = 110/(110+100) = **52.4%**

Your model predicts LeBron goes over 25.5 points **62% of the time**.

**Your Edge = 62% - 52.4% = 9.6%** (or 0.096 as a decimal)

---

**Step 2: Convert American Odds to Decimal Odds**

American odds of **-110** = decimal odds of **1.91**

How? For negative odds: Decimal = 1 + (100/110) = 1.91

This means: For every $1 you bet, you get back $1.91 if you win (your $1 plus $0.91 profit)

---

**Step 3: Apply Kelly Formula**
```
Kelly Bet Size = Edge / Decimal Odds
Kelly Bet Size = 0.096 / 1.91
Kelly Bet Size = 0.0503 = 5.03%
```

**Translation:** Bet **5% of your total bankroll** on this bet.

If your bankroll is $1,000 → Bet $50

---

## Why This Works (The Math Behind It)

Kelly Criterion balances two things:
1. **Betting enough** to take advantage of your edge
2. **Betting conservatively enough** to survive losing streaks

If you bet Kelly size repeatedly on +EV bets, you'll:
- Maximize your long-term bankroll growth rate
- Have very low risk of going broke (theoretically zero if your edge calculations are perfect)

---

## The Problem with Full Kelly

**Full Kelly is aggressive.** Even with an edge, you'll experience volatility:

- 10 bets in a row could easily go 4-6 (40% win rate) even if your true edge is 60%
- With 5% bets, losing 6 in a row = -30% bankroll drawdown
- This feels brutal psychologically

---

## Fractional Kelly (Our Solution)

**Fractional Kelly = Bet a fraction of what Kelly suggests**

Most professional bettors use **25% to 50% Kelly**:
```
Using 50% Kelly (Half Kelly):
- Kelly says bet 5%
- You actually bet 2.5%

Using 25% Kelly (Quarter Kelly):
- Kelly says bet 5%
- You actually bet 1.25%
```

### **Why Use Fractional Kelly?**

**Advantages:**
1. **Reduces volatility** - Smaller bets = smaller swings
2. **Protects against model errors** - If your 62% prediction is actually 58%, you're not over-betting
3. **Psychological comfort** - Easier to stick with the system during losing streaks
4. **Accounts for uncertainty** - We're never 100% sure of our exact edge

**The Trade-off:**
- You grow your bankroll slower than full Kelly
- But you have much smoother growth with less risk

========================================

## Real World Example

Let's say you have **$2,000 bankroll** and find 3 bets tonight:

| Player | Prop | Our Model | Sportsbook | Edge | Kelly % | Half Kelly Bet |
|--------|------|-----------|------------|------|---------|----------------|
| LeBron | Over 25.5 pts | 62% | 52.4% (-110) | 9.6% | 5.0% | **$50** |
| Curry | Over 4.5 threes | 58% | 50.0% (-110) | 8.0% | 4.2% | **$42** |
| Giannis | Over 11.5 reb | 55% | 52.4% (-110) | 2.6% | 1.4% | **$14** |

Notice:
- **Bigger edge = bigger bet** (LeBron has most edge, gets biggest bet)
- **Small edge = tiny bet** (Giannis has small edge, gets smallest bet)
- **Total risk = $106** (only 5.3% of bankroll across all bets)

---

## When NOT to Bet (Even with Positive EV)

Many bettors set a **minimum edge threshold**:
```
If Edge < 5% → Skip the bet
```

Why? 
- Small edges might be model error, not real edge
- Transaction costs, variance not worth it for tiny edges
- Focus on your best opportunities

---

## How We'll Implement This in Our System

Our system will:

1. **Calculate your edge** for every prop
2. **Apply Kelly Criterion** (you choose: 25%, 50%, or 100% Kelly)
3. **Show recommended bet size** in dollars
4. **Filter out bets below your minimum edge threshold**
5. **Track results** to refine edge calculations over time

**Example Output:**
```
========================================
TONIGHT'S RECOMMENDED BETS
Bankroll: $2,000 | Kelly Setting: 50%
Min Edge Threshold: 5%
========================================

1. LeBron James - Over 25.5 Points
   Odds: -110 | Our Model: 62% | Edge: +9.6%
   → BET: $50 (2.5% of bankroll)
   Expected Value: +$4.80

2. Stephen Curry - Over 4.5 Threes
   Odds: -110 | Our Model: 58% | Edge: +8.0%
   → BET: $42 (2.1% of bankroll)
   Expected Value: +$3.36


Key Takeaways from our assessment of the Kelly Criterion

1. Kelly Criterion = Math-based bet sizing to maximize growth
2. Your Edge ÷ Decimal Odds = Kelly percentage
3. Use Fractional Kelly (25-50%) to reduce volatility
4. Bigger edge = bigger bet (automatically)

5. This protects your bankroll from ruin during losing streaks

