#!/usr/bin/env python3
"""Build a noindex TEST page of the night cruises article.

It ports the approved Seine card design (thumbnail strip, exact price with a
price dropdown, "Personally tested" stamp, grouped combinable filters) and puts
the questions travellers keep asking in Budapest Facebook groups straight into
the top-10 card list:

- "When are you going?" month row in the filter box: every card then shows
  which of its listed sailings are fully lit, sunset-into-lights, or still daylight
- new filters: just views (no party, no dinner), good if you don't drink,
  party crowd, open-air deck, heated indoor, about 1 hour
- two new pill dropdowns per card: atmosphere ("relaxing or booze cruise?")
  and dock ("which dock should I pick?")

Usage: build_night_fb_test.py best-night-cruises-budapest.html best-night-cruises-budapest-test.html
"""
import html as H
import json
import re
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
SEINE = sys.argv[3] if len(sys.argv) > 3 else None
s = open(SRC, encoding="utf-8").read()


def rep(text, old, new, count=1, where=""):
    n = text.count(old)
    if n != count:
        raise SystemExit(f"[{where}] expected {count}x, found {n}x: {old[:100]!r}")
    return text.replace(old, new)


# ------------------------------------------------------------------ card data
# times = listed evening sailings (from each card's own time dropdown), dur = minutes
CARDS = {
    1: dict(cat="tested calm nodrink opendeck heated hour", dur=60,
            times=[f"{h:02d}:{m:02d}" for h in range(16, 22) for m in (0, 20, 40)
                   if "16:20" <= f"{h:02d}:{m:02d}" <= "21:00"], every="every 20 min",
            vibe=("🙂", "Calm sightseeing",
                  "Seated sightseeing with a 30-language audio guide on headsets, not a party boat.",
                  "Open-air seats at the back of the top deck, heated cabin below. The welcome drink can be a soft drink or water, so non-drinkers pay for nothing they skip."),
            dock=("Vigadó tér, Dock 7",
                  "Pest side, 2 minutes from Vörösmarty tér and the top of Váci utca.",
                  "Covered floating dock with restrooms and a rooftop waiting area.")),
    2: dict(cat="tested unlimited party opendeck hour", dur=75,
            times=["15:30", "15:45", "17:15", "18:45", "22:15", "22:30", "23:00"],
            vibe=("🎉", "Cocktail-party feel",
                  "Lively, not a quiet sightseeing hour.",
                  "On my cruise the commentary was hard to hear over the party noise. Open top deck plus two indoor decks; board early for the best top-deck spots. Lemonade is self-service, so non-drinkers are covered too."),
            dock=("3 docks to choose from",
                  "Akadémia 3 is by the Chain Bridge, best from Parliament or the Basilica. Vigadó 8/A is by Vörösmarty tér, best from Váci utca. Carl Lutz rakpart Dock 0 is further north on the Pest bank.",
                  "Pick the dock when you choose your time slot.")),
    3: dict(cat="tested calm nodrink opendeck heated hour under20", dur=60,
            times=["16:00", "17:30", "19:00", "20:30"],
            vibe=("🎹", "Quiet and historic",
                  "Classical piano plays between the narration on a historic paddle steamer.",
                  "Open-air panorama deck at the front, heated indoor area in winter. The welcome glass is prosecco or orange juice."),
            dock=("Dock 10, Elizabeth Bridge",
                  "Pest side next to Elizabeth Bridge, a short walk from Ferenciek tere metro.",
                  "No baby strollers and no wheelchair access on board.")),
    4: dict(cat="tested dinner nodrink opendeck heated", dur=150, times=["19:00"],
            vibe=("🕯️", "Romantic and quiet",
                  "Candlelit tables for two along the windows, a pianist and singer, no loud folk show.",
                  "Open top deck for photos at any point of the evening. Not for children under 3, and there is no vegan menu."),
            dock=("Vigadó tér, Dock 7",
                  "Pest side, 2 minutes from Vörösmarty tér and the top of Váci utca.",
                  "Legenda's covered dock has restrooms, so you can wait out of the rain.")),
    5: dict(cat="dinner unlimited opendeck", dur=150, times=["19:30"],
            vibe=("🎻", "All-inclusive evening",
                  "A seasonal buffet, unlimited drinks served to your table and live music in the Grand Salon.",
                  "After dinner you can go up to the rooftop deck, weather permitting."),
            dock=("Akadémia 3",
                  "Pest side by the Chain Bridge, best if you stay near Parliament, the Basilica or Széchenyi tér.",
                  "Bring a passport or ID card with the voucher.")),
    6: dict(cat="calm nodrink opendeck heated hour under20", dur=50,
            times=["16:10", "17:20", "18:30", "19:40", "20:50"],
            vibe=("🧺", "Relaxed, bring your own",
                  "A small boat with at most 150 guests, and everyone gets a rooftop seat.",
                  "No bar on board: bring your own drinks, alcohol-free included. The rooftop gets cold in November, so bring layers; the heated cabin is open to all."),
            dock=("Várkert Bazár, Buda side",
                  "Below the Castle on the Buda bank, the easy pick if you stay in Buda.",
                  "Most other boats leave from the Pest bank, so check which side you are on.")),
    7: dict(cat="tested dinner opendeck", dur=120, times=["19:00"],
            vibe=("🍷", "Intimate dinner",
                  "Dinner on the upper deck at 2 or 4-person tables; it never felt overcrowded.",
                  "Pick the no-show option for background music only. For night photos step out to the open bow or stern: the cabin lights reflect in the glass."),
            dock=("Dock 11, Elizabeth Bridge",
                  "Pest side next to Elizabeth Bridge, a short walk from Ferenciek tere metro.",
                  "Same boat and menu for all 3 show options.")),
    8: dict(cat="unlimited party opendeck heated hour under20", dur=75,
            times=["18:00", "19:30", "21:00"],
            vibe=("🎶", "Lively rooftop",
                  "Guests keep mentioning the music and the friendly crew.",
                  "Everyone has a seat on the heated lower deck; rooftop seats are first come, first served. Soft drinks and homemade lemonade are included."),
            dock=("Petőfi tér 9",
                  "Pest bank between Elizabeth Bridge and Vigadó tér, an easy walk from Váci utca.",
                  "Arrive 15 minutes early: boarding closes 5 minutes before departure.")),
    9: dict(cat="unlimited party hour", dur=60, times=["16:30", "19:30", "21:00"],
            vibe=("🍾", "Pre-party",
                  "Party songs from the loudspeakers, pitched as a warm-up before a night out.",
                  "Adults only: under-18s are not allowed, and it is not for pregnant guests."),
            dock=("Dock 11, Elizabeth Bridge",
                  "Pest side next to Elizabeth Bridge, a short walk from Ferenciek tere metro.",
                  "The upper deck is the spot for photos of the lit-up Parliament.")),
    10: dict(cat="tested calm nodrink heated hour under20", dur=60,
             times=["16:30", "17:00", "17:20", "18:20", "18:40", "19:40", "20:00", "21:00", "21:15"],
             vibe=("🙂", "No-frills sightseeing",
                   "A plain sightseeing hour with no drink included.",
                   "Heated main deck. The upper deck costs €5 more and has a roof with columns that block part of the view. Infants up to 3 ride free."),
             dock=("Dock 11, Elizabeth Bridge",
                   "Pest side next to Elizabeth Bridge, a short walk from Ferenciek tere metro.",
                   "Comfortable indoor meeting point.")),
}

