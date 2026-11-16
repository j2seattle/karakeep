"""Hand-picked design list apart from AI design tags (WISH-949, Jason approved 2026-11-16).

  python design_pick.py            dry run: count the hand-picked set and what would change
  python design_pick.py --apply    tag them design-pick and point the "Design and UI" smart list at #design-pick

The hand-picked set is every bookmark that carried design-ui in the pre-window export
(C:/Users/thedu/karakeep-exports/20261116-pre-window/bookmarks-tags.json), before the AI retag
spread design-ui to more bookmarks. design-pick is not in the curated AI vocabulary, so the AI
never adds it; only Jason (or a rule he approves) does. Prints ids and counts, not URLs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kk_client import Client  # noqa: E402
import mapping  # noqa: E402

EXPORT = Path(r"C:\Users\thedu\karakeep-exports\20261116-pre-window\bookmarks-tags.json")
TAG = "design-pick"
LIST_NAME = "Design and UI"
QUERY = "#design-pick"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    act = "APPLY" if a.apply else "DRY"
    if TAG in mapping.VOCAB:
        print(f"{TAG} is in the curated AI vocabulary; stop")
        return 1

    rows = json.loads(EXPORT.read_text(encoding="utf-8"))
    picked = [r["id"] for r in rows if any(t.get("name") == "design-ui" for t in r.get("tags") or [])]
    print(f"hand-picked design-ui in export: {len(picked)}")

    c = Client()
    done = missing = already = 0
    for bid in picked:
        s, b = c.rest("GET", f"/bookmarks/{bid}?includeContent=false")
        if s != 200:
            missing += 1
            continue
        if any(t["name"] == TAG for t in b.get("tags") or []):
            already += 1
            continue
        if a.apply:
            s, _ = c.rest("POST", f"/bookmarks/{bid}/tags", {"tags": [{"tagName": TAG}]})
            if s != 200:
                print(f"tag {bid}: HTTP {s}")
                continue
        done += 1
    print(f"{act} tag {TAG}: {done}; already {already}; gone since export {missing}")

    s, lists = c.rest("GET", "/lists")
    l = next((x for x in lists["lists"] if x["name"] == LIST_NAME), None)
    if l is None:
        print(f"list {LIST_NAME} not found")
        return 1
    if l.get("query") != QUERY:
        print(f"{act} list {LIST_NAME}: {l.get('query')} -> {QUERY}")
        if a.apply:
            s, _ = c.rest("PATCH", f"/lists/{l['id']}", {
                "query": QUERY,
                "description": "Hand-picked design and UI links (design-pick). The AI tag design-ui is broader."})
            print(f"  status={s}")
    else:
        print("list already points at #design-pick")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
