# Microsoft Access Import Guide
## IS441 Baseball Database Project

This guide will help you import the CSV data into Microsoft Access after running the extraction script.

---

## Prerequisites

✅ CSV files generated in `csv_data/` folder:
- `teams.csv` (~30 records)
- `players.csv` (~800 records)
- `games.csv` (~2,400 records)
- `game_statistics.csv` (~4,800 records)

✅ Microsoft Access installed (2016 or later recommended)

---

## Step 1: Create New Access Database

1. Open Microsoft Access
2. Click **Blank Database**
3. Name it: `IS441_Baseball_Scouting.accdb`
4. Choose location: `/Users/rjgar/Projects/Education/IS441-Baseball-DB/`
5. Click **Create**

---

## Step 2: Create Database Tables

### Option A: Using SQL Script (Recommended)

1. In Access, click **Create** tab → **Query Design**
2. Close the "Show Table" dialog
3. Click **SQL View** button (or View → SQL View)
4. Open `create_tables.sql` in a text editor
5. Copy the entire script
6. Paste into Access SQL View
7. Click **Run** (! icon)

**Note:** Access may require you to run each CREATE TABLE statement separately. If so:
- Run Conference table creation
- Run Division table creation
- Run Position table creation
- etc.

### Option B: Manual Table Creation

If SQL import doesn't work, manually create each table:

#### 1. Conference Table
1. Create → Table Design
2. Add fields:
   - Conference_ID: Number (Long Integer), Primary Key
   - Conference_Name: Short Text (50), Required
   - Description: Short Text (255)
3. Save as "Conference"

#### 2. Division Table
1. Create → Table Design
2. Add fields:
   - Division_ID: Number (Long Integer), Primary Key
   - Division_Name: Short Text (50), Required
   - Conference_ID: Number (Long Integer), Required
3. Set foreign key:
   - Database Tools → Relationships
   - Add Conference and Division tables
   - Drag Conference_ID from Conference to Division
4. Save as "Division"

**Repeat for remaining tables:** Team, Position, Player, Game, Game_Statistics
(See `Phase1_Database_Design.md` for complete field specifications)

---

## Step 3: Insert Static Data

Run these INSERT statements in SQL View:

```sql
-- Insert Conferences
INSERT INTO Conference (Conference_ID, Conference_Name, Description) VALUES
(1, 'American League', 'American League (AL) - Designated Hitter rule');

INSERT INTO Conference (Conference_ID, Conference_Name, Description) VALUES
(2, 'National League', 'National League (NL) - Pitchers must bat');

-- Insert Divisions
INSERT INTO Division (Division_ID, Division_Name, Conference_ID) VALUES
(1, 'East', 1);

INSERT INTO Division (Division_ID, Division_Name, Conference_ID) VALUES
(2, 'Central', 1);

INSERT INTO Division (Division_ID, Division_Name, Conference_ID) VALUES
(3, 'West', 1);

INSERT INTO Division (Division_ID, Division_Name, Conference_ID) VALUES
(4, 'East', 2);

INSERT INTO Division (Division_ID, Division_Name, Conference_ID) VALUES
(5, 'Central', 2);

INSERT INTO Division (Division_ID, Division_Name, Conference_ID) VALUES
(6, 'West', 2);

-- Insert Positions (all 13)
INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
(1, 'Starting Pitcher', 'Pitcher');

INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
(2, 'Relief Pitcher', 'Pitcher');

INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
(3, 'Closer', 'Pitcher');

INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
(4, 'Catcher', 'Fielder');

INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
(5, 'First Baseman', 'Fielder');

INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
(6, 'Second Baseman', 'Fielder');

INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
(7, 'Third Baseman', 'Fielder');

INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
(8, 'Shortstop', 'Fielder');

INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
(9, 'Left Fielder', 'Fielder');

INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
(10, 'Center Fielder', 'Fielder');

INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
(11, 'Right Fielder', 'Fielder');

INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
(12, 'Designated Hitter', 'Fielder');

INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
(13, 'Utility Player', 'Fielder');
```

**Verify:**
- Conference: 2 records
- Division: 6 records
- Position: 13 records

---

## Step 4: Import CSV Files

**IMPORTANT:** Import in this order to avoid foreign key errors!

### Import 1: Teams

