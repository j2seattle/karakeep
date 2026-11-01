#!/bin/bash
# Nightly logical backup for Karakeep (CT 136). The app stays running.
# db.db is copied with the SQLite online backup API, so no live file copy.
# queue.db is a work queue and Meilisearch is rebuilt from db.db, so neither is saved.
# Saved: the database copy, /etc/karakeep (holds secrets, mode 700 stage), and the assets folder.
set -euo pipefail
export KOPIA_PASSWORD KOPIA_CHECK_FOR_UPDATES=false
KOPIA_PASSWORD="$(cat /etc/kopia/user.password)"
CFG=/root/.config/kopia/repository.config
stage=/var/backups/kopia/karakeep
rm -rf "$stage"
install -d -m 700 "$stage"

python3 - /opt/karakeep_data/db.db "$stage/db.sqlite3" <<'PY'
import sqlite3, sys
src = sqlite3.connect("file:%s?mode=ro" % sys.argv[1], uri=True)
dst = sqlite3.connect(sys.argv[2])
with dst:
    src.backup(dst)
ok = dst.execute("pragma integrity_check").fetchone()[0]
n = dst.execute("select count(*) from bookmarks").fetchone()[0]
src.close(); dst.close()
if ok != "ok" or n < 1:
    sys.exit("database copy failed its check")
PY
cp -a /etc/karakeep "$stage/etc-karakeep"
chmod -R go-rwx "$stage"

kopia snapshot create --config-file="$CFG" --tags service:karakeep "$stage"
kopia snapshot create --config-file="$CFG" --tags service:karakeep /opt/karakeep_data/assets
