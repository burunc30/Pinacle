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

            html = await page.content()
            print("✅ HTML alındı.")

            # Səhifə başlığı
            title = await page.title()
            print(f"ℹ️ Səhifə Başlığı: {title}")

            # Komanda adlarını tap (Team A - Team B formatı)
            full_text = await page.locator("body").all_text_contents()
            teams = []
            for block in full_text:
                lines = block.split('\n')
                for line in lines:
                    line = line.strip()
                    if " - " in line and len(line) < 50 and all(x.isalpha() or x in " -'&" for x in line.replace(" - ", "")):
                        teams.append(line)

            if teams:
                print("⚽ Tapılan komanda adları:")
                for t in teams:
                    print("•", t)
            else:
                print("⚠️ Komanda adı tapılmadı.")

            # Əmsalları tap
            odds_matches = re.findall(r"\d+\.\d+", html)
            if odds_matches:
                print("🎯 Tapılan əmsal sayı:", len(odds_matches))
                for o in odds_matches[:15]:  # çoxdursa ilk 15-i göstər
                    print("•", o)
            else:
                print("❌ Əmsal tapılmadı.")

            await browser.close()

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
