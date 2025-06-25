import time
from playwright.sync_api import sync_playwright

def scrape_pinnacle():
    print("🔗 Sayta daxil olunur...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Yeni səhifə aç
        page = context.new_page()

        # Pinnacle saytında yalnız futbol üçün odds səhifəsi
        url = "https://www.pinnacle.com/en/odds/soccer"
        page.goto(url)

        time.sleep(10)  # Saytın JS ilə tam yüklənməsi üçün

        print("✅ HTML alındı.")

        # Səhifə başlığını çıxar
        title = page.title()
        print(f"ℹ️ Səhifə Başlığı: {title}")

        # Bütün div-ləri tap
        divs = page.query_selector_all("div")
        print(f"🔢 Tapılan DIV sayı: {len(divs)}")

        # İlk 10 div-in textlərini göstər
        for i, div in enumerate(divs[:10]):
            text = div.inner_text().strip()
            print(f"{i+1}. {text}")

        browser.close()

if __name__ == "__main__":
    scrape_pinnacle()
