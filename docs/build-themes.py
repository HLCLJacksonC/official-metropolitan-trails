# Generates colour-themes.html: one real-OSM board, re-themed live via CSS custom properties.
# Palettes are edited HERE, not in the 445 KB of generated HTML. Run: python3 build-themes.py
# Geometry is lifted from visual-directions.html so there is one source of OSM truth.
import json, re

src = open('visual-directions.html', encoding='utf-8').read()
_data = json.loads(re.search(r'const OSM = (\{.*?\});\n', src, re.S).group(1))
_shorts = re.findall(r"short:'((?:[^'\\]|\\.)*)'", src)
_gallery_order = ['Qinhuangdao Rd Wharf', 'Yangshupu Waterworks', 'Power Plant Ash Silo',
                  'Cotton & Hemp Warehouse', 'Dinghaiqiao', 'Fuxing Island']
_by_en = dict(zip(_gallery_order, _shorts))
for _st in _data['stops']:
    _st['short'] = _by_en[_st['en']]
OSM = json.dumps(_data, ensure_ascii=False, separators=(',', ':'))

THEMES = [
    dict(id='night', name='Night network', zh='夜网',
         note='Neutral dark. The city is white, the walk is the only colour in it.',
         ground='#121212', street='#F2F0EC', water='#7FA8BE', waterFill='#1B2A31',
         waterLabel='#8FB6C9', accent='#9EE86B', label='#F2F0EC',
         rule='rgba(242,240,236,.3)', grain='.2',
         waterPunch='#121212', op1='.95', op2='.72', op3='.46', otherOp='.38'),
    dict(id='cyanotype', name='Cyanotype', zh='蓝晒',
         note='The waterworks and the power station were drawn in this palette. Amber is the annotation ink.',
         ground='#0A2137', street='#C3DAEA', water='#5E93B5', waterFill='#0E2C45',
         waterLabel='#7FB0CE', accent='#F2C14E', label='#DCEAF4',
         rule='rgba(220,234,244,.32)', grain='.18',
         waterPunch='#0A2137', op1='.95', op2='.72', op3='.46', otherOp='.4'),
    dict(id='sodium', name='Sodium', zh='钠灯',
         note='Sodium street lighting against the cold LED of the new promenade — the two lights this walk happens under after dark.',
         ground='#14100B', street='#E3B571', water='#5A4A32', waterFill='#1E1810',
         waterLabel='#A8875A', accent='#6FD8E0', label='#F2DFBE',
         rule='rgba(242,223,190,.3)', grain='.22',
         waterPunch='#14100B', op1='.95', op2='.72', op3='.46', otherOp='.4'),
    dict(id='silt', name='Silt', zh='泥沙',
         note='The Huangpu’s own colour, and the oxide red of everything on this route that has stopped working.',
         ground='#191C18', street='#DAD5C4', water='#6E6647', waterFill='#221F16',
         waterLabel='#9A9070', accent='#E4572E', label='#E8E3D3',
         rule='rgba(232,227,211,.3)', grain='.2',
         waterPunch='#191C18', op1='.95', op2='.72', op3='.46', otherOp='.38'),
    # Not an inverted dark palette: on paper the water is a printed tint rather than a
    # void, the minor roads drop back hard, and the other trails have to come forward.
    dict(id='newsprint', name='Newsprint', zh='新闻纸',
         note='Water is a printed tint, not a void, and the minor roads drop right back. The route is ink red.',
         ground='#EDEAE2', street='#2E2B27', water='#6E93A1', waterFill='#D6E2E6',
         waterLabel='#4B707E', accent='#C63A22', label='#22201C',
         rule='rgba(34,32,28,.24)', grain='.05',
         waterPunch='#D9E4E8', op1='.88', op2='.5', op3='.26', otherOp='.6'),
]
ROLES = [('ground','Ground'), ('street','Street network'), ('water','Water'),
         ('accent','Trail'), ('label','Labels')]

