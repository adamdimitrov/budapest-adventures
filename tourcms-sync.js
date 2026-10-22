(function() {
    // Helper function to extract query parameters
    function getQueryParam(param) {
        if (typeof window === 'undefined' || !window.location) return null;
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    // Helper function to set cookie
    function setCookie(name, value, days) {
        if (typeof document === 'undefined') return;
        const d = new Date();
        d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "expires=" + d.toUTCString();
        document.cookie = name + "=" + encodeURIComponent(value) + ";" + expires + ";path=/";
    }

    // Helper function to get cookie
    function getCookie(name) {
        if (typeof document === 'undefined') return null;
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift());
        return null;
    }

    // 1. Capture fbclid and gclid from URL or persist via cookies
    const fbclid = getQueryParam('fbclid');
    const gclid = getQueryParam('gclid');

    if (fbclid) setCookie('tc_fbclid', fbclid, 30);
    if (gclid) setCookie('tc_gclid', gclid, 30);

    const savedFbclid = fbclid || getCookie('tc_fbclid');
    const savedGclid = gclid || getCookie('tc_gclid');

    // Build tracking string (e.g. fbclid:xxx|gclid:yyy)
    const trackingValues = [];
    if (savedFbclid) trackingValues.push(`fbclid:${savedFbclid}`);
    if (savedGclid) trackingValues.push(`gclid:${savedGclid}`);
    const trackingString = trackingValues.join('|');

    // Partner domains that represent booking checkout actions
    const PARTNER_DOMAINS = [
        'legenda.hu',
        'budapestrivercruise.eu',
        'tiqets.com'
    ];

    function isPartnerBookingLink(hostname) {
        if (!hostname) return false;
        return PARTNER_DOMAINS.some(domain => hostname.includes(domain));
    }

    // Helper to determine estimated booking value and product title
    function getBookingContext(linkEl) {
        const path = (typeof window !== 'undefined' && window.location.pathname) ? window.location.pathname.toLowerCase() : '';
        const href = (linkEl && linkEl.href) ? linkEl.href.toLowerCase() : '';
        const text = (linkEl && linkEl.textContent) ? linkEl.textContent.toLowerCase() : '';

        // Default values
        let contentName = 'Legenda Budapest Sightseeing Cruise';
        let estimatedValue = 22.00;

        // Check if dinner cruise
        if (path.includes('dinner') || href.includes('dinner') || href.includes('candlelit') || text.includes('dinner')) {
            contentName = 'Legenda Budapest Dinner Cruise';
            estimatedValue = 85.00;
        } else if (path.includes('prosecco') || href.includes('prosecco') || text.includes('prosecco') || text.includes('unlimited')) {
            contentName = 'Budapest Unlimited Drinks Cruise';
            estimatedValue = 25.00;
        } else if (href.includes('budapestrivercruise.eu')) {
            contentName = 'Silverline Budapest River Cruise';
            estimatedValue = path.includes('dinner') ? 85.00 : 25.00;
        }

        // Try extracting visual price nearby if rendered on the card
        try {
            const card = linkEl.closest('.table-row-grey-3, .table-row, .cruise-card, .grid-cell-3, tr');
            if (card) {
                const priceEl = card.querySelector('.price-3, .price-2, .price-6, .text-span-7, strong');
                if (priceEl && priceEl.textContent) {
                    const priceMatch = priceEl.textContent.match(/(\d+(?:\.\d+)?)\s*€|€\s*(\d+(?:\.\d+)?)/);
                    if (priceMatch) {
                        const parsed = parseFloat(priceMatch[1] || priceMatch[2]);
                        if (!isNaN(parsed) && parsed > 0) {
                            estimatedValue = parsed;
                        }
                    }
                }
            }
        } catch (e) {}

        return { contentName, estimatedValue };
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
            } else if (url.hostname.includes('legenda.hu') || url.hostname.includes('budapestrivercruise.eu')) {
                url.searchParams.set('subid', trackingString);
                link.href = url.toString();
            }
        } catch (e) {
            // Ignore invalid URLs
        }
    }

    // Scan and decorate all existing links on the page
    function decorateAllLinks() {
        if (typeof document === 'undefined' || !trackingString) return;
        const links = document.querySelectorAll('a');
        links.forEach(decorateLink);
    }

    // Intercept clicks globally in capture phase:
    // 1. Decorate link just-in-time
    // 2. Fire Meta Pixel InitiateCheckout on partner booking clicks
    document.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (!link || !link.href) return;

        try {
            const url = new URL(link.href);
            if (!isPartnerBookingLink(url.hostname)) return;

            // Just-in-time decoration to ensure subid is always appended
            decorateLink(link);

            // Fire Meta Pixel InitiateCheckout
            const { contentName, estimatedValue } = getBookingContext(link);

            if (typeof window.fbq === 'function') {
                window.fbq('track', 'InitiateCheckout', {
                    content_name: contentName,
                    content_category: 'River Cruise',
                    value: estimatedValue,
                    currency: 'EUR'
                });
            }

            // Also push to dataLayer for Google Analytics / GTM if available
            if (typeof window.dataLayer !== 'undefined' && Array.isArray(window.dataLayer)) {
                window.dataLayer.push({
                    event: 'initiate_checkout_partner',
                    partner: url.hostname,
                    content_name: contentName,
                    value: estimatedValue,
                    currency: 'EUR'
                });
            }
        } catch (err) {
            // Safe fallback
        }
    }, true);

    // Initial pass on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', decorateAllLinks);
    } else {
        decorateAllLinks();
    }
})();
