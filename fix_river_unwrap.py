import re

with open("/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_10_river_cruises.html", "r") as f:
    html = f.read()

# Let's check the current CSS and JS
# We want clean, powerful CSS and bulletproof JS execution

updated_css = """
/* === AUTO-UNWRAP 10 RIVER CRUISE REVIEWS INTO OPEN DOM === */
.div-block-27, .table-row-grey-3, .table-row-grey-3-copy,
[id^="1-"], [id^="2-"], [id^="3-"], [id^="4-"], [id^="5-"],
[id^="6-"], [id^="7-"], [id^="8-"], [id^="9-"], [id^="10-"] {
  scroll-margin-top: 90px !important;
}

/* Hide old table duplicate widgets */
.comparison-table .view-all-button,
.comparison-table .tabs-menu,
.comparison-table .grid-cell-2,
.comparison-table .div-block-21,
.comparison-table .grid-cell-5,
.comparison-table .price-2,
.comparison-table .buy-button-read-full-review,
.comparison-table .div-block-47,
.comparison-table .faq-item-toggle,
.load-more {
  display: none !important;
}

/* Transform table rows into open review cards */
.comparison-table .table-wrapper-2,
.comparison-table .table-2 {
  min-width: 0 !important;
  width: 100% !important;
  overflow: visible !important;
}
.comparison-table .table-row-grey-3,
.comparison-table .table-row-grey-3-copy {
  display: block !important;
  padding: 32px 28px !important;
  margin-bottom: 36px !important;
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 16px !important;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.05) !important;
}
.comparison-table .grid-cell-3 {
  display: block !important;
  width: 100% !important;
  padding: 0 !important;
}
.comparison-table .coin-name-wrapper {
  white-space: normal !important;
  margin-bottom: 20px !important;
  padding-bottom: 16px !important;
  border-bottom: 2px solid #f1f5f9 !important;
}
.comparison-table .coin-name-2 {
  font-size: 26px !important;
  line-height: 1.35 !important;
  font-weight: 800 !important;
  margin: 0 0 8px 0 !important;
  color: #0f172a !important;
}
.comparison-table .coin-name-2 a {
  color: #0f172a !important;
  text-decoration: none !important;
}
.comparison-table .coin-shortname {
  font-size: 14px !important;
  font-weight: 700 !important;
  color: #0284c7 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
}

/* Force open all review bodies & load-more content */
.comparison-table .faq-section,
.comparison-table .faq-container-2,
.comparison-table .faq-wrapper,
.comparison-table .faq-item,
.comparison-table nav.faq-content-wrap,
.comparison-table .faq-content-wrap.w-dropdown-list,
.comparison-table .w-dropdown-list,
.bpa-open-review-body,
.load-more-div {
  display: block !important;
  position: static !important;
  width: 100% !important;
  max-width: 100% !important;
  opacity: 1 !important;
  visibility: visible !important;
  overflow: visible !important;
  background: transparent !important;
  padding: 0 !important;
  margin: 0 !important;
  transform: none !important;
}
"""

# Replace the unwrap css section
css_start = html.find("/* === AUTO-UNWRAP")
if css_start == -1:
    css_start = html.find(".comparison-table .view-all-button")
    if css_start != -1:
        css_start = html.rfind("\n", 0, css_start)

css_end = html.find(".bpa-channel-item i {", css_start)
if css_start != -1 and css_end != -1:
    html = html[:css_start] + "\n" + updated_css.strip() + "\n" + html[css_end:]
    print("CSS updated successfully!")
else:
    print("Could not find exact CSS slice to replace!")

