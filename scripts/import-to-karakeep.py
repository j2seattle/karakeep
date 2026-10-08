"""Import new link JSON from the laptop dump folder into Karakeep.

The Grok bot writes files to C:\\Users\\thedu\\discord-link-archive\\items.
This script lives in the karakeep repo. The checkpoint stays next to the dump,
so a later run skips files already imported.

Reads C:\\Users\\thedu\\.cursor\\mcps\\karakeep.env. Prints counts only.
Does not need sudo.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(r"C:\Users\thedu\discord-link-archive")
ITEMS = ROOT / "items"
ENV_FILE = Path(r"C:\Users\thedu\.cursor\mcps\karakeep.env")
STATE = ROOT / "import-state.json"
LIST_NAME = "Discord links"


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def request(base: str, key: str, method: str, path: str, body: dict | None = None) -> tuple[int, dict | list | None]:
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        base + path,
        data=data,
        method=method,
        headers={
            "Authorization": "Bearer " + key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read().decode()
            parsed = json.loads(raw) if raw else None
            return response.status, parsed
    except urllib.error.HTTPError as error:
        raw = error.read().decode(errors="replace")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"error": raw[:180]}
        return error.code, parsed


def main() -> int:
    env = load_env()
    base = env["KARAKEEP_URL"].rstrip("/")
    key = env["KARAKEEP_API_KEY"]
    state = {"listId": None, "done": {}}
    if STATE.exists():
        state = json.loads(STATE.read_text(encoding="utf-8"))

    if not state.get("listId"):
        status, payload = request(base, key, "POST", "/api/v1/lists", {"name": LIST_NAME, "icon": "discord"})
        if status not in (200, 201) or not isinstance(payload, dict) or "id" not in payload:
            print(f"list_create_failed status={status}")
            return 1
        state["listId"] = payload["id"]
        STATE.write_text(json.dumps(state), encoding="utf-8")

    files = sorted(ITEMS.glob("*.json"))
    created = tagged = listed = skipped = failed = 0
    for index, path in enumerate(files, start=1):
        item_id = path.stem
        if item_id in state["done"]:
            skipped += 1
            continue
        item = json.loads(path.read_text(encoding="utf-8"))
        content = item["content"]
        body = {
            "type": "link",
            "url": content["url"],
            "title": item.get("title") or None,
            "note": item.get("note") or None,
            "createdAt": item.get("createdAt"),
        }
        status, payload = request(base, key, "POST", "/api/v1/bookmarks", body)
        if status not in (200, 201) or not isinstance(payload, dict) or "id" not in payload:
            # Some servers reject fractional timestamps. Retry without createdAt.
            body.pop("createdAt", None)
            status, payload = request(base, key, "POST", "/api/v1/bookmarks", body)
        if status not in (200, 201) or not isinstance(payload, dict) or "id" not in payload:
            failed += 1
            print(f"fail {item_id} status={status}")
            continue
        bookmark_id = payload["id"]
        created += 1
        tag_ok = True
        for tag in item.get("tags") or []:
            tag_status, _ = request(
                base,
                key,
                "POST",
                f"/api/v1/bookmarks/{bookmark_id}/tags",
                {"tags": [{"tagName": tag}]},
            )
            if tag_status not in (200, 201):
                tag_ok = False
                print(f"tag_fail {item_id} status={tag_status}")
        if tag_ok:
            tagged += 1
        list_status, _ = request(
            base,
            key,
            "PUT",
            f"/api/v1/lists/{state['listId']}/bookmarks/{bookmark_id}",
            {},
        )
        if list_status not in (200, 201, 204):
            list_status, _ = request(
                base,
                key,
                "POST",
                f"/api/v1/lists/{state['listId']}/bookmarks",
                {"bookmarkId": bookmark_id},
            )
        if list_status in (200, 201, 204):
            listed += 1
        else:
            print(f"list_fail {item_id} status={list_status}")
        state["done"][item_id] = bookmark_id
        if index % 25 == 0:
            STATE.write_text(json.dumps(state), encoding="utf-8")
            print(f"progress {index}/{len(files)} created={created} skipped={skipped} failed={failed}")
        time.sleep(0.05)

    STATE.write_text(json.dumps(state), encoding="utf-8")
    print(
        f"done files={len(files)} created={created} skipped={skipped} "
        f"tagged={tagged} listed={listed} failed={failed}"
    )
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
