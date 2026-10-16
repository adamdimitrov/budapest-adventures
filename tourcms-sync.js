document.addEventListener('DOMContentLoaded', () => {
    // Helper function to extract query parameters
    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    // Helper function to set cookie
    function setCookie(name, value, days) {
        const d = new Date();
        d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
        let expires = "expires=" + d.toUTCString();
        document.cookie = name + "=" + value + ";" + expires + ";path=/";
    }

    // Helper function to get cookie
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    // 1. Capture fbclid and gclid from URL
    const fbclid = getQueryParam('fbclid');
    const gclid = getQueryParam('gclid');

    if (fbclid) setCookie('tc_fbclid', fbclid, 30);
    if (gclid) setCookie('tc_gclid', gclid, 30);

    // 2. Retrieve them from cookies if not in URL
    const savedFbclid = fbclid || getCookie('tc_fbclid');
    const savedGclid = gclid || getCookie('tc_gclid');

    // 3. Build the tracking ID (e.g. fbclid:xxx|gclid:yyy)
    let trackingValues = [];
    if (savedFbclid) trackingValues.push(`fbclid:${savedFbclid}`);
    if (savedGclid) trackingValues.push(`gclid:${savedGclid}`);
    
    if (trackingValues.length === 0) return; // Nothing to append
    
    const trackingString = trackingValues.join('|');

    // 4. Update all outbound links to Tiqets, Legenda, Silverline, etc.
    const links = document.querySelectorAll('a');
    
    links.forEach(link => {
        try {
            const url = new URL(link.href);
            if (url.hostname.includes('tiqets.com')) {
                url.searchParams.set('subid', trackingString);
                url.searchParams.set('click_id', trackingString);
                link.href = url.toString();
            } else if (url.hostname.includes('legenda.hu') || 
                       url.hostname.includes('budapestrivercruise.eu')) {
                // Append the tracking data as 'subid'
                url.searchParams.set('subid', trackingString);
                link.href = url.toString();
            }
        } catch (e) {
            // Ignore invalid URLs (e.g., javascript:void(0), #, etc.)
        }
    });
});
