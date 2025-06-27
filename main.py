import requests
from bs4 import BeautifulSoup

# Saytların siyahısı
urls = {
    "pinnacle": "https://www.pinnacle.com/en/soccer/matchups/highlights/",
    "betfair": "https://www.betfair.com/sport/football",
    "williamhill": "https://sports.williamhill.com/betting/en-gb/football",
    "1xbet": "https://1xbet.com/en/line/Football/",
    "10bet": "https://www.10bet.com/sports/soccer/",
}

# Aktiv sayt adı (buranı dəyişməklə başqa sayt yoxlaya bilərsən)
active = "betfair"  # məsələn: "pinnacle", "1xbet", "williamhill"

# URL seç
url = urls.get(active)
print(f"🔗 Sayta daxil olunur: {url}")

try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    print("✅ HTML alındı.")

    # HTML analiz
    soup = BeautifulSoup(response.text, "html.parser")

    print(f"ℹ️ Səhifə Başlığı: {soup.title.string if soup.title else 'Tapılmadı'}")

    # Sadə blokların sayı (məsələn div, section və s.)
    divs = soup.find_all("div")
    print(f"🔢 Tapılan DIV sayı: {len(divs)}")

    # Test məqsədilə ilk 5 div içindəkini göstər
    for i, div in enumerate(divs[:5]):
        text = div.get_text(strip=True)
        print(f"{i+1}. {text[:300]}...")  # 300 simvoldan çox göstərməsin

except Exception as e:
    print(f"❌ Xəta baş verdi: {e}")