E = H.escape


def pill(emoji, label, lead, note, cls=""):
    return (f'<details class="bpa-lang {cls}"><summary class="bpa-sp">{emoji} <span class="bpa-lang-label">{E(label)}</span>'
            f'<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop"><strong>{E(lead)}</strong> '
            f'{E(note)}</div></details>')


def thumbs(media):
    imgs = re.findall(r"<img\b[^>]*>", media)
    out = []
    for i, im in enumerate(imgs):
        src = re.search(r'\sdata-src="([^"]+)"', im) or re.search(r'\ssrc="([^"]+)"', im)
        src = src.group(1)
        ss = re.search(r'(?:data-)?srcset="([^"]+)"', im)
        if ss:  # smallest candidate
            src = ss.group(1).split(",")[0].strip().split(" ")[0]
        cls = "cd-thumb" + (" is-on" if i == 0 else "") + (" is-hid" if i > 4 else "")
        more = f' data-more="+{len(imgs) - 4}"' if i == 4 and len(imgs) > 5 else ""
        out.append(f'<button type="button" class="{cls}" data-i="{i}"{more} aria-label="Show photo {i + 1} of {len(imgs)}">'
                   f'<img src="{src}" alt="" loading="lazy" decoding="async" width="80" height="60"></button>')
    return '<div class="cd-thumbs" aria-label="Photo thumbnails">' + "".join(out) + "</div>"


