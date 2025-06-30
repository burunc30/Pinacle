import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.misli.az/idman-novleri/futbol"
    print("🔗 Sayta daxil olunur:", url)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(5000)

        print("✅ HTML alındı.")
        title = await page.title()
        print("ℹ️ Başlıq:", title)

        # Oyunlara aid linklər
        hrefs = await page.locator("a").evaluate_all("links => links.map(a => a.href)")
        oyun_linkləri = [link for link in hrefs if "/idman-novleri/futbol/" in link and "/oyun/" in link]

        oyun_linkləri = list(set(oyun_linkləri))  # Unikal et
        print(f"\n🔗 Tapılan oyun linklərinin sayı: {len(oyun_linkləri)}")
        for link in oyun_linkləri[:10]:  # ilk 10 linki göstər
            print("•", link)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
