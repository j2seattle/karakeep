"""Apply Jason's image triage choices to Karakeep (plan KARAKEEP-WINDOW 5.3).

NOT run in the 2026-11-16 TAG lane. The coordinator runs it after Jason approves the action list.

Decisions file (JSON):
  {"decisions": [{"id": "<bookmark id>", "choice": "keep|remove|make-link|unsure", "note": "..."}]}

  python image_actions.py decisions.json                 dry run (default): counts and every id, no writes
  python image_actions.py decisions.json --apply --expect-remove N --expect-link M

Rules:
  keep, unsure   nothing happens.
  remove         the image bookmark is deleted.
  make-link      the original URL (asset sourceUrl) becomes a link bookmark (or an existing
                 link twin is used), tags / note / list membership are copied, then the image
                 is deleted.
Only bookmarks whose content type is "asset" are ever deleted. --apply refuses unless the
remove and make-link counts equal Jason's approved counts.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).parent))
from kk_client import Client  # noqa: E402
from dup_merge import dup_key  # noqa: E402

CHOICES = {"keep", "remove", "make-link", "unsure"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("decisions")
    ap.add_argument("--dry-run", action="store_true", help="default")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--expect-remove", type=int)
    ap.add_argument("--expect-link", type=int)
    a = ap.parse_args()

    dec = json.loads(Path(a.decisions).read_text(encoding="utf-8"))["decisions"]
    c = Client()
    live = {b["id"]: b for b in c.paged("/bookmarks?includeContent=false", "bookmarks", "limit=100")}
    twins = collections.defaultdict(list)
    for b in live.values():
        if b["content"]["type"] == "link":
            twins[dup_key(b["content"]["url"])].append(b["id"])

    counts = collections.Counter()
    todo = []
    errors = []
    for d in dec:
        ch = d.get("choice")
        b = live.get(d["id"])
        if ch not in CHOICES:
            errors.append((d["id"], "bad choice"))
            continue
        counts[ch] += 1
        if ch in ("keep", "unsure"):
            continue
        if not b or b["content"]["type"] != "asset":
            errors.append((d["id"], "missing or not an image bookmark"))
            continue
        if ch == "make-link":
            src = b["content"].get("sourceUrl")
            if not src:
                errors.append((d["id"], "no sourceUrl for make-link"))
                continue
            twin = twins.get(dup_key(src), [None])[0]
            todo.append({"id": d["id"], "choice": ch, "source": src, "twin": twin})
        else:
            todo.append({"id": d["id"], "choice": ch})

    print(f"choices: {dict(counts)}  errors: {len(errors)}")
    print("remove ids:", [t["id"] for t in todo if t["choice"] == "remove"])
    print("make-link ids:", [(t["id"], "twin" if t["twin"] else "new") for t in todo if t["choice"] == "make-link"])
    for e in errors:
        print("error", e)
    if not a.apply:
        print("dry run: nothing written")
        return 0 if not errors else 1
    if errors:
        print("ABORT: errors in the decisions file")
        return 2
    n_rm = counts["remove"]
    n_ln = counts["make-link"]
    if a.expect_remove != n_rm or a.expect_link != n_ln:
        print(f"ABORT: counts remove={n_rm} make-link={n_ln} differ from the approved list")
        return 2

    deleted = 0
    for t in todo:
        b = live[t["id"]]
        if t["choice"] == "make-link":
            target = t["twin"]
            if not target:
                s, r = c.rest("POST", "/bookmarks", {"type": "link", "url": t["source"],
                                                     "note": b.get("note") or None})
                if s not in (200, 201):
                    print(f"make_link_failed id={t['id']} status={s}")
                    continue
                target = r["id"]
            names = [{"tagName": x["name"], "attachedBy": x["attachedBy"]} for x in b["tags"]]
            if names:
                c.rest("POST", f"/bookmarks/{target}/tags", {"tags": names})
            s, lst = c.rest("GET", f"/bookmarks/{t['id']}/lists")
            for l in (lst or {}).get("lists", []):
                if l.get("type") == "manual":
                    c.rest("PUT", f"/lists/{l['id']}/bookmarks/{target}", {})
            if t["twin"] and b.get("note"):
                s, tw = c.rest("GET", f"/bookmarks/{target}?includeContent=false")
                if b["note"].strip() not in (tw.get("note") or ""):
                    new = ((tw.get("note") or "") + "\n\n" if tw.get("note") else "") + b["note"]
                    c.rest("PATCH", f"/bookmarks/{target}", {"note": new})
        s, _ = c.rest("DELETE", f"/bookmarks/{t['id']}")
        deleted += s in (200, 204)
    print(f"deleted images: {deleted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
