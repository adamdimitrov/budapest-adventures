import re

# 1. Clean CSS
css = """<style>
.bpa-deck-wrap{width:100%;max-width:1060px;margin:32px auto;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#1e293b;display:flex;flex-direction:column;gap:20px}
.bpa-card{background:#fff;border:1px solid #e2e8f0;border-radius:14px;box-shadow:0 4px 18px rgba(15,23,42,0.05);overflow:hidden;transition:all .2s ease}
.bpa-card:hover{border-color:#cbd5e1;box-shadow:0 10px 30px rgba(15,23,42,0.08)}
.bpa-main{display:grid;grid-template-columns:310px 1fr 190px;gap:22px;padding:20px;align-items:center}
.bpa-media{position:relative;width:100%;height:215px;border-radius:10px;overflow:hidden;background:#0f172a}
.bpa-slider{display:flex;width:100%;height:100%;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;scrollbar-width:none;cursor:grab}
.bpa-slider:active{cursor:grabbing}
.bpa-slider::-webkit-scrollbar{display:none}
.bpa-slider img{flex:0 0 100%;width:100%;height:100%;object-fit:cover;scroll-snap-align:start;pointer-events:none}
.bpa-arrow{position:absolute;top:50%;transform:translateY(-50%);width:32px;height:32px;background:rgba(255,255,255,0.92);border:none;border-radius:50%;font-size:16px;font-weight:700;color:#0f172a;cursor:pointer;z-index:3;display:flex;align-items:center;justify-content:center;transition:all .15s}
.bpa-arrow:hover{background:#fff;transform:translateY(-50%) scale(1.08)}
.bpa-arrow.prev{left:8px}.bpa-arrow.next{right:8px}
.bpa-pill{position:absolute;bottom:8px;right:8px;background:rgba(15,23,42,0.78);color:#fff;font-size:11px;font-weight:700;padding:3px 8px;border-radius:12px;z-index:3}
.bpa-rank-tag{position:absolute;top:10px;left:10px;background:#0f172a;color:#fff;font-size:11px;font-weight:800;padding:4px 10px;border-radius:6px;z-index:3;box-shadow:0 2px 8px rgba(0,0,0,0.25)}
.bpa-info{display:flex;flex-direction:column;gap:7px}
.bpa-kicker{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:800;color:#0284c7;}
.bpa-title{font-size:17.5px;font-weight:800;color:#0f172a;line-height:1.35;text-decoration:none;transition:color .15s}
.bpa-title:hover{color:#0284c7;text-decoration:underline}
.bpa-proof{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:13px}
.bpa-stars{color:#f59e0b;letter-spacing:1.5px;font-size:13px}
.bpa-score-text{font-weight:800;color:#0f172a}
.bpa-count-muted{font-size:12px;color:#64748b}
.bpa-vchip{background:#ecfdf5;color:#047857;font-size:11px;font-weight:700;padding:2px 7px;border-radius:4px}
.bpa-channels{display:flex;align-items:center;gap:15px;flex-wrap:wrap}
.bpa-ci{display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:600;color:#475569}
.bpa-ci i{display:inline-block;width:15px;height:15px;background-size:contain;background-repeat:no-repeat;background-position:center;border-radius:3px;vertical-align:middle}
.bpa-ic-gyg{background-image:url("/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3745_getyourguide-icon.png")}
.bpa-ic-ta{background-image:url("/assets/cdn/652d0405192ba076b04f74a3/68f64414502d0348145b678e_tripadvisor-icon.avif")}
.bpa-ic-viator{background-image:url("/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3747_viator-icon.png")}
.bpa-ci strong{color:#0f172a;font-weight:800}.bpa-ci span{color:#64748b;font-weight:500}
.bpa-specs-row{display:flex;flex-wrap:wrap;gap:6px;margin-top:3px}
.bpa-sp{background:#f1f5f9;color:#475569;padding:4px 9px;border-radius:6px;font-size:11px;font-weight:600}
.bpa-best-for{font-size:12px;color:#475569;background:#f8fafc;border-left:3px solid #0284c7;padding:4px 8px;border-radius:0 4px 4px 0;margin-top:2px}
.bpa-best-for strong{color:#0f172a}
.bpa-cta-cell{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:9px;padding-left:18px;border-left:1px solid #f1f5f9;height:100%;text-align:center}
.bpa-price{font-size:27px;font-weight:900;color:#0f172a;line-height:1}
.bpa-psub{font-size:11px;color:#64748b;margin-top:2px}
.bpa-btn{width:100%;background:#0284c7;color:#fff;padding:11px 14px;border-radius:8px;font-size:13.5px;font-weight:800;transition:all .15s ease}
.bpa-btn:hover{background:#0369a1;transform:translateY(-1px)}
.bpa-sublink{font-size:12px;font-weight:600;color:#64748b;text-decoration:underline;transition:color .15s;cursor:pointer}
.bpa-sublink:hover{color:#0284c7}
@media (max-width:900px){
  .bpa-main{grid-template-columns:1fr;gap:16px;padding:16px}
  .bpa-media{height:230px}
  .bpa-cta-cell{flex-direction:row;justify-content:space-between;border-left:none;border-top:1px solid #f1f5f9;padding-left:0;padding-top:12px;width:100%}
  .bpa-btn{width:auto;padding:9px 18px}
}
html{scroll-behavior:smooth}
.comparison-table{display:none !important}
.bpa-reviews-deck-container{width:100%;max-width:860px;margin:16px auto 50px auto}
.bpa-breakdown-top-bar{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin:28px 0 20px 0;padding-bottom:16px;border-bottom:2px solid #e2e8f0}
.bpa-breakdown-heading{font-size:26px;font-weight:800;color:#0f172a;margin:0}
.bpa-breakdown-sub{font-size:13px;color:#64748b;margin:4px 0 0 0}
.bpa-acc-controls{display:flex;gap:8px}
.bpa-acc-ctrl-btn{background:#f1f5f9;border:1px solid #cbd5e1;border-radius:6px;padding:6px 12px;font-size:12px;font-weight:700;color:#334155;cursor:pointer;transition:all .15s}
.bpa-acc-ctrl-btn:hover{background:#e2e8f0;color:#0f172a}
.bpa-acc-card{background:#fff;border:1px solid #e2e8f0;border-radius:14px;box-shadow:0 3px 14px rgba(15,23,42,0.04);margin-bottom:18px;overflow:hidden;transition:all .2s;scroll-margin-top:85px !important}
.bpa-acc-card:hover{border-color:#cbd5e1}
.bpa-acc-card.is-open{border-color:#0284c7;box-shadow:0 6px 24px rgba(2,132,199,0.08)}
.bpa-acc-header{padding:18px 22px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:16px;user-select:none;background:#fff;transition:background .15s}
.bpa-acc-card.is-open .bpa-acc-header{background:#f8fafc;border-bottom:1px solid #e2e8f0}
.bpa-acc-header:hover{background:#f8fafc}
.bpa-acc-titles{flex:1;min-width:0}
.bpa-acc-badge{display:inline-block;font-size:11px;font-weight:800;color:#0284c7;;margin-bottom:3px}
.bpa-acc-title{margin:0 0 5px 0;font-size:18px;line-height:1.35;font-weight:800;color:#0f172a}
.bpa-acc-sub{font-size:13px;color:#475569;display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.bpa-acc-sub strong{color:#0f172a}.bpa-acc-price{font-weight:800;color:#0284c7}.bpa-acc-desc{color:#64748b}
.bpa-acc-toggle-btn{display:inline-flex;align-items:center;gap:6px;background:#f1f5f9;border:1px solid #cbd5e1;color:#0f172a;font-size:12.5px;font-weight:700;padding:8px 14px;border-radius:8px;cursor:pointer;white-space:nowrap;transition:all .15s}
.bpa-acc-card.is-open .bpa-acc-toggle-btn{background:#0284c7;color:#fff;border-color:#0284c7}
.bpa-acc-header:hover .bpa-acc-toggle-btn{border-color:#0284c7}
.bpa-acc-chevron{font-size:13px;transition:transform .2s}
.bpa-acc-card.is-open .bpa-acc-chevron{transform:rotate(180deg)}
.bpa-acc-body{display:none;padding:22px}
.bpa-acc-card.is-open .bpa-acc-body{display:block}
.bpa-acc-body .faq-content,.bpa-acc-body .pro-con-box-wrapper,.bpa-acc-body .w-richtext,.bpa-acc-body .div-block-27,.bpa-acc-body .content-wrap-read-more,.bpa-acc-body .div-block-34,.bpa-acc-body .reviews-3,.bpa-acc-body .star-ratings-2{display:block !important;visibility:visible !important;opacity:1 !important}
.bpa-acc-body .content-wrap-read-more{display:flex !important;flex-wrap:wrap !important;gap:8px !important;margin:12px 0 18px 0 !important}
.bpa-acc-body .feature-column{display:flex !important;flex-wrap:wrap !important;gap:8px !important;width:100% !important}
.bpa-acc-body .feature-block{background:#f1f5f9 !important;border:1px solid #e2e8f0 !important;border-radius:6px !important;padding:5px 10px !important;font-size:12px !important;font-weight:600 !important}
.bpa-acc-body .div-block-34{display:flex !important;flex-wrap:wrap !important;gap:14px !important;align-items:center !important;margin:16px 0 !important;padding:12px 16px !important;background:#f8fafc !important;border-radius:10px !important;border:1px solid #e2e8f0 !important}
.bpa-acc-body .reviews-3{display:flex !important;align-items:center !important;gap:6px !important}
.bpa-acc-body .star-ratings-2{display:flex !important;align-items:center !important;gap:3px !important}
.bpa-acc-body .star-ratings-2 svg{width:16px !important;height:16px !important;color:#f59e0b !important}
.bpa-acc-body img{max-width:100% !important;height:auto !important;border-radius:8px !important}
.content-left{display:block !important}
.stick-wrapper{position:sticky !important;top:70px !important;z-index:90}
#toc.toc{display:flex;flex-direction:column;gap:1px}
.tocitem{color:#4a6a86 !important;border-left:1px solid #dbe2eb !important;border-radius:0 5px 5px 0 !important;padding:7px 10px 7px 8px !important;font-size:11px !important;font-weight:500 !important;line-height:1.25em !important;text-decoration:none !important;transition:all .15s ease !important;display:block !important}
.tocitem:hover{color:#070e27 !important;background-color:rgba(41,98,255,0.06) !important;border-left:2px solid #070e27 !important;padding-left:7px !important}
.tocitem.active{color:#070e27 !important;font-weight:700 !important;background-color:rgba(41,98,255,0.08) !important;border-left:2px solid #2962ff !important;padding-left:7px !important}
.sticky-mobile-bar{position:fixed;bottom:0;left:0;right:0;width:100%;background:rgba(255,255,255,0.96);backdrop-filter:blur(14px);box-shadow:0 -6px 24px rgba(15,23,42,0.12);border-top:1px solid rgba(226,232,240,0.9);z-index:9999;padding:10px 16px;transform:translateY(110%);opacity:0;pointer-events:none;transition:transform .3s cubic-bezier(.16,1,.3,1),opacity .25s ease}
.sticky-mobile-bar.visible{transform:translateY(0);opacity:1;pointer-events:auto}
.sticky-inner{max-width:1060px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:16px}
.sticky-boat-info{display:flex;align-items:center;gap:12px;min-width:0;flex:1}
.sticky-thumb-img{width:44px;height:44px;border-radius:8px;object-fit:cover;flex-shrink:0;box-shadow:0 2px 6px rgba(0,0,0,0.15)}
.sticky-text{display:flex;flex-direction:column;gap:2px;min-width:0}
.sticky-title-row{display:flex;align-items:center;gap:8px;min-width:0}
.sticky-rank-badge{background:#fef3c7;color:#92400e;border:1px solid #fde68a;font-size:10px;font-weight:800;padding:2px 6px;border-radius:4px;white-space:nowrap}
.sticky-title-row strong{font-size:13.5px;font-weight:800;color:#0f172a;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sticky-meta-row{display:flex;align-items:center;gap:6px;font-size:12px;color:#64748b;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sticky-price-tag{font-weight:800;color:#047857}.sticky-bullet{color:#cbd5e1;font-size:10px}.sticky-desc-text{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.btn-sticky-cta{display:inline-flex;align-items:center;justify-content:center;gap:6px;background:linear-gradient(135deg,#059669 0%,#047857 100%);color:#fff;font-size:13.5px;font-weight:800;padding:10px 22px;border-radius:10px;text-decoration:none;box-shadow:0 4px 14px rgba(5,150,105,0.35);transition:all .15s ease;flex-shrink:0;}
.btn-sticky-cta:hover{background:linear-gradient(135deg,#047857 0%,#065f46 100%);box-shadow:0 6px 18px rgba(5,150,105,0.45);transform:translateY(-1px);color:#fff}
@media (max-width:768px){
  .sticky-mobile-bar{padding:8px 12px}
  .sticky-inner{gap:10px}
  .sticky-thumb-img{width:38px;height:38px}
  .sticky-title-row strong{font-size:12.5px}
  .sticky-rank-badge,.sticky-desc-text,.sticky-bullet,.bpa-acc-toggle-text{display:none}
  .btn-sticky-cta{padding:8px 15px;font-size:12.5px}
  .bpa-acc-header{padding:14px 16px}
  .bpa-acc-title{font-size:16px}
}
</style>"""

