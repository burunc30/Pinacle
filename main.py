from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def run_scraper():
    url = "https://www.pinnacle.com/en/odds/matchups"
    print("🔗 Sayta daxil olunur...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        time.sleep(7)  # saytin JS ilə yüklənməsi üçün

        html = page.content()
        print("✅ HTML alındı.")
        print("ℹ️ Səhifə Başlığı:", page.title())

        soup = BeautifulSoup(html, 'html.parser')

        # Sadəcə yoxlama üçün ilk 10 <div> və ya <span> tipli blokları göstər
        divs = soup.find_all("div")
        print(f"🔢 Tapılan DIV sayı: {len(divs)}")

        for i, div in enumerate(divs[:10]):
            text = div.get_text(strip=True)
            print(f"{i+1}. {text}")

        browser.close()

if __name__ == "__main__":
    run_scraper()
