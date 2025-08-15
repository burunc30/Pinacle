from playwright.sync_api import sync_playwright

url = "https://www.betexplorer.com/next/soccer/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_selector(".table-main")

    matches = page.query_selector_all(".table-main tbody tr")
    print(f"📦 Tapılan oyun sayı: {len(matches)}")

    for match in matches:
        try:
            teams = match.query_selector(".table-participant").inner_text().strip()
            time = match.query_selector(".table-time").inner_text().strip()

            odds_cells = match.query_selector_all("td.odds-nowrp")
            odds = [cell.inner_text().strip() for cell in odds_cells]

            print(f"🏟 Oyun: {teams}")
            print(f"⏰ Vaxt: {time}")
            print(f"📊 Əmsallar: {odds}")
            print("-" * 40)
        except:
            continue

    browser.close()
