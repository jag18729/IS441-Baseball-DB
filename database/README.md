# Database - IS441 Baseball Database

**Database Name:** IS441_Baseball_Scouting.accdb
**Platform:** Microsoft Access
**Schema:** 7 tables, Third Normal Form (3NF)

---

## Overview

This directory contains database schema definitions and the Microsoft Access database file for the IS441 Baseball Database project.

**Database Purpose:** MLB player scouting system using Moneyball approach to identify undervalued talent through statistical analysis.

---

## Files in This Directory

### 1. `schema.sql` (To be added)

**Purpose:** Complete database schema definition in SQL format

**Contents:**
- CREATE TABLE statements for all 7 tables
- PRIMARY KEY definitions
- FOREIGN KEY constraints
- CHECK constraints
- INDEX definitions
- Static data INSERT statements

**Usage:** Can be used to recreate database structure in other SQL databases (MySQL, PostgreSQL, SQL Server)

---

### 2. `IS441_Baseball_Scouting.accdb` (Josh's task)

**Purpose:** Microsoft Access database file with imported data

**Status:** To be created by Josh Schmeltzer in Phase 3

**Contents:**
- 7 tables (Conference, Division, Team, Position, Player, Game, Game_Statistics)
- Imported CSV data (~140,000 records)
- Table relationships and constraints
- 7 SQL queries (Phase 4)

**Location:** Not committed to Git (binary file, see .gitignore)
**Sharing:** Via Google Drive or USB for team collaboration

---

## Database Schema

### Tables (7 Total)

| Table | Type | Records | Description |
|-------|------|---------|-------------|
| Conference | Lookup | 2 | AL and NL leagues |
| Division | Lookup | 6 | MLB divisions |
| Position | Lookup | 13 | Baseball positions |
| Team | Dimension | 30 | All MLB teams |
| Player | Dimension | 1,048 | Active players (2024) |
| Game | Fact | 46,000+ | Game results (2002-2024) |
| Game_Statistics | Fact | 92,000+ | Team game statistics |

**Total Records:** ~140,000

---

## Entity-Relationship Diagram

```
Conference (1) ──< Division (M)
                     │
                     │
Division (1) ─────< Team (M)
                     │
                     ├──< Player (M)
                     │
                     ├──< Game (M) [as home]
                     ├──< Game (M) [as away]
                     │
                     └──< Game_Statistics (M)

Position (1) ──────< Player (M)

Game (1) ──────────< Game_Statistics (2)
```

**See also:** `../docs/DATA_DICTIONARY.md` for complete field definitions

---

## Creating the Access Database

### Step 1: Create Blank Database

1. Open Microsoft Access
2. Click "Blank Database"
3. Name: `IS441_Baseball_Scouting.accdb`
4. Save location: This folder (`database/`)
5. Click "Create"

---

### Step 2: Create Tables

**Option A: Import SQL Script**

1. Open Access
2. Go to **External Data** → **More** → **SQL**
3. Browse to `../create_tables.sql`
4. Run script to create all tables

**Option B: Manual Creation**

Follow table specifications in `../docs/DATA_DICTIONARY.md`:

1. Create → Table Design
2. Define fields with data types
3. Set primary keys
4. Add field constraints
5. Save table
6. Repeat for all 7 tables

---

### Step 3: Set Relationships

1. Go to **Database Tools** → **Relationships**
2. Add all 7 tables to the diagram
3. Create relationships by dragging foreign keys:

**Relationships to Create:**
- Conference.Conference_ID → Division.Conference_ID (1:M)
- Division.Division_ID → Team.Division_ID (1:M)
- Team.Team_ID → Player.Team_ID (1:M)
- Position.Position_ID → Player.Position_ID (1:M)
- Team.Team_ID → Game.Home_Team_ID (1:M)
- Team.Team_ID → Game.Away_Team_ID (1:M)
- Game.Game_ID → Game_Statistics.Game_ID (1:M)
- Team.Team_ID → Game_Statistics.Team_ID (1:M)

**Relationship Settings:**
- Enforce Referential Integrity: ✓ Check
- Cascade Update Related Fields: ✓ Check
- Cascade Delete Related Records: ✗ Uncheck

---

### Step 4: Import CSV Data

**Import Order (Critical - respect foreign keys):**

1. **Conference** - Static data (already in SQL script)
2. **Division** - Static data (already in SQL script)
3. **Position** - Static data (already in SQL script)
4. **Team** → Import `../csv_data/teams.csv`
5. **Player** → Import `../csv_data/players.csv`
6. **Game** → Import `../csv_data/games.csv`
7. **Game_Statistics** → Import `../csv_data/game_statistics.csv`

**Import Steps for Each CSV:**

1. **External Data** → **New Data Source** → **From File** → **Text File**
2. Browse to CSV file
3. Choose **"Append a copy of records to the table"**
4. Select target table name
5. Click **OK**
6. **Delimited** → **Comma**
7. **First Row Contains Field Names** ✓
8. Map CSV columns to table fields
9. Click **Finish**
10. Verify import: Open table and check record count

