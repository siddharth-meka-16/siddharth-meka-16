#!/usr/bin/env python3
"""
Luxury Editorial Profile Asset Generator (v3)
Recreates the high-end editorial bento layout from reference screenshots:
- High-contrast Georgia serif titles & precision monospace eyebrows
- Full-width Project Showcase cards with 3 big numerical stat counters & animated SVG architecture flow diagrams
- 6-Box Bento Grid ("The tools I reach for.")
- Unified Commit Log ("A year of building, one square at a time.") combining heatmap and animated snake
- Signature Burgundy Palette: #0A0307, #10070C, #14080F, #190B12, #451126, #701A3D, #A24A70, #C77B9B, #E5B5C7, #F8F0F3
"""
import os, json, urllib.request, xml.sax.saxutils as sax

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
SERIF = "Georgia, 'Times New Roman', 'DejaVu Serif', serif"
SANS = "'Segoe UI', 'Helvetica Neue', Arial, 'DejaVu Sans', sans-serif"

def esc(text):
    return sax.escape(str(text))

def write_svg(filename, content):
    path = os.path.join(ASSETS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated {filename}")

# -------------------------------------------------------------
# 1. Section Headers (Editorial Typography with Serif + Mono Eyebrow)
# -------------------------------------------------------------
def make_section_header(num_str, eyebrow, title, filename):
    w, h = 1000, 72
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(eyebrow)} - {esc(title)}">
  <defs>
    <linearGradient id="sh-line-{num_str}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#C77B9B" stop-opacity="0.9"/>
      <stop offset="35%" stop-color="#701A3D" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#10070C" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Eyebrow -->
  <text x="4" y="22" font-family="{MONO}" font-size="11" font-weight="700" fill="#C77B9B" letter-spacing="2.5">{esc(num_str)}  ·  {esc(eyebrow.upper())}</text>

  <!-- Main Title -->
  <text x="4" y="54" font-family="{SERIF}" font-size="28" font-weight="600" fill="#F8F0F3" letter-spacing="0.2">{esc(title)}</text>

  <!-- Accent underline -->
  <line x1="4" y1="68" x2="{w-4}" y2="68" stroke="url(#sh-line-{num_str})" stroke-width="1.2"/>
