# Survey Report: Tracking Safeguards & Internationalization Pruning
**Project**: Budapest Adventures (`budapestadventures.com`)  
**Investigator**: Teamwork Explorer 3 (Tracking Safeguards & Internationalization Pruning)  
**Date**: November 6, 2026 (Staging Overhaul Phase)  
**Scope**: Outbound Booking Links, Query String Preservation, Meta Pixel / CAPI Pipeline, Linguana Multilingual Routing & `vercel.json` 301 Redirect Architecture

---

## 1. Executive Summary & Critical Alerts

This survey conducts a full forensic inspection of Budapest Adventures' commercial tracking infrastructure and multilingual routing architecture prior to the static staging deployment on branch `staging/static-overhaul`.

### 🚨 Critical Vulnerability 1: Legenda Partner ID Mismatch (`partner=38885` vs `partner=38585`)
- **Observation**:
  - The primary verified VIP Legenda partner ID across 14+ core files, including `river.html` (line 1121), `dinner.html` (line 865), `live_dinner_embed.html`, and `all_7_cruises_complete.html`, is **`38585`**.
  - However, in `legenda-city-cruises.html` (lines 365, 384, 403), `legenda.html`, and `direct_checkout_mockup.html`, the code sets:
    `legendaUrl: 'https://legenda.hu/en/ticket-purchase?partner=38885'`
- **Impact**: `38885` is a 1-digit typographical error (`8` instead of `5`) in the new dedicated Legenda terminal. Bookings generated through `legenda-city-cruises.html` will fail to credit Adam Dimitrov's VIP account (`38585`), jeopardizing the €130,000+ volume credential.
- **Immediate Fix**: Hardcode `partner=38585` across all Legenda checkout links.

### 🚨 Critical Vulnerability 2: Bare Links on Decision Hub (`danube_cruise_decision_hub.html`)
- **Observation**:
  - Line 467: `<a href="https://legenda.hu" target="_blank">` — **Zero partner ID, zero query tracking**.
  - Line 525: `<a href="https://silver-line.hu" target="_blank">` — **Zero affiliate code, zero query tracking**.
  - `danube_cruise_decision_hub.html` contains **NO Meta Pixel code**, **NO Google Ads tag**, **NO `tourcms-sync.js`**, and **NO `InitiateCheckout` triggers**.
- **Impact**: Any traffic sent to `danube_cruise_decision_hub.html` bleeds 100% of outbound conversions with zero affiliate commission attribution and zero pixel data.

### 🚨 Critical Vulnerability 3: Vercel Configuration Conflict (`routes` vs `redirects`)
- **Observation**: Current `vercel.json` uses the legacy Vercel v2 `"routes"` array:
  ```json
  "routes": [
      { "src": "/api/cron", "dest": "/api/cron.py" },
      { "src": "/legenda-city-cruises", "dest": "/legenda-city-cruises.html" },
      { "src": "/(.*)", "dest": "/$1" }
  ]
  ```
- **Constraint**: In Vercel, the `"routes"` property **cannot be combined** with `"redirects"`, `"rewrites"`, or `"cleanUrls"`. Attempting to add a `"redirects"` block while `"routes"` is defined triggers a fatal build failure:
  `Error: The "routes" property cannot be used with "redirects", "rewrites", "headers", "cleanUrls" or "trailingSlash".`
- **Solution**: Refactor `vercel.json` to modern Vercel schema using top-level `"redirects"` and `"rewrites"`.

