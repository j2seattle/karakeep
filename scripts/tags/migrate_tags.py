"""Tag migration for Karakeep (WISH-913, run 2026-11-16-karakeep-window, lane TAG).

  python migrate_tags.py                      dry run (default), writes --report
  python migrate_tags.py --apply --expect R   apply; aborts if a fresh plan differs from report R
  python migrate_tags.py --undo <export dir>  put every bookmark's tags back to the export

Rules live in mapping.py. Prints counts only, never a key or a URL.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kk_client import Client  # noqa: E402
import mapping  # noqa: E402


def fetch_bookmarks(c: Client):
    return list(c.paged("/bookmarks?includeContent=false", "bookmarks", "limit=100"))


def current_tags(b):
    return [(t["name"], t["attachedBy"]) for t in b.get("tags", [])]


def build_plan(bookmarks):
    """Per bookmark: detach and attach lists of (name, attachedBy)."""
    plan = []
    before, after, after_by, before_by = Counter(), Counter(), Counter(), Counter()
    for b in bookmarks:
        cur = current_tags(b)
        for n, by in cur:
            before[n] += 1
            before_by[(n, by)] += 1
        want = mapping.desired_tags(cur)
        curset = set(cur)
        wantset = set(want.items())
        detach = sorted(curset - wantset)
        attach = sorted(wantset - curset)
        for n, by in want.items():
            after[n] += 1
            after_by[(n, by)] += 1
        if detach or attach:
            plan.append({"id": b["id"], "detach": [list(x) for x in detach], "attach": [list(x) for x in attach]})
    return plan, before, after, before_by, after_by


def report_obj(bookmarks, plan, before, after, before_by, after_by):
    table = []
    for n, cnt in before.items():
        new, rule = mapping.target(n)
        table.append({"old": n, "new": new, "rule": rule, "bookmarks": cnt})
    table.sort(key=lambda r: (-r["bookmarks"], r["old"]))
    return {
        "bookmarks": len(bookmarks),
        "bookmarks_changed": len(plan),
        "tag_links_before": sum(before.values()),
        "tag_links_after": sum(after.values()),
        "distinct_tags_before": len(before),
        "distinct_tags_after": len(after),
        "before": dict(sorted(before.items(), key=lambda x: (-x[1], x[0]))),
        "after": dict(sorted(after.items(), key=lambda x: (-x[1], x[0]))),
        "after_by_attached": {f"{n}|{by}": v for (n, by), v in sorted(after_by.items())},
        "mapping_table": table,
        "attach_ops": sum(len(p["attach"]) for p in plan),
        "detach_ops": sum(len(p["detach"]) for p in plan),
        "tags_to_delete_when_empty": sorted(n for n in before if n not in mapping.KEEP_NAMES),
        "plan": plan,
    }


def list_tags(c: Client):
    s, d = c.trpc_query("tags.list")
    if not isinstance(d, dict) or "tags" not in d:
        raise RuntimeError(f"tags.list failed status={s}")
    return d["tags"]


def ensure_vocab(c: Client):
    names = {t["name"] for t in list_tags(c)}
    created = []
    for n in mapping.VOCAB + [mapping.SRC_TAG]:
        if n not in names:
            s, r = c.trpc_mutation("tags.create", {"name": n})
            if s != 200 or (isinstance(r, dict) and "_error" in r):
                raise RuntimeError(f"tags.create {n} failed status={s}")
            created.append(n)
    return created


def _push(c: Client, bid, rm_ids, add):
    ok = True
    if rm_ids:
        s, _ = c.rest("DELETE", f"/bookmarks/{bid}/tags", {"tags": [{"tagId": x} for x in rm_ids]})
        ok = ok and s in (200, 204)
    for by in ("human", "ai"):
        names = [n for n, b2 in add if b2 == by]
        if names:
            s, _ = c.rest(
                "POST",
                f"/bookmarks/{bid}/tags",
                {"tags": [{"tagName": n, "attachedBy": by} for n in names]},
            )
            ok = ok and s in (200, 201)
    return ok


def apply_plan(c: Client, bookmarks, plan):
    tagid = {}
    for b in bookmarks:
        for t in b["tags"]:
            tagid[(b["id"], t["name"], t["attachedBy"])] = t["id"]
    done = failed = 0
    for i, p in enumerate(plan, 1):
        bid = p["id"]
        ids = [tagid[(bid, n, by)] for n, by in p["detach"]]
        if _push(c, bid, ids, [tuple(x) for x in p["attach"]]):
            done += 1
        else:
            failed += 1
            print(f"op_failed bookmark={bid}")
        if i % 100 == 0:
            print(f"progress {i}/{len(plan)} done={done} failed={failed}")
    return done, failed


def delete_empty_old_tags(c: Client, old_names: set):
    deleted = 0
    for t in list_tags(c):
        if t["name"] in old_names and t["numBookmarks"] == 0:
            s2, _ = c.rest("DELETE", f"/tags/{t['id']}")
            if s2 in (200, 204):
                deleted += 1
    return deleted


def undo(c: Client, export_dir: Path):
    exp = json.loads((export_dir / "bookmarks-tags.json").read_text(encoding="utf-8"))
    live = {b["id"]: b for b in fetch_bookmarks(c)}
    restored = failed = 0
    for e in exp:
        b = live.get(e["id"])
        if not b:
            continue
        want = {(t["name"], t["attachedBy"]) for t in e["tags"]}
        cur = {(t["name"], t["attachedBy"]): t["id"] for t in b["tags"]}
        rm = [cur[k] for k in cur if k not in want]
        add = [k for k in want if k not in cur]
        if not rm and not add:
            continue
        if _push(c, b["id"], rm, add):
            restored += 1
        else:
            failed += 1
    print(f"undo restored={restored} failed={failed}")
    return failed == 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="default")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--undo", metavar="EXPORT_DIR")
    ap.add_argument("--report", default="parts/TAG-dry-run.json")
    ap.add_argument("--expect", help="dry-run report the apply must match")
    a = ap.parse_args()

    c = Client()
    if a.undo:
        return 0 if undo(c, Path(a.undo)) else 1

    bms = fetch_bookmarks(c)
    plan, before, after, before_by, after_by = build_plan(bms)
    rep = report_obj(bms, plan, before, after, before_by, after_by)
    print(
        f"bookmarks={rep['bookmarks']} changed={rep['bookmarks_changed']} "
        f"links {rep['tag_links_before']} -> {rep['tag_links_after']} "
        f"tags {rep['distinct_tags_before']} -> {rep['distinct_tags_after']} "
        f"attach_ops={rep['attach_ops']} detach_ops={rep['detach_ops']}"
    )

    if not a.apply:
        out = Path(a.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rep, indent=1), encoding="utf-8")
        print(f"dry run only, report written ({out})")
        return 0

    if not a.expect:
        print("refused: --apply needs --expect <dry-run report>")
        return 2
    exp = json.loads(Path(a.expect).read_text(encoding="utf-8"))
    if exp["after"] != rep["after"] or exp["plan"] != rep["plan"]:
        print("ABORT: fresh plan differs from the dry-run report")
        return 2

    created = ensure_vocab(c)
    print(f"vocab tags created: {len(created)}")
    done, failed = apply_plan(c, bms, plan)
    print(f"applied bookmarks done={done} failed={failed}")
    time.sleep(1)
    deleted = delete_empty_old_tags(c, set(rep["tags_to_delete_when_empty"]))
    print(f"empty old tags deleted: {deleted}")

    fresh = fetch_bookmarks(c)
    cnt = Counter(t["name"] for b in fresh for t in b["tags"])
    want = Counter(rep["after"])
    diff = {k: (cnt.get(k, 0), want.get(k, 0)) for k in set(cnt) | set(want) if cnt.get(k, 0) != want.get(k, 0)}
    if diff:
        print(f"MISMATCH tags differ from dry run: {len(diff)}")
        print(json.dumps(dict(list(diff.items())[:20])))
        return 3
    print("MATCH: per-tag counts equal the dry run")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