# Now replace the JS script block with bulletproof DOMContentLoaded + load + polling handler
updated_js = """<script>
(function() {
  const BPA_CDN = "/assets/cdn/60e43c7d6d05b671dff0dc1a/";
  
  // 1. Slider lazy images & drag
  function initSliders() {
    document.querySelectorAll(".bpa-slider[data-more]").forEach(c => {
      const m = c.getAttribute("data-more").split(",");
      m.forEach(f => {
        if (!f) return;
        const img = document.createElement("img");
        img.src = f.startsWith("http") ? f : BPA_CDN + f;
        img.loading = "lazy";
        img.alt = "Budapest River Cruise";
        c.appendChild(img);
      });
      c.removeAttribute("data-more");
      
      const tot = c.children.length;
      const cnt = c.parentElement.querySelector(".bpa-counter-pill");
      if (cnt) cnt.textContent = "1 / " + tot;
      
      let isDown = false, startX, sLeft;
      c.addEventListener("mousedown", e => {
        isDown = true;
        c.style.scrollSnapType = "none";
        startX = e.pageX - c.offsetLeft;
        sLeft = c.scrollLeft;
      });
      const stopDrag = () => {
        if (!isDown) return;
        isDown = false;
        c.style.scrollSnapType = "x mandatory";
        const w = c.offsetWidth || 1;
        const target = Math.round(c.scrollLeft / w) * w;
        c.scrollTo({ left: target, behavior: "smooth" });
      };
      c.addEventListener("mouseleave", stopDrag);
      c.addEventListener("mouseup", stopDrag);
      c.addEventListener("mousemove", e => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - c.offsetLeft;
        const walk = (x - startX) * 1.15;
        c.scrollLeft = sLeft - walk;
      });
    });
  }

  window.bpaSlide = function(btn, dir) {
    const c = btn.parentElement.querySelector(".bpa-slider");
    if (c) c.scrollBy({ left: dir * c.offsetWidth, behavior: "smooth" });
  };

  window.bpaCount = function(c) {
    if (c._ticking) return;
    c._ticking = true;
    requestAnimationFrame(() => {
      const w = c.offsetWidth || 1;
      const tot = c.children.length;
      const idx = Math.min(tot, Math.max(1, Math.round(c.scrollLeft / w) + 1));
      const cnt = c.parentElement.querySelector(".bpa-counter-pill");
      if (cnt) cnt.textContent = idx + " / " + tot;
      c._ticking = false;
    });
  };

  // 2. Robust Review Unwrapper & Anchor Hoister
  function unwrapRiverReviews() {
    const compHeading = document.getElementById("quick-summary-river-cruises-budapest") || document.querySelector(".comparison-table .heading-30");
    if (compHeading) {
      compHeading.textContent = "Detailed Breakdown — 10 Best River Cruises in Budapest";
    }

    const rows = document.querySelectorAll(".comparison-table .table-row-grey-3, .comparison-table .table-row-grey-3-copy");
    rows.forEach(row => {
      // Hoist anchor id to row card
      const innerTarget = row.querySelector('[id^="1-"], [id^="2-"], [id^="3-"], [id^="4-"], [id^="5-"], [id^="6-"], [id^="7-"], [id^="8-"], [id^="9-"], [id^="10-"]');
      if (innerTarget && innerTarget.id) {
        row.id = innerTarget.id;
        innerTarget.removeAttribute("id");
      }

      // Unwrap <nav class="faq-content-wrap"> into <div class="bpa-open-review-body">
      const navEl = row.querySelector("nav.faq-content-wrap");
      if (navEl) {
        const divEl = document.createElement("div");
        divEl.className = "bpa-open-review-body";
        while (navEl.firstChild) {
          divEl.appendChild(navEl.firstChild);
        }
        navEl.parentNode.replaceChild(divEl, navEl);
      }
    });

    // Handle incoming URL hash jump if page loaded with #hash
    if (window.location.hash) {
      const hash = window.location.hash;
      const target = document.getElementById(hash.substring(1)) || document.querySelector(hash);
      if (target) {
        setTimeout(() => {
          const targetTop = target.getBoundingClientRect().top + window.pageYOffset - 85;
          window.scrollTo({ top: Math.max(0, targetTop), behavior: "smooth" });
        }, 300);
      }
    }
  }

  // 3. Precision anchor scrolling
  function initAnchorScroll() {
    document.querySelectorAll('.bpa-sublink[href^="#"]').forEach(link => {
      link.addEventListener('click', function(e) {
        const hash = this.getAttribute('href');
        const target = document.getElementById(hash.substring(1)) || document.querySelector(hash);
        if (target) {
          e.preventDefault();
          const headerOffset = 85;
          const elementPosition = target.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
          window.scrollTo({
            top: Math.max(0, offsetPosition),
            behavior: 'smooth'
          });
          if (history.pushState) {
            history.pushState(null, null, hash);
          } else {
            location.hash = hash;
          }
        }
      });
    });
  }

  // Execute safely across all lifecycle states
  initSliders();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      unwrapRiverReviews();
      initAnchorScroll();
    });
  } else {
    unwrapRiverReviews();
    initAnchorScroll();
  }
  window.addEventListener("load", unwrapRiverReviews);
  setTimeout(unwrapRiverReviews, 400);
  setTimeout(unwrapRiverReviews, 1200);
})();
</script>"""

js_pos = html.find("<script>")
if js_pos != -1:
    html = html[:js_pos] + updated_js.strip()
    print("JS updated successfully!")

with open("/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_10_river_cruises.html", "w") as f:
    f.write(html)

print("Updated comparison_deck_10_river_cruises.html successfully!")
print("Final length in characters:", len(html))
