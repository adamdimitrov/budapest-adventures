# Handoff Report — Explorer Survey 3 (Tracking Safeguards & Internationalization Pruning)

## 1. Observation

1. **Legenda Partner ID Discrepancy**:
   - `river.html:1121`: `<a href="https://legenda.hu/en?partner=38585" target="_blank" class="mobile-sticky-cta-btn">`
   - `dinner.html:865`: `<a href="https://legenda.hu/en?partner=38585" target="_blank"`
   - `generate_full_river_deck.py:179`: `href="https://legenda.hu/en?partner=38585"`
   - `live_dinner_embed.html:161,177,633,657`: `https://legenda.hu/en?partner=38585`
   - `all_7_cruises_complete.html:411,450,543`: `https://legenda.hu/en?partner=38585`
   - `legenda-city-cruises.html:365,384,403`: `legendaUrl: 'https://legenda.hu/en/ticket-purchase?partner=38885'`
   - `direct_checkout_mockup.html:385,409,431`: `legendaUrl: 'https://legenda.hu/en/ticket-purchase?partner=38885'`
   - `legenda.html:385,409,431`: `legendaUrl: 'https://legenda.hu/en/ticket-purchase?partner=38885'`

2. **Decision Hub Tracking Void (`danube_cruise_decision_hub.html`)**:
   - Line 467: `<a href="https://legenda.hu" target="_blank" rel="noopener" ...>` (No partner parameter, no click ID).
   - Line 525: `<a href="https://silver-line.hu" target="_blank" rel="noopener" ...>` (No partner code, no click ID).
   - Lines 1-707: Zero references to `fbq`, `gtag`, `dataLayer`, or `tourcms-sync.js`.

