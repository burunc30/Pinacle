import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.betexplorer.com/next/soccer/"
    print(f"🔗 Sayta daxil olunur: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        ))
        page = await context.new_page()
        await page.goto(url)
        
        # Bütün sorğuların tamamlanmasını gözlə
        await page.wait_for_load_state("networkidle")
        
        # Cədvəl elementlərini tap
        rows = await page.query_selector_all(".table-main tr")
        print(f"📦 Tapılan sətir sayı: {len(rows)}")

        for row in rows:
            team_cell = await row.query_selector(".table-participant a")
            time_cell = await row.query_selector(".table-time")
            odds_cells = await row.query_selector_all(".odds-nowrp")

            if team_cell and len(odds_cells) >= 3:
                match_name = (await team_cell.inner_text()).strip()
                match_time = (await time_cell.inner_text()).strip() if time_cell else "N/A"
                odd1 = (await odds_cells[0].inner_text()).strip()
                oddx = (await odds_cells[1].inner_text()).strip()
                odd2 = (await odds_cells[2].inner_text()).strip()

                print(f"⚽ {match_time} | {match_name} → 1: {odd1}, X: {oddx}, 2: {odd2}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
