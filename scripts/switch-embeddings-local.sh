#!/bin/sh
# STAGED, NOT RUN. Move Karakeep embeddings from OpenRouter to a local Ollama model (tutorial decision 2).
# Run only after: (1) scripts/bakeoff-local-embeddings.py passed (docs/LOCAL-EMBEDDINGS.md), (2) a snapshot of CT 136
# (`<purpose>_YYYYMMDD_expYYYYMMDD`), (3) a window outside 01:45-03:30 and 05:00 Pacific, (4) a scratch copy proved that
# Karakeep accepts Ollama's /v1/embeddings (unverified today). Runs inside CT 136 as root. Prints names and states, never values.
# Usage: switch-embeddings-local.sh --go [model] [dimensions]      defaults: mxbai-embed-large 1024
# Undo:  cp -p /etc/karakeep/karakeep.env.bak-local-embed /etc/karakeep/karakeep.env; systemctl restart karakeep-workers karakeep-web
#        then Admin, Background Jobs, regenerate embeddings (the old 1536-dimension vectors are rebuilt from db.db).
set -eu
[ "${1:-}" = "--go" ] || { echo "refused: pass --go after reading the header"; exit 2; }
MODEL="${2:-mxbai-embed-large}"
DIMS="${3:-1024}"
OLLAMA="http://192.168.30.81:11434"
ENV=/etc/karakeep/karakeep.env
BAK=/etc/karakeep/karakeep.env.bak-local-embed
H=$(TZ=America/Los_Angeles date +%H%M)
if [ "$H" -ge 0145 ] && [ "$H" -lt 0330 ]; then echo "refused: backup window"; exit 2; fi
if [ "$H" -ge 0455 ] && [ "$H" -lt 0510 ]; then echo "refused: Kopia window"; exit 2; fi
# The model must exist and answer, and its dimension must match, before anything changes.
GOT=$(curl -s -m 60 "$OLLAMA/v1/embeddings" -H 'Content-Type: application/json' -d "{\"model\":\"$MODEL\",\"input\":\"hello\"}" \
  | python3 -c 'import sys,json; print(len(json.load(sys.stdin)["data"][0]["embedding"]))' 2>/dev/null || echo 0)
echo "model $MODEL answers with dimension $GOT (expected $DIMS)"
[ "$GOT" = "$DIMS" ] || { echo "refused: dimension mismatch or no answer. Nothing changed."; exit 3; }
[ -f "$BAK" ] || cp -p "$ENV" "$BAK"
set_kv() {
  if grep -q "^$1=" "$ENV"; then sed -i "s|^$1=.*|$1=$2|" "$ENV"; else printf '%s=%s\n' "$1" "$2" >> "$ENV"; fi
}
set_kv EMBEDDING_OPENAI_BASE_URL "$OLLAMA/v1"
set_kv EMBEDDING_OPENAI_API_KEY ollama
set_kv EMBEDDING_TEXT_MODEL "$MODEL"
set_kv EMBEDDING_DIMENSIONS "$DIMS"
echo "names now:"; grep -oE '^[A-Z_][A-Z0-9_]*=' "$ENV" | tr '\n' ' '; echo
stat -c 'mode %a owner %U' "$ENV"
systemctl restart karakeep-workers
sleep 5
systemctl restart karakeep-web
sleep 20
systemctl is-active karakeep-web karakeep-workers karakeep-browser meilisearch | tr '\n' ' '; echo
curl -s -o /dev/null -w 'health %{http_code}\n' http://127.0.0.1:3000/api/health
curl -s -o /dev/null -w 'signin %{http_code}\n' http://127.0.0.1:3000/signin
echo "NEXT: Admin, Background Jobs, regenerate embeddings. Watch karakeep_embeddings_pending fall and karakeep_semantic_search_ok return to 1."
