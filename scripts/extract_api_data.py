#!/usr/bin/env python3
"""
IS441 Baseball Database Project - Data Extraction Script
Pulls 2024 MLB data from Ball Don't Lie API and generates CSV files for Access import
"""

import requests
import csv
import json
import time
from datetime import datetime
from typing import List, Dict, Any

# API Configuration
API_KEY = "e8b6410a-dd6e-4819-9e1c-7ae21f885609"
BASE_URL = "https://api.balldontlie.io/mlb/v1"
HEADERS = {"Authorization": API_KEY}
RATE_LIMIT_DELAY = 12  # seconds (5 req/min = 12 sec between requests)

# Output directory
OUTPUT_DIR = "./csv_data"

# Division mapping (league + division → Division_ID)
DIVISION_MAP = {
    ('American', 'East'): 1,
    ('American', 'Central'): 2,
    ('American', 'West'): 3,
    ('National', 'East'): 4,
    ('National', 'Central'): 5,
    ('National', 'West'): 6,
}

# Position mapping (position name → Position_ID)
POSITION_MAP = {
    'Starting Pitcher': 1,
    'Relief Pitcher': 2,
    'Closer': 3,
    'Catcher': 4,
    'First Baseman': 5,
    'Second Baseman': 6,
    'Third Baseman': 7,
    'Shortstop': 8,
    'Left Fielder': 9,
    'Center Fielder': 10,
    'Right Fielder': 11,
    'Designated Hitter': 12,
    'Utility Player': 13,
}


def make_request(endpoint: str, params: Dict = None) -> Dict[str, Any]:
    """Make API request with rate limiting and error handling"""
    url = f"{BASE_URL}/{endpoint}"
    time.sleep(RATE_LIMIT_DELAY)

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def fetch_all_pages(endpoint: str, params: Dict = None) -> List[Dict]:
    """Fetch all pages of data from a paginated endpoint"""
    all_data = []
    cursor = None
    page = 1

    if params is None:
        params = {}

    params['per_page'] = 100  # Maximum allowed

    while True:
        if cursor:
            params['cursor'] = cursor

        print(f"  Fetching page {page}... ", end='', flush=True)
        data = make_request(endpoint, params)

        if not data or 'data' not in data:
            print("❌ Failed")
            break

        all_data.extend(data['data'])
        print(f"✅ Got {len(data['data'])} records (Total: {len(all_data)})")

        # Check if there's a next page
        if 'meta' in data and 'next_cursor' in data['meta'] and data['meta']['next_cursor']:
            cursor = data['meta']['next_cursor']
            page += 1
        else:
            break

    return all_data


def parse_date(date_str: str) -> str:
    """Parse API date to Access-friendly format (MM/DD/YYYY)"""
    if not date_str:
        return ''

    # API format: "26/6/1992" (D/M/YYYY)
    try:
        parts = date_str.split('/')
        if len(parts) == 3:
            day, month, year = parts
            return f"{month.zfill(2)}/{day.zfill(2)}/{year}"
    except:
        pass

    return date_str


def parse_datetime(datetime_str: str) -> str:
    """Parse ISO datetime to Access format"""
    if not datetime_str:
        return ''

    try:
        # API format: "2002-04-01T01:05:00.000Z"
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return dt.strftime("%m/%d/%Y %H:%M:%S")
    except:
        return datetime_str


