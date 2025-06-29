import asyncio
from playwright.async_api import async_playwright

async def run():
    url = "https://en.betway.co.tz/sport/soccer?sortOrder=League&fromStartEpoch=1751054400&toStartEpoch=1751140799"
    print(f"🔗 Sayta daxil olunur: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(5000)  # JS elementlər tam yüklənsin deyə gözləyirik

        print("✅ HTML alındı.")

        # Komanda adları üçün axtarış (mümkün qədər ümumi variant seçilib)
        team_blocks = await page.locator("div:has-text('vs')").all_text_contents()
        if team_blocks:
            print("⚽ Tapılan komandalar:")
            for team in team_blocks:
                print("•", team.strip())
        else:
            print("⚠️ Komanda adı tapılmadı.")

        # Əmsallar üçün sadə filtr
        odds_raw = await page.locator("span").all_text_contents()
        odds = []
        for text in odds_raw:
            try:
                val = float(text.strip())
                if 0.1 <= val <= 100.0:  # Real əmsal aralığı
                    odds.append(val)
            except:
                continue

        print(f"🎯 Tapılan əmsal sayı: {len(odds)}")
        for o in odds[:20]:
            print("•", o)

        await browser.close()

asyncio.run(run())
