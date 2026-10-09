---
title: CLAUDE — karakeep
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-08
parent: README.md
children: []
siblings: [CURSOR.md, ARCHITECTURE.md, README.md]
audience: internal
tags: [yingson-labs, karakeep, agent-briefing]
summary: "Entry point for AI agents working in karakeep. Rules of engagement and the lab-standards sync receipt."
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

# CLAUDE.md — karakeep

> **`lab-standards` is the source of truth for this repo's documentation.** This repo is a child of it.

**Slug:** `karakeep` · **Host:** CT 136 / 192.168.30.33 · **Tier:** `read-only`

## Lab-standards sync

| Field | Value |
|---|---|
| **Last reconciled** | 2026-10-08 |
| **lab-standards commit** | `6a449af` |
| **Reconciled by** | Cursor Grok |
| **Open items flowing up** | Gate 7 restore. Gate 8 baselines. Read-only Cursor wrapper. |

At session start: `git -C ../lab-standards log -1 --format=%h`. If the SHA moved past `6a449af`, read `lab-standards/CHANGELOG.md` since that commit before changing this service.

## Read order

1. `lab-standards/LAB-DOC-CONTRACT.md`
2. [CURSOR.md](CURSOR.md)
3. [ARCHITECTURE.md](ARCHITECTURE.md)
4. `lab-standards/SERVICE-INVENTORY.md`
5. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) · [BASELINES.md](BASELINES.md) · [docs/RUNBOOK.md](docs/RUNBOOK.md)

## Conflict rule

If two sources disagree, stop and ask Jason. Do not guess.

## Bookmarks are personal data

Do not dump bookmark titles, URLs, or page archives into chat to "check that it works." A healthy check is HTTP status plus `systemctl is-active` on the three units.

## Environment

| Field | Value |
|---|---|
| Proxmox | `ssh proxmox` = `jason@192.168.30.209`, key `id_ed25519_lab` |
| This guest | `ssh karakeep` after the Host block exists |
| Web | `https://karakeep.yingson.com` → `192.168.30.33:3000` |
| GitHub mirror | `github.com/j2seattle/karakeep` — Gitea push mirror, confirmed 2026-10-08. Push Gitea only. |
| Tagging | Ollama CT 112, `llama3.1:8b`, guest env only. UI: User Settings → AI Settings. |
