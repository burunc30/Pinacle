from playwright.sync_api import sync_playwright
import time

URL = "https://www.nesine.com/iddaa?et=1&ocg=MS-2%2C5&gt=Pop%C3%BCler"

def run(playwright):
    browser = playwright.chromium.launch(headless=False)  # Debug üçün headless False
    context = browser.new_context()
    page = context.new_page()
    
    print("🔗 Sayta daxil olunur...")
    page.goto(URL)
    page.wait_for_selector("tr[id^='match-row']", timeout=20000)  # Matçlar yüklənənə qədər gözlə

    rows = page.query_selector_all("tr[id^='match-row']")
    print(f"📦 Tapılan oyun sayı: {len(rows)}")

    for row in rows:
        try:
            time_elem = row.query_selector("td:nth-child(1) > div")
            teams_elem = row.query_selector("td:nth-child(2) > div")
            odds_elems = row.query_selector_all("td:nth-child(n+3):nth-child(-n+5) span")

            time_text = time_elem.inner_text().strip() if time_elem else "?"
            teams_text = teams_elem.inner_text().strip().replace("\n", " vs ") if teams_elem else "?"

            odds = [o.inner_text().strip() for o in odds_elems if o.inner_text().strip()]
            print(f"🕒 {time_text} | ⚽ {teams_text} | 🧮 Əmsallar: {odds}")
        except Exception as e:
            print(f"⚠️ Xəta: {e}")

    browser.close()


with sync_playwright() as p:
    run(p)
