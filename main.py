import asyncio
from playwright.async_api import async_playwright

async def run():
    print("🔗 Sayta daxil olunur: https://www.10bet.com/sports")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto("https://www.10bet.com/sports", timeout=60000)
            await page.wait_for_timeout(5000)

            html = await page.content()
            print("✅ HTML alındı.")
            print(f"ℹ️ Səhifə Başlığı: {await page.title()}")

            # Burda test üçün neçə "div" var, onu sayırıq
            divs = await page.query_selector_all("div")
            print(f"🔢 Tapılan DIV sayı: {len(divs)}")

            await browser.close()
    except Exception as e:
        print(f"❌ Xəta baş verdi: {e}")

asyncio.run(run())
