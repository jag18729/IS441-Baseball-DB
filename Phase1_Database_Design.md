# IS441 Baseball Database Project - Phase 1
## Database Design & Requirements

**Project Goal**: Create a scouting database using the Moneyball approach to identify undervalued MLB talent within budget constraints.

**Team Members**: [Add names here]
**Date**: November 8, 2025
**Data Source**: Ball Don't Lie MLB API (https://mlb.balldontlie.io/)

---

## Executive Summary

This database system will enable MLB scouts and team management to:
- Track player performance across teams and games
- Analyze game statistics to identify undervalued talent
- Monitor team performance and league standings
- Make data-driven acquisition decisions based on real performance metrics

**Moneyball Approach**: Focus on objective statistical analysis rather than subjective scouting opinions to find players whose market value is below their actual contribution to wins.

---

## Available Data from API (Free Tier)

### ✅ Available Endpoints:
1. **Teams** - All 30 MLB teams with league/division info
2. **Players** - Player rosters with biographical data, positions
3. **Games** - Game results with team statistics (hits, runs, errors)

### ❌ Unavailable (Requires Premium):
- Individual player season statistics (batting avg, ERA, etc.)
- Advanced analytics endpoints

### Data Coverage:
- Historical: 2002 - Present
- Current project focus: **2024 season data**

---

## Database Design: 7-Table Schema

### Proposed Tables:

#### 1. **Conference** (League)
- Conference_ID (PK)
- Conference_Name (AL, NL)
- Description

#### 2. **Division**
- Division_ID (PK)
- Division_Name (East, Central, West)
- Conference_ID (FK)

#### 3. **Team**
- Team_ID (PK) - API: id
- Team_Name - API: name
- Team_Location - API: location
- Team_Abbreviation - API: abbreviation
- Division_ID (FK)

#### 4. **Position**
- Position_ID (PK)
- Position_Name (e.g., "Starting Pitcher", "Shortstop", "Catcher")
- Position_Type (Pitcher/Fielder)

#### 5. **Player**
- Player_ID (PK) - API: id
- First_Name - API: first_name
- Last_Name - API: last_name
- Full_Name - API: full_name
- Jersey_Number - API: jersey
- Date_of_Birth - API: dob
- Birth_Place - API: birth_place
- Height - API: height
- Weight - API: weight
- Bats_Throws - API: bats_throws
- College - API: college
- Debut_Year - API: debut_year
- Active_Status - API: active
- Draft_Info - API: draft
- Team_ID (FK)
- Position_ID (FK)

#### 6. **Game**
- Game_ID (PK) - API: id
- Game_Date - API: date
- Season - API: season
- Home_Team_ID (FK → Team)
- Away_Team_ID (FK → Team)
- Venue - API: venue
- Attendance - API: attendance
- Postseason_Flag - API: postseason
- Game_Status - API: status

#### 7. **Game_Statistics**
- Game_Stats_ID (PK)
- Game_ID (FK)
- Team_ID (FK)
- Is_Home_Team (Boolean)
- Runs - API: home_team_data.runs / away_team_data.runs
- Hits - API: home_team_data.hits / away_team_data.hits
- Errors - API: home_team_data.errors / away_team_data.errors
- Inning_Scores - API: inning_scores (stored as text/JSON)

---

## Entity-Relationship Diagram (ERD)

```
Conference (1) ──────< (M) Division
                              │
                              │
Division (1) ────────< (M) Team
                              │
                              │
Team (1) ─────────────< (M) Player
                              │
                              │
Position (1) ─────────< (M) Player

Team (1) ────< (M) Game (as Home Team)
Team (1) ────< (M) Game (as Away Team)

Game (1) ────< (M) Game_Statistics
Team (1) ────< (M) Game_Statistics
```

### Key Relationships:

1. **Conference → Division**: One-to-Many (1:M)
   - Each conference has multiple divisions
   - Each division belongs to one conference

2. **Division → Team**: One-to-Many (1:M)
   - Each division has multiple teams
   - Each team belongs to one division

3. **Team → Player**: One-to-Many (1:M)
   - Each team has multiple players
   - Each player belongs to one team (current roster)

4. **Position → Player**: One-to-Many (1:M)
   - Each position can have multiple players
   - Each player has one primary position

5. **Team → Game**: Two One-to-Many (1:M) relationships
   - Team as home team (1:M)
   - Team as away team (1:M)
   - Each game involves exactly 2 teams

6. **Game → Game_Statistics**: One-to-Many (1:M)
   - Each game has 2 statistics records (home & away)

7. **Team → Game_Statistics**: One-to-Many (1:M)
   - Each team has many game statistics records

---

## Business Rules

### 1. League Structure Rules
- **BR-1**: Each conference (AL or NL) must have exactly 3 divisions (East, Central, West)
- **BR-2**: Each division must belong to exactly one conference
- **BR-3**: There are exactly 2 conferences in MLB (American League, National League)

