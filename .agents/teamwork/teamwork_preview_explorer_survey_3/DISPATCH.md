# DISPATCH — Explorer Survey 3 (Tracking Safeguards & Internationalization Pruning)

## Target
Survey outbound booking links, tracking query strings, Meta Pixel triggers, and Linguana multilingual routing / 301 redirect architecture.

## Instructions
1. Read `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md` and commercial context in `/Users/adamdimitrov/Development/budapest-adventures/GEMINI.md`.
2. Inspect outbound booking links across all hubs:
   - Legenda booking links
   - TourCMS booking links / webhooks / sync scripts
   - Tiqets partner links (`budapestadventures`)
3. Check query string preservation (gclid, fbclid, UTM parameters, referrer pass-through).
4. Inspect Meta Pixel implementation (`InitiateCheckout` triggers on buttons, cards, interactive filters).
5. Audit Linguana multilingual routes:
   - Identify active language folders/routes (en, de, it, fr, es vs zero-click machine-translated zombie paths).
   - Check existing redirect rules in `vercel.json` (or lack thereof).
   - Determine complete 301/308 redirect mapping rules needed for pruned zombie routes.
6. Write your comprehensive survey report to `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_explorer_survey_3/survey_tracking_i18n.md`.
7. Write `handoff.md` and send message to orchestrator.


## 2026-11-06T02:22:47Z
Message received from orchestrator (d93f7e16-54b1-470e-ae73-62c9d55a912a):
You are Survey Explorer 3 (Tracking Safeguards & Internationalization Pruning).
Your working directory is: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_explorer_survey_3`
Project root: `/Users/adamdimitrov/Development/budapest-adventures`
Mandatory: Read `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md` before starting work.
Also read `/Users/adamdimitrov/Development/budapest-adventures/GEMINI.md` for commercial context (Legenda €130k VIP channel).
Also read your assignment in `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_explorer_survey_3/DISPATCH.md`.

Your mission:
1. Inspect all outbound booking links on core hubs:
   - Legenda City Cruises direct links
   - TourCMS booking links, API sync scripts, and webhooks
   - Tiqets partner links (`budapestadventures`)
2. Inspect query string preservation logic (ensuring gclid, fbclid, UTM tags are preserved on outbound links and interactive elements).
3. Inspect Meta Pixel tracking and `InitiateCheckout` triggers on buttons, cards, and reservation engines.
4. Audit Linguana multilingual routes:
   - Find which languages are present (en, de, it, fr, es vs zero-click machine-translated paths).
   - Check `vercel.json` for current redirect rules.
   - Formulate a complete 301/308 redirect mapping from pruned zombie paths to canonical targets.
5. Document all findings, links, script snippets, and recommended redirect mappings in:
   `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_explorer_survey_3/survey_tracking_i18n.md`
6. Write `handoff.md` in your working directory and send a message back to the orchestrator.
