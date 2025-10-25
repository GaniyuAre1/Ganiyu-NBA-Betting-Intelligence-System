# 🏀 Ganiyu’s NBA Betting Intelligence System

## 📘 Overview
An automated Python system that analyzes NBA player props, spreads, and moneylines to uncover **positive expected-value (+EV)** betting opportunities by comparing model probabilities against sportsbook lines.

---

## 🧱 System Architecture

### 1️⃣ Data Collection Module
**Purpose:** Automatically gathers every dataset used by the pipeline.

**Sub-components**
- **Player Stats Scraper** – game logs, season stats, advanced metrics  
- **Team Stats Scraper** – pace, ratings, recent form  
- **Injury Report Scraper** – daily player updates  
- **Odds Scraper** – current sportsbook lines  
- **Historical Data Importer** – one-time import of past-season data  

**Data Sources**
- NBA Stats API (official, reliable)  
- Basketball-Reference (historical backup)  
- The Odds API (500 free requests / month)  
- ESPN (injury reports)  

**Design Decisions**
- Run scrapers daily before games  
- Store raw data → clean later (preserve source)  
- Include error handling for downtime  

---

### 2️⃣ Data Storage — SQLite
**Purpose:** Structured, queryable storage for all collected data.

**Why SQLite**
- Built into Python  
- Lightweight (single-file database)  
- Simple backup & easy upgrade path to PostgreSQL  

**Schema Overview**

| Table | Purpose |
|:--|:--|
| `players` | Player metadata |
| `games` | Schedules & results |
| `player_game_stats` | Box scores for each player/game |
| `team_stats` | Team ratings & pace |
| `injuries` | Daily player status |
| `betting_lines` | Sportsbook odds & props |
| `predictions` | Model forecasts |
| `bet_tracking` | Results & ROI tracking |


Summary
Data Sources:

✅ NBA Stats API (free, official stats)
✅ Basketball-Reference (free, backup/historical)
✅ The Odds API (free tier, betting lines)
✅ ESPN (free, injuries)

Collection Strategy:

One-time historical import (2-3 hours)
Daily automated updates (3 scripts, 5-10 minutes total)
All free or very cheap

---

### 3️⃣ Analysis & Prediction Engine
Transforms historical inputs into daily predictions.

#### Stage 1 — Baseline Statistical Model (Weeks 1 – 4)
- Rolling averages (5/10/15 games)  
- Season splits (home/away, opponent)  
- Pace & rest adjustments  


PredictedPoints = BaseAvg × PaceAdj × RestAdj × HomeAwayAdj × OppDefAdj

### Stage 2 — Machine Learning (Weeks 5–8)

- 50+ engineered features (usage, matchups, form)  
- Algorithms: Linear Regression → Random Forest → XGBoost  
- Cross-validation to avoid overfitting  

---

### Stage 3 — Advanced Model (Weeks 9–12)

- Lineup-based projections & minute forecasting  
- Line movement analysis  
- Correlation bets (between player props)  

**Design Notes**
- Version models (`v1.0`, `v1.1`, …)  
- Log which version made each prediction  
- A/B-test models for performance  

---

### 4️⃣ Odds Comparison Module

**Goal:** Identify +EV bets by comparing predictions to sportsbook lines.

**Workflow**
1. Pull daily sportsbook lines  
2. Convert odds → implied probability  
3. Compare to model probability  
4. Compute expected value (EV)  
5. Filter EV ≥ 5% (configurable)  
6. Rank by EV & confidence  

**Example Output**
LeBron James — Over 25.5 Points
Sportsbook: DraftKings @ −110 (52.4% implied)
Model: 62% probability
Edge: +9.6% EV
Kelly Bet Size: 3.2% bankroll
Confidence: HIGH


---

### 5️⃣ User Interface

| Option | Description |
| :-- | :-- |
| **CLI (Phase 1)** | Terminal output for fast iteration |
| **Web Dashboard (Phase 2)** | Browser UI with tables & charts |

**Planned Features**
- Today’s Top +EV Picks  
- Player Deep Dives  
- Model Performance (ROI & CLV)  
- Bet History Log  
- Line Movement Alerts  

---

## 🗓️ Development Roadmap

| Phase | Timeline | Focus | Deliverable |
| :-- | :-- | :-- | :-- |
| 1 | Weeks 1–2 | Environment setup & DB build | Populated DB |
| 2 | Weeks 3–4 | Rolling averages & baseline model | Accuracy baseline (v1.0) |
| 3 | Weeks 5–6 | Injury/odds scrapers + automation | Daily predictions |
| 4 | Weeks 7–10 | Feature engineering + ML training | v2.0 model |
| 5 | Weeks 11–14 | Bankroll tools + dashboard | Production-ready system |
| 6 | 15+ | Live updates + notifications | Full release |

---

## 💰 Risk Management & Bankroll

A strong model still needs disciplined bankroll control.  
Use **fractional Kelly (25–50%)** to limit volatility and protect capital.

---

## ⚙️ Tech Stack

| Category | Tools |
| :-- | :-- |
| Language | Python 3.9+ |
| Database | SQLite 3 |
| Data Processing | Pandas, NumPy |
| Web Scraping | Requests, BeautifulSoup4 |
| Machine Learning | Scikit-learn, XGBoost |
| Visualization | Matplotlib, Seaborn |
| Automation | Windows Task Scheduler |
| Dev Tools | VS Code, Git/GitHub, Pytest |

---

## 📈 Kelly Criterion Guide

**Formula**
Bet % of bankroll = Edge / Decimal Odds


**Example**
- Book: −110 → 52.4% implied → 1.91 decimal  
- Model: 62% → Edge = 9.6%  
- Bet = 0.096 / 1.91 ≈ **5%** of bankroll  

**Fractional Kelly**

| Kelly Fraction | Stake |
| :-- | :-- |
| 100% | 5% |
| 50% | 2.5% |
| 25% | 1.25% |

Most pros use 25–50% Kelly for smoother growth.

---

## 🧮 Worked Example

**Bankroll = $2,000**

| Player | Prop | Model | Book | Edge | Kelly % | ½ Kelly Bet |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| LeBron | Over 25.5 pts | 62% | 52.4% | 9.6% | 5.0% | $50 |
| Curry | Over 4.5 3PT | 58% | 50.0% | 8.0% | 4.2% | $42 |
| Giannis | Over 11.5 reb | 55% | 52.4% | 2.6% | 1.4% | $14 |

---

## 🚫 When Not to Bet

- Skip edges below **5%** — likely noise or model error.  
- Focus bankroll on highest-confidence opportunities.

---

## 🧠 Sample Output

---

## ✅ Key Takeaways

1. Kelly = math-based bet sizing for optimal growth  
2. Use fractional Kelly to reduce variance  
3. Bigger edge → bigger bet automatically  
4. Model tracking + bankroll discipline = profitability  
