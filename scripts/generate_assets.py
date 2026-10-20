#!/usr/bin/env python3
"""
Generate all supplementary profile SVG assets in the burgundy theme (v2):
#10070C, #190B12, #451126, #701A3D, #C77B9B, #E5B5C7, #F8F0F3

Features in v2:
1. Animated Interactive Terminal (assets/terminal.svg)
2. Animated Project Micro-Demos (radar sweep, code scanner, gauge meter)
3. Custom Burgundy Contribution Snake (assets/github-contribution-grid-snake.svg)
"""
import os, math, random, xml.sax.saxutils as sax

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, 'DejaVu Sans Mono', monospace"
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
# 1. Section Header Generator
# -------------------------------------------------------------
def make_section_header(num_str, title, subtitle, filename):
    w, h = 1000, 68
    title_w = len(title) * 14.5
    sub_x = int(82 + title_w + 12)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(num_str)} {esc(title)}">
  <defs>
    <linearGradient id="sh-bg-{num_str}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#10070C"/>
      <stop offset="40%" stop-color="#190B12"/>
      <stop offset="100%" stop-color="#10070C"/>
    </linearGradient>
    <linearGradient id="sh-rule-{num_str}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#C77B9B" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#701A3D" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#10070C" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="{w}" height="{h}" rx="12" fill="url(#sh-bg-{num_str})" stroke="#701A3D" stroke-opacity="0.6" stroke-width="1"/>

  <!-- Index badge -->
  <rect x="20" y="18" width="46" height="32" rx="16" fill="#10070C" stroke="#701A3D" stroke-width="1.2"/>
  <text x="43" y="39" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="#C77B9B" letter-spacing="1">{esc(num_str)}</text>

  <!-- Title -->
  <text x="82" y="42" font-family="{SERIF}" font-size="24" font-weight="600" fill="#F8F0F3" letter-spacing="0.5">{esc(title)}</text>

  <!-- Subtitle -->
  <text x="{sub_x}" y="42" font-family="{MONO}" font-size="12" fill="#C77B9B" letter-spacing="2" opacity="0.85">  ·  {esc(subtitle.upper())}</text>

  <!-- Glowing underline rule -->
  <line x1="20" y1="{h-1}" x2="{w-20}" y2="{h-1}" stroke="url(#sh-rule-{num_str})" stroke-width="1.5"/>

  <!-- Corner accent marks -->
  <g stroke="#C77B9B" stroke-opacity="0.35" stroke-width="1" fill="none">
    <path d="M {w-26} 22 L {w-18} 22 L {w-18} 30"/>
    <path d="M {w-18} 38 L {w-18} 46 L {w-26} 46"/>
  </g>