### 🚨 Critical Vulnerability 4: Dropped UTM Parameters in `tourcms-sync.js`
- **Observation**: `tourcms-sync.js` captures `fbclid`, `_fbp`, and `gclid`/`wbraid`/`gbraid`, but completely ignores `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, and `utm_term`.
- **Impact**: Google Ads, Meta Ads, and email campaigns passing UTM parameters lose all campaign-level tagging when users click outbound partner links.

### 🚨 Critical Vulnerability 5: 404 Trap in Multilingual Redirects
- **Observation**: Linguana machine-translated the URL slugs for 25 languages into distinct translated strings (e.g. Czech `/cs/nejlepší-budapest-řeka-plavby`, Arabic `/ar/أفضل-رحلات-العشاء-البحرية-في-نهر-بودابست`).
- **Impact**: A generic regex redirect `/:lang/:path* -> /:path*` redirects visitors to non-existent English URLs (e.g. `/nejlepší-budapest-řeka-plavby`), producing hard 404 errors for indexed URLs.
- **Solution**: Exact 1-to-1 301 mappings for all known translated slugs to `/best-budapest-river-cruises` and `/best-dinner-cruises-budapest`, followed by a fallback rule.

---

## 2. Outbound Booking Links Audit Across Core Hubs

### 2.1 Legenda City Cruises (`legenda.hu`)
- **Partner Account**: Adam Dimitrov / Budapest Adventures (`contact@budapestadventures.com`)
- **Verified Primary Partner ID**: `38585`
- **Typo Partner ID Found**: `38885` (in `legenda-city-cruises.html`, `legenda.html`, `direct_checkout_mockup.html`)
- **Target URL Formats**:
  1. Root Affiliate Entry: `https://legenda.hu/en?partner=38585`
  2. Direct Webshop Ticket Purchase: `https://legenda.hu/en/ticket-purchase?partner=38585`
  3. Pre-configured Deep Links:
     - Danube Legend Evening Sightseeing: `https://legenda.hu/en/ticket-purchase?partner=38585&cruise=2`
     - Duna Bella Daytime Sightseeing: `https://legenda.hu/en/ticket-purchase?partner=38585&cruise=1`
     - Candlelit Dinner Cruise: `https://legenda.hu/en/ticket-purchase?partner=38585&cruise=3`
- **Outbound Tracking Parameters Supported**:
  - `subid`: Accepts pipe-delimited click IDs (`fbclid:xxx|gclid:yyy|utm_source:zzz`)
  - `agent_ref`: Compatible alias passed by TourCMS bridge

### 2.2 TourCMS Direct Integration & API Sync (`tourcms.com`)
- **Marketplace ID**: `57509`
- **Channel ID**: `16485` (Legenda City Cruises dedicated channel)
- **Agent ID**: `16`
- **API Key**: `51405b89d978`
- **Hosted Booking Engine URLs**:
  - Tour 1 (Duna Bella): `https://live.tourcms.com/reserve/r1.php?t=1&a=15391&w=16485&k=293ef7e67eed&agent=16&m=57509&mh=845458`
  - Tour 2 (Danube Legend): `https://live.tourcms.com/reserve/r1.php?t=2&a=15391&w=16485&k=cd81b8592b34&agent=16&m=57509&mh=845458`
  - Tour 3 (Candlelit Dinner): `https://live.tourcms.com/reserve/r1.php?t=3&a=15391&w=16485&k=bd6e986b0364&agent=16&m=57509&mh=845458`
- **Commercial Contract & Margin**:
  - TourCMS Net Rate contract (`booking_has_net_price = 1`): **25.0% verified commission margin** on Legenda tickets.
  - Calculation in `api/cron.py`: `commission_value = sales_revenue - balance` (e.g. €25 retail - €18.75 net balance = €6.25 margin per adult).
- **Offline Conversion Sync Pipeline (`api/cron.py`)**:
  - Fetches completed bookings via `/c/bookings/search.xml` and `/c/booking/show.xml`.
  - Parses `agent_ref`, `lead_customer_agent_ref`, and `customer_special_request` for click IDs:
    - Regex: `fbclid:xxx`, `fbp:fb.1.xxx`, `gclid:yyy`, `wbraid:yyy`, `gbraid:yyy`.
  - Dispatches server-side conversions:
    1. **Meta Conversions API (CAPI)**:
       - Pixel ID: `1355732169631751`
       - Event: `Purchase`
       - Value: `booking["commission_value"]` (Net margin, EUR)
       - Event ID: `tourcms_{booking_id}` (prevents client/server deduplication collisions)
       - User Data: SHA-256 hashed email, phone, firstname, surname, country, fbc, fbp.
    2. **Google Ads Offline Conversion Upload**:
       - Customer ID: `4899321613` (Account: Budapest Adventures)
       - Conversion Action ID: `7715980036`
       - Uploads `gclid`, `wbraid`, or `gbraid` with exact transaction timestamp and net commission value.

