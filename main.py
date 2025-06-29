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

        # Bütün div-ləri tapırıq və filtrləyirik: içində həm komanda adı, həm də əmsallar var
        all_texts = await page.locator("div").all_inner_texts()

        print("\n📋 Tapılan potensial oyun blokları:")
        oyunlar = []
        for i, text in enumerate(all_texts):
            if any(k in text for k in ["Flamenqo", "Kanada", "ABŞ", "Duhok", "Paranavai"]):
                oyunlar.append(text.strip())

        if not oyunlar:
            print("⚠️ Oyun tapılmadı.")
        else:
            for idx, oyun in enumerate(oyunlar, 1):
                print(f"\n🔹 Oyun #{idx}:\n{oyun}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
