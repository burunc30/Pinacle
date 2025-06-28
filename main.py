import requests
from bs4 import BeautifulSoup
import re

url = "https://en.betway.co.tz/sport/soccer?sortOrder=League&fromStartEpoch=1751054400&toStartEpoch=1751140799"
print(f"🔗 Sayta daxil olunur: {url}")

try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print("✅ HTML alındı.")
except Exception as e:
    print(f"❌ Xəta baş verdi: {e}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
title = soup.title.string.strip() if soup.title else "Başlıq tapılmadı"
print(f"ℹ️ Səhifə Başlığı: {title}")

texts = soup.stripped_strings
text_list = list(texts)
print(f"🔢 Tapılan yazı sayı: {len(text_list)}")

# Əmsal tapmaq üçün regex
odds = re.findall(r"\d+\.\d{1,2}", response.text)
print(f"🎯 Tapılan əmsal sayı: {len(odds)}")
for odd in odds[:10]:  # Yalnız ilk 10 əmsalı göstər
    print(f"• {odd}")
