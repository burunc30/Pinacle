import requests

def fetch_pinnacle_matchups():
    print("🔗 JSON API-yə sorğu göndərilir...")

    url = "https://www.pinnacle.com/en/api/matchups?sportId=29"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("✅ Məlumat alındı.")

        matches = data.get("highlights", [])
        print(f"🔢 Tapılan oyun sayı: {len(matches)}")

        for i, match in enumerate(matches[:10]):
            teams = match.get("participants", [])
            start_time = match.get("startTime")
            league = match.get("league", {}).get("name", "")
            print(f"{i+1}. {league} | {teams} | Start: {start_time}")
    else:
        print(f"❌ Sorğu uğursuz oldu. Status kod: {response.status_code}")

if __name__ == "__main__":
    fetch_pinnacle_matchups()
