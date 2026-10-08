---
title: Changelog — karakeep
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-08
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
last_verified: 2026-10-08
---

# Changelog

All notable changes to **karakeep** are documented here. Prepend only.

---

## [Unreleased]

- [OPS] The Discord-link importer lives in `scripts/import-to-karakeep.py`. It still reads new files from `C:\Users\thedu\discord-link-archive\items`.

- [OPS] Laptop `karakeep.env` is filled. GitHub mirror was already configured; Jason saw the Gitea commits on `j2seattle/karakeep`. Agents push Gitea only. Official MCP stays unwired.
- [OPS] Jason confirmed Discord down/up, UniFi, and the first login. Tailscale only. Laptop `karakeep.env` created with blank secrets. Readiness R3.
