import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    url = "https://www.misli.az/idman-novleri/futbol"
    print("🔗 Sayta daxil olunur:", url)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(5000)  # JS yüklənməsi üçün gözləyir

            html = await page.content()
            print("✅ HTML alındı.")

            title = await page.title()
            print(f"ℹ️ Səhifə Başlığı: {title}")

            # Yalnız görünən yazılar
            text_elements = await page.locator("div, span, a").all_inner_texts()
            print("🔍 Tapılan yazılar (ilk 30):")
            for i, t in enumerate(text_elements[:30]):
                print(f"{i+1}.", t.strip())

            # Komanda adları ehtimalı olan sətirlər
            teams = [t.strip() for t in text_elements if "-" in t and len(t.strip()) < 50]
            if teams:
                print("⚽ Tapılan komanda adları:")
                for team in teams:
                    print("•", team)
            else:
                print("⚠️ Komanda adı tapılmadı.")

            # Əmsallar
            odds = re.findall(r"\d+\.\d+", html)
            print("🎯 Tapılan əmsal sayı:", len(odds))
            for o in odds[:15]:
                print("•", o)

            await browser.close()

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