</svg>"""
    write_svg(filename, svg)

# -------------------------------------------------------------
# 2. Animated Interactive Terminal Generator (v2)
# -------------------------------------------------------------
def make_terminal():
    w, h = 1000, 310
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Interactive Terminal — Siddharth Meka">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="term-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#14080F"/>
      <stop offset="60%" stop-color="#10070C"/>
      <stop offset="100%" stop-color="#190B12"/>
    </linearGradient>

    <!-- Header Gradient -->
    <linearGradient id="term-hdr" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#190B12"/>
      <stop offset="100%" stop-color="#14080F"/>
    </linearGradient>

    <!-- Master loop timer: 14s cycle -->
    <rect id="t_loop" width="0" height="0">
      <animate attributeName="width" from="0" to="100" dur="14s" repeatCount="indefinite"/>
    </rect>

    <!-- Clip path for Command 1: 'whoami' (width 0 to 100) -->
    <clipPath id="cp-cmd1">
      <rect x="230" y="55" width="0" height="30">
        <animate attributeName="width" from="0" to="120" dur="0.8s" begin="0.3s; t_loop.repeat(1)" fill="freeze"/>
      </rect>
    </clipPath>

    <!-- Clip path for Command 2: 'cat current_stack.json' (width 0 to 280) -->
    <clipPath id="cp-cmd2">
      <rect x="230" y="135" width="0" height="30">
        <animate attributeName="width" from="0" to="260" dur="1.1s" begin="2.6s; t_loop.repeat(1)+2.3s" fill="freeze"/>
      </rect>
    </clipPath>

    <!-- Clip path for Command 3: 'python -m status' (width 0 to 220) -->
    <clipPath id="cp-cmd3">
      <rect x="230" y="215" width="0" height="30">
        <animate attributeName="width" from="0" to="220" dur="0.9s" begin="5.2s; t_loop.repeat(1)+4.9s" fill="freeze"/>
      </rect>
    </clipPath>
  </defs>

  <!-- Terminal Window Outer Frame -->
  <rect width="{w}" height="{h}" rx="14" fill="url(#term-bg)" stroke="#701A3D" stroke-width="1.2"/>

  <!-- Title bar -->
  <rect width="{w}" height="36" rx="14" fill="url(#term-hdr)"/>
  <rect y="22" width="{w}" height="14" fill="url(#term-hdr)"/>
  <line x1="0" y1="36" x2="{w}" y2="36" stroke="#451126" stroke-width="1"/>

  <!-- Control dots -->
  <circle cx="26" cy="18" r="5.5" fill="#701A3D"/>
  <circle cx="44" cy="18" r="5.5" fill="#A24A70"/>
  <circle cx="62" cy="18" r="5.5" fill="#C77B9B"/>

  <!-- Title bar info -->
  <text x="{w/2}" y="22" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="#C77B9B" letter-spacing="1" opacity="0.9">siddharth@workstation: ~ (zsh)</text>
  <text x="{w-28}" y="22" text-anchor="end" font-family="{MONO}" font-size="10" fill="#E5B5C7" letter-spacing="1" opacity="0.5">● zsh · 80x24 · UTF-8</text>

  <!-- ================= LINE 1 ================= -->
  <!-- Prompt 1 -->
  <text x="32" y="75" font-family="{MONO}" font-size="13" font-weight="700" fill="#C77B9B" letter-spacing="0.5">siddharth@pvpsit:~$</text>
  
  <!-- Command 1 typed -->
  <g clip-path="url(#cp-cmd1)">
    <text x="230" y="75" font-family="{MONO}" font-size="13" font-weight="500" fill="#F8F0F3">whoami</text>
  </g>

  <!-- Output 1 (fades in) -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.25s" begin="1.3s; t_loop.repeat(1)+1.0s" fill="freeze"/>
    <text x="48" y="105" font-family="{MONO}" font-size="12.5" fill="#E5B5C7">
      <tspan fill="#F8F0F3" font-weight="600">Siddharth Meka</tspan> — B.Tech Computer Science (2024–2028) @ PVPSIT, Andhra Pradesh
    </text>
  </g>

  <!-- ================= LINE 2 ================= -->
  <!-- Prompt 2 (appears at 2.4s) -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="2.4s; t_loop.repeat(1)+2.1s" fill="freeze"/>
    <text x="32" y="155" font-family="{MONO}" font-size="13" font-weight="700" fill="#C77B9B" letter-spacing="0.5">siddharth@pvpsit:~$</text>
  </g>

  <!-- Command 2 typed -->
  <g clip-path="url(#cp-cmd2)">
    <text x="230" y="155" font-family="{MONO}" font-size="13" font-weight="500" fill="#F8F0F3">cat current_stack.json</text>
  </g>

  <!-- Output 2 (fades in) -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.25s" begin="3.9s; t_loop.repeat(1)+3.6s" fill="freeze"/>
    <text x="48" y="185" font-family="{MONO}" font-size="12" fill="#E5B5C7">
      <tspan fill="#C77B9B">&#123;</tspan> <tspan fill="#F8F0F3">"focus"</tspan>: [<tspan fill="#E5B5C7">"AI/ML"</tspan>, <tspan fill="#E5B5C7">"Full-Stack"</tspan>], <tspan fill="#F8F0F3">"core"</tspan>: [<tspan fill="#E5B5C7">"React"</tspan>, <tspan fill="#E5B5C7">"FastAPI"</tspan>, <tspan fill="#E5B5C7">"Gemini API"</tspan>, <tspan fill="#E5B5C7">"Java"</tspan>, <tspan fill="#E5B5C7">"Python"</tspan>] <tspan fill="#C77B9B">&#125;</tspan>
    </text>
  </g>

  <!-- ================= LINE 3 ================= -->
  <!-- Prompt 3 (appears at 5.0s) -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="5.0s; t_loop.repeat(1)+4.7s" fill="freeze"/>
    <text x="32" y="235" font-family="{MONO}" font-size="13" font-weight="700" fill="#C77B9B" letter-spacing="0.5">siddharth@pvpsit:~$</text>
  </g>

  <!-- Command 3 typed -->
  <g clip-path="url(#cp-cmd3)">
    <text x="230" y="235" font-family="{MONO}" font-size="13" font-weight="500" fill="#F8F0F3">python -m status</text>
  </g>

  <!-- Output 3 (fades in with green pulse) -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.25s" begin="6.3s; t_loop.repeat(1)+6.0s" fill="freeze"/>
    <circle cx="56" cy="261" r="4" fill="#C77B9B">
      <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="68" y="265" font-family="{MONO}" font-size="12" fill="#F8F0F3" font-weight="600">
      [READY] <tspan fill="#E5B5C7">Actively shipping ResQ &amp; exploring SDE / AI internships for 2025–2026</tspan>
    </text>
  </g>

  <!-- Blinking Terminal Cursor -->
  <rect x="420" y="222" width="8" height="15" rx="1" fill="#C77B9B" opacity="0">
    <animate attributeName="opacity" values="0;0;1;1;0" dur="0.9s" begin="6.3s; t_loop.repeat(1)+6.0s" repeatCount="indefinite"/>
  </rect>

  <!-- Bottom Accent Status Line -->
  <line x1="20" y1="{h-1}" x2="{w-20}" y2="{h-1}" stroke="#701A3D" stroke-opacity="0.5" stroke-width="1"/>
</svg>"""
    write_svg("terminal.svg", svg)

