"""Start the AI retag of the whole library (admin.reRunInferenceOnAllBookmarks, type=tag).

Dry run by default. --apply enqueues one tagging job per bookmark (low priority).
The tagging worker deletes every AI-attached tag on a bookmark, then attaches
the new set from the curated tags. Human tags are untouched.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kk_client import Client

ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
a = ap.parse_args()
c = Client()
s, st = c.rest("GET", "/users/me/stats")
print(f"bookmarks={st['numBookmarks']}")
if not a.apply:
    print("dry run: would call admin.reRunInferenceOnAllBookmarks {type: tag, status: all}")
    sys.exit(0)
s, r = c.trpc_mutation("admin.reRunInferenceOnAllBookmarks", {"type": "tag", "status": "all"})
print(f"status={s} {r if isinstance(r, dict) and '_error' in r else 'ok'}")
