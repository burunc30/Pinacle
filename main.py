import requests
from bs4 import BeautifulSoup

url = "https://www.betexplorer.com/soccer/"
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
    teams = row.select_one(".table-participant")
    odds = row.select(".odds-nowrp")

    if teams and len(odds) >= 3:
        home_vs_away = teams.text.strip()
        odd1 = odds[0].text.strip()
        oddx = odds[1].text.strip()
        odd2 = odds[2].text.strip()

        print(f"⚽ {home_vs_away} → 1: {odd1}, X: {oddx}, 2: {odd2}")
