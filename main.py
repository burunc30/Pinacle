import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.misli.az/idman-novleri/futbol"
    print("🔗 Sayta daxil olunur:", url)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        
        # JS yüklənməsini gözlə
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(5000)  # əlavə 5 saniyə tampon

        print("✅ HTML alındı.")
        title = await page.title()
        print("ℹ️ Başlıq:", title)

        # Butun div-ləri çıxardaq (debug məqsədi ilə)
        all_divs = await page.locator("div").all_inner_texts()
        print(f"🔍 Tapılan div sayı: {len(all_divs)}")

        # İlk 20 div-ə bax
        for i, d in enumerate(all_divs[:20]):
            print(f"{i+1}. 📄", d.strip())

        # Daha sonra buradan uyğun selector tapacağıq
        # Məs: div:has-text("Flamenqo") və ya data-testid varsa onunla

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