# -------------------------------------------------------------
# 3. Project Card Banner Generator with Micro-Demos (v2)
# -------------------------------------------------------------
def make_project_card(title, subtitle, tags, badge_text, icon_type, filename):
    w, h = 1000, 118
    key = filename.replace(".svg", "").replace("-", "_")

    # Tag chips computation
    tag_elements = []
    tx = 30
    for tag in tags:
        tw = len(tag) * 8 + 22
        tag_elements.append(f"""
    <g transform="translate({tx}, 76)">
      <rect width="{tw}" height="24" rx="12" fill="#10070C" stroke="#451126" stroke-width="1"/>
      <text x="{tw/2}" y="16" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#E5B5C7">{esc(tag)}</text>
    </g>""")
        tx += tw + 10

    # Project specific animated micro-demo components
    if icon_type == "resq":
        # Radar Sweep & Expanding Emergency Beacon
        demo_svg = """
        <!-- Radar Beacon Waves -->
        <circle cx="0" cy="0" r="14" fill="none" stroke="#C77B9B" stroke-width="1.4">
          <animate attributeName="r" values="14;34;14" dur="3s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.85;0;0.85" dur="3s" repeatCount="indefinite"/>
        </circle>
        <circle cx="0" cy="0" r="14" fill="none" stroke="#E5B5C7" stroke-width="1">
          <animate attributeName="r" values="14;34;14" dur="3s" begin="1.5s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.7;0;0.7" dur="3s" begin="1.5s" repeatCount="indefinite"/>
        </circle>
        <!-- Rotating Radar Sweep Line -->
        <line x1="0" y1="0" x2="22" y2="0" stroke="#E5B5C7" stroke-width="1.6" stroke-linecap="round">
          <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="4s" repeatCount="indefinite"/>
        </line>
        <!-- Center shield icon -->
        <path d="M 0 -12 L 12 -4 L 12 8 L 0 16 L -12 8 L -12 -4 Z" fill="#190B12" stroke="#C77B9B" stroke-width="1.5"/>
        <path d="M -4 2 L 4 2 M 0 -2 L 0 6" stroke="#E5B5C7" stroke-width="2" stroke-linecap="round"/>
        """
        right_metric = """
        <g transform="translate(740, 24)">
          <rect width="230" height="28" rx="14" fill="#10070C" stroke="#701A3D" stroke-width="1"/>
          <circle cx="16" cy="14" r="4" fill="#C77B9B">
            <animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/>
          </circle>
          <text x="32" y="18" font-family="'SFMono-Regular', Consolas, monospace" font-size="10.5" font-weight="700" fill="#E5B5C7" letter-spacing="1">LIVE COORDINATION</text>
          <text x="180" y="18" font-family="'SFMono-Regular', Consolas, monospace" font-size="9.5" fill="#C77B9B" opacity="0.85">GIS MAP</text>
        </g>
        """

    elif icon_type == "code":
        # Scanning laser beam & syntax highlight analyzer
        demo_svg = """
        <!-- Scanning Laser Beam -->
        <rect x="-24" y="-18" width="48" height="2" rx="1" fill="#C77B9B" opacity="0.9">
          <animate attributeName="y" values="-20;20;-20" dur="2.4s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.9;0.3;0.9" dur="2.4s" repeatCount="indefinite"/>
        </rect>
        <!-- Code Brackets with breathing scale -->
        <g>
          <animateTransform attributeName="transform" type="scale" values="1;1.08;1" dur="2.5s" repeatCount="indefinite"/>
          <path d="M -7 -7 L -13 0 L -7 7 M 7 -7 L 13 0 L 7 7" fill="none" stroke="#C77B9B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <line x1="2" y1="-9" x2="-2" y2="9" stroke="#E5B5C7" stroke-width="1.6" stroke-linecap="round"/>
        </g>
        """
        right_metric = """
        <g transform="translate(740, 24)">
          <rect width="230" height="28" rx="14" fill="#10070C" stroke="#701A3D" stroke-width="1"/>
          <!-- animated scan dot -->
          <circle cx="16" cy="14" r="4" fill="#C77B9B">
            <animate attributeName="r" values="3.5;5;3.5" dur="1.8s" repeatCount="indefinite"/>
          </circle>
          <text x="32" y="18" font-family="'SFMono-Regular', Consolas, monospace" font-size="10.5" font-weight="700" fill="#E5B5C7" letter-spacing="1">AST &amp; COMPLEXITY</text>
          <text x="175" y="18" font-family="'SFMono-Regular', Consolas, monospace" font-size="9.5" fill="#C77B9B" opacity="0.85">GEMINI</text>
        </g>
        """

    else: # fraud shield
        # Rotating Security Perimeter & Swinging Confidence Meter Needle
        demo_svg = """
        <!-- Rotating dashed perimeter -->
        <circle cx="0" cy="0" r="28" fill="none" stroke="#C77B9B" stroke-width="1.2" stroke-dasharray="7 5">
          <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/>
        </circle>
        <!-- Center security shield -->
        <path d="M 0 -13 C 7 -13 12 -9 12 -3 C 12 7 5 13 0 16 C -5 13 -12 7 -12 -3 C -12 -9 -7 -13 0 -13 Z" fill="#190B12" stroke="#C77B9B" stroke-width="1.6"/>
        <circle cx="0" cy="1" r="3" fill="#E5B5C7">
          <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
        </circle>
        """
        right_metric = """
        <g transform="translate(740, 24)">
          <rect width="230" height="28" rx="14" fill="#10070C" stroke="#701A3D" stroke-width="1"/>
          <!-- Mini gauge arc -->
          <path d="M 12 18 A 6 6 0 0 1 24 18" fill="none" stroke="#701A3D" stroke-width="2"/>
          <line x1="18" y1="18" x2="18" y2="12" stroke="#E5B5C7" stroke-width="1.5" stroke-linecap="round">
            <animateTransform attributeName="transform" type="rotate" values="-40 18 18; 40 18 18; 32 18 18; -40 18 18" dur="4s" repeatCount="indefinite"/>
          </line>
          <text x="32" y="18" font-family="'SFMono-Regular', Consolas, monospace" font-size="10.5" font-weight="700" fill="#E5B5C7" letter-spacing="1">99.4% F1 SCORE</text>
          <text x="160" y="18" font-family="'SFMono-Regular', Consolas, monospace" font-size="9.5" fill="#C77B9B" opacity="0.85">0.17% FRAUD</text>
        </g>
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)} Project Card">
  <defs>
    <linearGradient id="p-bg-{key}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#190B12"/>
      <stop offset="60%" stop-color="#14080F"/>
      <stop offset="100%" stop-color="#10070C"/>
    </linearGradient>
    <radialGradient id="p-glow-{key}" cx="0.05" cy="0.3" r="0.4">
      <stop offset="0%" stop-color="#701A3D" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#701A3D" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="{w}" height="{h}" rx="14" fill="url(#p-bg-{key})" stroke="#701A3D" stroke-opacity="0.8" stroke-width="1.2"/>
  <rect width="{w}" height="{h}" rx="14" fill="url(#p-glow-{key})"/>

  <!-- Left Accent Bar -->
  <rect x="0" y="24" width="4" height="70" rx="2" fill="#C77B9B"/>

  <!-- Project Icon container with animated micro-demo -->
  <g transform="translate(54, 42)">
    <circle cx="0" cy="0" r="24" fill="#10070C" stroke="#701A3D" stroke-width="1.2"/>
    {demo_svg}
  </g>

  <!-- Title & Subtitle -->
  <text x="96" y="38" font-family="{SERIF}" font-size="26" font-weight="600" fill="#F8F0F3" letter-spacing="0.5">{esc(title)}</text>
  <text x="96" y="58" font-family="{SANS}" font-size="13" fill="#E5B5C7" opacity="0.9">{esc(subtitle)}</text>

  <!-- Right Metric / Live Status Pill -->
  {right_metric}

  <!-- Tags -->
  <g>
    {"".join(tag_elements)}
  </g>
</svg>"""
    write_svg(filename, svg)

