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

---

### 3️⃣ Analysis & Prediction Engine
Transforms historical inputs into daily predictions.

#### Stage 1 — Baseline Statistical Model (Weeks 1 – 4)
- Rolling averages (5/10/15 games)  
- Season splits (home/away, opponent)  
- Pace & rest adjustments  

```python
PredictedPoints = BaseAvg × PaceAdj × RestAdj × HomeAwayAdj × OppDefAdj
