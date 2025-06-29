import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    url = "https://www.misli.com/spor/futbol"
    print("🔗 Sayta daxil olunur:", url)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            html = await page.content()
            print("✅ HTML alındı.")

            title = await page.title()
            print(f"ℹ️ Səhifə Başlığı: {title}")

            # Bütün görünən yazıları çıxar
            text_elements = await page.locator("div, span, a, button").all_inner_texts()
            print("🔍 Tapılan yazılar (ilk 30):")
            for i, t in enumerate(text_elements[:30]):
                print(f"{i+1}.", t.strip())

            # Komanda adlarını tap (məs: "Galatasaray - Fenerbahçe")
            team_names = [t.strip() for t in text_elements if "-" in t and len(t.strip()) < 50]
            if team_names:
                print("⚽ Tapılan komanda adları:")
                for team in team_names:
                    print("•", team)
            else:
                print("⚠️ Komanda adı tapılmadı.")

            # Əmsalları tap
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
