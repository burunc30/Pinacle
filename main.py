from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)  # ✅ Xətasız headless rejim
    context = browser.new_context()
    page = context.new_page()

    print("🔗 Sayta daxil olunur...")
    page.goto("https://www.nesine.com/iddaa?et=1&ocg=MS-2%2C5&gt=Pop%C3%BCler", timeout=60000)
    page.wait_for_timeout(5000)

    games = page.query_selector_all("tr.mbln-tbl-row")
    print(f"📦 Tapılan oyun sayı: {len(games)}")

    for game in games:
        try:
            teams = game.query_selector(".mbln-tbl-t1-t2").inner_text().strip()
            odds = game.query_selector_all(".mbln-tbl-odd")
            if len(odds) >= 5:
                odd_1 = odds[0].inner_text().strip()
                odd_x = odds[1].inner_text().strip()
                odd_2 = odds[2].inner_text().strip()
                under_2_5 = odds[3].inner_text().strip()
                over_2_5 = odds[4].inner_text().strip()
                print(f"\n🏟️ Oyun: {teams}")
                print(f"➡️ 1X2: {odd_1} / {odd_x} / {odd_2}")
                print(f"⚽ Under 2.5: {under_2_5} | Over 2.5: {over_2_5}")
        except:
            continue

    browser.close()

with sync_playwright() as p:
    run(p)
