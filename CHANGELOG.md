---
title: Changelog — karakeep
version: 0.1.0
status: active
last_edited_by: Claude Code
last_edited_date: 2026-11-01
parent: README.md
children: []
siblings: [ARCHITECTURE.md, CURSOR.md, CLAUDE.md]
audience: internal
tags: [yingson-labs, karakeep, changelog]
summary: "Prepend-only history for the karakeep service repo."
doc_type: changelog
scope: service
service_name: karakeep
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: [proxmox, adguard, npm, tailscale, pbs]
depended_on_by: []
agent_context: true
permission_tier: read-only
last_verified: 2026-11-01
---

# Changelog

All notable changes to **karakeep** are documented here. Prepend only.

---

## [Unreleased]

- [OPS] **PAT-01, SEC-03 and SEC-10 closed (2026-11-01).** Jason ran the upgrade to 0.34.1 (Node 24, Meilisearch 1.56.0, bookmarks 953 before and after). The units now run as `karakeep`, Chromium has its sandbox on, and NPM host 53 sends three security headers. SEC-03 caused an outage of about 3 minutes, from about 20:55 to 20:58 PST: the release files were not readable by other users, and the stage test had only checked one file. A throwaway bookmark crawled and was deleted. Findings now 52 of 67 fixed. `no decision`.

- [OPS] **Service Review fix run, docs lane (2026-11-01).** The 2026-10-12 working tree edits were checked against the live guest and committed: the guest env file names `OPENAI_BASE_URL=https://openrouter.ai/api/v1`, `INFERENCE_TEXT_MODEL` and `INFERENCE_IMAGE_MODEL` both `google/gemini-2.5-flash-lite`, and no `OLLAMA_BASE_URL`; the Ollama text in these docs is now history only. Added the privacy note that page text goes to OpenRouter and on to Google, measured `BASELINES.md` (one sample), four units in the health checks, the version check, the swap note, the OpenRouter vault reference (existence in Dashlane not confirmed), and the sync receipt (`3827b40`). The 26 or 25 curated tag count is still open (DOC-04). `no decision`.

- [OPS] **Alloy log shipping recorded (2026-10-24).** CT 136 ships its journal to Loki (CT 138) through Alloy (apt package held at 1.21.2), labels `host=karakeep`, `service=karakeep`. Proxmox exporter and the Grafana lab dashboards also cover CT 136. Docs only. `no decision`.

- [OPS] Removed `tools` from the curated tags (26 to 25) and detached the AI `tools` tag on 489 bookmarks that already had another tag (Jason, 2026-10-12). The Tools list went from 582 to 93. Human `tools` tags stayed. Cards whose only real tag was `tools` stayed.

- [OPS] Deleted 1,876 tag names that were on zero bookmarks (Jason, 2026-10-12). 162 tags remain, each on at least one bookmark. The 26 curated tags were kept. No bookmark lost a tag.

- [OPS] The whole library was retagged with OpenRouter `google/gemini-2.5-flash-lite` on 2026-10-12. 844 bookmarks finished with tagging status success. OpenRouter usage for the run was about $0.16. 71 bookmarks still carry an AI tag outside the 26 curated names. Human tags were left in place. Empty tag names from the old Ollama pass are still in the tag list.

- [OPS] Tagging now uses OpenRouter `google/gemini-2.5-flash-lite` for text and images. The key lives in the laptop file `karakeep-openrouter.env` and in `/etc/karakeep/karakeep.env` on CT 136. Thinking stays off. A test of eight existing items on 2026-10-12 stayed inside the 26 curated tags, including one image that had failed under Ollama. Auto-tagging is on again for new saves. The rest of the library was not retagged. Summarization stays off.

- [OPS] Earlier on 2026-10-12, before the OpenRouter test in the entry above, auto-tagging was off (Jason). It was switched on again later that day. Summarization stays off. Tag style stays lowercase with hyphens, and the 26 curated tags stay selected. Smart list **Twitter** (`#x or #twitter`) is in the sidebar and holds 336 bookmarks. Tag cleanup waits. Ollama `llama3.1:8b` stays the configured model until a stronger one is attached.

- [OPS] Auto-tagging is on, summarization is off, and tag style is lowercase with hyphens. Jason's 26 curated tags were kept. Host rules tag github, x/twitter, reddit, and youtube on new bookmarks. Smart lists GitHub, Tools, and Agents follow those tags. A full retag was queued through Ollama on 2026-10-08.

- [OPS] Auto-tagging uses Ollama on CT 112. The guest env holds `OPENAI_BASE_URL` and `INFERENCE_TEXT_MODEL=llama3.1:8b`. The API key field is the literal word `ollama`. AI Settings stays hidden until `karakeep-web` is restarted. Curated tags keep new links in the existing categories.

- [OPS] The Discord-link importer lives in `scripts/import-to-karakeep.py`. It still reads new files from `C:\Users\thedu\discord-link-archive\items`.

- [OPS] Laptop `karakeep.env` is filled. GitHub mirror was already configured; Jason saw the Gitea commits on `j2seattle/karakeep`. Agents push Gitea only. Official MCP stays unwired.
- [OPS] Jason confirmed Discord down/up, UniFi, and the first login. Tailscale only. Laptop `karakeep.env` created with blank secrets. Readiness R3.
