import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.nesine.com/iddaa?et=1&ocg=MS-2%2C5&gt=Pop%C3%BCler"
    print("🔗 Sayta daxil olunur:", url)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(4000)

        print("✅ HTML alındı.")

        # Oyun bloklarını tap
        game_rows = page.locator("div[id^='bet-container']")
        count = await game_rows.count()
        print(f"📦 Tapılan oyun sayı: {count}")

        for i in range(min(10, count)):
            game = game_rows.nth(i)

            try:
                teams = await game.locator(".market-group-container .mbln-tbl .row .col.col-2").all_inner_texts()
                odds = await game.locator(".mbln-tbl .odd-button span").all_inner_texts()

                team_names = [t for t in teams if "-" in t]
                if team_names:
                    print(f"\n🏟️ Oyun: {team_names[0]}")
                else:
                    print("\n🏟️ Oyun: (Komandalar tapılmadı)")

                # Əmsalların çıxarılması
                if len(odds) >= 5:
                    print(f"   1X2: 1={odds[0]}  X={odds[1]}  2={odds[2]}")
                    print(f"   Over 2.5: {odds[3]}   Under 2.5: {odds[4]}")
                else:
                    print("   ❌ Əmsallar tam deyil")

            except Exception as e:
                print("   ⚠️ Xəta:", e)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
