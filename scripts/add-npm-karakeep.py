#!/usr/bin/env python3
"""Add the LAN-only NPM proxy host for Karakeep. Run on CT 107.

Clone of NPM host 47 (grafana.yingson.com): wildcard cert npm-1, Force SSL,
HTTP/2, block exploits, websockets on. No Cloudflare.

Then: nginx -t && nginx -s reload
"""
import datetime
import json
import re
import sqlite3
from pathlib import Path

DB = Path("/data/database.sqlite")
CONF_DIR = Path("/data/nginx/proxy_host")
TEMPLATE_ID = 47
TEMPLATE_DOMAIN = "grafana.yingson.com"
TEMPLATE_HOST = "192.168.30.151"
TEMPLATE_PORT = 3000

DOMAIN = "karakeep.yingson.com"
FORWARD_HOST = "192.168.30.33"
FORWARD_PORT = 3000
NOW = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def main() -> None:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    existing = cur.execute(
        "SELECT id FROM proxy_host WHERE domain_names LIKE ? AND is_deleted=0",
        (f"%{DOMAIN}%",),
    ).fetchone()
    if existing:
        hid = existing[0]
        print(f"exists id={hid} {DOMAIN}")
    else:
        row = dict(cur.execute("SELECT * FROM proxy_host WHERE id=?", (TEMPLATE_ID,)).fetchone())
        row.pop("id")
        row.update(
            created_on=NOW,
            modified_on=NOW,
            domain_names=json.dumps([DOMAIN]),
            forward_host=FORWARD_HOST,
            forward_port=FORWARD_PORT,
            enabled=1,
            is_deleted=0,
        )
        cols = list(row.keys())
        cur.execute(
            f"INSERT INTO proxy_host ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
            [row[c] for c in cols],
        )
        hid = cur.lastrowid
        print(f"inserted id={hid} {DOMAIN} -> {FORWARD_HOST}:{FORWARD_PORT}")

    template_conf = (CONF_DIR / f"{TEMPLATE_ID}.conf").read_text(encoding="utf-8")
    conf = template_conf.replace(TEMPLATE_DOMAIN, DOMAIN)
    conf = conf.replace(f'"{TEMPLATE_HOST}"', f'"{FORWARD_HOST}"')
    conf = re.sub(
        rf"set \$port\s+{TEMPLATE_PORT};",
        f"set $port           {FORWARD_PORT};",
        conf,
    )
    conf = conf.replace(f"proxy-host-{TEMPLATE_ID}_", f"proxy-host-{hid}_")
    for needle in (TEMPLATE_DOMAIN, TEMPLATE_HOST, f"proxy-host-{TEMPLATE_ID}_"):
        if needle in conf:
            raise SystemExit(f"template residue {needle!r} left in generated conf")
    path = CONF_DIR / f"{hid}.conf"
    path.write_text(conf, encoding="utf-8")
    print(f"wrote {path}")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
