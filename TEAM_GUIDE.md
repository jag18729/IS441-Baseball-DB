# IS441 Baseball Database - Team Collaboration Guide

**Project Repository**: https://github.com/jag18729/IS441-Baseball-DB

## Team Members & Responsibilities

### Rafael Garcia (Member A)
**Completed:**
- ✅ ERD design and business rules
- ✅ API setup and testing
- ✅ Data extraction (teams, players, games)
- ✅ CSV file generation
- ✅ GitHub repository setup

**Remaining:**
- Executive Summary section (report)
- Background section (report)
- Queries 1-2 (test in Access)

### Josh Schmeltzer (Member B)
**To Do:**
- Create Microsoft Access database
- Import CSV files into Access (follow IMPORT_GUIDE.md)
- Validate data integrity and foreign keys
- Test Queries 3-5
- Write Data Model section (ERD, Relational Model, Normalization)

### Brandon Helmuth (Member C)
**To Do:**
- Test Queries 6-7 in Access
- Screenshot all 7 query outputs
- Write Recommendations section
- Create Appendix (screenshots, sample documents)
- Final report formatting and proofread

---

## Quick Start for Team Members

### 1. Clone the Repository

```bash
git clone https://github.com/jag18729/IS441-Baseball-DB.git
cd IS441-Baseball-DB
```

### 2. Review the Project Structure

```
IS441-Baseball-DB/
├── README.md                       # Project overview
├── TEAM_GUIDE.md                   # This file
├── Phase1_Database_Design.md       # Complete design (use for report)
├── ERD_Diagram.md                  # ERD diagrams
├── IMPORT_GUIDE.md                 # Step-by-step Access import
├── PROJECT_STATUS.md               # Current status
│
├── create_tables.sql               # SQL to create tables
├── sample_queries.sql              # 7 SQL queries with docs
│
└── csv_data/                       # Ready to import
    ├── teams.csv                   # 30 MLB teams
    ├── players.csv                 # 1,048 active players
    ├── games.csv                   # 46,000+ games
    └── game_statistics.csv         # 92,000+ game stats
```

### 3. Key Files to Use

**For Access Database (Josh):**
- `IMPORT_GUIDE.md` - Follow this step-by-step
- `create_tables.sql` - Table creation script
- `csv_data/*.csv` - Import these files

**For SQL Queries (All):**
- `sample_queries.sql` - All 7 queries ready to test
- Each query has description, code, and expected results

**For Report Writing (All):**
- `Phase1_Database_Design.md` - Copy content for report sections
- `ERD_Diagram.md` - Copy ERD diagrams
- `README.md` - Project overview for introduction

---

## Current Project Status

### ✅ Completed (Ready to Use)

**Phase 1 & 2: Database Design**
- 7-table schema designed
- 30 business rules documented
- ERD with all relationships
- Normalization verified (3NF)

**Phase 3: Data Extraction**
- All CSV files generated and tested
- 30 teams, 1,048 players, 46,000+ games
- Ready for Access import

**Phase 4: SQL Queries**
- All 7 queries written and documented
- Query requirements met:
  - ✅ Multi-table JOINs
  - ✅ GROUP BY, HAVING
  - ✅ Correlated & non-correlated subqueries
  - ✅ Self-joins
  - ✅ 4 queries with 2+ features
  - ✅ 3 queries with 3+ features

### ⏳ Next Steps (Team Effort)

**This Week:**
1. **Josh**: Create Access database and import CSV files (2-3 hours)
2. **All**: Test all 7 SQL queries in Access (1 hour each)
3. **All**: Screenshot query outputs (30 minutes)

**Next Week:**
4. **All**: Write assigned report sections (2-3 hours each)
5. **Brandon**: Compile final report and format (2-3 hours)
6. **All**: Review and proofread (1 hour)
7. **Rafael**: Submit final deliverables

---

## Access Database Setup (Josh)

### Step 1: Create the Database

1. Open Microsoft Access
2. Create new blank database: `IS441_Baseball_Scouting.accdb`
3. Save in project folder: `/IS441-Baseball-DB/`

### Step 2: Create Tables

**Option A: Run SQL Script**
- Open `create_tables.sql`
- Copy each CREATE TABLE statement
- Paste into Access SQL View
- Run each statement

**Option B: Manual Creation**
- Follow table specifications in `IMPORT_GUIDE.md`
- Create 7 tables with proper data types
- Set primary keys and foreign keys

### Step 3: Import CSV Data

