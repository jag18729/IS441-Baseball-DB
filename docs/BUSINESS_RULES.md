# Business Rules - IS441 Baseball Database

**Project:** Moneyball MLB Scouting Database
**Team:** Rafael Garcia, Josh Schmeltzer, Brandon Helmuth
**Last Updated:** November 10, 2025

---

## Overview

This document details all 30 business rules governing the IS441 Baseball Database. These rules ensure data integrity, enforce proper relationships, and support the Moneyball approach to player scouting.

---

## Table of Contents

1. [League Structure Rules (BR-1 to BR-3)](#league-structure-rules)
2. [Team Rules (BR-4 to BR-7)](#team-rules)
3. [Player Rules (BR-8 to BR-13)](#player-rules)
4. [Position Rules (BR-14 to BR-16)](#position-rules)
5. [Game Rules (BR-17 to BR-22)](#game-rules)
6. [Game Statistics Rules (BR-23 to BR-26)](#game-statistics-rules)
7. [Data Integrity Rules (BR-27 to BR-30)](#data-integrity-rules)

---

## League Structure Rules

### BR-1: Conference Division Structure
**Rule:** Each conference (AL or NL) must have exactly 3 divisions (East, Central, West)

**Supporting Logic:**
- MLB organizational structure mandates balanced competition
- Each league has 15 teams divided evenly across 3 divisions (5 teams each)
- Maintains scheduling fairness and playoff seeding consistency

**Database Impact:**
- Enforces 1:M relationship between Conference and Division tables
- Division_ID as foreign key in Division table

**Cardinality:** Conference (1) → Division (3)

---

### BR-2: Division Conference Assignment
**Rule:** Each division must belong to exactly one conference

**Supporting Logic:**
- A division cannot exist in both AL and NL simultaneously
- Divisions are uniquely named within their conference context
- Prevents ambiguity in team assignments

**Database Impact:**
- Conference_ID is NOT NULL in Division table
- Foreign key constraint enforces referential integrity

**Cardinality:** Division (M) → Conference (1)

---

### BR-3: Exactly Two Conferences
**Rule:** There are exactly 2 conferences in MLB (American League, National League)

**Supporting Logic:**
- MLB has a fixed organizational structure
- Historical structure since 1901 (with some reorganizations)
- All teams must belong to one of these two leagues

**Database Impact:**
- Conference table will have exactly 2 records
- Static data, not user-generated
- Referenced by all team/division queries

**Data Integrity:** Check constraint or application logic to prevent insertion of third conference

---

## Team Rules

### BR-4: Team Division Assignment
**Rule:** Each team must be assigned to exactly one division

**Supporting Logic:**
- Teams compete within their division throughout the season
- Division assignment determines schedule and playoff eligibility
- Cannot belong to multiple divisions simultaneously

**Database Impact:**
- Division_ID is NOT NULL foreign key in Team table
- Cascade updates if division structure changes

**Cardinality:** Team (M) → Division (1)

---

### BR-5: Unique Team Abbreviation
**Rule:** A team must have a unique abbreviation (e.g., NYY, BOS, LAD)

**Supporting Logic:**
- Abbreviations used in scorekeeping, broadcasts, and graphics
- Must be globally unique to avoid confusion
- Standard 2-3 character codes recognized across MLB

**Database Impact:**
- UNIQUE constraint on Team_Abbreviation column
- Prevents duplicate abbreviations during data entry

**Validation:** Check on INSERT/UPDATE operations

---

### BR-6: Team Requires Location and Name
**Rule:** Each team must have a location and name

**Supporting Logic:**
- Teams identified by city/region (location) and nickname (name)
- Example: "New York" (location) + "Yankees" (name)
- Both fields necessary for complete team identification

**Database Impact:**
- Team_Name: VARCHAR(100) NOT NULL
- Team_Location: VARCHAR(100) NOT NULL
- No NULL values allowed in either field

**Data Quality:** Ensures complete team records

---

### BR-7: Exactly 30 MLB Teams
**Rule:** There are exactly 30 MLB teams

**Supporting Logic:**
- Current MLB structure has 30 franchises
- 15 teams per league (AL/NL)
- Fixed organizational size (expansions are rare)

**Database Impact:**
- Team table will have 30 records after full import
- Can validate data completeness by COUNT(*)

**Application Logic:** Alert if team count ≠ 30 after import

---

## Player Rules

### BR-8: Player Team Assignment
**Rule:** Each player must be assigned to exactly one team at any given time

**Supporting Logic:**
- Players under contract with one MLB team
- Roster assignments are mutually exclusive
- Trade/transfers update team assignment

**Database Impact:**
- Team_ID is NOT NULL foreign key in Player table
- Represents current roster (2024 season)

**Limitation:** Historical team changes not tracked in this schema

**Cardinality:** Player (M) → Team (1)

---

### BR-9: Player Primary Position
**Rule:** Each player must have exactly one primary position

**Supporting Logic:**
- Players categorized by primary role (even if multi-position capable)
- Scouting reports focus on primary position performance
- Simplifies roster composition analysis

**Database Impact:**
- Position_ID is NOT NULL foreign key in Player table
- References Position lookup table

**Note:** Multi-position players assigned their most common position

**Cardinality:** Player (M) → Position (1)

---

### BR-10: Player Name Requirements
**Rule:** A player must have a first name and last name

**Supporting Logic:**
- Legal identification requirement
- Roster listings require formal names
- Query and reporting purposes

**Database Impact:**
- First_Name: VARCHAR(50) NOT NULL
- Last_Name: VARCHAR(50) NOT NULL
- Full_Name generated from both fields

**Data Quality:** No anonymous or incomplete player records

---

### BR-11: Unique Jersey Numbers Per Team
**Rule:** Jersey numbers must be unique within a team

**Supporting Logic:**
- MLB rule: No two players on same team can wear same number
- Essential for player identification during games
- Historical significance (retired numbers)

**Database Impact:**
- UNIQUE constraint on (Team_ID, Jersey_Number)
- Allows same number across different teams

**Special Cases:** NULL allowed (unsigned players, pending assignment)

---

### BR-12: Player Active Status
**Rule:** Players must have either "active" or "inactive" status

**Supporting Logic:**
- Distinguishes current roster (active) from historical/retired players
- API provides active flag for current season
- Supports queries focused on available talent

**Database Impact:**
- Active_Status: BOOLEAN NOT NULL
- TRUE = Active (current roster)
- FALSE = Inactive (retired, free agent, minors)

**Moneyball Application:** Filter to active players for scouting queries

---

### BR-13: Bats/Throws Recording
**Rule:** A player's bats/throws must be recorded (Left/Right/Both)

**Supporting Logic:**
- Critical scouting metric for matchup analysis
- Affects platoon advantages and lineup construction
- Standard MLB statistical tracking

**Database Impact:**
- Bats_Throws: VARCHAR(20) NULL
- Format: "R/R" (bats right, throws right), "L/R", "S/R" (switch)

**Data Quality:** Derived from API, nullable for incomplete records

---

## Position Rules

### BR-14: Unique Position Names
**Rule:** Each position must have a unique name

**Supporting Logic:**
- Positions are standardized MLB roles
- Names must be distinct for clarity
- Example: "Starting Pitcher" ≠ "Relief Pitcher"

**Database Impact:**
- UNIQUE constraint on Position_Name column
- Prevents duplicate position definitions

**Data Integrity:** Enforced at database level

---

### BR-15: Position Type Classification
**Rule:** Positions are categorized as either "Pitcher" or "Fielder"

**Supporting Logic:**
- Fundamental baseball distinction
- Pitchers vs. position players (offensive/defensive roles)
- Affects roster composition rules (25-man roster limits)

**Database Impact:**
- Position_Type: VARCHAR(20) NOT NULL
- CHECK constraint: Position_Type IN ('Pitcher', 'Fielder')

**Query Application:** Analyze pitcher/fielder distribution per team

---

### BR-16: Position Can Have Zero or More Players
**Rule:** A position can have zero or more players

**Supporting Logic:**
- Some positions may be unfilled on certain teams
- Multiple players can share same position (depth chart)
- Example: Team may have 5 starting pitchers

**Database Impact:**
- No NOT NULL constraint from Position to Player
- Optional relationship (0:M)

**Cardinality:** Position (1) → Player (0..M)

---

## Game Rules

### BR-17: Game Requires Home and Away Teams
**Rule:** Each game must have exactly one home team and one away team

**Supporting Logic:**
- Baseball games always involve two teams
- Home team has venue advantage
- Scheduling and statistics require both teams

**Database Impact:**
- Home_Team_ID: INT NOT NULL (FK → Team)
- Away_Team_ID: INT NOT NULL (FK → Team)
- Both fields required for valid game record

**Cardinality:** Game (M) → Team (1) [two relationships]

---

### BR-18: Home Team ≠ Away Team
**Rule:** The home team and away team in a game must be different

**Supporting Logic:**
- Prevents data entry errors
- Logically impossible for team to play itself
- Ensures valid matchup records

**Database Impact:**
- CHECK constraint: Home_Team_ID ≠ Away_Team_ID
- Enforced at database or application level

**Validation:** Reject game records where both teams are identical

---

### BR-19: Game Date Required
**Rule:** Each game must have a date

**Supporting Logic:**
- Games scheduled on specific dates
- Essential for season tracking and historical analysis
- Used in season wins/losses calculations

**Database Impact:**
- Game_Date: DATETIME NOT NULL
- Includes date and time of first pitch

**Query Application:** Filter games by date range, season, month

---

### BR-20: Game Season Assignment
**Rule:** Each game must be assigned to a specific season (year)

**Supporting Logic:**
- MLB seasons span calendar years (April-October)
- Season used for statistics aggregation
- Supports historical data analysis (2002-2024)

**Database Impact:**
- Season: INT NOT NULL
- Format: YYYY (e.g., 2024)

**Data Quality:** Derived from Game_Date, must match

---

### BR-21: Game Type Flag
**Rule:** A game is marked as either regular season or postseason

**Supporting Logic:**
- Postseason games (playoffs) separate from regular season
- Different statistical treatment and importance
- Affects team seeding and championship path

**Database Impact:**
- Postseason_Flag: BOOLEAN NOT NULL
- TRUE = Postseason, FALSE = Regular Season

**Query Application:** Filter to regular season only for Moneyball analysis

---

### BR-22: Game Venue Required
**Rule:** Each game must have a venue (stadium name)

**Supporting Logic:**
- Games played at specific ballparks
- Venue affects performance (altitude, dimensions, weather)
- Home team plays at their home venue

**Database Impact:**
- Venue: VARCHAR(100) NULL
- Contains stadium name (e.g., "Yankee Stadium")

**Data Quality:** Nullable for records with missing venue data

---

## Game Statistics Rules

### BR-23: Two Statistics Records Per Game
**Rule:** Each game must have exactly 2 statistics records (one for home, one for away)

**Supporting Logic:**
- Both teams generate statistics in every game
- Home and away stats stored separately for analysis
- Enables per-team performance queries

**Database Impact:**
- Game_Statistics has two records per Game_ID
- Is_Home_Team field distinguishes records

**Data Integrity:** COUNT(*) GROUP BY Game_ID should always = 2

---

### BR-24: Required Statistics Fields
**Rule:** Game statistics must record hits, runs, and errors

**Supporting Logic:**
- Fundamental baseball box score metrics
- Hits = offensive production
- Runs = scoring (win/loss determination)
- Errors = defensive quality

**Database Impact:**
- Runs: INT NOT NULL
- Hits: INT NOT NULL
- Errors: INT NOT NULL

**Moneyball Application:** Core metrics for undervaluation analysis

---

### BR-25: Non-Negative Statistics Values
**Rule:** Hits, runs, and errors must be non-negative integers

**Supporting Logic:**
- Cannot have negative hits, runs, or errors
- Zero is valid (e.g., shutout = 0 runs, no-hitter = 0 hits)
- Ensures logical data values

**Database Impact:**
- CHECK constraints: Runs >= 0, Hits >= 0, Errors >= 0
- Rejects invalid negative values

**Data Validation:** Enforced at database level

---

### BR-26: Statistics Team Match
**Rule:** The team in game statistics must match either the home or away team of the game

**Supporting Logic:**
- Statistics belong to one of the two teams playing
- Cannot assign statistics to team not in game
- Referential integrity requirement

**Database Impact:**
- Team_ID in Game_Statistics must equal Home_Team_ID or Away_Team_ID
- Complex CHECK constraint or application validation

**Validation:** JOIN verification query during import

---

## Data Integrity Rules

### BR-27: Foreign Key Enforcement
**Rule:** All foreign key relationships must reference existing records

**Supporting Logic:**
- Prevents orphaned records (e.g., player with invalid team)
- Maintains referential integrity across tables
- Ensures data consistency

**Database Impact:**
- All FK columns defined with REFERENCES constraint
- ON DELETE RESTRICT to prevent cascading deletes
- ON UPDATE CASCADE to maintain consistency

**Enforcement:** Database-level constraint checking

---

### BR-28: Historical Player Data Protection
**Rule:** Player records cannot be deleted if they are referenced in historical data

**Supporting Logic:**
- Historical game statistics reference players
- Deleting players breaks historical accuracy
- Moneyball analysis requires complete historical context

**Database Impact:**
- Foreign key constraints prevent deletion
- Alternative: Use Active_Status = FALSE instead of DELETE

**Data Management:** Deactivate rather than delete

---

### BR-29: Team Data Protection
**Rule:** Team records cannot be deleted if they have associated players or games

**Supporting Logic:**
- Teams referenced by players, games, statistics
- Deletion would orphan dependent records
- Teams rarely cease to exist (franchise relocation, not deletion)

**Database Impact:**
- RESTRICT constraint on Team table
- Must remove dependent records before team deletion

**Application Logic:** Warn user of dependent records

---

### BR-30: Game Statistics Protection
**Rule:** Game records cannot be deleted if they have associated statistics

**Supporting Logic:**
- Game_Statistics depends on Game table
- Deleting games loses statistical history
- Historical data preservation for analysis

**Database Impact:**
- Foreign key constraint prevents game deletion
- Must delete statistics first (or use CASCADE)

**Recommendation:** Archive old games rather than delete

---

## Business Rules Summary Table

| Category | Rules | Primary Focus |
|----------|-------|---------------|
| League Structure | BR-1 to BR-3 | Conference and division organization |
| Team | BR-4 to BR-7 | Team assignments and uniqueness |
| Player | BR-8 to BR-13 | Roster management and player attributes |
| Position | BR-14 to BR-16 | Position definitions and classifications |
| Game | BR-17 to BR-22 | Game scheduling and matchups |
| Game Statistics | BR-23 to BR-26 | Statistical data recording |
| Data Integrity | BR-27 to BR-30 | Referential integrity and data protection |

**Total Business Rules:** 30

---

## ERD Application

These business rules are enforced through:

1. **Primary Keys** - Ensure uniqueness (BR-5, BR-14)
2. **Foreign Keys** - Enforce relationships (BR-2, BR-4, BR-8, BR-9, BR-17, BR-23, BR-26, BR-27)
3. **NOT NULL Constraints** - Require data (BR-6, BR-10, BR-19, BR-20, BR-24)
4. **UNIQUE Constraints** - Prevent duplicates (BR-5, BR-11, BR-14)
5. **CHECK Constraints** - Validate data ranges (BR-15, BR-18, BR-25)
6. **Application Logic** - Complex validations (BR-3, BR-7, BR-23, BR-26)

---

## Moneyball Implications

These business rules support the Moneyball philosophy by:

- **Data Quality** (BR-24, BR-25): Ensures accurate statistics for analysis
- **Active Player Focus** (BR-12): Filters to current market opportunities
- **Team Performance Tracking** (BR-23): Enables win/loss correlation
- **Historical Preservation** (BR-28, BR-29, BR-30): Maintains trend analysis capability
- **Position Analysis** (BR-9, BR-15): Identifies roster gaps and market inefficiencies

---

**Document Status:** Complete
**Related Documents:**
- [Phase1_Database_Design.md](../Phase1_Database_Design.md)
- [ERD_Diagram.md](../ERD_Diagram.md)
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md)

---

**Last Reviewed:** November 10, 2025
**Next Review:** Phase 5 (Final Report Assembly)
