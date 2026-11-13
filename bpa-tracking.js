/**
 * Budapest Adventures — Unified Attribution, Dual-Storage Sync & Outbound Link Decorator
 * File: bpa-tracking.js
 *
 * Features covered:
 * - Feature 15: Authoritative Legenda VIP Partner ID (partner=38585; replaces legacy 38885)
 *   Standard link: https://legenda.hu/en?partner=38585
 * - Feature 16: Decision Hub & Multi-Operator Outbound Tracking (Legenda, TourCMS, Tiqets, Silverline)
 * - Feature 17: Inbound UTM & Click ID Capture (gclid, fbclid, _fbp, wbraid, gbraid, utm_*)
 * - Feature 18: Bidirectional Cookie + localStorage Persistence (bpa_attribution, 30-day TTL, Safari ITP/Private mode safe)
 * - Feature 19: Standardized Meta Pixel (1355732169631751) InitiateCheckout with 25% Net Commission Value in EUR
 * - Feature 20: Tiqets Partner Handle Preservation (partner=budapestadventures)
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'bpa_attribution';
  var COOKIE_MAX_AGE = 2592000; // 30 days in seconds (30 * 24 * 60 * 60)
  var TTL_MS = COOKIE_MAX_AGE * 1000;
  var META_PIXEL_ID = '1355732169631751';
  var VIP_LEGENDA_PARTNER = '38585';
  var TYPO_LEGENDA_PARTNER = '38885';
  var TOURCMS_AGENT_REF = '38585';
  var TIQETS_PARTNER = 'budapestadventures';
  var SILVERLINE_PARTNER = 'budapestadventures';
  var SILVERLINE_CODE = 'bpadventures';
  var NET_COMMISSION_RATE = 0.25;
  var CLARITY_PROJECT_ID = 'zap3ccm9my';

  var TRACKED_PARAMS = [
    'gclid',
    'fbclid',
    '_fbp',
    'wbraid',
    'gbraid',
    'utm_source',
    'utm_medium',
    'utm_campaign',
    'utm_term',
    'utm_content'
  ];

  var PARTNER_DOMAINS = [
    'legenda.hu',
    'tourcms.com',
    'budapestrivercruise.eu',
    'tiqets.com',
    'silver-line.hu'
  ];

  /**
   * Read a cookie value by name from document.cookie.
   */
  function getCookie(name) {
    if (typeof document === 'undefined' || !document.cookie) return null;
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var part = cookies[i].trim();
      if (part.indexOf(name + '=') === 0) {
        var raw = part.substring(name.length + 1);
        try {
          return decodeURIComponent(raw);
        } catch (err) {
          return raw;
        }
      }
    }
    return null;
  }

  /**
   * Write a cookie with 30-day max-age, expires fallback, root path=/, and SameSite=Lax.
   */
  function setCookie(name, value) {
    if (typeof document === 'undefined') return;
    try {
      var expiresDate = new Date(Date.now() + TTL_MS).toUTCString();
      var encoded = encodeURIComponent(value);
      // Persist with both max-age=2592000 and expires for full browser compatibility
      document.cookie =
        name +
        '=' +
        encoded +
        '; max-age=' +
        COOKIE_MAX_AGE +
        '; expires=' +
        expiresDate +
        '; path=/; SameSite=Lax';
    } catch (err) {
      // Ignore cookie write restriction errors
    }
  }

  /**
   * Parse JSON safely with fallback to null on corrupted payloads.
   */
  function safeJsonParse(raw) {
    if (!raw || typeof raw !== 'string') return null;
    try {
      var parsed = JSON.parse(raw);
      if (parsed && typeof parsed === 'object') {
        return parsed;
      }
    } catch (err) {
      return null;
    }
    return null;
  }

  /**
   * Read attribution object from localStorage (wrapped in try/catch for Safari Private Browsing).
   */
  function readLocalStorage() {
    if (typeof window === 'undefined' || !window.localStorage) return null;
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      return safeJsonParse(raw);
    } catch (err) {
      return null;
    }
  }

  /**
   * Write attribution object to localStorage (wrapped in try/catch for QuotaExceededError / Private Browsing).
   */
  function writeLocalStorage(data) {
    if (typeof window === 'undefined' || !window.localStorage) return;
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (err) {
      // Safari Private Browsing or QuotaExceededError safe fallback
    }
  }

  /**
   * Bidirectional storage recovery and synchronization:
   * Restores from localStorage or document.cookie (bpa_attribution) if either is cleared,
   * validates 30-day TTL, and re-syncs both stores.
   */
  function loadAndSyncAttribution() {
    var fromStorage = readLocalStorage();
    var fromCookie = safeJsonParse(getCookie(STORAGE_KEY));
    var now = Date.now();

    // Check TTL expiration (30 days)
    if (fromStorage && fromStorage._ts && now - fromStorage._ts > TTL_MS) {
      fromStorage = null;
    }
    if (fromCookie && fromCookie._ts && now - fromCookie._ts > TTL_MS) {
      fromCookie = null;
    }

    var merged = {};
    if (fromCookie) {
      for (var k1 in fromCookie) {
        if (Object.prototype.hasOwnProperty.call(fromCookie, k1) && fromCookie[k1]) {
          merged[k1] = fromCookie[k1];
        }
      }
    }
    if (fromStorage) {
      for (var k2 in fromStorage) {
        if (Object.prototype.hasOwnProperty.call(fromStorage, k2) && fromStorage[k2]) {
          merged[k2] = fromStorage[k2];
        }
      }
    }

    // Capture inbound URL query parameters from window.location.search
    if (typeof window !== 'undefined' && window.location && window.location.search) {
      try {
        var searchParams = new URLSearchParams(window.location.search);
        for (var i = 0; i < TRACKED_PARAMS.length; i++) {
          var paramKey = TRACKED_PARAMS[i];
          var paramVal = searchParams.get(paramKey);
          if (paramVal && paramVal.trim() !== '') {
            merged[paramKey] = paramVal.trim();
          }
        }
      } catch (err) {
        // Fallback if URLSearchParams fails on malformed query string
      }
    }

    // Also capture first-party _fbp cookie if present and not already in URL
    if (!merged._fbp) {
      var fbpCookie = getCookie('_fbp');
      if (fbpCookie) {
        merged._fbp = fbpCookie;
      }
    }

    if (Object.keys(merged).length > 0) {
      if (!merged._ts) {
        merged._ts = now;
      }
      var serialized = JSON.stringify(merged);
      setCookie(STORAGE_KEY, serialized);
      writeLocalStorage(merged);
    }

    return merged;
  }

  /**
   * Build serialized subid string for partner checkout attribution.
   */
  function buildSubId(attribution) {
    if (!attribution) return '';
    var parts = [];
    if (attribution.gclid) {
      parts.push('g_' + attribution.gclid);
    } else if (attribution.wbraid) {
      parts.push('wb_' + attribution.wbraid);
    } else if (attribution.gbraid) {
      parts.push('gb_' + attribution.gbraid);
    }
    if (attribution.fbclid) {
      parts.push('f_' + attribution.fbclid);
    }
    if (attribution.utm_campaign) {
      parts.push('c_' + attribution.utm_campaign);
    }
    if (attribution.utm_source && parts.length === 0) {
      parts.push('s_' + attribution.utm_source);
    }
    return parts.join('_');
  }

  /**
   * Decorate an outbound URL string with partner credentials and campaign attribution.
   */
  function decorateOutboundUrl(rawHref, attribution) {
    if (!rawHref || typeof rawHref !== 'string') return rawHref;
    var attr = attribution || {};
    try {
      var base =
        typeof window !== 'undefined' && window.location && window.location.origin
          ? window.location.origin
          : 'https://www.budapestadventures.com';
      var url = new URL(rawHref, base);
      var host = url.hostname.toLowerCase();
      var subId = buildSubId(attr);

      // 1. Legenda City Cruises (Authoritative VIP Partner 38585: https://legenda.hu/en?partner=38585)
      if (host.indexOf('legenda.hu') !== -1) {
        var existingPartner = url.searchParams.get('partner');
        if (!existingPartner || existingPartner === TYPO_LEGENDA_PARTNER || existingPartner !== VIP_LEGENDA_PARTNER) {
          url.searchParams.set('partner', VIP_LEGENDA_PARTNER);
        }
        if (subId) {
          url.searchParams.set('subid', subId);
        }
        return url.toString();
      }

      // 2a. Silverline (budapestrivercruise.eu): our agent code is ?code=bpadventures.
      //     agent_ref=38585 is the Legenda/TourCMS account and must not be sent here.
      if (host.indexOf('budapestrivercruise.eu') !== -1) {
        url.searchParams.delete('agent_ref');
        if (url.searchParams.get('code') !== SILVERLINE_CODE) {
          url.searchParams.set('code', SILVERLINE_CODE);
        }
        return url.toString();
      }

      // 2b. TourCMS
      if (host.indexOf('tourcms.com') !== -1) {
        url.searchParams.set('agent_ref', TOURCMS_AGENT_REF);
        if (subId) {
          url.searchParams.set('subid', subId);
        }
        if (attr.gclid) {
          url.searchParams.set('tc_gclid', attr.gclid);
          url.searchParams.set('tc_gclid_type', 'gclid');
        } else if (attr.wbraid) {
          url.searchParams.set('tc_gclid', attr.wbraid);
          url.searchParams.set('tc_gclid_type', 'wbraid');
        } else if (attr.gbraid) {
          url.searchParams.set('tc_gclid', attr.gbraid);
          url.searchParams.set('tc_gclid_type', 'gbraid');
        }
        if (attr.fbclid) {
          url.searchParams.set('tc_fbclid', attr.fbclid);
        }
        if (attr._fbp) {
          url.searchParams.set('_fbp', attr._fbp);
        }
        return url.toString();
      }

      // 3. Tiqets
      if (host.indexOf('tiqets.com') !== -1) {
        url.searchParams.set('partner', TIQETS_PARTNER);
        if (attr.utm_campaign) {
          url.searchParams.set('utm_campaign', attr.utm_campaign);
        }
        if (subId) {
          url.searchParams.set('subid', subId);
          url.searchParams.set('click_id', subId);
        }
        return url.toString();
      }

      // 4. Silverline Cruises
      if (host.indexOf('silver-line.hu') !== -1) {
        if (!url.searchParams.get('partner')) {
          url.searchParams.set('partner', SILVERLINE_PARTNER);
        }
        if (subId) {
          url.searchParams.set('subid', subId);
        }
        return url.toString();
      }

      return rawHref;
    } catch (err) {
      return rawHref;
    }
  }

  /**
   * Check whether a hostname belongs to an outbound booking partner.
   */
  function isPartnerHostname(hostname) {
    if (!hostname) return false;
    var lower = hostname.toLowerCase();
    for (var i = 0; i < PARTNER_DOMAINS.length; i++) {
      if (lower.indexOf(PARTNER_DOMAINS[i]) !== -1) {
        return true;
      }
    }
    return false;
  }

  /**
   * Calculate 25% net commission in EUR for Meta Pixel InitiateCheckout event.
   */
  function calculateNetCommission(retailEur, rate) {
    var commissionRate = typeof rate === 'number' ? rate : NET_COMMISSION_RATE;
    var numericPrice = parseFloat(retailEur);
    if (isNaN(numericPrice) || numericPrice <= 0) return 0.0;
    return Math.round(numericPrice * commissionRate * 100) / 100;
  }

  /**
   * Infer booking product context & net commission value in EUR from clicked anchor element.
   */
  function getCheckoutPayload(linkEl) {
    var path =
      typeof window !== 'undefined' && window.location && window.location.pathname
        ? window.location.pathname.toLowerCase()
        : '';
    var href = linkEl && linkEl.href ? linkEl.href.toLowerCase() : '';
    var text = linkEl && linkEl.textContent ? linkEl.textContent.toLowerCase() : '';

    var contentName = 'Legenda Budapest Sightseeing Cruise';
    var retailPrice = 18.0;

    if (
      path.indexOf('candlelit') !== -1 ||
      href.indexOf('candlelit') !== -1 ||
      text.indexOf('candlelit') !== -1
    ) {
      contentName = 'Legenda Budapest Candlelit Dinner Cruise';
      retailPrice = 85.0;
    } else if (
      path.indexOf('dinner') !== -1 ||
      href.indexOf('dinner') !== -1 ||
      text.indexOf('dinner') !== -1
    ) {
      contentName = 'Budapest Danube Dinner Cruise';
      retailPrice = 85.0;
    } else if (
      href.indexOf('silver-line.hu') !== -1 ||
      href.indexOf('budapestrivercruise.eu') !== -1
    ) {
      contentName = 'Silverline Budapest River Cruise';
      retailPrice = 25.0;
    } else if (href.indexOf('tiqets.com') !== -1) {
      contentName = 'Budapest River Cruise (Tiqets)';
      retailPrice = 22.0;
    }

    // Attempt to read explicit data-price attribute if present on element or card
    if (linkEl && linkEl.getAttribute) {
      var dataPrice = linkEl.getAttribute('data-price');
      if (dataPrice && !isNaN(parseFloat(dataPrice))) {
        retailPrice = parseFloat(dataPrice);
      }
    }

    var netCommissionValue = calculateNetCommission(retailPrice, NET_COMMISSION_RATE);
    return {
      content_name: contentName,
      content_category: 'River Cruise',
      value: netCommissionValue,
      currency: 'EUR'
    };
  }

  /**
   * Ensure Microsoft Clarity (zap3ccm9my) is loaded if not already initialized by page head.
   */
  function ensureClarity() {
    if (typeof window === 'undefined') return;
    if (typeof window.clarity === 'function') return;
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", CLARITY_PROJECT_ID);
  }

  /**
   * Ensure Meta Pixel (1355732169631751) stub is available if not already initialized by page head.
   */
  function ensureMetaPixel() {
    if (typeof window === 'undefined') return;
    if (typeof window.fbq === 'function') return;
    var f = window;
    var b = document;
    var e = 'script';
    var v = 'https://connect.facebook.net/en_US/fbevents.js';
    var n, t, s;
    if (f.fbq) return;
    n = f.fbq = function () {
      n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    };
    if (!f._fbq) f._fbq = n;
    n.push = n;
    n.loaded = true;
    n.version = '2.0';
    n.queue = [];
    t = b.createElement(e);
    t.async = true;
    t.src = v;
    s = b.getElementsByTagName(e)[0];
    if (s && s.parentNode) {
      s.parentNode.insertBefore(t, s);
    }
    window.fbq('init', META_PIXEL_ID);
    window.fbq('track', 'PageView');
  }

  /**
   * Decorate all outbound partner links on the page.
   */
  function decorateAllPageLinks(attribution) {
    if (typeof document === 'undefined' || !document.querySelectorAll) return;
    var links = document.querySelectorAll('a[href]');
    for (var i = 0; i < links.length; i++) {
      var link = links[i];
      var rawHref = link.getAttribute('href');
      if (!rawHref || rawHref.indexOf('#') === 0 || rawHref.indexOf('javascript:') === 0) {
        continue;
      }
      var decorated = decorateOutboundUrl(link.href || rawHref, attribution);
      if (decorated && decorated !== link.href) {
        link.href = decorated;
      }
    }
  }

  // Initialize attribution & link decoration on load
  var activeAttribution = loadAndSyncAttribution();

  function initTracking() {
    ensureClarity();
    ensureMetaPixel();
    activeAttribution = loadAndSyncAttribution();
    decorateAllPageLinks(activeAttribution);
  }

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initTracking);
    } else {
      initTracking();
    }

    // Intercept clicks on outbound partner CTAs to re-verify decoration and fire InitiateCheckout
    document.addEventListener(
      'click',
      function (event) {
        var target = event.target;
        var link = target && target.closest ? target.closest('a[href]') : null;
        if (!link || !link.href) return;

        try {
          var url = new URL(link.href, window.location.origin);
          if (!isPartnerHostname(url.hostname)) return;

          var currentAttr = loadAndSyncAttribution();
          link.href = decorateOutboundUrl(link.href, currentAttr);

          var payload = getCheckoutPayload(link);
          if (typeof window.fbq === 'function') {
            window.fbq('track', 'InitiateCheckout', {
              content_name: payload.content_name,
              content_category: payload.content_category,
              value: payload.value,
              currency: 'EUR'
            });
          }
          if (typeof window.clarity === 'function') {
            window.clarity('event', 'partner_outbound_click');
            window.clarity('set', 'partner_operator', payload.content_name);
            window.clarity('set', 'target_url', link.href);
          }
        } catch (err) {
          // Ignore malformed URL errors on click
        }
      },
      true
    );
  }

  // Expose public API for testing and manual invocation
  if (typeof window !== 'undefined') {
    window.BPATracking = {
      STORAGE_KEY: STORAGE_KEY,
      META_PIXEL_ID: META_PIXEL_ID,
      CLARITY_PROJECT_ID: CLARITY_PROJECT_ID,
      VIP_LEGENDA_PARTNER: VIP_LEGENDA_PARTNER,
      TIQETS_PARTNER: TIQETS_PARTNER,
      loadAndSyncAttribution: loadAndSyncAttribution,
      decorateOutboundUrl: decorateOutboundUrl,
      calculateNetCommission: calculateNetCommission,
      decorateAllPageLinks: decorateAllPageLinks
    };
  }
})();