theme_css = '\n'.join(
    f'.cv[data-t="{t["id"]}"]{{--ground:{t["ground"]};--street:{t["street"]};--water:{t["water"]};'
    f'--water-fill:{t["waterFill"]};--water-label:{t["waterLabel"]};--accent:{t["accent"]};'
    f'--label:{t["label"]};--rule:{t["rule"]};--grain:{t["grain"]};'
    f'--water-punch:{t["waterPunch"]};--op1:{t["op1"]};--op2:{t["op2"]};--op3:{t["op3"]};'
    f'--other-op:{t["otherOp"]}}}' for t in THEMES)

cards = '\n'.join(f'''      <button type="button" class="tcard" data-set="{t['id']}" aria-pressed="false">
        <span class="sw"><i style="background:{t['ground']}"></i><i style="background:{t['street']}"></i><i style="background:{t['water']}"></i><i style="background:{t['accent']}"></i></span>
        <b>{t['name']}</b><span class="zh">{t['zh']}</span>
        <span class="note">{t['note']}</span>
      </button>''' for t in THEMES)

head = ''.join(f'<th>{t["name"]}</th>' for t in THEMES)
rows = ''
for key, lbl in ROLES:
    cells = ''.join(f'<td><i style="background:{t[key]}"></i>{t[key].upper()}</td>' for t in THEMES)
    rows += f'    <tr><th scope="row">{lbl}</th>{cells}</tr>\n'

