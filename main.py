daxil olunur:", url)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            print("✅ HTML alındı.")

            title = await page.title()
            print(f"ℹ️ Səhifə Başlığı: {title}")

            # Komanda adlarını gözlə və al
            selectors = [
                '[data-testid="event-title"]',
                '.event-name', '.match-row',
                '.match-title', '.fixture',
                '.market-title'
            ]

            found_teams = False
            for sel in selectors:
                try:
                    await page.wait_for_selector(sel, timeout=3000)
                    event_names = await page.locator(sel).all_inner_texts()
                    if event_names:
                        print("⚽ Tapılan komanda adları:")
                        for team in event_names[:15]:
                            print("•", team.strip())
                        found_teams = True
                        break
                except:
                    continue

            if not found_teams:
                print("⚠️ Komanda adı tapılmadı.")

            # Əmsallar tap
            html = await page.content()
            odds_matches = re.findall(r"\d+\.\d+", html)
            if odds_matches:
                print("🎯 Tapılan əmsal sayı:", len(odds_matches))
                for o in odds_matches[:15]:
                    print("•", o)
            else:
                print("❌ Əmsal tapılmadı.")

            await browser.close()

    except Exception as e:
        print("❌ Xəta baş verdi:", e)

if __name__ == "__main__":
    asyncio.run(main())
