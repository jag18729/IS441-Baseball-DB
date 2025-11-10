# IS441 Baseball Database Project

**Moneyball Approach to MLB Player Scouting**

**Team Members:**
- Rafael Garcia
- Josh Schmeltzer
- Brandon Helmuth

## Project Overview

This project implements a Microsoft Access database for MLB team scouting using the "Moneyball" philosophy - leveraging statistical analysis to identify undervalued players within budget constraints.

### Key Components

- **7-Table Relational Database** for MLB teams, players, and game statistics
- **Real 2024 MLB Data** from Ball Don't Lie API
- **7 SQL Queries** demonstrating advanced database concepts
- **Complete Documentation** including ERD, business rules, and normalization analysis

---

## Project Structure

```
IS441-Baseball-DB/
│
├── README.md                          # This file
├── Phase1_Database_Design.md          # Complete design documentation
├── ERD_Diagram.md                     # Entity-Relationship Diagram
│
├── create_tables.sql                  # DDL script to create all tables
├── sample_queries.sql                 # 7 SQL queries for Phase 4
│
├── api_explorer.py                    # Script to explore API endpoints
├── extract_api_data.py                # Main data extraction script
├── api_exploration_results.json       # API structure analysis
│
└── csv_data/                          # Generated CSV files (after running extract script)
    ├── teams.csv
    ├── players.csv
    ├── games.csv
    └── game_statistics.csv
```

---

## Quick Start Guide

### Step 1: Extract Data from API

Run the data extraction script to pull 2024 MLB data:

```bash
cd /Users/rjgar/Projects/Education/IS441-Baseball-DB
python3 extract_api_data.py
```

**Expected Output:**
- `csv_data/teams.csv` - All 30 MLB teams
- `csv_data/players.csv` - All active players
- `csv_data/games.csv` - 2024 season games
- `csv_data/game_statistics.csv` - Game-level team statistics

**Time Required:** ~20-30 minutes (due to API rate limiting)

### Step 2: Create Access Database

1. Open Microsoft Access
2. Create a new blank database named `IS441_Baseball_Scouting.accdb`
3. Go to **External Data** → **SQL**
4. Import and run `create_tables.sql` to create all tables

**Alternative:** Manually create tables using the schema in `Phase1_Database_Design.md`

### Step 3: Import CSV Data

Import CSV files in this order (to respect foreign key constraints):

1. **Conference** - Already created in SQL script (static data)
2. **Division** - Already created in SQL script (static data)
3. **Position** - Already created in SQL script (static data)
4. **Team** - Import `csv_data/teams.csv`
5. **Player** - Import `csv_data/players.csv`
6. **Game** - Import `csv_data/games.csv`
7. **Game_Statistics** - Import `csv_data/game_statistics.csv`

**Import Steps in Access:**
1. External Data → Text File
2. Browse to CSV file
3. Choose "Append to existing table"
4. Map CSV columns to database fields
5. Verify no import errors

### Step 4: Run SQL Queries

1. Open `sample_queries.sql`
2. Copy each query into Access SQL View
3. Run and capture results
4. Screenshot output for project report

---

## Database Schema

### 7 Tables:

1. **Conference** - American League (AL) and National League (NL)
2. **Division** - 6 divisions (AL East, AL Central, AL West, NL East, NL Central, NL West)
3. **Team** - 30 MLB teams with location, abbreviation, division
4. **Position** - 13 baseball positions (pitchers, fielders, DH, utility)
5. **Player** - Active MLB players with biographical data, team, position
6. **Game** - 2024 season games with home/away teams, venue, attendance
7. **Game_Statistics** - Per-game team statistics (runs, hits, errors)

### Key Relationships:

```
Conference (1) ──< Division (M)
Division (1) ──< Team (M)
Team (1) ──< Player (M)
Position (1) ──< Player (M)
Team (1) ──< Game (M) [as home team]
Team (1) ──< Game (M) [as away team]
Game (1) ──< Game_Statistics (2) [home & away stats]
Team (1) ──< Game_Statistics (M)
```

---

## SQL Queries Summary

### Query 1: Active Players Roster
**Features:** Multi-table JOIN
**Purpose:** View all active players with their teams and positions

### Query 2: Total Runs Per Team
**Features:** GROUP BY, Aggregation, Multi-table JOIN
**Purpose:** Identify offensive powerhouses (Moneyball: run production)