html = f'''<meta charset="utf-8">
<title>Yangshupu in Five Palettes</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{{
  --paper:#F2F1EE; --card:#FBFAF8; --ink:#17181A; --ink2:#5C6067; --ink3:#8A8E96;
  --hair:#D2CFC8; --hair2:#E2DFD9; --link:#2E4A7D;
  --cjk:"PingFang SC","Hiragino Sans GB","Noto Sans SC","Microsoft YaHei";
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
  --paper:#121316; --card:#191B1F; --ink:#E9E8E4; --ink2:#9BA0A8; --ink3:#71767E;
  --hair:#2E3238; --hair2:#24272C; --link:#93B2E4;}}}}
:root[data-theme="dark"]{{
  --paper:#121316; --card:#191B1F; --ink:#E9E8E4; --ink2:#9BA0A8; --ink3:#71767E;
  --hair:#2E3238; --hair2:#24272C; --link:#93B2E4;}}
*{{box-sizing:border-box}}
body{{background:var(--paper);color:var(--ink);font-family:"IBM Plex Sans",var(--cjk),system-ui,sans-serif;
  font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1220px;margin:0 auto;padding:0 28px}}
h1,h2{{text-wrap:balance;margin:0}}
:focus-visible{{outline:2px solid var(--link);outline-offset:3px;border-radius:2px}}
.eyebrow{{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink3)}}
.mast{{padding:64px 0 28px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:36px;align-items:end}}
.mast h1{{font-size:clamp(30px,4.4vw,44px);line-height:1.06;font-weight:600;letter-spacing:-.022em;margin-top:14px}}
.mast p{{max-width:62ch;color:var(--ink2);margin:16px 0 0}}
.spec{{font-family:"IBM Plex Mono",monospace;font-size:11.5px;line-height:2;color:var(--ink2);
  border-left:1px solid var(--hair);padding-left:18px;white-space:nowrap}}
.spec b{{color:var(--ink);font-weight:500}}

/* ---- switcher ---- */
.picker{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;padding:26px 0 24px;
  border-top:1px solid var(--hair);margin-top:30px}}
.tcard{{font:inherit;text-align:left;background:var(--card);border:1px solid var(--hair);border-radius:3px;
  padding:13px 14px 15px;cursor:pointer;display:flex;flex-direction:column;gap:2px;transition:.15s;color:inherit}}
.tcard:hover{{border-color:var(--ink3)}}
.tcard[aria-pressed="true"]{{border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}}
.tcard .sw{{display:flex;gap:0;margin-bottom:10px;border-radius:2px;overflow:hidden;border:1px solid var(--hair2)}}
.tcard .sw i{{display:block;height:26px;flex:1}}
.tcard b{{font-size:14px;font-weight:600;letter-spacing:-.01em}}
.tcard .zh{{font-size:11.5px;color:var(--ink3);margin-bottom:5px}}
.tcard .note{{font-size:11.5px;line-height:1.45;color:var(--ink2)}}

/* ---- the board, themed ---- */
.board{{border:1px solid var(--hair);border-radius:3px;overflow:hidden;overflow-x:auto}}
.cv{{background:var(--ground);color:var(--label);font-family:Archivo,var(--cjk),sans-serif;min-width:900px}}
.cv .map{{position:relative}}
.cv svg{{display:block}}
.cv .bg{{fill:var(--ground)}}
.cv .net{{stroke:var(--street)}}
.cv .n1{{stroke-opacity:var(--op1)}}
.cv .n2{{stroke-opacity:var(--op2)}}
.cv .n3{{stroke-opacity:var(--op3)}}
.cv .other{{stroke-opacity:var(--other-op)}}
.cv .punch{{stroke:var(--water-punch)}}
.cv .tint{{stroke:var(--water)}}
.cv .lake{{fill:var(--water-fill);stroke:var(--water)}}
.cv .other-h{{stroke:var(--ground)}}
.cv .other{{stroke:var(--accent)}}
.cv .place{{fill:var(--label);stroke:var(--ground)}}
.cv .hydro{{fill:var(--water-label);stroke:var(--ground)}}
.cv .rte-h{{stroke:var(--ground)}}
.cv .rte{{stroke:var(--accent)}}
.cv .dot{{fill:var(--accent);stroke:var(--ground)}}
.cv .dotn{{fill:var(--ground)}}
.cv .xh{{stroke:var(--ground)}}
.cv .xl{{stroke:var(--label)}}
.cv .grain{{opacity:var(--grain)}}
/* no colour transitions: thousands of svg nodes, and a half-repainted board reads as a bug */
{theme_css}

.cv .topbar{{display:flex;align-items:baseline;padding:12px 26px;font-size:14px;font-weight:600;
  letter-spacing:.055em;text-transform:uppercase;border-bottom:1px solid var(--rule)}}
.cv .topbar b{{font-weight:800;color:var(--accent);margin-right:.45em;letter-spacing:.03em}}
.cv .pincard{{position:absolute;left:26px;bottom:26px;width:300px;background:var(--ground);
  border:1px solid var(--rule);padding:16px 17px 17px}}
.cv .pincard .n{{font-size:9.5px;font-weight:700;font-stretch:76%;letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}}
.cv .pincard h4{{margin:7px 0 0;font-size:17px;font-weight:800;letter-spacing:-.01em}}
.cv .pincard .zh{{font-size:12.5px;font-weight:500;opacity:.6;margin-top:2px}}
.cv .pincard p{{margin:9px 0 0;font-size:12.5px;line-height:1.52;opacity:.82}}
.cv .pincard .tg{{display:inline-block;margin-top:12px;background:var(--accent);color:var(--ground);
  font-size:10px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:4px 10px}}
.cv .key{{position:absolute;right:26px;bottom:26px;display:flex;flex-direction:column;align-items:flex-end;
  gap:8px;background:var(--ground);border:1px solid var(--rule);padding:13px 15px}}
.cv .key div{{display:flex;align-items:center;gap:9px;font-size:11.5px;font-weight:600;opacity:.58}}
.cv .key div.on{{opacity:1}}
.cv .key i{{width:24px;height:3px;background:var(--accent);opacity:.42;flex:none;border-radius:2px}}
.cv .key div.on i{{height:4px;opacity:1}}
.cv .bar{{display:flex;align-items:center;gap:7px;padding:13px 26px;flex-wrap:wrap;border-top:1px solid var(--rule)}}
.cv .bar .lbl{{font-size:9.5px;font-weight:700;font-stretch:74%;letter-spacing:.18em;text-transform:uppercase;
  opacity:.5;margin-right:5px}}
.cv .chip{{font-size:10.5px;font-weight:700;font-stretch:80%;letter-spacing:.1em;text-transform:uppercase;
  border:1px solid var(--rule);border-radius:999px;padding:5px 12px}}
.cv .chip.on{{background:var(--accent);border-color:var(--accent);color:var(--ground)}}
.cv .facts{{margin-left:auto;font-size:10.5px;font-weight:700;font-stretch:76%;letter-spacing:.13em;
  text-transform:uppercase;opacity:.62;font-variant-numeric:tabular-nums}}
.cv .stops{{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));border-top:1px solid var(--rule)}}
.cv .stops > div{{padding:15px 17px 18px;border-right:1px solid var(--rule)}}
.cv .stops > div:last-child{{border-right:0}}
.cv .stops .n{{font-size:11px;font-weight:800;color:var(--accent);letter-spacing:.12em}}
.cv .stops h4{{font-size:13.5px;font-weight:700;margin:7px 0 0;line-height:1.18}}
.cv .stops .zh{{font-size:11.5px;opacity:.52;margin-top:3px}}
.cv .stops p{{font-size:11.5px;line-height:1.48;opacity:.66;margin:8px 0 0}}
.cv .stops .tg{{display:inline-block;margin-top:10px;font-size:9px;font-weight:700;font-stretch:78%;
  letter-spacing:.12em;text-transform:uppercase;border:1px solid var(--rule);border-radius:999px;padding:3px 9px;opacity:.85}}
.caption{{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--ink3);padding:11px 2px 0}}

/* ---- spec table ---- */
.specs{{margin:56px 0 0;border-top:1px solid var(--hair);padding-top:30px}}
.specs h2{{font-size:20px;font-weight:600;letter-spacing:-.015em;margin-bottom:16px}}
.tw{{overflow-x:auto}}
table{{border-collapse:collapse;width:100%;min-width:760px;font-family:"IBM Plex Mono",monospace;font-size:11.5px}}
th,td{{text-align:left;padding:10px 14px 10px 0;border-bottom:1px solid var(--hair2);white-space:nowrap}}
thead th{{color:var(--ink3);font-weight:500;letter-spacing:.08em;text-transform:uppercase;font-size:10.5px}}
tbody th{{font-weight:500;color:var(--ink2)}}
td i{{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:8px;vertical-align:-1px;
  border:1px solid var(--hair)}}
.note-out{{margin:44px 0 90px;display:grid;grid-template-columns:200px minmax(0,1fr);gap:36px}}
.note-out h2{{font-size:20px;font-weight:600;letter-spacing:-.015em}}
.note-out p{{color:var(--ink2);max-width:66ch;margin:0 0 14px}}
.note-out strong{{color:var(--ink);font-weight:600}}
@media (max-width:1000px){{.picker{{grid-template-columns:repeat(2,minmax(0,1fr))}}
  .mast,.note-out{{grid-template-columns:1fr}}
  .spec{{border-left:0;border-top:1px solid var(--hair);padding:16px 0 0}}}}
</style>

<div class="wrap">
  <header class="mast">
    <div>
      <div class="eyebrow">Metropolitan Trails · Shanghai · palette review</div>
      <h1>Five palettes, one map</h1>
      <p>The same board, the same OpenStreetMap geometry, the same six stops — only the colour changes.
         Pick a palette below and the map re-themes in place, chrome included, so you are judging a whole
         system rather than a swatch. Every value is listed at the foot of the page.</p>
    </div>
    <div class="spec">
      <b>Board</b>&nbsp; 03 · Yangshupu Rd<br>
      <b>Base map</b>&nbsp; OpenStreetMap, ODbL<br>
      <b>Roles</b>&nbsp; 5 themed, 8 tokens<br>
      <b>Date</b>&nbsp; 2026-09-03
    </div>
  </header>

  <div class="picker" role="group" aria-label="Palette">
{cards}
  </div>

  <div class="board"><div class="cv" id="cv" data-t="newsprint"></div></div>
  <div class="caption">Live re-theme — eight custom properties drive the map, the labels and every piece of chrome.</div>

  <section class="specs">
    <h2>Values</h2>
    <div class="tw"><table>
      <thead><tr><th>Role</th>{head}</tr></thead>
      <tbody>
{rows}      </tbody>
    </table></div>
  </section>

  <section class="note-out">
    <h2>Reading them</h2>
    <div>
      <p><strong>Newsprint is the one to beat</strong>, and it opens on it. It has had a proper light-map pass
         rather than being an inverted dark palette: the water is a printed tint instead of a void, the minor
         roads drop back to a quarter strength so the arterials carry the structure, and the other trails come
         forward — on paper a 38% line simply disappears. It reads as something printed rather than something
         rendered, which suits a project whose output is a walk and a set of notes rather than an app.</p>
      <p><strong>What adopting it costs.</strong> The gallery board is still green on black, so that would
         change too — one palette, not two. A light ground also gives up the thing the dark palettes do best:
         on black the lit route is the only bright object on the board and needs no help. On paper the route
         competes with the network, which is why the minor roads had to drop so far back. Watch that on the
         busiest trails.</p>
      <p><strong>The dark four, briefly.</strong> Night is the safest and the least specific — it could be any
         city. Cyanotype is the drawing office the waterworks came out of. Sodium is the light this walk
         actually happens under after dark, and is the one to revisit if the project turns toward night
         walking. Silt is the river’s own colour and the oxide red of everything on the route that has stopped
         working — the most site-specific of them, and the strongest dark counter-proposal.</p>
      <p>If Newsprint stands, the open question is the accent: <strong>ink red</strong> is doing a lot of work
         here and is the one value that will end up on everything. Worth testing against a deep green and an
         ink blue before it hardens.</p>
    </div>
  </section>
</div>

<script>
const OSM = {OSM};
const TAGS = {{comfortable:{{zh:'舒适',en:'Comfortable'}},inconvenient:{{zh:'不便',en:'Inconvenient'}},
  oppressive:{{zh:'压迫',en:'Oppressive'}},safe:{{zh:'安全',en:'Safe'}},nostalgic:{{zh:'怀旧',en:'Nostalgic'}}}};

const cross = (x,y) => `<g><path class="xh" d="M${{x-9}},${{y-9}} L${{x+9}},${{y+9}} M${{x+9}},${{y-9}} L${{x-9}},${{y+9}}"
    stroke-width="7.5" stroke-linecap="round" fill="none"/>
  <path class="xl" d="M${{x-9}},${{y-9}} L${{x+9}},${{y+9}} M${{x+9}},${{y-9}} L${{x-9}},${{y+9}}"
    stroke-width="2.8" stroke-linecap="round" fill="none"/></g>`;

const strip = OSM.stops.map((s,i) => `
  <div><div class="n">${{String(i+1).padStart(2,'0')}}&nbsp;·&nbsp;${{s.km}} KM</div>
    <h4>${{s.en}}</h4><div class="zh">${{s.zh}} · ${{s.yr}}</div><p>${{s.short}}</p>
    <span class="tg">${{TAGS[s.tag].zh}} ${{TAGS[s.tag].en}}</span></div>`).join('');
const pin = OSM.stops[1];

document.getElementById('cv').innerHTML = `
<div class="topbar"><b>03. SHANGHAI</b> — 杨树浦路 YANGSHUPU ROAD — Y. ZHOU &amp; K. LIN</div>
<div class="map">
  <svg viewBox="0 0 1000 640" width="100%" role="img"
       aria-label="Central Shanghai from OpenStreetMap — the Huangpu turning east at the Bund, Suzhou Creek and the ring roads — with the six-stop Yangshupu Road trail marked.">
    <defs><filter id="gr"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/></filter></defs>
    <rect class="bg" width="1000" height="640"/>
    <path class="lake" d="${{OSM.lake}}" stroke-opacity=".22" stroke-width=".8"/>
    <g class="net" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path class="n3" d="${{OSM.c}}" stroke-width=".62"/>
      <path class="n2" d="${{OSM.b}}" stroke-width="1.15"/>
    </g>
    <g class="punch" fill="none" stroke-linecap="round" stroke-linejoin="round">
      ${{OSM.riv.map(r=>`<path d="${{r[0]}}" stroke-width="${{r[1]}}"/>`).join('')}}
    </g>
    <g class="tint" fill="none" stroke-linecap="round" stroke-linejoin="round">
      ${{OSM.riv.map(r=>`<path d="${{r[0]}}" stroke-width="${{r[1]}}" stroke-opacity=".1"/>`).join('')}}
    </g>
    <g class="net" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path class="n1" d="${{OSM.a}}" stroke-width="2.3"/>
    </g>
    <g fill="none" stroke-linejoin="round" stroke-linecap="round">
      ${{OSM.others.map(o=>`<path class="other-h" d="${{o[0]}}" stroke-width="7" stroke-opacity=".85"/>`).join('')}}
      ${{OSM.others.map(o=>`<path class="other" d="${{o[0]}}" stroke-width="2.6"/>`).join('')}}
    </g>
    <g class="place" font-family="Archivo, sans-serif" font-weight="700" font-stretch="80%"
       paint-order="stroke" text-anchor="middle">
      ${{OSM.places.map(([x,y,t,fs,ls])=>`<text x="${{x}}" y="${{y}}" font-size="${{fs}}" letter-spacing="${{ls}}"
        stroke-width="${{fs>15?7:4.6}}" fill-opacity="${{fs>15?.58:.78}}">${{t}}</text>`).join('')}}
    </g>
    <g class="hydro" fill-opacity=".85" font-family="Archivo, sans-serif" font-weight="600" font-size="10.5"
       font-stretch="82%" letter-spacing="2.4" stroke-width="4.2" paint-order="stroke">
      <text transform="translate(392,556) rotate(-58)">黄浦江 HUANGPU</text>
      <text transform="translate(120,300) rotate(6)">苏州河 SUZHOU CREEK</text>
    </g>
    <path class="rte-h route" d="${{OSM.route}}" pathLength="1" fill="none" stroke-width="11"
          stroke-linecap="round" stroke-linejoin="round" stroke-opacity=".92"/>
    <path class="rte route" d="${{OSM.route}}" pathLength="1" fill="none" stroke-width="5"
          stroke-linecap="round" stroke-linejoin="round"/>
    ${{cross(600,367)}}${{cross(748,232)}}
    ${{OSM.stops.map((s,k)=>`
      <circle class="dot" cx="${{s.x}}" cy="${{s.y}}" r="8.5" stroke-width="2.4"/>
      <text class="dotn" x="${{s.x}}" y="${{s.y+3.6}}" text-anchor="middle" font-size="10.5"
            font-weight="800" font-family="Archivo, sans-serif">${{k+1}}</text>`).join('')}}
    <rect class="grain" width="1000" height="640" filter="url(#gr)" style="mix-blend-mode:overlay"/>
  </svg>
  <div class="pincard">
    <div class="n">Stop 02 · ${{pin.km}} km · Y. Zhou · 19.08.26</div>
    <h4>${{pin.en}}</h4><div class="zh">${{pin.zh}} · ${{pin.yr}}</div>
    <p>${{pin.short}}</p>
    <span class="tg">${{TAGS[pin.tag].zh}} ${{TAGS[pin.tag].en}}</span>
  </div>
  <div class="key">
    <div class="on">杨树浦路 Yangshupu Road · industrial zone<i></i></div>
    ${{OSM.others.map(o=>`<div>${{o[1]}}<i></i></div>`).join('')}}
  </div>
</div>
<div class="bar">
  <span class="lbl">Theme</span>
  <span class="chip on">Industrial zone</span><span class="chip">Colonial history</span>
  <span class="chip">Urban village</span><span class="chip">Gender &amp; public space</span>
  <span class="facts">4 trails · this one ${{OSM.total}} km · 2 h 30 · 6 stops · © OpenStreetMap</span>
</div>
<div class="stops">${{strip}}</div>`;

const cv = document.getElementById('cv');
const cards = [...document.querySelectorAll('.tcard')];
function pick(id){{
  cv.dataset.t = id;
  cards.forEach(c => c.setAttribute('aria-pressed', String(c.dataset.set === id)));
  try {{ localStorage.setItem('mt-palette', id); }} catch (e) {{}}
}}
cards.forEach(c => c.addEventListener('click', () => pick(c.dataset.set)));
let saved = null;
try {{ saved = localStorage.getItem('mt-palette'); }} catch (e) {{}}
pick(cards.some(c => c.dataset.set === saved) ? saved : 'newsprint');

const io = new IntersectionObserver(es => es.forEach(e => {{
  if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }}
}}), {{ threshold:.15 }});
document.querySelectorAll('.board').forEach(b => io.observe(b));
</script>
'''
open('colour-themes.html','w',encoding='utf-8').write(html)
print('written', len(html)//1024, 'kb')
