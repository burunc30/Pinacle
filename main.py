import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    url = "https://www.misli.com/spor/futbol"
    print("🔗 Sayta daxil olunur:", url)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(locale="tr-TR")
            page = await context.new_page()

            await page.goto(url, timeout=90000)
            await page.wait_for_timeout(5000)  # Sayt tam yüklənsin deyə

            html = await page.content()
            print("✅ HTML alındı.")

            title = await page.title()
            print(f"ℹ️ Səhifə Başlığı: {title}")

            # Komanda adlarını tapmağa çalışırıq
            team_names = await page.locator('div.match-info').all_inner_texts()
            if team_names:
                print("⚽ Tapılan komanda adları:")
                for team in team_names[:10]:  # ilk 10-u göstər
                    print("•", team.strip())
            else:
                print("⚠️ Komanda adı tapılmadı.")

            # Əmsalları çıxarırıq
            odds = re.findall(r"\d+\.\d+", html)
            if odds:
                print("🎯 Tapılan əmsal sayı:", len(odds))
                for o in odds[:15]:
                    print("•", o)
            else:
                print("❌ Əmsal tapılmadı.")

            await browser.close()

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
