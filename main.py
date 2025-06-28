import asyncio
from playwright.async_api import async_playwright
import re

async def run():
    print("🔗 Sayta daxil olunur: https://www.188bet.com/en/sports")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://www.188bet.com/en/sports", timeout=60000)
            await page.wait_for_timeout(10000)
            print("✅ HTML alındı.")
            print(f"ℹ️ Səhifə Başlığı: {await page.title()}")

            # Sayfadaki bütün yazılı mətnləri topla
            texts = await page.eval_on_selector_all(
                "*",
                "els => els.map(el => el.innerText).filter(t => t && t.trim().length > 0)"
            )

            odds_pattern = re.compile(r"\b\d+\.\d{1,2}\b")  # 1.25, 3.75 kimi
            found_odds = set()

            for text in texts:
                matches = odds_pattern.findall(text)
                for match in matches:
                    found_odds.add(match)

            print(f"🔢 Tapılan əmsal sayı: {len(found_odds)}")
            for odd in sorted(found_odds):
                print("•", odd)

            await browser.close()

    except Exception as e:
        print(f"❌ Xəta baş verdi: {e}")

asyncio.run(run())