</svg>"""
    write_svg(filename, svg)

# -------------------------------------------------------------
# 2. Luxury Project Architecture Cards (Screenshot 1 Reference)
# -------------------------------------------------------------
def make_luxury_project_card(eyebrow, title, one_liner, built_highlight, metrics, tags, diag_type, filename):
    w, h = 1000, 260
    key = filename.replace(".svg", "").replace("-", "_")

    # Metrics rendering (3 big numbers + labels)
    metric_svgs = []
    mx = 36
    for val, lbl in metrics:
        metric_svgs.append(f"""
      <g transform="translate({mx}, 184)">
        <text x="0" y="0" font-family="{SERIF}" font-size="28" font-weight="700" fill="#F8F0F3">{esc(val)}</text>
        <text x="0" y="16" font-family="{MONO}" font-size="10" font-weight="500" fill="#C77B9B" letter-spacing="1">{esc(lbl.upper())}</text>
      </g>""")
        mx += 175

    # Tags rendering
    tag_svgs = []
    tx = 36
    for tag in tags:
        tw = len(tag) * 7.5 + 18
        tag_svgs.append(f"""
      <g transform="translate({tx}, 218)">
        <rect width="{tw}" height="22" rx="11" fill="#14080F" stroke="#451126" stroke-width="0.9"/>
        <text x="{tw/2}" y="15" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#E5B5C7">{esc(tag)}</text>
      </g>""")
        tx += tw + 8

    # Right-side architecture diagram
    if diag_type == "resq":
        diagram = """
      <!-- Architecture Flow: Incident -> Gemini Triage -> GIS Replanning -->
      <g transform="translate(630, 40)">
        <rect width="330" height="180" rx="12" fill="#14080F" stroke="#451126" stroke-width="1"/>
        <text x="16" y="24" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" fill="#C77B9B" letter-spacing="1.5">ARCHITECTURE FLOW</text>
        
        <!-- Status dot -->
        <circle cx="304" cy="20" r="4" fill="#C77B9B">
          <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
        </circle>

        <!-- Connecting Bezier Lines with flowing pulse -->
        <path d="M 60 75 C 95 75, 105 110, 145 110" fill="none" stroke="#701A3D" stroke-width="1.8"/>
        <path d="M 195 110 C 225 110, 235 75, 270 75" fill="none" stroke="#701A3D" stroke-width="1.8"/>

        <!-- Flowing photon pulse on path -->
        <circle cx="60" cy="75" r="3" fill="#F8F0F3">
          <animateMotion path="M 0 0 C 35 0, 45 35, 85 35 C 115 35, 125 0, 160 0 C 125 0, 115 35, 85 35 C 45 35, 35 0, 0 0" dur="4s" repeatCount="indefinite"/>
        </circle>

        <!-- Node 1: Incident -->
        <g transform="translate(20, 60)">
          <rect width="80" height="30" rx="6" fill="#190B12" stroke="#701A3D" stroke-width="1"/>
          <text x="40" y="19" text-anchor="middle" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" fill="#E5B5C7">INCIDENT</text>
        </g>

        <!-- Node 2: Gemini Triage (Center) -->
        <g transform="translate(130, 95)">
          <rect width="90" height="30" rx="6" fill="#190B12" stroke="#C77B9B" stroke-width="1.2"/>
          <text x="45" y="19" text-anchor="middle" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" font-weight="700" fill="#F8F0F3">GEMINI AI</text>
        </g>

        <!-- Node 3: Route Dispatch -->
        <g transform="translate(230, 60)">
          <rect width="80" height="30" rx="6" fill="#190B12" stroke="#701A3D" stroke-width="1"/>
          <text x="40" y="19" text-anchor="middle" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" fill="#E5B5C7">GIS ROUTE</text>
        </g>

        <!-- Bottom specs note -->
        <text x="16" y="156" font-family="'SFMono-Regular', Consolas, monospace" font-size="9" fill="#C77B9B" opacity="0.8">FAIL-SAFE HEURISTIC · SUPABASE RLS</text>
      </g>"""
    elif diag_type == "code":
        diagram = """
      <!-- Architecture Flow: Code Input -> AST Parser -> Gemini Analysis -->
      <g transform="translate(630, 40)">
        <rect width="330" height="180" rx="12" fill="#14080F" stroke="#451126" stroke-width="1"/>
        <text x="16" y="24" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" fill="#C77B9B" letter-spacing="1.5">INTELLIGENCE PIPELINE</text>
        
        <circle cx="304" cy="20" r="4" fill="#C77B9B">
          <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
        </circle>

        <!-- Scanning Beam across simulated code lines -->
        <g transform="translate(24, 52)">
          <line x1="0" y1="12" x2="80" y2="12" stroke="#701A3D" stroke-width="2"/>
          <line x1="10" y1="24" x2="70" y2="24" stroke="#451126" stroke-width="2"/>
          <line x1="10" y1="36" x2="85" y2="36" stroke="#701A3D" stroke-width="2"/>
          <line x1="0" y1="48" x2="50" y2="48" stroke="#451126" stroke-width="2"/>
          <rect x="0" y="0" width="3" height="60" fill="#C77B9B">
            <animate attributeName="x" values="0;85;0" dur="2.5s" repeatCount="indefinite"/>
          </rect>
        </g>

        <!-- Connector -->
        <path d="M 125 80 L 155 80" stroke="#701A3D" stroke-width="1.8"/>

        <!-- Center Engine -->
        <g transform="translate(155, 65)">
          <rect width="80" height="32" rx="6" fill="#190B12" stroke="#C77B9B" stroke-width="1.2"/>
          <text x="40" y="20" text-anchor="middle" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" font-weight="700" fill="#F8F0F3">AST + GEMINI</text>
        </g>

        <!-- Connector -->
        <path d="M 235 80 L 265 80" stroke="#701A3D" stroke-width="1.8"/>

        <!-- Verdict Node -->
        <g transform="translate(265, 65)">
          <rect width="50" height="32" rx="6" fill="#190B12" stroke="#701A3D" stroke-width="1"/>
          <text x="25" y="20" text-anchor="middle" font-family="'SFMono-Regular', Consolas, monospace" font-size="9" fill="#E5B5C7">AUDIT</text>
        </g>

        <text x="16" y="156" font-family="'SFMono-Regular', Consolas, monospace" font-size="9" fill="#C77B9B" opacity="0.8">TIME &amp; SPACE COMPLEXITY · BUG LOCALIZATION</text>
      </g>"""
    else: # fraud shield
        diagram = """
      <!-- Architecture Flow: Imbalanced Stream -> Ensemble Pipeline -> Metric Gauge -->
      <g transform="translate(630, 40)">
        <rect width="330" height="180" rx="12" fill="#14080F" stroke="#451126" stroke-width="1"/>
        <text x="16" y="24" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" fill="#C77B9B" letter-spacing="1.5">CLASSIFIER BENCHMARK</text>
        
        <circle cx="304" cy="20" r="4" fill="#C77B9B">
          <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
        </circle>

        <!-- Dynamic Gauge Needle -->
        <g transform="translate(70, 95)">
          <path d="M -30 0 A 30 30 0 0 1 30 0" fill="none" stroke="#451126" stroke-width="6"/>
          <path d="M -30 0 A 30 30 0 0 1 20 -22" fill="none" stroke="#C77B9B" stroke-width="6"/>
          <circle cx="0" cy="0" r="4" fill="#F8F0F3"/>
          <line x1="0" y1="0" x2="16" y2="-18" stroke="#F8F0F3" stroke-width="2" stroke-linecap="round">
            <animateTransform attributeName="transform" type="rotate" values="-35 0 0; 35 0 0; 25 0 0; -35 0 0" dur="4s" repeatCount="indefinite"/>
          </line>
          <text x="0" y="22" text-anchor="middle" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" font-weight="700" fill="#E5B5C7">99.4% F1</text>
        </g>

        <!-- Model Compare Bars on right -->
        <g transform="translate(150, 60)">
          <text x="0" y="10" font-family="'SFMono-Regular', Consolas, monospace" font-size="9" fill="#C77B9B">RANDOM FOREST</text>
          <rect x="0" y="15" width="130" height="6" rx="3" fill="#451126"/>
          <rect x="0" y="15" width="128" height="6" rx="3" fill="#C77B9B"/>

          <text x="0" y="38" font-family="'SFMono-Regular', Consolas, monospace" font-size="9" fill="#C77B9B">XGBOOST</text>
          <rect x="0" y="43" width="130" height="6" rx="3" fill="#451126"/>
          <rect x="0" y="43" width="122" height="6" rx="3" fill="#A24A70"/>

          <text x="0" y="66" font-family="'SFMono-Regular', Consolas, monospace" font-size="9" fill="#C77B9B">LOGISTIC REG</text>
          <rect x="0" y="71" width="130" height="6" rx="3" fill="#451126"/>
          <rect x="0" y="71" width="95" height="6" rx="3" fill="#701A3D"/>
        </g>

        <text x="16" y="156" font-family="'SFMono-Regular', Consolas, monospace" font-size="9" fill="#C77B9B" opacity="0.8">0.17% FRAUD BASE RATE · EXTREME IMBALANCE</text>
      </g>"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)} Showcase">
  <defs>
    <linearGradient id="lxc-bg-{key}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#14080F"/>
      <stop offset="60%" stop-color="#10070C"/>
      <stop offset="100%" stop-color="#190B12"/>
    </linearGradient>
    <radialGradient id="lxc-glow-{key}" cx="0.85" cy="0.3" r="0.6">
      <stop offset="0%" stop-color="#701A3D" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#701A3D" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Card Frame -->
  <rect width="{w}" height="{h}" rx="16" fill="url(#lxc-bg-{key})" stroke="#701A3D" stroke-opacity="0.85" stroke-width="1.2"/>
  <rect width="{w}" height="{h}" rx="16" fill="url(#lxc-glow-{key})"/>

  <!-- Left Accent Notch -->
  <rect x="0" y="32" width="4" height="64" rx="2" fill="#C77B9B"/>

  <!-- Eyebrow -->
  <text x="36" y="44" font-family="{MONO}" font-size="11" font-weight="700" fill="#C77B9B" letter-spacing="2">{esc(eyebrow.upper())}</text>

  <!-- Title -->
  <text x="36" y="82" font-family="{SERIF}" font-size="34" font-weight="700" fill="#F8F0F3" letter-spacing="0.3">{esc(title)}</text>

  <!-- One-liner Description -->
  <text x="36" y="112" font-family="{SANS}" font-size="13.5" fill="#E5B5C7" opacity="0.95">{esc(one_liner)}</text>

  <!-- BUILT Highlight Strip -->
  <g transform="translate(36, 126)">
    <rect width="560" height="26" rx="6" fill="#190B12" stroke="#451126" stroke-width="0.9"/>
    <rect x="0" y="0" width="58" height="26" rx="6" fill="#701A3D"/>
    <text x="29" y="17" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" fill="#F8F0F3" letter-spacing="1">BUILT</text>
    <text x="70" y="17" font-family="{MONO}" font-size="10.5" fill="#E5B5C7">{esc(built_highlight)}</text>
  </g>

  <!-- 3 Big Metric Counters -->
  {"".join(metric_svgs)}

  <!-- Tech tags -->
  {"".join(tag_svgs)}

  <!-- Right Architecture Flow Diagram -->
  {diagram}