1. **External Data** tab → **New Data Source** → **From File** → **Text File**
2. Browse to `csv_data/teams.csv`
3. Choose **"Append a copy of records to the table"**
4. Select **Team** from dropdown
5. Click **OK**
6. **Import Wizard:**
   - Delimited, Next
   - Delimiter: Comma, First Row Contains Field Names ✓, Next
   - Next (field options - defaults OK)
   - Finish
7. Close without saving import steps

**Verify:** Team table should have 30 records

### Import 2: Players

1. **External Data** → **Text File**
2. Browse to `csv_data/players.csv`
3. Append to **Player** table
4. Follow same wizard steps as Teams
5. **IMPORTANT:** Map CSV columns to database fields:
   - Player_ID → Player_ID
   - First_Name → First_Name
   - Last_Name → Last_Name
   - Full_Name → Full_Name
   - Jersey_Number → Jersey_Number
   - Date_of_Birth → Date_of_Birth (may need date format adjustment)
   - Birth_Place → Birth_Place
   - Height → Height
   - Weight → Weight
   - Bats_Throws → Bats_Throws
   - College → College
   - Debut_Year → Debut_Year
   - Active_Status → Active_Status
   - Draft_Info → Draft_Info
   - Team_ID → Team_ID
   - Position_ID → Position_ID
6. Finish import

**Verify:** Player table should have ~800 records

**Troubleshooting:**
- If date format errors occur, open CSV in Excel, format Date_of_Birth as MM/DD/YYYY, save, and re-import
- If Team_ID or Position_ID errors occur, verify those tables were imported first

### Import 3: Games

1. **External Data** → **Text File**
2. Browse to `csv_data/games.csv`
3. Append to **Game** table
4. Follow wizard steps
5. Map fields:
   - Game_ID → Game_ID
   - Game_Date → Game_Date
   - Season → Season
   - Home_Team_ID → Home_Team_ID
   - Away_Team_ID → Away_Team_ID
   - Venue → Venue
   - Attendance → Attendance
   - Postseason_Flag → Postseason_Flag
   - Game_Status → Game_Status
6. Finish import

**Verify:** Game table should have ~2,400 records for 2024 season

### Import 4: Game Statistics

1. **External Data** → **Text File**
2. Browse to `csv_data/game_statistics.csv`
3. Append to **Game_Statistics** table
4. Follow wizard steps
5. Map fields:
   - Game_Stats_ID → Game_Stats_ID
   - Game_ID → Game_ID
   - Team_ID → Team_ID
   - Is_Home_Team → Is_Home_Team
   - Runs → Runs
   - Hits → Hits
   - Errors → Errors
   - Inning_Scores → Inning_Scores
6. Finish import

**Verify:** Game_Statistics table should have ~4,800 records (2 per game)

---

## Step 5: Verify Relationships

1. **Database Tools** tab → **Relationships**
2. Click **All Relationships** (if not already showing)
3. Verify the following relationships exist:

**Expected Relationships:**
- Conference (Conference_ID) → Division (Conference_ID)
- Division (Division_ID) → Team (Division_ID)
- Team (Team_ID) → Player (Team_ID)
- Position (Position_ID) → Player (Position_ID)
- Team (Team_ID) → Game (Home_Team_ID)
- Team (Team_ID) → Game (Away_Team_ID)
- Game (Game_ID) → Game_Statistics (Game_ID)
- Team (Team_ID) → Game_Statistics (Team_ID)

**If relationships are missing:**
1. Click **Edit Relationships**
2. Select tables and fields
3. Check **Enforce Referential Integrity**
4. Click **Create**

---

## Step 6: Test Queries

Now test the 7 SQL queries from `sample_queries.sql`:

### Test Query 1: Active Players Roster

1. Create → Query Design
2. Close "Show Table" dialog
3. View → SQL View
4. Copy Query 1 from `sample_queries.sql`
5. Paste into SQL View
6. Click **Run** (! icon)

**Expected Result:** List of all active players with their teams and positions

**If errors occur:**
- Check that all tables have data
- Verify field names match (Access may auto-rename fields)
- Adjust JOIN syntax if needed (Access uses different JOIN syntax)

### Access-Specific SQL Syntax Adjustments

Access SQL differs slightly from standard SQL. You may need to adjust:

**Standard SQL:**
```sql
STRING_AGG(p.Full_Name, ', ')
```

**Access SQL:**
```sql
-- Access doesn't have STRING_AGG, use a subquery or omit
```

**Standard SQL:**
```sql
CAST(SUM(gs.Runs) AS FLOAT)
```

**Access SQL:**
```sql
CDbl(SUM(gs.Runs))
```

**Standard SQL:**
```sql
ROUND(value, 2)
```

