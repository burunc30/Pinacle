from playwright.sync_api import sync_playwright

def run():
    url = "https://www.betexplorer.com/next/soccer/"
    print(f"🔗 Sayta daxil olunur: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Səhifənin tam yüklənməsini gözləyirik
        page.wait_for_load_state("networkidle")

        # Matç linklərini tapırıq
        rows = page.query_selector_all("a[href*='/match/']")
        print(f"📦 Tapılan sətir sayı: {len(rows)}")

        for row in rows:
            print(row.inner_text())

        browser.close()

if __name__ == "__main__":
    run()
