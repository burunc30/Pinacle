import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.misli.az/idman-novleri/futbol"
    print("🔗 Sayta daxil olunur:", url)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)  # dəyişiklik burada
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(5000)  # 5 saniyə gözlə

            await page.mouse.wheel(0, 10000)  # scroll aşağı
            await page.wait_for_timeout(3000)

            print("✅ Scroll və gözləmə tamamlandı.")

            divs = await page.locator("div").all_inner_texts()
            print(f"🔢 Tapılan div sayı: {len(divs)}")

            for i, div in enumerate(divs[:30]):
                print(f"{i+1}. {div.strip()}")

            await browser.close()

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
