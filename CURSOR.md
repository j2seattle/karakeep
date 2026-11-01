---
title: CURSOR — karakeep
version: 0.1.0
status: active
last_edited_by: Claude Code
last_edited_date: 2026-11-01
parent: README.md
children: []
siblings: [CLAUDE.md, ARCHITECTURE.md, CHANGELOG.md]
audience: internal
tags: [yingson-labs, karakeep, agent-briefing]
summary: "Agent briefing for karakeep. Current state of the CT 136 bring-up."
doc_type: agent-briefing
scope: service
service_name: karakeep
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: [proxmox, adguard, npm, tailscale, pbs]
depended_on_by: []
agent_context: true
permission_tier: read-only
last_verified: 2026-11-01
---

# CURSOR — karakeep

**Slug:** `karakeep` · **CT 136** · `192.168.30.33` · **R3**

## Now

Karakeep 0.33.2 is up. Tailscale only, including the iOS app. Discord links are imported. Auto-tagging is on for new saves (2026-10-12), via OpenRouter `google/gemini-2.5-flash-lite` for text and images. Thinking is off. Summarization is off. Tag style is lowercase hyphens, and the 26 curated tags are still selected. An eight-item test that day stayed inside those tags, and the rest of the library was retagged the same day. 71 bookmarks still have an AI tag outside the 26. Host rules cover github, x/twitter, reddit, and youtube on new saves. Smart lists: GitHub, Tools, Agents, Twitter (`#x or #twitter`, 336). `C:\Users\thedu\.cursor\mcps\karakeep.env` is the Cursor key. `karakeep-openrouter.env` is the OpenRouter key. Do not print either. Publish by pushing Gitea `jason/karakeep`. GitHub follows that push.

## Do not

- Put `/opt/karakeep_data` on NFS. It is better-sqlite3.
- Print `/etc/karakeep/karakeep.env` or `/root/karakeep-lxc-root.password`.
- Put inference settings in the laptop `karakeep.env`. The guest file is the one the units read.
- Reuse CT 109 or CT 131.
- Do not add a Cloudflare hostname. Jason decided Tailscale only on 2026-10-08.

## Next

Gate 7 restore is still open. Do not add `@karakeep/mcp` to Cursor. Its tools include delete.
