---
title: CURSOR — karakeep
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-08
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
last_verified: 2026-10-08
---

# CURSOR — karakeep

**Slug:** `karakeep` · **CT 136** · `192.168.30.33` · **R3**

## Now

Karakeep 0.33.2 is up. Tailscale only — no Cloudflare. Discord down and up confirmed. UniFi group and icon done. First account exists. Laptop env file is `C:\Users\thedu\.cursor\mcps\karakeep.env` with blank secret values until Jason fills them.

## Do not

- Put `/opt/karakeep_data` on NFS. It is better-sqlite3.
- Print `/etc/karakeep/karakeep.env` or `/root/karakeep-lxc-root.password`.
- Reuse CT 109 or CT 131.
- Do not add a Cloudflare hostname. Jason decided Tailscale only on 2026-10-08.

## Next

Jason pastes the Dashlane values into `C:\Users\thedu\.cursor\mcps\karakeep.env` and says the file is filled. Do not paste them in chat. Gate 7 restore is still open.