### 2. Team Rules
- **BR-4**: Each team must be assigned to exactly one division
- **BR-5**: A team must have a unique abbreviation (e.g., NYY, BOS, LAD)
- **BR-6**: Each team must have a location and name
- **BR-7**: There are exactly 30 MLB teams

### 3. Player Rules
- **BR-8**: Each player must be assigned to exactly one team at any given time
- **BR-9**: Each player must have exactly one primary position
- **BR-10**: A player must have a first name and last name
- **BR-11**: Jersey numbers must be unique within a team
- **BR-12**: Players must have either "active" or "inactive" status
- **BR-13**: A player's bats/throws must be recorded (Left/Right/Both)

### 4. Position Rules
- **BR-14**: Each position must have a unique name
- **BR-15**: Positions are categorized as either "Pitcher" or "Fielder"
- **BR-16**: A position can have zero or more players

### 5. Game Rules
- **BR-17**: Each game must have exactly one home team and one away team
- **BR-18**: The home team and away team in a game must be different
- **BR-19**: Each game must have a date
- **BR-20**: Each game must be assigned to a specific season (year)
- **BR-21**: A game is marked as either regular season or postseason
- **BR-22**: Each game must have a venue (stadium name)

### 6. Game Statistics Rules
- **BR-23**: Each game must have exactly 2 statistics records (one for home, one for away)
- **BR-24**: Game statistics must record hits, runs, and errors
- **BR-25**: Hits, runs, and errors must be non-negative integers
- **BR-26**: The team in game statistics must match either the home or away team of the game

### 7. Data Integrity Rules
- **BR-27**: All foreign key relationships must reference existing records
- **BR-28**: Player records cannot be deleted if they are referenced in historical data
- **BR-29**: Team records cannot be deleted if they have associated players or games
- **BR-30**: Game records cannot be deleted if they have associated statistics

---

## Data Dictionary

### Conference Table
| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| Conference_ID | INT | PK, AUTO_INCREMENT | Unique identifier |
| Conference_Name | VARCHAR(50) | NOT NULL, UNIQUE | AL or NL |
| Description | VARCHAR(255) | NULL | League description |

### Division Table
| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| Division_ID | INT | PK, AUTO_INCREMENT | Unique identifier |
| Division_Name | VARCHAR(50) | NOT NULL | East, Central, or West |
| Conference_ID | INT | FK, NOT NULL | References Conference |

### Team Table
| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| Team_ID | INT | PK | From API (1-30) |
| Team_Name | VARCHAR(100) | NOT NULL | Team name (e.g., "Yankees") |
| Team_Location | VARCHAR(100) | NOT NULL | City/State |
| Team_Abbreviation | VARCHAR(5) | NOT NULL, UNIQUE | 2-3 letter code |
| Division_ID | INT | FK, NOT NULL | References Division |

### Position Table
| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| Position_ID | INT | PK, AUTO_INCREMENT | Unique identifier |
| Position_Name | VARCHAR(50) | NOT NULL, UNIQUE | Full position name |
| Position_Type | VARCHAR(20) | NOT NULL | "Pitcher" or "Fielder" |

### Player Table
| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| Player_ID | INT | PK | From API |
| First_Name | VARCHAR(50) | NOT NULL | Player first name |
| Last_Name | VARCHAR(50) | NOT NULL | Player last name |
| Full_Name | VARCHAR(100) | NOT NULL | Full display name |
| Jersey_Number | VARCHAR(5) | NULL | Jersey # (can be null for unsigned) |
| Date_of_Birth | DATE | NULL | Birth date (parsed from dob) |
| Birth_Place | VARCHAR(100) | NULL | Birthplace |
| Height | VARCHAR(20) | NULL | Height (e.g., "6' 2\"") |
| Weight | VARCHAR(20) | NULL | Weight (e.g., "200 lbs") |
| Bats_Throws | VARCHAR(20) | NULL | Batting/Throwing hand |
| College | VARCHAR(100) | NULL | College attended |
| Debut_Year | INT | NULL | First MLB season |
| Active_Status | BOOLEAN | NOT NULL | Active or inactive |
| Draft_Info | VARCHAR(100) | NULL | Draft round and pick |
| Team_ID | INT | FK, NOT NULL | Current team |
| Position_ID | INT | FK, NOT NULL | Primary position |

### Game Table
| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| Game_ID | INT | PK | From API |
| Game_Date | DATETIME | NOT NULL | Date and time of game |
| Season | INT | NOT NULL | Year (e.g., 2024) |
| Home_Team_ID | INT | FK, NOT NULL | Home team |
| Away_Team_ID | INT | FK, NOT NULL | Away team |
| Venue | VARCHAR(100) | NULL | Stadium name |
| Attendance | INT | NULL | Number of attendees |
| Postseason_Flag | BOOLEAN | NOT NULL | Regular or postseason |
| Game_Status | VARCHAR(50) | NULL | Game status |

