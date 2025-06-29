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
            await page.wait_for_timeout(6000)

            html = await page.content()
            print("✅ HTML alındı.")

            title = await page.title()
            print(f"ℹ️ Səhifə Başlığı: {title}")

            # Komanda adlarını çıxarmağa çalışırıq
            text_elements = await page.locator("div, span, a, button").all_inner_texts()
            team_names = [t.strip() for t in text_elements if "-" in t and len(t.strip()) < 50]

            if team_names:
                print("⚽ Tapılan komanda adları:")
                for name in team_names[:10]:
                    print("•", name)
            else:
                print("⚠️ Komanda adı tapılmadı.")

            # Əmsallar (rəqəmlər) çıxarılır
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