# -------------------------------------------------------------
# 4. Custom Burgundy Contribution Snake Initial Generator
# -------------------------------------------------------------
def make_snake():
    w, h = 1000, 200
    # Generate 53 columns x 7 rows of contribution tiles in burgundy gradient
    cols = 53
    rows = 7
    cell = 12
    gap = 4
    x0 = 40
    y0 = 46

    LEVELS = ["#190B12", "#451126", "#701A3D", "#A24A70", "#C77B9B"]
    
    rects = []
    # Seeded pattern for realistic activity distribution
    random.seed(168)
    for c in range(cols):
        for r in range(rows):
            # simulate recent activity being slightly denser
            prob = random.random()
            if prob < 0.25:
                lvl = 0
            elif prob < 0.55:
                lvl = 1
            elif prob < 0.78:
                lvl = 2
            elif prob < 0.92:
                lvl = 3
            else:
                lvl = 4
            
            x = x0 + c * (cell + gap)
            y = y0 + r * (cell + gap)
            rects.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{LEVELS[lvl]}"/>')

    # Animated snake path over tiles
    # Snake body elements
    snake_body = """
    <!-- Animated Burgundy Snake -->
    <g>
      <!-- Snake Trail -->
      <path d="M 40 52 L 200 52 L 200 100 L 450 100 L 450 68 L 680 68 L 680 132 L 880 132" fill="none" stroke="#C77B9B" stroke-width="3" stroke-linecap="round" stroke-dasharray="16 120" stroke-dashoffset="0">
        <animate attributeName="stroke-dashoffset" from="0" to="-700" dur="8s" repeatCount="indefinite"/>
      </path>
      <!-- Snake Head -->
      <circle cx="200" cy="52" r="5" fill="#F8F0F3" filter="drop-shadow(0 0 4px #C77B9B)">
        <animateMotion path="M -160 0 L 0 0 L 0 48 L 250 48 L 250 16 L 480 16 L 480 80 L 680 80" dur="8s" repeatCount="indefinite"/>
      </circle>
    </g>
    """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Burgundy Contribution Snake">
  <defs>
    <linearGradient id="snk-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10070C"/>
      <stop offset="60%" stop-color="#14080F"/>
      <stop offset="100%" stop-color="#190B12"/>
    </linearGradient>
  </defs>

  <!-- Container Frame -->
  <rect width="{w}" height="{h}" rx="14" fill="url(#snk-bg)" stroke="#701A3D" stroke-width="1.2"/>

  <!-- Top label -->
  <rect x="36" y="16" width="30" height="2" fill="#C77B9B"/>
  <text x="74" y="21" font-family="{MONO}" font-size="11" letter-spacing="2" fill="#C77B9B">BURGUNDY CONTRIBUTION MATRIX · LIVE TRACKER</text>
  <text x="{w-40}" y="21" text-anchor="end" font-family="{MONO}" font-size="10" fill="#E5B5C7" opacity="0.6">YEAR 2025–2026</text>

  <!-- Contribution Grid Tiles -->
  <g>
    {"".join(rects)}
  </g>

  <!-- Animated Snake -->
  {snake_body}

  <!-- Legend at bottom -->
  <g transform="translate({w-230}, {h-24})">
    <text x="0" y="10" font-family="{MONO}" font-size="10" fill="#C77B9B">LESS</text>
    <rect x="38" y="0" width="10" height="10" rx="2" fill="#190B12"/>
    <rect x="52" y="0" width="10" height="10" rx="2" fill="#451126"/>
    <rect x="66" y="0" width="10" height="10" rx="2" fill="#701A3D"/>
    <rect x="80" y="0" width="10" height="10" rx="2" fill="#A24A70"/>
    <rect x="94" y="0" width="10" height="10" rx="2" fill="#C77B9B"/>
    <text x="114" y="10" font-family="{MONO}" font-size="10" fill="#C77B9B">MORE</text>
  </g>
