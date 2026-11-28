#!/usr/bin/env python3
"""Smoke test for scripts/bakeoff-local-embeddings.py with a fake Ollama and a temp database. No network, no real data."""
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "scripts", "bakeoff-local-embeddings.py")
DIM = 64


def vec(text):
    v = [0.0] * DIM
    for w in text.lower().split():
        v[int(hashlib.md5(w.encode()).hexdigest(), 16) % DIM] += 1.0
    return v


class Fake(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        out = json.dumps({"embeddings": [vec(t) for t in body["input"]]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):
        pass


def main():
    srv = HTTPServer(("127.0.0.1", 0), Fake)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    tmp = tempfile.mkdtemp()
    db = os.path.join(tmp, "db.db")
    c = sqlite3.connect(db)
    c.executescript("""create table bookmarks(id text, title text, note text);
      create table bookmarkLinks(id text, title text, description text);
      create table bookmarkTexts(id text, text text);""")
    docs = {"a1": "python library that draws diagrams and checks layout overlaps", "b2": "native photo app for iphone and mac",
            "c3": "face swap in live video", "d4": "cooking pasta at home"}
    for k, t in docs.items():
        c.execute("insert into bookmarks values (?,?,?)", (k, t, ""))
    c.commit()
    q = os.path.join(tmp, "q.json")
    json.dump({"queries": [{"q": "diagrams that check their layout", "expect": "a1", "note": "diag"},
                           {"q": "swap a face in live video", "expect": "c3", "note": "face"}]}, open(q, "w"))
    cur = os.path.join(tmp, "cur.json")
    json.dump({"diagrams that check their layout": ["x", "a1"], "swap a face in live video": ["c3"]}, open(cur, "w"))
    env = dict(os.environ, KK_DB=db, KK_CACHE=os.path.join(tmp, "cache"))
    run = lambda *extra: subprocess.run([sys.executable, SCRIPT, "--ollama", f"http://127.0.0.1:{srv.server_port}", "--model", "fake",
                                         "--queries", q, "--current", cur, "--force-quiet", *extra], env=env, capture_output=True, text=True)
    r = run()
    print(r.stdout, r.stderr)
    assert r.returncode == 0, r.returncode
    assert "documents: 4" in r.stdout and "dimension 64" in r.stdout
    assert "local plain 2/2" in r.stdout.replace("plain ", "plain ") or "local plain 2/5" in r.stdout
    assert "diag" in r.stdout and "face" in r.stdout
    assert oct(os.stat(os.path.join(tmp, "cache", "fake.json")).st_mode)[-3:] == "600" or os.name == "nt"
    bad = subprocess.run([sys.executable, SCRIPT, "--ollama", "http://openrouter.ai:11434", "--queries", q, "--force-quiet"], env=env, capture_output=True, text=True)
    assert bad.returncode == 2 and "not a lab Ollama host" in bad.stdout, bad.stdout
    clean = run("--clean")
    assert not os.path.exists(os.path.join(tmp, "cache", "fake.json")), clean.stdout
    print("smoke test OK: runs, ranks, refuses a non-lab host, cleans its cache")


if __name__ == "__main__":
    main()