---

### Step 5: Verify Data Integrity

Run validation queries:

```sql
-- Check record counts
SELECT 'Conference' AS TableName, COUNT(*) AS Records FROM Conference
UNION ALL
SELECT 'Division', COUNT(*) FROM Division
UNION ALL
SELECT 'Position', COUNT(*) FROM Position
UNION ALL
SELECT 'Team', COUNT(*) FROM Team
UNION ALL
SELECT 'Player', COUNT(*) FROM Player
UNION ALL
SELECT 'Game', COUNT(*) FROM Game
UNION ALL
SELECT 'Game_Statistics', COUNT(*) FROM Game_Statistics;
```

**Expected Results:**
- Conference: 2
- Division: 6
- Position: 13
- Team: 30
- Player: 1,048
- Game: 46,000+
- Game_Statistics: 92,000+

**Check for orphaned records:**
```sql
-- Players with invalid Team_ID
SELECT * FROM Player
WHERE Team_ID NOT IN (SELECT Team_ID FROM Team);

-- Games with invalid Home_Team_ID
SELECT * FROM Game
WHERE Home_Team_ID NOT IN (SELECT Team_ID FROM Team);
```

Should return 0 records.

---

## SQL Queries

### Location

All 7 project queries are in: `../sample_queries.sql`

### Running Queries in Access

1. **Create** → **Query Design**
2. Close the "Show Table" dialog
3. Click **SQL View** (top left)
4. Paste query from `sample_queries.sql`
5. Click **Run** (!) to execute
6. View results

### Query Assignments

- **Rafael:** Queries 1-2
- **Josh:** Queries 3-5
- **Brandon:** Queries 6-7

### Saving Queries

1. After running query successfully
2. **File** → **Save** (Ctrl+S)
3. Name: `Query1_Active_Players`, `Query2_Total_Runs`, etc.
4. Query saved in Access database

---

## Troubleshooting

### CSV Import Errors

**Error: "Field does not exist in target table"**

**Cause:** CSV column name doesn't match table field name

**Solution:**
- Manually map columns during import
- Or edit CSV header row to match exactly

---

**Error: "Type mismatch in expression"**

**Cause:** Data type mismatch (e.g., text in number field)

**Solution:**
- Check data types in table design
- Verify CSV data format
- Look for NULL values represented as empty strings

---

**Error: "Cannot add or change record; referential integrity"**

**Cause:** Foreign key value doesn't exist in parent table

**Solution:**
- Verify import order (parent tables first)
- Check that Division_ID, Team_ID, Position_ID exist before importing child records

---

**Error: "Primary key violation" or "Duplicate values"**

**Cause:** CSV contains duplicate IDs

**Solution:**
- Check for duplicate rows in CSV
- Verify primary key field is unique
- Delete existing records before re-import

---

### Date Format Issues

**Problem:** Date_of_Birth or Game_Date importing incorrectly

**Solution:**
- Access expects: MM/DD/YYYY or YYYY-MM-DD
- Open CSV in Excel
- Format date column
- Save and re-import

---

### Query Syntax Errors

**Problem:** SQL query works in MySQL but fails in Access

**Common differences:**
- Access uses `*` for wildcard (not `%`)
- Date format: `#2024-01-01#` (not quotes)
- LIMIT not supported (use TOP instead)
- CONCAT function: Use `&` operator instead

**Examples:**
```sql
-- MySQL
SELECT * FROM Player LIMIT 10;

-- Access
SELECT TOP 10 * FROM Player;

-- MySQL
WHERE Game_Date > '2024-01-01'

-- Access
WHERE Game_Date > #2024-01-01#
```

---

## Backup Strategy

### Creating Backups

**Recommended frequency:** Daily during development

**Method 1: Manual Copy**
```bash
cp IS441_Baseball_Scouting.accdb IS441_Baseball_Scouting_BACKUP_20251110.accdb
```

**Method 2: Access Backup**
1. **File** → **Save As**
2. **Save Database As** → **Back Up Database**
3. Access adds date to filename automatically

**Backup naming:** `IS441_Baseball_Scouting_YYYY-MM-DD.accdb`

---

### Restoring from Backup

1. Close current database
2. Delete or rename corrupted file
3. Copy backup file
4. Rename to `IS441_Baseball_Scouting.accdb`
5. Open and verify

---

## Performance Optimization

### Indexing Strategy

**Already indexed (Primary Keys):**
- Conference_ID
- Division_ID
- Team_ID
- Position_ID
- Player_ID
- Game_ID
- Game_Stats_ID

**Recommended additional indexes:**

```sql
-- Foreign keys
CREATE INDEX idx_division_conference ON Division(Conference_ID);
CREATE INDEX idx_team_division ON Team(Division_ID);
CREATE INDEX idx_player_team ON Player(Team_ID);
CREATE INDEX idx_player_position ON Player(Position_ID);
CREATE INDEX idx_game_home ON Game(Home_Team_ID);
CREATE INDEX idx_game_away ON Game(Away_Team_ID);
CREATE INDEX idx_gamestats_game ON Game_Statistics(Game_ID);
CREATE INDEX idx_gamestats_team ON Game_Statistics(Team_ID);

-- Query optimization
CREATE INDEX idx_game_season ON Game(Season);
CREATE INDEX idx_player_active ON Player(Active_Status);
```

