import asyncio
from playwright.async_api import async_playwright

async def run():
    url = "https://en.betway.co.tz/sport/soccer?sortOrder=League&fromStartEpoch=1751054400&toStartEpoch=1751140799"
    print(f"🔗 Sayta daxil olunur: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(8000)

        print("✅ HTML alındı.")

        # Komanda adlarını daha ümumi formada axtar
        texts = await page.locator("text=/.* - .*/").all_text_contents()
        if texts:
            print("⚽ Tapılan komanda adları:")
            for t in texts:
                print("•", t.strip())
        else:
            print("⚠️ Komanda adı tapılmadı.")

        # Əmsalları tapmağa çalış: sadəcə görünən rəqəmlər (0.1 - 100 aralığında)
        raw_texts = await page.locator("body").all_text_contents()
        odds = []
        for block in raw_texts:
            for part in block.split():
                try:
                    val = float(part.strip())
                    if 0.1 <= val <= 100.0:
                        odds.append(val)
                except:
                    continue

        if odds:
            print(f"🎯 Tapılan əmsal sayı: {len(odds)}")
            for o in odds[:20]:
                print("•", o)
        else:
            print("⚠️ Heç bir əmsal tapılmadı.")

        await browser.close()

asyncio.run(run())
