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
    if os.path.isabs(filename):
        path = filename
    elif filename.startswith("assets/") or filename.startswith("assets\\"):
        path = os.path.join(os.path.dirname(ASSETS_DIR), filename)
    else:
        path = os.path.join(ASSETS_DIR, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated {os.path.basename(path)}")

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
def make_section_header(num_str, eyebrow, title, filename, right_text=None):
    w, h = 1000, 72
    right_svg = ""
    if right_text:
        right_svg = f'<text x="{w-16}" y="22" text-anchor="end" font-family="{MONO}" font-size="10.5" font-weight="700" fill="#C77B9B" letter-spacing="1.5">{esc(right_text)}</text>'
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
  {right_svg}

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
      <text x="14" y="0" font-family="{SANS}" font-size="11" letter-spacing="0.1">{content}</text>
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
            if is_primary:
                badge = f"""<rect x="{bw - 60}" y="{iy-12}" width="44" height="15" rx="7.5" fill="#701A3D"/>
                <text x="{bw - 38}" y="{iy-1}" text-anchor="middle" font-family="{MONO}" font-size="8" font-weight="700" fill="#F8F0F3" letter-spacing="0.5">CORE</text>"""
                item_svgs.append(f"""
        <text x="18" y="{iy}" font-family="{SERIF}" font-size="15" font-weight="600" fill="#F8F0F3">{esc(name)}</text>
        {badge}""")
            else:
                item_svgs.append(f"""
        <text x="18" y="{iy}" font-family="{SANS}" font-size="12.5" font-weight="500" fill="#E5B5C7" opacity="0.9">{esc(name)}</text>""")
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
    from generate_activity import fetch_public, render_svg
    data = fetch_public("siddharth-meka-16")
    svg = render_svg(data, "siddharth-meka-16")
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
      <line x1="16" y1="1" x2="444" y2="1" stroke="#C77B9B" stroke-opacity="0.35" stroke-width="1"/>
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
# 6. GitHub At A Glance Card (Matching Screenshot 1)
# -------------------------------------------------------------
def make_github_glance(stars=6, commits=57, prs=2, issues=0, repos=8, filename="github-glance.svg"):
    w, h = 1000, 270
    
    rows = [
        ("star", "Total Stars Earned:", str(stars)),
        ("commits", "Total Commits (last year):", str(commits)),
        ("prs", "Total PRs:", str(prs)),
        ("issues", "Total Issues:", str(issues)),
        ("repos", "Contributed to (last year):", str(repos)),
    ]
    
    row_svgs = []
    ry = 106
    for icon_type, label, val in rows:
        if icon_type == "star":
            icon = '<path d="M0 -6 L1.8 -1.8 L6 -1.8 L2.6 0.8 L3.8 5.2 L0 2.6 L-3.8 5.2 L-2.6 0.8 L-6 -1.8 L-1.8 -1.8 Z" fill="#C77B9B"/>'
        elif icon_type == "commits":
            icon = '<circle cx="0" cy="0" r="5.5" fill="none" stroke="#C77B9B" stroke-width="1.3"/><path d="M0 -3 L0 0 L2.2 2.2" fill="none" stroke="#F8F0F3" stroke-width="1.3" stroke-linecap="round"/>'
        elif icon_type == "prs":
            icon = '<circle cx="-3" cy="-3.5" r="1.8" fill="none" stroke="#C77B9B" stroke-width="1.2"/><circle cx="-3" cy="3.5" r="1.8" fill="none" stroke="#C77B9B" stroke-width="1.2"/><circle cx="3" cy="-0.8" r="1.8" fill="none" stroke="#C77B9B" stroke-width="1.2"/><path d="M-3 -1.7 L-3 1.7 M-3 0.8 C-1 0.8, 3 2.5, 3 1" fill="none" stroke="#C77B9B" stroke-width="1.2"/>'
        elif icon_type == "issues":
            icon = '<circle cx="0" cy="0" r="5.5" fill="none" stroke="#C77B9B" stroke-width="1.3"/><circle cx="0" cy="0" r="2" fill="#F8F0F3"/>'
        else:
            icon = '<rect x="-4.5" y="-4.5" width="9" height="9" rx="1.8" fill="none" stroke="#C77B9B" stroke-width="1.2"/><line x1="-4.5" y1="-1" x2="4.5" y2="-1" stroke="#C77B9B" stroke-width="0.9"/><rect x="-1.8" y="-1" width="3.6" height="1.8" rx="0.5" fill="#F8F0F3"/>'
        
        row_svgs.append(f"""
      <g transform="translate(36, {ry})">
        <circle cx="12" cy="0" r="11" fill="#190B12" stroke="#451126" stroke-width="0.8"/>
        <g transform="translate(12, 0)">{icon}</g>
        <text x="32" y="4" font-family="{SANS}" font-size="13" font-weight="500" fill="#E5B5C7">{esc(label)}</text>
        <line x1="244" y1="2" x2="388" y2="2" stroke="#451126" stroke-width="1" stroke-dasharray="2 4"/>
        <rect x="398" y="-11" width="48" height="22" rx="6" fill="#190B12" stroke="#701A3D" stroke-width="1"/>
        <text x="422" y="5" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="#F8F0F3">{esc(val)}</text>
      </g>""")
        ry += 30

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="GitHub at a glance">
  <defs>
    <linearGradient id="glance-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#14080F"/>
      <stop offset="60%" stop-color="#10070C"/>
      <stop offset="100%" stop-color="#190B12"/>
    </linearGradient>
    <radialGradient id="glance-glow" cx="0.25" cy="0.4" r="0.6">
      <stop offset="0%" stop-color="#701A3D" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#701A3D" stop-opacity="0"/>
    </radialGradient>
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <rect width="{w}" height="{h}" rx="16" fill="url(#glance-bg)"/>
  <rect width="{w}" height="{h}" rx="16" fill="url(#glance-glow)"/>

  <!-- Left Header -->
  <text x="36" y="38" font-family="{MONO}" font-size="10.5" font-weight="700" fill="#C77B9B" letter-spacing="2">METRICS  ·  LIFETIME &amp; ANNUAL ACTIVITY</text>
  <text x="36" y="70" font-family="{SERIF}" font-size="28" font-weight="600" fill="#F8F0F3">GitHub at a glance</text>

  <!-- Metric Rows (Matching Screenshot 1) -->
  {"".join(row_svgs)}

  <!-- Right Side Benchmark Bento Box -->
  <g transform="translate(500, 26)">
    <rect width="464" height="218" rx="12" fill="#14080F" stroke="#451126" stroke-width="1"/>
    <rect x="0" y="0" width="464" height="28" rx="12" fill="#190B12"/>
    <rect x="0" y="16" width="464" height="12" fill="#190B12"/>
    <line x1="0" y1="28" x2="464" y2="28" stroke="#451126" stroke-width="1"/>
    <text x="18" y="18" font-family="{MONO}" font-size="10" font-weight="700" fill="#C77B9B" letter-spacing="1.5">DEVELOPER PROFILE SUMMARY</text>

    <!-- Radar / Activity Pulse in top corner -->
    <circle cx="436" cy="14" r="4" fill="#C77B9B">
      <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
    </circle>

    <!-- Benchmark Lines -->
    <g transform="translate(20, 52)">
      <circle cx="2" cy="-3" r="2.2" fill="#C77B9B"/>
      <text x="12" y="0" font-family="{MONO}" font-size="9.5" font-weight="700" fill="#C77B9B" letter-spacing="1">SPECIALIZATION</text>
      <text x="12" y="19" font-family="{SERIF}" font-size="15" font-weight="600" fill="#F8F0F3">Full-Stack AI &amp; Machine Learning</text>

      <circle cx="2" cy="43" r="2.2" fill="#C77B9B"/>
      <text x="12" y="46" font-family="{MONO}" font-size="9.5" font-weight="700" fill="#C77B9B" letter-spacing="1">ANNUAL CADENCE</text>
      <text x="12" y="65" font-family="{SERIF}" font-size="15" font-weight="600" fill="#F8F0F3">57 Contributions across 8 Public Repos</text>

      <circle cx="2" cy="89" r="2.2" fill="#C77B9B"/>
      <text x="12" y="92" font-family="{MONO}" font-size="9.5" font-weight="700" fill="#C77B9B" letter-spacing="1">PRODUCTION STACK</text>
      <text x="12" y="111" font-family="{SERIF}" font-size="15" font-weight="600" fill="#F8F0F3">Next.js · React · FastAPI · Supabase · Python</text>

      <circle cx="2" cy="135" r="2.2" fill="#E5B5C7"/>
      <text x="12" y="138" font-family="{MONO}" font-size="9.5" font-weight="700" fill="#E5B5C7" letter-spacing="1">PROFILE AVAILABILITY</text>
      <text x="12" y="157" font-family="{SERIF}" font-size="15" font-weight="600" fill="#E5B5C7">Open for Software &amp; AI/ML Internships</text>
    </g>

    <!-- Box Neon Moving Border -->
    <rect width="462" height="216" x="1" y="1" rx="11" fill="none"
          stroke="#C77B9B" stroke-width="2.2" stroke-linecap="round" opacity="0.45"
          stroke-dasharray="70 850" stroke-dashoffset="0" filter="url(#neon-glow)">
      <animate attributeName="stroke-dashoffset" from="0" to="-920" dur="4.5s" repeatCount="indefinite"/>
    </rect>
    <rect width="462" height="216" x="1" y="1" rx="11" fill="none"
          stroke="#F8F0F3" stroke-width="1.4" stroke-linecap="round"
          stroke-dasharray="70 850" stroke-dashoffset="0">
      <animate attributeName="stroke-dashoffset" from="0" to="-920" dur="4.5s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- Outer Animated Neon Pink Moving Border -->
  {neon_border(w, h, rx=16, dur="8s", dash=150)}
</svg>"""
# -------------------------------------------------------------
# 6.5 LeetCode Radial Bento Card (Concentric Gauge & Mastery Telemetry)
# -------------------------------------------------------------
def make_leetcode_radial(total=142, easy=95, med=44, hard=3, total_easy=972, total_med=2131, total_hard=984, total_q=4087, acceptance=71.5, streak=11, active_days=78, ranking=1247511, filename="leetcode.svg"):
    import math
    w, h = 1000, 280
    cx, cy = 175, 142

    # Radii and circumferences for 3 concentric rings
    r1, r2, r3 = 90, 72, 54
    c1 = 2 * math.pi * r1  # ~565.49
    c2 = 2 * math.pi * r2  # ~452.39
    c3 = 2 * math.pi * r3  # ~339.29

    # Proportional sweeps for visual elegance
    # Easy: 95 solved -> ~64% sweep
    f1 = min(0.92, max(0.12, (easy / 150) * 0.95))
    dash1 = f1 * c1
    gap1 = c1 - dash1

    # Med: 44 solved -> ~55% sweep
    f2 = min(0.90, max(0.10, (med / 80) * 0.95))
    dash2 = f2 * c2
    gap2 = c2 - dash2

    # Hard: 3 solved -> ~30% sweep
    f3 = min(0.85, max(0.08, (hard / 12) * 0.95))
    dash3 = f3 * c3
    gap3 = c3 - dash3

    # Progress bar fill widths (out of 370px)
    w_easy = int(370 * min(1.0, max(0.06, easy / 200)))
    w_med = int(370 * min(1.0, max(0.06, med / 100)))
    w_hard = int(370 * min(1.0, max(0.06, hard / 20)))

    pct_easy = (easy / total_easy * 100)
    pct_med = (med / total_med * 100)
    pct_hard = (hard / total_hard * 100)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="LeetCode Algorithmic Mastery - {total} Problems Solved">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="lc-card-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#14080F"/>
      <stop offset="60%" stop-color="#10070C"/>
      <stop offset="100%" stop-color="#0A0307"/>
    </linearGradient>

    <!-- Radial Hub Ambient Spotlight -->
    <radialGradient id="lc-spotlight" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#701A3D" stop-opacity="0.38"/>
      <stop offset="70%" stop-color="#451126" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#10070C" stop-opacity="0"/>
    </radialGradient>

    <!-- Neon Glow Filter -->
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Subtle Drop Shadow -->
    <filter id="hub-shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#C77B9B" flood-opacity="0.3"/>
    </filter>

    <!-- Progress Bar Gradients -->
    <linearGradient id="easy-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#C77B9B"/>
      <stop offset="100%" stop-color="#E5B5C7"/>
    </linearGradient>
    <linearGradient id="med-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#701A3D"/>
      <stop offset="100%" stop-color="#C77B9B"/>
    </linearGradient>
    <linearGradient id="hard-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#451126"/>
      <stop offset="100%" stop-color="#A24A70"/>
    </linearGradient>

    <!-- Ring Gradients -->
    <linearGradient id="ring-easy" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8F0F3"/>
      <stop offset="100%" stop-color="#E5B5C7"/>
    </linearGradient>
    <linearGradient id="ring-med" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E5B5C7"/>
      <stop offset="100%" stop-color="#C77B9B"/>
    </linearGradient>
    <linearGradient id="ring-hard" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#C77B9B"/>
      <stop offset="100%" stop-color="#701A3D"/>
    </linearGradient>
  </defs>

  <!-- Card Background -->
  <rect width="{w}" height="{h}" rx="16" fill="url(#lc-card-bg)"/>

  <!-- Radial Hub Ambient Light -->
  <circle cx="{cx}" cy="{cy}" r="135" fill="url(#lc-spotlight)"/>

  <!-- ================= LEFT: CONCENTRIC RADIAL GAUGE ================= -->
  <g id="radial-hub">
    <!-- Ring 1 (Easy, Outer) -->
    <circle cx="{cx}" cy="{cy}" r="{r1}" fill="none" stroke="#230E19" stroke-width="8.5"/>
    <circle cx="{cx}" cy="{cy}" r="{r1}" fill="none" stroke="url(#ring-easy)" stroke-width="8.5"
            stroke-linecap="round" stroke-dasharray="{dash1:.1f} {gap1:.1f}"
            transform="rotate(-90 {cx} {cy})"/>

    <!-- Ring 2 (Medium, Middle) -->
    <circle cx="{cx}" cy="{cy}" r="{r2}" fill="none" stroke="#230E19" stroke-width="8.5"/>
    <circle cx="{cx}" cy="{cy}" r="{r2}" fill="none" stroke="url(#ring-med)" stroke-width="8.5"
            stroke-linecap="round" stroke-dasharray="{dash2:.1f} {gap2:.1f}"
            transform="rotate(-90 {cx} {cy})"/>

    <!-- Ring 3 (Hard, Inner) -->
    <circle cx="{cx}" cy="{cy}" r="{r3}" fill="none" stroke="#230E19" stroke-width="8.5"/>
    <circle cx="{cx}" cy="{cy}" r="{r3}" fill="none" stroke="url(#ring-hard)" stroke-width="8.5"
            stroke-linecap="round" stroke-dasharray="{dash3:.1f} {gap3:.1f}"
            transform="rotate(-90 {cx} {cy})"/>

    <!-- Centerpiece Typography -->
    <g filter="url(#hub-shadow)">
      <text x="{cx}" y="{cy - 8}" text-anchor="middle" font-family="{SERIF}" font-size="38" font-weight="700" fill="#F8F0F3">{total}</text>
    </g>
    <text x="{cx}" y="{cy + 12}" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" fill="#C77B9B" letter-spacing="2.8">SOLVED</text>
    <text x="{cx}" y="{cy + 28}" text-anchor="middle" font-family="{MONO}" font-size="8.5" fill="#8E6B7A" letter-spacing="1">{total_q:,} POOL</text>

    <!-- Gauge Legend -->
    <g transform="translate(0, 0)">
      <circle cx="75" cy="254" r="4" fill="#E5B5C7"/>
      <text x="85" y="258" font-family="{MONO}" font-size="9.5" font-weight="700" fill="#E5B5C7">EASY {easy}</text>

      <circle cx="165" cy="254" r="4" fill="#C77B9B"/>
      <text x="175" y="258" font-family="{MONO}" font-size="9.5" font-weight="700" fill="#C77B9B">MED {med}</text>

      <circle cx="245" cy="254" r="4" fill="#A24A70"/>
      <text x="255" y="258" font-family="{MONO}" font-size="9.5" font-weight="700" fill="#A24A70">HARD {hard}</text>
    </g>
  </g>

  <!-- ================= RIGHT: MASTERY BENTO PANEL ================= -->
  <g transform="translate(340, 24)">
    <!-- Container Box -->
    <rect width="636" height="232" rx="12" fill="#14080F" stroke="#451126" stroke-width="1.2"/>

    <!-- Subtle Inner Top Glow -->
    <rect width="636" height="1" fill="#701A3D" opacity="0.6"/>

    <!-- Header Line -->
    <text x="22" y="30" font-family="{MONO}" font-size="10.5" font-weight="700" fill="#C77B9B" letter-spacing="2">ALGORITHMIC DISCIPLINE  ·  LEETCODE PROFILE</text>

    <!-- Handle & Rank Capsule Badge -->
    <g transform="translate(422, 14)">
      <rect width="192" height="24" rx="12" fill="#190B12" stroke="#701A3D" stroke-width="1.2"/>
      <!-- LeetCode hex icon -->
      <g transform="translate(14, 12) scale(0.65)">
        <path d="M0 -6 L5 -3 L5 3 L0 6 L-5 3 L-5 -3 Z" fill="none" stroke="#C77B9B" stroke-width="1.6"/>
        <path d="M-1.5 -1.5 L1.5 0 L-1.5 1.5" fill="none" stroke="#F8F0F3" stroke-width="1.4" stroke-linecap="round"/>
      </g>
      <text x="26" y="16" font-family="{MONO}" font-size="9.5" font-weight="700" fill="#F8F0F3">@Siddharth_OP</text>
      <line x1="118" y1="4" x2="118" y2="20" stroke="#701A3D" stroke-width="1"/>
      <text x="126" y="16" font-family="{MONO}" font-size="9" fill="#C77B9B">TOP 30%</text>
    </g>

    <!-- Title & Subtitle -->
    <text x="22" y="60" font-family="{SERIF}" font-size="20" font-weight="600" fill="#F8F0F3" letter-spacing="0.2">Data Structures &amp; Problem Solving</text>
    <text x="614" y="60" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="#8E6B7A">GLOBAL RANK #{ranking:,}</text>

    <!-- ================= 3 PROGRESS BARS ================= -->
    <!-- Easy Bar -->
    <g transform="translate(22, 74)">
      <text x="0" y="14" font-family="{MONO}" font-size="11" font-weight="700" fill="#E5B5C7" letter-spacing="1">EASY</text>
      <rect x="68" y="5" width="370" height="10" rx="5" fill="#1D0A14" stroke="#3D1224" stroke-width="1"/>
      <rect x="68" y="5" width="{w_easy}" height="10" rx="5" fill="url(#easy-grad)"/>
      <text x="452" y="14" font-family="{MONO}" font-size="11" font-weight="700" fill="#F8F0F3">{easy} <tspan fill="#8E6B7A" font-weight="400">/ {total_easy}</tspan></text>
      <text x="592" y="14" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="#C77B9B">({pct_easy:.1f}%)</text>
    </g>

    <!-- Medium Bar -->
    <g transform="translate(22, 102)">
      <text x="0" y="14" font-family="{MONO}" font-size="11" font-weight="700" fill="#C77B9B" letter-spacing="1">MEDIUM</text>
      <rect x="68" y="5" width="370" height="10" rx="5" fill="#1D0A14" stroke="#3D1224" stroke-width="1"/>
      <rect x="68" y="5" width="{w_med}" height="10" rx="5" fill="url(#med-grad)"/>
      <text x="452" y="14" font-family="{MONO}" font-size="11" font-weight="700" fill="#F8F0F3">{med} <tspan fill="#8E6B7A" font-weight="400">/ {total_med:,}</tspan></text>
      <text x="592" y="14" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="#C77B9B">({pct_med:.1f}%)</text>
    </g>

    <!-- Hard Bar -->
    <g transform="translate(22, 130)">
      <text x="0" y="14" font-family="{MONO}" font-size="11" font-weight="700" fill="#A24A70" letter-spacing="1">HARD</text>
      <rect x="68" y="5" width="370" height="10" rx="5" fill="#1D0A14" stroke="#3D1224" stroke-width="1"/>
      <rect x="68" y="5" width="{w_hard}" height="10" rx="5" fill="url(#hard-grad)"/>
      <text x="452" y="14" font-family="{MONO}" font-size="11" font-weight="700" fill="#F8F0F3">{hard} <tspan fill="#8E6B7A" font-weight="400">/ {total_hard}</tspan></text>
      <text x="592" y="14" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="#C77B9B">({pct_hard:.1f}%)</text>
    </g>

    <!-- ================= BOTTOM TELEMETRY STRIP ================= -->
    <g transform="translate(22, 168)">
      <!-- Metric 1: Acceptance Rate -->
      <g transform="translate(0, 0)">
        <rect width="186" height="48" rx="8" fill="#10070C" stroke="#701A3D" stroke-width="1"/>
        <text x="14" y="18" font-family="{MONO}" font-size="9" fill="#C77B9B" letter-spacing="1.2">ACCEPTANCE RATE</text>
        <text x="14" y="38" font-family="{MONO}" font-size="15" font-weight="700" fill="#F8F0F3">{acceptance}% <tspan font-size="9.5" font-weight="400" fill="#8E6B7A">(218/305)</tspan></text>
      </g>

      <!-- Metric 2: Active Streak -->
      <g transform="translate(202, 0)">
        <rect width="186" height="48" rx="8" fill="#10070C" stroke="#701A3D" stroke-width="1"/>
        <text x="14" y="18" font-family="{MONO}" font-size="9" fill="#C77B9B" letter-spacing="1.2">ACTIVE STREAK</text>
        <text x="14" y="38" font-family="{MONO}" font-size="14.5" font-weight="700" fill="#F8F0F3">🔥 {streak} DAYS <tspan font-size="9.5" font-weight="400" fill="#8E6B7A">active</tspan></text>
      </g>

      <!-- Metric 3: Total Active Days -->
      <g transform="translate(404, 0)">
        <rect width="190" height="48" rx="8" fill="#10070C" stroke="#701A3D" stroke-width="1"/>
        <text x="14" y="18" font-family="{MONO}" font-size="9" fill="#C77B9B" letter-spacing="1.2">TOTAL PRACTICE</text>
        <text x="14" y="38" font-family="{MONO}" font-size="14.5" font-weight="700" fill="#F8F0F3">{active_days} DAYS <tspan font-size="9.5" font-weight="400" fill="#8E6B7A">logged</tspan></text>
      </g>
    </g>

    <!-- Bento Inner Moving Border -->
    <rect width="634" height="230" x="1" y="1" rx="11" fill="none"
          stroke="#C77B9B" stroke-width="2.2" stroke-linecap="round" opacity="0.45"
          stroke-dasharray="70 850" stroke-dashoffset="0" filter="url(#neon-glow)">
      <animate attributeName="stroke-dashoffset" from="0" to="-920" dur="4.5s" repeatCount="indefinite"/>
    </rect>
    <rect width="634" height="230" x="1" y="1" rx="11" fill="none"
          stroke="#F8F0F3" stroke-width="1.4" stroke-linecap="round"
          stroke-dasharray="70 850" stroke-dashoffset="0">
      <animate attributeName="stroke-dashoffset" from="0" to="-920" dur="4.5s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- Outer Animated Neon Pink Moving Border -->
  {neon_border(w, h, rx=16, dur="8s", dash=150)}
</svg>"""
    write_svg(filename, svg)

# -------------------------------------------------------------
# 7. Two-Tone Segmented Pill Badges (Matching Screenshot 2)
# -------------------------------------------------------------
def make_two_tone_pill(icon_type, label, value, w_left, w_right, filename):
    w, h = w_left + w_right, 38
    key = filename.replace(".svg", "").replace("-", "_")
    
    if icon_type == "email":
        icon = '<g transform="translate(18, 19) scale(0.72)"><rect x="-10" y="-7" width="20" height="14" rx="2" fill="none" stroke="#C77B9B" stroke-width="1.6"/><path d="M-10 -5 L0 2 L10 -5" fill="none" stroke="#C77B9B" stroke-width="1.6" stroke-linejoin="round"/></g>'
    elif icon_type == "linkedin":
        icon = '<g transform="translate(18, 19) scale(0.75)"><rect x="-9" y="-9" width="18" height="18" rx="3" fill="#701A3D" opacity="0.4"/><path d="M-6 -2H-3V5H-6V-2ZM-4.5 -5.5C-3.7 -5.5 -3.2 -4.9 -3.2 -4.1C-3.2 -3.3 -3.7 -2.7 -4.5 -2.7C-5.3 -2.7 -5.8 -3.3 -5.8 -4.1C-5.8 -4.9 -5.3 -5.5 -4.5 -5.5ZM-1.5 -2H1.5V-0.9H1.6C2 -1.6 2.9 -2.2 4.1 -2.2C6.5 -2.2 7 -0.7 7 1.3V5H4V1.7C4 0.8 4 -0.3 2.8 -0.3C1.6 -0.3 1.5 0.5 1.5 1.6V5H-1.5V-2Z" fill="#C77B9B"/></g>'
    elif icon_type == "github":
        icon = '<g transform="translate(18, 19) scale(0.68)"><path d="M0 -14C-7.73 -14 -14 -7.73 -14 0C-14 6.19 -9.99 11.43 -4.42 13.28C-3.72 13.41 -3.46 12.98 -3.46 12.61C-3.46 12.28 -3.47 11.19 -3.48 9.99C-7.37 10.84 -8.19 8.97 -8.19 8.97C-8.83 7.35 -9.75 6.92 -9.75 6.92C-11.02 6.05 -9.65 6.07 -9.65 6.07C-8.25 6.17 -7.51 7.51 -7.51 7.51C-6.26 9.65 -4.24 9.03 -3.44 8.67C-3.31 7.76 -2.95 7.14 -2.55 6.79C-5.66 6.44 -8.93 5.24 -8.93 -0.12C-8.93 -1.65 -8.38 -2.9 -7.48 -3.88C-7.62 -4.23 -8.1 -5.65 -7.34 -7.56C-7.34 -7.56 -6.16 -7.94 -3.47 -6.12C-2.35 -6.43 -1.17 -6.59 0 -6.59C1.17 -6.59 2.35 -6.43 3.47 -6.12C6.16 -7.94 7.34 -7.56 7.34 -7.56C8.1 -5.65 7.62 -4.23 7.48 -3.88C8.38 -2.9 8.93 -1.65 8.93 -0.12C8.93 5.25 5.65 6.43 2.54 6.78C3.03 7.2 3.46 8.04 3.46 9.32C3.46 11.16 3.44 12.64 3.44 12.61C3.44 12.98 3.7 13.42 4.42 13.28C9.99 11.43 14 6.19 14 0C14 -7.73 7.73 -14 0 -14Z" fill="#C77B9B"/></g>'
    else: # leetcode
        icon = '<g transform="translate(18, 19) scale(0.72)"><path d="M0 -7 L6 -3.5 L6 3.5 L0 7 L-6 3.5 L-6 -3.5 Z" fill="none" stroke="#C77B9B" stroke-width="1.5"/><path d="M-2 -2 L2 0 L-2 2" fill="none" stroke="#F8F0F3" stroke-width="1.3" stroke-linecap="round"/></g>'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}: {esc(value)}">
  <defs>
    <linearGradient id="pill-left-{key}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#14080F"/>
      <stop offset="100%" stop-color="#190B12"/>
    </linearGradient>
    <linearGradient id="pill-right-{key}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#701A3D"/>
      <stop offset="100%" stop-color="#451126"/>
    </linearGradient>
    <clipPath id="pill-clip-{key}">
      <rect width="{w}" height="{h}" rx="10"/>
    </clipPath>
  </defs>

  <g clip-path="url(#pill-clip-{key})">
    <!-- Left dark capsule -->
    <rect x="0" y="0" width="{w_left}" height="{h}" fill="url(#pill-left-{key})"/>
    <!-- Right burgundy capsule -->
    <rect x="{w_left}" y="0" width="{w_right}" height="{h}" fill="url(#pill-right-{key})"/>
    <!-- Center divider line -->
    <line x1="{w_left}" y1="0" x2="{w_left}" y2="{h}" stroke="#701A3D" stroke-width="1.2"/>
  </g>

  <!-- Outer Border -->
  <rect width="{w}" height="{h}" rx="10" fill="none" stroke="#701A3D" stroke-width="1.2"/>

  <!-- Left Icon & Label -->
  {icon}
  <text x="34" y="24" font-family="{MONO}" font-size="10" font-weight="700" fill="#F8F0F3" letter-spacing="1">{esc(label)}</text>

  <!-- Right Value Text -->
  <text x="{w_left + w_right/2}" y="24" text-anchor="middle" font-family="{MONO}" font-size="10.5" font-weight="600" fill="#F8F0F3">{esc(value)}</text>