### 2.3 Tiqets Partner Program (`tiqets.com`)
- **Partner Handle**: `budapestadventures` (and `thecruisedetective.com-176436` in secondary bridge funnels)
- **Active Products**:
  - Budapest Evening Sightseeing Cruise: `p1114614`
  - Budapest Sightseeing Cruise (Daytime): `p1114615`
  - Budapest Danube Dinner Cruise with Live Music: `p1114795`
  - Budapest Hop-On Hop-Off Cruise with Drink: `p1132213`
- **Outbound Tracking Parameters Required**:
  - `partner`: `budapestadventures`
  - `click_id`: Pass-through click ID string
  - `subid`: Pass-through click ID string
  - `tq_campaign`: Funnel tag + click identifier (e.g. `bpa-river-hub--fbclid_xxx`)

### 2.4 Other Operator Partners
| Operator | Domain | Tracking Query Format | Active Pages |
| :--- | :--- | :--- | :--- |
| **Silverline Cruises** | `budapestrivercruise.eu` | `?code=bpadventures&subid=...&agent_ref=...` | `river.html`, `dinner.html`, `all_7_cruises_complete.html` |
| **Silverline Direct** | `silver-line.hu` | Needs `?code=bpadventures` (Currently bare!) | `index.html`, `danube_cruise_decision_hub.html` |
| **BudapestXplore** | `budapestxplore.com` | `?affi=6876&subid=...` | `dinner.html`, `all_7_cruises_complete.html` |
| **Rubin Group** | `rubingroup.hu` | Currently bare! | `index.html` |

---

## 3. Query String Preservation Audit

### 3.1 Current Architecture (`tourcms-sync.js`)
The existing script performs the following steps:
1. Checks `window.location.search` for `fbclid` and `gclid`/`wbraid`/`gbraid`.
2. Sets 30-day first-party cookies: `tc_fbclid`, `tc_gclid`, `tc_gclid_type`.
3. Reads `_fbp` cookie.
4. Generates `trackingString`: `fbclid:xxx|fbp:yyy|gclid:zzz`.
5. Iterates through links matching `PARTNER_DOMAINS` and appends `subid` and `agent_ref` or `click_id`.
6. Attaches a capture-phase click listener to re-decorate links and trigger `window.fbq('track', 'InitiateCheckout', ...)`.

### 3.2 Vulnerabilities & Technical Debt
1. **Zero UTM Parameter Capture**: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term` are completely dropped.
2. **First-Party Cookie Fragility**: Safari ITP restricts JavaScript-written cookies (`document.cookie`) to a 7-day or 24-hour lifetime. If a user browses multiple pages or returns the next day, tracking strings degrade.
3. **Internal Navigation Stripping**: When a user clicks from `/` to `/best-budapest-river-cruises`, URL parameters are not appended to internal links. If the user opens the target in a new tab where cookies fail, attribution is severed.
4. **Missing Coverage**:
   - `danube_cruise_decision_hub.html`: Script is completely missing.
   - `legenda-city-cruises.html`: Uses isolated inline script that misses cookie persistence and UTM tags.
5. **Dynamic Link Mutation**: Interactive elements that set `link.href` on click or select (e.g. date slot changes, quiz completion) can bypass decoration if clicked before the next event loop tick.

### 3.3 Enhanced Universal Tracking Script Specification (`bpa-tracking.js`)
The staging build requires an updated, unified client tracking script deployed across all staging pages:

```javascript
/**
 * Budapest Adventures Universal Tracking Safeguard (bpa-tracking.js)
 * Preserves gclid, fbclid, wbraid, gbraid, UTMs, and _fbp across sessions,
 * decorates all partner outbound links, and fires unified conversion events.
 */
