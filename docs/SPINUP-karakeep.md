---
title: Spin-up checklist — karakeep
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-08
parent: ARCHITECTURE.md
children: []
siblings: [RUNBOOK.md]
audience: internal
tags: [yingson-labs, karakeep, runbook]
summary: "Appendix A checklist for the 2026-10-08 Karakeep bring-up. Open boxes are still open."
doc_type: runbook
scope: service
service_name: karakeep
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: [proxmox, adguard, npm, uptime-kuma, homarr, pbs]
depended_on_by: []
agent_context: true
permission_tier: read-only
last_verified: 2026-10-08
---

# Service Spin-Up Checklist: karakeep

**Date Started:** 2026-10-08
**Date Completed:** open
**Service Description:** Bookmark and page archive for Jason.
**Initial Release Tag:** not tagged yet

## Phase 0 — Pre-Provisioning

- [x] LXC booted; UniFi has seen the MAC (`search_clients` returned `bc:24:11:bc:f5:e7`)
- [x] Alias `karakeep-LXC` set (`update_dhcp_reservation`). `create_dhcp_reservation` then returned `api.err.MacUsed`
- [ ] `get_dhcp_reservation` still returns not found — re-check in the UniFi UI
- [x] Added to `Proxmox Lab` group (Jason, 2026-10-08)
- [x] Custom icon set (Jason, 2026-10-08)
- [x] IP recorded: `192.168.30.33`

## Phase 1 — Provisioning

- [x] CT 136 created. Debian 13, unprivileged, 2 vCPU, 4096 MB, 15 GB, `onboot: 1`
- [x] Reachable at `192.168.30.33`
- [x] NAS bind mount — N/A. SQLite must stay on the local disk
- [x] `lab-init.sh` — N/A. The community script covered packages, hostname, and timezone. Recorded in ARCHITECTURE §2
- [x] `jason` user and laptop Host block
- [x] `ssh -o BatchMode=yes karakeep whoami` returns `jason`
- [x] Guest outbound Gitea key — N/A. This guest does not pull the repo

## Phase 2 — DNS & Access

- [x] Explicit AdGuard rewrite `karakeep.yingson.com` → `192.168.30.182`, enabled, and `dig` returns `.30.182`
- [x] NPM proxy host 53 and a trusted certificate (`curl` without `-k` returned 200)
- [x] `https://karakeep.yingson.com/signin` loads
- [x] External access decided. Tailscale only. No Cloudflare (Jason, 2026-10-08)

## Phase 3 — Version Control

- [x] Gitea repo `jason/karakeep` — `main` and tag `v0.1` pushed 2026-10-08
- [ ] GitHub `j2seattle/karakeep` push mirror. The repo exists. This laptop's `gh` is `j2wavepoint` and got 403. Jason adds the mirror in Gitea → Settings → Mirror Settings. No sudo.
- [ ] Push mirror
- [ ] v0.1 tag

## Phase 4 — Monitoring

- [x] DNS monitor 115
- [x] IP monitor 116
- [x] Kuma restarted. Both heartbeats `200 - OK` at 2026-10-08 17:31 UTC
- [x] Discord down + recovery seen by Jason (2026-10-08)

## Phase 5 — Dashboard

- [x] Homarr app `vpqz4utg8qdw1mvuyhge23kz` on YingsonDash (not Lab-Dashboard)
- [x] LAN ping URL `http://192.168.30.33:3000/`
- [x] Native integration — N/A. Homarr has no Karakeep kind

## Phase 6 — Secrets & Backup

- [ ] Root password moved from `/root/karakeep-lxc-root.password` on the Proxmox host into Dashlane, then the file deleted
- [x] Admin password in Dashlane (Jason, 2026-10-08)
- [x] Cursor API key in Dashlane
- [x] Laptop `C:\Users\thedu\.cursor\mcps\karakeep.env` created with blank values. Jason pastes the secrets there.
- [ ] Cursor MCP — `needs-wrapper`, not wired
- [x] PBS backup finished successfully. Snapshot `ct/136/2026-10-08T17:30:26Z`
- [ ] Restore tested — not this pass

## Phase 7 — Sign-off

- [ ] Standards conformance has no blank boxes
- [ ] Inventory readiness updated from R1 only when the gates actually pass
