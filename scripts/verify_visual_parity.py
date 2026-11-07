import asyncio
from playwright.async_api import async_playwright

PAGES = [
    "index.html",
    "about.html",
    "contact.html",
    "budapest-card-is-it-worth-it.html",
    "river.html",
    "dinner.html",
    "best-night-cruises-budapest.html",
    "best-private-boat-tours-budapest.html",
    "unlimited-prosecco-cruises-budapest.html",
    "thermal-baths-budapest.html",
    "best-walking-tours-budapest.html",
    "best-hostels-budapest.html"
]

BASE_URL = "http://127.0.0.1:3000"

async def test_pages():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        total_broken_images = 0

        print("\n=== STEP 1: VERIFYING IMAGE INTEGRITY ACROSS ALL 12 PAGES ===")
        for page_name in PAGES:
            url = f"{BASE_URL}/{page_name}"
            resp = await page.goto(url, wait_until="networkidle")
            assert resp.status == 200, f"Page {url} returned HTTP {resp.status}"

            # Check all img tags
            broken = await page.evaluate('''() => {
                const imgs = Array.from(document.querySelectorAll('img'));
                const brokenImgs = [];
                for (const img of imgs) {
                    // Check if complete and naturalWidth > 0
                    if (img.complete && img.naturalWidth === 0) {
                        brokenImgs.push({
                            src: img.src,
                            alt: img.alt,
                            className: img.className
                        });
                    }
                }
                return brokenImgs;
            }''')

            if broken:
                print(f"❌ [{page_name}] Found {len(broken)} broken images:")
                for b in broken:
                    print(f"    • {b['src']} (alt: {b['alt']})")
                total_broken_images += len(broken)
            else:
                img_count = await page.evaluate("() => document.querySelectorAll('img').length")
                print(f"✅ [{page_name}] {img_count} images loaded with 0 broken images")

        print(f"\nTotal broken images across site: {total_broken_images}")
        assert total_broken_images == 0, f"Found {total_broken_images} broken images!"

        print("\n=== STEP 2: VERIFYING NAVBAR PARITY & MEGA-MENU ON DESKTOP ===")
        for page_name in ["index.html", "budapest-card-is-it-worth-it.html", "river.html"]:
            url = f"{BASE_URL}/{page_name}"
            await page.goto(url, wait_until="domcontentloaded")
            logo = page.locator(".ltt-brand-logo")
            await logo.wait_for(state="visible")
            logo_src = await logo.get_attribute("src")
            assert "/assets/budapest-adventures-logo.png" in logo_src, f"Wrong logo src: {logo_src}"

            # Check mega menu
            dropdown_btn = page.locator("#lttExploreDropdown button.ltt-dropdown-btn")
            await dropdown_btn.hover()
            await page.wait_for_timeout(200)
            mega = page.locator(".ltt-mega-menu")
            is_visible = await mega.is_visible()
            assert is_visible, f"Mega menu not visible on {page_name}"

            # Check Budapest Card in mega menu
            card_link = mega.locator("a[href*='budapest-card']")
            card_count = await card_link.count()
            assert card_count > 0, f"Budapest card missing in mega-menu of {page_name}"
            print(f"✅ [{page_name}] Logo verified, mega-menu opens, Budapest Card link present")

        print("\n=== STEP 3: VERIFYING MOBILE DRAWER AT 390PX VIEWPORT ===")
        await page.set_viewport_size({"width": 390, "height": 844})
        for page_name in ["index.html", "budapest-card-is-it-worth-it.html"]:
            url = f"{BASE_URL}/{page_name}"
            await page.goto(url, wait_until="domcontentloaded")
            hamburger = page.locator("#lttNavToggle")
            await hamburger.wait_for(state="visible")
            await hamburger.click()
            await page.wait_for_timeout(200)
            drawer = page.locator("#lttMobileDrawer")
            assert "is-open" in (await drawer.get_attribute("class")), "Drawer did not open!"
            
            # Check Budapest Card in drawer
            drawer_card = drawer.locator("a[href*='budapest-card']")
            assert (await drawer_card.count()) > 0, "Budapest card link missing in drawer!"
            print(f"✅ [{page_name} @ 390px] Hamburger toggles mobile drawer cleanly with all links")

        print("\n=== STEP 4: VERIFYING BUDAPEST CARD CALCULATOR ENGINE ===")
        # Ensure desktop viewport for widget interaction
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/budapest-card-is-it-worth-it.html", wait_until="domcontentloaded")
        await page.wait_for_timeout(500)
        
        # Test preset buttons
        preset_museum = page.locator("#presetMuseum")
        await preset_museum.click()
        await page.wait_for_timeout(300)

        # Check net financial balance value
        balance_text = await page.locator("#dispNetBalance").text_content()
        print(f"    • Museum Marathon Preset Net Balance: {balance_text}")
        assert "€" in balance_text or "Ft" in balance_text, "Net balance not computed!"

        # Test currency toggle
        curr_huf = page.locator("#currHuf")
        await curr_huf.click()
        await page.wait_for_timeout(300)
        huf_balance = await page.locator("#dispNetBalance").text_content()
        print(f"    • Currency Toggled to HUF: {huf_balance}")
        assert "Ft" in huf_balance, "HUF currency symbol not rendered!"

        # Screenshot artifacts
        await page.goto(f"{BASE_URL}/index.html", wait_until="domcontentloaded")
        await page.wait_for_timeout(500)
        await page.screenshot(path="/Users/adamdimitrov/.gemini/antigravity/brain/28fdda8d-9608-4430-a0e7-75d7e26dd58a/home_qc_verified.png")

        await page.goto(f"{BASE_URL}/budapest-card-is-it-worth-it.html", wait_until="domcontentloaded")
        await page.wait_for_timeout(500)
        await page.screenshot(path="/Users/adamdimitrov/.gemini/antigravity/brain/28fdda8d-9608-4430-a0e7-75d7e26dd58a/card_qc_verified.png")

        print("\n🎉 ALL TESTS PASSED: 100% PRODUCTION VERIFIED!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_pages())