### Query 3: Teams with High Batting
**Features:** GROUP BY, HAVING, Aggregation
**Purpose:** Find teams exceeding 8.0 hits per game average

### Query 4: Position Depth by Team
**Features:** GROUP BY, HAVING, Aggregation (3+ features)
**Purpose:** Identify teams with multiple players at same position (roster management)

### Query 5: Players on Winning Teams
**Features:** Non-correlated SUBQUERY, Multi-table JOIN (2+ features)
**Purpose:** Find players on teams with >50 wins (market efficiency)

### Query 6: Roster Composition by Position Type
**Features:** Correlated SUBQUERY, GROUP BY, Multi-table JOIN (3+ features)
**Purpose:** Analyze pitcher vs. fielder distribution per team

### Query 7: Strong Divisions Analysis
**Features:** Multi-table JOIN, GROUP BY, HAVING, Subquery (3+ features)
**Purpose:** Identify divisions exceeding league average wins (competitive analysis)

**All required features covered:**
✅ GROUP BY (Queries 2, 3, 4, 6, 7)
✅ HAVING (Queries 3, 4, 7)
✅ Multi-table JOIN (All queries)
✅ Self-join (Query 4)
✅ Non-correlated subquery (Query 5)
✅ Correlated subquery (Query 6)
✅ 4 queries with 2+ features (Queries 2, 3, 5, 7)
✅ 1 query with 3+ features (Queries 4, 6, 7)

---

## Moneyball Strategy Implementation

### How This Database Supports Moneyball Analysis:

#### 1. **Identify Undervalued Players**
- Query players on losing teams (talent undervalued due to poor team record)
- Find teams with high hits but low runs (inefficient offense to exploit)
- Track young players with proven performance (low salary, high output)

#### 2. **Statistical Analysis Over Scouting Opinions**
- Game statistics drive decisions (hits, runs, errors)
- Position analysis reveals roster gaps
- Performance metrics quantify player value

#### 3. **Budget Efficiency**
- Track debut years (younger = cheaper)
- Identify players on underperforming teams (potential trade targets)
- Compare team performance vs. spending (attendance as proxy)

#### 4. **Market Inefficiencies**
- Teams with high attendance but poor records (fan base value)
- Players on small-market teams (overlooked talent)
- Statistical outliers (high OPS, low recognition)

---

## Business Rules (30 Total)

### League Structure (BR-1 to BR-3)
- 2 conferences (AL, NL) with 3 divisions each

### Team Rules (BR-4 to BR-7)
- 30 teams, each in one division with unique abbreviation

### Player Rules (BR-8 to BR-13)
- Each player on one team with one primary position
- Unique jersey numbers within team

### Position Rules (BR-14 to BR-16)
- 13 positions categorized as Pitcher or Fielder

### Game Rules (BR-17 to BR-22)
- Each game has home/away teams, date, season, venue

### Game Statistics Rules (BR-23 to BR-26)
- 2 stats records per game (home & away)
- Non-negative integer values for hits/runs/errors

### Data Integrity Rules (BR-27 to BR-30)
- Foreign key enforcement
- No deletion of historical records

**Full details:** See `Phase1_Database_Design.md` section on Business Rules

---

## Normalization Analysis

### ✅ First Normal Form (1NF)
- All columns contain atomic values
- No repeating groups
- Unique primary keys

### ✅ Second Normal Form (2NF)
- All in 1NF
- No partial dependencies
- All non-key attributes depend on entire primary key

### ✅ Third Normal Form (3NF)
- All in 2NF
- No transitive dependencies
- Non-key attributes depend ONLY on primary key

**Example:** Player table references Team_ID (FK) instead of storing team name directly, avoiding transitive dependency.

---

## API Data Source

**Ball Don't Lie MLB API**
- Base URL: `https://api.balldontlie.io/mlb/v1`
- Documentation: https://mlb.balldontlie.io/
- API Key: `e8b6410a-dd6e-4819-9e1c-7ae21f885609`
- Rate Limit: 5 requests per minute (free tier)
- Data Coverage: 2002 - Present

### Available Endpoints (Free Tier):
✅ `/teams` - All 30 MLB teams
✅ `/players` - Player biographical data
✅ `/games` - Game results with team statistics

### Premium Only:
❌ `/stats` - Individual player season statistics
❌ `/stats/players` - Advanced player analytics

---

## Troubleshooting

### CSV Import Errors