def get_position_id(position_name: str) -> int:
    """Map position name to Position_ID, with fallback"""
    # Exact match
    if position_name in POSITION_MAP:
        return POSITION_MAP[position_name]

    # Fuzzy matching
    if 'Pitcher' in position_name and 'Relief' in position_name:
        return POSITION_MAP['Relief Pitcher']
    elif 'Pitcher' in position_name and 'Starting' in position_name:
        return POSITION_MAP['Starting Pitcher']
    elif 'Pitcher' in position_name and 'Closer' in position_name:
        return POSITION_MAP['Closer']
    elif 'Pitcher' in position_name:
        return POSITION_MAP['Starting Pitcher']  # Default for pitchers
    elif 'Designated Hitter' in position_name:
        return POSITION_MAP['Designated Hitter']
    else:
        # Check for partial matches
        for pos_name, pos_id in POSITION_MAP.items():
            if pos_name.lower() in position_name.lower() or position_name.lower() in pos_name.lower():
                return pos_id

    # Default to Utility Player if no match
    print(f"  ⚠️  Unknown position '{position_name}', defaulting to Utility Player")
    return POSITION_MAP['Utility Player']


def extract_teams() -> List[Dict]:
    """Extract all MLB teams and save to CSV"""
    print("\n" + "="*60)
    print("📊 Extracting TEAMS data")
    print("="*60)

    teams = fetch_all_pages("teams")

    # Transform for CSV
    team_rows = []
    for team in teams:
        division_id = DIVISION_MAP.get((team['league'], team['division']))

        team_rows.append({
            'Team_ID': team['id'],
            'Team_Name': team['name'],
            'Team_Location': team['location'],
            'Team_Abbreviation': team['abbreviation'],
            'Division_ID': division_id
        })

    # Write to CSV
    filename = f"{OUTPUT_DIR}/teams.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Team_ID', 'Team_Name', 'Team_Location', 'Team_Abbreviation', 'Division_ID'])
        writer.writeheader()
        writer.writerows(team_rows)

    print(f"✅ Saved {len(team_rows)} teams to {filename}")
    return teams


def extract_players() -> List[Dict]:
    """Extract all active MLB players and save to CSV"""
    print("\n" + "="*60)
    print("📊 Extracting PLAYERS data")
    print("="*60)

    players = fetch_all_pages("players")

    # Filter for active players only
    active_players = [p for p in players if p.get('active', False)]
    print(f"  Filtered to {len(active_players)} active players (out of {len(players)} total)")

    # Transform for CSV
    player_rows = []
    for player in active_players:
        position_id = get_position_id(player.get('position', 'Utility Player'))

        player_rows.append({
            'Player_ID': player['id'],
            'First_Name': player.get('first_name', ''),
            'Last_Name': player.get('last_name', ''),
            'Full_Name': player.get('full_name', ''),
            'Jersey_Number': player.get('jersey', ''),
            'Date_of_Birth': parse_date(player.get('dob', '')),
            'Birth_Place': player.get('birth_place', ''),
            'Height': player.get('height', ''),
            'Weight': player.get('weight', ''),
            'Bats_Throws': player.get('bats_throws', ''),
            'College': player.get('college', ''),
            'Debut_Year': player.get('debut_year', ''),
            'Active_Status': 1 if player.get('active', False) else 0,
            'Draft_Info': player.get('draft', ''),
            'Team_ID': player['team']['id'] if player.get('team') else '',
            'Position_ID': position_id
        })

    # Write to CSV
    filename = f"{OUTPUT_DIR}/players.csv"
    fieldnames = ['Player_ID', 'First_Name', 'Last_Name', 'Full_Name', 'Jersey_Number',
                  'Date_of_Birth', 'Birth_Place', 'Height', 'Weight', 'Bats_Throws',
                  'College', 'Debut_Year', 'Active_Status', 'Draft_Info', 'Team_ID', 'Position_ID']

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(player_rows)

    print(f"✅ Saved {len(player_rows)} active players to {filename}")
    return active_players


