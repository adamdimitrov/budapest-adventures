import re

with open("/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_10_river_cruises.html", "r") as f:
    orig = f.read()

deck_start = orig.find("<div class=\"bpa-deck-wrap\">")
deck_end = orig.find("</aside>") + len("</aside>")
deck_html = orig[deck_start:deck_end]

css = """<style>
.bpa-deck-wrap{width:100%;max-width:1060px;margin:32px auto;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#1e293b;-webkit-font-smoothing:antialiased;display:flex;flex-direction:column;gap:20px}
.bpa-card{background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;box-shadow:0 4px 18px rgba(15,23,42,0.05);overflow:hidden;transition:box-shadow .2s ease,border-color .2s ease}
.bpa-card:hover{border-color:#cbd5e1;box-shadow:0 10px 30px rgba(15,23,42,0.08)}
.bpa-main{display:grid;grid-template-columns:310px 1fr 190px;gap:22px;padding:20px;align-items:center}
.bpa-media{position:relative;width:100%;height:215px;border-radius:10px;overflow:hidden;background:#0f172a}
.bpa-slider{display:flex;width:100%;height:100%;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain;touch-action:pan-y pinch-zoom;scrollbar-width:none;user-select:none;cursor:grab}
.bpa-slider:active{cursor:grabbing}
.bpa-slider::-webkit-scrollbar{display:none}
.bpa-slider img{flex:0 0 100%;width:100%;height:100%;object-fit:cover;scroll-snap-align:start;scroll-snap-stop:always;user-select:none;-webkit-user-drag:none;pointer-events:none}
.bpa-nav-arrow{position:absolute;top:50%;transform:translateY(-50%);width:32px;height:32px;background:rgba(255,255,255,0.92);border:none;border-radius:50%;font-size:16px;font-weight:700;color:#0f172a;cursor:pointer;z-index:3;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,0.25);transition:background .15s,transform .15s}
.bpa-nav-arrow:hover{background:#ffffff;transform:translateY(-50%) scale(1.08)}
.bpa-nav-arrow.prev{left:8px}
.bpa-nav-arrow.next{right:8px}
.bpa-counter-pill{position:absolute;bottom:8px;right:8px;background:rgba(15,23,42,0.78);color:#ffffff;font-size:11px;font-weight:700;padding:3px 8px;border-radius:12px;backdrop-filter:blur(4px);z-index:3}
.bpa-rank-tag{position:absolute;top:10px;left:10px;background:#0f172a;color:#ffffff;font-size:11px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;padding:4px 10px;border-radius:6px;z-index:3;box-shadow:0 2px 8px rgba(0,0,0,0.25)}
.bpa-info{display:flex;flex-direction:column;gap:7px}
.bpa-kicker{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:800;color:#0284c7;text-transform:uppercase;letter-spacing:.5px}
.bpa-headline{font-size:17.5px;font-weight:800;color:#0f172a;line-height:1.35;text-decoration:none;transition:color .15s}
.bpa-headline:hover{color:#0284c7;text-decoration:underline}
.bpa-proof-bar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:13px;margin-top:1px}
.bpa-gold-stars{color:#f59e0b;letter-spacing:1.5px;font-size:13px}
.bpa-score-text{font-weight:800;color:#0f172a}
.bpa-count-muted{font-size:12px;color:#64748b}
.bpa-verified-chip{background:#ecfdf5;color:#047857;font-size:11px;font-weight:700;padding:2px 7px;border-radius:4px}
.bpa-channels{display:flex;align-items:center;gap:15px;flex-wrap:wrap;margin-top:1px}
.bpa-channel-item{display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:600;color:#475569}
.bpa-channel-item i{display:inline-block;width:15px;height:15px;background-size:contain;background-repeat:no-repeat;background-position:center;border-radius:3px;vertical-align:middle}
.bpa-ic-gyg{background-image:url("/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3745_getyourguide-icon.png")}
.bpa-ic-ta{background-image:url("/assets/cdn/652d0405192ba076b04f74a3/68f64414502d0348145b678e_tripadvisor-icon.avif")}
.bpa-ic-viator{background-image:url("/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3747_viator-icon.png")}
.bpa-channel-item strong{color:#0f172a;font-weight:800}
.bpa-channel-item span{color:#64748b;font-weight:500}
.bpa-specs-row{display:flex;flex-wrap:wrap;gap:6px;margin-top:3px}
.bpa-spec-pill{background:#f1f5f9;color:#475569;padding:4px 9px;border-radius:6px;font-size:11px;font-weight:600}
.bpa-best-for{font-size:12px;color:#475569;background:#f8fafc;border-left:3px solid #0284c7;padding:4px 8px;border-radius:0 4px 4px 0;margin-top:2px}
.bpa-best-for strong{color:#0f172a}
.bpa-cta-cell{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:9px;padding-left:18px;border-left:1px solid #f1f5f9;height:100%;text-align:center}
.bpa-price-num{font-size:27px;font-weight:900;color:#0f172a;line-height:1}
.bpa-price-sub{font-size:11px;color:#64748b;margin-top:2px}
.bpa-book-button{width:100%;background:#0284c7;color:#ffffff;padding:11px 14px;border-radius:8px;font-size:13.5px;font-weight:800;text-decoration:none;text-align:center;box-shadow:0 2px 6px rgba(2,132,199,0.3);transition:all .15s ease}
.bpa-book-button:hover{background:#0369a1;box-shadow:0 4px 12px rgba(2,132,199,0.4);transform:translateY(-1px)}
.bpa-sublink{font-size:12px;font-weight:600;color:#64748b;text-decoration:underline;transition:color .15s;cursor:pointer}
.bpa-sublink:hover{color:#0284c7}
@media (max-width:900px){
  .bpa-main{grid-template-columns:1fr;gap:16px;padding:16px}
  .bpa-media{height:230px}
  .bpa-cta-cell{flex-direction:row;justify-content:space-between;border-left:none;border-top:1px solid #f1f5f9;padding-left:0;padding-top:12px;width:100%}
  .bpa-book-button{width:auto;padding:9px 18px}
}
html{scroll-behavior:smooth}
.comparison-table{display:none !important}

/* Reviews Deck & Smart Accordion Styles */
.bpa-reviews-deck-container{width:100%;max-width:860px;margin:16px auto 50px auto}
.bpa-breakdown-top-bar{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin:28px 0 20px 0;padding-bottom:16px;border-bottom:2px solid #e2e8f0}
.bpa-breakdown-heading{font-size:26px;font-weight:800;color:#0f172a;margin:0}
.bpa-breakdown-sub{font-size:13px;color:#64748b;margin:4px 0 0 0}
.bpa-acc-controls{display:flex;gap:8px}
.bpa-acc-ctrl-btn{background:#f1f5f9;border:1px solid #cbd5e1;border-radius:6px;padding:6px 12px;font-size:12px;font-weight:700;color:#334155;cursor:pointer;transition:all .15s}
.bpa-acc-ctrl-btn:hover{background:#e2e8f0;color:#0f172a}

.bpa-acc-card{background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;box-shadow:0 3px 14px rgba(15,23,42,0.04);margin-bottom:18px;overflow:hidden;transition:border-color .2s,box-shadow .2s;scroll-margin-top:85px !important}
.bpa-acc-card:hover{border-color:#cbd5e1}
.bpa-acc-card.is-open{border-color:#0284c7;box-shadow:0 6px 24px rgba(2,132,199,0.08)}
.bpa-acc-header{padding:18px 22px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:16px;user-select:none;background:#ffffff;transition:background-color .15s}
.bpa-acc-card.is-open .bpa-acc-header{background:#f8fafc;border-bottom:1px solid #e2e8f0}
.bpa-acc-header:hover{background:#f8fafc}
.bpa-acc-titles{flex:1;min-width:0}
.bpa-acc-badge{display:inline-block;font-size:11px;font-weight:800;color:#0284c7;text-transform:uppercase;letter-spacing:.5px;margin-bottom:3px}
.bpa-acc-title{margin:0 0 5px 0;font-size:18px;line-height:1.35;font-weight:800;color:#0f172a}
.bpa-acc-sub{font-size:13px;color:#475569;display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.bpa-acc-sub strong{color:#0f172a}
.bpa-acc-price{font-weight:800;color:#0284c7}
.bpa-acc-desc{color:#64748b}
.bpa-acc-toggle-btn{display:inline-flex;align-items:center;gap:6px;background:#f1f5f9;border:1px solid #cbd5e1;color:#0f172a;font-size:12.5px;font-weight:700;padding:8px 14px;border-radius:8px;cursor:pointer;white-space:nowrap;transition:all .15s}
.bpa-acc-card.is-open .bpa-acc-toggle-btn{background:#0284c7;color:#ffffff;border-color:#0284c7}
.bpa-acc-header:hover .bpa-acc-toggle-btn{border-color:#0284c7}
.bpa-acc-chevron{font-size:13px;transition:transform .2s}
.bpa-acc-card.is-open .bpa-acc-chevron{transform:rotate(180deg)}
.bpa-acc-body{display:none;padding:22px}
.bpa-acc-card.is-open .bpa-acc-body{display:block}

/* Unhide all rich content inside review bodies */
.bpa-acc-body .faq-content,.bpa-acc-body .pro-con-box-wrapper,.bpa-acc-body .w-richtext,.bpa-acc-body .div-block-27,.bpa-acc-body .content-wrap-read-more,.bpa-acc-body .div-block-34,.bpa-acc-body .reviews-3,.bpa-acc-body .star-ratings-2{display:block !important;visibility:visible !important;opacity:1 !important;overflow:visible !important;max-width:100% !important}
.bpa-acc-body .content-wrap-read-more{display:flex !important;flex-wrap:wrap !important;gap:8px !important;margin:12px 0 18px 0 !important}
.bpa-acc-body .feature-column{display:flex !important;flex-wrap:wrap !important;gap:8px !important;width:100% !important}
.bpa-acc-body .feature-block{background:#f1f5f9 !important;border:1px solid #e2e8f0 !important;border-radius:6px !important;padding:5px 10px !important;font-size:12px !important;font-weight:600 !important}
.bpa-acc-body .div-block-34{display:flex !important;flex-wrap:wrap !important;gap:14px !important;align-items:center !important;margin:16px 0 !important;padding:12px 16px !important;background:#f8fafc !important;border-radius:10px !important;border:1px solid #e2e8f0 !important}
.bpa-acc-body .reviews-3{display:flex !important;align-items:center !important;gap:6px !important}
.bpa-acc-body .star-ratings-2{display:flex !important;align-items:center !important;gap:3px !important}
.bpa-acc-body .star-ratings-2 svg{width:16px !important;height:16px !important;color:#f59e0b !important}
.bpa-acc-body img{max-width:100% !important;height:auto !important;border-radius:8px !important}

/* Sidebar Table of Contents Styles (Matches Dinner Cruises exactly) */
.content-left{display:block !important}
.stick-wrapper{position:sticky !important;top:70px !important;z-index:90}
#toc.toc{display:flex;flex-direction:column;gap:1px}
.tocitem{color:#4a6a86 !important;border-left:1px solid #dbe2eb !important;border-radius:0 5px 5px 0 !important;padding:7px 10px 7px 8px !important;font-size:11px !important;font-weight:500 !important;line-height:1.25em !important;text-decoration:none !important;transition:all .15s ease !important;display:block !important}
.tocitem:hover{color:#070e27 !important;background-color:rgba(41,98,255,0.06) !important;border-left:2px solid #070e27 !important;padding-left:7px !important}
.tocitem.active{color:#070e27 !important;font-weight:700 !important;background-color:rgba(41,98,255,0.08) !important;border-left:2px solid #2962ff !important;padding-left:7px !important}

/* Seine-style Sticky Floating Mobile/Desktop Bar */
.sticky-mobile-bar{position:fixed;bottom:0;left:0;right:0;width:100%;background:rgba(255,255,255,0.96);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);box-shadow:0 -6px 24px rgba(15,23,42,0.12);border-top:1px solid rgba(226,232,240,0.9);z-index:9999;padding:10px 16px;box-sizing:border-box;transform:translateY(110%);opacity:0;pointer-events:none;transition:transform .3s cubic-bezier(.16,1,.3,1),opacity .25s ease}
.sticky-mobile-bar.visible{transform:translateY(0);opacity:1;pointer-events:auto}
.sticky-inner{max-width:1060px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:16px}
.sticky-boat-info{display:flex;align-items:center;gap:12px;min-width:0;flex:1}
.sticky-thumb-img{width:44px;height:44px;border-radius:8px;object-fit:cover;flex-shrink:0;box-shadow:0 2px 6px rgba(0,0,0,0.15)}
.sticky-text{display:flex;flex-direction:column;gap:2px;min-width:0}
.sticky-title-row{display:flex;align-items:center;gap:8px;min-width:0}
.sticky-rank-badge{background:#fef3c7;color:#92400e;border:1px solid #fde68a;font-size:10px;font-weight:800;padding:2px 6px;border-radius:4px;white-space:nowrap}
.sticky-title-row strong{font-size:13.5px;font-weight:800;color:#0f172a;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sticky-meta-row{display:flex;align-items:center;gap:6px;font-size:12px;color:#64748b;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sticky-price-tag{font-weight:800;color:#047857}
.sticky-bullet{color:#cbd5e1;font-size:10px}
.sticky-desc-text{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.btn-sticky-cta{display:inline-flex;align-items:center;justify-content:center;gap:6px;background:linear-gradient(135deg,#059669 0%,#047857 100%);color:#ffffff;font-size:13.5px;font-weight:800;padding:10px 22px;border-radius:10px;text-decoration:none;box-shadow:0 4px 14px rgba(5,150,105,0.35);transition:all .15s ease;flex-shrink:0;letter-spacing:.2px}
.btn-sticky-cta:hover{background:linear-gradient(135deg,#047857 0%,#065f46 100%);box-shadow:0 6px 18px rgba(5,150,105,0.45);transform:translateY(-1px);color:#ffffff}
@media (max-width:768px){
  .sticky-mobile-bar{padding:8px 12px}
  .sticky-inner{gap:10px}
  .sticky-thumb-img{width:38px;height:38px}
  .sticky-title-row strong{font-size:12.5px}
  .sticky-rank-badge{display:none}
  .sticky-desc-text{display:none}
  .sticky-bullet{display:none}
  .btn-sticky-cta{padding:8px 15px;font-size:12.5px}
  .bpa-acc-header{padding:14px 16px}
  .bpa-acc-title{font-size:16px}
  .bpa-acc-toggle-text{display:none}
}
</style>"""

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
      const cnt=c.parentElement.querySelector(".bpa-counter-pill");
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
      const cnt=c.parentElement.querySelector(".bpa-counter-pill");
      if(cnt)cnt.textContent=idx+" / "+c.children.length;
      c._ticking=false;
    });
  };

  const cruises=[
    {id:"1-legenda",r:"1",tag:"🏆 #1 Best Overall",name:"Legenda City Cruises",p:"€20–25",d:"Dock 7 • Welcome Drink Included",l:"https://legenda.hu/en?partner=38585",t:"1. Best Cruise Overall: Budapest Day or Night River Cruise with Audio Guide & Welcome Drink"},
    {id:"2-rubingroup",r:"2",tag:"🥂 #2 Unlimited Drinks",name:"Rubin Group Prosecco",p:"€25",d:"Dock 11 • Unlimited Prosecco &amp; Aperol",l:"https://www.getyourguide.com/budapest-l29/budapest-unlimited-prosecco-party-cruise-with-boat-tour-t416276/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-river-cruises-h3-rubin-btn&mkt_cmp=true",t:"2. Best Unlimited Drinks: Night Cruise with Prosecco &amp; Aperol"},
    {id:"4-kisfaludy-historic-cruise",r:"3",tag:"🚢 #3 Historic Steamer",name:"Kisfaludy Steam Boat",p:"€10–32",d:"Dock 10 • 19th-Century Paddle Steamer",l:"https://www.getyourguide.com/budapest-l29/budapest-city-lights-evening-or-night-cruise-on-steam-boat-t863690/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-river-cruises-h3-kisfaludy-btn&mkt_cmp=true",t:"3. Best Historic Cruise: River Cruise on 19th-Century Steam Boat"},
    {id:"3-portum",r:"4",tag:"💰 #4 Budget Value",name:"Portum Lines Cruising",p:"€14",d:"Dock 42 • Budget Friendly with Drink",l:"https://www.getyourguide.com/budapest-l29/budapest-boat-cruise-cocktail-drink-t73250/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-river-cruises-h3-portum-btn&mkt_cmp=true",t:"4. Best Budget Value: Sightseeing Cruise with Welcome Drink"},
    {id:"5-silverline-no-frills",r:"5",tag:"💸 #5 No-Frills Budget",name:"Silverline No-Frills",p:"€12–14",d:"Dock 11 • 75-Min Pure Sightseeing",l:"https://budapestrivercruise.eu/product/budapest-sightseeing-cruises/?code=bpa-river-cruises-silverline-no-frills-btn",t:"5. No-Frills Budget Cruise: Sightseeing without Welcome Drink"},
    {id:"6-sunset-cocktail-cruise",r:"6",tag:"🍸 #6 Best Cocktail Cruise",name:"Silverline Cocktails",p:"€32–37",d:"Dock 11 • 2 Fresh Cocktails Included",l:"https://budapestrivercruise.eu/product/sunset-cocktail-cruise/?code=bpa-river-cruises-silverline-cocktail-btn",t:"6. Best Cocktail Cruise: Sightseeing Cruise With 2 Cocktails"},
    {id:"9-pizza-and-beer-cruise",r:"7",tag:"🍕 #7 Best Pizza Cruise",name:"Silverline Pizza & Beer",p:"€35–39",d:"Dock 11 • Warm Pizza &amp; Unlimited Beer",l:"https://budapestrivercruise.eu/product/pizza-cruise-budapest/?code=bpa-river-cruises-silverline-pizza-btn",t:"7. Best Pizza Cruise: Sightseeing Cruise with Pizza &amp; Unlimited Beer"},
    {id:"7-hk-dinner-cruise",r:"8",tag:"🍽️ #8 Buffet & Folk Show",name:"Hungária Koncert Dinner",p:"€89",d:"Vigadó Dock • Warm Buffet &amp; Live Show",l:"https://budapestxplore.com/en/served-dinner-and-cruise-with-live-music-and-folklore-show-xpZWMYjcMjIw?affi=6876",t:"8. Buffet Dinner Cruise With Live Folk Music &amp; Dance Show"},
    {id:"8-hk-drinks-cruise",r:"9",tag:"🍻 #9 Folklore Drinks",name:"Hungária Koncert Drinks",p:"€21–65",d:"Vigadó Dock • Live Music &amp; 3 Drinks",l:"https://www.getyourguide.com/budapest-l29/budapest-evening-cruise-including-drinks-and-live-music-t40871/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-river-cruises-h3-hk-drinks-btn&mkt_cmp=true",t:"9. Folklore Drinks Cruise: Night Cruise with Cocktails, Beer or Wine"},
    {id:"10-mahart",r:"10",tag:"☀️ #10 Cheapest Day Ferry",name:"Mahart Hop-On Hop-Off",p:"€12–18",d:"Vigadó Dock 5 • Margaret Island Pass",l:"https://www.getyourguide.com/budapest-l29/budapest-winter-cruise-from-downtown-to-margaret-island-t69093/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-river-cruises-h3-mahart-btn&mkt_cmp=true",t:"10. Cheapest Day Cruise: Budapest Sightseeing Cruise with Welcome Drink"}
  ];

  window.bpaToggleAcc=function(id,forceOpen){
    const card=document.getElementById(id);
    if(!card)return;
    const isOpen=card.classList.contains("is-open");
    const willOpen=forceOpen!==undefined?forceOpen:!isOpen;
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
    cruises.forEach(c=>{
      bpaToggleAcc(c.id,openAll);
    });
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

    const items=[
      {id:"0-itinerary-and-landmarks",text:"Budapest Boat Tour Itinerary & Map"},
      {id:"river-cruises-breakdown",text:"Detailed Breakdown — 10 Best River Cruises"}
    ];
    cruises.forEach(c=>{
      items.push({id:c.id,text:c.r+". "+c.name});
    });
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

final_html = css + deck_html + js

print("CSS length:", len(css))
print("Deck length:", len(deck_html))
print("JS length:", len(js))
print("Total length:", len(final_html))

if len(final_html) <= 50000:
    with open("/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_10_river_cruises.html", "w") as out:
        out.write(final_html)
    print("SUCCESS: File saved and within 50k limit!")
else:
    print("WARNING: Exceeds 50k limit by", len(final_html) - 50000)
