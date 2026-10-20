#!/usr/bin/env python3
"""
Luxury Editorial Profile Asset Generator (v5)
Features:
- Self-contained Project Cards with embedded key features, summary bullets, metrics & architecture diagrams
- Individual moving neon pink border lines on EVERY Bento box in the Toolset (Languages, Frontend, etc.)
- Moving neon pink border lines on outer card perimeters
- Zero mentions of "Gemini" or "LLM"
- High-contrast Georgia serif titles & precision monospace eyebrows
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

def neon_border(w, h, rx=16, dur="8s", dash=130):
    """Generate SVG elements for the moving neon pink border line."""
    p = int(2 * (w + h) - (8 - 6.283) * rx)
    gap = p - dash
    return f"""
  <!-- Static Base Border -->
  <rect width="{w}" height="{h}" rx="{rx}" fill="none" stroke="#701A3D" stroke-opacity="0.5" stroke-width="1.2"/>

  <!-- Neon Glow Soft Filter Layer -->
  <rect width="{w-2}" height="{h-2}" x="1" y="1" rx="{rx-1}" fill="none"
        stroke="#C77B9B" stroke-width="3" stroke-linecap="round" opacity="0.45"
        stroke-dasharray="{dash} {gap}" stroke-dashoffset="0" filter="url(#neon-glow)">
    <animate attributeName="stroke-dashoffset" from="0" to="-{p}" dur="{dur}" repeatCount="indefinite"/>
  </rect>

  <!-- Core Neon Moving Line -->
  <rect width="{w-2}" height="{h-2}" x="1" y="1" rx="{rx-1}" fill="none"
        stroke="#F8F0F3" stroke-width="1.8" stroke-linecap="round"
        stroke-dasharray="{dash} {gap}" stroke-dashoffset="0">
    <animate attributeName="stroke-dashoffset" from="0" to="-{p}" dur="{dur}" repeatCount="indefinite"/>
  </rect>
    """

# -------------------------------------------------------------
# 1. Section Headers
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
# 2. Luxury Project Architecture Cards (Full-Width, Self-Contained)
# -------------------------------------------------------------
def make_luxury_project_card(eyebrow, title, one_liner, built_highlight, bullets, metrics, tags, diag_type, filename):
    w, h = 1000, 336
    key = filename.replace(".svg", "").replace("-", "_")

    # Bullets rendering inside the card (Key Features + Summary)
    bullet_svgs = []
    by = 164
    for b in bullets:
        if isinstance(b, tuple):
            lead, detail = b
            content = f'<tspan font-weight="700" fill="#F8F0F3">{esc(lead)}: </tspan><tspan fill="#E5B5C7" opacity="0.9">{esc(detail)}</tspan>'
        else:
            content = f'<tspan fill="#E5B5C7" opacity="0.95">{esc(b)}</tspan>'
        bullet_svgs.append(f"""
    <g transform="translate(36, {by})">
      <circle cx="3" cy="-3.5" r="2.5" fill="#C77B9B"/>
      <text x="14" y="0" font-family="{SANS}" font-size="11.5">{content}</text>
    </g>""")
        by += 21

    # Metrics rendering (3 big numbers + labels)
    metric_svgs = []
    mx = 36
    for val, lbl in metrics:
        metric_svgs.append(f"""
      <g transform="translate({mx}, 254)">
        <text x="0" y="0" font-family="{SERIF}" font-size="26" font-weight="700" fill="#F8F0F3">{esc(val)}</text>
        <text x="0" y="15" font-family="{MONO}" font-size="9.5" font-weight="500" fill="#C77B9B" letter-spacing="1">{esc(lbl.upper())}</text>
      </g>""")
        mx += 175

    # Tags rendering
    tag_svgs = []
    tx = 36
    for tag in tags:
        tw = len(tag) * 7.2 + 18
        tag_svgs.append(f"""
      <g transform="translate({tx}, 292)">
        <rect width="{tw}" height="22" rx="11" fill="#14080F" stroke="#451126" stroke-width="0.9"/>
        <text x="{tw/2}" y="15" text-anchor="middle" font-family="{MONO}" font-size="9.5" fill="#E5B5C7">{esc(tag)}</text>
      </g>""")
        tx += tw + 8

    # Right-side architecture diagram (h=250px)
    if diag_type == "resq":
        diagram = """
      <!-- Architecture Flow: Incident -> AI Triage -> GIS Route -->
      <g transform="translate(620, 38)">
        <rect width="344" height="258" rx="12" fill="#14080F" stroke="#451126" stroke-width="1"/>
        <text x="18" y="26" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" fill="#C77B9B" letter-spacing="1.5">ARCHITECTURE FLOW</text>
        
        <circle cx="316" cy="22" r="4" fill="#C77B9B">
          <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
        </circle>

        <!-- Connecting Bezier Lines with flowing pulse -->
        <path d="M 65 95 C 100 95, 110 145, 150 145" fill="none" stroke="#701A3D" stroke-width="1.8"/>
        <path d="M 200 145 C 235 145, 245 95, 280 95" fill="none" stroke="#701A3D" stroke-width="1.8"/>

        <!-- Flowing photon pulse on path -->
        <circle cx="65" cy="95" r="3.5" fill="#F8F0F3">
          <animateMotion path="M 0 0 C 35 0, 45 50, 85 50 C 120 50, 130 0, 165 0 C 130 0, 120 50, 85 50 C 45 50, 35 0, 0 0" dur="4s" repeatCount="indefinite"/>
        </circle>

        <!-- Node 1: Incident -->
        <g transform="translate(22, 78)">
          <rect width="84" height="34" rx="6" fill="#190B12" stroke="#701A3D" stroke-width="1"/>
          <text x="42" y="21" text-anchor="middle" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" fill="#E5B5C7">INCIDENT</text>
        </g>

        <!-- Node 2: AI Triage Engine -->
        <g transform="translate(128, 128)">
          <rect width="95" height="34" rx="6" fill="#190B12" stroke="#C77B9B" stroke-width="1.2"/>
          <text x="47" y="21" text-anchor="middle" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" font-weight="700" fill="#F8F0F3">AI TRIAGE</text>
        </g>

        <!-- Node 3: GIS Route -->
        <g transform="translate(238, 78)">
          <rect width="84" height="34" rx="6" fill="#190B12" stroke="#701A3D" stroke-width="1"/>
          <text x="42" y="21" text-anchor="middle" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" fill="#E5B5C7">GIS ROUTE</text>
        </g>

        <!-- Dynamic Radar Sweep & Specs -->
        <g transform="translate(18, 194)">
          <circle cx="16" cy="16" r="14" fill="none" stroke="#701A3D" stroke-width="1"/>
          <circle cx="16" cy="16" r="8" fill="none" stroke="#C77B9B" stroke-width="1.2">
            <animate attributeName="r" values="8;18;8" dur="2.5s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.9;0;0.9" dur="2.5s" repeatCount="indefinite"/>
          </circle>
          <line x1="16" y1="16" x2="28" y2="8" stroke="#E5B5C7" stroke-width="1.5" stroke-linecap="round">
            <animateTransform attributeName="transform" type="rotate" from="0 16 16" to="360 16 16" dur="3.5s" repeatCount="indefinite"/>
          </line>
          <text x="44" y="14" font-family="'SFMono-Regular', Consolas, monospace" font-size="9.5" fill="#E5B5C7" font-weight="600">DYNAMIC REPLANNING ACTIVE</text>
          <text x="44" y="27" font-family="'SFMono-Regular', Consolas, monospace" font-size="8.5" fill="#C77B9B" opacity="0.8">FAIL-SAFE HEURISTIC · SUPABASE RLS</text>
        </g>
      </g>"""
    elif diag_type == "code":
        diagram = """
      <!-- Architecture Flow: Code Input -> AST Parser -> AI Analysis -->
      <g transform="translate(620, 38)">
        <rect width="344" height="258" rx="12" fill="#14080F" stroke="#451126" stroke-width="1"/>
        <text x="18" y="26" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" fill="#C77B9B" letter-spacing="1.5">INTELLIGENCE PIPELINE</text>
        
        <circle cx="316" cy="22" r="4" fill="#C77B9B">
          <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
        </circle>

        <!-- Scanning Beam across simulated code lines -->
        <g transform="translate(24, 62)">
          <line x1="0" y1="14" x2="85" y2="14" stroke="#701A3D" stroke-width="2"/>
          <line x1="10" y1="28" x2="75" y2="28" stroke="#451126" stroke-width="2"/>
          <line x1="10" y1="42" x2="90" y2="42" stroke="#701A3D" stroke-width="2"/>
          <line x1="0" y1="56" x2="55" y2="56" stroke="#451126" stroke-width="2"/>
          <rect x="0" y="0" width="3" height="70" fill="#C77B9B">
            <animate attributeName="x" values="0;90;0" dur="2.5s" repeatCount="indefinite"/>
          </rect>
        </g>

        <!-- Connector -->
        <path d="M 128 98 L 152 98" stroke="#701A3D" stroke-width="1.8"/>

        <!-- Center AI Analyzer -->
        <g transform="translate(152, 80)">
          <rect width="94" height="36" rx="6" fill="#190B12" stroke="#C77B9B" stroke-width="1.2"/>
          <text x="47" y="22" text-anchor="middle" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" font-weight="700" fill="#F8F0F3">AI ANALYZER</text>
        </g>

        <!-- Connector -->
        <path d="M 246 98 L 272 98" stroke="#701A3D" stroke-width="1.8"/>

        <!-- Verdict Node -->
        <g transform="translate(272, 80)">
          <rect width="52" height="36" rx="6" fill="#190B12" stroke="#701A3D" stroke-width="1"/>
          <text x="26" y="22" text-anchor="middle" font-family="'SFMono-Regular', Consolas, monospace" font-size="9.5" fill="#E5B5C7">AUDIT</text>
        </g>

        <!-- Bottom specs note -->
        <g transform="translate(18, 194)">
          <text x="0" y="14" font-family="'SFMono-Regular', Consolas, monospace" font-size="9.5" fill="#E5B5C7" font-weight="600">STRUCTURED FEEDBACK DIAGNOSTICS</text>
          <text x="0" y="27" font-family="'SFMono-Regular', Consolas, monospace" font-size="8.5" fill="#C77B9B" opacity="0.8">TIME &amp; SPACE COMPLEXITY · BUG LOCALIZATION</text>
        </g>
      </g>"""
    else: # fraud shield
        diagram = """
      <!-- Architecture Flow: Imbalanced Stream -> Ensemble Pipeline -> Metric Gauge -->
      <g transform="translate(620, 38)">
        <rect width="344" height="258" rx="12" fill="#14080F" stroke="#451126" stroke-width="1"/>
        <text x="18" y="26" font-family="'SFMono-Regular', Consolas, monospace" font-size="10" fill="#C77B9B" letter-spacing="1.5">CLASSIFIER BENCHMARK</text>
        
        <circle cx="316" cy="22" r="4" fill="#C77B9B">
          <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
        </circle>

        <!-- Dynamic Gauge Needle -->
        <g transform="translate(74, 114)">
          <path d="M -34 0 A 34 34 0 0 1 34 0" fill="none" stroke="#451126" stroke-width="7"/>
          <path d="M -34 0 A 34 34 0 0 1 24 -24" fill="none" stroke="#C77B9B" stroke-width="7"/>
          <circle cx="0" cy="0" r="4.5" fill="#F8F0F3"/>
          <line x1="0" y1="0" x2="18" y2="-20" stroke="#F8F0F3" stroke-width="2.2" stroke-linecap="round">
            <animateTransform attributeName="transform" type="rotate" values="-35 0 0; 35 0 0; 26 0 0; -35 0 0" dur="4s" repeatCount="indefinite"/>
          </line>
          <text x="0" y="24" text-anchor="middle" font-family="'SFMono-Regular', Consolas, monospace" font-size="10.5" font-weight="700" fill="#E5B5C7">99.4% F1</text>
        </g>

        <!-- Model Compare Bars on right -->
        <g transform="translate(156, 76)">
          <text x="0" y="10" font-family="'SFMono-Regular', Consolas, monospace" font-size="9" fill="#C77B9B">RANDOM FOREST</text>
          <rect x="0" y="15" width="140" height="7" rx="3.5" fill="#451126"/>
          <rect x="0" y="15" width="138" height="7" rx="3.5" fill="#C77B9B"/>

          <text x="0" y="40" font-family="'SFMono-Regular', Consolas, monospace" font-size="9" fill="#C77B9B">XGBOOST</text>
          <rect x="0" y="45" width="140" height="7" rx="3.5" fill="#451126"/>
          <rect x="0" y="45" width="131" height="7" rx="3.5" fill="#A24A70"/>

          <text x="0" y="70" font-family="'SFMono-Regular', Consolas, monospace" font-size="9" fill="#C77B9B">LOGISTIC REG</text>
          <rect x="0" y="75" width="140" height="7" rx="3.5" fill="#451126"/>
          <rect x="0" y="75" width="102" height="7" rx="3.5" fill="#701A3D"/>
        </g>

        <!-- Bottom specs note -->
        <g transform="translate(18, 194)">
          <text x="0" y="14" font-family="'SFMono-Regular', Consolas, monospace" font-size="9.5" fill="#E5B5C7" font-weight="600">REAL-TIME RISK SERVER</text>
          <text x="0" y="27" font-family="'SFMono-Regular', Consolas, monospace" font-size="8.5" fill="#C77B9B" opacity="0.8">0.17% FRAUD BASE RATE · THREE.JS WEB CLIENT</text>
        </g>
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
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <!-- Card Background -->
  <rect width="{w}" height="{h}" rx="16" fill="url(#lxc-bg-{key})"/>
  <rect width="{w}" height="{h}" rx="16" fill="url(#lxc-glow-{key})"/>

  <!-- Left Accent Notch -->
  <rect x="0" y="32" width="4" height="64" rx="2" fill="#C77B9B"/>

  <!-- Eyebrow -->
  <text x="36" y="44" font-family="{MONO}" font-size="11" font-weight="700" fill="#C77B9B" letter-spacing="2">{esc(eyebrow.upper())}</text>

  <!-- Title -->
  <text x="36" y="80" font-family="{SERIF}" font-size="32" font-weight="700" fill="#F8F0F3" letter-spacing="0.3">{esc(title)}</text>

  <!-- One-liner Description -->
  <text x="36" y="104" font-family="{SANS}" font-size="13" fill="#E5B5C7" opacity="0.95">{esc(one_liner)}</text>

  <!-- BUILT Highlight Strip -->
  <g transform="translate(36, 118)">
    <rect width="560" height="25" rx="6" fill="#190B12" stroke="#451126" stroke-width="0.9"/>
    <rect x="0" y="0" width="54" height="25" rx="6" fill="#701A3D"/>
    <text x="27" y="16" text-anchor="middle" font-family="{MONO}" font-size="9.5" font-weight="700" fill="#F8F0F3" letter-spacing="1">BUILT</text>
    <text x="66" y="16" font-family="{MONO}" font-size="10" fill="#E5B5C7">{esc(built_highlight)}</text>
  </g>

  <!-- Summary & Key Feature Bullets inside the card -->
  {"".join(bullet_svgs)}

  <!-- 3 Big Metric Counters -->
  {"".join(metric_svgs)}

  <!-- Tech tags -->
  {"".join(tag_svgs)}

  <!-- Right Architecture Flow Diagram -->
  {diagram}

  <!-- Animated Neon Pink Moving Border -->
  {neon_border(w, h, rx=16, dur="7.5s", dash=150)}