**Issue:** Foreign key constraint violation
**Solution:** Import tables in correct order (Conference → Division → Team → Player)

**Issue:** Date format errors
**Solution:** Ensure dates are in MM/DD/YYYY format (script handles this)

**Issue:** Player has invalid Position_ID
**Solution:** Check that position exists in Position table (script maps all positions)

### API Rate Limiting

**Issue:** "Too many requests" error
**Solution:** Script includes 12-second delay between requests (5 req/min limit)

**Issue:** 401 Unauthorized on stats endpoints
**Solution:** Stats require premium subscription - use game-level data instead

### Query Performance

**Issue:** Slow query execution
**Solution:** Indexes are defined in `create_tables.sql` - ensure they're created

**Issue:** Query returns no results
**Solution:** Verify Season = 2024 in WHERE clause, check that data import was successful

---

## Project Timeline

| Week | Phase | Deliverable | Status |
|------|-------|-------------|--------|
| 1-2 | Phase 1A | ERD & Business Rules | ✅ Complete |
| 2 | Phase 1B | API Testing & Mapping | ✅ Complete |
| 3 | Phase 2 | Relational Model & Normalization | ✅ Complete |
| 3-4 | Phase 3 | Access Build & Data Import | ⏳ Ready to Execute |
| 5 | Phase 4 | SQL Queries Development | ✅ Queries Written |
| 6 | Phase 5 | Final Report | ⏳ Pending |
| 7 | Phase 6 | Submission | ⏳ Pending |

---

## Team Member Task Assignments

### Member A: API & Data Collection
- [x] Sign up for API key
- [x] Test API endpoints
- [x] Run data extraction script
- [ ] Export CSV files
- [ ] Validate data quality
- [ ] Write Queries 1-2
- [ ] Executive Summary, Background (report)

### Member B: Database Design & Import
- [x] Create ERD diagram
- [x] Define business rules
- [x] Document relationships
- [ ] Create Access database
- [ ] Import CSV data
- [ ] Validate foreign keys
- [ ] Write Queries 3-5
- [ ] Data Model, Normalization (report)

### Member C: SQL & Documentation
- [x] Design SQL queries
- [x] Document query requirements
- [ ] Test all 7 queries
- [ ] Screenshot query results
- [ ] Write Queries 6-7
- [ ] Recommendations, Appendix (report)

---

## Submission Checklist

### Hard Copy (8.5 x 11 envelope):
- [ ] Complete project report (printed)
- [ ] Access database file on USB drive
- [ ] Team evaluation forms (sealed envelopes)

### Soft Copy (Canvas):
- [ ] Project report (PDF)
- [ ] Access database (.accdb file)
- [ ] Team evaluation forms

### Report Sections:
- [ ] Title page with team member names
- [ ] Executive Summary
- [ ] Background (business context)
- [ ] Business Problem & Objectives
- [ ] Business Rules (all 30 with logic)
- [ ] Data Model (ERD, Relational, Normalization)
- [ ] Query Documentation (7 queries with descriptions, code, output)
- [ ] Recommendations to Business
- [ ] Appendix (sample documents)

---

## Resources

### Documentation
- `Phase1_Database_Design.md` - Complete design document
- `ERD_Diagram.md` - Entity-Relationship Diagram
- `create_tables.sql` - Database creation script
- `sample_queries.sql` - All 7 SQL queries with explanations

### Scripts
- `api_explorer.py` - Explore API structure
- `extract_api_data.py` - Pull data and generate CSVs

### External Links
- [Ball Don't Lie API Documentation](https://mlb.balldontlie.io/)
- [Microsoft Access Help](https://support.microsoft.com/en-us/access)
- [Moneyball (2011) - IMDb](https://www.imdb.com/title/tt1210166/)

---

## Contact & Support

For questions or issues:
1. Review `Phase1_Database_Design.md` for detailed specifications
2. Check `api_exploration_results.json` for API data structure
3. Consult with team members
4. Reach out to instructor during office hours

---

## License & Attribution

**Project:** IS441 Baseball Database (Academic Project)
**Data Source:** Ball Don't Lie MLB API
**Inspiration:** Moneyball by Michael Lewis / Moneyball (2011 film)
**Team:** [Add team member names]
**Date:** November 2025

---

**Last Updated:** November 8, 2025
**Version:** 1.0
**Status:** Design Complete, Ready for Implementation
