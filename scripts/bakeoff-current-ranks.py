#!/usr/bin/env python3
"""Karakeep embedding bake-off, step 1 of 2: record what the CURRENT embedding model returns.

Runs on the laptop. For each query in config/bakeoff-queries.json it asks Karakeep for a semantic search
through `director-worker/scripts/labread.py karakeep search ... semantic` (read only) and keeps only the
bookmark ids, in order. No bookmark title or text is printed or saved. The query text itself goes to the
current embedder (OpenRouter), which is what every search already does.

Usage: python bakeoff-current-ranks.py [--mode semantic|hybrid] [--out current.json]
Output: current.json  {"<query>": ["<id>", ...]}  (top 20)
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LABREAD = os.environ.get("LABREAD", r"C:\Development\Yingson Labs\director-worker\scripts\labread.py")
ID_RE = re.compile(r"^([a-z0-9]{24})\s")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--queries", default=os.path.join(HERE, "..", "config", "bakeoff-queries.json"))
    ap.add_argument("--mode", default="semantic", choices=["semantic", "hybrid"])
    ap.add_argument("--out", default="current.json")
    a = ap.parse_args()
    queries = json.load(open(a.queries, encoding="utf-8"))["queries"]
    out = {}
    for item in queries:
        r = subprocess.run([sys.executable, LABREAD, "karakeep", "search", item["q"], a.mode, "--limit", "20"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        ids = [m.group(1) for line in (r.stdout or "").splitlines() if (m := ID_RE.match(line))]
        out[item["q"]] = ids
        rank = ids.index(item["expect"]) + 1 if item["expect"] in ids else None
        print(f"{item['note']:24} results={len(ids):2d} expected rank={rank}")
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {a.out} (ids only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