starts = [m.start() for m in re.finditer(r'<div class="bpa-card" data-cat="[^"]*" id="card-\d+">', s)]
assert len(starts) == 10, len(starts)
ends = starts[1:] + [None]
new_cards = []
for n, st in enumerate(starts):
    num = n + 1
    c = s[st:ends[n]] if ends[n] else None
    if c is None:
        # last card: up to the close of its cta-cell block
        i = s.find('class="bpa-sublink"', st)
        i = s.find("</div>\n</div>\n</div>", i) + len("</div>\n</div>\n</div>")
        c = s[st:i]
    d = CARDS[num]
    # data-cat
    c = re.sub(r'data-cat="[^"]*"', f'data-cat="{d["cat"]}"', c, count=1)
    # gallery -> thumbnails
    mi = c.find('<div class="bpa-media">')
    ii = c.find('\n<div class="bpa-info">')
    media = c[mi:ii]
    c = c[:mi] + '<div class="cd-gal">' + media + thumbs(media) + "</div>" + c[ii:]
    # tested stamp: move the mobile tested dropdown into the proof slot
    tm = re.search(r'<details class="bpa-lang bpa-tested bpa-proof-mobile">.*?</details>', c, re.S)
    if tm:
        det = tm.group(0).replace("✓ Personally Tested", "Personally tested")
        det = det.replace('class="bpa-lang bpa-tested bpa-proof-mobile"', 'class="bpa-lang bpa-tested"').replace(
            'class="bpa-vchip bpa-proof-mobile"', 'class="bpa-vchip"')
        c = c.replace(tm.group(0), "")
        c = re.sub(r'<div class="bpa-proof">.*?</div>', f'<div class="bpa-proof">{det}</div>', c, count=1, flags=re.S)
    # pills: fixed order time -> commentary -> atmosphere -> dock -> extras
    sr = re.search(r'(<div class="bpa-specs-row">)(.*?)(</div>\n<div class="bpa-best-for)', c, re.S)
    body = sr.group(2)
    items = re.findall(r'<details class="bpa-lang[^"]*"[^>]*>.*?</details>|<span class="bpa-sp">.*?</span>', body, re.S)
    time = [x for x in items if "🕒" in x[:200]]
    comm = [x for x in items if "🎧" in x[:200]]
    extra = [x for x in items if x not in time and x not in comm]
    v, dk = d["vibe"], d["dock"]
    new = time + comm + [pill(v[0], v[1], v[2], v[3], "fbm-vibe"), pill("📍", dk[0], dk[1], dk[2], "fbm-dock")] + extra
    slot = (f'<div class="fbm-slot" data-times="{" ".join(d["times"])}" data-dur="{d["dur"]}"'
            + (f' data-every="{d["every"]}"' if d.get("every") else "") + "></div>")
    c = c.replace(sr.group(0), sr.group(1) + "\n" + "\n".join(new) + "\n</div>\n" + slot + "\n" + sr.group(3)[len("</div>\n"):])
    # price -> exact price + dropdown
    pm = re.search(r'<div class="bpa-price">(?:From )?(€[\d.,]+)</div>\s*<div class="bpa-psub">[^<]*</div>', c)
    p = pm.group(1)
    pdd = (f'<details class="cd-pdd"><summary><span class="cd-pdd-main">{p}</span><span class="cd-pdd-sub">per adult '
           f'<span class="cd-pdd-chev" aria-hidden="true">▾</span></span></summary><div class="cd-pdd-pop"><div class="cd-pdd-h">All ticket prices</div>'
           f'<table><tr><td>Adult</td><td>{p}</td></tr><tr><td>Kids<small>age bands per listing</small></td><td class="fbm-verify">verify</td></tr></table>'
           f'<div class="cd-pdd-note">Final price shown on the booking page before you pay.</div></div></details>')
    c = c.replace(pm.group(0), pdd)
    new_cards.append(c)

# rebuild: everything before card 1, the new cards, then the rest after the last card
i = s.find('class="bpa-sublink"', starts[-1])
tail_start = s.find("</div>\n</div>\n</div>", i) + len("</div>\n</div>\n</div>")
s = s[:starts[0]] + "".join(new_cards) + s[tail_start:]

