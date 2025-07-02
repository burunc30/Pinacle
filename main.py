from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("🔗 Sayta daxil olunur...")
        page.goto("https://www.nesine.com/iddaa?et=1&ocg=MS-2%2C5&gt=Pop%C3%BCler")
        page.wait_for_timeout(15000)  # Dinamik datanın gəlməsi üçün 15 saniyə gözlə

        matches = page.query_selector_all("tr[id^='match-row']")

        if not matches:
            print("⚠️ Heç bir oyun tapılmadı.")
        else:
            print(f"📦 Tapılan oyun sayı: {len(matches)}")
            for match in matches:
                try:
                    teams = match.query_selector(".match-link").inner_text().strip()
                    odds = match.query_selector_all(".mbln-odds-column span")
                    odds_values = [o.inner_text().strip() for o in odds if o.inner_text().strip()]
                    print(f"⚽ {teams} | Əmsallar: {', '.join(odds_values)}")
                except:
                    continue

        browser.close()

if __name__ == "__main__":
    run()
