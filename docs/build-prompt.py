import html

PROMPT = r'''Build "Metropolitan Trails — Shanghai", a private research tool for a small group
(2-4 people) documenting walking routes through Shanghai. It surfaces space and history
that normal city maps and tourist routes leave out: colonial history, old industrial
zones, urban villages and migrant communities, and how gender-friendly public space is.

This is NOT a public product. Access is by direct URL and everyone with the link is a
trusted collaborator. No sign-up, no login, no accounts, no moderation.

=== PLATFORM ===
Web. A responsive single-page web app opened at a URL. Not native, not a PWA. No offline
mode, no install prompt, no app shell.

The primary device is a laptop, 1280-1680px wide: that is where the map is read, trails
are compared and narratives are written. A phone browser must be good enough to add a pin
and read a trail while standing in the street — iOS Safari especially, because the
fieldwork happens on phones — but the phone is the secondary case, not the design driver.
Tablet follows the desktop layout.

There is no landing page, no marketing page and no home page. The URL opens directly onto
the map with the seeded trail already visible. Anyone arriving has been invited.

Interface language is English. Place names, stop titles and feeling tags carry 中文
alongside the English. Do not build a language switcher.

Responsive behaviour:
  desktop   map fills the viewport; pin detail is a panel over the bottom-left; the stop
            strip sits beneath the map; the key panel sits bottom-right.
  phone     map fills the viewport; pin detail becomes a bottom sheet; the stop strip
            becomes a horizontal scroller; the key panel collapses to one line.

=== STACK ===
React + Vite + TypeScript + Tailwind. Supabase for Postgres and Storage.
MapLibre GL JS for the map (not Leaflet, not Google Maps).

=== DATA MODEL ===
Two tables. Keep it loose; optimise for "easy to add an entry", not normalisation.

trails
  id           uuid primary key default gen_random_uuid()
  title        text not null            -- bilingual, e.g. "杨树浦路：水厂到电厂 / Yangshupu Road"
  theme        text not null            -- colonial_history | industrial_zone | urban_village | gender_friendliness | other
  author       text not null
  description  text                     -- short framing: why this trail exists
  created_at   timestamptz default now()

pins
  id           uuid primary key default gen_random_uuid()
  trail_id     uuid references trails(id) on delete cascade
  position     int not null             -- order along the trail, 1-based
  lat          float8 not null
  lng          float8 not null
  title        text not null
  title_zh     text
  year         text                     -- e.g. "1883", "1920s"
  body         text                     -- the observation / reflection
  tag          text                     -- comfortable | oppressive | safe | inconvenient | nostalgic
  photo_url    text
  author       text not null
  created_at   timestamptz default now()

Supabase Storage bucket "pin-photos", public read, anon insert.
Enable RLS but allow read and write for the anon role on both tables. The group is
trusted; do not build permissions.

=== SCREENS ===

1. MAP (home). Full-bleed map. Every trail draws as a route line connecting its pins in
   order, with numbered circular markers. Theme filter chips along the bottom. Clicking a
   pin opens the pin detail. A key panel bottom-right lists the trails; the selected one
   is full strength, the others recede. Beneath the map, a horizontal strip of the
   selected trail's stops, one column each.

2. PIN DETAIL. A panel over the map, bottom-left on desktop and a bottom sheet on mobile.
   Shows photo, title, Chinese title, year, body text, feeling tag, author, and distance
   along the trail.

3. TRAIL NARRATIVE at /trail/:id. A scrollable, numbered, top-to-bottom reading of one
   trail: photo and text per stop, in order. Header carries title, theme, author,
   description, total distance and stop count. This is the "read the trail as a story"
   mode and is separate from the free-roam map.

4. ADD TRAIL. Form: title, theme (select), author, description.

5. ADD PIN. Form: choose an existing trail, place the location by clicking the map (also
   allow pasting "lat, lng"), then title, Chinese title, year, body, feeling tag, photo
   upload, author. It must work whether or not you created the trail — one person walks
   and annotates someone else's route.

6. THEME FILTERING on the map via the chips, and the same chips filter the trail list.

=== DESIGN LANGUAGE: "NEWSPRINT" ===
Chosen from a five-palette study. It is a PRINTED MAP look — a research instrument, not a
travel app, and not a dark dashboard.

Tokens:
  --ground      #EDEAE2   page and map background (warm paper)
  --ink         #22201C   primary text and map labels
  --street      #2E2B27   road linework
  --water       #6E93A1   water edge and hydronym labels
  --water-fill  #D9E4E8   water body fill
  --accent      #C63A22   INK RED - trails, active chips, tags, stop numbers
  --rule        rgba(34,32,28,0.24)   hairlines

Ink red is the identity colour and the single accent. Nothing else on a printed map is
red, so it reads as "route" with no ambiguity. Do NOT substitute green (reads as
parkland), blue (reads as water), or near-black (sinks into the road network). These were
tested and rejected.

Type: Archivo for everything structural (700/800 weights; use the condensed widths for
small uppercase labels) and IBM Plex Mono for data - coordinates, distances, dates,
eyebrow lines. Both from Google Fonts. Small labels are uppercase with ~0.12em letter
spacing. Use tabular numerals wherever figures align in columns.

Rules:
  - Square corners everywhere. No rounded cards, no drop shadows, no gradients, no glass.
  - Hairline rules, not heavy borders. Let spacing do the separating.
  - Bilingual throughout: place names carry 中文 and English together; feeling tags show
    both, e.g. "不便 INCONVENIENT".
  - Numbering encodes real stop order, so use it. Do not add decorative 01/02/03 markers
    anywhere else.
  - Documentary and slightly austere in tone. No friendly illustration, no pastel, no
    emoji, no rounded playfulness.

=== MAP STYLE (this part matters most) ===
MapLibre GL JS with OpenFreeMap vector tiles - https://tiles.openfreemap.org/planet -
which needs no API key. Write a CUSTOM style; do not use an off-the-shelf basemap.
Centre 31.265, 121.52 (Yangpu, Shanghai) at zoom 12.5.

  - Background: #EDEAE2.
  - Water: filled #D9E4E8 with a #6E93A1 hairline edge. Water is a printed TINT, never a
    hole. This is the single most important rule for making it read as printed.
  - Roads, by class, with minor roads dropped right back so the arterials carry the
    structure:
      motorway / trunk / primary   #2E2B27, opacity 0.88, width 2.3 at z12
      secondary / tertiary         #2E2B27, opacity 0.50, width 1.15
      residential / service        #2E2B27, opacity 0.26, width 0.62
  - Rounded line caps and joins.
  - Turn OFF: road casings, building fills, POI icons, green landuse, street name labels.
    The map is line-work only.
  - Labels: settlement and district names only. Uppercase, ~0.12em letter spacing, #22201C
    at 78% opacity, with a #EDEAE2 halo 2px.

Components:
  - TOP BAR: "03. SHANGHAI — 杨树浦路 YANGSHUPU ROAD — Y. ZHOU & K. LIN". Trail number in
    ink red 800 weight, the rest in ink, uppercase and letter-spaced, hairline rule under.
  - ROUTE LINE: 5px ink red, round caps, with an 11px --ground halo beneath so it stays
    legible crossing the road network.
  - PIN MARKERS: 8.5px ink red circles with a 2.4px --ground stroke and the stop number
    inside in paper colour, Archivo 800, 10.5px.
  - FRICTION MARKS: an ✗ drawn in --ink with a --ground halo, placed where the route is
    obstructed — a forced detour, a locked gate, a fence. This is a first-class device,
    not decoration: the project is about what the city stops you doing, and this is the
    only way the map can say it. Add an "obstruction" boolean to pins to drive it.
  - PIN CARD: --ground background, 1px --rule border, square corners. Eyebrow line in ink
    red mono uppercase ("STOP 02 · 1.9 KM · Y. ZHOU · 19.08.26"), then the English title,
    then Chinese title · year at 60% opacity, then body, then the feeling tag as a SOLID
    ink red chip with paper text.
  - THEME CHIPS: pills, 1px --rule border, uppercase Archivo condensed 10.5px, 0.1em
    letter spacing. Active chip is solid ink red with paper text.
  - STOP STRIP: a row beneath the map, one column per stop, divided by hairlines. Each
    column: "01 · 0.0 KM" in ink red mono, title, Chinese · year at 52%, a one-line blurb,
    then the feeling tag as an outlined pill.
  - KEY PANEL: bottom-right of the map. --ground background, --rule border. One row per
    trail: name, then a short colour bar. Selected trail at full opacity, others at 58%.

=== SEED DATA ===
Seed one real trail so the app is never empty.

Trail: "杨树浦路：水厂到电厂 / Yangshupu Road: Waterworks to Powerhouse"
  theme industrial_zone, author "Y. Zhou & K. Lin", 6.8 km, 6 stops.
  description: "Six and a half kilometres of the East Bund, where Shanghai's first
  waterworks, first power station and first shipyard now sit inside one continuous public
  promenade completed in 2019. The route asks a single question at every stop: what does
  the promenade let you approach, and what does it walk you past?"

  1. Qinhuangdao Rd Wharf / 秦皇岛路码头 / 1930s / 31.25285, 121.50701 / 0.0 km /
     comfortable — "The ferry still runs every twelve minutes and costs two yuan. On the
     deck nobody looks at the skyline; they look at their phones, or at the water. This
     pier is the only place on the whole route where you can stand at the river's edge
     with nothing between you and it."

  2. Yangshupu Waterworks / 杨树浦水厂 / 1883 / 31.26121, 121.52520 / 1.9 km /
     inconvenient / OBSTRUCTION — "The waterworks has drawn from the Huangpu since 1883
     and it is still working, so the promenade cannot cross it. Instead you are lifted
     onto a 550-metre steel walkway hung out over the water, which puts a fence and eight
     metres of air between you and the castellated brick you came to look at. You pass the
     building without ever being beside it."

  3. Cotton & Hemp Warehouse / 毛麻仓库 / 1920 / 31.26533, 121.53120 / 3.3 km / safe —
     "New paving, new lighting, a security guard at each end and no shade anywhere. At
     three in the afternoon this is the safest and least occupied stretch of the entire
     route: twelve people in twenty minutes, nine of them walking through, none of them
     sitting down."

  4. Power Plant Ash Silo / 杨树浦发电厂灰仓 / 1913 / 31.27457, 121.54699 / 4.9 km /
     oppressive — "Coal ash was stored here for eighty years. The concrete cylinders are
     an art space now, with a café on the roof; the walls were never painted and still
     smell of cement dust when it rains. Inside the silo your own footsteps come back at
     you about half a second late."

  5. Dinghaiqiao / 定海桥 / 1920s- / 31.27909, 121.55400 / 5.7 km / nostalgic — "Two
     blocks inland the promenade's vocabulary stops. Shops face the street, laundry
     crosses the lane, the ground floor is doing five jobs at once. This is where the
     people who serviced the mills lived, and it is the only place on the route where
     anyone asked us what we were doing."

  6. Fuxing Island / 复兴岛 / 1920s / 31.28544, 121.56199 / 6.8 km / oppressive /
     OBSTRUCTION — "The island is state land and mostly closed. The gate stands open, but
     there is a guard post beside it and a sign listing what may not be photographed. We
     walked eight hundred metres in and found nowhere to sit down."

=== DO NOT BUILD ===
Comments or replies. Real-time sync (people refresh). Login, accounts, or roles.
Moderation. Notifications. Search. Dark mode. Onboarding or tours. A marketing or landing
page. Analytics. Offline or mobile capture. Leave room in the schema for comments later,
but build no UI for them.'''

