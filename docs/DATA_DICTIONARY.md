# Data Dictionary - IS441 Baseball Database

**Project:** Moneyball MLB Scouting Database
**Team:** Rafael Garcia, Josh Schmeltzer, Brandon Helmuth
**Database:** Microsoft Access
**Last Updated:** November 10, 2025

---

## Table of Contents

1. [Database Overview](#database-overview)
2. [Conference Table](#1-conference-table)
3. [Division Table](#2-division-table)
4. [Team Table](#3-team-table)
5. [Position Table](#4-position-table)
6. [Player Table](#5-player-table)
7. [Game Table](#6-game-table)
8. [Game_Statistics Table](#7-game_statistics-table)
9. [Relationships Summary](#relationships-summary)
10. [Index Strategy](#index-strategy)
11. [Sample Data](#sample-data)

---

## Database Overview

**Database Name:** IS441_Baseball_Scouting.accdb
**Total Tables:** 7
**Total Records (Estimated):** ~140,000
**Data Source:** Ball Don't Lie MLB API (2024 season data)
**Normalization Level:** Third Normal Form (3NF)

### Entity Summary

| Table Name | Type | Records | Description |
|------------|------|---------|-------------|
| Conference | Lookup | 2 | American and National Leagues |
| Division | Lookup | 6 | MLB divisions (AL/NL × East/Central/West) |
| Position | Lookup | 13 | Baseball positions (pitchers and fielders) |
| Team | Dimension | 30 | All 30 MLB teams |
| Player | Dimension | 1,048 | Active MLB players (2024 rosters) |
| Game | Fact | 46,000+ | Game results (2002-2024) |
| Game_Statistics | Fact | 92,000+ | Team statistics per game |

**Total Estimated Records:** 139,099

---

## 1. Conference Table

**Purpose:** Stores MLB league/conference information (American League, National League)

**Primary Key:** Conference_ID

**Table Type:** Lookup table (static data)

### Fields

| Column Name | Data Type | Size | Constraints | Description |
|-------------|-----------|------|-------------|-------------|
| Conference_ID | INT | - | PK, NOT NULL | Unique identifier for conference |
| Conference_Name | VARCHAR | 50 | NOT NULL, UNIQUE | Conference name ("American" or "National") |
| Description | VARCHAR | 255 | NULL | Additional conference details |

### Sample Data

| Conference_ID | Conference_Name | Description |
|---------------|-----------------|-------------|
| 1 | American | American League (founded 1901) |
| 2 | National | National League (founded 1876) |

### Business Rules

- Must have exactly 2 records (BR-3)
- Conference_Name must be unique (BR-2)
- Referenced by Division table

### SQL CREATE Statement

```sql
CREATE TABLE Conference (
    Conference_ID INT PRIMARY KEY,
    Conference_Name VARCHAR(50) NOT NULL UNIQUE,
    Description VARCHAR(255)
);
```

---

## 2. Division Table

**Purpose:** Stores MLB division information within each conference

**Primary Key:** Division_ID
**Foreign Keys:** Conference_ID → Conference

**Table Type:** Lookup table (static data)

### Fields

| Column Name | Data Type | Size | Constraints | Description |
|-------------|-----------|------|-------------|-------------|
| Division_ID | INT | - | PK, NOT NULL | Unique identifier for division |
| Division_Name | VARCHAR | 50 | NOT NULL | Division name ("East", "Central", "West") |
| Conference_ID | INT | - | FK, NOT NULL | References Conference table |

### Sample Data

| Division_ID | Division_Name | Conference_ID |
|-------------|---------------|---------------|
| 1 | East | 1 |
| 2 | Central | 1 |
| 3 | West | 1 |
| 4 | East | 2 |
| 5 | Central | 2 |
| 6 | West | 2 |

### Business Rules

- Must have exactly 6 records (3 per conference)
- Each conference must have East, Central, West divisions (BR-1)
- Conference_ID cannot be NULL (BR-2)

### Relationships

- **Conference (1) → Division (M):** One conference has many divisions

### SQL CREATE Statement

```sql
CREATE TABLE Division (
    Division_ID INT PRIMARY KEY,
    Division_Name VARCHAR(50) NOT NULL,
    Conference_ID INT NOT NULL,
    FOREIGN KEY (Conference_ID) REFERENCES Conference(Conference_ID)
);
```

---

## 3. Team Table

**Purpose:** Stores information about all 30 MLB teams

**Primary Key:** Team_ID
**Foreign Keys:** Division_ID → Division

**Table Type:** Dimension table

**Data Source:** API endpoint `/teams`

### Fields

| Column Name | Data Type | Size | Constraints | Description | API Field |
|-------------|-----------|------|-------------|-------------|-----------|
| Team_ID | INT | - | PK, NOT NULL | Unique team identifier (from API) | id |
| Team_Name | VARCHAR | 100 | NOT NULL | Team nickname (e.g., "Yankees") | name |
| Team_Location | VARCHAR | 100 | NOT NULL | City or region (e.g., "New York") | location |
| Team_Abbreviation | VARCHAR | 5 | NOT NULL, UNIQUE | 2-3 letter code (e.g., "NYY") | abbreviation |
| Division_ID | INT | - | FK, NOT NULL | Team's division assignment | division + league (mapped) |

### Sample Data

| Team_ID | Team_Name | Team_Location | Team_Abbreviation | Division_ID |
|---------|-----------|---------------|-------------------|-------------|
| 1 | Diamondbacks | Arizona | ARI | 6 |
| 2 | Red Sox | Boston | BOS | 1 |
| 22 | Yankees | New York | NYY | 1 |
| 19 | Dodgers | Los Angeles | LAD | 6 |

### Business Rules

- Must have exactly 30 records (BR-7)
- Team_Abbreviation must be unique (BR-5)
- Team_Name and Team_Location required (BR-6)
- Each team assigned to exactly one division (BR-4)

### Relationships

- **Division (1) → Team (M):** One division has many teams
- **Team (1) → Player (M):** One team has many players
- **Team (1) → Game (M):** One team plays many games (as home/away)

### SQL CREATE Statement

```sql
CREATE TABLE Team (
    Team_ID INT PRIMARY KEY,
    Team_Name VARCHAR(100) NOT NULL,
    Team_Location VARCHAR(100) NOT NULL,
    Team_Abbreviation VARCHAR(5) NOT NULL UNIQUE,
    Division_ID INT NOT NULL,
    FOREIGN KEY (Division_ID) REFERENCES Division(Division_ID)
);
```

---

## 4. Position Table

**Purpose:** Stores baseball position types for player classification

**Primary Key:** Position_ID

**Table Type:** Lookup table (static data)

### Fields

| Column Name | Data Type | Size | Constraints | Description |
|-------------|-----------|------|-------------|-------------|
| Position_ID | INT | - | PK, AUTO_INCREMENT | Unique position identifier |
| Position_Name | VARCHAR | 50 | NOT NULL, UNIQUE | Full position name |
| Position_Type | VARCHAR | 20 | NOT NULL | "Pitcher" or "Fielder" |

### Sample Data

| Position_ID | Position_Name | Position_Type |
|-------------|---------------|---------------|
| 1 | Starting Pitcher | Pitcher |
| 2 | Relief Pitcher | Pitcher |
| 3 | Catcher | Fielder |
| 4 | First Base | Fielder |
| 5 | Second Base | Fielder |
| 6 | Third Base | Fielder |
| 7 | Shortstop | Fielder |
| 8 | Left Field | Fielder |
| 9 | Center Field | Fielder |
| 10 | Right Field | Fielder |
| 11 | Designated Hitter | Fielder |
| 12 | Outfield | Fielder |
| 13 | Utility Player | Fielder |

### Business Rules

- Position_Name must be unique (BR-14)
- Position_Type must be "Pitcher" or "Fielder" (BR-15)
- Positions can have zero or more players (BR-16)

### Relationships

- **Position (1) → Player (0..M):** One position can have multiple players

### SQL CREATE Statement

```sql
CREATE TABLE Position (
    Position_ID INT PRIMARY KEY AUTO_INCREMENT,
    Position_Name VARCHAR(50) NOT NULL UNIQUE,
    Position_Type VARCHAR(20) NOT NULL CHECK (Position_Type IN ('Pitcher', 'Fielder'))
);
```

---

## 5. Player Table

**Purpose:** Stores MLB player biographical data and current roster assignments

**Primary Key:** Player_ID
**Foreign Keys:** Team_ID → Team, Position_ID → Position

**Table Type:** Dimension table

**Data Source:** API endpoint `/players` (filtered to active = true)

### Fields

| Column Name | Data Type | Size | Constraints | Description | API Field |
|-------------|-----------|------|-------------|-------------|-----------|
| Player_ID | INT | - | PK, NOT NULL | Unique player identifier (from API) | id |
| First_Name | VARCHAR | 50 | NOT NULL | Player's first name | first_name |
| Last_Name | VARCHAR | 50 | NOT NULL | Player's last name | last_name |
| Full_Name | VARCHAR | 100 | NOT NULL | Complete display name | full_name |
| Jersey_Number | VARCHAR | 5 | NULL | Player's jersey number | jersey |
| Date_of_Birth | DATE | - | NULL | Birth date (parsed from string) | dob |
| Birth_Place | VARCHAR | 100 | NULL | City/state of birth | birth_place |
| Height | VARCHAR | 20 | NULL | Height (e.g., "6' 2\"") | height |
| Weight | VARCHAR | 20 | NULL | Weight (e.g., "200 lbs") | weight |
| Bats_Throws | VARCHAR | 20 | NULL | Batting/throwing hand (e.g., "R/R") | bats_throws |
| College | VARCHAR | 100 | NULL | College attended | college |
| Debut_Year | INT | - | NULL | First MLB season year | debut_year |
| Active_Status | BOOLEAN | - | NOT NULL | TRUE = active, FALSE = inactive | active |
| Draft_Info | VARCHAR | 100 | NULL | Draft round and pick | draft |
| Team_ID | INT | - | FK, NOT NULL | Current team assignment | team.id |
| Position_ID | INT | - | FK, NOT NULL | Primary position | position (mapped) |

### Sample Data

| Player_ID | Full_Name | Jersey_Number | Date_of_Birth | Debut_Year | Active_Status | Team_ID | Position_ID |
|-----------|-----------|---------------|---------------|------------|---------------|---------|-------------|
| 12345 | Aaron Judge | 99 | 1992-04-26 | 2016 | TRUE | 22 | 10 |
| 23456 | Shohei Ohtani | 17 | 1994-07-05 | 2018 | TRUE | 19 | 11 |
| 34567 | Mookie Betts | 50 | 1992-10-07 | 2014 | TRUE | 19 | 10 |

### Business Rules

- Each player assigned to exactly one team (BR-8)
- Each player has one primary position (BR-9)
- First_Name and Last_Name required (BR-10)
- Jersey_Number must be unique within team (BR-11)
- Active_Status required (BR-12)
- Bats_Throws should be recorded (BR-13)

### Relationships

- **Team (1) → Player (M):** One team has many players
- **Position (1) → Player (M):** One position has many players

### Notes

- Date_of_Birth parsed from API string format (e.g., "April 26, 1992")
- Height and Weight stored as VARCHAR (non-standard units)
- Jersey_Number nullable for unsigned/pending players
- Draft_Info format: "2013 1st Round (32nd Overall)"

### SQL CREATE Statement

```sql
CREATE TABLE Player (
    Player_ID INT PRIMARY KEY,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Full_Name VARCHAR(100) NOT NULL,
    Jersey_Number VARCHAR(5),
    Date_of_Birth DATE,
    Birth_Place VARCHAR(100),
    Height VARCHAR(20),
    Weight VARCHAR(20),
    Bats_Throws VARCHAR(20),
    College VARCHAR(100),
    Debut_Year INT,
    Active_Status BOOLEAN NOT NULL,
    Draft_Info VARCHAR(100),
    Team_ID INT NOT NULL,
    Position_ID INT NOT NULL,
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID),
    FOREIGN KEY (Position_ID) REFERENCES Position(Position_ID),
    UNIQUE (Team_ID, Jersey_Number)
);
```

---

## 6. Game Table

**Purpose:** Stores MLB game information including teams, dates, and venues

**Primary Key:** Game_ID
**Foreign Keys:** Home_Team_ID → Team, Away_Team_ID → Team

**Table Type:** Fact table

**Data Source:** API endpoint `/games`

### Fields

| Column Name | Data Type | Size | Constraints | Description | API Field |
|-------------|-----------|------|-------------|-------------|-----------|
| Game_ID | INT | - | PK, NOT NULL | Unique game identifier (from API) | id |
| Game_Date | DATETIME | - | NOT NULL | Date and time of game | date |
| Season | INT | - | NOT NULL | Season year (e.g., 2024) | season |
| Home_Team_ID | INT | - | FK, NOT NULL | Home team identifier | home_team.id |
| Away_Team_ID | INT | - | FK, NOT NULL | Away team identifier | away_team.id |
| Venue | VARCHAR | 100 | NULL | Stadium name | venue |
| Attendance | INT | - | NULL | Number of attendees | attendance |
| Postseason_Flag | BOOLEAN | - | NOT NULL | TRUE = postseason, FALSE = regular | postseason |
| Game_Status | VARCHAR | 50 | NULL | Game status (e.g., "Final") | status |

### Sample Data

| Game_ID | Game_Date | Season | Home_Team_ID | Away_Team_ID | Venue | Attendance | Postseason_Flag |
|---------|-----------|--------|--------------|--------------|-------|------------|-----------------|
| 567890 | 2024-04-01 19:05:00 | 2024 | 22 | 2 | Yankee Stadium | 42000 | FALSE |
| 567891 | 2024-04-02 13:05:00 | 2024 | 19 | 28 | Dodger Stadium | 51000 | FALSE |

### Business Rules

- Each game has exactly one home and one away team (BR-17)
- Home_Team_ID ≠ Away_Team_ID (BR-18)
- Game_Date required (BR-19)
- Season required (BR-20)
- Postseason_Flag required (BR-21)
- Venue should be recorded (BR-22)

### Relationships

- **Team (1) → Game (M):** One team plays many games as home team
- **Team (1) → Game (M):** One team plays many games as away team
- **Game (1) → Game_Statistics (2):** Each game has two statistics records

### Notes

- Game_Date in DATETIME format (includes time zone)
- Attendance nullable (some games have missing data)
- Season derived from Game_Date but stored separately for indexing

### SQL CREATE Statement

```sql
CREATE TABLE Game (
    Game_ID INT PRIMARY KEY,
    Game_Date DATETIME NOT NULL,
    Season INT NOT NULL,
    Home_Team_ID INT NOT NULL,
    Away_Team_ID INT NOT NULL,
    Venue VARCHAR(100),
    Attendance INT,
    Postseason_Flag BOOLEAN NOT NULL,
    Game_Status VARCHAR(50),
    FOREIGN KEY (Home_Team_ID) REFERENCES Team(Team_ID),
    FOREIGN KEY (Away_Team_ID) REFERENCES Team(Team_ID),
    CHECK (Home_Team_ID != Away_Team_ID)
);
```

---

## 7. Game_Statistics Table

**Purpose:** Stores team-level statistics for each game (hits, runs, errors)

**Primary Key:** Game_Stats_ID
**Foreign Keys:** Game_ID → Game, Team_ID → Team

**Table Type:** Fact table

**Data Source:** API endpoint `/games` (home_team_data, away_team_data)

### Fields

| Column Name | Data Type | Size | Constraints | Description | API Field |
|-------------|-----------|------|-------------|-------------|-----------|
| Game_Stats_ID | INT | - | PK, AUTO_INCREMENT | Unique identifier for stat record | N/A |
| Game_ID | INT | - | FK, NOT NULL | References game | id |
| Team_ID | INT | - | FK, NOT NULL | Team for these statistics | home_team.id or away_team.id |
| Is_Home_Team | BOOLEAN | - | NOT NULL | TRUE = home, FALSE = away | N/A |
| Runs | INT | - | NOT NULL, >= 0 | Runs scored by team | home/away_team_data.runs |
| Hits | INT | - | NOT NULL, >= 0 | Hits recorded by team | home/away_team_data.hits |
| Errors | INT | - | NOT NULL, >= 0 | Errors committed by team | home/away_team_data.errors |
| Inning_Scores | TEXT | - | NULL | JSON array of inning scores | home/away_team_data.inning_scores |

### Sample Data

| Game_Stats_ID | Game_ID | Team_ID | Is_Home_Team | Runs | Hits | Errors | Inning_Scores |
|---------------|---------|---------|--------------|------|------|--------|---------------|
| 1 | 567890 | 22 | TRUE | 5 | 9 | 1 | [0,2,0,0,1,0,2,0,0] |
| 2 | 567890 | 2 | FALSE | 3 | 7 | 2 | [1,0,0,2,0,0,0,0,0] |

### Business Rules

- Each game has exactly 2 statistics records (BR-23)
- Runs, Hits, Errors required (BR-24)
- All statistics must be non-negative (BR-25)
- Team_ID must match home or away team from game (BR-26)

### Relationships

- **Game (1) → Game_Statistics (2):** One game has two stat records
- **Team (1) → Game_Statistics (M):** One team has many stat records

### Notes

- Game_Stats_ID is auto-incremented (not from API)
- Two records per game: one for home team, one for away team
- Inning_Scores stored as JSON text array
- Runs/Hits/Errors critical for Moneyball analysis

### Moneyball Application

**Key Metrics:**
- **Runs Per Game:** Offensive production indicator
- **Hits Per Game:** Batting effectiveness
- **Errors Per Game:** Defensive quality
- **Runs vs. Hits Ratio:** Offensive efficiency

### SQL CREATE Statement

```sql
CREATE TABLE Game_Statistics (
    Game_Stats_ID INT PRIMARY KEY AUTO_INCREMENT,
    Game_ID INT NOT NULL,
    Team_ID INT NOT NULL,
    Is_Home_Team BOOLEAN NOT NULL,
    Runs INT NOT NULL CHECK (Runs >= 0),
    Hits INT NOT NULL CHECK (Hits >= 0),
    Errors INT NOT NULL CHECK (Errors >= 0),
    Inning_Scores TEXT,
    FOREIGN KEY (Game_ID) REFERENCES Game(Game_ID),
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID)
);
```

---

## Relationships Summary

### ERD Visualization

```
Conference (1) ──< Division (M)
                     │
                     │
Division (1) ────< Team (M)
                     │
                     ├──< Player (M)
                     │
                     ├──< Game (M) [as home team]
                     ├──< Game (M) [as away team]
                     │
                     └──< Game_Statistics (M)

Position (1) ─────< Player (M)

Game (1) ─────────< Game_Statistics (2)
```

### Relationship Types

| Relationship | Type | Cardinality | Description |
|--------------|------|-------------|-------------|
| Conference → Division | 1:M | 1:3 | Each conference has 3 divisions |
| Division → Team | 1:M | 1:5 | Each division has ~5 teams |
| Team → Player | 1:M | 1:35 | Each team has ~35 players |
| Position → Player | 1:M | 1:80 | Each position has ~80 players |
| Team → Game (Home) | 1:M | 1:1500 | Each team plays ~1500 home games |
| Team → Game (Away) | 1:M | 1:1500 | Each team plays ~1500 away games |
| Game → Game_Statistics | 1:2 | 1:2 | Each game has exactly 2 stat records |
| Team → Game_Statistics | 1:M | 1:3000 | Each team has ~3000 stat records |

---

## Index Strategy

### Primary Key Indexes (Automatic)

All primary keys automatically have clustered indexes:
- Conference_ID
- Division_ID
- Team_ID
- Position_ID
- Player_ID
- Game_ID
- Game_Stats_ID

### Foreign Key Indexes (Recommended)

```sql
-- Division table
CREATE INDEX idx_division_conference ON Division(Conference_ID);

-- Team table
CREATE INDEX idx_team_division ON Team(Division_ID);

-- Player table
CREATE INDEX idx_player_team ON Player(Team_ID);
CREATE INDEX idx_player_position ON Player(Position_ID);
CREATE INDEX idx_player_active ON Player(Active_Status);

-- Game table
CREATE INDEX idx_game_home_team ON Game(Home_Team_ID);
CREATE INDEX idx_game_away_team ON Game(Away_Team_ID);
CREATE INDEX idx_game_season ON Game(Season);
CREATE INDEX idx_game_date ON Game(Game_Date);

-- Game_Statistics table
CREATE INDEX idx_gamestats_game ON Game_Statistics(Game_ID);
CREATE INDEX idx_gamestats_team ON Game_Statistics(Team_ID);
```

### Composite Indexes (For Complex Queries)

```sql
-- Games by team and season
CREATE INDEX idx_game_team_season ON Game(Home_Team_ID, Season);

-- Active players by team
CREATE INDEX idx_player_team_active ON Player(Team_ID, Active_Status);
```

---

## Sample Data

### Complete Sample Record Set

**Conference:**
```
1 | American | American League (founded 1901)
2 | National | National League (founded 1876)
```

**Division:**
```
1 | East    | 1  # AL East
2 | Central | 1  # AL Central
3 | West    | 1  # AL West
4 | East    | 2  # NL East
5 | Central | 2  # NL Central
6 | West    | 2  # NL West
```

**Team (Sample):**
```
22 | Yankees       | New York     | NYY | 1
2  | Red Sox       | Boston       | BOS | 1
19 | Dodgers       | Los Angeles  | LAD | 6
28 | Mets          | New York     | NYM | 4
```

**Position:**
```
1  | Starting Pitcher    | Pitcher
2  | Relief Pitcher      | Pitcher
3  | Catcher             | Fielder
7  | Shortstop           | Fielder
10 | Right Field         | Fielder
13 | Utility Player      | Fielder
```

**Player (Sample):**
```
12345 | Aaron Judge   | 99 | 1992-04-26 | 2016 | TRUE | 22 | 10
23456 | Shohei Ohtani | 17 | 1994-07-05 | 2018 | TRUE | 19 | 11
34567 | Mookie Betts  | 50 | 1992-10-07 | 2014 | TRUE | 19 | 10
```

**Game (Sample):**
```
567890 | 2024-04-01 19:05:00 | 2024 | 22 | 2  | Yankee Stadium | 42000 | FALSE
567891 | 2024-04-02 13:05:00 | 2024 | 19 | 28 | Dodger Stadium | 51000 | FALSE
```

**Game_Statistics (Sample):**
```
1 | 567890 | 22 | TRUE  | 5 | 9 | 1 | [0,2,0,0,1,0,2,0,0]
2 | 567890 | 2  | FALSE | 3 | 7 | 2 | [1,0,0,2,0,0,0,0,0]
3 | 567891 | 19 | TRUE  | 7 | 12| 0 | [2,0,3,0,2,0,0,0,0]
4 | 567891 | 28 | FALSE | 4 | 8 | 1 | [0,2,0,2,0,0,0,0,0]
```

---

## Data Quality Guidelines

### Required Data Validation

1. **Foreign Key Integrity**
   - All FK values must exist in referenced tables
   - Verify before import: Team_ID, Division_ID, Position_ID

2. **Non-Negative Constraints**
   - Runs, Hits, Errors must be >= 0
   - Reject records with negative statistics

3. **Date Format Consistency**
   - Game_Date in YYYY-MM-DD HH:MM:SS format
   - Date_of_Birth in YYYY-MM-DD format

4. **Boolean Values**
   - Active_Status, Postseason_Flag, Is_Home_Team
   - Must be TRUE or FALSE (1 or 0 in Access)

5. **Unique Constraints**
   - Team_Abbreviation must be unique
   - Position_Name must be unique
   - (Team_ID, Jersey_Number) must be unique

### Import Order (Critical)

To respect foreign key constraints:

1. Conference (static data in SQL script)
2. Division (static data in SQL script)
3. Position (static data in SQL script)
4. Team (from teams.csv)
5. Player (from players.csv)
6. Game (from games.csv)
7. Game_Statistics (from game_statistics.csv)

---

## Appendix: Access Data Type Mapping

| SQL Standard | Microsoft Access | Notes |
|--------------|------------------|-------|
| INT | Number (Long Integer) | 4-byte integer |
| VARCHAR(n) | Short Text | Max 255 characters |
| TEXT | Long Text | Unlimited text |
| DATE | Date/Time | Date only |
| DATETIME | Date/Time | Date and time |
| BOOLEAN | Yes/No | TRUE/FALSE |
| AUTO_INCREMENT | AutoNumber | Automatic sequential |

---

**Document Status:** Complete
**Related Documents:**
- [BUSINESS_RULES.md](BUSINESS_RULES.md)
- [API_RESEARCH.md](API_RESEARCH.md)
- [Phase1_Database_Design.md](../Phase1_Database_Design.md)
- [ERD_Diagram.md](../ERD_Diagram.md)

**SQL Scripts:**
- `create_tables.sql` (in repository root)
- `sample_queries.sql` (in repository root)

---

**Last Updated:** November 10, 2025
**Version:** 1.0
**Status:** Ready for Access Implementation