</svg>"""
    write_svg(filename, svg)

# -------------------------------------------------------------
# 3. The 6-Box Bento Grid with Moving Neon Lines on EVERY Box!
# -------------------------------------------------------------
def make_bento_grid():
    w, h = 1000, 370
    boxes = [
        # Col 0, Row 0
        {"idx": "01", "cat": "LANGUAGES", "x": 20, "y": 24, "w": 300, "h": 150, "dur": "4.2s",
         "items": [("Java", True), ("Python", False), ("C / C++", False), ("TypeScript · JavaScript", False)]},
        # Col 1, Row 0
        {"idx": "02", "cat": "AI & MACHINE LEARNING", "x": 350, "y": 24, "w": 300, "h": 150, "dur": "4.6s",
         "items": [("Deep Learning", True), ("scikit-learn · XGBoost", False), ("Neural Networks & NLP", False), ("Feature Engineering", False)]},
        # Col 2, Row 0
        {"idx": "03", "cat": "FRONTEND", "x": 680, "y": 24, "w": 300, "h": 150, "dur": "4.0s",
         "items": [("Next.js · React", True), ("HTML5 · Vanilla CSS", False), ("Tailwind CSS", False), ("Responsive & GIS UI", False)]},
        # Col 0, Row 1
        {"idx": "04", "cat": "BACKEND & APIS", "x": 20, "y": 196, "w": 300, "h": 150, "dur": "4.8s",
         "items": [("FastAPI", True), ("Node.js · Express", False), ("REST APIs · Microservices", False), ("JWT Auth · RBAC", False)]},
        # Col 1, Row 1
        {"idx": "05", "cat": "DATA & CLOUD", "x": 350, "y": 196, "w": 300, "h": 150, "dur": "4.4s",
         "items": [("Supabase", True), ("SQL · MySQL", False), ("PostgreSQL", False), ("Vercel Deployment", False)]},
        # Col 2, Row 1
        {"idx": "06", "cat": "CS & FUNDAMENTALS", "x": 680, "y": 196, "w": 300, "h": 150, "dur": "4.3s",
         "items": [("Data Structures & Algorithms", True), ("OOP · DBMS", False), ("Operating Systems · Networks", False), ("Git · GitHub · VS Code", False)]},
    ]

    card_elements = []
    box_p = int(2 * (300 + 150) - (8 - 6.283) * 12)  # ~880px
    box_dash = 70
    box_gap = box_p - box_dash

    for b in boxes:
        bx, by, bw, bh, bdur = b["x"], b["y"], b["w"], b["h"], b["dur"]
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
        <!-- Box Background -->
        <rect width="{bw}" height="{bh}" rx="12" fill="#14080F"/>
        <rect x="0" y="0" width="{bw}" height="28" rx="12" fill="#190B12"/>
        <rect x="0" y="16" width="{bw}" height="12" fill="#190B12"/>
        <line x1="0" y1="28" x2="{bw}" y2="28" stroke="#451126" stroke-width="1"/>

        <!-- Header eyebrow -->
        <text x="16" y="18" font-family="{MONO}" font-size="10" font-weight="700" fill="#C77B9B" letter-spacing="1.5">{esc(b["idx"])}  {esc(b["cat"])}</text>

        <!-- Items list -->
        {"".join(item_svgs)}

        <!-- Base box border -->
        <rect width="{bw}" height="{bh}" rx="12" fill="none" stroke="#701A3D" stroke-opacity="0.4" stroke-width="1"/>

        <!-- Animated Moving Neon Pink Border for THIS box -->
        <rect width="{bw-2}" height="{bh-2}" x="1" y="1" rx="11" fill="none"
              stroke="#C77B9B" stroke-width="2.6" stroke-linecap="round" opacity="0.45"
              stroke-dasharray="{box_dash} {box_gap}" stroke-dashoffset="0" filter="url(#neon-glow)">
          <animate attributeName="stroke-dashoffset" from="0" to="-{box_p}" dur="{bdur}" repeatCount="indefinite"/>
        </rect>
        <rect width="{bw-2}" height="{bh-2}" x="1" y="1" rx="11" fill="none"
              stroke="#F8F0F3" stroke-width="1.6" stroke-linecap="round"
              stroke-dasharray="{box_dash} {box_gap}" stroke-dashoffset="0">
          <animate attributeName="stroke-dashoffset" from="0" to="-{box_p}" dur="{bdur}" repeatCount="indefinite"/>
        </rect>
      </g>""")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="The tools I reach for - Bento Grid">
  <defs>
    <linearGradient id="bg-bento" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10070C"/>
      <stop offset="50%" stop-color="#14080F"/>
      <stop offset="100%" stop-color="#10070C"/>
    </linearGradient>
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <rect width="{w}" height="{h}" rx="16" fill="url(#bg-bento)"/>

  {"".join(card_elements)}

  <!-- Outer container moving neon pink border -->
  {neon_border(w, h, rx=16, dur="8s", dash=160)}
