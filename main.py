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

            # Komanda adlarını tapmağa çalış
            event_names = await page.locator('[data-testid="event-title"]').all_inner_texts()
            if not event_names:
                event_names = await page.locator('.event-name, .match-row, .title, .fixture, .match-title, .name').all_inner_texts()

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

            # 🔍 Daha geniş selector-larla class-ları araşdır
            tag_names = ["div", "span", "a", "li", "section", "article"]
            unique_classes = set()
            total_found = 0

            for tag in tag_names:
                elements = await page.locator(tag).all()
                total_found += len(elements)
                for el in elements:
                    class_attr = await el.get_attribute("class")
                    if class_attr:
                        for cls in class_attr.split():
                            unique_classes.add(cls)

            print(f"🔢 Tapılan element sayı: {total_found}")
            print("🔍 Tapılan unikal class-lar (ilk 30):")
            for cls in list(unique_classes)[:30]:
                print("-", cls)

            await browser.close()

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
