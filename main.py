import requests
from bs4 import BeautifulSoup
import re

url = "https://en.betway.co.tz/sport/soccer?sortOrder=League&fromStartEpoch=1751054400&toStartEpoch=1751140799"

print(f"🔗 Sayta daxil olunur: {url}")
try:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    print("✅ HTML alındı.")
except Exception as e:
    print(f"❌ Xəta baş verdi: {e}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
print(f"ℹ️ Səhifə Başlığı: {soup.title.text.strip()}")

# Komanda adlarını çıxar
texts = soup.find_all(text=True)
teams = set()
for t in texts:
    if " v " in t or " vs " in t:
        teams.add(t.strip())

if teams:
    print(f"⚽ Tapılan komanda cütləri: {len(teams)}")
    for team in sorted(teams):
        print("•", team)
else:
    print("⚠️ Komanda adı tapılmadı.")

# Əmsalları çıxar
odds = []
for t in texts:
    found = re.findall(r"\b\d{1,3}\.\d{1,2}\b", t)
    for val in found:
        try:
            fval = float(val)
            if 1.01 <= fval <= 200:
                odds.append(fval)
        except:
            pass

if odds:
    print(f"🎯 Tapılan əmsal sayı: {len(odds)}")
    for o in odds[:20]:
        print("•", o)
else:
    print("⚠️ Əmsal tapılmadı.")