**Access SQL:**
```sql
Round(value, 2)
```

### Screenshot Each Query Output

For the project report, you need screenshots of all 7 query results:

1. Run query
2. **Windows:** Press `Windows + Shift + S` (Snipping Tool)
3. **Mac:** Press `Cmd + Shift + 4` (drag to select area)
4. Save screenshot as: `Query1_Output.png`, `Query2_Output.png`, etc.
5. Store in `csv_data/` folder for easy access

---

## Step 7: Validate Data Integrity

Run these validation queries to ensure data quality:

### Check for Orphaned Records

```sql
-- Players without valid teams
SELECT COUNT(*) AS Orphaned_Players
FROM Player p
LEFT JOIN Team t ON p.Team_ID = t.Team_ID
WHERE t.Team_ID IS NULL;
```
**Expected:** 0

```sql
-- Games with invalid teams
SELECT COUNT(*) AS Invalid_Games
FROM Game g
LEFT JOIN Team ht ON g.Home_Team_ID = ht.Team_ID
LEFT JOIN Team at ON g.Away_Team_ID = at.Team_ID
WHERE ht.Team_ID IS NULL OR at.Team_ID IS NULL;
```
**Expected:** 0

### Check Record Counts

```sql
SELECT
    'Conference' AS TableName, COUNT(*) AS RecordCount FROM Conference
UNION ALL
SELECT 'Division', COUNT(*) FROM Division
UNION ALL
SELECT 'Team', COUNT(*) FROM Team
UNION ALL
SELECT 'Position', COUNT(*) FROM Position
UNION ALL
SELECT 'Player', COUNT(*) FROM Player
UNION ALL
SELECT 'Game', COUNT(*) FROM Game
UNION ALL
SELECT 'Game_Statistics', COUNT(*) FROM Game_Statistics;
```

**Expected:**
- Conference: 2
- Division: 6
- Team: 30
- Position: 13
- Player: ~800
- Game: ~2,400
- Game_Statistics: ~4,800

---

## Troubleshooting Common Issues

### Issue: "Field not found" error
**Solution:** Check that CSV column names match database field names exactly (case-sensitive)

### Issue: Foreign key constraint violation
**Solution:** Ensure tables are imported in correct order (Conference → Division → Team → Player → Game → Game_Statistics)

### Issue: Date format errors
**Solution:**
1. Open CSV in Excel
2. Format date columns as MM/DD/YYYY
3. Save and re-import

### Issue: "Type mismatch" error
**Solution:** Check that CSV data types match database field types (e.g., numbers vs. text)

### Issue: Query returns no results
**Solution:**
1. Verify data was imported (check table record counts)
2. Check WHERE clause conditions (e.g., Season = 2024)
3. Verify JOIN conditions are correct

### Issue: SQL syntax error in Access
**Solution:** Access uses different SQL syntax than standard SQL
- Use `CDbl()` instead of `CAST(... AS FLOAT)`
- Use `IIf()` instead of `CASE WHEN`
- Some functions like `STRING_AGG` don't exist in Access

---

## Next Steps After Import

1. ✅ Verify all data imported correctly
2. ✅ Test all 7 SQL queries
3. ✅ Screenshot query outputs
4. ✅ Create Access forms/reports (optional, extra credit)
5. ✅ Begin compiling final project report
6. ✅ Prepare for submission

---

## Quick Reference: Import Checklist

- [ ] Access database created
- [ ] All 7 tables created
- [ ] Static data inserted (Conference, Division, Position)
- [ ] Teams CSV imported (30 records)
- [ ] Players CSV imported (~800 records)
- [ ] Games CSV imported (~2,400 records)
- [ ] Game_Statistics CSV imported (~4,800 records)
- [ ] Relationships verified
- [ ] Query 1 tested and screenshot captured
- [ ] Query 2 tested and screenshot captured
- [ ] Query 3 tested and screenshot captured
- [ ] Query 4 tested and screenshot captured
- [ ] Query 5 tested and screenshot captured
- [ ] Query 6 tested and screenshot captured
- [ ] Query 7 tested and screenshot captured
- [ ] Data validation queries run
- [ ] Database file saved and backed up

---

**Estimated Time:** 2-3 hours for complete import and testing

**Need Help?**
- Check `Phase1_Database_Design.md` for table specifications
- Check `sample_queries.sql` for query examples
- Consult Access Help documentation
- Ask team members or instructor

---

**Last Updated:** November 8, 2025
**Version:** 1.0
