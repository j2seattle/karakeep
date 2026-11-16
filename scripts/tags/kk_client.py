"""Small Karakeep client shared by the scripts in this folder.

Reads KARAKEEP_URL and KARAKEEP_API_KEY from the laptop env file. Never prints
either value. REST under /api/v1, tRPC under /api/trpc (superjson envelope).
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ENV_FILE = Path(r"C:\Users\thedu\.cursor\mcps\karakeep.env")


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


class Client:
    def __init__(self) -> None:
        env = load_env()
        self.base = env["KARAKEEP_URL"].rstrip("/")
        self._key = env["KARAKEEP_API_KEY"]

    def _req(self, method: str, path: str, body=None, retries: int = 3):
        data = None if body is None else json.dumps(body).encode()
        headers = {
            "Authorization": "Bearer " + self._key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        for attempt in range(retries):
            req = urllib.request.Request(self.base + path, data=data, method=method, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=90) as r:
                    raw = r.read().decode()
                    return r.status, (json.loads(raw) if raw else None)
            except urllib.error.HTTPError as e:
                raw = e.read().decode(errors="replace")
                try:
                    parsed = json.loads(raw)
                except json.JSONDecodeError:
                    parsed = {"error": raw[:200]}
                if e.code >= 500 and attempt < retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                return e.code, parsed
            except (urllib.error.URLError, TimeoutError):
                if attempt < retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise
        return 0, None

    def rest(self, method: str, path: str, body=None):
        return self._req(method, "/api/v1" + path, body)

    def trpc_query(self, proc: str, payload=None):
        path = "/api/trpc/" + proc
        if payload is not None:
            path += "?input=" + urllib.parse.quote(json.dumps({"json": payload}))
        s, d = self._req("GET", path)
        return s, _unwrap(d)

    def trpc_mutation(self, proc: str, payload=None):
        s, d = self._req("POST", "/api/trpc/" + proc, {"json": payload})
        return s, _unwrap(d)

    def paged(self, path: str, key: str, params: str = "limit=100"):
        """Walk a REST list with nextCursor."""
        cursor = None
        while True:
            q = path + ("&" if "?" in path else "?") + params
            if cursor:
                q += "&cursor=" + urllib.parse.quote(cursor)
            s, d = self.rest("GET", q)
            if s != 200:
                raise RuntimeError(f"GET {path} status={s}")
            for item in d[key]:
                yield item
            cursor = d.get("nextCursor")
            if not cursor:
                return


def _unwrap(d):
    if isinstance(d, dict) and "result" in d:
        return d["result"].get("data", {}).get("json")
    if isinstance(d, dict) and "error" in d:
        e = d["error"]
        msg = (e.get("json") or e).get("message") if isinstance(e, dict) else str(e)
        return {"_error": str(msg)[:300]}
    return d