# 2. Extract original photos and build cards
with open("/Users/adamdimitrov/Development/budapest-adventures/river.html") as f:
    r_html = f.read()

sliders = re.findall(r"<div[^>]*class=\"[^\"]*slider-2[^\"]*\"[^>]*>(.*?)</div>\s*</div>\s*</div>", r_html, re.DOTALL)
cruises_imgs = []
for s in sliders:
    imgs = re.findall(r"<img[^>]*src=\"([^\"]+)\"", s)
    cruises_imgs.append(imgs)

BPA_CDN = "/assets/cdn/60e43c7d6d05b671dff0dc1a/"
cleaned_imgs = []
for group in cruises_imgs:
    grp_cleaned = []
    for u in group:
        if u.startswith(BPA_CDN):
            grp_cleaned.append(u[len(BPA_CDN):])
        else:
            grp_cleaned.append(u)
    cleaned_imgs.append(grp_cleaned)

with open("/Users/adamdimitrov/Development/budapest-adventures/build_river_deck.py") as f:
    brd = f.read()

start_cruises = brd.find("cruises = [")
end_cruises = brd.find("\n]\n", start_cruises) + 3
cruises_data = eval(brd[start_cruises:end_cruises].split("=", 1)[1])

cards = []
for i, c in enumerate(cruises_data):
    imgs = cleaned_imgs[i]
    hero = imgs[0]
    more = ",".join(imgs[1:])
    tot = len(imgs)
    
    badge_cls = c["badge_cls"]
    badge_txt = c["badge"]
    badge_html = f'<span class="bpa-rank-tag {badge_cls}">{badge_txt}</span>'
    
    chan_html = ""
    for ch, score, revs in c["channels"]:
        chan_html += f'<div class="bpa-ci"><i class="bpa-ic-{ch}"></i><strong>{score}</strong><span>{revs}</span></div>'
        
    specs_html = "".join([f'<span class="bpa-sp">{sp}</span>' for sp in c["specs"]])
    
    hero_url = hero if hero.startswith("http") else (BPA_CDN + hero)
    title = c["title"]
    kicker = c["kicker"]
    url = c["url"]
    stars = c["stars"]
    score = c["score"]
    reviews = c["reviews"]
    best_for = c["best_for"]
    price = c["price"]
    price_sub = c["price_sub"]
    anchor = c["anchor"]
    
    card = f"""<div class="bpa-card"><div class="bpa-main"><div class="bpa-media">{badge_html}<button class="bpa-arrow prev" onclick="bpaSlide(this,-1)">‹</button><button class="bpa-arrow next" onclick="bpaSlide(this,1)">›</button><span class="bpa-pill">1 / {tot}</span><div class="bpa-slider" data-more="{more}" onscroll="bpaCount(this)"><img src="{hero_url}" alt="Budapest Cruise"></div></div><div class="bpa-info"><div class="bpa-kicker">{kicker}</div><a href="{url}" target="_blank" rel="noopener" class="bpa-title">{title}</a><div class="bpa-proof"><span class="bpa-stars">{stars}</span><span class="bpa-score-text">{score}</span><span class="bpa-count-muted">{reviews}</span><span class="bpa-vchip">✓ Verified</span></div><div class="bpa-channels">{chan_html}</div><div class="bpa-specs-row">{specs_html}</div><div class="bpa-best-for">🎯 <strong>Best For:</strong> {best_for}</div></div><div class="bpa-cta-cell"><div><div class="bpa-price">{price}</div><div class="bpa-psub">{price_sub}</div></div><a href="{url}" target="_blank" rel="noopener" class="bpa-btn">Book Now →</a><a href="{anchor}" class="bpa-sublink">Read Full Review ↓</a></div></div></div>"""
    cards.append(card)

