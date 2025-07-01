import requests

def main():
    url = "https://www.nesine.com/Iddaa/MatchList/Popular"
    print("🔗 API-yə sorğu göndərilir:", url)

    try:
        response = requests.get(url)
        data = response.json()

        matches = data.get("data", {}).get("matches", [])
        print(f"📦 Tapılan oyun sayı: {len(matches)}")

        for match in matches[:10]:
            home_team = match.get("homeTeamName")
            away_team = match.get("awayTeamName")
            match_time = match.get("matchDate")
            odds = match.get("markets", [])

            print(f"⏰ {match_time}")
            print(f"⚽ {home_team} vs {away_team}")

            for market in odds:
                desc = market.get("ocGroup", "")
                selections = market.get("ocs", [])
                print(f"🎯 {desc}:")
                for sel in selections:
                    label = sel.get("oc")
                    value = sel.get("ocRate")
                    print(f"   • {label}: {value}")
            print("—" * 40)

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    main()