(function() {
    'use strict';

    const COOKIE_EXPIRY_DAYS = 30;
    const STORAGE_PREFIX = 'bpa_';

    const TRACKING_PARAMS = [
        'fbclid', 'gclid', 'wbraid', 'gbraid',
        'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'
    ];

    const PARTNER_CONFIG = {
        'legenda.hu': { partnerKey: 'partner', partnerVal: '38585', refKey: 'subid', agentKey: 'agent_ref' },
        'tourcms.com': { partnerKey: 'w', partnerVal: '16485', refKey: 'subid', agentKey: 'agent_ref' },
        'tiqets.com': { partnerKey: 'partner', partnerVal: 'budapestadventures', refKey: 'subid', clickKey: 'click_id' },
        'budapestrivercruise.eu': { partnerKey: 'code', partnerVal: 'bpadventures', refKey: 'subid', agentKey: 'agent_ref' },
        'silver-line.hu': { partnerKey: 'code', partnerVal: 'bpadventures', refKey: 'subid' },
        'budapestxplore.com': { partnerKey: 'affi', partnerVal: '6876', refKey: 'subid' }
    };

    function getParam(key) {
        if (typeof window === 'undefined' || !window.location) return null;
        return new URLSearchParams(window.location.search).get(key);
    }

    function setStorage(key, val) {
        try {
            localStorage.setItem(STORAGE_PREFIX + key, val);
        } catch(e) {}
        const d = new Date();
        d.setTime(d.getTime() + (COOKIE_EXPIRY_DAYS * 86400000));
        document.cookie = `${STORAGE_PREFIX}${key}=${encodeURIComponent(val)};expires=${d.toUTCString()};path=/;SameSite=Lax`;
    }

    function getStorage(key) {
        try {
            const ls = localStorage.getItem(STORAGE_PREFIX + key);
            if (ls) return ls;
        } catch(e) {}
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${STORAGE_PREFIX}${key}=`);
        if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift());
        return null;
    }

    // 1. Capture incoming parameters
    TRACKING_PARAMS.forEach(param => {
        const val = getParam(param);
        if (val) setStorage(param, val);
    });

    // 2. Build structured tracking ref string
    const activeParams = {};
    TRACKING_PARAMS.forEach(param => {
        const val = getParam(param) || getStorage(param);
        if (val) activeParams[param] = val;
    });

    const fbpMatch = document.cookie.match(/(?:^|;\s*)_fbp=([^;]+)/);
    if (fbpMatch) activeParams['_fbp'] = fbpMatch[1];

    const trackingParts = [];
    if (activeParams.fbclid) trackingParts.push(`fbclid:${activeParams.fbclid}`);
    if (activeParams._fbp) trackingParts.push(`fbp:${activeParams._fbp}`);
    if (activeParams.gclid) trackingParts.push(`gclid:${activeParams.gclid}`);
    else if (activeParams.wbraid) trackingParts.push(`wbraid:${activeParams.wbraid}`);
    else if (activeParams.gbraid) trackingParts.push(`gbraid:${activeParams.gbraid}`);
    if (activeParams.utm_source) trackingParts.push(`utm_s:${activeParams.utm_source}`);
    if (activeParams.utm_campaign) trackingParts.push(`utm_c:${activeParams.utm_campaign}`);
    const trackingString = trackingParts.join('|');

    // 3. Decorate Outbound Partner Links
    window.bpaDecorateLink = function(link) {
        if (!link || !link.href) return;
        try {
            const url = new URL(link.href, window.location.origin);
            for (const [domain, conf] of Object.entries(PARTNER_CONFIG)) {
                if (url.hostname.includes(domain)) {
                    if (conf.partnerKey && !url.searchParams.has(conf.partnerKey)) {
                        url.searchParams.set(conf.partnerKey, conf.partnerVal);
                    }
                    if (trackingString) {
                        if (conf.refKey) url.searchParams.set(conf.refKey, trackingString);
                        if (conf.agentKey) url.searchParams.set(conf.agentKey, trackingString);
                        if (conf.clickKey) url.searchParams.set(conf.clickKey, trackingString);
                    }
                    link.href = url.toString();
                    break;
                }
            }
        } catch(e) {}
    };

    function decorateAll() {
        document.querySelectorAll('a').forEach(window.bpaDecorateLink);
    }

    // 4. Click Interceptor for Instant Attribution & Pixel Events
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (!link || !link.href) return;

        window.bpaDecorateLink(link);

        const url = new URL(link.href, window.location.origin);
        const isPartner = Object.keys(PARTNER_CONFIG).some(dom => url.hostname.includes(dom));
        if (!isPartner) return;

        // Context extraction (price & product name)
        let contentName = 'Budapest River Cruise';
        let retailPrice = 25.00;
        const commissionRate = 0.25;

        const hrefLower = link.href.toLowerCase();
        if (hrefLower.includes('dinner') || hrefLower.includes('candlelit') || hrefLower.includes('cruise=3')) {
            contentName = 'Legenda Candlelit Dinner Cruise';
            retailPrice = 110.00;
        } else if (hrefLower.includes('bella') || hrefLower.includes('cruise=1')) {
            contentName = 'Legenda Duna Bella Daytime Cruise';
            retailPrice = 20.00;
        } else if (hrefLower.includes('cruise=2') || hrefLower.includes('legend')) {
            contentName = 'Legenda Danube Legend Evening Cruise';
            retailPrice = 25.00;
        }

        const netCommission = Math.round(retailPrice * commissionRate * 100) / 100;

        // Fire Meta Pixel
        if (typeof window.fbq === 'function') {
            window.fbq('track', 'InitiateCheckout', {
                content_name: contentName,
                content_category: 'River Cruise',
                value: netCommission,
                currency: 'EUR'
            });
        }

        // Fire Google Ads gtag
        if (typeof window.gtag === 'function') {
            window.gtag('event', 'begin_checkout', {
                value: netCommission,
                currency: 'EUR',
                items: [{ item_name: contentName, price: retailPrice }]
            });
        }

        // Push to DataLayer
        if (Array.isArray(window.dataLayer)) {
            window.dataLayer.push({
                event: 'initiate_checkout_partner',
                partner: url.hostname,
                content_name: contentName,
                value: netCommission,
                retail_price: retailPrice,
                currency: 'EUR'
            });
        }
    }, true);

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', decorateAll);
    } else {
        decorateAll();
    }
})();
```

---

## 4. Meta Pixel & Conversion Tracking Audit

### 4.1 Pixel ID Identification & Discrepancies
- **Active Production Pixel ID**: **`1355732169631751`**
  - Confirmed in `.env` (`META_PIXEL_ID=1355732169631751`)
  - Confirmed in `api/cron.py` (line 195)
  - Confirmed in `legenda-city-cruises.html` (lines 28, 32)
- **Legacy Pixel ID**: **`889886707052830`**
  - Found in `dinner_desktop_wide_preview.html` (line 85)
  - Found in `river_desktop_wide_preview.html` (line 278)
- **Directive**: Standardize strictly on `1355732169631751` across all pages. The legacy pixel `889886707052830` should be retired.

### 4.2 Conversion Value Reconciliation (Gross Retail vs Net Commission)
There is a fundamental accounting split between funnel events:
1. **Gross Retail Value**:
   - Adult Sightseeing: €20.00 – €25.00
   - Candlelit Dinner: €110.00
   - Used in `legenda-city-cruises.html` UI display and currently passed to `fbq('track', 'InitiateCheckout', { value: retailTotal })`.
2. **Net Commission Value**:
   - Adult Sightseeing (25% margin): **€5.00 – €6.25**
   - Candlelit Dinner (25% margin): **€27.50**
   - Used in `api/cron.py` for Meta CAPI `Purchase` events and Google Ads offline conversion uploads.
3. **The Problem**: If `InitiateCheckout` reports €110.00 (gross) and backend `Purchase` reports €27.50 (net commission), Meta's algorithm detects a 75% value decline at checkout, muddying automated bidding (Value Optimization / ROAS).
4. **The Recommendation**: Report **Net Commission Value** across both `InitiateCheckout` and `Purchase`. This grounds Meta Ads ROAS bidding in actual cash profits retained by Budapest Adventures, preventing artificial ROAS inflation.

---

## 5. Linguana Multilingual Route Audit & Pruning Strategy

### 5.1 Language Roster Breakdown (30 Languages)
Budapest Adventures currently hosts Linguana configurations for 30 languages.

#### Approved Core High-Volume Converting Languages (5 retained):
1. **English (`en`)**: Default canonical language at root `/`
2. **German (`de`)**: High German tourist volume in Budapest
3. **Italian (`it`)**: Major Mediterranean tourist demographic
4. **French (`fr`)**: Significant European leisure segment
5. **Spanish (`es`)**: Large European and Latin American inbound market

#### Pruned Machine-Translated Zombie Languages (25 to eliminate):
`cs` (Czech), `bg` (Bulgarian), `zh` (Chinese), `vi` (Vietnamese), `uk` (Ukrainian), `ar` (Arabic), `sv` (Swedish), `sr` (Serbian), `el` (Greek), `fi` (Finnish), `da` (Danish), `th` (Thai), `hr` (Croatian), `nl` (Dutch), `no` (Norwegian), `sk` (Slovak), `tr` (Turkish), `ko` (Korean), `ru` (Russian), `pt` (Portuguese), `ja` (Japanese), `ro` (Romanian), `he` (Hebrew), `pl` (Polish), `hu` (Hungarian).

### 5.2 Complete Inventory of Pruned Localized Slugs
Below is the full table of verified machine-translated URLs extracted from `river.html`, `dinner.html`, and `things-to-do.html`. Every single one must be mapped via 301/308 redirect to prevent crawl errors.

| Language | River Cruises Slug (Canonical: `/best-budapest-river-cruises`) | Dinner Cruises Slug (Canonical: `/best-dinner-cruises-budapest`) |
| :--- | :--- | :--- |
| **Arabic (`ar`)** | `/ar/أفضل-رحلات-العشاء-البحرية-في-نهر-بودابست` | `/ar/أفضل-رحلات-العشاء-البحرية-في-بودابست` |
| **Bulgarian (`bg`)** | `/bg/най-добрите-будапеща-речни-круизи` | `/bg/най-добрата-вечеря-круизи-будапеща` |
| **Czech (`cs`)** | `/cs/nejlepší-budapest-řeka-plavby` | `/cs/nejlepší-večeře-plavby-budapešť` |
| **Danish (`da`)** | `/da/bedste-budapest-flodkrydstogter` | `/da/bedste-middagskrydstogter-budapest` |
| **Greek (`el`)** | `/el/Βουδαπέστη-ποτάμι-κρουαζιέρες` | `/el/καλύτερο-δείπνο-κρουαζιέρες-Βουδαπέστη` |
| **Finnish (`fi`)** | `/fi/parhaat-illallisristeilyt-budapest` | `/fi/parhaat-budapest-jokiristeilyt` |
| **Hebrew (`he`)** | `/he/הפלגות-דנובה-בודפשט` | `/he/ארוחתערב-שייט-דנובה-בודפשט` |
| **Croatian (`hr`)** | `/hr/najbolja-krstarenja-rijekom-budimpešta` | `/hr/najbolja-krstarenja-svečerom-budimpešta` |
| **Hungarian (`hu`)**| `/hu/setahajozas-a-dunan-budapest` | `/hu/setahajozas-a-dunan-vacsoraval` |
| **Japanese (`ja`)** | `/ja/budapesuto-ribakuruzu` | `/ja/budapesuto-dinakuruzu` |
| **Korean (`ko`)** | `/ko/gang-keulujeu-budapeseuteu-danyubeu` | `/ko/dineo-keulujeu-budapeseuteu-danyubeu` |
| **Dutch (`nl`)** | `/nl/beste-boedapest-riviercruises` | `/nl/beste-diner-cruises-boedapest` |
| **Norwegian (`no`)**| `/no/beste-budapest-elve-cruise` | `/no/beste-middagscruise-budapest` |
| **Polish (`pl`)** | `/pl/rejsy-dunaju-budapeszt` | `/pl/rejsy-dunaju-budapeszt-kolacja` |
| **Portuguese (`pt`)**| `/pt/budapeste-cruzeiros-danubio` | `/pt/budapeste-jantar-cruzeiros-danubio` |
| **Romanian (`ro`)** | `/ro/croaziera-dunare-budapesta` | `/ro/croaziera-dunare-cu-cina-budapesta` |
| **Russian (`ru`)** | `/ru/rechnyye-kruizy-budapesht-dunay` | `/ru/uzhin-kruizy-budapesht-dunay` |
| **Slovak (`sk`)** | `/sk/riecne-plavby-budapest-dunaj` | `/sk/vecera-plavby-budapest-dunaj` |
| **Serbian (`sr`)** | `/sr/најбоље-будапест-река-крстарења` | `/sr/најбоља-вечера-крстарења-будимпешта` |
| **Swedish (`sv`)** | `/sv/bästa-budapest-flod-kryssningar` | `/sv/bästa-middag-kryssningar-budapest` |
| **Thai (`th`)** | `/th/บูดาเปสต์-ล่องเรือแม่น้ำ` | `/th/บูดาเปสต์-ดินเนอร์-ล่องเรือ` |
| **Turkish (`tr`)** | `/tr/nehir-yolculuklari-budapeste-tuna` | `/tr/aksam-yemegi-yolculuklari-budapeste-tuna` |
| **Ukrainian (`uk`)**| `/uk/найкращі-річкові-круїзи-будапешті` | `/uk/найкраща-вечеря-круїзи-будапешт` |
| **Vietnamese (`vi`)**| `/vi/du-thuyền-trên-sông-tốt-nhất-budapest` | `/vi/bữa-tối-ngon-nhất-du-thuyền-budapest` |
| **Chinese (`zh`)** | `/zh/布达佩斯最佳河流游轮` | `/zh/布达佩斯最佳晚餐游轮` |

---

## 6. Complete `vercel.json` 301/308 Redirect Architecture

To prevent Vercel configuration collisions and preserve 100% of historical SEO equity from the pruned Linguana paths, `vercel.json` must be structured as follows:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "version": 2,
  "cleanUrls": true,
  "trailingSlash": false,
  "redirects": [
    {
      "source": "/(cs|cs/.*)",
      "has": [{ "type": "query", "key": "dummy", "value": "x" }],
      "destination": "/",
      "permanent": true
    },
    { "source": "/cs/nejlep:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/bg/най-добрите:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/zh/布达佩斯最佳河流游轮", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/vi/du-thuy:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/uk/найкращі-річкові:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/ar/أفضل-رحلات-العشاء-البحرية-في-نهر:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/sv/bästa-budapest-flod:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/sr/најбоље-будапест:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/el/Βουδαπέστη-ποτάμι:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/fi/parhaat-illallisristeilyt:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/da/bedste-budapest-flod:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/th/บูดาเปสต์-ล่องเรือ:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/hr/najbolja-krstarenja-rijekom:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/nl/beste-boedapest-rivier:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/no/beste-budapest-elve:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/sk/riecne-plavby:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/tr/nehir-yolculuklari:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/ko/gang-keulujeu:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/ru/rechnyye-kruizy:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/pt/budapeste-cruzeiros:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/ja/budapesuto-ribakuruzu", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/ro/croaziera-dunare:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/he/הפלגות-דנובה:slug(.*)", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/pl/rejsy-dunaju-budapeszt", "destination": "/best-budapest-river-cruises", "permanent": true },
    { "source": "/hu/setahajozas-a-dunan-budapest", "destination": "/best-budapest-river-cruises", "permanent": true },

    { "source": "/cs/nejlepší-večeře:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/bg/най-добрата-вечеря:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/zh/布达佩斯最佳晚餐游轮", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/vi/bữa-tối-ngon-nhất:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/uk/найкраща-вечеря:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/ar/أفضل-رحلات-العشاء-البحرية-في-بودابست", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/sv/bästa-middag:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/sr/најбоља-вечера:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/el/καλύτερο-δείπνο:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/fi/parhaat-budapest-joki:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/da/bedste-middags:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/th/บูดาเปสต์-ดินเนอร์:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/hr/najbolja-krstarenja-svečerom:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/nl/beste-diner:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/no/beste-middags:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/sk/vecera-plavby:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/tr/aksam-yemegi:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/ko/dineo-keulujeu:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/ru/uzhin-kruizy:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/pt/budapeste-jantar:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/ja/budapesuto-dinakuruzu", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/ro/croaziera-dunare-cu-cina:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/he/ארוחתערב-שייט:slug(.*)", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/pl/rejsy-dunaju-budapeszt-kolacja", "destination": "/best-dinner-cruises-budapest", "permanent": true },
    { "source": "/hu/setahajozas-a-dunan-vacsoraval", "destination": "/best-dinner-cruises-budapest", "permanent": true },

    {
      "source": "/:lang(cs|bg|zh|vi|uk|ar|sv|sr|el|fi|da|th|hr|nl|no|sk|tr|ko|ru|pt|ja|ro|he|pl|hu)/:path*",
      "destination": "/:path*",
      "permanent": true
    },
    {
      "source": "/:lang(cs|bg|zh|vi|uk|ar|sv|sr|el|fi|da|th|hr|nl|no|sk|tr|ko|ru|pt|ja|ro|he|pl|hu)",
      "destination": "/",
      "permanent": true
    }
  ],
  "rewrites": [
    { "source": "/api/cron", "destination": "/api/cron.py" },
    { "source": "/legenda-city-cruises", "destination": "/legenda-city-cruises.html" },
    { "source": "/budapest-river-cruises", "destination": "/river.html" },
    { "source": "/best-budapest-river-cruises", "destination": "/river.html" },
    { "source": "/budapest-dinner-cruises", "destination": "/dinner.html" },
    { "source": "/best-dinner-cruises-budapest", "destination": "/dinner.html" },
    { "source": "/danube-river-cruise-hub", "destination": "/danube_cruise_decision_hub.html" }
  ]
}
```

---

## 7. Action Items for Implementation Phase

1. **Fix Legenda Partner ID**: Replace `partner=38885` with `partner=38585` in `legenda-city-cruises.html`, `legenda.html`, and `direct_checkout_mockup.html`.
2. **Deploy Universal Tracking Safeguard**:
   - Create `/bpa-tracking.js` incorporating UTM parameter retention, cookie/localStorage persistence, and automatic link decoration across all partner domains (`legenda.hu`, `tourcms.com`, `tiqets.com`, `budapestrivercruise.eu`, `silver-line.hu`, `budapestxplore.com`).
   - Add `<script src="/bpa-tracking.js"></script>` to `legenda-city-cruises.html`, `danube_cruise_decision_hub.html`, `river.html`, `dinner.html`, and `index.html`.
3. **Harmonize Meta Pixel ID & Conversion Values**:
   - Ensure Meta Pixel `1355732169631751` is installed in `<head>` across all active staging pages.
   - Standardize `InitiateCheckout` value on estimated net commission to match backend CAPI `Purchase` events.
4. **Deploy Refactored `vercel.json`**:
   - Replace legacy `"routes"` with top-level `"redirects"`, `"rewrites"`, and `"cleanUrls"`.
   - Verify all 25 pruned languages 301 redirect cleanly to canonical English targets without 404s.
5. **Strip Linguana Bloat**:
   - Remove `<meta name="linguana-site-verification">`, `linguana_switcher.min.js`, `linguana_switcher.min.css`, and 25 pruned hreflang tags from `river.html` and `dinner.html`.
   - Preserve hreflang tags exclusively for `en`, `de`, `it`, `fr`, `es`.
