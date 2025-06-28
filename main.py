import asyncio
from playwright.async_api import async_playwright
import re

async def run():
    url = "https://www.188bet.com/en/sports/soccer/highlights"
    print(f"🔗 Sayta daxil olunur: {url}")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(10000)
            print("✅ HTML alındı.")
            print(f"ℹ️ Səhifə Başlığı: {await page.title()}")

            # Bütün yazıları topla
            texts = await page.eval_on_selector_all(
                "*",
                "els => els.map(el => el.innerText).filter(t => t && t.trim().length > 0)"
            )

            print(f"🔢 Tapılan yazı sayı: {len(texts)}")

            # Sadəcə ilk 10 yazını göstər
            for i, t in enumerate(texts[:10], 1):
                print(f"{i}. {t.strip()[:80]}...")

            # Əmsalları axtar
            odds_pattern = re.compile(r"\b\d+\.\d{1,2}\b")
            found_odds = set()

            for text in texts:
                matches = odds_pattern.findall(text)
                for match in matches:
                    if 1.01 <= float(match) <= 10.0:  # Əmsal aralığı
                        found_odds.add(match)

            print(f"🎯 Tapılan əmsal sayı: {len(found_odds)}")
            for odd in sorted(found_odds):
                print("•", odd)

            await browser.close()

    except Exception as e:
        print(f"❌ Xəta baş verdi: {e}")

asyncio.run(run())
