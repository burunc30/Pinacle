import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    base_url = "https://www.misli.az/idman-novleri/futbol"
    print("🔗 Sayta daxil olunur:", base_url)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(base_url, timeout=60000)
            await page.wait_for_timeout(5000)

            # 1. Oyun bloklarını tap
            print("\n⚽ Oyunlar:")
            links = await page.locator("a").all()
            game_links = []
            for link in links:
                href = await link.get_attribute("href")
                if href and "/idman-novleri/futbol/" in href and "canli" not in href:
                    game_links.append("https://www.misli.az" + href)

            # 2. İlk 3 oyuna bax (test məqsədilə)
            for i, game_url in enumerate(game_links[:3]):
                print(f"\n🎮 {i+1}) Oyuna keçilir: {game_url}")
                game_page = await browser.new_page()
                await game_page.goto(game_url, timeout=60000)
                await game_page.wait_for_timeout(5000)

                # 3. Over/Under 2.5 əmsalını tapmağa çalış
                html = await game_page.content()
                overunder_texts = re.findall(r"(Over\s?2\.5|Under\s?2\.5)[^<>{}]{0,100}?\d+\.\d+", html, re.IGNORECASE)
                if overunder_texts:
                    print("📊 Over/Under əmsalları tapıldı:")
                    for item in overunder_texts:
                        print("•", item)
                else:
                    print("⚠️ Over/Under 2.5 tapılmadı")

                await game_page.close()

            await browser.close()

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
