# Scripts - IS441 Baseball Database

**Purpose:** Python scripts for API data extraction and data processing

---

## Available Scripts

### 1. `extract_api_data.py`

**Purpose:** Main data extraction script that pulls MLB data from Ball Don't Lie API

**Features:**
- Fetches all 30 MLB teams
- Retrieves active players (2024 rosters)
- Downloads games from 2002-2024 seasons
- Generates game statistics for each game
- Outputs CSV files for Access import

**Usage:**
```bash
cd /Users/rjgar/Projects/Education/IS441-Baseball-DB
python3 scripts/extract_api_data.py
```

**Requirements:**
- Python 3.7+
- `requests` library: `pip install requests`

**API Configuration:**
- API Key: Configured in script
- Base URL: https://api.balldontlie.io/mlb/v1
- Rate Limit: 5 requests per minute
- Delay: 12 seconds between requests

**Outputs:**
- `csv_data/teams.csv` - 30 MLB teams
- `csv_data/players.csv` - 1,048 active players
- `csv_data/games.csv` - 46,000+ games
- `csv_data/game_statistics.csv` - 92,000+ stats records

**Estimated Runtime:** 90-120 minutes (due to API rate limiting)

**Progress Tracking:**
Script prints progress every 100 records:
```
Fetching teams...
✓ Teams: 30 fetched

Fetching players...
Progress: 100 players...
Progress: 200 players...
...
✓ Players: 1,048 fetched

Fetching games...
Progress: 1,000 games...
Progress: 2,000 games...
...
✓ Games: 46,123 fetched
```

---

### 2. `api_explorer.py`

**Purpose:** Utility script to explore API endpoints and data structures

**Features:**
- Tests all available endpoints
- Displays sample responses
- Checks authentication
- Identifies premium vs. free endpoints
- Outputs results to JSON file

**Usage:**
```bash
python3 scripts/api_explorer.py
```

**Outputs:**
- `api_exploration_results.json` - Full API structure analysis

**Use Cases:**
- Understanding API data format
- Testing new endpoints
- Debugging API authentication
- Documenting available fields

**Sample Output:**
```json
{
  "teams": {
    "status": 200,
    "count": 30,
    "sample": { "id": 1, "name": "Diamondbacks", ... }
  },
  "players": {
    "status": 200,
    "count": 100,
    "sample": { "id": 12345, "full_name": "Aaron Judge", ... }
  },
  "stats": {
    "status": 401,
    "error": "Unauthorized - Premium tier required"
  }
}
```

---

## Installation

### Prerequisites

**Python 3.7 or higher:**
```bash
python3 --version
```

**Install required packages:**
```bash
pip install requests
```

Or using requirements file:
```bash
pip install -r requirements.txt
```

---

## API Documentation

**API Provider:** Ball Don't Lie
**Documentation:** https://mlb.balldontlie.io/
**Base URL:** https://api.balldontlie.io/mlb/v1

**Available Endpoints (Free Tier):**
- `/teams` - All MLB teams
- `/players` - Player biographical data
- `/games` - Game results with team statistics

**Rate Limits:**
- Free Tier: 5 requests per minute
- Scripts include automatic rate limiting

---

## Data Flow

```
Ball Don't Lie API
       ↓
extract_api_data.py
       ↓
CSV Files (csv_data/)
       ↓
Microsoft Access Import
       ↓
IS441_Baseball_Scouting.accdb
```

---

## Troubleshooting

### Error: 401 Unauthorized

**Cause:** Invalid or missing API key

**Solution:**
1. Check API key in script (line 15)
2. Verify key is active: https://mlb.balldontlie.io/
3. Ensure no extra spaces in key string

---

### Error: 429 Too Many Requests

**Cause:** Rate limit exceeded

**Solution:**
- Script includes 12-second delay (automatic)
- Don't run multiple instances simultaneously
- Wait 60 seconds and retry

---

### Error: Connection timeout

**Cause:** Network issues or API downtime

**Solution:**
1. Check internet connection
2. Verify API status: https://mlb.balldontlie.io/
3. Retry after a few minutes
4. Script will resume from last successful request

---

### Error: CSV file permissions

**Cause:** csv_data/ folder doesn't exist or is read-only

**Solution:**
```bash
mkdir -p csv_data
chmod 755 csv_data
```

---

### Incomplete Data Extraction

**Cause:** Script interrupted before completion

