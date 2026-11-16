#!/bin/sh
# Enable Karakeep semantic search with OpenRouter embeddings (window 2026-11-16, plan KARAKEEP-WINDOW.md section 4).
# Runs inside CT 136 as root: pct push then pct exec. Prints names and states only, never values.
# Undo: cp /etc/karakeep/karakeep.env.bak-20261116 /etc/karakeep/karakeep.env; systemctl restart karakeep-workers karakeep-web
set -eu
ENV=/etc/karakeep/karakeep.env
BAK=/etc/karakeep/karakeep.env.bak-20261116
[ -f "$BAK" ] || cp -p "$ENV" "$BAK"
set_kv() {
  if grep -q "^$1=" "$ENV"; then sed -i "s|^$1=.*|$1=$2|" "$ENV"; else printf '%s=%s\n' "$1" "$2" >> "$ENV"; fi
}
set_kv EMBEDDING_ENABLE_AUTO_INDEXING true
set_kv SEMANTIC_SEARCH_ENABLED true
set_kv EMBEDDING_TEXT_MODEL openai/text-embedding-3-small
set_kv EMBEDDING_DIMENSIONS 1536
set_kv EMBEDDING_NUM_WORKERS 2
echo "names now:"; grep -oE '^[A-Z_][A-Z0-9_]*=' "$ENV" | tr '\n' ' '; echo
stat -c 'mode %a owner %U' "$ENV"
du -sh /var/lib/meilisearch 2>/dev/null | awk '{print "meili before " $1}'
systemctl restart karakeep-workers
sleep 5
systemctl restart karakeep-web
sleep 20
systemctl is-active karakeep-web karakeep-workers karakeep-browser meilisearch | tr '\n' ' '; echo
curl -s -o /dev/null -w 'health %{http_code}\n' http://127.0.0.1:3000/api/health
curl -s -o /dev/null -w 'signin %{http_code}\n' http://127.0.0.1:3000/signin
