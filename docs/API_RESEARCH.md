# API Research - Ball Don't Lie MLB API

**Project:** IS441 Baseball Database
**Team:** Rafael Garcia, Josh Schmeltzer, Brandon Helmuth
**Date:** November 10, 2025

---

## Table of Contents

1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [Available Endpoints](#available-endpoints)
4. [Data Structures](#data-structures)
5. [Rate Limiting](#rate-limiting)
6. [Python Integration](#python-integration)
7. [Data Mapping to Database](#data-mapping-to-database)
8. [Known Limitations](#known-limitations)
9. [Alternative APIs Considered](#alternative-apis-considered)

---

## API Overview

**API Name:** Ball Don't Lie MLB API
**Base URL:** `https://api.balldontlie.io/mlb/v1`
**Documentation:** https://mlb.balldontlie.io/
**Tier:** Free (with rate limits)
**Data Coverage:** 2002 - Present
**Update Frequency:** Real-time during season

### Why This API?

1. **Free Access** - No credit card required
2. **Comprehensive Data** - Teams, players, games with statistics
3. **Historical Data** - 20+ years of MLB history
4. **Active Development** - Well-maintained and documented
5. **Simple Authentication** - API key via header

### What Makes It Suitable for Moneyball Analysis?

- Game-level team statistics (hits, runs, errors)
- Complete team rosters with player positions
- Historical performance data for trend analysis
- Player biographical data (debut year, draft info)
- League/division structure for competitive analysis

---

## Authentication

### API Key

**Key:** `e8b6410a-dd6e-4819-9e1c-7ae21f885609`
**Header Name:** `Authorization`
**Format:** Plain API key (not Bearer token)

### How to Authenticate

```python
import requests

API_KEY = "e8b6410a-dd6e-4819-9e1c-7ae21f885609"
BASE_URL = "https://api.balldontlie.io/mlb/v1"

headers = {
    "Authorization": API_KEY
}

response = requests.get(f"{BASE_URL}/teams", headers=headers)
```

### Security Note

- Store API key in environment variable for production
- Never commit API keys to public repositories
- Current key is for educational project use only

---

## Available Endpoints

### Free Tier Endpoints (Accessible)

#### 1. `/teams` - MLB Teams

**Purpose:** Retrieve all 30 MLB teams with league/division information

**HTTP Method:** GET
**Authentication:** Required
**Pagination:** Yes (cursor-based)

**Query Parameters:**
- `per_page` - Results per page (max: 100, default: 25)
- `cursor` - Pagination cursor for next page

**Example Request:**
```bash
curl -X GET "https://api.balldontlie.io/mlb/v1/teams?per_page=100" \
  -H "Authorization: e8b6410a-dd6e-4819-9e1c-7ae21f885609"
```

**Example Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Diamondbacks",
      "location": "Arizona",
      "abbreviation": "ARI",
      "league": "National",
      "division": "West"
    }
  ],
  "meta": {
    "next_cursor": "eyJ...",
    "per_page": 100
  }
}
```

---

#### 2. `/players` - MLB Players

**Purpose:** Retrieve player biographical data and current roster assignments

**HTTP Method:** GET
**Authentication:** Required
**Pagination:** Yes (cursor-based)

**Query Parameters:**
- `per_page` - Results per page (max: 100)
- `cursor` - Pagination cursor
- `active` - Filter by active status (true/false)
- `team_ids[]` - Filter by team ID

**Example Request:**
```bash
curl -X GET "https://api.balldontlie.io/mlb/v1/players?per_page=100&active=true" \
  -H "Authorization: YOUR_API_KEY"
```

**Example Response:**
```json
{
  "data": [
    {
      "id": 12345,
      "first_name": "Aaron",
      "last_name": "Judge",
      "full_name": "Aaron Judge",
      "jersey": "99",
      "position": "RF",
      "dob": "April 26, 1992",
      "birth_place": "Linden, CA",
      "height": "6' 7\"",
      "weight": "282 lbs",
      "bats_throws": "R/R",
      "college": "Fresno State",
      "debut_year": 2016,
      "active": true,
      "draft": "2013 1st Round (32nd Overall)",
      "team": {
        "id": 22,
        "name": "Yankees",
        "abbreviation": "NYY"
      }
    }
  ],
  "meta": {
    "next_cursor": "eyJ...",
    "per_page": 100
  }
}
```

**Data Coverage:**
- All MLB players (active and historical)
- Biographical data (DOB, birthplace, college)
- Physical attributes (height, weight)
- Career milestones (debut year, draft info)
- Current team and position

---

#### 3. `/games` - Game Results

**Purpose:** Retrieve game results with team statistics

**HTTP Method:** GET
**Authentication:** Required
**Pagination:** Yes (cursor-based)

**Query Parameters:**
- `per_page` - Results per page (max: 100)
- `cursor` - Pagination cursor
- `seasons[]` - Filter by season(s) (e.g., 2024)
- `team_ids[]` - Filter by team ID
- `start_date` - Start date (YYYY-MM-DD)
- `end_date` - End date (YYYY-MM-DD)
- `postseason` - Filter postseason games (true/false)

**Example Request:**
```bash
curl -X GET "https://api.balldontlie.io/mlb/v1/games?per_page=100&seasons[]=2024" \
  -H "Authorization: YOUR_API_KEY"
```

**Example Response:**
```json
{
  "data": [
    {
      "id": 567890,
      "date": "2024-04-01T19:05:00.000Z",
      "season": 2024,
      "status": "Final",
      "postseason": false,
      "home_team": {
        "id": 22,
        "name": "Yankees",
        "abbreviation": "NYY"
      },
      "away_team": {
        "id": 2,
        "name": "Red Sox",
        "abbreviation": "BOS"
      },
      "home_team_data": {
        "runs": 5,
        "hits": 9,
        "errors": 1,
        "inning_scores": [0, 2, 0, 0, 1, 0, 2, 0, 0]
      },
      "away_team_data": {
        "runs": 3,
        "hits": 7,
        "errors": 2,
        "inning_scores": [1, 0, 0, 2, 0, 0, 0, 0, 0]
      },
      "venue": "Yankee Stadium",
      "attendance": 42000
    }
  ],
  "meta": {
    "next_cursor": "eyJ...",
    "per_page": 100
  }
}
```

**Game Statistics Included:**
- Runs scored (home and away)
- Hits recorded (home and away)
- Errors committed (home and away)
- Inning-by-inning scores
- Venue and attendance
- Game date and status

---

### Premium Tier Endpoints (Unavailable)

#### `/stats` - Player Season Statistics
**Status:** 401 Unauthorized (Requires paid subscription)
**Data:** Individual player batting/pitching statistics

#### `/stats/players` - Advanced Player Analytics
**Status:** 401 Unauthorized (Requires paid subscription)
**Data:** OPS, WAR, ERA+, advanced metrics

---

## Data Structures

### Pagination Format (Cursor-Based)

All endpoints use cursor-based pagination:

```json
{
  "data": [ /* array of results */ ],
  "meta": {
    "next_cursor": "eyJpZCI6MTIzfQ==",
    "per_page": 100
  }
}
```

**How It Works:**
1. First request: No cursor parameter
2. API returns `next_cursor` in meta
3. Subsequent requests: Include `cursor=<next_cursor>` parameter
4. When `next_cursor` is absent, pagination complete

---

### Player Position Codes

| Code | Position Name | Position Type |
|------|---------------|---------------|
| SP | Starting Pitcher | Pitcher |
| RP | Relief Pitcher | Pitcher |
| C | Catcher | Fielder |
| 1B | First Base | Fielder |
| 2B | Second Base | Fielder |
| 3B | Third Base | Fielder |
| SS | Shortstop | Fielder |
| LF | Left Field | Fielder |
| CF | Center Field | Fielder |
| RF | Right Field | Fielder |
| DH | Designated Hitter | Fielder |
| OF | Outfield (general) | Fielder |
| IF | Infield (general) | Fielder |
| UTIL | Utility Player | Fielder |

---

### League and Division Structure

| League (Conference) | Division | Teams |
|---------------------|----------|-------|
| American | East | 5 teams |
| American | Central | 5 teams |
| American | West | 5 teams |
| National | East | 5 teams |
| National | Central | 5 teams |
| National | West | 5 teams |

**Total:** 2 leagues × 3 divisions = 6 divisions, 30 teams

---

## Rate Limiting

### Free Tier Limits

**Rate:** 5 requests per minute
**Enforcement:** HTTP 429 (Too Many Requests) response
**Reset:** Rolling 60-second window

### Recommended Strategy

```python
import time

RATE_LIMIT_DELAY = 12  # seconds (5 requests/min = 1 request per 12 sec)

def make_request(url, headers):
    response = requests.get(url, headers=headers)
    time.sleep(RATE_LIMIT_DELAY)  # Respect rate limit
    return response.json()
```

### Data Extraction Time Estimates

| Endpoint | Records | Requests | Time (@ 5 req/min) |
|----------|---------|----------|---------------------|
| Teams | 30 | 1 | ~12 seconds |
| Players (active) | 1,048 | 11 | ~2.5 minutes |
| Players (all) | 6,830 | 69 | ~14 minutes |
| Games (2024) | 2,430 | 25 | ~5 minutes |
| Games (2002-2024) | 46,000+ | 460+ | ~95 minutes |

**Total for Full Extract:** ~100 minutes (1.5-2 hours)

---

## Python Integration

### Installation

```bash
pip install requests
```

### Basic Request Example

```python
import requests
import time

API_KEY = "e8b6410a-dd6e-4819-9e1c-7ae21f885609"
BASE_URL = "https://api.balldontlie.io/mlb/v1"

def fetch_teams():
    headers = {"Authorization": API_KEY}
    response = requests.get(f"{BASE_URL}/teams?per_page=100", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        print(f"Error: {response.status_code}")
        return []

teams = fetch_teams()
print(f"Fetched {len(teams)} teams")
```

### Pagination Helper Function

```python
def fetch_all_pages(endpoint, params=None):
    """Fetch all pages from a paginated endpoint"""
    if params is None:
        params = {}

    params['per_page'] = 100  # Maximum allowed
    all_data = []
    cursor = None

    while True:
        if cursor:
            params['cursor'] = cursor

        headers = {"Authorization": API_KEY}
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        all_data.extend(data['data'])

        # Check for next page
        if 'next_cursor' not in data.get('meta', {}):
            break

        cursor = data['meta']['next_cursor']
        time.sleep(12)  # Rate limit: 5 req/min

    return all_data
```

### Usage Example

```python
# Fetch all active players
active_players = fetch_all_pages('players', {'active': 'true'})
print(f"Total active players: {len(active_players)}")

# Fetch all 2024 season games
games_2024 = fetch_all_pages('games', {'seasons[]': 2024})
print(f"Total 2024 games: {len(games_2024)}")
```

---

## Data Mapping to Database

### Teams Endpoint → Team Table

| API Field | Database Column | Transformation |
|-----------|-----------------|----------------|
| `id` | Team_ID | Direct mapping (PK) |
| `name` | Team_Name | Direct mapping |
| `location` | Team_Location | Direct mapping |
| `abbreviation` | Team_Abbreviation | Direct mapping |
| `league` | Conference_ID | Lookup: "American" → 1, "National" → 2 |
| `division` | Division_ID | Lookup: Combine league + division |

---

### Players Endpoint → Player Table

| API Field | Database Column | Transformation |
|-----------|-----------------|----------------|
| `id` | Player_ID | Direct mapping (PK) |
| `first_name` | First_Name | Direct mapping |
| `last_name` | Last_Name | Direct mapping |
| `full_name` | Full_Name | Direct mapping |
| `jersey` | Jersey_Number | Direct mapping (nullable) |
| `dob` | Date_of_Birth | Parse string to DATE |
| `birth_place` | Birth_Place | Direct mapping |
| `height` | Height | Direct mapping (VARCHAR) |
| `weight` | Weight | Direct mapping (VARCHAR) |
| `bats_throws` | Bats_Throws | Direct mapping |
| `college` | College | Direct mapping |
| `debut_year` | Debut_Year | Direct mapping (INT) |
| `active` | Active_Status | Convert to BOOLEAN |
| `draft` | Draft_Info | Direct mapping |
| `position` | Position_ID | Lookup from Position table |
| `team.id` | Team_ID | Direct mapping (FK) |

---

### Games Endpoint → Game & Game_Statistics Tables

#### Game Table Mapping

| API Field | Database Column | Transformation |
|-----------|-----------------|----------------|
| `id` | Game_ID | Direct mapping (PK) |
| `date` | Game_Date | Parse ISO 8601 to DATETIME |
| `season` | Season | Direct mapping (INT) |
| `home_team.id` | Home_Team_ID | Direct mapping (FK) |
| `away_team.id` | Away_Team_ID | Direct mapping (FK) |
| `venue` | Venue | Direct mapping |
| `attendance` | Attendance | Direct mapping (INT, nullable) |
| `postseason` | Postseason_Flag | Convert to BOOLEAN |
| `status` | Game_Status | Direct mapping |

#### Game_Statistics Table Mapping

Two records created per game:

**Home Team Record:**
| API Field | Database Column | Value |
|-----------|-----------------|-------|
| `id` | Game_ID | From parent game |
| `home_team.id` | Team_ID | Home team ID |
| N/A | Is_Home_Team | TRUE |
| `home_team_data.runs` | Runs | Direct mapping |
| `home_team_data.hits` | Hits | Direct mapping |
| `home_team_data.errors` | Errors | Direct mapping |
| `home_team_data.inning_scores` | Inning_Scores | JSON array as TEXT |

**Away Team Record:**
| API Field | Database Column | Value |
|-----------|-----------------|-------|
| `id` | Game_ID | From parent game |
| `away_team.id` | Team_ID | Away team ID |
| N/A | Is_Home_Team | FALSE |
| `away_team_data.runs` | Runs | Direct mapping |
| `away_team_data.hits` | Hits | Direct mapping |
| `away_team_data.errors` | Errors | Direct mapping |
| `away_team_data.inning_scores` | Inning_Scores | JSON array as TEXT |

---

## Known Limitations

### 1. No Individual Player Statistics (Free Tier)

**Limitation:** Cannot access batting averages, ERAs, RBIs, home runs per player
**Workaround:** Use game-level team statistics as proxy for team performance
**Impact on Moneyball:** Analysis focuses on team-level metrics rather than individual player sabermetrics

### 2. Rate Limiting (5 requests/minute)

**Limitation:** Long extraction times for historical data
**Workaround:** Implement delay between requests, run extraction overnight
**Impact:** Initial data load takes ~2 hours for full 2002-2024 dataset

### 3. Date of Birth Parsing

**Limitation:** DOB returned as string ("April 26, 1992"), not standard date format
**Workaround:** Parse string to DATE using Python datetime library
**Code Example:**
```python
from datetime import datetime

dob_str = "April 26, 1992"
dob_date = datetime.strptime(dob_str, "%B %d, %Y")
```

### 4. Position Code Variations

**Limitation:** Some players have non-standard position codes
**Workaround:** Create position mapping dictionary with fallback to "Utility Player"
**Affected Records:** ~5% of players with unusual position designations

### 5. No Historical Team Changes

**Limitation:** API only shows current team assignment
**Workaround:** Accept snapshot of 2024 rosters, no trade history
**Impact:** Cannot track player movement between teams over time

### 6. Missing Attendance Data

**Limitation:** Some games have NULL attendance values
**Workaround:** Allow NULL in database schema, filter out in queries
**Affected Records:** ~10% of games missing attendance

---

## Alternative APIs Considered

### 1. MLB Stats API (Official)

**URL:** https://statsapi.mlb.com/
**Pros:**
- Official MLB data source
- Comprehensive individual player statistics
- Real-time updates during games
- No rate limiting

**Cons:**
- Undocumented (reverse-engineered)
- No official API key system
- Inconsistent data structures
- Risk of breaking changes

**Verdict:** Rejected due to lack of documentation and support

---

### 2. ESPN API

**URL:** https://site.api.espn.com/apis/site/v2/sports/baseball/mlb
**Pros:**
- Well-known data source
- Real-time scores and standings
- Free access

**Cons:**
- Limited historical data
- No player biographical data
- Focused on current season only
- Unofficial/undocumented

**Verdict:** Rejected due to limited historical coverage

---

### 3. Sportradar API

**URL:** https://developer.sportradar.com/
**Pros:**
- Official sports data provider
- Comprehensive statistics
- Professional-grade API

**Cons:**
- Requires paid subscription ($$$)
- Free tier very limited (1,000 requests/month)
- Overkill for academic project

**Verdict:** Rejected due to cost

---

### 4. Baseball Reference (web scraping)

**URL:** https://www.baseball-reference.com/
**Pros:**
- Most comprehensive baseball statistics
- Historical data back to 1871
- Free access via web interface

**Cons:**
- No official API
- Web scraping against ToS
- Difficult to parse HTML
- Risk of IP ban

**Verdict:** Rejected due to ToS violations and technical complexity

---

## Why Ball Don't Lie MLB API Won

✅ **Free tier with reasonable limits**
✅ **Official API with documentation**
✅ **Consistent data structures (JSON)**
✅ **Historical data (2002-present)**
✅ **Active development and maintenance**
✅ **Suitable for academic projects**
✅ **Game-level statistics (sufficient for team analysis)**

**Trade-off Accepted:** No individual player stats, but game-level team statistics enable Moneyball-style analysis of team performance and roster composition.

---

## API Resources

### Documentation
- **Official Docs:** https://mlb.balldontlie.io/
- **API Base URL:** https://api.balldontlie.io/mlb/v1

### Code Examples
- **Python Script:** `extract_api_data.py` (in repository root)
- **API Explorer:** `api_explorer.py` (endpoint testing utility)

### Support
- **Issues:** Report via API documentation website
- **Email:** Contact info available on Ball Don't Lie website

---

**Document Status:** Complete
**Last Updated:** November 10, 2025
**Related Documents:**
- [Phase1_Database_Design.md](../Phase1_Database_Design.md)
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md)
- `extract_api_data.py` (script)

---

## Appendix: Complete API Response Examples

### Full Team Response
```json
{
  "data": [
    {
      "id": 1,
      "name": "Diamondbacks",
      "location": "Arizona",
      "abbreviation": "ARI",
      "league": "National",
      "division": "West"
    }
  ],
  "meta": {
    "next_cursor": null,
    "per_page": 100
  }
}
```

### Full Player Response
```json
{
  "data": [
    {
      "id": 12345,
      "first_name": "Aaron",
      "last_name": "Judge",
      "full_name": "Aaron Judge",
      "jersey": "99",
      "position": "RF",
      "dob": "April 26, 1992",
      "birth_place": "Linden, CA",
      "height": "6' 7\"",
      "weight": "282 lbs",
      "bats_throws": "R/R",
      "college": "Fresno State",
      "debut_year": 2016,
      "active": true,
      "draft": "2013 1st Round (32nd Overall)",
      "team": {
        "id": 22,
        "name": "Yankees",
        "location": "New York",
        "abbreviation": "NYY",
        "league": "American",
        "division": "East"
      }
    }
  ],
  "meta": {
    "next_cursor": "eyJpZCI6MTIzNDZ9",
    "per_page": 100
  }
}
```

### Full Game Response
```json
{
  "data": [
    {
      "id": 567890,
      "date": "2024-04-01T19:05:00.000Z",
      "season": 2024,
      "status": "Final",
      "postseason": false,
      "home_team": {
        "id": 22,
        "name": "Yankees",
        "location": "New York",
        "abbreviation": "NYY",
        "league": "American",
        "division": "East"
      },
      "away_team": {
        "id": 2,
        "name": "Red Sox",
        "location": "Boston",
        "abbreviation": "BOS",
        "league": "American",
        "division": "East"
      },
      "home_team_data": {
        "runs": 5,
        "hits": 9,
        "errors": 1,
        "inning_scores": [0, 2, 0, 0, 1, 0, 2, 0, 0]
      },
      "away_team_data": {
        "runs": 3,
        "hits": 7,
        "errors": 2,
        "inning_scores": [1, 0, 0, 2, 0, 0, 0, 0, 0]
      },
      "venue": "Yankee Stadium",
      "attendance": 42000
    }
  ],
  "meta": {
    "next_cursor": "eyJpZCI6NTY3ODkxfQ==",
    "per_page": 100
  }
}
```

---

**End of Document**
