#!/usr/bin/env python3
"""Generate assets/activity.svg from real GitHub contribution data.

Run by .github/workflows/activity.yml with the workflow's built-in GITHUB_TOKEN,
or locally/fallback via public endpoints.
No secrets are written to the output. If all API calls fail, the existing SVG is left untouched.
Usage: python scripts/generate_activity.py [--login siddharth-meka-16] [--out assets/activity.svg]
"""
import argparse, datetime as dt, json, os, sys, urllib.request

QUERY = """
query($login:String!){
  user(login:$login){
    repositories(ownerAffiliations:OWNER, privacy:PUBLIC, isFork:false, first:100){
      totalCount
      nodes{ stargazerCount }
    }
    contributionsCollection{
      contributionCalendar{
        totalContributions
        weeks{ contributionDays{ date contributionCount } }
      }
    }
  }
}"""

MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, 'DejaVu Sans Mono', monospace"
SERIF = "Georgia, 'Times New Roman', 'DejaVu Serif', serif"
DIM = ' fill-opacity="0.35"'
LEVELS = ["#451126", "#701A3D", "#A24A70", "#C77B9B", "#E5B5C7"]  # palette steps between wine and pale rose


def fetch_graphql(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-activity"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload or not payload.get("data", {}).get("user"):
        raise RuntimeError("GitHub API returned no usable data")
    u = payload["data"]["user"]
    cal = u["contributionsCollection"]["contributionCalendar"]
    weeks = [[d["contributionCount"] for d in w["contributionDays"]] for w in cal["weeks"]]
    dates = [[d["date"] for d in w["contributionDays"]] for w in cal["weeks"]]
    return {
        "total": cal["totalContributions"], "weeks": weeks, "dates": dates,
        "repos": u["repositories"]["totalCount"],
        "stars": sum(n["stargazerCount"] for n in u["repositories"]["nodes"]),
    }


def fetch_public(login):
    # 1. User profile for repos count
    u_req = urllib.request.Request(f"https://api.github.com/users/{login}", headers={"User-Agent": "profile-activity"})
    with urllib.request.urlopen(u_req, timeout=20) as r:
        u_data = json.load(r)
    repos_count = u_data.get("public_repos", 0)

    # 2. Public repos for stars count
    r_req = urllib.request.Request(f"https://api.github.com/users/{login}/repos?per_page=100", headers={"User-Agent": "profile-activity"})
    with urllib.request.urlopen(r_req, timeout=20) as r:
        r_data = json.load(r)
    stars_count = sum(repo.get("stargazers_count", 0) for repo in r_data)

    # 3. Contributions calendar via reliable public provider
    c_req = urllib.request.Request(f"https://github-contributions-api.jogruber.de/v4/{login}?y=last", headers={"User-Agent": "profile-activity"})
    with urllib.request.urlopen(c_req, timeout=20) as r:
        c_data = json.load(r)

    days = c_data.get("contributions", [])
    total = c_data.get("total", {}).get("lastYear", sum(d.get("count", 0) for d in days))

    weeks = []
    dates = []
    cw = []
    cd = []
    for d in days:
        cw.append(d.get("count", 0))
        cd.append(d.get("date", ""))
        if len(cw) == 7:
            weeks.append(cw)
            dates.append(cd)
            cw, cd = [], []
    if cw:
        while len(cw) < 7:
            cw.append(0)
            cd.append("")
        weeks.append(cw)
        dates.append(cd)

    return {
        "total": total,
        "weeks": weeks,
        "dates": dates,
        "repos": repos_count,
        "stars": stars_count,
    }


def fetch(login, token=None):
    if token:
        try:
            return fetch_graphql(login, token)
        except Exception as e:
            print(f"GraphQL fetch failed ({e}), falling back to public endpoint...")
    return fetch_public(login)


def longest_streak(weeks):
    best = cur = 0
    for w in weeks:
        for c in w:
            cur = cur + 1 if c > 0 else 0
            best = max(best, cur)
    return best


def level(c, mx):
    if c <= 0 or mx <= 0: return 0
    q = c / mx
    return 1 if q <= 0.25 else 2 if q <= 0.5 else 3 if q <= 0.75 else 4


def esc(s): return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(data, login):
    W, H = 1000, 400
    live = data is not None
    weeks = data["weeks"] if live else [[0] * 7 for _ in range(53)]
    dates = data["dates"] if live else None
    mx = max((c for w in weeks for c in w), default=0)
    cell, gap, x0, y0 = 13, 4, 62, 196
    stats = ([(f'{data["total"]:,}', "CONTRIBUTIONS", "LAST 12 MONTHS"), (str(data["repos"]), "PUBLIC", "REPOSITORIES"),
              (str(data["stars"]), "STARS EARNED", "ON OWN REPOS"), (str(longest_streak(weeks)), "LONGEST STREAK", "DAYS IN WINDOW")]
             if live else [("—", "CONTRIBUTIONS", "LAST 12 MONTHS"), ("—", "PUBLIC", "REPOSITORIES"),
                           ("—", "STARS EARNED", "ON OWN REPOS"), ("—", "LONGEST STREAK", "DAYS IN WINDOW")])
    note = ("REAL GITHUB DATA · REFRESHED DAILY" if live else "WAITING FOR FIRST WORKFLOW RUN · NO DATA SHOWN YET")
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ac-title ac-desc">',
           f'  <title id="ac-title">GitHub activity for {esc(login)}</title>',
           f'  <desc id="ac-desc">{"Contribution calendar for the last 12 months generated from GitHub data." if live else "Placeholder. The contribution calendar appears after the activity workflow runs for the first time."}</desc>',
           '  <defs>',
           '    <linearGradient id="ac-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#10070C"/><stop offset="0.55" stop-color="#190B12"/><stop offset="1" stop-color="#451126"/></linearGradient>',
           '    <radialGradient id="ac-glow" cx="0.9" cy="0.1" r="0.6"><stop offset="0" stop-color="#701A3D" stop-opacity="0.6"/><stop offset="1" stop-color="#701A3D" stop-opacity="0"/></radialGradient>',
           f'    <clipPath id="ac-clip"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
           '  </defs>',
           f'  <g clip-path="url(#ac-clip)"><rect width="{W}" height="{H}" fill="url(#ac-bg)"/><rect width="{W}" height="{H}" fill="url(#ac-glow)"/>',
           f'  <rect x="40" y="38" width="28" height="2" fill="#C77B9B"/>',
           f'  <text x="78" y="44" font-family="{MONO}" font-size="13" letter-spacing="3" fill="#C77B9B">{note}</text>']
    for i, (big, l1, l2) in enumerate(stats):
        x = 40 + i * 236
        out += [f'  <text x="{x}" y="104" font-family="{SERIF}" font-size="46" fill="#F8F0F3">{esc(big)}</text>',
                f'  <text x="{x}" y="128" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="#C77B9B">{l1}</text>',
                f'  <text x="{x}" y="146" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="#C77B9B" fill-opacity="0.75">{l2}</text>']
    # month labels (live only)
    if live and dates:
        last = None
        for wi, d in enumerate(dates):
            if not d or not d[0]: continue
            try:
                m = dt.date.fromisoformat(d[0]).strftime("%b").upper()
            except Exception:
                continue
            if m != last and wi < len(dates) - 2:
                out.append(f'  <text x="{x0 + wi * (cell + gap)}" y="{y0 - 10}" font-family="{MONO}" font-size="11" letter-spacing="1" fill="#C77B9B" fill-opacity="0.8">{m}</text>')
                last = m
    for lab, row in (("MON", 1), ("WED", 3), ("FRI", 5)):
        out.append(f'  <text x="40" y="{y0 + row * (cell + gap) + 11}" font-family="{MONO}" font-size="10" letter-spacing="1" fill="#C77B9B" fill-opacity="0.8">{lab}</text>')
    for wi, w in enumerate(weeks):
        for di, c in enumerate(w):
            lv = level(c, mx) if live else 0
            fill_op = ' fill-opacity="0.35"' if (lv == 0) else ""
            out.append(f'  <rect x="{x0 + wi * (cell + gap)}" y="{y0 + di * (cell + gap)}" width="{cell}" height="{cell}" rx="3" fill="{LEVELS[lv]}"{fill_op}/>')
    ly = y0 + 7 * (cell + gap) + 18
    out.append(f'  <text x="{W - 40 - 5 * 17 - 92}" y="{ly + 10}" font-family="{MONO}" font-size="11" letter-spacing="1" fill="#C77B9B">LESS</text>')
    for i, col in enumerate(LEVELS):
        out.append(f'  <rect x="{W - 40 - 5 * 17 - 40 + i * 17}" y="{ly}" width="13" height="13" rx="3" fill="{col}"{DIM if i == 0 else ""}/>')
    out.append(f'  <text x="{W - 40 - 28}" y="{ly + 10}" font-family="{MONO}" font-size="11" letter-spacing="1" fill="#C77B9B">MORE</text>')
    out += ['  </g>', f'  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="#701A3D" stroke-opacity="0.85"/>', '</svg>', '']
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--login", default=os.environ.get("PROFILE_LOGIN", "siddharth-meka-16"))
    ap.add_argument("--out", default="assets/activity.svg")
    ap.add_argument("--placeholder", action="store_true", help="write the no-data placeholder and exit")
    ap.add_argument("--from-json", help="(testing only) render from a local JSON file instead of the API")
    a = ap.parse_args()
    if a.placeholder:
        data = None
    elif a.from_json:
        data = json.load(open(a.from_json))
    else:
        token = os.environ.get("GITHUB_TOKEN")
        try:
            data = fetch(a.login, token)
        except Exception as e:
            sys.exit(f"Could not fetch data ({e}); leaving existing file untouched")
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(render(data, a.login))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