### Game_Statistics Table
| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| Game_Stats_ID | INT | PK, AUTO_INCREMENT | Unique identifier |
| Game_ID | INT | FK, NOT NULL | References Game |
| Team_ID | INT | FK, NOT NULL | Team for these stats |
| Is_Home_Team | BOOLEAN | NOT NULL | TRUE if home, FALSE if away |
| Runs | INT | NOT NULL, >= 0 | Runs scored |
| Hits | INT | NOT NULL, >= 0 | Hits recorded |
| Errors | INT | NOT NULL, >= 0 | Errors committed |
| Inning_Scores | TEXT | NULL | JSON array of inning scores |

---

## Normalization Analysis

### First Normal Form (1NF)
✅ **All tables are in 1NF**
- Each column contains atomic values
- No repeating groups
- Each record has a unique identifier (primary key)

### Second Normal Form (2NF)
✅ **All tables are in 2NF**
- All tables are in 1NF
- All non-key attributes are fully functionally dependent on the primary key
- No partial dependencies exist

### Third Normal Form (3NF)
✅ **All tables are in 3NF**
- All tables are in 2NF
- No transitive dependencies
- All non-key attributes depend only on the primary key

Example: Player table does not store team name directly (which would create a transitive dependency), but instead references Team_ID as a foreign key.

---

## Moneyball Application Strategy

### How This Database Supports Moneyball Analysis:

1. **Game Performance Tracking**
   - Track team hits, runs, errors across all games
   - Identify teams with high hits but low runs (inefficient offense)
   - Find teams with low errors but poor records (undervalued defense)

2. **Player Position Analysis**
   - Identify underrepresented positions on roster
   - Compare position distribution across successful vs. unsuccessful teams

3. **Team Budget Efficiency**
   - Track player acquisition data (draft info, debut year)
   - Identify young talent (low salary) with proven game performance
   - Find veteran players on underperforming teams (potential trades)

4. **Statistical Queries** (Phase 4)
   - Calculate team win percentages
   - Find players on losing teams (undervalued due to team record)
   - Identify teams with high attendance but poor performance (market inefficiency)

---

## API Data Mapping

### Teams Endpoint → Team Table
```
API Field          → DB Column
-------------------------------------
id                 → Team_ID
name               → Team_Name
location           → Team_Location
abbreviation       → Team_Abbreviation
league             → (used to lookup Division_ID)
division           → (used to lookup Division_ID)
```

### Players Endpoint → Player Table
```
API Field          → DB Column
-------------------------------------
id                 → Player_ID
first_name         → First_Name
last_name          → Last_Name
full_name          → Full_Name
jersey             → Jersey_Number
dob                → Date_of_Birth
birth_place        → Birth_Place
height             → Height
weight             → Weight
bats_throws        → Bats_Throws
college            → College
debut_year         → Debut_Year
active             → Active_Status
draft              → Draft_Info
position           → (used to lookup Position_ID)
team.id            → Team_ID
```

### Games Endpoint → Game & Game_Statistics Tables
```
API Field                    → DB Column
---------------------------------------------
id                           → Game.Game_ID
date                         → Game.Game_Date
season                       → Game.Season
home_team.id                 → Game.Home_Team_ID
away_team.id                 → Game.Away_Team_ID
venue                        → Game.Venue
attendance                   → Game.Attendance
postseason                   → Game.Postseason_Flag
status                       → Game.Game_Status

home_team_data.runs          → Game_Statistics.Runs (home)
home_team_data.hits          → Game_Statistics.Hits (home)
home_team_data.errors        → Game_Statistics.Errors (home)
away_team_data.runs          → Game_Statistics.Runs (away)
away_team_data.hits          → Game_Statistics.Hits (away)
away_team_data.errors        → Game_Statistics.Errors (away)
```

---

## Project Timeline

| Phase | Deliverable | Target Date | Status |
|-------|-------------|-------------|--------|
| 1A | ERD & Business Rules | Week 2 | ✅ Complete |
| 1B | API Testing & Data Mapping | Week 2 | ✅ Complete |
| 2 | Relational Model & Normalization | Week 3 | 🔄 Next |
| 3 | Access Database Build & Data Import | Week 3-4 | ⏳ Pending |
| 4 | SQL Queries (7 total) | Week 5 | ⏳ Pending |
| 5 | Final Report | Week 6 | ⏳ Pending |
| 6 | Submission | Week 7 | ⏳ Pending |

---

## Next Steps

1. Review and approve ERD design
2. Create Access database with 7 tables
3. Set up relationships and constraints
4. Pull 2024 season data from API
5. Transform API data to CSV format
6. Import CSV files into Access tables
7. Validate data integrity
8. Begin SQL query development

---

## Notes & Assumptions

1. **API Limitations**: Free tier does not include individual player statistics endpoints. We will use game-level statistics instead.

2. **Current Roster Only**: The Player table represents current 2024 roster assignments. Historical team changes are not tracked.

3. **Primary Position Only**: Each player is assigned one primary position. Players who play multiple positions will have their most common position listed.

4. **Season Focus**: Data collection will focus on the 2024 season, though the API contains data from 2002-present.

5. **Attendance Data**: Some games may have null attendance values (not reported).

---

**Document Version**: 1.0
**Last Updated**: November 8, 2025
**Next Review**: Phase 2 completion