deck_html = f"""<div class="bpa-deck-wrap"><div class="bpa-section-header"><h2 class="bpa-section-title">Comparison — 10 Best Boat Tours &amp; River Cruises in Budapest (2026)</h2><p class="bpa-section-sub">Personally field-tested on the Danube • Verified prices, dock locations &amp; real photos</p></div>{"".join(cards)}</div><aside class="sticky-mobile-bar" id="sticky-bar" aria-label="Current Cruise Quick Reservation"><div class="sticky-inner"><div class="sticky-boat-info"><img id="sticky-thumb" src="{BPA_CDN}68f3738fe72bf6e25526e991_best-budapest-river-cruises-legenda-sightseeing-cruise-00025.avif" alt="Budapest Cruise" class="sticky-thumb-img"><div class="sticky-text"><div class="sticky-title-row"><span id="sticky-rank" class="sticky-rank-badge">🏆 #1 Best Overall</span><strong id="sticky-name">Legenda City Cruises</strong></div><div class="sticky-meta-row"><span id="sticky-price" class="sticky-price-tag">€20–25</span><span class="sticky-bullet">•</span><span id="sticky-desc" class="sticky-desc-text">Dock 7 • Welcome Drink Included</span></div></div></div><a id="sticky-cta-btn" href="https://legenda.hu/en?partner=38585" target="_blank" rel="noopener" class="btn-sticky-cta">Book Tickets →</a></div></aside>"""

