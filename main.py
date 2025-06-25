from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def run_scraper():
    url = "https://www.pinnacle.com/en/sports"  # əsas səhifə, sonra dəqiqləşdirəcəyik
    print("🔗 Sayta daxil olunur...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        html = page.content()
        print("✅ HTML alındı.")

        # Saytın başlığını yoxla
        print("ℹ️ Səhifə Başlığı:", page.title())

        # BeautifulSoup ilə test
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')
        print(f"🔍 Tapılan link sayı: {len(links)}")

        # İlk 10 linki göstər
        for i, a in enumerate(links[:10]):
            text = a.get_text(strip=True)
            href = a.get('href')
            print(f"{i+1}. {text} -> {href}")

        browser.close()

if __name__ == "__main__":
    run_scraper()
