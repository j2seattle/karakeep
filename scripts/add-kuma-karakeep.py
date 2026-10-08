#!/usr/bin/env python3
"""Add Karakeep DNS + IP monitors on CT 100. Restart Uptime Kuma after.

Notification id 1 is Yingson Labs Discord Alerts. Do not attach id 2.
"""
import datetime
import sqlite3

DB = "/opt/uptime-kuma/data/kuma.db"
TEMPLATE_ID = 69
NOTIFICATION_ID = 1
TAG_YINGSON = 9

MONITORS = [
    {
        "name": "karakeep (DNS)",
        "url": "https://karakeep.yingson.com/",
        "type": "http",
        "keyword": None,
        "description": "CT136 Karakeep via NPM. Discord #alerts only.",
        "tags": (TAG_YINGSON,),
    },
    {
        "name": "karakeep (IP)",
        "url": "http://192.168.30.33:3000/",
        "type": "http",
        "keyword": None,
        "description": "CT136 Karakeep direct port 3000. Discord #alerts only.",
        "tags": (TAG_YINGSON,),
    },
]


def main() -> None:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    template = dict(cur.execute("SELECT * FROM monitor WHERE id=?", (TEMPLATE_ID,)).fetchone())
    template.pop("id")
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    created = []

    for spec in MONITORS:
        existing = cur.execute(
            "SELECT id FROM monitor WHERE name=? AND active=1", (spec["name"],)
        ).fetchone()
        if existing:
            print(f"exists id={existing[0]} {spec['name']}")
            mid = existing[0]
        else:
            row = dict(template)
            row["name"] = spec["name"]
            row["url"] = spec["url"]
            row["type"] = spec["type"]
            row["keyword"] = spec["keyword"]
            row["description"] = spec["description"]
            row["created_date"] = now
            row["active"] = 1
            row["user_id"] = 1
            cols = list(row.keys())
            cur.execute(
                f"INSERT INTO monitor ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                [row[c] for c in cols],
            )
            mid = cur.lastrowid
            print(f"inserted id={mid} {spec['name']} {spec['url']}")
            created.append(mid)

        linked = cur.execute(
            "SELECT 1 FROM monitor_notification WHERE monitor_id=? AND notification_id=?",
            (mid, NOTIFICATION_ID),
        ).fetchone()
        if not linked:
            cur.execute(
                "INSERT INTO monitor_notification (monitor_id, notification_id) VALUES (?,?)",
                (mid, NOTIFICATION_ID),
            )
            print(f"  notify {NOTIFICATION_ID}")

        for tag_id in spec["tags"]:
            tagged = cur.execute(
                "SELECT 1 FROM monitor_tag WHERE monitor_id=? AND tag_id=?",
                (mid, tag_id),
            ).fetchone()
            if not tagged:
                cur.execute(
                    "INSERT INTO monitor_tag (monitor_id, tag_id, value) VALUES (?,?,?)",
                    (mid, tag_id, ""),
                )

    conn.commit()
    conn.close()
    print(f"done created={created}")


if __name__ == "__main__":
    main()
