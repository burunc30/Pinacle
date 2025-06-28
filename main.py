import asyncio
from playwright.async_api import async_playwright

async def run():
    print("🔗 Sayta daxil olunur: https://www.188bet.com/en/sports")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://www.188bet.com/en/sports", timeout=60000)
            await page.wait_for_timeout(10000)  # 10 saniyə gözləyirik ki, dinamik kontent yüklənsin
            print("✅ HTML alındı.")
            print(f"ℹ️ Səhifə Başlığı: {await page.title()}")

            # Tapılan bütün div-lərin class adlarını çıxarır
            classes = await page.eval_on_selector_all(
                "div",
                "els => els.map(el => el.className).filter(Boolean)"
            )

            unique_classes = list(set(classes))
            print(f"🔍 Tapılan unikal class-lar ({len(unique_classes)}):")
            for cls in unique_classes[:15]:  # İlk 15-ni göstər
                print("-", cls)

            await browser.close()

    except Exception as e:
        print(f"❌ Xəta baş verdi: {e}")

asyncio.run(run())
