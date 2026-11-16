"""Merge duplicate link bookmarks (plan KARAKEEP-WINDOW 5.4, run 2026-11-16-karakeep-window).

  python dup_merge.py --plan P.json              find duplicates, write the plan (default, no changes)
  python dup_merge.py --merge P.json             move tags, notes and list membership onto the oldest copy; NO deletes
  python dup_merge.py --delete P.json --yes      delete the newer copies listed in the plan

Duplicate key: host without www (lowercase) + path without trailing slash. Query
strings are tracking noise (utm, s, a, shem, via, dub_id) except for YouTube,
where the v value is part of the key. Keep the oldest by createdAt. Only the
delete mode removes a bookmark, only ids named in the plan, and only when the
keeper still exists and every copy already shows the keeper's human tags.
Prints ids and counts, not URLs.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

sys.path.insert(0, str(Path(__file__).parent))
from kk_client import Client  # noqa: E402


def dup_key(url: str) -> str:
    p = urlsplit(url)
    host = p.netloc.lower().removeprefix("www.")
    path = p.path.rstrip("/")
    # YouTube: key by video id, whatever the link form (watch?v=, embed/, shorts/, live/, youtu.be/) (WISH-950).
    if host == "youtu.be":
        return "youtube:" + path.strip("/").split("/")[0]
    if host.endswith("youtube.com"):
        parts = [x for x in path.split("/") if x]
        if parts and parts[0] in ("embed", "shorts", "live", "v") and len(parts) > 1:
            return "youtube:" + parts[1]
        vid = dict(parse_qsl(p.query)).get("v", "")
        return "youtube:" + vid if vid else host + path
    return host + path


def list_membership(c: Client, bid: str):
    s, d = c.rest("GET", f"/bookmarks/{bid}/lists")
    return [l["id"] for l in d["lists"]] if s == 200 else None


def build_plan(c: Client):
    bms = list(c.paged("/bookmarks?includeContent=false", "bookmarks", "limit=100"))
    groups = collections.defaultdict(list)
    for b in bms:
        co = b["content"]
        if co.get("type") != "link":
            continue  # image bookmarks are never touched
        groups[dup_key(co["url"])].append(b)
    plan = []
    for key, items in groups.items():
        if len(items) < 2:
            continue
        items.sort(key=lambda b: b["createdAt"])
        keep, rest = items[0], items[1:]
        exact = all(r["content"]["url"] == keep["content"]["url"] for r in rest)
        entry = {
            "host": key.split("/")[0],
            "match": "exact-url" if exact else "same host+path (query or trailing slash differs)",
            "keep": keep["id"],
            "keep_created": keep["createdAt"],
            "delete": [r["id"] for r in rest],
            "moves": [],
        }
        keep_lists = set(list_membership(c, keep["id"]) or [])
        keep_human = {t["name"] for t in keep["tags"] if t["attachedBy"] == "human"}
        keep_all = {t["name"] for t in keep["tags"]}
        for r in rest:
            human = sorted({t["name"] for t in r["tags"] if t["attachedBy"] == "human"} - keep_all)
            lists = sorted(set(list_membership(c, r["id"]) or []) - keep_lists)
            note_add = bool(r.get("note")) and (r["note"] or "").strip() not in (keep.get("note") or "")
            entry["moves"].append(
                {"from": r["id"], "human_tags": human, "lists": lists, "append_note": note_add,
                 "favourite": bool(r["favourited"]) and not keep["favourited"]}
            )
            keep_human |= set(human)
            keep_lists |= set(lists)
        plan.append(entry)
    plan.sort(key=lambda e: e["keep"])
    return plan


def merge(c: Client, plan):
    for e in plan:
        s, keep = c.rest("GET", f"/bookmarks/{e['keep']}?includeContent=false")
        note = keep.get("note") or ""
        have_tags = {t["name"] for t in keep["tags"]}
        for m in e["moves"]:
            s, src = c.rest("GET", f"/bookmarks/{m['from']}?includeContent=false")
            if m["human_tags"]:
                names = [n for n in m["human_tags"] if n not in have_tags]
                if names:
                    s, _ = c.rest("POST", f"/bookmarks/{e['keep']}/tags",
                                  {"tags": [{"tagName": n, "attachedBy": "human"} for n in names]})
                    print(f"tags keep={e['keep'][:6]} from={m['from'][:6]} n={len(names)} status={s}")
                    have_tags |= set(names)
            for lid in m["lists"]:
                s, _ = c.rest("PUT", f"/lists/{lid}/bookmarks/{e['keep']}", {})
                print(f"list keep={e['keep'][:6]} status={s}")
            sn = (src.get("note") or "").strip()
            if sn and sn not in note:
                note = (note + "\n\n" if note else "") + "Merged duplicate note: " + sn
            if m["favourite"]:
                s, _ = c.rest("PATCH", f"/bookmarks/{e['keep']}", {"favourited": True})
        if note != (keep.get("note") or ""):
            s, _ = c.rest("PATCH", f"/bookmarks/{e['keep']}", {"note": note})
            print(f"note keep={e['keep'][:6]} status={s}")


def verify_merged(c: Client, plan):
    bad = 0
    for e in plan:
        s, keep = c.rest("GET", f"/bookmarks/{e['keep']}?includeContent=false")
        if s != 200:
            bad += 1
            continue
        names = {t["name"] for t in keep["tags"]}
        lists = set(list_membership(c, e["keep"]) or [])
        for m in e["moves"]:
            if not set(m["human_tags"]) <= names or not set(m["lists"]) <= lists:
                bad += 1
            s2, src = c.rest("GET", f"/bookmarks/{m['from']}?includeContent=false")
            sn = (src.get("note") or "").strip() if s2 == 200 else ""
            if sn and sn not in (keep.get("note") or ""):
                bad += 1
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", metavar="OUT")
    ap.add_argument("--merge", metavar="PLAN")
    ap.add_argument("--delete", metavar="PLAN")
    ap.add_argument("--yes", action="store_true")
    a = ap.parse_args()
    c = Client()

    if a.merge or a.delete:
        plan = json.loads(Path(a.merge or a.delete).read_text(encoding="utf-8"))["groups"]
    if a.merge:
        merge(c, plan)
        bad = verify_merged(c, plan)
        print(f"merge done, verification problems: {bad}")
        return 0 if bad == 0 else 1
    if a.delete:
        if not a.yes:
            print("refused: needs --yes")
            return 2
        if verify_merged(c, plan):
            print("ABORT: merge verification failed, nothing deleted")
            return 2
        deleted = 0
        for e in plan:
            for bid in e["delete"]:
                if bid == e["keep"]:
                    raise SystemExit("keep id in delete list")
                s, _ = c.rest("DELETE", f"/bookmarks/{bid}")
                deleted += s in (200, 204)
        print(f"deleted {deleted}")
        return 0

    out = Path(a.plan or "parts/TAG-dup-plan.json")
    plan = build_plan(c)
    obj = {
        "rule": "keep oldest; same host+path ignoring query/trailing slash (YouTube: same v)",
        "urls": len(plan),
        "extra_copies": sum(len(e["delete"]) for e in plan),
        "groups": plan,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, indent=1), encoding="utf-8")
    print(f"duplicate URLs={obj['urls']} extra copies={obj['extra_copies']} plan written ({out})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
