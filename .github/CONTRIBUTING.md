# Contributing to IS441 Baseball Database

**Project:** Moneyball MLB Scouting Database
**Team:** Rafael Garcia, Josh Schmeltzer, Brandon Helmuth
**Repository:** https://github.com/jag18729/IS441-Baseball-DB

---

## Table of Contents

1. [Team Workflow](#team-workflow)
2. [Git Branching Strategy](#git-branching-strategy)
3. [Commit Message Guidelines](#commit-message-guidelines)
4. [Pull Request Process](#pull-request-process)
5. [Code Review Guidelines](#code-review-guidelines)
6. [File Organization](#file-organization)
7. [Phase Checkpoints](#phase-checkpoints)
8. [Communication Protocol](#communication-protocol)

---

## Team Workflow

### Getting Started

1. **Clone the repository** (first time only):
   ```bash
   git clone https://github.com/jag18729/IS441-Baseball-DB.git
   cd IS441-Baseball-DB
   ```

2. **Update your local copy** (before starting work):
   ```bash
   git checkout main
   git pull origin main
   ```

3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes and commit**:
   ```bash
   git add .
   git commit -m "Descriptive commit message"
   ```

5. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

---

## Git Branching Strategy

### Branch Naming Convention

Use descriptive branch names that indicate the purpose:

**Format:** `<type>/<description>`

**Types:**
- `feature/` - New features or enhancements
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `data/` - Data extraction or CSV updates
- `query/` - SQL query development
- `report/` - Report writing

**Examples:**
```
feature/api-data-extraction
feature/access-database-setup
fix/csv-import-errors
docs/business-rules-update
query/moneyball-analysis
data/2024-season-update
report/executive-summary
```

### Branch Lifecycle

1. **main** - Production-ready code (protected)
   - Only merge via Pull Requests
   - Requires review before merge
   - Always deployable

2. **feature/** - Work in progress
   - Create from main
   - Merge back to main when complete
   - Delete after successful merge

3. **hotfix/** - Emergency fixes (if needed)
   - Create from main
   - Merge immediately after fix

---

## Commit Message Guidelines

### Format

```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

### Types

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Formatting (no code change)
- `refactor:` - Code restructuring
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks
- `data:` - Data updates

### Good Commit Messages

✅ **Good:**
```
feat: Add API data extraction for 2024 season

Implemented pagination logic to fetch all teams, players, and games
from Ball Don't Lie API. Includes rate limiting (5 req/min) and
error handling for 401 responses.

Closes #5
```

✅ **Good:**
```
fix: Correct foreign key constraint in Player table

Changed Team_ID constraint to ON DELETE RESTRICT to prevent
orphaned player records when teams are deleted.
```

✅ **Good:**
```
docs: Update business rules with Moneyball implications

Added section explaining how each business rule supports
Moneyball analysis approach.
```

❌ **Bad:**
```
updated stuff
```

❌ **Bad:**
```
Fixed bug
```

❌ **Bad:**
```
changes to queries
```

### Subject Line Rules

1. Use imperative mood ("Add feature" not "Added feature")
2. Don't capitalize first letter (except proper nouns)
3. No period at the end
4. Limit to 50 characters
5. Be specific and descriptive

### Body Guidelines

- Explain **what** and **why**, not **how**
- Wrap at 72 characters
- Use bullet points for multiple changes
- Reference issue numbers (#5, #12)

---

## Pull Request Process

### Before Creating a PR

**Checklist:**
- [ ] Code is tested and working
- [ ] All commits have descriptive messages
- [ ] Documentation updated (if applicable)
- [ ] No merge conflicts with main
- [ ] CSV files validated (if data update)
- [ ] SQL queries tested in Access (if query update)

### Creating a Pull Request

1. **Go to GitHub repository**
2. **Click "Pull Requests" → "New Pull Request"**
3. **Select your branch** (compare: feature/your-branch, base: main)
4. **Fill out PR template:**

```markdown
## Description
Brief summary of changes made

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Data update
- [ ] Query development

## Related Phase
Phase [1/2/3/4/5] - [Phase Name]

## Testing
How was this tested? What queries/scripts were run?

## Checklist
- [ ] Code/documentation is complete
- [ ] No errors or warnings
- [ ] Follows project conventions
- [ ] Ready for team review

## Screenshots (if applicable)
Add screenshots of query results, ERD updates, etc.
```

### PR Title Format

Use same format as commit messages:

```
feat: Add Query 5 with non-correlated subquery
fix: Resolve CSV import foreign key errors
docs: Complete data dictionary for all 7 tables
data: Extract 2024 postseason games
```

---

## Code Review Guidelines

### For Reviewers

**What to Check:**

1. **Code Quality**
   - SQL syntax is correct
   - Python code follows PEP 8
   - No hardcoded values (use variables/constants)

2. **Documentation**
   - Markdown files are properly formatted
   - Code comments are clear
   - README updates are accurate

3. **Data Integrity**
   - CSV files have correct headers
   - Foreign keys are valid
   - No duplicate records

4. **Queries**
   - Queries meet project requirements
   - Results are accurate
   - Performance is acceptable

**Review Process:**

1. Click "Files changed" in PR
2. Add inline comments for specific issues
3. Use "Review changes" button:
   - **Comment** - General feedback
   - **Approve** - Ready to merge
   - **Request changes** - Needs fixes

**Feedback Style:**

✅ **Good:** "Great work! One suggestion: consider adding an index on Season field for faster query performance."

✅ **Good:** "Query 3 looks good, but the HAVING clause threshold (8.0) should be documented. Why 8.0 hits per game?"

❌ **Bad:** "This is wrong."

❌ **Bad:** "Bad code."

### For Authors

**Responding to Reviews:**

1. Thank the reviewer
2. Discuss disagreements respectfully
3. Make requested changes
4. Mark conversations as resolved
5. Request re-review if needed

**Example Response:**
```
Thanks for catching that! I've updated the query to use an index
on the Season field. Performance improved from 2.3s to 0.4s.

Changes in commit abc1234.
```

---

## File Organization

### Directory Structure

```
IS441-Baseball-DB/
├── README.md                    # Project overview
├── .gitignore                   # Git ignore rules
│
├── docs/                        # Documentation
│   ├── BUSINESS_RULES.md
│   ├── API_RESEARCH.md
│   ├── DATA_DICTIONARY.md
│   └── (future phase docs)
│
├── .github/                     # GitHub configuration
│   └── CONTRIBUTING.md          # This file
│
├── scripts/                     # Python scripts
│   ├── extract_api_data.py
│   ├── api_explorer.py
│   └── README.md
│
├── database/                    # Database files
│   ├── schema.sql
│   └── README.md
│
├── csv_data/                    # CSV exports
│   ├── teams.csv
│   ├── players.csv
│   ├── games.csv
│   └── game_statistics.csv
│
└── (legacy files at root)       # To be organized
    ├── Phase1_Database_Design.md
    ├── ERD_Diagram.md
    ├── create_tables.sql
    └── sample_queries.sql
```

### File Naming Conventions

- Use **UPPERCASE** for important docs: `README.md`, `CONTRIBUTING.md`
- Use **PascalCase** for design docs: `Phase1_Database_Design.md`
- Use **snake_case** for scripts: `extract_api_data.py`
- Use **lowercase** for data files: `teams.csv`, `players.csv`

### Where to Put New Files

| File Type | Location | Example |
|-----------|----------|---------|
| Documentation | `docs/` | `docs/QUERIES_PLAN.md` |
| Python scripts | `scripts/` | `scripts/validate_data.py` |
| SQL scripts | `database/` | `database/queries.sql` |
| CSV data | `csv_data/` | `csv_data/new_data.csv` |
| Access database | `database/` | `database/IS441_Baseball_Scouting.accdb` |
| Report drafts | `reports/` (create) | `reports/executive_summary.docx` |
| Screenshots | `screenshots/` (create) | `screenshots/query1_result.png` |

---

## Phase Checkpoints

### Phase 1: Database Design ✅ COMPLETE
**Deliverables:**
- [x] ERD with 7 entities
- [x] 30 business rules
- [x] Relational model
- [x] Normalization analysis

**Git Tag:** `phase-1-complete`

---

### Phase 2: Relational Model ✅ COMPLETE
**Deliverables:**
- [x] Data dictionary
- [x] Table schemas
- [x] CREATE TABLE scripts

**Git Tag:** `phase-2-complete`

---

### Phase 3: Data Extraction ✅ COMPLETE
**Deliverables:**
- [x] API integration
- [x] CSV files generated
- [x] Data validation

**Git Tag:** `phase-3-complete`

**Team Actions:**
- Josh: Create feature branch `feature/access-database-import`
- Josh: Import CSV data to Access
- Josh: Push Access database to repository
- Josh: Create PR for review

---

### Phase 4: SQL Queries (IN PROGRESS)
**Deliverables:**
- [ ] 7 SQL queries written ✅ (Done by Rafael)
- [ ] All queries tested in Access
- [ ] Query results screenshots
- [ ] Query documentation

**Team Actions:**
- Rafael: Test Queries 1-2, create PR
- Josh: Test Queries 3-5, create PR
- Brandon: Test Queries 6-7, create PR

**Branches:**
- `query/rafael-queries-1-2`
- `query/josh-queries-3-5`
- `query/brandon-queries-6-7`

---

### Phase 5: Final Report (UPCOMING)
**Deliverables:**
- [ ] Executive summary (Rafael)
- [ ] Background section (Rafael)
- [ ] Business rules section (Josh)
- [ ] Data model section (Josh)
- [ ] Query documentation (All)
- [ ] Recommendations (Brandon)
- [ ] Appendix (Brandon)
- [ ] Final compilation (Brandon)

**Team Actions:**
- Each member creates branch for their section
- Submit PRs for peer review
- Brandon merges all sections
- Team reviews complete report

**Branches:**
- `report/rafael-executive-summary`
- `report/josh-data-model`
- `report/brandon-recommendations`

---

## Communication Protocol

### Daily Standups (Async)

**Post in team chat daily:**
1. What I completed yesterday
2. What I'm working on today
3. Any blockers or questions

**Example:**
```
✅ Completed: Imported teams.csv and players.csv to Access
🚧 Working on: Importing games.csv (large file, may take time)
❓ Blocker: Getting foreign key error on game imports - need help
```

### Weekly Sync Meetings

**Schedule:** [Team decides - suggest Monday 7pm]

**Agenda:**
1. Review last week's progress
2. Demo completed work
3. Discuss blockers
4. Plan next week's tasks
5. Assign new issues

**Rotate meeting leader** each week.

---

### Issue Tracking

**Use GitHub Issues** for task management:

**Label System:**
- `phase-1` to `phase-6` - Phase tags
- `bug` - Something broken
- `enhancement` - New feature
- `documentation` - Doc updates
- `data` - Data-related tasks
- `query` - SQL query tasks
- `help-wanted` - Need assistance
- `blocked` - Cannot proceed

**Issue Template:**
```markdown
## Description
What needs to be done?

## Phase
Phase [X] - [Name]

## Assignee
@username

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2

## Related Files
- path/to/file.md
```

---

### Asking for Help

**When stuck:**

1. **Check documentation first**
   - README.md
   - TEAM_GUIDE.md
   - API_RESEARCH.md

2. **Search existing issues**
   - Someone may have solved it

3. **Create an issue**
   - Tag with `help-wanted`
   - Include error messages
   - Describe what you tried

4. **Tag team members**
   - @jag18729 (Rafael) - API, data extraction
   - @josh (Josh) - Access, database
   - @brandon (Brandon) - Queries, reports

---

## Best Practices

### General Guidelines

1. **Commit often** - Small, focused commits
2. **Pull frequently** - Stay updated with main
3. **Test before pushing** - Don't break the build
4. **Document as you go** - Don't leave it for later
5. **Ask questions early** - Don't struggle alone
6. **Review others' work** - Learn from each other
7. **Celebrate wins** - Acknowledge good work

### SQL Query Development

1. **Start with comments** - Explain query purpose
2. **Format consistently** - Use indentation
3. **Test with LIMIT** - Verify logic on small dataset
4. **Check edge cases** - NULL values, empty results
5. **Document assumptions** - Why certain thresholds?

**Example:**
```sql
-- Query 3: Teams with High Batting Average
-- Purpose: Identify teams exceeding 8.0 hits per game (Moneyball: offensive efficiency)
-- Requirements: GROUP BY, HAVING, Aggregation (2+ features)
-- Author: Josh Schmeltzer
-- Date: 2025-11-10

SELECT
    t.Team_Abbreviation,
    t.Team_Name,
    AVG(gs.Hits) AS Avg_Hits_Per_Game
FROM Team t
INNER JOIN Game_Statistics gs ON t.Team_ID = gs.Team_ID
GROUP BY t.Team_Abbreviation, t.Team_Name
HAVING AVG(gs.Hits) > 8.0
ORDER BY Avg_Hits_Per_Game DESC;
```

### CSV Data Management

1. **Validate before committing** - Check row counts
2. **Document source** - Where did data come from?
3. **Include headers** - First row = column names
4. **Consistent encoding** - UTF-8
5. **No sensitive data** - Remove API keys

---

## Conflict Resolution

### Merge Conflicts

**If you encounter merge conflicts:**

1. **Don't panic** - Conflicts are normal
2. **Communicate** - Tell team you're resolving conflicts
3. **Update your branch:**
   ```bash
   git checkout main
   git pull origin main
   git checkout your-branch
   git merge main
   ```
4. **Resolve conflicts** - Edit files to fix
5. **Test** - Ensure everything still works
6. **Commit** - Mark conflicts as resolved
   ```bash
   git add .
   git commit -m "fix: Resolve merge conflicts with main"
   git push origin your-branch
   ```

### Disagreements

**If team members disagree:**

1. **Discuss in PR comments** - Public discussion
2. **Seek consensus** - Find middle ground
3. **Escalate if needed** - Ask instructor
4. **Document decision** - Why we chose approach A over B

---

## Security & Privacy

### What NOT to Commit

❌ **Never commit:**
- API keys (unless project-specific non-sensitive)
- Passwords
- Personal information
- Access database with sensitive data
- .DS_Store, .vscode/, __pycache__/

✅ **Always commit:**
- Code
- Documentation
- Sample/anonymized data
- SQL scripts
- Public API keys (Ball Don't Lie)

### Using .gitignore

Current `.gitignore` excludes:
```
__pycache__/
*.pyc
.DS_Store
.vscode/
*.accdb (Access databases)
*.laccdb (Access lock files)
```

---

## Recognition & Credit

### Contribution Tracking

All contributions are tracked via:
- Git commit history
- Pull request authorship
- Code review participation
- Issue assignments

### Peer Evaluation Alignment

Your GitHub activity will be referenced in peer evaluations:
- Number of commits
- Quality of code/docs
- Timeliness of deliverables
- Team collaboration (reviews, help)

---

## Questions?

**Contact:**
- **Rafael Garcia** - @jag18729 (GitHub), [email]
- **Josh Schmeltzer** - @josh (GitHub), [email]
- **Brandon Helmuth** - @brandon (GitHub), [email]

**Resources:**
- [GitHub Docs](https://docs.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Markdown Guide](https://www.markdownguide.org/)

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025-11-10 | Initial CONTRIBUTING.md created | Rafael Garcia |

---

**Happy Contributing!** 🎉⚾

Let's build an amazing database project together!

---

**Last Updated:** November 10, 2025
**Repository:** https://github.com/jag18729/IS441-Baseball-DB