</svg>"""
    write_svg("github-contribution-grid-snake.svg", svg)

# -------------------------------------------------------------
# 5. Buttons, Certifications, and Skills
# -------------------------------------------------------------
def make_button(text, icon_type, w, filename):
    h = 40
    key = filename.replace(".svg", "").replace("-", "_")
    if icon_type == "github":
        icon = """
        <g transform="translate(24, 20) scale(0.85)">
          <path d="M0 -14C-7.73 -14 -14 -7.73 -14 0C-14 6.19 -9.99 11.43 -4.42 13.28C-3.72 13.41 -3.46 12.98 -3.46 12.61C-3.46 12.28 -3.47 11.19 -3.48 9.99C-7.37 10.84 -8.19 8.97 -8.19 8.97C-8.83 7.35 -9.75 6.92 -9.75 6.92C-11.02 6.05 -9.65 6.07 -9.65 6.07C-8.25 6.17 -7.51 7.51 -7.51 7.51C-6.26 9.65 -4.24 9.03 -3.44 8.67C-3.31 7.76 -2.95 7.14 -2.55 6.79C-5.66 6.44 -8.93 5.24 -8.93 -0.12C-8.93 -1.65 -8.38 -2.9 -7.48 -3.88C-7.62 -4.23 -8.1 -5.65 -7.34 -7.56C-7.34 -7.56 -6.16 -7.94 -3.47 -6.12C-2.35 -6.43 -1.17 -6.59 0 -6.59C1.17 -6.59 2.35 -6.43 3.47 -6.12C6.16 -7.94 7.34 -7.56 7.34 -7.56C8.1 -5.65 7.62 -4.23 7.48 -3.88C8.38 -2.9 8.93 -1.65 8.93 -0.12C8.93 5.25 5.65 6.43 2.54 6.78C3.03 7.2 3.46 8.04 3.46 9.32C3.46 11.16 3.44 12.64 3.44 12.61C3.44 12.98 3.7 13.42 4.42 13.28C9.99 11.43 14 6.19 14 0C14 -7.73 7.73 -14 0 -14Z" fill="#C77B9B"/>
        </g>
        """
        text_x = 42
    elif icon_type == "linkedin":
        icon = """
        <g transform="translate(24, 20) scale(0.85)">
          <rect x="-12" y="-12" width="24" height="24" rx="4" fill="#701A3D" opacity="0.3"/>
          <path d="M-8 -3H-5V6H-8V-3ZM-6.5 -7.5C-5.5 -7.5 -4.8 -6.7 -4.8 -5.7C-4.8 -4.7 -5.5 -4 -6.5 -4C-7.4 -4 -8.2 -4.7 -8.2 -5.7C-8.2 -6.7 -7.4 -7.5 -6.5 -7.5ZM-3 -3H0V-1.8H0.1C0.5 -2.6 1.6 -3.3 2.9 -3.3C5.7 -3.3 6.3 -1.5 6.3 0.9V6H3.3V1.6C3.3 0.5 3.3 -0.9 1.9 -0.9C0.5 -0.9 0.3 0.2 0.3 1.5V6H-3V-3Z" fill="#C77B9B"/>
        </g>
        """
        text_x = 42
    else: # arrow button
        icon = """
        <g transform="translate(22, 20)">
          <path d="M-4 0 L4 0 M1 -4 L5 0 L1 4" stroke="#C77B9B" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        </g>
        """
        text_x = 38

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(text)}">
  <defs>
    <linearGradient id="btn-bg-{key}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#190B12"/>
      <stop offset="100%" stop-color="#10070C"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" rx="20" fill="url(#btn-bg-{key})" stroke="#701A3D" stroke-width="1.2"/>
  {icon}
  <text x="{text_x}" y="25" font-family="{MONO}" font-size="12" font-weight="600" fill="#F8F0F3" letter-spacing="0.5">{esc(text)}</text>
</svg>"""
    write_svg(filename, svg)

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
      <rect width="460" height="85" rx="12" fill="#14080F" stroke="#701A3D" stroke-opacity="0.7" stroke-width="1"/>
      <g transform="translate(24, 42)">
        <circle cx="0" cy="0" r="14" fill="#10070C" stroke="#C77B9B" stroke-width="1.2"/>
        <path d="M -5 0 L -1 4 L 6 -3" fill="none" stroke="#E5B5C7" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
      <text x="50" y="32" font-family="{MONO}" font-size="11" font-weight="700" fill="#C77B9B" letter-spacing="1">{esc(issuer.upper())}</text>
      <text x="50" y="52" font-family="{SERIF}" font-size="15" font-weight="600" fill="#F8F0F3">{esc(title)}</text>
      <text x="50" y="70" font-family="{MONO}" font-size="10" fill="#E5B5C7" opacity="0.75">{esc(date_str)}  ·  {badge}</text>
      <circle cx="438" cy="42" r="3" fill="#701A3D"/>
    </g>""")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Certifications">
  <defs>
    <linearGradient id="cert-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10070C"/>
      <stop offset="50%" stop-color="#190B12"/>
      <stop offset="100%" stop-color="#10070C"/>
    </linearGradient>
    <radialGradient id="cert-glow" cx="0.8" cy="0.2" r="0.5">
      <stop offset="0%" stop-color="#701A3D" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#701A3D" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="{w}" height="{h}" rx="16" fill="url(#cert-bg)" stroke="#701A3D" stroke-opacity="0.85" stroke-width="1.2"/>
  <rect width="{w}" height="{h}" rx="16" fill="url(#cert-glow)"/>

  {"".join(cards_svg)}
</svg>"""
    write_svg("certifications.svg", svg)