**Solution:**
- Script can be re-run safely (overwrites CSVs)
- Check console output for last completed endpoint
- Verify all 4 CSV files exist and have data

---

## Future Enhancements

### Planned Features

1. **Resume Capability**
   - Save progress to JSON
   - Resume from last checkpoint
   - Avoid re-downloading existing data

2. **Incremental Updates**
   - Only fetch new games since last run
   - Update player roster changes
   - Track data freshness

3. **Data Validation**
   - Verify foreign key integrity
   - Check for duplicate records
   - Validate data types

4. **Multiple Seasons**
   - Command-line argument for season selection
   - Fetch specific date ranges
   - Filter postseason vs. regular season

5. **Premium Tier Support**
   - Individual player statistics
   - Advanced analytics endpoints
   - Real-time data streaming

---

## Script Reference

### extract_api_data.py Functions

| Function | Purpose |
|----------|---------|
| `make_request()` | Makes HTTP request with rate limiting |
| `fetch_all_pages()` | Handles pagination with cursor |
| `fetch_teams()` | Retrieves all 30 MLB teams |
| `fetch_active_players()` | Gets 2024 active player rosters |
| `fetch_games()` | Downloads games for specified seasons |
| `map_division_id()` | Converts league/division to Division_ID |
| `map_position_id()` | Converts position codes to Position_ID |
| `save_to_csv()` | Writes data to CSV files |

### Configuration Variables

```python
API_KEY = "e8b6410a-dd6e-4819-9e1c-7ae21f885609"
BASE_URL = "https://api.balldontlie.io/mlb/v1"
RATE_LIMIT_DELAY = 12  # seconds
SEASONS = list(range(2002, 2025))  # 2002-2024
OUTPUT_DIR = "csv_data"
```

---

## Performance Metrics

### Typical Extraction Times

| Endpoint | Records | Requests | Time |
|----------|---------|----------|------|
| Teams | 30 | 1 | ~15 sec |
| Players | 1,048 | 11 | ~3 min |
| Games (2024) | 2,430 | 25 | ~5 min |
| Games (2002-2024) | 46,123 | 462 | ~95 min |
| **Total** | **139,099** | **499** | **~100 min** |

### Optimization Tips

1. **Fetch specific seasons only** - Reduce games dataset
2. **Run overnight** - Long extraction times
3. **Use maximum per_page** - Fewer requests (100/page)
4. **Cache API responses** - Avoid re-fetching
5. **Parallel requests** - If premium tier (no rate limit)

---

## Data Integrity Checks

### Post-Extraction Validation

**Run these checks after extraction:**

```bash
# Check CSV row counts
wc -l csv_data/*.csv

# Expected:
# teams.csv: 31 (30 + header)
# players.csv: 1,049 (1,048 + header)
# games.csv: 46,124 (46,123 + header)
# game_statistics.csv: 92,247 (92,246 + header)
```

**Verify CSV headers:**
```bash
head -1 csv_data/teams.csv
# Should show: Team_ID,Team_Name,Team_Location,Team_Abbreviation,Division_ID
```

**Check for blank lines or errors:**
```bash
grep -c "^$" csv_data/*.csv  # Should be 0
```

---

## Contributing

### Adding New Scripts

1. **Follow naming convention:** `snake_case.py`
2. **Add docstrings:** Describe purpose, inputs, outputs
3. **Include error handling:** Try/except blocks
4. **Log progress:** Print statements for user feedback
5. **Update this README:** Document new script

### Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Comment complex logic
- Include function docstrings

**Example:**
```python
def fetch_teams():
    """
    Fetches all MLB teams from the API.

    Returns:
        list: List of team dictionaries with id, name, location, etc.

    Raises:
        requests.HTTPError: If API request fails
    """
    # Function implementation
```

---

## Resources

- **API Documentation:** https://mlb.balldontlie.io/
- **Python Requests Docs:** https://requests.readthedocs.io/
- **CSV Module Docs:** https://docs.python.org/3/library/csv.html
- **Project README:** ../README.md
- **Data Dictionary:** ../docs/DATA_DICTIONARY.md

---

## Support

**Issues or Questions?**
1. Check [API_RESEARCH.md](../docs/API_RESEARCH.md) for API details
2. Review script comments for inline documentation
3. Create GitHub issue with `scripts` label
4. Contact Rafael Garcia (@jag18729) - Script author

---

**Last Updated:** November 10, 2025
**Maintained By:** Rafael Garcia
**Status:** Production-ready
