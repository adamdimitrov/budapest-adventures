# Original User Request

## Initial Request — 2026-11-06T02:19:49Z

# Teamwork Project Prompt — Budapest Adventures

> Status: Launched
> Goal: Multi-agent overhaul of Budapest Adventures (Staging Architecture)
> Integrity mode: development
> Working directory: /Users/adamdimitrov/Development/budapest-adventures

Build a staging-first static architecture overhaul for Budapest Adventures (`budapestadventures.com`) on a dedicated branch (`staging/static-overhaul`) that eliminates Webflow/Linguana DOM bloat and broken `#` anchor fragments, prunes zero-click zombie language paths with 301 redirects, protects the €130k+ Legenda City Cruises & TourCMS direct booking tracking pipelines, and rebuilds the core revenue hubs locally for instant Vercel preview without touching live production DNS.

Working directory: `/Users/adamdimitrov/Development/budapest-adventures`
Integrity mode: development

## Requirements

### R1. Staging Isolation & Core Money Hubs Pipeline
Build a local and staging-preview environment on a dedicated branch (`staging/static-overhaul`) for Budapest Adventures' top revenue-generating hubs without modifying live production DNS (`35.187.176.9` / Linguana / Webflow):
1. **Danube River Cruises Main Hub** (`/` and `/budapest-river-cruises`)
2. **Budapest Dinner Cruises Hub** (`/budapest-dinner-cruises`)
3. **Candlelit Dinner Cruise Tested Review** (`/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`)
4. **Legenda City Cruises Dedicated Terminal** (`/legenda-city-cruises`)
5. **Danube Cruise Decision Hub & Filter Engines** (`danube_cruise_decision_hub.html`)

### R2. HCU & Webflow Anchor Pollution Elimination
- Strip all legacy Webflow table-of-contents hash fragments (`#...`), unicode artifacts, and duplicated CMS anchor IDs from the codebase.
- Replace with clean semantic HTML5 IDs and self-referencing canonical tags pointing strictly to clean root URLs.

### R3. Internationalization Pruning & 301 Redirect Architecture
- Audit Linguana multilingual routes: retain high-volume converting languages (e.g. English `en`, German `de`, Italian `it`, French `fr`, Spanish `es`) while pruning zero-click automated machine-translated zombie paths.
- Generate comprehensive 301/308 redirect mapping in `vercel.json` pointing all pruned paths back to their canonical targets.

### R4. Legenda (€130k VIP Channel) & TourCMS Tracking Safeguards
- 100% verification that all outbound Legenda booking links, TourCMS API webhooks, and Tiqets partner IDs (`budapestadventures`) retain complete tracking query strings (`gclid`, `fbclid`, UTMs).
- Verify Meta Pixel InitiateCheckout tracking triggers on all interactive decision cards and reservation buttons.

## Verification Resources
- Project root: `/Users/adamdimitrov/Development/budapest-adventures`
- Existing sync & test tools: `tourcms-sync.js`, `test_tourcms.py`, `sync_ratings.sh`, `api/cron.py`
- Commercial context: `GEMINI.md` (Top VIP partner for Legenda, €130,000+ volume)

## Acceptance Criteria

### Technical & SEO Quality
- [ ] 100% of staging pages have clean canonical tags containing 0 `#` fragments.
- [ ] `sitemap.xml` generated strictly containing valid canonical hubs across active approved languages.
- [ ] `vercel.json` contains complete 301 redirect rules for all pruned zombie URLs.

### E-Commerce & Distribution Integrity
- [ ] 100% of outbound booking buttons (Legenda, TourCMS, Tiqets) preserve partner tracking and click IDs.
- [ ] Zero broken booking links or console errors on core decision hubs.

### Delivery & Safety
- [ ] Live production DNS (`35.187.176.9` / Linguana / Webflow) remains untouched.
- [ ] Local build and Vercel staging deployment verified and previewable before any merge.