**To create indexes in Access:**
1. Open table in Design View
2. Select field
3. Set "Indexed" property to "Yes (Duplicates OK)"

---

### Query Performance Tips

1. **Use specific fields** - Avoid `SELECT *`
2. **Add WHERE clauses** - Filter early
3. **Limit result sets** - Use TOP N
4. **Join efficiently** - Index foreign keys
5. **Avoid complex subqueries** - Consider CTEs

**Example optimization:**
```sql
-- Slow
SELECT * FROM Player;

-- Fast
SELECT Player_ID, Full_Name, Team_ID
FROM Player
WHERE Active_Status = True;
```

---

## Database Maintenance

### Compact and Repair

**Run weekly** to optimize database:

1. Close all open tables
2. **Database Tools** → **Compact and Repair Database**
3. Wait for completion
4. Reopen tables

**Benefits:**
- Reduces file size
- Fixes corruption
- Improves performance

---

### Data Quality Checks

**Run monthly:**

```sql
-- Check for NULL values in required fields
SELECT COUNT(*) FROM Player WHERE Team_ID IS NULL;

-- Verify referential integrity
SELECT p.Player_ID, p.Full_Name
FROM Player p
LEFT JOIN Team t ON p.Team_ID = t.Team_ID
WHERE t.Team_ID IS NULL;

-- Find duplicate records
SELECT Full_Name, COUNT(*)
FROM Player
GROUP BY Full_Name
HAVING COUNT(*) > 1;
```

---

## Access Database Features

### Forms (Optional)

Create data entry forms:
1. Select table
2. **Create** → **Form**
3. Customize layout
4. Save form

**Useful for:**
- Manual data entry
- Viewing related records
- User-friendly interface

---

### Reports (Optional)

Generate printable reports:
1. Select query or table
2. **Create** → **Report**
3. Add grouping/sorting
4. Format layout
5. Save report

**Useful for:**
- Query result summaries
- Player rosters
- Game statistics

---

## Security & Permissions

### Database Password (Optional)

To password-protect the database:

1. Close database
2. **File** → **Open** → **Open Exclusive**
3. **Database Tools** → **Encrypt with Password**
4. Enter password
5. Save

**Warning:** If password is lost, database is unrecoverable.

---

## Version Control

### Why Access Files Aren't in Git

- Binary format (not text-based)
- Large file size (10-100 MB)
- Merge conflicts impossible to resolve
- Changes not trackable line-by-line

### Alternative: Schema Only

- Keep `schema.sql` in Git (text file)
- Share `.accdb` via Google Drive
- Document changes in commit messages

**Example workflow:**
```bash
# After modifying Access database
# Export schema to SQL
# Commit SQL file

git add database/schema.sql
git commit -m "feat: Add indexes for query performance"
```

---

## Resources

### Documentation

- [Microsoft Access Help](https://support.microsoft.com/en-us/access)
- [SQL in Access](https://support.microsoft.com/en-us/office/access-sql-basic-concepts-vocabulary-and-syntax-444d0303-cde1-424e-9a74-60be5ab6bcad)
- [Data Dictionary](../docs/DATA_DICTIONARY.md)
- [Business Rules](../docs/BUSINESS_RULES.md)

### Tutorials

- [Import CSV to Access](https://support.microsoft.com/en-us/office/import-or-link-to-data-in-a-text-file-4b8c5d78-7368-4cea-a5bb-5d3f725f99c7)
- [Create Table Relationships](https://support.microsoft.com/en-us/office/create-edit-or-delete-a-relationship-cebb77c9-e1e9-489f-bada-f4e04e56e6c9)
- [Optimize Access Performance](https://support.microsoft.com/en-us/office/optimize-an-access-database-7fc40088-2b9a-4f7b-a8b4-70c2cb1e3e5c)

---

## Support

**Questions or Issues?**

1. Check [IMPORT_GUIDE.md](../IMPORT_GUIDE.md) - Step-by-step import instructions
2. Review [DATA_DICTIONARY.md](../docs/DATA_DICTIONARY.md) - Table schemas
3. Search Microsoft Access help documentation
4. Create GitHub issue with `database` label
5. Contact Josh Schmeltzer - Database lead

---

## Team Assignments

| Task | Owner | Status |
|------|-------|--------|
| Create Access database | Josh | Pending |
| Import CSV data | Josh | Pending |
| Set up relationships | Josh | Pending |
| Test queries 1-2 | Rafael | Pending |
| Test queries 3-5 | Josh | Pending |
| Test queries 6-7 | Brandon | Pending |
| Performance tuning | Josh | Pending |

---

**Last Updated:** November 10, 2025
**Maintained By:** Josh Schmeltzer (Database Lead)
**Status:** Awaiting Phase 3 implementation
