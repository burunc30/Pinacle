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
        await page.wait_for_timeout(5000)  # daha çox gözləyək ki, elementlər yüklənsin

        print("✅ HTML alındı.")

        # Bütün oyun satırları
        games = page.locator("div[data-event-name]")
        count = await games.count()
        print(f"📦 Tapılan oyun sayı: {count}")

        for i in range(min(count, 10)):
            row = games.nth(i)
            try:
                team_name = await row.get_attribute("data-event-name")
                odds = await row.locator(".outcome-button__odd").all_inner_texts()

                print(f"\n🏟️ Oyun: {team_name}")
                if len(odds) >= 5:
                    print(f"   1X2: 1={odds[0]}  X={odds[1]}  2={odds[2]}")
                    print(f"   Over 2.5: {odds[3]}  Under 2.5: {odds[4]}")
                else:
                    print("   ⚠️ Əmsallar natamam və ya tapılmadı")

            except Exception as e:
                print("   ❌ Xəta:", e)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
