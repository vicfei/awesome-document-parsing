#!/usr/bin/env python3
"""Community star leaderboard — snapshot-diff method.

GitHub has closed stargazer timeline access to third-party tokens
(REST /stargazers 404, GraphQL edges empty, star+json preview removed),
so "weekly gain" cannot be queried directly. Instead: this script snapshots
total stars; the gain since the previous snapshot is computed by diff.

Usage:
  python3 leaderboard.py                    # reads latest snapshots/*.json, writes new one, prints tables
  GH_PAT / GITHUB_TOKEN env or ~/.git-credentials used for auth (5000 req/h).
Refresh cadence: weekly recommended (any cadence works — diff is divided by days).
"""
import json, glob, os, sys, datetime, urllib.request

REPOS = ["PaddlePaddle/PaddleOCR","docling-project/docling","opendatalab/MinerU",
         "opendataloader-project/opendataloader-pdf","datalab-to/marker",
         "Unstructured-IO/unstructured","mindee/doctr","NanoNets/docstrange",
         "datalab-to/indra","Topdu/OpenOCR"]

def get_pat():
    if os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN"):
        return os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
    try:
        cred = open(os.path.expanduser("~/.git-credentials")).read()
        for line in cred.splitlines():
            if "github.com" in line and ":" in line:
                return line.split(":")[-1].rstrip("@github.com").split("@")[0] if False else line.rsplit(":",1)[1].split("@")[0]
    except FileNotFoundError:
        pass
    return None

def fetch(pat):
    opener = urllib.request.build_opener()
    headers = {"User-Agent":"leaderboard","Accept":"application/vnd.github+json"}
    if pat: headers["Authorization"] = f"token {pat}"
    out = []
    for r in REPOS:
        req = urllib.request.Request(f"https://api.github.com/repos/{r}", headers=headers)
        d = json.loads(opener.open(req, timeout=30).read())
        out.append({"repo": r, "stars": d["stargazers_count"]})
        print(f"{r}: {d['stargazers_count']}", file=sys.stderr)
    return out, datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

def main():
    snapdir = os.path.join(os.path.dirname(__file__), "..", "snapshots")
    prev = sorted(glob.glob(os.path.join(snapdir, "leaderboard-*.json")))
    pat = get_pat()
    cur, today = fetch(pat)
    if prev:
        p = json.load(open(prev[-1]))
        pdate = os.path.basename(prev[-1]).removeprefix("leaderboard-").removesuffix(".json")
        days = max((datetime.datetime.strptime(today,"%Y-%m-%d") - datetime.datetime.strptime(pdate,"%Y-%m-%d")).days, 1)
        pv = {x["repo"]: x["stars"] for x in p}
        for c in cur: c["gain"] = c["stars"] - pv.get(c["repo"], c["stars"]); c["per_week"] = round(c["gain"] * 7 / days)
        label = f"gain since {pdate} ({days}d), normalized to 7d"
    else:
        for c in cur: c["gain"] = None; c["per_week"] = None
        label = "first snapshot — gains appear from the next refresh"
    json.dump({"date": today, "label": label, "rows": cur},
              open(os.path.join(snapdir, f"leaderboard-{today}.json"),"w"), indent=1)
    print(f"\n## By total stars (as of {today})\n")
    print("| # | Repo | Stars | Weekly gain* |")
    print("|---|---|---|---|")
    for i, c in enumerate(sorted(cur, key=lambda x: -x["stars"]), 1):
        w = c["per_week"] if c["per_week"] is not None else "—"
        print(f"| {i} | [{c['repo']}](https://github.com/{c['repo']}) | {c['stars']:,} | {w} |")
    ranked = [c for c in cur if c["per_week"] is not None]
    print(f"\n## By weekly gain* ({label})\n")
    print("| # | Repo | Weekly gain* | Stars |")
    print("|---|---|---|---|")
    if ranked:
        for i, c in enumerate(sorted(ranked, key=lambda x: -x["per_week"]), 1):
            print(f"| {i} | [{c['repo']}](https://github.com/{c['repo']}) | +{c['per_week']} | {c['stars']:,} |")
    else:
        print("| — | _appears after second refresh_ | — | — |")

if __name__ == "__main__":
    main()
