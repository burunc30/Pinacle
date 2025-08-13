import requests
from bs4 import BeautifulSoup

url = "https://www.betexplorer.com/next/soccer/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

print(f"🔗 Sayta daxil olunur: {url}")
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("❌ Sayta daxil olmaq mümkün olmadı.")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
matches = soup.select(".table-main tr")

print(f"📦 Tapılan sətir sayı: {len(matches)}")

for row in matches:
    team_cell = row.select_one(".table-participant a")
    time_cell = row.select_one(".table-time")
    odds_cells = row.select(".odds-nowrp")

    if team_cell and len(odds_cells) >= 3:
        match_name = team_cell.text.strip()
        match_time = time_cell.text.strip() if time_cell else "N/A"
        odd1 = odds_cells[0].text.strip()
        oddx = odds_cells[1].text.strip()
        odd2 = odds_cells[2].text.strip()

        print(f"⚽ {match_time} | {match_name} → 1: {odd1}, X: {oddx}, 2: {odd2}")
