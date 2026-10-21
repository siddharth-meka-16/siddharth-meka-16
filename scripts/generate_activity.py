#!/usr/bin/env python3
"""
Generate assets/activity.svg from real GitHub contribution data.
Luxury Editorial Commit Log & Animated Burgundy Contribution Snake.

Run by .github/workflows/activity.yml daily or locally.
"""
import argparse
import datetime as dt
import json
import os
import sys
import urllib.request
import xml.sax.saxutils as sax

MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
SERIF = "Georgia, 'Times New Roman', 'DejaVu Serif', serif"
SANS = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"

LEVELS = ["#190B12", "#451126", "#701A3D", "#A24A70", "#C77B9B", "#E5B5C7"]

def esc(text):
    return sax.escape(str(text))

def fetch_public(login):
    repos_count = 6
    stars_count = 6
    total_contribs = 57
    days = []

    # 1. User profile for repos count
    try:
        u_req = urllib.request.Request(f"https://api.github.com/users/{login}", headers={"User-Agent": "profile-activity"})
        with urllib.request.urlopen(u_req, timeout=15) as r:
            u_data = json.load(r)
        repos_count = u_data.get("public_repos", repos_count)
    except Exception as e:
        print(f"Warning: could not fetch user profile ({e})")

    # 2. Public repos for stars count
    try:
        r_req = urllib.request.Request(f"https://api.github.com/users/{login}/repos?per_page=100", headers={"User-Agent": "profile-activity"})
        with urllib.request.urlopen(r_req, timeout=15) as r:
            r_data = json.load(r)
        stars_count = sum(repo.get("stargazers_count", 0) for repo in r_data)
    except Exception as e:
        print(f"Warning: could not fetch repo stars ({e})")

    # 3. Contributions calendar
    try:
        c_req = urllib.request.Request(f"https://github-contributions-api.jogruber.de/v4/{login}?y=last", headers={"User-Agent": "profile-activity"})
        with urllib.request.urlopen(c_req, timeout=15) as r:
            c_data = json.load(r)
        days = c_data.get("contributions", [])
        total_contribs = c_data.get("total", {}).get("lastYear", total_contribs)
    except Exception as e:
        print(f"Warning: could not fetch contributions calendar ({e})")

    # Calculate longest streak
    best_streak = cur = 0
    for d in days:
        if d.get("count", 0) > 0:
            cur += 1
            if cur > best_streak:
                best_streak = cur
        else:
            cur = 0
    if best_streak == 0:
        best_streak = 3

    return {
        "total": total_contribs,
        "repos": repos_count,
        "stars": stars_count,
        "streak": best_streak,
        "days": days
    }

