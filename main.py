import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.misli.az/idman-novleri/futbol"
    print("🔗 Sayta daxil olunur:", url)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(5000)
            await page.mouse.wheel(0, 10000)
            await page.wait_for_timeout(3000)

            print("✅ Sayt yükləndi və scroll edildi.")

            full_text = await page.content()

            # Tapılan bütün mətnlər
            texts = await page.locator("div").all_inner_texts()
            match_lines = [t.strip() for t in texts if any(word in t for word in ["1", "X", "2"]) and len(t.strip()) > 10]

            print("\n📋 Tapılan Matçlar və Əmsallar:")
            for line in match_lines[:10]:
                print("—", line)

            # Over/Under (Alt/Üst) əmsallarını ara
            ou_lines = [t.strip() for t in texts if "Over" in t or "Under" in t or "Üst" in t or "Alt" in t]
            if ou_lines:
                print("\n⚽ Over/Under bölmələri:")
                for line in ou_lines[:10]:
                    print("•", line)
            else:
                print("⚠️ Over/Under tapılmadı.")

            await browser.close()

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