# ------------------------------------------------------------------ filter box
def btn(cat, label):
    return (f'<button class="ltt-tab-btn" data-cat="{cat}" onclick="lttFilterCruises(\'{cat}\', this)" type="button" '
            f'aria-pressed="false">{label} <span class="cd-n"></span></button>')


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
fbox = (
    '<div class="ltt-integrated-filter-bar cd-fbox" id="cd-filters" role="group" aria-label="Filter cruises">'
    '<div class="cd-frow fbm-mrow"><span class="cd-flab">When are you going</span><div class="cd-fchips">'
    '<label class="fbm-msel"><span class="sr-only">Travel month</span><select id="fbm-month" aria-label="Travel month">'
    + "".join(f'<option value="{i}">{m}</option>' for i, m in enumerate(MONTHS))
    + '</select></label><span class="fbm-mnote" id="fbm-mnote"></span></div></div>'
    '<div class="cd-frow"><span class="cd-flab">Who is coming</span><div class="cd-fchips">'
    + btn("nodrink", "🥤 Good if you don't drink") + btn("party", "🎉 Party crowd") + "</div></div>"
    '<div class="cd-frow"><span class="cd-flab">The trip</span><div class="cd-fchips">'
    + btn("calm", "🌃 Just views, no party, no dinner") + btn("dinner", "🍽️ Dinner") + btn("unlimited", "🍾 Unlimited drinks")
    + btn("opendeck", "☀️ Open-air deck") + btn("heated", "🔥 Heated indoor") + btn("hour", "⏱️ About 1 hour") + "</div></div>"
    '<div class="cd-frow"><span class="cd-flab">Budget &amp; proof</span><div class="cd-fchips">'
    + btn("tested", "✓ Personally tested") + btn("under20", "💶 Under €20") + "</div></div>"
    '<div class="cd-ffoot"><span class="cd-fcount" aria-live="polite">Showing <b>10</b> of 10 cruises</span>'
    '<div class="cd-fapplied"></div><button type="button" class="cd-fclear" hidden onclick="lttFilterCruises(\'all\')">Clear all</button></div></div>'
)
fb_start = s.find('<div class="ltt-integrated-filter-bar">')
fb_end = s.find("Personally Tested (6)</button>\n</div>\n</div>", fb_start) + len("Personally Tested (6)</button>\n</div>\n</div>")
assert fb_start > 0 and fb_end > fb_start
s = s[:fb_start] + fbox + s[fb_end:]

mini = ('<div class="cd-fmini" aria-hidden="true"><div class="cd-fmini-in"><button type="button" class="cd-fmini-btn" '
        'onclick="cdFiltersJump()">⚙️ Filters <span class="cd-fmini-n" hidden></span></button><span class="cd-fmini-res">'
        '<b>10</b> of 10 cruises</span></div></div>')
s = rep(s, '<div class="bpa-deck-wrap" id="ltt-cards-deck">', '<div class="bpa-deck-wrap" id="ltt-cards-deck">' + mini, where="mini")

# ------------------------------------------------------------------ assets
seine = open(SEINE, encoding="utf-8").read()


def block(tag, i):
    return re.search(r'<%s id="%s"[^>]*>.*?</%s>' % (tag, i, tag), seine, re.S).group(0)


fbm_css = """<style id="fbm-css">
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0}
.fbm-mrow{background:#fffbeb;margin:0 -16px;padding:10px 16px!important;border-radius:14px 14px 0 0}
.fbm-msel select{appearance:auto;font:700 13px/1 'Plus Jakarta Sans',sans-serif;color:#0f172a;border:1px solid #cbd5e1;border-radius:9999px;padding:7px 12px;background:#fff;cursor:pointer}
.fbm-mnote{font:600 12.5px/1.35 'Plus Jakarta Sans',sans-serif;color:#92400e;align-self:center}
.fbm-slot{margin:2px 0 8px;padding:8px 10px;border-radius:10px;background:#f8fafc;border:1px solid #e2e8f0;font:500 13px/1.45 'Plus Jakarta Sans',sans-serif;color:#334155}
.fbm-slot b{color:#0f172a}
.fbm-slot .t{display:inline-block;padding:1px 6px;margin:1px 2px;border-radius:6px;font-weight:700;font-size:12.5px}
.fbm-slot .lit{background:#0a192f;color:#fde68a}
.fbm-slot .dusk{background:#fef3c7;color:#92400e}
.fbm-slot .day{background:#f1f5f9;color:#64748b}
.fbm-slot.is-none{background:#fff7ed;border-color:#fed7aa}
.fbm-verify{background:#fef3c7;color:#92400e!important;font-weight:700}
@media (max-width:767px){.fbm-mrow{margin:0 -12px;padding:10px 12px!important}}
</style>"""