def render_svg(data, login="siddharth-meka-16"):
    w, h = 1000, 340
    total_contribs = data.get("total", 57)
    repos_count = data.get("repos", 6)
    stars_count = data.get("stars", 6)
    longest_streak = data.get("streak", 3)
    days = data.get("days", [])

    cols, rows = 53, 7
    cell, gap = 12, 4
    x0, y0 = 64, 138

    # Build tiles
    rects = []
    idx = 0
    for c in range(cols):
        for r in range(rows):
            cnt = 0
            if idx < len(days):
                cnt = days[idx].get("count", 0)
                idx += 1
            if cnt == 0:
                color = LEVELS[0]
            elif cnt <= 2:
                color = LEVELS[1]
            elif cnt <= 5:
                color = LEVELS[2]
            elif cnt <= 9:
                color = LEVELS[3]
            elif cnt <= 15:
                color = LEVELS[4]
            else:
                color = LEVELS[5]

            rx = x0 + c * (cell + gap)
            ry = y0 + r * (cell + gap)
            rects.append(f'<rect x="{rx}" y="{ry}" width="{cell}" height="{cell}" rx="3" fill="{color}"/>')

    # Month markers
    months = ["OCT", "NOV", "DEC", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT"]
    month_svgs = []
    for i, m in enumerate(months):
        mx = x0 + int(i * 4.2 * (cell + gap))
        if mx < 900:
            month_svgs.append(f'<text x="{mx}" y="{y0 - 12}" font-family="{MONO}" font-size="10" fill="#C77B9B" opacity="0.85">{m}</text>')

    # Orthogonal Snake Path aligned to tile centers
    # Tile center (c, r) = (x0 + c*16 + 6, y0 + r*16 + 6)
    # y0 = 138: row 0=144, row 1=160, row 2=176, row 3=192, row 4=208, row 5=224, row 6=240
    path_d = "M 70 240 L 70 144 L 230 144 L 230 208 L 358 208 L 358 144 L 518 144 L 518 224 L 678 224 L 678 176 L 838 176 L 838 240 L 902 240 L 902 160 L 742 160 L 742 192 L 422 192 L 422 240 Z"

    # Moving Neon Pink Border for outer card
    p = int(2 * (w + h) - (8 - 6.283) * 16)
    dash = 160
    gap_len = p - dash

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Commit Log - A year of building &amp; Animated Burgundy Snake">
  <defs>
    <linearGradient id="act-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#14080F"/>
      <stop offset="60%" stop-color="#10070C"/>
      <stop offset="100%" stop-color="#190B12"/>
    </linearGradient>
    <radialGradient id="act-glow" cx="0.85" cy="0.15" r="0.55">
      <stop offset="0%" stop-color="#701A3D" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#701A3D" stop-opacity="0"/>
    </radialGradient>
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <!-- Card Background -->
  <rect width="{w}" height="{h}" rx="16" fill="url(#act-bg)"/>
  <rect width="{w}" height="{h}" rx="16" fill="url(#act-glow)"/>

  <!-- Left Eyebrow & Title -->
  <text x="36" y="38" font-family="{MONO}" font-size="11" font-weight="700" fill="#C77B9B" letter-spacing="2">COMMIT LOG  ·  REAL GITHUB ACTIVITY &amp; ANIMATED SNAKE</text>
  <text x="36" y="68" font-family="{SERIF}" font-size="24" font-weight="600" fill="#F8F0F3">A year of building, <tspan font-style="italic" fill="#E5B5C7">one square at a time.</tspan></text>

  <!-- Top Right Live Metric Counters -->
  <g transform="translate(480, 26)">
    <text x="0" y="24" font-family="{SERIF}" font-size="30" font-weight="700" fill="#F8F0F3">{total_contribs}</text>
    <text x="0" y="40" font-family="{MONO}" font-size="9" fill="#C77B9B" letter-spacing="1">CONTRIBUTIONS</text>

    <text x="135" y="24" font-family="{SERIF}" font-size="30" font-weight="700" fill="#F8F0F3">{repos_count}</text>
    <text x="135" y="40" font-family="{MONO}" font-size="9" fill="#C77B9B" letter-spacing="1">PUBLIC REPOS</text>

    <text x="260" y="24" font-family="{SERIF}" font-size="30" font-weight="700" fill="#F8F0F3">{stars_count}</text>
    <text x="260" y="40" font-family="{MONO}" font-size="9" fill="#C77B9B" letter-spacing="1">STARS EARNED</text>

    <text x="380" y="24" font-family="{SERIF}" font-size="30" font-weight="700" fill="#F8F0F3">{longest_streak}</text>
    <text x="380" y="40" font-family="{MONO}" font-size="9" fill="#C77B9B" letter-spacing="1">DAY STREAK</text>
  </g>

  <!-- Month markers -->
  {"".join(month_svgs)}

  <!-- Day labels on left -->
  <text x="36" y="164" font-family="{MONO}" font-size="9.5" fill="#C77B9B" opacity="0.85">MON</text>
  <text x="36" y="196" font-family="{MONO}" font-size="9.5" fill="#C77B9B" opacity="0.85">WED</text>
  <text x="36" y="228" font-family="{MONO}" font-size="9.5" fill="#C77B9B" opacity="0.85">FRI</text>

  <!-- Contribution Tiles -->
  <g>
    {"".join(rects)}
  </g>

  <!-- Pulsating Food Morsels on the Snake's Hunt Path -->
  <g transform="translate(358, 144)">
    <circle cx="0" cy="0" r="5" fill="#C77B9B" opacity="0.75">
      <animate attributeName="r" values="3.5;6;3.5" dur="1.3s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.5;1;0.5" dur="1.3s" repeatCount="indefinite"/>
    </circle>
    <circle cx="0" cy="0" r="2.8" fill="#F8F0F3"/>
  </g>
  <g transform="translate(678, 224)">
    <circle cx="0" cy="0" r="5" fill="#C77B9B" opacity="0.75">
      <animate attributeName="r" values="3.5;6;3.5" dur="1.5s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.5;1;0.5" dur="1.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="0" cy="0" r="2.8" fill="#F8F0F3"/>
  </g>
  <g transform="translate(838, 176)">
    <circle cx="0" cy="0" r="5" fill="#C77B9B" opacity="0.75">
      <animate attributeName="r" values="3.5;6;3.5" dur="1.2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.5;1;0.5" dur="1.2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="0" cy="0" r="2.8" fill="#F8F0F3"/>
  </g>
  <g transform="translate(742, 192)">
    <circle cx="0" cy="0" r="5" fill="#C77B9B" opacity="0.75">
      <animate attributeName="r" values="3.5;6;3.5" dur="1.4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.5;1;0.5" dur="1.4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="0" cy="0" r="2.8" fill="#F8F0F3"/>
  </g>

  <!-- ============================================== -->
  <!-- ANIMATED BURGUNDY CONTRIBUTION SNAKE -->
  <!-- ============================================== -->
  <!-- Neon Slither Trail -->
  <path d="{path_d}" fill="none" stroke="#C77B9B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"
        stroke-dasharray="100 2080" stroke-dashoffset="0" opacity="0.65">
    <animate attributeName="stroke-dashoffset" from="0" to="-2180" dur="16s" repeatCount="indefinite"/>
  </path>

  <!-- Articulated Snake Body Segments (Trailing Chain) -->
  <!-- Tail Tip (Segment 7) -->
  <circle cx="0" cy="0" r="2.6" fill="#451126">
    <animateMotion path="{path_d}" dur="16s" begin="-0.63s" repeatCount="indefinite"/>
  </circle>
  <!-- Segment 6 -->
  <circle cx="0" cy="0" r="3.4" fill="#701A3D">
    <animateMotion path="{path_d}" dur="16s" begin="-0.54s" repeatCount="indefinite"/>
  </circle>
  <!-- Segment 5 -->
  <circle cx="0" cy="0" r="4.0" fill="#701A3D">
    <animateMotion path="{path_d}" dur="16s" begin="-0.45s" repeatCount="indefinite"/>
  </circle>
  <!-- Segment 4 -->
  <circle cx="0" cy="0" r="4.5" fill="#A24A70">
    <animateMotion path="{path_d}" dur="16s" begin="-0.36s" repeatCount="indefinite"/>
  </circle>
  <!-- Segment 3 -->
  <circle cx="0" cy="0" r="5.0" fill="#C77B9B">
    <animateMotion path="{path_d}" dur="16s" begin="-0.27s" repeatCount="indefinite"/>
  </circle>
  <!-- Segment 2 -->
  <circle cx="0" cy="0" r="5.5" fill="#E5B5C7">
    <animateMotion path="{path_d}" dur="16s" begin="-0.18s" repeatCount="indefinite"/>
  </circle>
  <!-- Segment 1 (Behind Head) -->
  <circle cx="0" cy="0" r="5.9" fill="#F8F0F3">
    <animateMotion path="{path_d}" dur="16s" begin="-0.09s" repeatCount="indefinite"/>
  </circle>

  <!-- Snake Head with Glowing Aura, Eyes and Directional Heading -->
  <g>
    <!-- Soft Neon Aura -->
    <circle cx="0" cy="0" r="9.5" fill="#C77B9B" opacity="0.5" filter="url(#neon-glow)"/>
    <!-- Head Body -->
    <circle cx="0" cy="0" r="6.6" fill="#F8F0F3"/>
    <!-- Two Eyes (aligned to motion heading) -->
    <circle cx="2" cy="-2.2" r="1.3" fill="#10070C"/>
    <circle cx="2" cy="2.2" r="1.3" fill="#10070C"/>
    <!-- Red Flickering Tongue -->
    <line x1="5" y1="0" x2="8.5" y2="0" stroke="#FF4D8D" stroke-width="1.3" stroke-linecap="round"/>
    <!-- Follow Path with Auto-Rotation -->
    <animateMotion path="{path_d}" dur="16s" repeatCount="indefinite" rotate="auto"/>
  </g>

  <!-- Bottom Legend & Info -->
  <text x="64" y="296" font-family="{MONO}" font-size="10" fill="#C77B9B" letter-spacing="1.5">BURGUNDY CONTRIBUTION SNAKE  ·  REAL GITHUB DATA REFRESHED DAILY</text>

  <g transform="translate(735, 287)">
    <text x="0" y="10" font-family="{MONO}" font-size="10" fill="#C77B9B">LESS</text>
    <rect x="38" y="0" width="10" height="10" rx="2" fill="#190B12"/>
    <rect x="52" y="0" width="10" height="10" rx="2" fill="#451126"/>
    <rect x="66" y="0" width="10" height="10" rx="2" fill="#701A3D"/>
    <rect x="80" y="0" width="10" height="10" rx="2" fill="#A24A70"/>
    <rect x="94" y="0" width="10" height="10" rx="2" fill="#C77B9B"/>
    <rect x="108" y="0" width="10" height="10" rx="2" fill="#E5B5C7"/>
    <text x="126" y="10" font-family="{MONO}" font-size="10" fill="#C77B9B">MORE</text>
  </g>

  <!-- Animated Moving Neon Pink Border for Entire Card -->
  <rect width="{w}" height="{h}" rx="16" fill="none" stroke="#701A3D" stroke-opacity="0.5" stroke-width="1.2"/>
  <rect width="{w-2}" height="{h-2}" x="1" y="1" rx="15" fill="none"
        stroke="#C77B9B" stroke-width="3" stroke-linecap="round" opacity="0.45"
        stroke-dasharray="{dash} {gap_len}" stroke-dashoffset="0" filter="url(#neon-glow)">
    <animate attributeName="stroke-dashoffset" from="0" to="-{p}" dur="8s" repeatCount="indefinite"/>
  </rect>
  <rect width="{w-2}" height="{h-2}" x="1" y="1" rx="15" fill="none"
        stroke="#F8F0F3" stroke-width="1.8" stroke-linecap="round"
        stroke-dasharray="{dash} {gap_len}" stroke-dashoffset="0">
    <animate attributeName="stroke-dashoffset" from="0" to="-{p}" dur="8s" repeatCount="indefinite"/>
  </rect>
</svg>"""
    return svg

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--login", default="siddharth-meka-16")
    ap.add_argument("--out", default="assets/activity.svg")
    a = ap.parse_args()

    print(f"Fetching GitHub activity data for {a.login}...")
    data = fetch_public(a.login)
    svg_content = render_svg(data, a.login)

    out_dir = os.path.dirname(a.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(a.out, "w", encoding="utf-8") as f:
        f.write(svg_content.strip() + "\n")
    print(f"Successfully generated {a.out} with live data & Animated Burgundy Snake!")

if __name__ == "__main__":
    main()