</svg>"""
    write_svg(filename, svg)

# -------------------------------------------------------------
# 3. The 6-Box Bento Grid ("The tools I reach for." - Screenshot 2)
# -------------------------------------------------------------
def make_bento_grid():
    w, h = 1000, 370
    boxes = [
        # Col 0, Row 0
        {"idx": "01", "cat": "LANGUAGES", "x": 20, "y": 24, "w": 300, "h": 150,
         "items": [("Java", True), ("Python", False), ("C / C++", False), ("TypeScript · JavaScript", False)]},
        # Col 1, Row 0
        {"idx": "02", "cat": "AI · ML · LLMS", "x": 350, "y": 24, "w": 300, "h": 150,
         "items": [("Gemini API", True), ("scikit-learn · XGBoost", False), ("Prompt Engineering", False), ("Deep Learning Basics", False)]},
        # Col 2, Row 0
        {"idx": "03", "cat": "FRONTEND", "x": 680, "y": 24, "w": 300, "h": 150,
         "items": [("Next.js · React", True), ("HTML5 · Vanilla CSS", False), ("Tailwind CSS", False), ("Responsive & GIS UI", False)]},
        # Col 0, Row 1
        {"idx": "04", "cat": "BACKEND & APIS", "x": 20, "y": 196, "w": 300, "h": 150,
         "items": [("FastAPI", True), ("Node.js · Express", False), ("REST APIs · Microservices", False), ("JWT Auth · RBAC", False)]},
        # Col 1, Row 1
        {"idx": "05", "cat": "DATA & CLOUD", "x": 350, "y": 196, "w": 300, "h": 150,
         "items": [("Supabase", True), ("SQL · MySQL", False), ("PostgreSQL", False), ("Vercel Deployment", False)]},
        # Col 2, Row 1
        {"idx": "06", "cat": "CS & FUNDAMENTALS", "x": 680, "y": 196, "w": 300, "h": 150,
         "items": [("Data Structures & Algorithms", True), ("OOP · DBMS", False), ("Operating Systems · Networks", False), ("Git · GitHub · VS Code", False)]},
    ]

    card_elements = []
    for b in boxes:
        bx, by, bw, bh = b["x"], b["y"], b["w"], b["h"]
        item_svgs = []
        iy = 48
        for name, is_primary in b["items"]:
            badge = ""
            if is_primary:
                badge = f"""<rect x="{len(name)*10 + 24}" y="{iy-12}" width="54" height="16" rx="8" fill="#701A3D"/>
                <text x="{len(name)*10 + 51}" y="{iy}" text-anchor="middle" font-family="{MONO}" font-size="9" font-weight="700" fill="#F8F0F3">CORE</text>"""
            item_svgs.append(f"""
        <text x="20" y="{iy}" font-family="{SERIF}" font-size="16" font-weight="600" fill="#F8F0F3">{esc(name)}</text>
        {badge}""")
            iy += 26

        card_elements.append(f"""
      <g transform="translate({bx}, {by})">
        <rect width="{bw}" height="{bh}" rx="12" fill="#14080F" stroke="#701A3D" stroke-opacity="0.75" stroke-width="1.1"/>
        <rect x="0" y="0" width="{bw}" height="28" rx="12" fill="#190B12"/>
        <rect x="0" y="16" width="{bw}" height="12" fill="#190B12"/>
        <line x1="0" y1="28" x2="{bw}" y2="28" stroke="#451126" stroke-width="1"/>

        <!-- Header eyebrow -->
        <text x="16" y="18" font-family="{MONO}" font-size="10" font-weight="700" fill="#C77B9B" letter-spacing="1.5">{esc(b["idx"])}  {esc(b["cat"])}</text>

        <!-- Items list -->
        {"".join(item_svgs)}
      </g>""")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="The tools I reach for - Bento Grid">
  <defs>
    <linearGradient id="bg-bento" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10070C"/>
      <stop offset="50%" stop-color="#14080F"/>
      <stop offset="100%" stop-color="#10070C"/>
    </linearGradient>
  </defs>

  <rect width="{w}" height="{h}" rx="16" fill="url(#bg-bento)" stroke="#701A3D" stroke-opacity="0.85" stroke-width="1.2"/>

  {"".join(card_elements)}
</svg>"""
    write_svg("skills.svg", svg)

