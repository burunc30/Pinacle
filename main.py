from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def run_scraper():
    url = "https://www.pinnacle.com/en/sports"  # əsas səhifə
    print("🔗 Sayta daxil olunur...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        # Yüklənməsi üçün vaxt ver
        time.sleep(5)  # 5 saniyə gözlə (lazım olsa 7-10 da olar)

        html = page.content()
        print("✅ HTML alındı.")
        print("ℹ️ Səhifə Başlığı:", page.title())

        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')
        print(f"🔍 Tapılan link sayı: {len(links)}")

        for i, a in enumerate(links[:10]):
            text = a.get_text(strip=True)
            href = a.get('href')
            print(f"{i+1}. {text} -> {href}")

        browser.close()

if __name__ == "__main__":
    run_scraper()
