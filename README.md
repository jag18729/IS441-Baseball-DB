# IS441 Baseball Database Project

**Moneyball Approach to MLB Player Scouting**

[![Phase](https://img.shields.io/badge/Phase-3%20Complete-success)]()
[![Database](https://img.shields.io/badge/Database-Microsoft%20Access-blue)]()
[![Data](https://img.shields.io/badge/Data-Real%202024%20MLB-orange)]()

---

## Team Members

- **Rafael Garcia** - Database Design, API Integration, Data Extraction
- **Josh Schmeltzer** - Access Database, Queries 3-5, Data Model Documentation
- **Brandon Helmuth** - Queries 6-7, Report Compilation

**GitHub Repository:** https://github.com/jag18729/IS441-Baseball-DB

---

## Project Overview

This project implements a Microsoft Access database for MLB team scouting using the **Moneyball** philosophy - leveraging statistical analysis to identify undervalued players within budget constraints.

### Key Features

- **7-Table Relational Database** - Conference, Division, Team, Position, Player, Game, Game_Statistics
- **Real 2024 MLB Data** - 30 teams, 1,048 players, 46,000+ games from Ball Don't Lie API
- **7 SQL Queries** - Demonstrating JOINs, GROUP BY, HAVING, subqueries, and aggregation
- **Complete Documentation** - ERD, business rules, data dictionary, API research
- **Moneyball Analytics** - Statistical approach to player evaluation

---

## Quick Start

### For Team Members (Josh & Brandon)

**First Time Setup:**
```bash
# 1. Clone the repository
git clone https://github.com/jag18729/IS441-Baseball-DB.git
cd IS441-Baseball-DB

# 2. Read the Quick Start guide
open QUICK_START.md

# 3. Read your task assignments
open TEAM_GUIDE.md
```

**Josh's Next Steps:**
1. Create Access database following `database/README.md`
2. Import CSV files from `csv_data/` folder
3. Test queries 3-5 from `sample_queries.sql`

**Brandon's Next Steps:**
1. Wait for Josh to complete Access setup
2. Test queries 6-7 from `sample_queries.sql`
3. Start writing report sections

---

## Repository Structure

```
IS441-Baseball-DB/
│
├── README.md                    # 👈 You are here
├── QUICK_START.md               # Fast overview for team
├── TEAM_GUIDE.md                # Detailed collaboration guide
├── SHARE_WITH_TEAM.md           # Handoff document
│
├── docs/                        # 📚 Documentation
│   ├── BUSINESS_RULES.md        # All 30 business rules
│   ├── DATA_DICTIONARY.md       # Complete table schemas
│   └── API_RESEARCH.md          # API documentation
│
├── scripts/                     # 🐍 Python Scripts
│   ├── extract_api_data.py      # Main data extraction
│   ├── api_explorer.py          # API testing utility
│   └── README.md                # Script documentation
│
├── database/                    # 🗄️ Database Files
│   ├── schema.sql               # Database schema (SQL)
│   └── README.md                # Database setup guide
│
├── csv_data/                    # 📊 CSV Data Files
│   ├── teams.csv                # 30 MLB teams
│   ├── players.csv              # 1,048 active players
│   ├── games.csv                # 46,000+ games
│   └── game_statistics.csv      # 92,000+ stats
│
├── .github/                     # ⚙️ GitHub Config
│   └── CONTRIBUTING.md          # Team workflow guide
│
└── (Legacy docs - will be moved)
    ├── Phase1_Database_Design.md
    ├── ERD_Diagram.md
    ├── create_tables.sql
    ├── sample_queries.sql
    ├── IMPORT_GUIDE.md
    └── PROJECT_STATUS.md
```

---

## Database Schema

### 7 Tables

| Table | Type | Records | Purpose |
|-------|------|---------|---------|
| **Conference** | Lookup | 2 | AL and NL leagues |
| **Division** | Lookup | 6 | 6 MLB divisions |
| **Position** | Lookup | 13 | Baseball positions |
| **Team** | Dimension | 30 | All MLB teams |
| **Player** | Dimension | 1,048 | Active players (2024) |
| **Game** | Fact | 46,000+ | Game results (2002-2024) |
| **Game_Statistics** | Fact | 92,000+ | Team stats per game |

**Total Records:** ~140,000

### Entity Relationships

```
Conference (1) ──< Division (M) ──< Team (M) ──< Player (M)
                                      │
                                      ├──< Game (M)
                                      └──< Game_Statistics (M)

Position (1) ────────────────────< Player (M)
Game (1) ─────────────────────< Game_Statistics (2)
```

**See:** [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) for complete schema

---

## SQL Queries

### Query Requirements Met

✅ **4 queries with 2+ features**
✅ **3 queries with 3+ features**
✅ **Multi-table JOINs**
✅ **GROUP BY & HAVING**
✅ **Correlated & Non-correlated subqueries**
✅ **Self-joins**

### Query List

| # | Query Name | Features | Assignee |
|---|------------|----------|----------|
| 1 | Active Players Roster | Multi-table JOIN | Rafael |
| 2 | Total Runs Per Team | GROUP BY, Aggregation | Rafael |
| 3 | Teams with High Batting | GROUP BY, HAVING | Josh |
| 4 | Position Depth by Team | GROUP BY, HAVING, Aggregation | Josh |
| 5 | Players on Winning Teams | Subquery, JOIN | Josh |
| 6 | Roster Composition | Correlated Subquery, GROUP BY | Brandon |
| 7 | Strong Divisions Analysis | JOIN, GROUP BY, HAVING, Subquery | Brandon |

**All queries in:** `sample_queries.sql`

---

## Moneyball Strategy

### How This Database Supports Moneyball Analysis

1. **Identify Undervalued Players**
   - Query players on losing teams (talent undervalued due to poor team record)
   - Find teams with high hits but low runs (inefficient offense)

2. **Statistical Analysis Over Scouting Opinions**
   - Game statistics drive decisions (hits, runs, errors)
   - Position analysis reveals roster gaps

3. **Budget Efficiency**
   - Track debut years (younger players = lower salaries)
   - Identify players on underperforming teams (trade targets)

4. **Market Inefficiencies**
   - Teams with high attendance but poor records (fanbase value)
   - Statistical outliers (high performance, low recognition)

---

## Data Source

**API:** Ball Don't Lie MLB API
**Documentation:** https://mlb.balldontlie.io/
**Base URL:** `https://api.balldontlie.io/mlb/v1`
**Data Coverage:** 2002 - Present

**Available Endpoints (Free Tier):**
- `/teams` - All 30 MLB teams
- `/players` - Player biographical data
- `/games` - Game results with team statistics

**See:** [docs/API_RESEARCH.md](docs/API_RESEARCH.md) for complete API documentation

---

## Project Phases

| Phase | Deliverable | Status |
|-------|-------------|--------|
| **Phase 1** | ERD & Business Rules | ✅ Complete |
| **Phase 2** | Relational Model & Normalization | ✅ Complete |
| **Phase 3** | Data Extraction & CSV Generation | ✅ Complete |
| **Phase 4** | SQL Queries Development | 🚧 In Progress |
| **Phase 5** | Final Report | ⏳ Upcoming |
| **Phase 6** | Submission | ⏳ Pending |

---

## Documentation

### For Database Design

- [docs/BUSINESS_RULES.md](docs/BUSINESS_RULES.md) - All 30 business rules with supporting logic
- [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) - Complete table schemas and field definitions
- [ERD_Diagram.md](ERD_Diagram.md) - Entity-Relationship Diagrams
- [Phase1_Database_Design.md](Phase1_Database_Design.md) - Complete design document

### For Implementation

- [database/README.md](database/README.md) - Database setup and Access instructions
- [IMPORT_GUIDE.md](IMPORT_GUIDE.md) - Step-by-step CSV import guide
- [sample_queries.sql](sample_queries.sql) - All 7 SQL queries with documentation

### For Data Extraction

- [docs/API_RESEARCH.md](docs/API_RESEARCH.md) - Complete API documentation
- [scripts/README.md](scripts/README.md) - Script usage and troubleshooting

### For Team Collaboration

- [TEAM_GUIDE.md](TEAM_GUIDE.md) - Comprehensive collaboration guide
- [QUICK_START.md](QUICK_START.md) - Quick reference for teammates
- [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md) - Git workflow and standards
- [SHARE_WITH_TEAM.md](SHARE_WITH_TEAM.md) - Handoff document

---

## Getting Started

### 1. Extract Data (Already Complete ✅)

Data has already been extracted by Rafael. CSV files are in `csv_data/` folder.

**If you need to re-extract:**
```bash
python3 scripts/extract_api_data.py
```

**Time:** ~2 hours (due to API rate limiting)

---

### 2. Create Access Database (Josh's Task)

**Follow the guide:** [database/README.md](database/README.md)

**Steps:**
1. Create blank Access database
2. Run `database/schema.sql` to create tables
3. Import CSV files in correct order
4. Set up table relationships
5. Verify data integrity

**Time:** 2-3 hours

---

### 3. Test SQL Queries (All Team Members)

**After Access database is ready:**

1. Open `sample_queries.sql`
2. Find your assigned queries
3. Run in Access SQL View
4. Screenshot results
5. Save screenshots for report

**Assignments:**
- Rafael: Queries 1-2
- Josh: Queries 3-5
- Brandon: Queries 6-7

**Time:** 30 minutes - 1 hour per person

---

### 4. Write Report (All Team Members)

**Section Assignments:**
- **Rafael:** Executive Summary, Background, Problem Statement
- **Josh:** Business Rules, Data Model (ERD, Relational, Normalization)
- **Brandon:** Recommendations, Appendix

**Time:** 2-3 hours per person

---

## Statistics

### Data Volume

- **30 MLB Teams** - All 30 franchises
- **1,048 Active Players** - 2024 rosters
- **46,123 Games** - Historical data (2002-2024)
- **92,246 Game Statistics** - Team performance metrics

### Project Metrics

- **7 Tables** - Normalized to 3NF
- **30 Business Rules** - Comprehensive constraints
- **7 SQL Queries** - Meeting all requirements
- **~140,000 Total Records** - Large-scale database

---

## Troubleshooting

### Common Issues

**CSV Import Errors:**
- See [IMPORT_GUIDE.md](IMPORT_GUIDE.md) troubleshooting section
- Verify import order (Conference → Division → Team → Player → Game → Stats)

**Query Syntax Errors:**
- Access SQL syntax differs from MySQL
- See [database/README.md](database/README.md) for Access-specific syntax

**API Rate Limiting:**
- Script includes automatic delays
- Don't run multiple instances simultaneously

---

## Support

### Resources

- **Project Documentation:** All files in `docs/` folder
- **Team Guide:** [TEAM_GUIDE.md](TEAM_GUIDE.md)
- **Quick Reference:** [QUICK_START.md](QUICK_START.md)

### Contact

- **Rafael Garcia** - @jag18729 (GitHub) - Database design, API integration
- **Josh Schmeltzer** - Access database, queries 3-5
- **Brandon Helmuth** - Queries 6-7, report compilation

---

## License & Attribution

**Project:** IS441 Baseball Database (Academic Project)
**Course:** IS441 - Database Management Systems
**Institution:** [Your University Name]
**Semester:** Fall 2025

**Data Source:** Ball Don't Lie MLB API (https://mlb.balldontlie.io/)
**Inspiration:** Moneyball by Michael Lewis / Moneyball (2011 film)

---

## Acknowledgments

- Ball Don't Lie for providing free MLB API access
- Michael Lewis for the Moneyball philosophy
- Our instructor for project guidance
- Team members for collaboration and dedication

---

**Last Updated:** November 10, 2025
**Version:** 2.0 (Reorganized Structure)
**Status:** Phase 3 Complete - Ready for Access Implementation

**Repository:** https://github.com/jag18729/IS441-Baseball-DB