ESC = html.escape(PROMPT)
WORDS = len(PROMPT.split())

SW = [("--ground", "#EDEAE2", "Paper ground"), ("--ink", "#22201C", "Text and map labels"),
      ("--street", "#2E2B27", "Road linework"), ("--water", "#6E93A1", "Water edge"),
      ("--water-fill", "#D9E4E8", "Water fill"), ("--accent", "#C63A22", "Ink red — the trail")]
swatches = "\n".join(
    f'<div class="sw"><i style="background:{h}"></i><b>{n}</b><em>{h}</em><span>{d}</span></div>'
    for n, h, d in SW)

open('metropolitan-trails-prompt.txt', 'w', encoding='utf-8').write(PROMPT)
open('lovable-prompt.html', 'w', encoding='utf-8').write(f'''<meta charset="utf-8">
<title>Metropolitan Trails Build Prompt</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--ground:#EDEAE2;--ink:#22201C;--street:#2E2B27;--water:#6E93A1;
 --water-fill:#D9E4E8;--accent:#C63A22;--rule:rgba(34,32,28,.24);--rule2:rgba(34,32,28,.12);
 --cjk:"PingFang SC","Hiragino Sans GB","Noto Sans SC";}}
*{{box-sizing:border-box}}
body{{background:var(--ground);color:var(--ink);
 font-family:Archivo,var(--cjk),system-ui,sans-serif;font-size:15px;line-height:1.62}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 28px}}
h1,h2{{margin:0;text-wrap:balance;letter-spacing:-.02em;font-weight:800}}
:focus-visible{{outline:2px solid var(--accent);outline-offset:3px}}
.top{{display:flex;align-items:baseline;gap:0;padding:13px 0;font-size:13.5px;font-weight:600;
 letter-spacing:.055em;text-transform:uppercase;border-bottom:1px solid var(--rule)}}
.top b{{font-weight:800;color:var(--accent);margin-right:.5em}}
header{{padding:44px 0 26px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:34px;align-items:end}}
header h1{{font-size:clamp(28px,4vw,42px);line-height:1.04}}
header p{{max-width:60ch;margin:14px 0 0;opacity:.76}}
.meta{{font-family:"IBM Plex Mono",monospace;font-size:11.5px;line-height:2;opacity:.72;
 border-left:1px solid var(--rule);padding-left:18px;white-space:nowrap}}
.meta b{{font-weight:500;opacity:1}}
.actions{{display:flex;align-items:center;gap:12px;padding:0 0 16px;flex-wrap:wrap}}
button{{font:inherit;font-weight:700;font-size:12.5px;letter-spacing:.11em;text-transform:uppercase;
 background:var(--accent);color:var(--ground);border:0;padding:11px 20px;cursor:pointer}}
button:hover{{opacity:.9}}
button.ghost{{background:none;color:var(--ink);border:1px solid var(--rule)}}
.hint{{font-family:"IBM Plex Mono",monospace;font-size:11.5px;opacity:.6}}
pre{{background:#F6F4EE;border:1px solid var(--rule);margin:0;padding:22px 24px;
 font-family:"IBM Plex Mono",monospace;font-size:12px;line-height:1.66;white-space:pre-wrap;
 word-wrap:break-word;max-height:62vh;overflow:auto}}
h2{{font-size:19px;margin:52px 0 4px}}
.lede{{opacity:.72;margin:0 0 20px;max-width:64ch}}
.sws{{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:0;
 border-top:1px solid var(--rule)}}
.sw{{padding:14px 16px 16px 0;border-right:1px solid var(--rule2)}}
.sw:last-child{{border-right:0}}
.sw i{{display:block;height:44px;border:1px solid var(--rule);margin-bottom:10px}}
.sw b{{display:block;font-family:"IBM Plex Mono",monospace;font-size:11.5px;font-weight:500}}
.sw em{{display:block;font-family:"IBM Plex Mono",monospace;font-style:normal;font-size:11.5px;
 color:var(--accent);margin:2px 0 4px}}
.sw span{{font-size:12px;opacity:.66}}
.checks{{border-top:1px solid var(--rule);padding-top:18px;margin-top:6px}}
.checks li{{margin:0 0 9px;max-width:70ch;opacity:.82}}
footer{{margin:60px 0 80px;padding-top:18px;border-top:1px solid var(--rule);
 font-family:"IBM Plex Mono",monospace;font-size:11.5px;opacity:.6}}
@media(max-width:820px){{header,.meta{{grid-template-columns:1fr}}
 .meta{{border-left:0;border-top:1px solid var(--rule);padding:14px 0 0}}}}
</style>

<div class="wrap">
  <div class="top"><b>03. SHANGHAI</b> — Metropolitan Trails — Build prompt for Lovable</div>

  <header>
    <div>
      <h1>Paste this into Lovable</h1>
      <p>The full MVP brief: platform, stack, schema, five screens, the Newsprint design
         language and the map style, plus one seeded trail with real coordinates. Written so Lovable has
         no room to invent a generic travel app.</p>
    </div>
    <div class="meta">
      <b>Words</b>&nbsp; {WORDS}<br>
      <b>Platform</b>&nbsp; Responsive web, desktop-first<br>
      <b>Stack</b>&nbsp; React · Supabase · MapLibre<br>
      <b>Palette</b>&nbsp; Newsprint / ink red<br>
      <b>Seed</b>&nbsp; 1 trail · 6 stops
    </div>
  </header>

  <div class="actions">
    <button id="copy" type="button">Copy prompt</button>
    <span class="hint" id="status"></span>
  </div>

  <pre id="prompt">{ESC}</pre>

  <h2>Palette</h2>
  <p class="lede">These six values are in the prompt. Ink red is the identity colour and the
     only accent — green, blue and near-black were tested against this map and rejected.</p>
  <div class="sws">{swatches}</div>

  <h2>What to check when it comes back</h2>
  <ul class="checks">
    <li><b>Water is a filled tint, not a hole.</b> This is the single thing that decides whether it reads as a printed map. If the water is the same colour as the land, the style did not apply.</li>
    <li><b>Minor roads are far lighter than the arterials.</b> If every road is the same weight it becomes grey mush and the route stops standing out.</li>
    <li><b>The route is the only red thing.</b> If chips, links and errors are also red, the accent stops meaning "route".</li>
    <li><b>Square corners.</b> Lovable's defaults are rounded; expect to push back once.</li>
    <li><b>The ✗ friction marks exist</b> on stops 2 and 6. They are the whole argument of the project and are the first thing an AI builder drops.</li>
    <li><b>Adding a pin works on a trail you did not create.</b> Easy to get wrong when there is no auth to hang it on.</li>
  </ul>

  <footer>Base map © OpenStreetMap contributors, ODbL · seed coordinates measured along 杨树浦路 · sample field notes, not verified</footer>
</div>

<script>
const pre = document.getElementById('prompt');
const status = document.getElementById('status');
function flash(m){{ status.textContent = m; setTimeout(() => status.textContent = '', 2600); }}
document.getElementById('copy').addEventListener('click', async () => {{
  try {{ await navigator.clipboard.writeText(pre.textContent); flash('Copied — paste into Lovable.'); }}
  catch (e) {{
    const r = document.createRange(); r.selectNodeContents(pre);
    const s = getSelection(); s.removeAllRanges(); s.addRange(r);
    flash('Selected — press ⌘C to copy.');
  }}
}});
</script>
''')
print('words', WORDS)
