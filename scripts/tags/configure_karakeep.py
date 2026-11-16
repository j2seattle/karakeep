"""Karakeep settings for the tag vocabulary (run 2026-11-16-karakeep-window, lane TAG).

Idempotent. Default is a dry run that prints what would change.

  python configure_karakeep.py            dry run
  python configure_karakeep.py --apply    curated tags, custom prompt, design host rule, smart lists

Does not start the retag (see retag.py) and never deletes a bookmark.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kk_client import Client  # noqa: E402
import mapping  # noqa: E402

PROMPT_TEXT = (
    "Use only the curated tags. If none fits, add no tag. "
    "Never use a tag for the website a link is on."
)

DESIGN_HOSTS = ["codepen.io", "dribbble.com", "figma.com", "framer.com"]
RULE_NAME = "Host design sites"

# Smart lists: (name, icon, description, query). One per area in plan section 5.2.
NEW_LISTS = [
    ("AI and agents", "\U0001F916", "Agents, Claude, MCP, skills, models, local AI, prompts.",
     "#agents or #claude or #mcp or #skills or #llm-models or #local-ai or #prompts"),
    ("Images and video", "\U0001F3AC", "ComfyUI, image and video generation.",
     "#comfyui or #image-gen or #video-gen"),
    ("Home and hardware", "\U0001F3E0", "Home Assistant, homelab, self-hosted, hardware.",
     "#home-assistant or #homelab or #self-hosted or #hardware"),
    ("Lab areas", "\U0001F5A5", "Media server, networking, security, backups, monitoring, docs.",
     "#media-server or #networking or #security or #backups or #monitoring or #docs-knowledge"),
    ("Building", "\U0001F6E0", "Design, web, mobile, dev tools, GitHub repos.",
     "#design-ui or #web-dev or #mobile-dev or #dev-tools or #github-repo"),
    ("Trading and reading", "\U0001F4C8", "Trading and long reads.",
     "#trading or #reading"),
    ("Last 7 days", "\U0001F551", "Saved in the last seven days.", "age:<7d"),
    ("Untagged", "\U0001F3F7", "Bookmarks with no tag at all.", "-is:tagged"),
]

# Existing smart lists: name -> (new query, new description)
UPDATE_LISTS = {
    "Home Assistant": ("#home-assistant", "Links tagged home-assistant."),
    "Tools": ("#dev-tools", "Links tagged dev-tools."),
    "Twitter": ("#x", "Links tagged x (twitter merged into x)."),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    c = Client()
    act = "APPLY" if a.apply else "DRY"

    # 1. curated tags
    s, d = c.trpc_query("tags.list")
    tags = {t["name"]: t["id"] for t in d["tags"]}
    missing = [n for n in mapping.VOCAB if n not in tags]
    if missing:
        print(f"{act} curated: missing tags {missing} (run migrate_tags.py --apply first)")
        return 1
    want_ids = [tags[n] for n in mapping.VOCAB]
    s, settings = c.trpc_query("users.settings")
    cur_ids = settings.get("curatedTagIds") or []
    if set(cur_ids) != set(want_ids):
        print(f"{act} curated tags: {len(cur_ids)} -> {len(want_ids)}")
        if a.apply:
            s, r = c.trpc_mutation("users.updateSettings", {"curatedTagIds": want_ids})
            print(f"  status={s} {r if isinstance(r, dict) and '_error' in r else 'ok'}")
    else:
        print("curated tags already set")

    # 2. prompt
    s, prompts = c.trpc_query("prompts.list")
    have = [p for p in prompts if p["text"] == PROMPT_TEXT]
    if not have:
        print(f"{act} create prompt (all_tagging), {len(PROMPT_TEXT)} chars")
        if a.apply:
            s, r = c.trpc_mutation("prompts.create", {"text": PROMPT_TEXT, "appliesTo": "all_tagging"})
            print(f"  status={s} {r if isinstance(r, dict) and '_error' in r else 'ok'}")
    else:
        print("prompt already present")

    # 3. design host rule
    s, rules = c.trpc_query("rules.list")
    if not any(r["name"] == RULE_NAME for r in rules["rules"]):
        print(f"{act} create rule {RULE_NAME}: {DESIGN_HOSTS}")
        if a.apply:
            rule = {
                "name": RULE_NAME,
                "description": "Adds design-ui for design sites (WISH-913).",
                "enabled": True,
                "event": {"type": "bookmarkAdded"},
                "condition": {
                    "type": "or",
                    "conditions": [{"type": "urlContains", "str": h} for h in DESIGN_HOSTS],
                },
                "actions": [{"type": "addTag", "tagId": tags["design-ui"]}],
            }
            s, r = c.trpc_mutation("rules.create", rule)
            print(f"  status={s} {r if isinstance(r, dict) and '_error' in r else 'ok'}")
    else:
        print("rule already present")

    # 4. lists
    s, lists = c.rest("GET", "/lists")
    by_name = {l["name"]: l for l in lists["lists"]}
    for name, (query, desc) in UPDATE_LISTS.items():
        l = by_name.get(name)
        if l and l.get("query") != query:
            print(f"{act} update list {name}: {l.get('query')} -> {query}")
            if a.apply:
                s, _ = c.rest("PATCH", f"/lists/{l['id']}", {"query": query, "description": desc})
                print(f"  status={s}")
    for name, icon, desc, query in NEW_LISTS:
        if name in by_name:
            print(f"list {name} already exists")
            continue
        print(f"{act} create smart list {name}: {query}")
        if a.apply:
            s, r = c.rest("POST", "/lists", {"name": name, "icon": icon, "description": desc,
                                              "type": "smart", "query": query})
            print(f"  status={s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
