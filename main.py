import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.nesine.com/iddaa?et=1&ocg=MS-2%2C5&gt=Pop%C3%BCler"
    print("🔗 Sayta daxil olunur:", url)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await page.wait_for_selector("tr.mbln-tbl-row", timeout=15000)
            print("✅ HTML alındı.")

            title = await page.title()
            print(f"ℹ️ Səhifə Başlığı: {title}")

            # Bütün oyun satırlarını seç
            games = page.locator("tr.mbln-tbl-row")
            count = await games.count()
            print(f"📦 Tapılan oyun sayı: {count}")

            for i in range(min(count, 10)):  # ilk 10 oyun
                row = games.nth(i)
                try:
                    time = await row.locator("td.mbln-td-time").inner_text()
                    teams = await row.locator("td.mbln-td-team").inner_text()
                    odds = await row.locator("td.mbln-td-oc").all_inner_texts()
                    
                    print("⏰ Saat:", time.strip())
                    print("⚽ Oyun:", teams.strip())
                    print("💸 Əmsallar:")
                    for odd in odds:
                        print("•", odd.strip())
                    print("—" * 30)
                except Exception as e:
                    print("⚠️ Xəta oldu (oyun sırasında):", e)

            await browser.close()

    except Exception as e:
        print("❌ Ümumi xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
