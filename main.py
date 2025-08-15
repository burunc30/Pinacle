import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.betexplorer.com/next/soccer/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # headless=False açıq görmək üçün
        page = await browser.new_page()
        print(f"🔗 Sayta daxil olunur: {url}")
        await page.goto(url, timeout=60000)
        
        try:
            await page.wait_for_selector(".table-main", timeout=30000)
            print("✅ Selector tapıldı!")
        except:
            print("❌ Selector tapılmadı! HTML çıxarılır...")
            html = await page.content()
            with open("betexplorer_debug.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("📄 HTML faylı 'betexplorer_debug.html' kimi saxlanıldı.")

        await browser.close()

asyncio.run(main())
