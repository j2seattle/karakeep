#!/bin/sh
# MON-02 (2026-11-01): read-only deeper health check for Karakeep, as a textfile metric.
# Runs as root from /etc/cron.d/karakeep-health every 5 minutes on CT 136.
# Reads queue.db and db.db with mode=ro. Prints counts and times only, never a URL or a title.
# Alloy's node exporter textfile collector picks up /var/lib/yingson-telemetry/karakeep.prom.
set -eu
DATA=/opt/karakeep_data
OUT=/var/lib/yingson-telemetry/karakeep.prom
TMP="$OUT.tmp"
python3 - "$DATA" > "$TMP" <<'PY'
import sqlite3, sys, time
d = sys.argv[1]
print("# HELP karakeep_queue_tasks Queued tasks in queue.db by queue and status.")
print("# TYPE karakeep_queue_tasks gauge")
ok = 1
try:
    q = sqlite3.connect("file:%s/queue.db?mode=ro" % d, uri=True, timeout=5)
    for queue, status, n in q.execute("select queue, status, count(*) from tasks group by queue, status"):
        print('karakeep_queue_tasks{queue="%s",status="%s"} %d' % (queue, status, n))
    row = q.execute("select min(createdAt) from tasks where status in ('pending','pending_retry')").fetchone()
    print("# HELP karakeep_queue_oldest_pending_timestamp_seconds Creation time of the oldest waiting task, 0 when none.")
    print("# TYPE karakeep_queue_oldest_pending_timestamp_seconds gauge")
    print("karakeep_queue_oldest_pending_timestamp_seconds %d" % (row[0] or 0))
    b = sqlite3.connect("file:%s/db.db?mode=ro" % d, uri=True, timeout=5)
    last = b.execute("select max(crawledAt) from bookmarkLinks").fetchone()[0] or 0
    total = b.execute("select count(*) from bookmarks").fetchone()[0]
    print("# HELP karakeep_last_crawl_timestamp_seconds Time of the newest finished crawl.")
    print("# TYPE karakeep_last_crawl_timestamp_seconds gauge")
    print("karakeep_last_crawl_timestamp_seconds %d" % last)
    print("# HELP karakeep_bookmarks_total Bookmarks in the library.")
    print("# TYPE karakeep_bookmarks_total gauge")
    print("karakeep_bookmarks_total %d" % total)
except Exception:
    ok = 0
print("# HELP karakeep_health_probe_success 1 when the databases could be read.")
print("# TYPE karakeep_health_probe_success gauge")
print("karakeep_health_probe_success %d" % ok)
print("# HELP karakeep_health_probe_timestamp_seconds When this check last ran.")
print("# TYPE karakeep_health_probe_timestamp_seconds gauge")
print("karakeep_health_probe_timestamp_seconds %d" % int(time.time()))
PY
chmod 644 "$TMP"
mv "$TMP" "$OUT"
