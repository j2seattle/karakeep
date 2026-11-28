#!/usr/bin/env python3
"""Karakeep embedding bake-off, step 2 of 2: rank the same bookmarks with a LOCAL embedding model.

Runs ON CT 136 (reads db.db read only, talks to the lab's own Ollama). It changes nothing in Karakeep:
no setting, no vector, no restart. Bookmark text goes only to the Ollama host you name, which must be a
lab host (ai-node 192.168.30.81:11434 or CT 112). The script refuses any other address, so text cannot
reach a cloud model by a typing mistake.

Not run yet: ai-node VM 141 was busy on 2026-11-28 and the run charter said leave it alone. CT 136 can open a TCP
connection to ai-node port 11434 (checked 2026-11-28). Run it in a quiet window when the GPU is free.

Usage on CT 136 (as root or the karakeep user):
  python3 bakeoff-local-embeddings.py --ollama http://192.168.30.81:11434 --model mxbai-embed-large \
      --queries bakeoff-queries.json --current current-semantic.json
  python3 bakeoff-local-embeddings.py ... --clean        # delete the vector cache afterwards

Prints only ids, ranks and timings. No title or text. The cache /var/tmp/kk-bakeoff/<model>.json holds vectors
derived from bookmark text, so it is mode 600 and --clean removes it.
The document text is title, description, note and saved text (an approximation of what Karakeep embeds:
Karakeep also embeds the crawled page body, which lives in an asset file this script does not read).
"""
import argparse
import datetime
import json
import math
import os
import sqlite3
import sys
import time
import urllib.request
import zoneinfo

DB = os.environ.get("KK_DB", "/opt/karakeep_data/db.db")
CACHE_DIR = os.environ.get("KK_CACHE", "/var/tmp/kk-bakeoff")
ALLOWED_HOSTS = {"192.168.30.81", "localhost", "127.0.0.1"} | set(filter(None, os.environ.get("KK_EXTRA_HOSTS", "").split(",")))  # ai-node and local; add CT 112 (DHCP, address not recorded) with KK_EXTRA_HOSTS
MAX_CHARS = 1500  # mxbai-embed-large reads about 512 tokens (from memory, unverified)
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "  # mxbai model card prefix (from memory, unverified); both forms are tried


def quiet_window() -> bool:
    now = datetime.datetime.now(zoneinfo.ZoneInfo("America/Los_Angeles"))
    m = now.hour * 60 + now.minute
    return (105 <= m < 210) or (295 <= m < 305)  # 01:45 to 03:30 and about 05:00


def post(url: str, body: dict) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def embed(base: str, model: str, texts: list) -> list:
    return post(base.rstrip("/") + "/api/embed", {"model": model, "input": texts, "truncate": True})["embeddings"]


def load_docs() -> list:
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    rows = c.execute(
        """SELECT b.id, COALESCE(b.title,''), COALESCE(l.title,''), COALESCE(l.description,''), COALESCE(b.note,''), COALESCE(t.text,'')
           FROM bookmarks b LEFT JOIN bookmarkLinks l ON l.id = b.id LEFT JOIN bookmarkTexts t ON t.id = b.id"""
    ).fetchall()
    docs = []
    for bid, bt, lt, ld, note, text in rows:
        s = " ".join(x for x in (bt or lt, ld, note, text) if x).strip()
        if s:
            docs.append((bid, s[:MAX_CHARS]))
    return docs


def norm(v):
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ollama", required=True)
    ap.add_argument("--model", default="mxbai-embed-large")
    ap.add_argument("--queries", required=True)
    ap.add_argument("--current", help="current.json from bakeoff-current-ranks.py (ids only)")
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--limit-docs", type=int, default=0, help="embed only the first N bookmarks (smoke test)")
    ap.add_argument("--force-quiet", action="store_true", help="run inside the backup window (do not)")
    a = ap.parse_args()

    host = a.ollama.split("//", 1)[-1].split(":")[0]
    if host not in ALLOWED_HOSTS:
        print(f"refused: {host} is not a lab Ollama host. Bookmark text must stay in the lab.")
        return 2
    if quiet_window() and not a.force_quiet:
        print("refused: inside the backup window (01:45 to 03:30) or about 05:00 Pacific")
        return 2

    os.makedirs(CACHE_DIR, mode=0o700, exist_ok=True)
    cache = os.path.join(CACHE_DIR, a.model.replace("/", "_").replace(":", "_") + ".json")
    if a.clean:
        if os.path.exists(cache):
            os.remove(cache)
        print("cache removed")
        return 0

    docs = load_docs()
    if a.limit_docs:
        docs = docs[: a.limit_docs]
    print(f"documents: {len(docs)}")
    vecs = {}
    if os.path.exists(cache):
        vecs = json.load(open(cache))
    todo = [d for d in docs if d[0] not in vecs]
    t0 = time.time()
    for i in range(0, len(todo), 16):
        batch = todo[i:i + 16]
        out = embed(a.ollama, a.model, [t for _, t in batch])
        for (bid, _), v in zip(batch, out):
            vecs[bid] = norm(v)
        if (i // 16) % 8 == 0:
            print(f"  embedded {min(i + 16, len(todo))} of {len(todo)} ({time.time() - t0:.0f}s)", flush=True)
        if os.path.exists(os.path.join(CACHE_DIR, "STOP")):
            print("STOP file found, pausing here")
            break
    fd = os.open(cache, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(vecs, f)
    dim = len(next(iter(vecs.values())))
    per_doc = (time.time() - t0) / max(len(todo), 1)
    print(f"dimension {dim}, {per_doc * 1000:.0f} ms per document")

    queries = json.load(open(a.queries))["queries"]
    current = json.load(open(a.current)) if a.current else {}
    print(f"\n{'query note':24} {'local plain':>12} {'local prefix':>13} {'current':>9}   (rank of the expected bookmark, 20 = not in top 20)")
    wins = {"plain": 0, "prefix": 0, "current": 0}
    for item in queries:
        ranks = {}
        for label, text in (("plain", item["q"]), ("prefix", QUERY_PREFIX + item["q"])):
            qv = norm(embed(a.ollama, a.model, [text])[0])
            scored = sorted(((sum(x * y for x, y in zip(qv, v)), bid) for bid, v in vecs.items()), reverse=True)[:20]
            ids = [b for _, b in scored]
            ranks[label] = ids.index(item["expect"]) + 1 if item["expect"] in ids else 20
        cur_ids = current.get(item["q"], [])
        ranks["current"] = cur_ids.index(item["expect"]) + 1 if item["expect"] in cur_ids else 20
        print(f"{item['note']:24} {ranks['plain']:>12} {ranks['prefix']:>13} {ranks['current']:>9}")
        for k in wins:
            if ranks[k] <= 3:
                wins[k] += 1
    print(f"\nexpected bookmark in top 3: local plain {wins['plain']}/{len(queries)}, local prefix {wins['prefix']}/{len(queries)}, current {wins['current']}/{len(queries)}")
    print("Pass rule (plan): switch only if local is at least as good as current on these five AND you read the top 5 of 10 of your own searches. Then follow the steps in docs/LOCAL-EMBEDDINGS.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