def extract_games_2024() -> tuple:
    """Extract 2024 season games and game statistics"""
    print("\n" + "="*60)
    print("📊 Extracting 2024 GAMES data")
    print("="*60)

    # Fetch games for 2024 season
    games = fetch_all_pages("games", {'season': 2024})

    # Transform for Game CSV
    game_rows = []
    game_stats_rows = []
    game_stats_id = 1

    for game in games:
        # Game table row
        game_rows.append({
            'Game_ID': game['id'],
            'Game_Date': parse_datetime(game.get('date', '')),
            'Season': game.get('season', 2024),
            'Home_Team_ID': game['home_team']['id'] if game.get('home_team') else '',
            'Away_Team_ID': game['away_team']['id'] if game.get('away_team') else '',
            'Venue': game.get('venue', ''),
            'Attendance': game.get('attendance', ''),
            'Postseason_Flag': 1 if game.get('postseason', False) else 0,
            'Game_Status': game.get('status', '')
        })

        # Game_Statistics rows (home team)
        if game.get('home_team_data'):
            htd = game['home_team_data']
            game_stats_rows.append({
                'Game_Stats_ID': game_stats_id,
                'Game_ID': game['id'],
                'Team_ID': game['home_team']['id'],
                'Is_Home_Team': 1,
                'Runs': htd.get('runs', 0),
                'Hits': htd.get('hits', 0),
                'Errors': htd.get('errors', 0),
                'Inning_Scores': json.dumps(htd.get('inning_scores', []))
            })
            game_stats_id += 1

        # Game_Statistics rows (away team)
        if game.get('away_team_data'):
            atd = game['away_team_data']
            game_stats_rows.append({
                'Game_Stats_ID': game_stats_id,
                'Game_ID': game['id'],
                'Team_ID': game['away_team']['id'],
                'Is_Home_Team': 0,
                'Runs': atd.get('runs', 0),
                'Hits': atd.get('hits', 0),
                'Errors': atd.get('errors', 0),
                'Inning_Scores': json.dumps(atd.get('inning_scores', []))
            })
            game_stats_id += 1

    # Write Games CSV
    game_filename = f"{OUTPUT_DIR}/games.csv"
    game_fieldnames = ['Game_ID', 'Game_Date', 'Season', 'Home_Team_ID', 'Away_Team_ID',
                       'Venue', 'Attendance', 'Postseason_Flag', 'Game_Status']

    with open(game_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=game_fieldnames)
        writer.writeheader()
        writer.writerows(game_rows)

    print(f"✅ Saved {len(game_rows)} games to {game_filename}")

    # Write Game_Statistics CSV
    stats_filename = f"{OUTPUT_DIR}/game_statistics.csv"
    stats_fieldnames = ['Game_Stats_ID', 'Game_ID', 'Team_ID', 'Is_Home_Team',
                        'Runs', 'Hits', 'Errors', 'Inning_Scores']

    with open(stats_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=stats_fieldnames)
        writer.writeheader()
        writer.writerows(game_stats_rows)

    print(f"✅ Saved {len(game_stats_rows)} game statistics to {stats_filename}")

    return games, game_stats_rows


def main():
    """Main execution function"""
    import os

    print("="*60)
    print("🏀 IS441 Baseball Database - Data Extraction")
    print("="*60)
    print(f"API: {BASE_URL}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Rate Limit: {60 / RATE_LIMIT_DELAY:.1f} requests per minute")
    print("="*60)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Extract all data
    start_time = time.time()

    teams = extract_teams()
    players = extract_players()
    games, game_stats = extract_games_2024()

    elapsed = time.time() - start_time

    # Summary
    print("\n" + "="*60)
    print("📈 EXTRACTION SUMMARY")
    print("="*60)
    print(f"  Teams: {len(teams)}")
    print(f"  Active Players: {len(players)}")
    print(f"  2024 Games: {len(games)}")
    print(f"  Game Statistics: {len(game_stats)}")
    print(f"\n  Total Time: {elapsed/60:.1f} minutes")
    print(f"  CSV files saved to: {OUTPUT_DIR}/")
    print("="*60)
    print("\n✅ Data extraction complete!")
    print("\nNext Steps:")
    print("  1. Review CSV files for data quality")
    print("  2. Import CSV files into Microsoft Access")
    print("  3. Verify foreign key relationships")
    print("  4. Begin SQL query development")


if __name__ == "__main__":
    main()
