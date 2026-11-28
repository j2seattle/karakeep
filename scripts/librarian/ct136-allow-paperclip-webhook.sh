#!/bin/bash
# STAGED. Let Karakeep's webhook worker call Paperclip on the LAN. Run inside CT 136 as root.
# Why: Karakeep sends webhooks through the same URL guard as its crawler (apps/workers/network.ts, v0.35.0). That guard refuses
# private addresses unless the host is listed in CRAWLER_ALLOWED_INTERNAL_HOSTNAMES. Without this line a webhook to
# 192.168.30.34 fails with "Refusing to access disallowed IP address". Only the exact Paperclip address is added.
# Run only when: (1) lane AGENTS finished and the Aegis intake gate is live, (2) the Paperclip routine with a webhook trigger exists,
# (3) a CT 136 snapshot `pre_<purpose>_YYYYMMDD_expYYYYMMDD` exists, (4) not 01:45-03:30 or about 05:00 Pacific.
# Undo: cp -p /etc/karakeep/karakeep.env.bak-librarian /etc/karakeep/karakeep.env; systemctl restart karakeep-workers
set -eu
ENV=/etc/karakeep/karakeep.env
BAK=/etc/karakeep/karakeep.env.bak-librarian
HOSTIP=192.168.30.34
H=$(TZ=America/Los_Angeles date +%H%M)
if [ "$((10#$H))" -ge 145 ] && [ "$((10#$H))" -lt 330 ]; then echo "refused: backup window"; exit 2; fi
if [ "$((10#$H))" -ge 455 ] && [ "$((10#$H))" -lt 510 ]; then echo "refused: Kopia window"; exit 2; fi
timeout 4 bash -c "</dev/tcp/$HOSTIP/3100" || { echo "refused: cannot reach $HOSTIP:3100"; exit 3; }
[ -f "$BAK" ] || cp -p "$ENV" "$BAK"
if grep -q '^CRAWLER_ALLOWED_INTERNAL_HOSTNAMES=' "$ENV"; then
  grep -q "^CRAWLER_ALLOWED_INTERNAL_HOSTNAMES=.*$HOSTIP" "$ENV" || sed -i "s|^CRAWLER_ALLOWED_INTERNAL_HOSTNAMES=\(.*\)|CRAWLER_ALLOWED_INTERNAL_HOSTNAMES=\1,$HOSTIP|" "$ENV"
else
  printf 'CRAWLER_ALLOWED_INTERNAL_HOSTNAMES=%s\n' "$HOSTIP" >> "$ENV"
fi
echo "names now:"; grep -oE '^[A-Z_][A-Z0-9_]*=' "$ENV" | tr '\n' ' '; echo
stat -c 'mode %a owner %U' "$ENV"
systemctl restart karakeep-workers
sleep 15
systemctl is-active karakeep-web karakeep-workers karakeep-browser meilisearch | tr '\n' ' '; echo
curl -s -o /dev/null -w 'health %{http_code}\n' http://127.0.0.1:3000/api/health
curl -s -o /dev/null -w 'signin %{http_code}\n' http://127.0.0.1:3000/signin
