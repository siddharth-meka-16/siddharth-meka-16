#!/usr/bin/env python3
"""
Generate all supplementary profile SVG assets in the burgundy theme:
#10070C, #190B12, #451126, #701A3D, #C77B9B, #E5B5C7, #F8F0F3
"""
import os, xml.sax.saxutils as sax

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
    # Estimate title width for placing subtitle
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
# 2. Project Card Banner Generator
# -------------------------------------------------------------
def make_project_card(title, subtitle, tags, badge_text, icon_type, filename):
    w, h = 1000, 114
    key = filename.replace(".svg", "").replace("-", "_")

    # Tag chips computation
    tag_elements = []
    tx = 30
    for tag in tags:
        tw = len(tag) * 8 + 22
        tag_elements.append(f"""
    <g transform="translate({tx}, 74)">
      <rect width="{tw}" height="24" rx="12" fill="#10070C" stroke="#451126" stroke-width="1"/>
      <text x="{tw/2}" y="16" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#E5B5C7">{esc(tag)}</text>
    </g>""")
        tx += tw + 10

    # Project icon SVG path
    if icon_type == "resq":
        icon_path = """
        <path d="M 0 -12 L 12 -4 L 12 8 L 0 16 L -12 8 L -12 -4 Z" fill="none" stroke="#C77B9B" stroke-width="1.5"/>
        <path d="M -4 2 L 4 2 M 0 -2 L 0 6" stroke="#E5B5C7" stroke-width="2" stroke-linecap="round"/>
        """
    elif icon_type == "code":
        icon_path = """
        <path d="M -6 -6 L -12 0 L -6 6 M 6 -6 L 12 0 L 6 6" fill="none" stroke="#C77B9B" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
        <line x1="2" y1="-8" x2="-2" y2="8" stroke="#E5B5C7" stroke-width="1.5" stroke-linecap="round"/>
        """
    else: # fraud shield
        icon_path = """
        <path d="M 0 -12 C 7 -12 11 -8 11 -2 C 11 7 4 12 0 15 C -4 12 -11 7 -11 -2 C -11 -8 -7 -12 0 -12 Z" fill="none" stroke="#C77B9B" stroke-width="1.5"/>
        <circle cx="0" cy="1" r="2.5" fill="#E5B5C7"/>
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
  <rect x="0" y="24" width="4" height="66" rx="2" fill="#C77B9B"/>

  <!-- Project Icon container -->
  <g transform="translate(52, 40)">
    <circle cx="0" cy="0" r="22" fill="#10070C" stroke="#701A3D" stroke-width="1.2"/>
    {icon_path}
  </g>

  <!-- Title & Subtitle -->
  <text x="88" y="37" font-family="{SERIF}" font-size="26" font-weight="600" fill="#F8F0F3" letter-spacing="0.5">{esc(title)}</text>
  <text x="88" y="56" font-family="{SANS}" font-size="13" fill="#E5B5C7" opacity="0.9">{esc(subtitle)}</text>

  <!-- Badge pill on top right -->
  <g transform="translate({w-170}, 24)">
    <rect width="144" height="26" rx="13" fill="#10070C" stroke="#701A3D" stroke-width="1"/>
    <circle cx="15" cy="13" r="3.5" fill="#C77B9B">
      <animate attributeName="opacity" values="1;0.4;1" dur="2.5s" repeatCount="indefinite"/>
    </circle>
    <text x="76" y="17" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="600" fill="#E5B5C7" letter-spacing="1">{esc(badge_text)}</text>
  </g>

  <!-- Tags -->
  <g>
    {"".join(tag_elements)}
  </g>
</svg>"""
    write_svg(filename, svg)

# -------------------------------------------------------------
# 3. Pill Button Badges
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

# -------------------------------------------------------------
# 4. Certifications Card
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
      <rect width="460" height="85" rx="12" fill="#14080F" stroke="#701A3D" stroke-opacity="0.7" stroke-width="1"/>
      <!-- verified check icon -->
      <g transform="translate(24, 42)">
        <circle cx="0" cy="0" r="14" fill="#10070C" stroke="#C77B9B" stroke-width="1.2"/>
        <path d="M -5 0 L -1 4 L 6 -3" fill="none" stroke="#E5B5C7" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
      <!-- issuer & title -->
      <text x="50" y="32" font-family="{MONO}" font-size="11" font-weight="700" fill="#C77B9B" letter-spacing="1">{esc(issuer.upper())}</text>
      <text x="50" y="52" font-family="{SERIF}" font-size="15" font-weight="600" fill="#F8F0F3">{esc(title)}</text>
      <text x="50" y="70" font-family="{MONO}" font-size="10" fill="#E5B5C7" opacity="0.75">{esc(date_str)}  ·  {esc(badge)}</text>
      <!-- decorative badge on right -->
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

# -------------------------------------------------------------
# 5. Technical Skills Card
# -------------------------------------------------------------
def make_skills():
    w, h = 1000, 310
    categories = [
        ("PROGRAMMING LANGUAGES", ["Java", "Python", "C", "TypeScript", "JavaScript"]),
        ("CS FUNDAMENTALS", ["Data Structures & Algorithms", "OOP", "DBMS", "Operating Systems", "Networks"]),
        ("FRONTEND & BACKEND", ["React", "Next.js", "HTML5 & CSS3", "FastAPI", "Node.js", "Express.js", "REST APIs"]),
        ("AI, CLOUD & TOOLS", ["Gemini API", "scikit-learn", "XGBoost", "Supabase", "MySQL", "Vercel", "Git & GitHub"]),
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
      <text x="36" y="{sy+16}" font-family="{SANS}" font-size="11" font-weight="500" fill="#E5B5C7">{esc(skill)}</text>""")
            sy += 29

        cols_svg.append(f"""
    <g transform="translate({cx}, 20)">
      <rect width="{col_w}" height="268" rx="12" fill="#14080F" stroke="#701A3D" stroke-opacity="0.6" stroke-width="1"/>
      <rect x="0" y="0" width="{col_w}" height="38" rx="12" fill="#190B12"/>
      <rect x="0" y="26" width="{col_w}" height="12" fill="#190B12"/>
      <line x1="0" y1="38" x2="{col_w}" y2="38" stroke="#701A3D" stroke-width="1"/>
      <text x="14" y="24" font-family="{MONO}" font-size="10.5" font-weight="700" fill="#C77B9B" letter-spacing="1">{esc(cat_title)}</text>
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

    # 2. Project cards
    make_project_card("ResQ", "Real-Time Disaster Coordination & AI Relief Platform",
                      ["Next.js", "React", "TypeScript", "Supabase", "Gemini API"],
                      "AI RELIEF SYSTEM", "resq", "project-resq.svg")

    make_project_card("AI Code Explainer", "AI-Powered Code Analysis & Optimization Platform",
                      ["React", "FastAPI", "Gemini API", "Python", "AST Analyzer"],
                      "AI CODE ANALYSIS", "code", "project-code-explainer.svg")

    make_project_card("Fraud Shield", "AI Fraud Detection System (99.4% F1 · 99.5% ROC-AUC)",
                      ["Python", "FastAPI", "scikit-learn", "XGBoost", "Three.js"],
                      "MACHINE LEARNING", "shield", "project-fraud-shield.svg")

    # 3. Buttons
    make_button("View Repository →", "arrow", 180, "link-repo-resq.svg")
    make_button("siddharth-meka-16", "github", 195, "link-github.svg")
    make_button("siddharth-meka", "linkedin", 185, "link-linkedin.svg")

    # 4. Complex cards
    make_certifications()
    make_skills()

if __name__ == "__main__":
    main()
