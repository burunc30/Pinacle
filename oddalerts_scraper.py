from playwright.sync_api import sync_playwright
import json

def scrape_oddalerts():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://oddalerts.com/live")

        # Sayt yüklənənə qədər gözlə
        page.wait_for_selector("div.match-card", timeout=10000)

        matches = page.query_selector_all("div.match-card")
        result = []

        for match in matches:
            try:
                teams = match.query_selector("div.match-name").inner_text()
                btts = match.query_selector("div.market-btts span").inner_text()
                over25 = match.query_selector("div.market-over25 span").inner_text()

                result.append({
                    "match": teams,
                    "BTTS": btts,
                    "Over 2.5": over25
                })
            except:
                continue

        browser.close()
        return result

if __name__ == "__main__":
    data = scrape_oddalerts()
    print(json.dumps(data, indent=2))