def make_skills():
    w, h = 1000, 310
    categories = [
        ("PROGRAMMING LANGUAGES", ["Java", "Python", "C", "TypeScript", "JavaScript"]),
        ("CS FUNDAMENTALS", ["Data Structures &amp; Algorithms", "OOP", "DBMS", "Operating Systems", "Networks"]),
        ("FRONTEND &amp; BACKEND", ["React", "Next.js", "HTML5 &amp; CSS3", "FastAPI", "Node.js", "Express.js", "REST APIs"]),
        ("AI, CLOUD &amp; TOOLS", ["Gemini API", "scikit-learn", "XGBoost", "Supabase", "MySQL", "Vercel", "Git &amp; GitHub"]),
    ]

    col_w = 222
    col_gap = 20
    x_start = 30
    cols_svg = []

    for i, (cat_title, skills) in enumerate(categories):
        cx = x_start + i * (col_w + col_gap)
        skill_pills = []
        sy = 54
        for skill in skills:
            skill_pills.append(f"""
      <rect x="14" y="{sy}" width="{col_w - 28}" height="24" rx="6" fill="#10070C" stroke="#451126" stroke-width="0.9"/>
      <circle cx="26" cy="{sy+12}" r="2.5" fill="#C77B9B"/>
      <text x="36" y="{sy+16}" font-family="{SANS}" font-size="11" font-weight="500" fill="#E5B5C7">{skill}</text>""")
            sy += 29

        cols_svg.append(f"""
    <g transform="translate({cx}, 20)">
      <rect width="{col_w}" height="268" rx="12" fill="#14080F" stroke="#701A3D" stroke-opacity="0.6" stroke-width="1"/>
      <rect x="0" y="0" width="{col_w}" height="38" rx="12" fill="#190B12"/>
      <rect x="0" y="26" width="{col_w}" height="12" fill="#190B12"/>
      <line x1="0" y1="38" x2="{col_w}" y2="38" stroke="#701A3D" stroke-width="1"/>
      <text x="14" y="24" font-family="{MONO}" font-size="10.5" font-weight="700" fill="#C77B9B" letter-spacing="1">{cat_title}</text>
      {"".join(skill_pills)}
    </g>""")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Technical Skills">
  <defs>
    <linearGradient id="sk-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10070C"/>
      <stop offset="50%" stop-color="#190B12"/>
      <stop offset="100%" stop-color="#10070C"/>
    </linearGradient>
    <radialGradient id="sk-glow" cx="0.5" cy="0" r="0.6">
      <stop offset="0%" stop-color="#701A3D" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#701A3D" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="{w}" height="{h}" rx="16" fill="url(#sk-bg)" stroke="#701A3D" stroke-opacity="0.85" stroke-width="1.2"/>
  <rect width="{w}" height="{h}" rx="16" fill="url(#sk-glow)"/>

  {"".join(cols_svg)}
