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

**Slug:** `karakeep` · **CT 136** · `192.168.30.33` · **R2**

## Now

Karakeep 0.33.2 is up. `https://karakeep.yingson.com/signin` returns 200. NPM host 53. Kuma 115 and 116 are beating. Homarr tile is on YingsonDash. PBS snapshot `ct/136/2026-10-08T17:30:26Z` succeeded. `ssh karakeep` returns `jason`.

## Do not

- Put `/opt/karakeep_data` on NFS. It is better-sqlite3.
- Print `/etc/karakeep/karakeep.env` or `/root/karakeep-lxc-root.password`.
- Reuse CT 109 or CT 131.
- Open a Cloudflare hostname without Jason's decision.

## Next

Jason: UniFi group `Proxmox Lab` and icon, first account, Dashlane, Gitea repo `jason/karakeep` (token lacks `write:user`), empty GitHub `j2seattle/karakeep`, confirm `#alerts`, say whether Cloudflare should be on.