**Import Order (IMPORTANT - respect foreign keys):**
1. Conference (static data - already in SQL script)
2. Division (static data - already in SQL script)
3. Position (static data - already in SQL script)
4. Team → `csv_data/teams.csv`
5. Player → `csv_data/players.csv`
6. Game → `csv_data/games.csv`
7. Game_Statistics → `csv_data/game_statistics.csv`

**Detailed steps in `IMPORT_GUIDE.md`**

### Step 4: Verify Data

Run these validation queries:

```sql
-- Check record counts
SELECT 'Conference' AS TableName, COUNT(*) AS Records FROM Conference
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

**Expected Results:**
- Conference: 2
- Division: 6
- Position: 13
- Team: 30
- Player: 1,048
- Game: 46,000+
- Game_Statistics: 92,000+

---

## SQL Queries Testing (All Team Members)

### Query Assignments

**Rafael (Queries 1-2):**
- Query 1: Active Players Roster (Multi-table JOIN)
- Query 2: Total Runs Per Team (GROUP BY, Aggregation)

**Josh (Queries 3-5):**
- Query 3: Teams with High Batting (GROUP BY, HAVING)
- Query 4: Position Depth by Team (Self-JOIN concept)
- Query 5: Players on Winning Teams (Non-correlated subquery)

**Brandon (Queries 6-7):**
- Query 6: Roster Composition (Correlated subquery)
- Query 7: Strong Divisions Analysis (Complex multi-feature)

### How to Test

1. Open `sample_queries.sql`
2. Find your assigned query
3. Copy the SQL code
4. In Access: Create → Query Design → SQL View
5. Paste query code
6. Click Run (!)
7. **Screenshot the results** (Cmd+Shift+4 on Mac)
8. Save screenshot as `Query1_Output.png`, etc.
9. Note: You may need to adjust syntax for Access (see IMPORT_GUIDE.md)

### Screenshot Checklist

For each query screenshot, include:
- [ ] Query results (full table)
- [ ] Query name/number visible
- [ ] Record count visible
- [ ] Clear, readable text

Save all screenshots in: `csv_data/screenshots/`

---

## Report Writing Guide

### Report Structure (50 points total)

**Title Page**
- IS441 Baseball Database Project
- Team members: Rafael Garcia, Josh Schmeltzer, Brandon Helmuth
- Due date: [Add date - one week before final exam]

**Section 1: Executive Summary (Rafael - 1 page)**
- Brief business description
- Problem statement (Moneyball approach)
- Database solution overview
- Key findings/results

**Section 2: Background (Rafael - 1 page)**
- MLB team scouting business context
- Current challenges in player evaluation
- Data-driven approach benefits
- Project scope and objectives

**Section 3: Business Problem (Rafael - 1 page)**
- Traditional scouting limitations
- Moneyball philosophy explanation
- How database addresses the problem
- Expected outcomes

**Section 4: Business Rules (Josh - 2 pages)**
- Copy all 30 business rules from `Phase1_Database_Design.md`
- Include supporting logic for each rule
- Organize by category (League, Team, Player, Game, etc.)

**Section 5: Data Model (Josh - 3-4 pages)**

**5.1 ERD Diagram**
- Copy ERD from `ERD_Diagram.md`
- Show all 7 tables with relationships
- Include cardinalities

**5.2 Relational Model**
- List all tables with attributes
- Show primary keys (underlined)
- Show foreign keys (with arrows)
- Copy from `Phase1_Database_Design.md`

**5.3 Normalization Analysis**
- Verify 1NF, 2NF, 3NF
- Provide examples
- Copy from `Phase1_Database_Design.md`

**Section 6: Query Documentation (All - 7-10 pages)**

**For Each of 7 Queries:**
1. **Description** (plain English)
   - What business question does it answer?
   - Why is it useful for Moneyball approach?

2. **SQL Code**
   - Copy from `sample_queries.sql`
   - Format neatly with indentation

3. **Output**
   - Include screenshot
   - Describe results (# of records, key findings)

4. **Features Used**
   - List SQL features (JOIN, GROUP BY, etc.)
   - Show which requirements are met

**Section 7: Recommendations (Brandon - 2 pages)**

**Database Enhancements:**
- Add individual player statistics (if premium API available)
- Implement historical tracking (player team changes)
- Add salary/contract data for budget analysis
- Create calculated fields (OPS, WAR equivalents)

**Business Process Improvements:**
- Regular data updates (weekly/monthly)
- Integration with scouting reports
- Dashboard development for visual analysis
- Automated alerts for undervalued players

**Future Expansion:**
- Minor league player tracking
- Injury history analysis
- Performance prediction models
- Comparative team analysis tools

**Section 8: Appendix (Brandon - 2-3 pages)**
- Sample Access forms (if created)
- All query screenshots (if not in Section 6)
- API documentation references
- Data dictionary (table/field descriptions)
- Sample game statistics report

---

## Report Formatting Guidelines

### Document Setup
- **Paper**: 8.5 x 11 inches
- **Margins**: 1 inch all sides
- **Font**: Times New Roman, 12pt
- **Line Spacing**: 1.5 or Double
- **Page Numbers**: Bottom center

### Headers
- **Title**: 16pt, Bold
- **Section Headers**: 14pt, Bold
- **Subsection Headers**: 12pt, Bold

### Tables & Figures
- Number all tables and figures
- Include captions
- Reference in text ("See Table 1")

### Code Formatting
- Use monospace font (Courier New, 10pt)
- Include line breaks for readability
- Comment complex queries

### Citations
- Cite Ball Don't Lie API
- Reference Moneyball (book/film)
- Include any other sources used

---

## Team Communication

### Collaboration Tools
- **GitHub**: https://github.com/jag18729/IS441-Baseball-DB
- **Email**: [Add team emails]
- **Meeting Schedule**: [Add schedule]

### Milestones & Deadlines

**Week 1 (This Week):**
- [ ] Josh: Access database created
- [ ] Josh: CSV files imported
- [ ] All: Queries tested and screenshots captured

**Week 2:**
- [ ] Rafael: Sections 1-3 drafted
- [ ] Josh: Sections 4-5 drafted
- [ ] Brandon: Sections 7-8 drafted

**Week 3:**
- [ ] All: Section 6 completed (query documentation)
- [ ] Brandon: Report compiled and formatted
- [ ] All: Review and proofread

**Week 4:**
- [ ] All: Peer evaluation forms completed
- [ ] Rafael: Final submission to Canvas
- [ ] All: Hard copy in envelope

### File Sharing
- **Working Drafts**: Share via Google Docs
- **Final Report**: Compile in Word/PDF
- **Access Database**: Share via Google Drive (too large for GitHub)
- **Screenshots**: Push to GitHub in `csv_data/screenshots/`

---

## Quality Checklist

### Before Submission

**Database:**
- [ ] All 7 tables created with correct schema
- [ ] All CSV data imported successfully
- [ ] Foreign key relationships verified
- [ ] All 7 queries run without errors
- [ ] Query results make sense (no data anomalies)

**Report:**
- [ ] All sections complete (1-8 + appendix)
- [ ] All 30 business rules included
- [ ] ERD diagram included and labeled
- [ ] All 7 queries documented with screenshots
- [ ] Page numbers on all pages
- [ ] Team member names on title page
- [ ] Proofread for spelling/grammar
- [ ] Consistent formatting throughout

**Deliverables:**
- [ ] Printed report (8.5 x 11 envelope)
- [ ] Access database file (.accdb)
- [ ] Soft copy uploaded to Canvas
- [ ] Peer evaluation forms (sealed envelopes)

---

## Getting Help

### Resources
1. **IMPORT_GUIDE.md** - Detailed Access import steps
2. **Phase1_Database_Design.md** - All design details
3. **sample_queries.sql** - Query code with comments
4. **PROJECT_STATUS.md** - Current status overview

### Common Issues & Solutions

**Problem**: CSV import errors
**Solution**: Check IMPORT_GUIDE.md troubleshooting section

**Problem**: Query syntax errors in Access
**Solution**: Access uses different syntax than standard SQL - see IMPORT_GUIDE.md for conversions

**Problem**: Foreign key violations
**Solution**: Import tables in correct order (see IMPORT_GUIDE.md Step 4)

**Problem**: Date format issues
**Solution**: Open CSV in Excel, reformat dates as MM/DD/YYYY

### Contact
- **Rafael Garcia**: [Add email/phone]
- **Josh Schmeltzer**: [Add email/phone]
- **Brandon Helmuth**: [Add email/phone]

---

## Success Tips

1. **Start Early**: Don't wait until the last week
2. **Test Thoroughly**: Run all queries before documenting
3. **Communicate Often**: Daily check-ins via email/chat
4. **Backup Everything**: Save multiple copies of Access database
5. **Proofread**: Fresh eyes catch errors - swap sections to review
6. **Follow Instructions**: Stick to requirements in project guidelines
7. **Ask Questions**: Better to clarify than guess
8. **Document As You Go**: Take notes during testing for easier report writing

---

**Last Updated**: November 9, 2025
**Repository**: https://github.com/jag18729/IS441-Baseball-DB
**Status**: Phase 3 Complete - Ready for Access Import & Report Writing

Good luck team! 🎓⚾