</svg>"""
    write_svg(filename, svg)

# -------------------------------------------------------------
# 8. Grand Luxury Footer Hero (Matching Screenshot 2)
# -------------------------------------------------------------
def make_luxury_footer(filename="siddharth-footer.svg"):
    w, h = 1000, 280
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Siddharth - Building systems that can explain themselves">
  <defs>
    <linearGradient id="ft-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10070C"/>
      <stop offset="50%" stop-color="#14080F"/>
      <stop offset="100%" stop-color="#10070C"/>
    </linearGradient>
    <radialGradient id="ft-spotlight" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#701A3D" stop-opacity="0.6"/>
      <stop offset="45%" stop-color="#451126" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#10070C" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="ft-line" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#701A3D" stop-opacity="0"/>
      <stop offset="50%" stop-color="#C77B9B" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#701A3D" stop-opacity="0"/>
    </linearGradient>
    <filter id="text-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <!-- Frame Background -->
  <rect width="{w}" height="{h}" rx="16" fill="url(#ft-bg)"/>
  <rect width="{w}" height="{h}" rx="16" fill="url(#ft-spotlight)"/>

  <!-- Subtle Starlight Constellation Particles -->
  <circle cx="160" cy="80" r="1.5" fill="#E5B5C7" opacity="0.4"/>
  <circle cx="280" cy="190" r="1.2" fill="#C77B9B" opacity="0.5"/>
  <circle cx="380" cy="70" r="1.8" fill="#F8F0F3" opacity="0.6">
    <animate attributeName="opacity" values="0.2;0.8;0.2" dur="4s" repeatCount="indefinite"/>
  </circle>
  <circle cx="620" cy="70" r="1.8" fill="#F8F0F3" opacity="0.6">
    <animate attributeName="opacity" values="0.8;0.2;0.8" dur="4.5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="740" cy="90" r="1.5" fill="#E5B5C7" opacity="0.4"/>
  <circle cx="850" cy="180" r="1.2" fill="#C77B9B" opacity="0.5"/>
  <circle cx="500" cy="40" r="2.2" fill="#F8F0F3" opacity="0.75">
    <animate attributeName="opacity" values="0.3;0.9;0.3" dur="3s" repeatCount="indefinite"/>
  </circle>

  <!-- Giant Glowing Brand Name (Screenshot 2 Match) -->
  <text x="500" y="128" text-anchor="middle" font-family="{SERIF}" font-size="76" font-weight="700" fill="#C77B9B" opacity="0.55" filter="url(#text-glow)">Siddharth</text>
  <text x="500" y="128" text-anchor="middle" font-family="{SERIF}" font-size="76" font-weight="700" fill="#F8F0F3" letter-spacing="1">Siddharth</text>

  <!-- Italic Subtitle -->
  <text x="500" y="172" text-anchor="middle" font-family="{SERIF}" font-size="18.5" font-style="italic" fill="#E5B5C7" opacity="0.95">Building systems that can explain themselves.</text>

  <!-- Precision Monospace Sub-Brand -->
  <text x="500" y="214" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="#C77B9B" letter-spacing="4">ENGINEERING INTELLIGENCE  ·  DESIGNING EXPERIENCES</text>

  <!-- Subtle Accent Underline -->
  <line x1="320" y1="236" x2="680" y2="236" stroke="url(#ft-line)" stroke-width="1.2"/>

  <!-- Animated Neon Pink Moving Border -->
  {neon_border(w, h, rx=16, dur="8s", dash=160)}
</svg>"""
    write_svg(filename, svg)

