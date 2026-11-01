---
title: CLAUDE — karakeep
version: 0.1.0
status: active
last_edited_by: Claude Code
last_edited_date: 2026-11-01
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
last_verified: 2026-11-01
---

# CLAUDE.md — karakeep

> **`lab-standards` is the source of truth for this repo's documentation.** This repo is a child of it.

**Slug:** `karakeep` · **Host:** CT 136 / 192.168.30.33 · **Tier:** `read-only`

## Lab-standards sync

| Field | Value |
|---|---|
| **Last reconciled** | 2026-11-01 |
| **lab-standards commit** | `3827b40` |
| **Reconciled by** | Claude Code (fix run) |
| **Open items flowing up** | Gate 7 restore. Read-only Cursor wrapper. OpenRouter dependency edges and `TOOLS.yaml` `lab_use` (returned to the coordinator, 2026-11-01). |

At session start: `git -C ../lab-standards log -1 --format=%h`. If the SHA moved past `3827b40`, read `lab-standards/CHANGELOG.md` since that commit before changing this service.

## Read order

1. `lab-standards/LAB-DOC-CONTRACT.md`
2. [CURSOR.md](CURSOR.md)
3. [ARCHITECTURE.md](ARCHITECTURE.md)
4. `lab-standards/SERVICE-INVENTORY.md`
5. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) · [BASELINES.md](BASELINES.md) · [docs/RUNBOOK.md](docs/RUNBOOK.md)

## Conflict rule

If two sources disagree, stop and ask Jason. Do not guess.

## Bookmarks are personal data

Do not dump bookmark titles, URLs, or page archives into chat to "check that it works." A healthy check is HTTP status plus `systemctl is-active` on the four units (`karakeep-web`, `karakeep-workers`, `karakeep-browser`, `meilisearch`).

## Environment

| Field | Value |
|---|---|
| Proxmox | `ssh proxmox` = `jason@192.168.30.209`, key `id_ed25519_lab` |
| This guest | `ssh karakeep` after the Host block exists |
| Web | `https://karakeep.yingson.com` → `192.168.30.33:3000` |
| GitHub mirror | `github.com/j2seattle/karakeep` — Gitea push mirror, confirmed 2026-10-08. Push Gitea only. |
| Tagging | OpenRouter `google/gemini-2.5-flash-lite` for text and images. Auto-tagging on for new saves (2026-10-12), summarization off, lowercase hyphens, 26 curated tags. Host rules on new bookmarks. Smart lists GitHub, Tools, Agents, Twitter. |


## Session-end gate

- [ ] A choice in the changelog or other docs has a decision in this same session, or the changelog says `no decision` (LAB-DEC-035)
