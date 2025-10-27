"""
NBA Betting Intelligence System - Database Setup
This script creates the SQLite database and all necessary tables
"""

import sqlite3
from datetime import datetime

def create_database():
    """Create the SQLite database and all tables"""
    
    # Connect to database (creates file if it doesn't exist)
    conn = sqlite3.connect('nba_betting.db')
    cursor = conn.cursor()
    
    print("=" * 60)
    print("NBA BETTING INTELLIGENCE SYSTEM - DATABASE SETUP")
    print("=" * 60)
    print(f"Creating database at: {datetime.now()}")
    print()
    
    # Table 1: Players
    print("Creating table: players...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            team TEXT,
            position TEXT,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table 2: Games
    print("Creating table: games...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_date DATE NOT NULL,
            home_team TEXT NOT NULL,
            away_team TEXT NOT NULL,
            home_score INTEGER,
            away_score INTEGER,
            pace REAL,
            season TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table 3: Player Game Stats
    print("Creating table: player_game_stats...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            minutes_played REAL,
            points INTEGER,
            rebounds INTEGER,
            assists INTEGER,
            steals INTEGER,
            blocks INTEGER,
            turnovers INTEGER,
            field_goals_made INTEGER,
            field_goals_attempted INTEGER,
            three_pointers_made INTEGER,
            three_pointers_attempted INTEGER,
            free_throws_made INTEGER,
            free_throws_attempted INTEGER,
            plus_minus INTEGER,
            FOREIGN KEY (player_id) REFERENCES players(player_id),
            FOREIGN KEY (game_id) REFERENCES games(game_id)
        )
    ''')
    
    # Table 4: Team Stats
    print("Creating table: team_stats...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS team_stats (
            team_stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL,
            game_date DATE NOT NULL,
            offensive_rating REAL,
            defensive_rating REAL,
            pace REAL,
            wins INTEGER,
            losses INTEGER,
            season TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table 5: Injuries
    print("Creating table: injuries...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS injuries (
            injury_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            report_date DATE NOT NULL,
            status TEXT,
            injury_type TEXT,
            return_date DATE,
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        )
    ''')
    
    # Table 6: Betting Lines
    print("Creating table: betting_lines...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS betting_lines (
            line_id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            player_id INTEGER,
            sportsbook TEXT NOT NULL,
            line_timestamp TIMESTAMP NOT NULL,
            line_type TEXT NOT NULL,
            prop_type TEXT,
            line_value REAL NOT NULL,
            odds TEXT NOT NULL,
            over_under TEXT,
            FOREIGN KEY (game_id) REFERENCES games(game_id),
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        )
    ''')
    
    # Table 7: Predictions
    print("Creating table: predictions...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_date DATE NOT NULL,
            game_id INTEGER,
            player_id INTEGER,
            prediction_type TEXT NOT NULL,
            predicted_value REAL NOT NULL,
            confidence_score REAL,
            model_version TEXT,
            actual_value REAL,
            prediction_correct INTEGER,
            FOREIGN KEY (game_id) REFERENCES games(game_id),
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        )
    ''')
    
    # Table 8: Bet Tracking
    print("Creating table: bet_tracking...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bet_tracking (
            bet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_id INTEGER,
            bet_date DATE NOT NULL,
            bet_amount REAL NOT NULL,
            odds TEXT NOT NULL,
            bet_type TEXT NOT NULL,
            result TEXT,
            profit_loss REAL,
            actual_outcome TEXT,
            sportsbook TEXT,
            FOREIGN KEY (prediction_id) REFERENCES predictions(prediction_id)
        )
    ''')
    
    # Create indexes for faster queries
    print("Creating indexes for performance...")
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_player_name ON players(player_name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_game_date ON games(game_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_player_game ON player_game_stats(player_id, game_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_betting_lines_game ON betting_lines(game_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_predictions_date ON predictions(prediction_date)')
    
    # Commit changes
    conn.commit()
    
    print()
    print("=" * 60)
    print("✅ DATABASE CREATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Database file: nba_betting.db")
    print()
    print("Tables created:")
    print("  1. players - Store player information")
    print("  2. games - Store game results")
    print("  3. player_game_stats - Store detailed player performance")
    print("  4. team_stats - Store team metrics")
    print("  5. injuries - Track player injuries")
    print("  6. betting_lines - Store sportsbook odds")
    print("  7. predictions - Store our model predictions")
    print("  8. bet_tracking - Track actual bets and results")
    print()
    print("🎯 Next Step: Import historical data from 2024-25 season")
    print("=" * 60)
    
    # Close connection
    conn.close()

def verify_database():
    """Verify the database was created correctly"""
    try:
        conn = sqlite3.connect('nba_betting.db')
        cursor = conn.cursor()
        
        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("\n📊 Database Verification:")
        print(f"   Total tables: {len(tables)}")
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   - {table[0]}: {count} rows")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error verifying database: {e}")
        return False

if __name__ == "__main__":
    # Create the database
    create_database()
    
    # Verify it was created successfully
    verify_database()
    
    print("\n✅ Setup complete! You can now run data collection scripts.")