fbm_js = """<script id="fbm-js">
(function(){
  /* Sunset and full dark in Budapest around mid-month (local time). */
  var SUN=['16:25','17:10','17:50','19:35','20:15','20:45','20:40','20:00','19:05','18:05','16:15','15:55'];
  var DARK=['17:00','17:45','18:25','20:10','20:55','21:30','21:20','20:35','19:40','18:40','16:50','16:35'];
  var NAMES=['January','February','March','April','May','June','July','August','September','October','November','December'];
  function m(t){var p=t.split(':');return +p[0]*60+(+p[1]);}
  function hm(x){return ('0'+Math.floor(x/60)).slice(-2)+':'+('0'+(x%60)).slice(-2);}
  function span(t,c){return '<span class="t '+c+'">'+t+'</span>';}
  function render(mi){
    var sun=m(SUN[mi]), dark=m(DARK[mi]), name=NAMES[mi];
    var note=document.getElementById('fbm-mnote');
    if(note) note.textContent='Sunset about '+SUN[mi]+', fully dark by '+DARK[mi]+'. Each card now shows which sailings are lit up.';
    document.querySelectorAll('.fbm-slot').forEach(function(el){
      var times=(el.getAttribute('data-times')||'').split(' ').filter(Boolean), dur=+el.getAttribute('data-dur');
      var lit=[],dusk=[],day=[];
      times.forEach(function(t){var a=m(t),b=a+dur; if(a>=dark-10) lit.push(t); else if(b>=dark+10&&a>=sun-45) dusk.push(t); else day.push(t);});
      el.classList.toggle('is-none',!lit.length&&!dusk.length);
      var h;
      if(dur>=120&&times.length===1){
        var a=m(times[0]),b=a+dur,left=b-Math.max(a,dark);
        h=left>0?('🌙 <b>'+name+':</b> dark from '+DARK[mi]+', so the last '+(left>=60?Math.floor(left/60)+' h '+(left%60?left%60+' min':''):left+' min')+' of dinner ('+times[0]+' to '+hm(b)+') is under the lights.')
                :(b>sun?('🌇 <b>'+name+':</b> sunset ('+SUN[mi]+') happens during dinner; it is fully dark only after you dock ('+DARK[mi]+').')
                  :('☀️ <b>'+name+':</b> the cruise ends before sunset ('+SUN[mi]+').'));
      } else if(!lit.length&&!dusk.length){
        h='☀️ <b>'+name+':</b> every listed sailing ends before full dark ('+DARK[mi]+'). Times change by season, so check the calendar for your date.';
      } else {
        h='';
        if(lit.length) h+='🌙 <b>Fully lit in '+name+':</b> '+(el.getAttribute('data-every')&&lit.length>3?span(lit[0],'lit')+' then every 20 min to '+span(lit[lit.length-1],'lit'):lit.map(function(t){return span(t,'lit');}).join(''));
        if(dusk.length) h+=(h?'<br>':'')+'🌇 <b>Sunset into lights:</b> '+dusk.map(function(t){return span(t,'dusk');}).join('');
      }
      el.innerHTML=h;
    });
  }
  var sel=document.getElementById('fbm-month'); if(!sel) return;
  var now=new Date().getMonth(); sel.value=now; render(now);
  sel.addEventListener('change',function(){render(+sel.value);});
})();
</script>"""

css = block("style", "cd-cards-css") + block("style", "cd-tested-css") + block("style", "cd-filters-css") + fbm_css
js = block("script", "cd-cards-js") + block("script", "cd-filters-js") + fbm_js
s = rep(s, "</head>", css + "</head>", where="css")
k = s.rfind("</body>")
s = s[:k] + js + s[k:]
s = rep(s, "<head>", '<head><meta name="robots" content="noindex,nofollow">', where="noindex")
open(OUT, "w", encoding="utf-8").write(s)
print("ok", OUT, len(s))
