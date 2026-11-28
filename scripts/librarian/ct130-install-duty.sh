#!/bin/bash
# STAGED for the coordinator. Install the Librarian watch duty file on CT 130 (Hermes) and prove it arrived.
# Run on CT 130 as root, AFTER lane AGENTS reports "CT130 DONE". Lane AGENTS owns CT 130 until then.
# Usage: ct130-install-duty.sh /path/to/librarian-watch.md
# The source is _drafts/2026-11-28-big-push/KNOW/paperclip/docs/duties/librarian-watch.md (or the paperclip repo copy once merged).
# Idempotent. Undo: rm /opt/hermes-data/duties/librarian-watch.md (a .bak copy is kept if a different file existed).
set -euo pipefail
SRC="${1:?path to librarian-watch.md}"
DST=/opt/hermes-data/duties/librarian-watch.md
[ -s "$SRC" ] || { echo "refused: $SRC is missing or empty"; exit 2; }
grep -q "outside content" "$SRC" || { echo "refused: the file lacks the injection guard text"; exit 2; }
if [ -f "$DST" ] && ! cmp -s "$SRC" "$DST"; then cp -p "$DST" "$DST.bak-$(date +%Y%m%d%H%M)"; fi
install -o root -g root -m 644 "$SRC" "$DST"
want=$(sha256sum "$SRC" | cut -c1-12)
host=$(sha256sum "$DST" | cut -c1-12)
inside=$(docker exec hermes sha256sum /opt/data/duties/librarian-watch.md | cut -c1-12)
echo "source $want | host file $host | inside container $inside"
if [ "$want" = "$host" ] && [ "$want" = "$inside" ]; then
  echo "OK: the duty file arrived in the container"
else
  echo "FAILED: hashes differ (INC-20261125-01 pattern: check the mount)"
  exit 1
fi
# The Librarian's instructions must point at it. This only reports; changing instructions is a Paperclip step for lane AGENTS.
if grep -q "librarian-watch.md" /opt/hermes-data/duties/librarian.md 2>/dev/null; then
  echo "librarian.md already points at librarian-watch.md"
else
  echo "NOTE: add the pointer line to librarian.md (see the lane EDITS.md, paperclip entry)"
fi