# -------------------------------------------------------------
# 4. Unified Commit Log & Snake Card (Screenshot 3 Reference)
# -------------------------------------------------------------
def make_unified_commit_log():
    w, h = 1000, 320

    # Fetch live GitHub data
    total_contribs = 51
    repos_count = 8
    stars_count = 6
    longest_streak = 3
    days = []

    try:
        c_req = urllib.request.Request("https://github-contributions-api.jogruber.de/v4/siddharth-meka-16?y=last", headers={"User-Agent": "profile-activity"})
        with urllib.request.urlopen(c_req, timeout=10) as r:
            c_data = json.load(r)
        days = c_data.get("contributions", [])
        total_contribs = c_data.get("total", {}).get("lastYear", 51)
        # calculate longest streak
        best = cur = 0
        for d in days:
            if d.get("count", 0) > 0:
                cur += 1
                if cur > best: best = cur
            else: cur = 0
        longest_streak = best
    except Exception:
        pass

    LEVELS = ["#190B12", "#451126", "#701A3D", "#A24A70", "#C77B9B"]
    cols, rows = 53, 7
    cell, gap = 12, 4
    x0, y0 = 64, 134

    rects = []
    idx = 0
    for c in range(cols):
        for r in range(rows):
            lvl = 0
            if idx < len(days):
                lvl = min(max(0, days[idx].get("level", 0)), 4)
            idx += 1
            x = x0 + c * (cell + gap)
            y = y0 + r * (cell + gap)
            rects.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{LEVELS[lvl]}"/>')

    # Month markers
    months = ["NOV", "DEC", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT"]
    month_svgs = []
    for i, m in enumerate(months):
        mx = x0 + int(i * 4.35 * (cell + gap))
        month_svgs.append(f'<text x="{mx}" y="{y0 - 10}" font-family="{MONO}" font-size="10" fill="#C77B9B" opacity="0.8">{m}</text>')

    # Animated Burgundy Snake crawling along the real grid
    snake_animation = """
    <!-- Animated Burgundy Snake on live tiles -->
    <g>
      <path d="M 64 140 L 224 140 L 224 188 L 460 188 L 460 156 L 680 156 L 680 220 L 900 220" fill="none" stroke="#C77B9B" stroke-width="3" stroke-linecap="round" stroke-dasharray="16 120" stroke-dashoffset="0">
        <animate attributeName="stroke-dashoffset" from="0" to="-700" dur="8s" repeatCount="indefinite"/>
      </path>
      <circle cx="224" cy="140" r="4.5" fill="#F8F0F3" filter="drop-shadow(0 0 4px #C77B9B)">
        <animateMotion path="M -160 0 L 0 0 L 0 48 L 236 48 L 236 16 L 456 16 L 456 80 L 676 80" dur="8s" repeatCount="indefinite"/>
      </circle>
    </g>
    """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Commit Log - A year of building">
  <defs>
    <linearGradient id="act-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#14080F"/>
      <stop offset="60%" stop-color="#10070C"/>
      <stop offset="100%" stop-color="#190B12"/>
    </linearGradient>
    <radialGradient id="act-glow" cx="0.85" cy="0.15" r="0.5">
      <stop offset="0%" stop-color="#701A3D" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#701A3D" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="{w}" height="{h}" rx="16" fill="url(#act-bg)" stroke="#701A3D" stroke-opacity="0.85" stroke-width="1.2"/>
  <rect width="{w}" height="{h}" rx="16" fill="url(#act-glow)"/>

  <!-- Left Eyebrow -->
  <text x="36" y="38" font-family="{MONO}" font-size="11" font-weight="700" fill="#C77B9B" letter-spacing="2">COMMIT LOG  ·  REAL GITHUB ACTIVITY</text>
  <text x="36" y="68" font-family="{SERIF}" font-size="24" font-weight="600" fill="#F8F0F3">A year of building, <tspan font-style="italic" fill="#E5B5C7">one square at a time.</tspan></text>

  <!-- Top Right Live Metric Counters -->
  <g transform="translate(620, 26)">
    <text x="0" y="24" font-family="{SERIF}" font-size="30" font-weight="700" fill="#F8F0F3">{total_contribs}</text>
    <text x="0" y="40" font-family="{MONO}" font-size="9.5" fill="#C77B9B" letter-spacing="1">CONTRIBUTIONS</text>

    <text x="100" y="24" font-family="{SERIF}" font-size="30" font-weight="700" fill="#F8F0F3">{repos_count}</text>
    <text x="100" y="40" font-family="{MONO}" font-size="9.5" fill="#C77B9B" letter-spacing="1">PUBLIC REPOS</text>

    <text x="210" y="24" font-family="{SERIF}" font-size="30" font-weight="700" fill="#F8F0F3">{longest_streak}</text>
    <text x="210" y="40" font-family="{MONO}" font-size="9.5" fill="#C77B9B" letter-spacing="1">DAY STREAK</text>
  </g>

  <!-- Month markers -->
  {"".join(month_svgs)}

  <!-- Day labels on left -->
  <text x="36" y="146" font-family="{MONO}" font-size="9" fill="#C77B9B" opacity="0.8">MON</text>
  <text x="36" y="178" font-family="{MONO}" font-size="9" fill="#C77B9B" opacity="0.8">WED</text>
  <text x="36" y="210" font-family="{MONO}" font-size="9" fill="#C77B9B" opacity="0.8">FRI</text>

  <!-- Contribution Tiles -->
  <g>
    {"".join(rects)}
  </g>

  <!-- Animated Snake -->
  {snake_animation}

  <!-- Bottom Strip -->
  <text x="36" y="286" font-family="{MONO}" font-size="10" fill="#C77B9B" letter-spacing="1.5">REAL GITHUB DATA  ·  REFRESHED DAILY VIA GITHUB ACTIONS</text>

  <!-- Legend -->
  <g transform="translate({w-230}, 278)">
    <text x="0" y="9" font-family="{MONO}" font-size="9.5" fill="#C77B9B">LESS</text>
    <rect x="36" y="0" width="10" height="10" rx="2" fill="#190B12"/>
    <rect x="50" y="0" width="10" height="10" rx="2" fill="#451126"/>
    <rect x="64" y="0" width="10" height="10" rx="2" fill="#701A3D"/>
    <rect x="78" y="0" width="10" height="10" rx="2" fill="#A24A70"/>
    <rect x="92" y="0" width="10" height="10" rx="2" fill="#C77B9B"/>
    <text x="110" y="9" font-family="{MONO}" font-size="9.5" fill="#C77B9B">MORE</text>
  </g>
</svg>"""
    write_svg("activity.svg", svg)

# -------------------------------------------------------------
# 5. Luxury Certifications Shelf
# -------------------------------------------------------------
def make_certifications():
    w, h = 1000, 230
    certs = [
        ("Anthropic", "AI Fluency: Framework and Foundations", "ISSUED 2026", "VERIFIED CREDENTIAL"),
        ("Infosys Springboard", "Front End Development Certification", "ISSUED 2026", "PROFESSIONAL CERT"),
        ("Cisco Networking Academy", "Python Essentials 1", "ISSUED 2025", "FOUNDATIONAL"),
        ("Cisco Networking Academy", "Python Essentials 2", "ISSUED 2025", "INTERMEDIATE"),
    ]

    cards_svg = []
    positions = [(30, 25), (510, 25), (30, 125), (510, 125)]
    
    for i, (issuer, title, date_str, badge) in enumerate(certs):
        cx, cy = positions[i]
        cards_svg.append(f"""
    <g transform="translate({cx}, {cy})">
      <rect width="460" height="85" rx="12" fill="#14080F" stroke="#701A3D" stroke-opacity="0.75" stroke-width="1.1"/>
      <g transform="translate(26, 42)">
        <circle cx="0" cy="0" r="14" fill="#10070C" stroke="#C77B9B" stroke-width="1.2"/>
        <path d="M -5 0 L -1 4 L 6 -3" fill="none" stroke="#E5B5C7" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
      <text x="52" y="32" font-family="{MONO}" font-size="10.5" font-weight="700" fill="#C77B9B" letter-spacing="1">{esc(issuer.upper())}</text>
      <text x="52" y="52" font-family="{SERIF}" font-size="15.5" font-weight="600" fill="#F8F0F3">{esc(title)}</text>
      <text x="52" y="70" font-family="{MONO}" font-size="10" fill="#E5B5C7" opacity="0.8">{esc(date_str)}  ·  {esc(badge)}</text>
      <circle cx="438" cy="42" r="3" fill="#701A3D"/>
    </g>""")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Certifications Shelf">
  <defs>
    <linearGradient id="cert-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10070C"/>
      <stop offset="50%" stop-color="#14080F"/>
      <stop offset="100%" stop-color="#10070C"/>
    </linearGradient>
  </defs>

  <rect width="{w}" height="{h}" rx="16" fill="url(#cert-bg)" stroke="#701A3D" stroke-opacity="0.85" stroke-width="1.2"/>
  {"".join(cards_svg)}
</svg>"""
    write_svg("certifications.svg", svg)

# -------------------------------------------------------------
# 6. Action Button Badges
# -------------------------------------------------------------
def make_button(text, icon_type, w, filename):
    h = 38
    key = filename.replace(".svg", "").replace("-", "_")
    if icon_type == "github":
        icon = """
        <g transform="translate(22, 19) scale(0.8)">
          <path d="M0 -14C-7.73 -14 -14 -7.73 -14 0C-14 6.19 -9.99 11.43 -4.42 13.28C-3.72 13.41 -3.46 12.98 -3.46 12.61C-3.46 12.28 -3.47 11.19 -3.48 9.99C-7.37 10.84 -8.19 8.97 -8.19 8.97C-8.83 7.35 -9.75 6.92 -9.75 6.92C-11.02 6.05 -9.65 6.07 -9.65 6.07C-8.25 6.17 -7.51 7.51 -7.51 7.51C-6.26 9.65 -4.24 9.03 -3.44 8.67C-3.31 7.76 -2.95 7.14 -2.55 6.79C-5.66 6.44 -8.93 5.24 -8.93 -0.12C-8.93 -1.65 -8.38 -2.9 -7.48 -3.88C-7.62 -4.23 -8.1 -5.65 -7.34 -7.56C-7.34 -7.56 -6.16 -7.94 -3.47 -6.12C-2.35 -6.43 -1.17 -6.59 0 -6.59C1.17 -6.59 2.35 -6.43 3.47 -6.12C6.16 -7.94 7.34 -7.56 7.34 -7.56C8.1 -5.65 7.62 -4.23 7.48 -3.88C8.38 -2.9 8.93 -1.65 8.93 -0.12C8.93 5.25 5.65 6.43 2.54 6.78C3.03 7.2 3.46 8.04 3.46 9.32C3.46 11.16 3.44 12.64 3.44 12.61C3.44 12.98 3.7 13.42 4.42 13.28C9.99 11.43 14 6.19 14 0C14 -7.73 7.73 -14 0 -14Z" fill="#C77B9B"/>
        </g>
        """
        text_x = 38
    elif icon_type == "linkedin":
        icon = """
        <g transform="translate(22, 19) scale(0.8)">
          <rect x="-12" y="-12" width="24" height="24" rx="4" fill="#701A3D" opacity="0.3"/>
          <path d="M-8 -3H-5V6H-8V-3ZM-6.5 -7.5C-5.5 -7.5 -4.8 -6.7 -4.8 -5.7C-4.8 -4.7 -5.5 -4 -6.5 -4C-7.4 -4 -8.2 -4.7 -8.2 -5.7C-8.2 -6.7 -7.4 -7.5 -6.5 -7.5ZM-3 -3H0V-1.8H0.1C0.5 -2.6 1.6 -3.3 2.9 -3.3C5.7 -3.3 6.3 -1.5 6.3 0.9V6H3.3V1.6C3.3 0.5 3.3 -0.9 1.9 -0.9C0.5 -0.9 0.3 0.2 0.3 1.5V6H-3V-3Z" fill="#C77B9B"/>
        </g>
        """
        text_x = 38
    else: # arrow/repo button
        icon = """
        <g transform="translate(20, 19)">
          <path d="M-4 0 L4 0 M1 -4 L5 0 L1 4" stroke="#C77B9B" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        </g>
        """
        text_x = 34

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(text)}">
  <defs>
    <linearGradient id="btn-bg-{key}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#190B12"/>
      <stop offset="100%" stop-color="#10070C"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" rx="19" fill="url(#btn-bg-{key})" stroke="#701A3D" stroke-width="1.1"/>
  {icon}
  <text x="{text_x}" y="24" font-family="{MONO}" font-size="11.5" font-weight="600" fill="#F8F0F3" letter-spacing="0.5">{esc(text)}</text>
</svg>"""
    write_svg(filename, svg)

def main():
    # 1. Section headers (Editorial Serif + Eyebrow)
    make_section_header("01", "Introduction", "Curiosity, code, and practical intelligence.", "section-01-introduction.svg")
    make_section_header("02", "Featured Work", "Selected systems & architecture platforms.", "section-02-projects.svg")
    make_section_header("03", "Toolset", "The tools I reach for.", "section-04-skills.svg")
    make_section_header("04", "Credentials", "Verified certifications & honors.", "section-03-certifications.svg")
    make_section_header("05", "Commit Log", "A year of building, one square at a time.", "section-05-activity.svg")
    make_section_header("06", "Connect", "Professional links & contact.", "section-06-links.svg")

    # 2. Luxury Project Architecture Cards (Screenshot 1 Reference)
    make_luxury_project_card(
        "01 — FULL-STACK & AI — 2024",
        "ResQ",
        "Real-Time Disaster Coordination & Dynamic AI Relief Platform",
        "Gemini flood-route replanning + heuristic fail-safe + Supabase RLS",
        [("LIVE", "DISPATCH ENGINE"), ("100%", "DATA ISOLATION"), ("< 2s", "DYNAMIC RE-ROUTE")],
        ["Next.js", "React", "TypeScript", "Supabase", "Gemini API", "Leaflet GIS"],
        "resq",
        "project-resq.svg"
    )

    make_luxury_project_card(
        "02 — AI & DEVELOPER TOOLS — 2024",
        "AI Code Explainer",
        "AI-Powered Code Analysis & Algorithmic Complexity Platform",
        "Python FastAPI + Gemini API + AST inspection + React feedback UI",
        [("O(N)", "COMPLEXITY AUDIT"), ("100%", "STRUCTURED AST"), ("< 180ms", "FASTAPI LATENCY")],
        ["React", "FastAPI", "Gemini API", "Python", "AST Analyzer", "Tailwind"],
        "code",
        "project-code-explainer.svg"
    )

    make_luxury_project_card(
        "03 — MACHINE LEARNING — 2024",
        "Fraud Shield",
        "AI Fraud Detection System on Imbalanced Financial Streams",
        "Random Forest + XGBoost benchmark + FastAPI risk server + Three.js UI",
        [("99.4%", "RANDOM FOREST F1"), ("99.5%", "ROC-AUC SCORE"), ("0.17%", "EXTREME FRAUD RATE")],
        ["Python", "FastAPI", "scikit-learn", "XGBoost", "JavaScript", "Three.js"],
        "shield",
        "project-fraud-shield.svg"
    )

    # 3. The 6-Box Bento Grid (Screenshot 2 Reference)
    make_bento_grid()

    # 4. Unified Commit Log Card (Screenshot 3 Reference)
    make_unified_commit_log()

    # 5. Buttons
    make_button("VIEW REPOSITORY →", "arrow", 185, "link-repo-resq.svg")
    make_button("siddharth-meka-16", "github", 195, "link-github.svg")
    make_button("siddharth-meka", "linkedin", 185, "link-linkedin.svg")

    # 6. Certifications Shelf
    make_certifications()

if __name__ == "__main__":
    main()
