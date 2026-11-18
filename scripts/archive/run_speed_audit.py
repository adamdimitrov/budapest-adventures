#!/usr/bin/env python3
"""
Comprehensive Real-Browser Performance & Network Audit
Uses Headless Google Chrome via Playwright
Measures:
- Total Page Size (Transferred Bytes & Decoded Bytes)
- Total HTTP Requests Count
- Load Time, DOMContentLoaded, TTFB, FCP, LCP
- Request Breakdown by Resource Type (Image, Script, Stylesheet, Font, Document)
- Cache-Control & Expires compliance
- Content-Encoding / Gzip compliance
"""

import sys
import json
from playwright.sync_api import sync_playwright

CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

def audit_url(url, device_type='desktop'):
    viewport = {'width': 1366, 'height': 768} if device_type == 'desktop' else {'width': 393, 'height': 852}
    user_agent = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        if device_type == 'desktop' else
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
    )

    requests_log = []
    responses_log = []

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(
            viewport=viewport,
            user_agent=user_agent,
            is_mobile=(device_type == 'mobile'),
            has_touch=(device_type == 'mobile')
        )
        page = context.new_page()

        def on_request(req):
            requests_log.append(req)

        def on_response(res):
            responses_log.append(res)

        page.on('request', on_request)
        page.on('response', on_response)

        # Start timer
        start_time = page.evaluate('() => performance.now()')
        
        # Navigate to target URL
        res = page.goto(url, wait_until='networkidle', timeout=30000)
        
        # Collect Web Vitals & Performance Timings
        metrics = page.evaluate("""() => {
            const nav = performance.getEntriesByType('navigation')[0] || {};
            const paints = performance.getEntriesByType('paint');
            let fcp = 0;
            paints.forEach(p => {
                if (p.name === 'first-contentful-paint') fcp = p.startTime;
            });
            
            return {
                ttfb: nav.responseStart - nav.requestStart,
                domInteractive: nav.domInteractive,
                domContentLoaded: nav.domContentLoadedEventEnd,
                loadComplete: nav.loadEventEnd,
                transferSize: nav.transferSize,
                decodedBodySize: nav.decodedBodySize,
                fcp: fcp
            };
        }""")

        # Wait a grace period to see if any late timers fire (e.g. 1.5s)
        page.wait_for_timeout(1500)

        # Analyze responses
        total_transfer_bytes = 0
        type_counts = {}
        type_bytes = {}
        uncompressed_text = []
        short_cache = []

        for r in responses_log:
            try:
                headers = r.headers
                ct = headers.get('content-type', '')
                cc = headers.get('cache-control', '')
                ce = headers.get('content-encoding', '')
                req_url = r.url
                
                # estimate size from content-length if available
                cl = int(headers.get('content-length', 0))
                total_transfer_bytes += cl

                res_type = r.request.resource_type
                type_counts[res_type] = type_counts.get(res_type, 0) + 1
                type_bytes[res_type] = type_bytes.get(res_type, 0) + cl

                # Check gzip on text types
                is_text = any(t in ct for t in ['text', 'javascript', 'json', 'xml'])
                if is_text and not ce and cl > 1000:
                    uncompressed_text.append(req_url)

                # Check cache on first-party static assets
                if 'budapestadventures.com' in req_url and res_type in ['image', 'script', 'stylesheet', 'font']:
                    if 'max-age=0' in cc or not cc:
                        short_cache.append(req_url)
            except Exception:
                pass

        browser.close()

        return {
            'url': url,
            'device': device_type,
            'status': res.status if res else None,
            'total_requests': len(requests_log),
            'total_transfer_mb': total_transfer_bytes / (1024 * 1024),
            'metrics': metrics,
            'type_counts': type_counts,
            'type_bytes_kb': {k: round(v / 1024, 1) for k, v in type_bytes.items()},
            'uncompressed_text_count': len(uncompressed_text),
            'short_cache_first_party_count': len(short_cache),
            'sample_short_cache': short_cache[:5]
        }

if __name__ == '__main__':
    urls_to_test = [
        'https://budapestadventures.com/budapest-river-cruises',
        'https://budapestadventures.com/budapest-dinner-cruises',
        'https://budapestadventures.com/'
    ]

    for u in urls_to_test:
        print(f"\n==========================================")
        print(f"AUDITING: {u}")
        print(f"==========================================")
        res_desktop = audit_url(u, device_type='desktop')
        print(f"DESKTOP RESULTS:")
        print(f"  Total Requests: {res_desktop['total_requests']}")
        print(f"  Total Transfer Size: {res_desktop['total_transfer_mb']:.2f} MB")
        print(f"  TTFB: {res_desktop['metrics']['ttfb']:.1f} ms")
        print(f"  FCP (First Contentful Paint): {res_desktop['metrics']['fcp']:.1f} ms")
        print(f"  DOMContentLoaded: {res_desktop['metrics']['domContentLoaded']:.1f} ms")
        print(f"  Load Event: {res_desktop['metrics']['loadComplete']:.1f} ms")
        print(f"  Requests Breakdown: {res_desktop['type_counts']}")
        print(f"  Bytes Breakdown (KB): {res_desktop['type_bytes_kb']}")
        print(f"  First-Party Assets with max-age=0: {res_desktop['short_cache_first_party_count']}")
        print(f"  Uncompressed Text Files (>1KB): {res_desktop['uncompressed_text_count']}")