3. **TourCMS Sync & Meta CAPI Backend**:
   - `.env:9-15`:
     - `TOURCMS_MARKETPLACE_ID=57509`
     - `TOURCMS_CHANNEL_ID=16485`
     - `TOURCMS_API_KEY=51405b89d978`
     - `META_PIXEL_ID=1355732169631751`
   - `api/cron.py:277-288`:
     - Net margin calculation: `commission_value = sales_revenue - balance` (25% margin on Legenda channel 16485).
   - `api/cron.py:320-370`:
     - Sends server-side `Purchase` to Meta CAPI with `user_data` (`em`, `ph`, `fn`, `ln`, `fbc`, `fbp`) and `value: booking["commission_value"]`.
   - `tourcms-sync.js:25-27`:
     - Captures only `fbclid`, `_fbp`, `gclid`/`wbraid`/`gbraid`. Drops all UTM parameters (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`).

4. **Pixel ID Split**:
   - `.env:15` & `legenda-city-cruises.html:28`: `fbq('init', '1355732169631751');`
   - `dinner_desktop_wide_preview.html:85` & `river_desktop_wide_preview.html:278`: `fbq('init', '889886707052830');`

5. **Linguana 30-Language Deployment**:
   - `river.html:86`, `dinner.html:86`, `river-ecom.html:86`: `const LINGUANA_LANGUAGE_ROUTES = [...]` defines exactly 30 languages.
   - 5 target active languages: `en` (default canonical root), `de`, `it`, `fr`, `es`.
   - 25 machine-translated zombie languages: `cs`, `bg`, `zh`, `vi`, `uk`, `ar`, `sv`, `sr`, `el`, `fi`, `da`, `th`, `hr`, `nl`, `no`, `sk`, `tr`, `ko`, `ru`, `pt`, `ja`, `ro`, `he`, `pl`, `hu`.
   - Each language features unique translated slugs (e.g. Czech `/cs/nejlepší-budapest-řeka-plavby`, Arabic `/ar/أفضل-رحلات-العشاء-البحرية-في-نهر-بودابست`).

6. **Vercel Configuration Schema Conflict**:
   - `vercel.json:14-27`: Uses legacy `"routes": [...]`.
   - Vercel specification states that `"routes"` cannot coexist with `"redirects"`, `"rewrites"`, or `"cleanUrls"`.

---

## 2. Logic Chain

1. **Attribution Loss via Legenda Partner Typo**:
   - Observation 1 demonstrates that Legenda partner ID `38585` is used across all historical production templates and scripts, whereas `38885` is isolated to newly drafted terminal mockups (`legenda-city-cruises.html`, `legenda.html`, `direct_checkout_mockup.html`).
   - If traffic is sent to `legenda-city-cruises.html`, ticket sales will register under affiliate account `38885` rather than Adam's VIP account `38585`, severing the €130,000+ commercial credential.
   - Therefore, `38885` must be corrected to `38585` immediately.

2. **Traffic Bleed on Decision Hub**:
   - Observation 2 proves that `danube_cruise_decision_hub.html` has zero tracking scripts and un-tagged outbound links (`legenda.hu` and `silver-line.hu`).
   - Any visitor clicking outbound CTAs from this hub will convert with zero partner commission credited and zero pixel event signals.
   - Therefore, the decision hub must have partner tags appended to links and include the universal tracking script.

3. **Incomplete Attribution Pipeline in `tourcms-sync.js`**:
   - Observation 3 shows that while TourCMS and Meta CAPI sync successfully capture click IDs (`fbclid`, `gclid`), campaign-level marketing metadata (`utm_source`, `utm_campaign`, etc.) is dropped before reaching outbound links.
   - Furthermore, client-side cookie storage without `localStorage` fallback is vulnerable to browser ITP restrictions.
   - Therefore, an enhanced tracking script (`bpa-tracking.js`) must be deployed that stores both click IDs and UTMs in dual cookie + `localStorage` storage and decorates all partner domains (`legenda.hu`, `tourcms.com`, `tiqets.com`, `budapestrivercruise.eu`, `silver-line.hu`, `budapestxplore.com`).

4. **Conversion Value Divergence**:
   - Observation 3 & 4 show that `legenda-city-cruises.html` fires client-side `InitiateCheckout` with gross retail ticket price (€50.00 – €220.00), while `tourcms-sync.js` and `api/cron.py` report net commission (€6.25 – €27.50).
   - This 75% discrepancy between client checkout intent and server purchase fulfillment distorts Meta Ads value-based bidding.
   - Therefore, conversion tracking should standardize on net commission value across all funnel stages.

5. **SEO Risk in Multilingual Pruning**:
   - Observation 5 confirms that Linguana machine-translated paths created hundreds of indexed URLs across 25 languages with localized foreign-character slugs.
   - If pruned paths are redirected via a generic rule `/:lang/:path* -> /:path*`, incoming requests for translated slugs will land on 404 pages on the English site.
   - Therefore, explicit 1-to-1 301 mappings must be deployed for each known localized slug to `/best-budapest-river-cruises` and `/best-dinner-cruises-budapest`, followed by a fallback rule.

6. **Deployment Failure Prevention in `vercel.json`**:
   - Observation 6 shows `vercel.json` currently uses `"routes"`.
   - Adding a `"redirects"` array to this file will cause Vercel deployment builds to crash.
   - Therefore, `vercel.json` must be fully refactored into modern top-level `"redirects"`, `"rewrites"`, and `"cleanUrls"` properties.

---

## 3. Caveats

1. **Live Production DNS Unchecked**: In accordance with project integrity constraints, live DNS (`35.187.176.9` / Linguana proxy) was not modified or tested live. All redirect verification must be performed on Vercel preview deployments.
2. **Tiqets Partner Contract ID**: Mockups reference `thecruisedetective.com-176436`. If Budapest Adventures holds a dedicated sub-account handle on Tiqets (e.g. `budapestadventures`), that exact string should be verified before final production traffic routing.

---

## 4. Conclusion

The survey phase has identified five critical technical and commercial risks that must be resolved during the implementation phase on `staging/static-overhaul`:
1. Fix the Legenda affiliate typo from `partner=38885` to `partner=38585` on `legenda-city-cruises.html`.
2. Add missing partner parameters and tracking scripts to `danube_cruise_decision_hub.html`.
3. Deploy unified tracking safeguard script (`bpa-tracking.js`) capturing UTMs, click IDs, and dual cookie/localStorage persistence.
4. Retire legacy Pixel ID `889886707052830` and harmonize conversion values to net commission margin.
5. Deploy complete 301 redirect architecture in `vercel.json` for all 25 pruned Linguana languages, mapping exact localized slugs to canonical English targets without 404 errors.

---

## 5. Verification Method

To independently verify these findings:
1. **Grep Partner ID Typo**:
   ```bash
   grep -rn "partner=38885" /Users/adamdimitrov/Development/budapest-adventures/
   ```
   *Expected result*: Matches in `legenda-city-cruises.html`, `legenda.html`, `direct_checkout_mockup.html`.
2. **Grep Verified VIP Partner ID**:
   ```bash
   grep -rn "partner=38585" /Users/adamdimitrov/Development/budapest-adventures/
   ```
   *Expected result*: Matches in `river.html`, `dinner.html`, `live_dinner_embed.html`, `all_7_cruises_complete.html`, `generate_full_river_deck.py`.
3. **Verify Decision Hub Links**:
   ```bash
   grep -n "href=\"https://legenda" /Users/adamdimitrov/Development/budapest-adventures/danube_cruise_decision_hub.html
   ```
   *Expected result*: Line 467 shows bare `https://legenda.hu` without query parameters.
4. **Inspect Full Survey Report**:
   Read `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_explorer_survey_3/survey_tracking_i18n.md`.
