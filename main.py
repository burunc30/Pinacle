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
            await page.wait_for_timeout(5000)  # Dinamik yükləmə üçün gözləmə
            print("✅ HTML alındı.")

            title = await page.title()
            print(f"ℹ️ Səhifə Başlığı: {title}")

            # DOM üzərində görünən textləri al
            visible_text = await page.evaluate("""() => {
                return document.body.innerText;
            }""")

            # Komanda adlarını tapmağa cəhd (məsələn: "Team A vs Team B")
            matches = re.findall(r"[A-Za-z\s\.\-&]{2,} vs [A-Za-z\s\.\-&]{2,}", visible_text)
            if matches:
                print("⚽ Tapılan komanda adları:")
                for m in matches:
                    print("•", m.strip())
            else:
                print("⚠️ Komanda adı tapılmadı.")

            # Əmsalları HTML-dən tap
            html = await page.content()
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
