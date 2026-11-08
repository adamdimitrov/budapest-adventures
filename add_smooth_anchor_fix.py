with open("/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_7_cruises.html", "r") as f:
    html = f.read()

# 1. Add scroll-margin-top to the CSS block
css_addition = """
/* Fix anchor jump offsets so titles land with clean 85px headroom */
html {
  scroll-behavior: smooth;
}
.div-block-27, 
[id^="1-"], [id^="2-"], [id^="3-"], [id^="4-"], [id^="5-"], [id^="6-"] {
  scroll-margin-top: 90px !important;
}
"""

if "scroll-margin-top" not in html:
    html = html.replace("</style>", css_addition + "</style>")

# 2. Add precision JS scroll handler for .bpa-sublink inside the script
js_anchor_handler = """
  // Precision anchor scrolling with 85px top offset
  document.querySelectorAll('.bpa-sublink[href^="#"]').forEach(link => {
    link.addEventListener('click', function(e) {
      const hash = this.getAttribute('href');
      const target = document.querySelector(hash);
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
"""

if "Precision anchor scrolling" not in html:
    # Insert before the closing IIFE
    html = html.replace("})();\n</script>", js_anchor_handler + "})();\n</script>")

with open("/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_7_cruises.html", "w") as f:
    f.write(html)

print("Anchor fix added to comparison_deck_7_cruises.html successfully!")
print("New length in characters:", len(html))
