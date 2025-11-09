#!/usr/bin/env python3
"""
IS441 Baseball Database Project - API Explorer
Explores Ball Don't Lie MLB API to understand available data for database design
"""

import requests
import json
import time

API_KEY = "e8b6410a-dd6e-4819-9e1c-7ae21f885609"
BASE_URL = "https://api.balldontlie.io/mlb/v1"
HEADERS = {"Authorization": API_KEY}

def make_request(endpoint, params=None):
    """Make API request with rate limiting"""
    url = f"{BASE_URL}/{endpoint}"
    time.sleep(2)  # Avoid rate limiting (5 req/min = 12 sec between requests)

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}
    except Exception as e:
        return {"error": str(e)}

def explore_endpoints():
    """Test various endpoints to see what data is available"""

    endpoints_to_test = [
        ("teams", {}),
        ("players", {"per_page": 2}),
        ("games", {"per_page": 2}),
        ("stats", {"per_page": 2}),
        ("stats/players", {"per_page": 2}),
    ]

    results = {}

    for endpoint, params in endpoints_to_test:
        print(f"\n{'='*60}")
        print(f"Testing endpoint: /{endpoint}")
        print(f"{'='*60}")

        data = make_request(endpoint, params)
        results[endpoint] = data

        if "error" in data:
            print(f"❌ Error: {data}")
        else:
            print(f"✅ Success!")
            if "data" in data and len(data["data"]) > 0:
                print(f"   Sample record keys: {list(data['data'][0].keys())}")
                print(f"   Total records returned: {len(data['data'])}")
                if "meta" in data:
                    print(f"   Meta: {data['meta']}")

    return results

def analyze_player_fields():
    """Analyze player data structure for database design"""
    print("\n" + "="*60)
    print("PLAYER DATA STRUCTURE ANALYSIS")
    print("="*60)

    data = make_request("players", {"per_page": 5})

    if "data" in data and len(data["data"]) > 0:
        player = data["data"][0]

        print("\n📊 Available Player Fields:")
        print("-" * 60)
        for key, value in player.items():
            if isinstance(value, dict):
                print(f"  {key}: (nested object)")
                for sub_key in value.keys():
                    print(f"    - {sub_key}")
            else:
                print(f"  {key}: {type(value).__name__}")

        return player

    return None

def analyze_team_structure():
    """Analyze team data structure"""
    print("\n" + "="*60)
    print("TEAM DATA STRUCTURE ANALYSIS")
    print("="*60)

    data = make_request("teams", {})

    if "data" in data:
        print(f"\n✅ Total MLB Teams: {len(data['data'])}")

        # Group by league
        leagues = {}
        for team in data["data"]:
            league = team.get("league")
            if league not in leagues:
                leagues[league] = []
            leagues[league].append(team["abbreviation"])

        for league, teams in leagues.items():
            print(f"\n  {league} League: {len(teams)} teams")
            print(f"    {', '.join(sorted(teams))}")

        return data["data"]

    return None

if __name__ == "__main__":
    print("🔍 IS441 Baseball Database - API Data Explorer")
    print("=" * 60)

    # Explore all endpoints
    results = explore_endpoints()

    # Analyze specific structures
    player_structure = analyze_player_fields()
    team_structure = analyze_team_structure()

    # Save results
    print("\n" + "="*60)
    print("💾 Saving results to api_exploration_results.json")
    print("="*60)

    output = {
        "endpoints": results,
        "player_sample": player_structure,
        "teams": team_structure
    }

    with open("api_exploration_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print("✅ Done! Check api_exploration_results.json for full results")
