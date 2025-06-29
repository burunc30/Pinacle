import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.misli.az/idman-novleri/futbol"
    print("🔗 Sayta daxil olunur:", url)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(3000)

        print("✅ HTML alındı.")

        # Saytdakı oyun kartlarını tap
        cards = await page.locator("div[class*=match-card], div[class*=match]").all()
        print(f"🔢 Tapılan oyun sayı: {len(cards)}")

        for i, card in enumerate(cards[:5]):  # Test üçün yalnız ilk 5 oyun
            print(f"\n🎯 Oyun {i+1}:")

            try:
                # Komanda adlarını al
                teams = await card.locator("div:has-text(' - ')").all_inner_texts()
                if teams:
                    print("⚽ Komandalar:", teams[0])

                # Əmsalları al
                odds = await card.locator("span.odds-value").all_inner_texts()
                if odds:
                    print("💰 1X2 Əmsallar:", odds[:3])

                # "+614" düyməsinə klik et (əgər varsa)
                try:
                    plus_btn = card.locator("text=+").first
                    await plus_btn.click()
                    await page.wait_for_timeout(1000)

                    # Açılan bazarlardan Over/Under seç
                    markets = await page.locator("div:has-text('Ümumi Qollar')").all_inner_texts()
                    if markets:
                        print("📊 Over/Under:", markets[:5])
                    else:
                        print("⚠️ Over/Under tapılmadı")

                except:
                    print("➕ Əlavə bazar düyməsi yoxdur və ya klik alınmadı.")

            except Exception as e:
                print("❌ Xəta:", e)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