</svg>"""
    write_svg("skills.svg", svg)

# -------------------------------------------------------------
# 4. Unified Commit Log & Snake Card with Moving Neon Border
# -------------------------------------------------------------
def make_unified_commit_log():
    w, h = 1000, 320

    total_contribs = 51
    repos_count = 8
    longest_streak = 3
    days = []

    try:
        c_req = urllib.request.Request("https://github-contributions-api.jogruber.de/v4/siddharth-meka-16?y=last", headers={"User-Agent": "profile-activity"})
        with urllib.request.urlopen(c_req, timeout=10) as r:
            c_data = json.load(r)
        days = c_data.get("contributions", [])
        total_contribs = c_data.get("total", {}).get("lastYear", 51)
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

    months = ["NOV", "DEC", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT"]
    month_svgs = []
    for i, m in enumerate(months):
        mx = x0 + int(i * 4.35 * (cell + gap))
        month_svgs.append(f'<text x="{mx}" y="{y0 - 10}" font-family="{MONO}" font-size="10" fill="#C77B9B" opacity="0.8">{m}</text>')

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
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <rect width="{w}" height="{h}" rx="16" fill="url(#act-bg)"/>
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

  <!-- Animated Neon Pink Moving Border -->
  {neon_border(w, h, rx=16, dur="8s", dash=160)}
</svg>"""
    write_svg("activity.svg", svg)

