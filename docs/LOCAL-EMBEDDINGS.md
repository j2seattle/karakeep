---
title: Karakeep search modes and the local embedding bake-off
version: 1.0.0
status: active
last_edited_by: Claude Code (run 2026-11-28-big-push, lane KNOW)
last_edited_date: 2026-11-28
parent: ../README.md
children: []
siblings: [RUNBOOK.md, UPGRADE-0.35.0.md]
audience: internal
tags: [yingson-labs, karakeep, semantic-search, embeddings, runbook]
summary: "What was done for the approved Karakeep search plan (Hybrid mode, the local embedding test, the Library search box helper), the measured results for the current embedding model, and the staged steps to run the local test and switch."
doc_type: runbook
scope: service
service_name: karakeep
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: [ollama, ai-node]
depended_on_by: []
agent_context: true
permission_tier: read-only
last_verified: 2026-11-28
---

# Karakeep search modes and the local embedding bake-off

Plan: `lab-standards/docs/audits/2026-11-25-overnight/karakeep-semantic-search-tutorial.md` (approved, LAB-DEC-217: all three decisions yes). Written 2026-11-28 by lane KNOW of run 2026-11-28-big-push. Karakeep was not changed, not restarted and not snapshotted tonight. Live check 2026-11-28 00:5x: version 0.35.0, the four units active, `http://127.0.0.1:3000/` 307 (sign-in redirect) and `https://karakeep.yingson.com/signin` 200.

## Decision 1: Hybrid mode

No server setting exists for the default mode, so nothing changes in Karakeep. Jason picks Hybrid from the menu beside the search box when he wants meaning. Agents pass `hybrid` to `labread karakeep search "<text>" hybrid`. Whether the browser remembers the choice is still unverified (needs a browser).

Read-only check run 2026-11-28 through `labread` (ids only, no bookmark text printed): five described-in-other-words queries, rank of the bookmark that should come back (20 means not in the top 20):

| Query about | Semantic | Hybrid |
|---|---|---|
| Nightshift (unattended coding agent) | 1 | 2 |
| open-diagram (self-checking diagrams) | 1 | 1 |
| krea2 prompting skill | 1 | 12 |
| Verso for Immich | 3 | 3 |
| Deep-Live-Cam | 2 | 1 |

So the current OpenRouter model finds the expected bookmark in the top 3 for 5 of 5 in Semantic and 4 of 5 in Hybrid. Hybrid ranked the krea2 skill 12th because the keyword half has no matching words. That matches the tutorial: Hybrid adds noise when words differ, and Semantic is the better pick for "I do not know the words". Queries are in `config/bakeoff-queries.json`.

## Decision 2: local embedding test (staged, not run)

Why not run: ai-node VM 141 was busy on the night of 2026-11-28 and the run rules said leave it alone; CT 112 has no embedding model and its config is off limits. Facts found tonight:

- ai-node Ollama already lists `mxbai-embed-large:latest` (read of `/api/tags` from the Proxmox host).
- CT 136 can open a TCP connection to `192.168.30.81:11434` (checked from inside CT 136). This was unverified before.

To run, in a quiet window when the GPU is free (not 01:45 to 03:30, not 05:00):

1. Laptop: `python scripts/bakeoff-current-ranks.py --mode semantic --out current-semantic.json` (ids only).
2. Copy `scripts/bakeoff-local-embeddings.py`, `config/bakeoff-queries.json` and `current-semantic.json` to CT 136 (for example `pct push`).
3. On CT 136: `python3 bakeoff-local-embeddings.py --ollama http://192.168.30.81:11434 --model mxbai-embed-large --queries bakeoff-queries.json --current current-semantic.json`. It reads `db.db` read only, embeds about 1,040 bookmarks (title, description, note and saved text, an approximation of what Karakeep embeds), and prints ranks and speed. It refuses any host that is not a lab Ollama host, and refuses the backup window. Then `... --clean` deletes the vector cache.
4. Repeat with `--model qwen3-embedding:4b` if pulled (recommendation file `karakeep-local-model-recommendation.md`).

Pass rule: local model at least as good as current on the five queries, then Jason reads the top 5 of 10 of his own searches. Smoke test with a fake Ollama and a temporary database: `python tests/test_bakeoff_smoke.py` (passes).

## Switching (only after the pass, staged)

`scripts/switch-embeddings-local.sh --go` backs up the env file, checks the model answers with the expected dimension, sets `EMBEDDING_OPENAI_BASE_URL`, `EMBEDDING_OPENAI_API_KEY` (the placeholder word `ollama`, not a secret), `EMBEDDING_TEXT_MODEL` and `EMBEDDING_DIMENSIONS`, restarts workers then web, and prints health. Then Admin, Background Jobs, regenerate embeddings. Needs a snapshot first (`pre_<purpose>_YYYYMMDD_expYYYYMMDD`).

Unverified until a scratch copy proves it: that Karakeep accepts Ollama's `/v1/embeddings` through `EMBEDDING_OPENAI_BASE_URL`; that a changed dimension is accepted without clearing the Meilisearch vectors index by hand. Do not switch production before that.

Note: tagging still sends page text to OpenRouter (finding INT-01, unchanged). Switching embeddings does not fix that. Tagging on a local model is a separate step in `karakeep-local-model-recommendation.md`.

## Decision 3: Library search box (WISH-1390)

Command Center belongs to lane CC. This repo holds the reference helper they can port: `scripts/search_filters.py` turns "immich things I bookmarked this week" into `immich after:2026-11-23` and picks keyword or Hybrid mode (`python scripts/search_filters.py --test`, 6 cases pass). Checked live: `after:` includes the named day (a bookmark saved 2026-11-24 is found by `after:2026-11-24` and not by `after:2026-11-25`). The box spec is in `_drafts/2026-11-28-big-push/KNOW/CC-SPEC-library-search-box.md`.
