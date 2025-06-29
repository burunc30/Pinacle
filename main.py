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
            print("✅ HTML alındı.")

            title = await page.title()
            print(f"ℹ️ Səhifə Başlığı: {title}")

            # Bütün linkləri tap
            anchors = await page.locator("a").all()
            found = False
            print("🔍 Tapılan linklər və başlıqlar:")
            for i, a in enumerate(anchors[:50]):
                href = await a.get_attribute("href")
                text = await a.inner_text()
                if href:
                    print(f"{i+1}. [{text.strip()}]({href})")
                    found = True

            if not found:
                print("⚠️ Heç bir link tapılmadı.")

            await browser.close()

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
