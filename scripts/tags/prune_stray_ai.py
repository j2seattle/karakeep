"""Remove AI-attached tags that are outside the curated vocabulary, then delete the emptied tags.

The model sometimes ignores "use only the curated tags" (about 3 percent of bookmarks after the
2026-11-16 retag). Human tags are never touched.

  python prune_stray_ai.py            dry run (default)
  python prune_stray_ai.py --apply
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kk_client import Client  # noqa: E402
import mapping  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    c = Client()
    bms = list(c.paged("/bookmarks?includeContent=false", "bookmarks", "limit=100"))
    keep = set(mapping.VOCAB)
    stray = Counter()
    todo = []
    for b in bms:
        ids = [t["id"] for t in b["tags"] if t["attachedBy"] == "ai" and t["name"] not in keep]
        for t in b["tags"]:
            if t["attachedBy"] == "ai" and t["name"] not in keep:
                stray[t["name"]] += 1
        if ids:
            todo.append((b["id"], ids))
    print(f"bookmarks with stray AI tags: {len(todo)}; stray links: {sum(stray.values())}; distinct: {len(stray)}")
    if not a.apply:
        print("dry run: nothing written")
        return 0
    ok = 0
    for bid, ids in todo:
        s, _ = c.rest("DELETE", f"/bookmarks/{bid}/tags", {"tags": [{"tagId": x} for x in ids]})
        ok += s in (200, 204)
    print(f"detached on {ok}/{len(todo)} bookmarks")
    s, d = c.trpc_query("tags.list")
    deleted = 0
    for t in d["tags"]:
        if t["name"] in stray and t["numBookmarks"] == 0:
            s2, _ = c.rest("DELETE", f"/tags/{t['id']}")
            deleted += s2 in (200, 204)
    print(f"empty stray tags deleted: {deleted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
