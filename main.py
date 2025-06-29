import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    url = "https://en.betway.co.tz/sport/soccer?sortOrder=League&fromStartEpoch=1751054400&toStartEpoch=1751140799"
    print("🔗 Sayta daxil olunur:", url)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(6000)  # Yüklənməsi üçün 6 saniyə gözlə

            print("✅ HTML alındı.")
            title = await page.title()
            print(f"ℹ️ Səhifə Başlığı: {title}")

            # Komanda adları üçün potensial class-ları yoxla
            team_selectors = [
                '[data-testid="event-title"]',
                '.event-title', 
                '.event-name', 
                '.team-name', 
                '.participant__name', 
                '.market-name', 
                '.c-events-event-name__name'
            ]

            found_teams = []
            for selector in team_selectors:
                items = await page.locator(selector).all_inner_texts()
                if items:
                    found_teams.extend(items)

            if found_teams:
                print("⚽ Tapılan komanda adları:")
                for team in set(found_teams):
                    print("•", team.strip())
            else:
                print("⚠️ Komanda adı tapılmadı.")

            # Əmsalları tap
            html = await page.content()
            odds_matches = re.findall(r"\d+\.\d+", html)
            if odds_matches:
                print("🎯 Tapılan əmsal sayı:", len(odds_matches))
                for o in odds_matches[:15]:
                    print("•", o)
            else:
                print("❌ Əmsal tapılmadı.")

            await browser.close()

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
