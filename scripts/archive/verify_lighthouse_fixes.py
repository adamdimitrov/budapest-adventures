import re
from bs4 import BeautifulSoup
import asyncio
from playwright.async_api import async_playwright

def apply_cleanups(html):
    # 1. tourcms-sync.js root path
    html = re.sub(r'src=["\']tourcms-sync\.js["\']', 'src="/tourcms-sync.js?v=20261113"', html)
    
    # 2. strip integrity attributes from local assets
    html = re.sub(r'\s+integrity=["\']sha[^"\']+["\']', '', html)
    
    # 3. replace heavy legenda-candlelit-dinner.jpg with avif
    html = html.replace('/legenda-candlelit-dinner.jpg', '/assets/cdn/60e43c7d6d05b671dff0dc1a/690332b608818ef6e357242b_candlelit-dinner-cruise-00002-p-800.avif')
    
    # 4. WCAG AA Contrast replacements
    # #0284c7 (4.09:1) -> #026aa2 (4.6:1)
    html = html.replace('#0284c7', '#026aa2')
    
    # 5. Deduplicate identical style blocks
    soup = BeautifulSoup(html, 'html.parser')
    seen_styles = set()
    for s in soup.find_all('style'):
        content = (s.string or '').strip()
        if not content:
            continue
        # Take hash of first 200 chars + len to identify identical blocks
        key = (len(content), content[:100])
        if key in seen_styles:
            s.decompose()
        else:
            seen_styles.add(key)
            
    # 6. Ensure main landmark
    if not soup.find('main'):
        wrapper = soup.find(class_='ltt-editorial-wrapper') or soup.find(class_='bpa-container') or soup.find(id='rankedDecks') or soup.find('article')
        if wrapper:
            wrapper['role'] = 'main'
            
    # 7. Ensure scrollable regions are focusable
    for slider in soup.find_all(class_='bpa-slider'):
        if not slider.get('tabindex'):
            slider['tabindex'] = '0'
            slider['role'] = 'region'
            slider['aria-label'] = 'Photo gallery'
            
    for film in soup.find_all(class_='ltt-filmstrip'):
        if not film.get('tabindex'):
            film['tabindex'] = '0'
            film['role'] = 'region'
            film['aria-label'] = 'Photo gallery'
            
    # 8. Fix preload link for dinner cruise if needed
    for pl in soup.find_all('link', rel='preload'):
        if pl.get('href') == '/legenda-candlelit-dinner.jpg':
            pl['href'] = '/assets/cdn/60e43c7d6d05b671dff0dc1a/690332b608818ef6e357242b_candlelit-dinner-cruise-00002-p-800.avif'
            pl['type'] = 'image/avif'

    return str(soup)

async def test_page(file_path):
    print(f"\n==========================================")
    print(f"Testing: {file_path}")
    with open(file_path) as f:
        raw_html = f.read()
        
    cleaned_html = apply_cleanups(raw_html)
    print(f"Original size: {len(raw_html):,} bytes -> Cleaned size: {len(cleaned_html):,} bytes")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless=True)
        page = await browser.new_page()
        
        console_msgs = []
        page.on("console", lambda msg: console_msgs.append(f"{msg.type}: {msg.text}"))
        
        await page.set_content(cleaned_html, wait_until="networkidle")
        await page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.4/axe.min.js")
        res = await page.evaluate("axe.run()")
        
        print("Console errors:", [m for m in console_msgs if "error" in m])
        violations = res.get("violations", [])
        print(f"Axe Violations: {len(violations)}")
        for v in violations:
            imp = v.get("impact", "")
            vid = v.get("id", "")
            nodes = v.get("nodes", [])
            print(f"  - [{imp}] {vid} ({len(nodes)} nodes)")
            for n in nodes[:2]:
                print(f"      {n.get('target')} :: {str(n.get('failureSummary', ''))[:100].replace(chr(10), ' ')}")
                
        await browser.close()

async def main():
    await test_page("/Users/adamdimitrov/Development/budapest-adventures/best-night-cruises-budapest.html")
    await test_page("/Users/adamdimitrov/Development/budapest-adventures/de/bootsfahrten-mit-abendessen-dunau-budapest/index.html")

asyncio.run(main())