# -------------------------------------------------------------
# 5. Luxury Certifications Shelf with Moving Neon Border
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
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <rect width="{w}" height="{h}" rx="16" fill="url(#cert-bg)"/>
  {"".join(cards_svg)}

  <!-- Animated Neon Pink Moving Border -->
  {neon_border(w, h, rx=16, dur="7.5s", dash=140)}
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
    # 1. Section headers
    make_section_header("01", "Introduction", "Curiosity, code, and practical intelligence.", "section-01-introduction.svg")
    make_section_header("02", "Featured Work", "Selected systems & architecture platforms.", "section-02-projects.svg")
    make_section_header("03", "Toolset", "The tools I reach for.", "section-04-skills.svg")
    make_section_header("04", "Credentials", "Verified certifications & honors.", "section-03-certifications.svg")
    make_section_header("05", "Commit Log", "A year of building, one square at a time.", "section-05-activity.svg")
    make_section_header("06", "Connect", "Professional links & contact.", "section-06-links.svg")

    # 2. Luxury Project Architecture Cards (Key features, summary bullets & architecture ALL INSIDE THE CARD!)
    make_luxury_project_card(
        "01 — FULL-STACK & AI — 2024",
        "ResQ",
        "Real-Time Disaster Coordination and Dynamic AI Relief Platform",
        "AI incident classification + dynamic flood-route replanning + Supabase RLS",
        [
            ("Disaster Coordination", "Real-time incident dispatching, GIS map & workflows"),
            ("Dynamic AI Routing", "Incident classification with fail-safe heuristic engine"),
            ("Production Architecture", "Vercel deployment + Supabase Row Level Security (RLS)")
        ],
        [("LIVE", "DISPATCH ENGINE"), ("100%", "DATA ISOLATION"), ("< 2s", "DYNAMIC RE-ROUTE")],
        ["Next.js", "React", "TypeScript", "Supabase", "AI Incident Engine", "Leaflet GIS"],
        "resq",
        "project-resq.svg"
    )

    make_luxury_project_card(
        "02 — AI & DEVELOPER TOOLS — 2024",
        "AI Code Explainer",
        "AI-Powered Code Analysis & Algorithmic Complexity Platform",
        "Python FastAPI + AST parser + bug localization + React feedback UI",
        [
            ("Code Intelligence", "Explains syntax & semantics, detects bugs & audits complexity"),
            ("FastAPI Backend", "Sub-180ms real-time AST parsing & structured insights engine"),
            ("Developer Feedback", "Clean diagnostics & recommendations to debug and optimize")
        ],
        [("O(N)", "COMPLEXITY AUDIT"), ("100%", "STRUCTURED AST"), ("< 180ms", "FASTAPI LATENCY")],
        ["React", "FastAPI", "Python", "Code Intelligence", "AST Analyzer", "Tailwind"],
        "code",
        "project-code-explainer.svg"
    )

    make_luxury_project_card(
        "03 — MACHINE LEARNING — 2024",
        "Fraud Shield",
        "AI Fraud Detection System on Imbalanced Financial Streams",
        "Random Forest + XGBoost benchmark + FastAPI risk server + Three.js UI",
        [
            ("Imbalanced ML", "End-to-end classifier benchmark on 0.17% skewed transaction data"),
            ("Ensemble Benchmark", "Random Forest achieved 99.4% F1 & 99.5% ROC-AUC over XGBoost"),
            ("Real-Time Inference", "FastAPI risk server paired with interactive 3D Three.js UI")
        ],
        [("99.4%", "RANDOM FOREST F1"), ("99.5%", "ROC-AUC SCORE"), ("0.17%", "EXTREME FRAUD RATE")],
        ["Python", "FastAPI", "scikit-learn", "XGBoost", "JavaScript", "Three.js"],
        "shield",
        "project-fraud-shield.svg"
    )

    # 3. The 6-Box Bento Grid (Every single box has its OWN moving neon pink border!)
    make_bento_grid()

    # 4. Unified Commit Log Card
    make_unified_commit_log()

    # 5. Buttons
    make_button("VIEW REPOSITORY →", "arrow", 185, "link-repo-resq.svg")
    make_button("siddharth-meka-16", "github", 195, "link-github.svg")
    make_button("siddharth-meka", "linkedin", 185, "link-linkedin.svg")

    # 6. Certifications Shelf
    make_certifications()

if __name__ == "__main__":
    main()
