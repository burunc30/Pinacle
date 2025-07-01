import requests
import json

def main():
    url = "https://www.nesine.com/Iddaa/MatchList/Popular"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }

    print("🔗 API-yə sorğu göndərilir:", url)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        matches = data.get("data", {}).get("matches", [])
        print(f"📦 Tapılan oyun sayı: {len(matches)}")

        for match in matches[:10]:
            home_team = match.get("homeTeamName")
            away_team = match.get("awayTeamName")
            match_time = match.get("matchDate")
            print(f"\n⏰ {match_time}")
            print(f"⚽ {home_team} vs {away_team}")

            for market in match.get("markets", []):
                if market.get("ocGroup") == "MS":  # 1X2
                    print("🔢 Nəticə (1X2):")
                    for oc in market.get("ocs", []):
                        print(f"   • {oc['oc']} → {oc['ocRate']}")
                if market.get("ocGroup") == "ALTÜST25":  # Over/Under 2.5
                    print("📊 Over/Under 2.5:")
                    for oc in market.get("ocs", []):
                        print(f"   • {oc['oc']} → {oc['ocRate']}")

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    main()
