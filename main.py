import time
from playwright.sync_api import sync_playwright

def scrape_pinnacle_highlights():
    print("🔗 Sayta daxil olunur...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        url = "https://www.pinnacle.com/en/soccer/matchups/highlights/"
        page.goto(url)

        time.sleep(10)  # Sayt JS ilə yüklənsin deyə gözləyirik

        print("✅ HTML alındı.")
        print(f"ℹ️ Səhifə Başlığı: {page.title()}")

        # Ən çox matç məlumatı olan elementləri tapmağa çalışırıq
        match_blocks = page.query_selector_all("div.style_row__")
        print(f"🔢 Tapılan matç bloklarının sayı: {len(match_blocks)}")

        for i, match in enumerate(match_blocks[:10]):
            text = match.inner_text().strip()
            print(f"{i+1}. {text}")

        browser.close()

if __name__ == "__main__":
    scrape_pinnacle_highlights()
