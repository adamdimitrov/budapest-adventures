(function() {
    function getQueryParam(param) {
        if (typeof window === 'undefined' || !window.location) return null;
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    function setCookie(name, value, days) {
        if (typeof document === 'undefined') return;
        const d = new Date();
        d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "expires=" + d.toUTCString();
        document.cookie = name + "=" + encodeURIComponent(value) + ";" + expires + ";path=/";
    }

    function getCookie(name) {
        if (typeof document === 'undefined') return null;
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift());
        return null;
    }

    // 1. Capture fbclid, _fbp, and gclid/wbraid/gbraid from URL or persist via cookies
    const fbclid = getQueryParam('fbclid');
    const gclid = getQueryParam('gclid') || getQueryParam('wbraid') || getQueryParam('gbraid');
    const gclidType = getQueryParam('gclid') ? 'gclid' : (getQueryParam('wbraid') ? 'wbraid' : (getQueryParam('gbraid') ? 'gbraid' : 'gclid'));

    if (fbclid) setCookie('tc_fbclid', fbclid, 30);
    if (gclid) {
        setCookie('tc_gclid', gclid, 30);
        setCookie('tc_gclid_type', gclidType, 30);
    }

    const savedFbclid = fbclid || getCookie('tc_fbclid');
    const savedGclid = gclid || getCookie('tc_gclid');
    const savedGclidType = gclid ? gclidType : (getCookie('tc_gclid_type') || 'gclid');
    const fbpCookie = getCookie('_fbp');

    // Build tracking string (e.g. fbclid:xxx|fbp:fb.1.xxx|gclid:yyy)
    const trackingValues = [];
    if (savedFbclid) trackingValues.push(`fbclid:${savedFbclid}`);
    if (fbpCookie) trackingValues.push(`fbp:${fbpCookie}`);
    if (savedGclid) trackingValues.push(`${savedGclidType}:${savedGclid}`);
    const trackingString = trackingValues.join('|');

    // Partner domains that represent booking checkout actions
    const PARTNER_DOMAINS = [
        'legenda.hu',
        'tourcms.com',
        'budapestrivercruise.eu',
        'tiqets.com'
    ];

    function isPartnerBookingLink(hostname) {
        if (!hostname) return false;
        return PARTNER_DOMAINS.some(domain => hostname.includes(domain));
    }

    // Helper to determine estimated NET COMMISSION value (not gross retail) and product title
    function getBookingContext(linkEl) {
        const path = (typeof window !== 'undefined' && window.location.pathname) ? window.location.pathname.toLowerCase() : '';
        const href = (linkEl && linkEl.href) ? linkEl.href.toLowerCase() : '';
        const text = (linkEl && linkEl.textContent) ? linkEl.textContent.toLowerCase() : '';

        // Default values: Legenda Evening Sightseeing (Danube Legend €25 retail -> €6.25 net commission per adult, ~2 adults = €12.50)
        let contentName = 'Legenda Budapest Sightseeing Cruise';
        let retailPrice = 25.00;
        let commissionRate = 0.25; // 25% verified TourCMS net margin on Legenda (Channel 16485)

        if (path.includes('dinner') || href.includes('dinner') || href.includes('candlelit') || href.includes('t=3') || text.includes('dinner')) {
            contentName = 'Legenda Budapest Candlelit Dinner Cruise';
            retailPrice = 110.00; // €110 retail -> €27.50 net commission per adult
        } else if (href.includes('bella') || href.includes('t=1') || text.includes('daytime')) {
            contentName = 'Legenda Duna Bella Daytime Cruise';
            retailPrice = 20.00; // €20 retail -> €5.00 net commission per adult
        } else if (path.includes('prosecco') || href.includes('prosecco') || text.includes('prosecco') || text.includes('unlimited')) {
            contentName = 'Budapest Unlimited Drinks Cruise';
            retailPrice = 25.00;
        } else if (href.includes('budapestrivercruise.eu')) {
            contentName = 'Silverline Budapest River Cruise';
            retailPrice = path.includes('dinner') ? 85.00 : 25.00;
        }

        try {
            const card = linkEl.closest('.table-row-grey-3, .table-row, .cruise-card, .grid-cell-3, tr');
            if (card) {
                const priceEl = card.querySelector('.price-3, .price-2, .price-6, .text-span-7, strong');
                if (priceEl && priceEl.textContent) {
                    const priceMatch = priceEl.textContent.match(/(\d+(?:\.\d+)?)\s*€|€\s*(\d+(?:\.\d+)?)/);
                    if (priceMatch) {
                        const parsed = parseFloat(priceMatch[1] || priceMatch[2]);
                        if (!isNaN(parsed) && parsed > 0) {
                            retailPrice = parsed;
                        }
                    }
                }
            }
        } catch (e) {}

        const estimatedCommission = Math.round(retailPrice * commissionRate * 100) / 100;
        return { contentName, estimatedValue: estimatedCommission, retailPrice };
    }

    // Decorate outbound link with tracking parameters
    function decorateLink(link) {
        if (!link || !link.href || !trackingString) return;
        try {
            const url = new URL(link.href);
            if (url.hostname.includes('tiqets.com')) {
                url.searchParams.set('subid', trackingString);
                url.searchParams.set('click_id', trackingString);
                link.href = url.toString();
            } else if (url.hostname.includes('legenda.hu') || url.hostname.includes('tourcms.com')) {
                // subid only: partner=38585 / agent_ref=38585 are set by bpa-tracking.js
                // and must never be overwritten with the tracking string.
                url.searchParams.set('subid', trackingString);
                link.href = url.toString();
            }
            // Silverline (budapestrivercruise.eu) links stay as ?code=bpadventures only.
        } catch (e) {
            // Ignore invalid URLs
        }
    }

    function decorateAllLinks() {
        if (typeof document === 'undefined' || !trackingString) return;
        const links = document.querySelectorAll('a');
        links.forEach(decorateLink);
    }

    document.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (!link || !link.href) return;

        try {
            const url = new URL(link.href);
            if (!isPartnerBookingLink(url.hostname)) return;

            decorateLink(link);

            const { contentName, estimatedValue, retailPrice } = getBookingContext(link);

            if (typeof window.fbq === 'function') {
                window.fbq('track', 'InitiateCheckout', {
                    content_name: contentName,
                    content_category: 'River Cruise',
                    value: estimatedValue,
                    currency: 'EUR'
                });
            }

            if (typeof window.dataLayer !== 'undefined' && Array.isArray(window.dataLayer)) {
                window.dataLayer.push({
                    event: 'initiate_checkout_partner',
                    partner: url.hostname,
                    content_name: contentName,
                    value: estimatedValue,
                    retail_price: retailPrice,
                    currency: 'EUR'
                });
            }
        } catch (err) {}
    }, true);

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', decorateAllLinks);
    } else {
        decorateAllLinks();
    }
})();
