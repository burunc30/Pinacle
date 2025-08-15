import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.betexplorer.com/next/soccer/"
    print(f"🔗 Sayta daxil olunur: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)

        # BetExplorer-də oyunların olduğu elementlər yeni strukturdadır
        await page.wait_for_selector("div.eventRow", timeout=20000)

        matches = await page.query_selector_all("div.eventRow")

        print(f"📦 Tapılan sətir sayı: {len(matches)}")

        for match in matches:
            try:
                teams = await match.query_selector("a.eventRow__name")
                teams_text = await teams.inner_text() if teams else "???"

                time_el = await match.query_selector("span.eventRow__time")
                match_time = await time_el.inner_text() if time_el else "???"

                print(f"🕒 {match_time} | ⚽ {teams_text}")
            except Exception as e:
                print(f"Xəta: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