# 3. Minified JS
js = """<script>
(function(){
const BPA_CDN="/assets/cdn/60e43c7d6d05b671dff0dc1a/";
function initSliders(){
document.querySelectorAll(".bpa-slider[data-more]").forEach(c=>{
const m=c.getAttribute("data-more").split(",");
m.forEach(f=>{
if(!f)return;
const img=document.createElement("img");
img.src=f.startsWith("http")?f:BPA_CDN+f;
img.loading="lazy";
img.alt="Budapest River Cruise";
c.appendChild(img);
});
c.removeAttribute("data-more");
const tot=c.children.length;
const cnt=c.parentElement.querySelector(".bpa-pill");
if(cnt)cnt.textContent="1 / "+tot;
let isDown=false,startX,sLeft;
c.addEventListener("mousedown",e=>{
isDown=true;c.style.scrollSnapType="none";
startX=e.pageX-c.offsetLeft;sLeft=c.scrollLeft;
});
const stopDrag=()=>{
if(!isDown)return;isDown=false;c.style.scrollSnapType="x mandatory";
const w=c.offsetWidth||1;c.scrollTo({left:Math.round(c.scrollLeft/w)*w,behavior:"smooth"});
};
c.addEventListener("mouseleave",stopDrag);
c.addEventListener("mouseup",stopDrag);
c.addEventListener("mousemove",e=>{
if(!isDown)return;e.preventDefault();
c.scrollLeft=sLeft-(e.pageX-c.offsetLeft-startX)*1.15;
});
});
}
window.bpaSlide=function(btn,dir){
const c=btn.parentElement.querySelector(".bpa-slider");
if(c)c.scrollBy({left:dir*c.offsetWidth,behavior:"smooth"});
};
window.bpaCount=function(c){
if(c._ticking)return;c._ticking=true;
requestAnimationFrame(()=>{
const w=c.offsetWidth||1;
const idx=Math.min(c.children.length,Math.max(1,Math.round(c.scrollLeft/w)+1));
const cnt=c.parentElement.querySelector(".bpa-pill");
if(cnt)cnt.textContent=idx+" / "+c.children.length;
c._ticking=false;
});
};
function getCruises(){
return Array.from(document.querySelectorAll(".bpa-card")).map((card,i)=>{
const sub=card.querySelector(".bpa-sublink");
const id=sub?sub.getAttribute("href").replace("#",""):"";
const kicker=card.querySelector(".bpa-kicker");
const head=card.querySelector(".bpa-title");
const tag=card.querySelector(".bpa-rank-tag");
const p=card.querySelector(".bpa-price");
const psub=card.querySelector(".bpa-psub");
const kp=kicker?kicker.textContent.split("•"):[];
return{
id:id,
r:String(i+1),
tag:tag?tag.textContent.trim():"",
name:kp[0]?kp[0].trim():"",
p:p?p.textContent.trim():"",
d:(kp[1]?kp[1].trim():"")+(psub?" • "+psub.textContent.trim():""),
l:head?head.href:"",
t:(i+1)+". "+(head?head.textContent.trim():"")
};
});
}
window.bpaToggleAcc=function(id,forceOpen){
const card=document.getElementById(id);
if(!card)return;
const willOpen=forceOpen!==undefined?forceOpen:!card.classList.contains("is-open");
if(willOpen){
card.classList.add("is-open");
const txt=card.querySelector(".bpa-acc-toggle-text");
if(txt)txt.textContent="Close Review";
}else{
card.classList.remove("is-open");
const txt=card.querySelector(".bpa-acc-toggle-text");
if(txt)txt.textContent="Read Review";
}
};
window.bpaToggleAllAcc=function(openAll){
getCruises().forEach(c=>bpaToggleAcc(c.id,openAll));
};
function buildDetailedReviews(){
let deck=document.getElementById("ba-river-reviews-deck");
const target=document.getElementById("0-itinerary-and-landmarks");
const content=document.getElementById("content");
if(!deck){
deck=document.createElement("div");
deck.id="ba-river-reviews-deck";
deck.className="bpa-reviews-deck-container";
}
if(target&&target.nextSibling){
if(deck.parentNode!==target.parentNode||deck.previousSibling!==target){
target.parentNode.insertBefore(deck,target.nextSibling);
}
}else if(content&&deck.parentNode!==content){
content.insertBefore(deck,content.firstChild);
}
if(deck.getAttribute("data-built")==="true")return;
const cruises=getCruises();
if(!cruises.length)return;
deck.innerHTML=`<div class="bpa-breakdown-top-bar"><div><h2 id="river-cruises-breakdown" class="bpa-breakdown-heading">Detailed Breakdown — 10 Best River Cruises in Budapest</h2><p class="bpa-breakdown-sub">Personally field-tested • Click any cruise or TOC item to expand full review</p></div><div class="bpa-acc-controls"><button type="button" class="bpa-acc-ctrl-btn" onclick="bpaToggleAllAcc(true)">Expand All</button><button type="button" class="bpa-acc-ctrl-btn" onclick="bpaToggleAllAcc(false)">Collapse All</button></div></div>`;
let mounted=0;
cruises.forEach((m,idx)=>{
const a=document.getElementById(m.id);
if(!a)return;
const navEl=a.closest("nav.faq-content-wrap")||a;
const card=document.createElement("div");
card.className="bpa-acc-card"+(idx===0?" is-open":"");
card.id=m.id;
card.innerHTML=`<div class="bpa-acc-header" onclick="bpaToggleAcc('${m.id}')"><div class="bpa-acc-titles"><div class="bpa-acc-badge">${m.tag}</div><h3 class="bpa-acc-title">${m.t}</h3><div class="bpa-acc-sub"><strong>${m.name}</strong> • <span class="bpa-acc-price">${m.p}</span> • <span class="bpa-acc-desc">${m.d}</span></div></div><div class="bpa-acc-btn-wrap"><button type="button" class="bpa-acc-toggle-btn"><span class="bpa-acc-toggle-text">${idx===0?"Close Review":"Read Review"}</span><span class="bpa-acc-chevron">▾</span></button></div></div><div class="bpa-acc-body"><div class="bpa-review-content"></div></div>`;
const holder=card.querySelector(".bpa-review-content");
while(navEl.firstChild)holder.appendChild(navEl.firstChild);
a.removeAttribute("id");
deck.appendChild(card);
mounted++;
});
if(mounted>0)deck.setAttribute("data-built","true");
}
function syncSidebarTOC(){
const toc=document.querySelector("#toc");
if(!toc||toc.getAttribute("data-synced")==="true")return;
const cruises=getCruises();
if(!cruises.length)return;
const items=[
{id:"0-itinerary-and-landmarks",text:"Budapest Boat Tour Itinerary & Map"},
{id:"river-cruises-breakdown",text:"Detailed Breakdown — 10 Best River Cruises"}
];
cruises.forEach(c=>{items.push({id:c.id,text:c.r+". "+c.name});});
const cat=document.getElementById("categories");
if(cat)items.push({id:"categories",text:"Types of River Cruises in Budapest"});
const faq=document.getElementById("faq");
if(faq)items.push({id:"faq",text:"Frequently Asked Questions"});
toc.innerHTML="";
const frag=document.createDocumentFragment();
items.forEach(it=>{
const a=document.createElement("a");
a.className="tocitem";
a.href="#"+it.id;
a.textContent=it.text;
frag.appendChild(a);
});
toc.appendChild(frag);
toc.setAttribute("data-synced","true");
const leftCol=toc.closest(".content-left");
if(leftCol)leftCol.style.display="block";
if(window._tocObs)window._tocObs.disconnect();
window._tocObs=new IntersectionObserver(entries=>{
entries.forEach(entry=>{
if(entry.isIntersecting){
toc.querySelectorAll(".tocitem.active").forEach(z=>z.classList.remove("active"));
const link=toc.querySelector('a[href="#'+entry.target.id+'"]');
if(link)link.classList.add("active");
}
});
},{rootMargin:"0px 0px -70% 0px"});
items.forEach(it=>{
const el=document.getElementById(it.id);
if(el)window._tocObs.observe(el);
});
}
function updateFloatingCTA(){
const bar=document.getElementById("sticky-bar");
if(!bar)return;
const cards=document.querySelectorAll(".bpa-card");
const reviews=document.querySelectorAll(".bpa-acc-card");
if(!cards.length)return;
const cruises=getCruises();
const vCenter=window.innerHeight/2;
const firstTop=cards[0].getBoundingClientRect().top;
const lastRev=reviews.length?reviews[reviews.length-1]:cards[cards.length-1];
const lastBottom=lastRev.getBoundingClientRect().bottom;
if(firstTop>vCenter||lastBottom<vCenter){
bar.classList.remove("visible");
return;
}
let activeIdx=0,minDistance=Infinity;
cards.forEach((card,i)=>{
const r=card.getBoundingClientRect();
const dist=Math.abs(r.top+r.height/2-vCenter);
if(dist<minDistance){minDistance=dist;activeIdx=i;}
});
reviews.forEach((rev,i)=>{
const r=rev.getBoundingClientRect();
if(r.top<=vCenter&&r.bottom>=vCenter){
activeIdx=i;
}else{
const dist=Math.abs(r.top+r.height/2-vCenter);
if(dist<minDistance){minDistance=dist;activeIdx=i;}
}
});
const active=cruises[activeIdx];
if(active){
const card=cards[activeIdx];
const imgEl=card?card.querySelector(".bpa-slider img"):null;
if(imgEl)document.getElementById("sticky-thumb").src=imgEl.src;
document.getElementById("sticky-rank").textContent=active.tag;
document.getElementById("sticky-name").textContent=active.name;
document.getElementById("sticky-price").textContent=active.p;
document.getElementById("sticky-desc").textContent=active.d;
document.getElementById("sticky-cta-btn").href=active.l;
bar.classList.add("visible");
}
}
document.addEventListener("click",e=>{
const a=e.target.closest('a[href^="#"]');
if(!a)return;
const hash=a.getAttribute("href");
if(!hash||hash==="#")return;
const targetId=hash.substring(1);
const target=document.getElementById(targetId);
if(target){
e.preventDefault();
e.stopPropagation();
if(target.classList.contains("bpa-acc-card")){
bpaToggleAcc(targetId,true);
}
const top=target.getBoundingClientRect().top+window.pageYOffset-85;
window.scrollTo({top:Math.max(0,top),behavior:"smooth"});
history.pushState(null,"",hash);
}
},true);
window.addEventListener("scroll",()=>{
if(!window._flTicking){
window._flTicking=true;
requestAnimationFrame(()=>{
updateFloatingCTA();
window._flTicking=false;
});
}
},{passive:true});
initSliders();
function initAll(){
buildDetailedReviews();
syncSidebarTOC();
updateFloatingCTA();
if(window.location.hash){
const h=window.location.hash.substring(1);
const el=document.getElementById(h);
if(el){
if(el.classList.contains("bpa-acc-card"))bpaToggleAcc(h,true);
setTimeout(()=>{
const top=el.getBoundingClientRect().top+window.pageYOffset-85;
window.scrollTo({top:Math.max(0,top),behavior:"smooth"});
},300);
}
}
}
if(document.readyState==="loading"){
document.addEventListener("DOMContentLoaded",initAll);
}else{
initAll();
}
window.addEventListener("load",initAll);
setTimeout(initAll,200);
setTimeout(initAll,600);
setTimeout(initAll,1200);
})();
</script>"""

final_code = css + "\n" + deck_html + "\n" + js
print("Final assembled length:", len(final_code))
print("Within 50,000 Webflow limit:", len(final_code) <= 50000)

with open("/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_10_river_cruises.html", "w") as out:
    out.write(final_code)

print("Saved /Users/adamdimitrov/Development/budapest-adventures/comparison_deck_10_river_cruises.html successfully!")
