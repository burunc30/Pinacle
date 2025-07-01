import asyncio
from playwright.async_api import async_playwright
import requests

async def main():
    url = "https://www.nesine.com/iddaa?et=1&ocg=MS-2%2C5&gt=Pop%C3%BCler"
    print("🔗 Sayta daxil olunur:", url)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)

            html = await page.content()
            print("✅ HTML alındı.")

            title = await page.title()
            print(f"ℹ️ Səhifə Başlığı: {title}")

            # Oyun adlarını seçmək üçün uyğun selector yazılmalıdır (bu test məqsədi ilə sadədir)
            oyunlar = await page.locator("tr.mbln-tbl-row").all_inner_texts()
            print("📦 Tapılan oyun sayı:", len(oyunlar))

            if oyunlar:
                for oyun in oyunlar[:10]:  # ilk 10 oyunu göstər
                    print("•", oyun)
            else:
                print("⚠️ Oyun tapılmadı. Element yüklənməmiş ola bilər.")

            await browser.close()

    except Exception as e:
        print("❌ Ümumi xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
