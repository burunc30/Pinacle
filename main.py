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

            title = await page.title()
            print(f"ℹ️ Səhifə Başlığı: {title}")

            # Komanda adlarını tapmağa çalış — əvvəlki üsullar
            event_names = await page.locator('[data-testid="event-title"]').all_inner_texts()
            if not event_names:
                event_names = await page.locator('.event-name, .match-row').all_inner_texts()

            if event_names:
                print("⚽ Tapılan komanda adları:")
                for team in event_names:
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

            # 🔍 Unikal class-ların siyahısı
            all_divs = await page.locator('div').all()
            print(f"🔢 Tapılan DIV sayı: {len(all_divs)}")

            unique_classes = set()
            for div in all_divs:
                class_attr = await div.get_attribute("class")
                if class_attr:
                    for cls in class_attr.split():
                        unique_classes.add(cls)

            print("🔍 Tapılan unikal class-lar:")
            for cls in list(unique_classes)[:30]:  # ilk 30 class
                print("-", cls)

            await browser.close()

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
