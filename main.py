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

            # Oyun linklərini topla
            links = await page.locator("a").all()
            game_links = []

            for link in links:
                href = await link.get_attribute("href")
                if href and "/idman-novleri/futbol/" in href and "canli" not in href:
                    if href.startswith("/"):
                        full_url = "https://www.misli.az" + href
                    else:
                        full_url = href
                    game_links.append(full_url)

            if game_links:
                print("🎯 Tapılan oyun linkləri:")
                for i, game in enumerate(game_links[:10]):
                    print(f"{i+1}. {game}")
            else:
                print("⚠️ Heç bir oyun linki tapılmadı.")

            await browser.close()

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