</svg>"""
    write_svg("skills.svg", svg)

def main():
    # 1. Section headers
    make_section_header("01", "Introduction", "Background & Focus", "section-01-introduction.svg")
    make_section_header("02", "Featured Projects", "Full-Stack & AI Systems", "section-02-projects.svg")
    make_section_header("03", "Certifications", "Verified Credentials", "section-03-certifications.svg")
    make_section_header("04", "Technical Skills", "Core Stack & Technologies", "section-04-skills.svg")
    make_section_header("05", "GitHub Activity", "Contributions & Workflows", "section-05-activity.svg")
    make_section_header("06", "Professional Links", "Connect & Collaborate", "section-06-links.svg")

    # 2. Interactive Terminal (v2)
    make_terminal()

    # 3. Project cards with animated micro-demos (v2)
    make_project_card("ResQ", "Real-Time Disaster Coordination & AI Relief Platform",
                      ["Next.js", "React", "TypeScript", "Supabase", "Gemini API"],
                      "AI RELIEF SYSTEM", "resq", "project-resq.svg")

    make_project_card("AI Code Explainer", "AI-Powered Code Analysis & Optimization Platform",
                      ["React", "FastAPI", "Gemini API", "Python", "AST Analyzer"],
                      "AI CODE ANALYSIS", "code", "project-code-explainer.svg")

    make_project_card("Fraud Shield", "AI Fraud Detection System (99.4% F1 · 99.5% ROC-AUC)",
                      ["Python", "FastAPI", "scikit-learn", "XGBoost", "Three.js"],
                      "MACHINE LEARNING", "shield", "project-fraud-shield.svg")

    # 4. Custom Burgundy Contribution Snake (v2)
    make_snake()

    # 5. Buttons
    make_button("View Repository →", "arrow", 180, "link-repo-resq.svg")
    make_button("siddharth-meka-16", "github", 195, "link-github.svg")
    make_button("siddharth-meka", "linkedin", 185, "link-linkedin.svg")

    # 6. Complex cards
    make_certifications()
    make_skills()

if __name__ == "__main__":
    main()