# -------------------------------------------------------------
# 9. Action Button Badges
# -------------------------------------------------------------
def make_button(text, icon_type, w, filename):
    h = 38
    key = filename.replace(".svg", "").replace("-", "_")
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
    # 1. Section headers with rich right-side captions
    make_section_header("01", "Introduction", "Curiosity, code, and practical intelligence.", "section-01-introduction.svg", right_text="B.TECH CSE · 2024–2028")
    make_section_header("02", "Featured Work", "Selected systems & architecture platforms.", "section-02-projects.svg", right_text="PRODUCTION & RESEARCH →")
    make_section_header("03", "Toolset", "The tools I reach for.", "section-03-skills.svg", right_text="6-BOX BENTO SUITE")
    make_section_header("03", "Toolset", "The tools I reach for.", "section-04-skills.svg", right_text="6-BOX BENTO SUITE")  # compatibility alias
    make_section_header("04", "Credentials", "Verified certifications & honors.", "section-04-certifications.svg", right_text="OFFICIAL RECORDS")
    make_section_header("04", "Credentials", "Verified certifications & honors.", "section-03-certifications.svg", right_text="OFFICIAL RECORDS")  # compatibility alias
    make_section_header("05", "Commit Log & Telemetry", "A year of building, one square at a time.", "section-05-activity.svg", right_text="LIVE TELEMETRY · 365 DAYS")
    make_section_header("06", "Connect", "Let's build something worth explaining.", "section-06-links.svg", right_text="OPEN INBOX →")

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

    # 4. Unified Commit Log Card (Authentic Square-Tile Burgundy Snake)
    make_unified_commit_log()

    # 5. GitHub At A Glance Card (Matching Screenshot 1)
    make_github_glance(stars=6, commits=57, prs=2, issues=0, repos=8, filename="github-glance.svg")

    # 5.5 LeetCode Radial Bento Card (Real Live Stats from @Siddharth_OP)
    make_leetcode_radial(total=142, easy=95, med=44, hard=3, total_easy=972, total_med=2131, total_hard=984, total_q=4087, acceptance=71.5, streak=11, active_days=78, ranking=1247511, filename="leetcode.svg")

    # 6. Certifications Shelf
    make_certifications()

    # 7. Action Button Badges (Project repo links)
    make_button("VIEW REPOSITORY →", "arrow", 185, "link-repo-resq.svg")

    # 8. Two-Tone Contact Pills (Matching Screenshot 2)
    make_two_tone_pill("email", "EMAIL", "siddharthmeka168@gmail.com", 92, 248, "pill-email.svg")
    make_two_tone_pill("linkedin", "LINKEDIN", "siddharth-meka", 104, 146, "pill-linkedin.svg")
    make_two_tone_pill("github", "GITHUB", "siddharth-meka-16", 94, 166, "pill-github.svg")
    make_two_tone_pill("leetcode", "LEETCODE", "Siddharth_OP", 106, 142, "pill-leetcode.svg")

    # 9. Grand Luxury Footer Hero (Matching Screenshot 2)
    make_luxury_footer("siddharth-footer.svg")

if __name__ == "__main__":
    main()
