---
title: Baselines — karakeep
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-08
parent: ARCHITECTURE.md
children: []
siblings: [TROUBLESHOOTING.md, CHANGELOG.md]
audience: ops
tags: [yingson-labs, karakeep, baselines]
summary: "Healthy-state ranges for karakeep. Nothing measured yet."
doc_type: baselines
scope: service
service_name: karakeep
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: [proxmox]
depended_on_by: []
agent_context: true
permission_tier: read-only
last_verified: 2026-10-08
---

# Baselines — Karakeep

**Slug:** `karakeep` · **Last full review:** 2026-10-08

Every value here is observed. `not yet measured` means we have not measured it.

## Measurement environment

| Field | Value |
|---|---|
| **Host** | CT 136, 2 vCPU / 4 GB RAM / 15 GB disk |
| **App version** | 0.33.2 |
| **Typical load** | not yet measured |
| **Measured over** | not yet measured |

## Health endpoint

- **Normal range:** not yet measured
- **Warning threshold:** not yet measured
- **Critical threshold:** not yet measured
- **Measurement source:** `curl -w '%{time_total}' -o /dev/null -s http://127.0.0.1:3000/` inside CT 136
- **Known false-positive conditions:** not yet measured
- **Last verified:** not yet measured

## Resource ranges

| Metric | Idle | Warning | Critical |
|---|---|---|---|
| CPU | not yet measured | not yet measured | not yet measured |
| RAM | not yet measured | not yet measured | not yet measured |
| Disk | not yet measured | not yet measured | not yet measured |
| Swap | not yet measured | not yet measured | not yet measured |

## Notes

Gate 8 is open. Do not invent a threshold from the 4 GB allocation.
