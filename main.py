import asyncio
from playwright.sync_api import sync_playwright
import re

def run():
    url = "https://en.betway.co.tz/sport/soccer?sortOrder=League&fromStartEpoch=1751054400&toStartEpoch=1751140799"
    print(f"🔗 Sayta daxil olunur: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)  # 5 saniyə gözləyir ki, bütün JS yüklənsin

        content = page.content()
        title = page.title()
        print(f"✅ HTML alındı.")
        print(f"ℹ️ Səhifə Başlığı: {title}")

        odds = re.findall(r"\d+\.\d{1,2}", content)
        print(f"🎯 Tapılan əmsal sayı: {len(odds)}")
        for odd in odds[:15]:
            print(f"• {odd}")

        browser.close()

if __name__ == "__main__":
    run()
