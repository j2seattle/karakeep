---
title: Architecture — karakeep
version: 0.1.0
status: active
last_edited_by: Claude Code
last_edited_date: 2026-11-01
parent: README.md
children: []
siblings: [CHANGELOG.md, CURSOR.md, BASELINES.md, TROUBLESHOOTING.md]
audience: internal
tags: [yingson-labs, karakeep, architecture]
summary: "Karakeep bookmark archive on CT 136: host, network, data layout, and how the lab reaches it."
doc_type: architecture
scope: service
service_name: karakeep
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: [proxmox, adguard, npm, tailscale, pbs]
depended_on_by: []
agent_context: true
permission_tier: read-only
last_verified: 2026-11-01
---

# Architecture — Karakeep

**Slug:** `karakeep` · **Status:** `active` · **Host:** CT 136 / 192.168.30.33 · **Readiness:** R3

## Table of Contents

1. [Overview](#1-overview)
2. [Host & Runtime](#2-host--runtime)
3. [Network & Access](#3-network--access)
4. [Components](#4-components)
5. [Dependencies](#5-dependencies)
6. [Data Flow](#6-data-flow)
7. [Storage & Layout](#7-storage--layout)
8. [Configuration & Environment](#8-configuration--environment)
9. [Deployment](#9-deployment)
10. [Backup & Recovery](#10-backup--recovery)
11. [Monitoring & Health](#11-monitoring--health)
12. [API & Automation Profile](#12-api--automation-profile)
13. [Security](#13-security)
14. [Known Issues & Constraints](#14-known-issues--constraints)
15. [Operational Procedures](#15-operational-procedures)
16. [Open Items & Planned Changes](#16-open-items--planned-changes)

## 1. Overview

Karakeep (formerly Hoarder) saves links, page archives, and screenshots. This lab copy is for Jason. No lab service depends on it. The laptop import script and the Cursor key call its API.

The app is Karakeep **0.33.2**, installed by the Proxmox VE community script on 2026-10-08. It is not a Docker Compose stack.

## 2. Host & Runtime

| Field | Value |
|---|---|
| Guest | CT 136, unprivileged |
| Hostname | `karakeep` (bare name) |
| OS | Debian 13 (`debian-13-standard_13.1-2`) |
| CPU / RAM / disk | 2 vCPU / 4096 MB / 15 GB `local-lvm` |
| Swap | 512 MB |
| Start at boot | `onboot: 1` |
| Features | `nesting=1,keyctl=1` |
| Timezone | `America/Los_Angeles` |
| Nameserver | `192.168.30.242` (AdGuard) |
| SSH | `ssh karakeep` after the laptop Host block. `pct exec` from `jason@proxmox` is the fallback. |

Resources are the helper script's tested size, not the lab default of 2 GB / 8 GB. Chromium and Meilisearch live in this guest, and the install builds the Next.js app here.

`lab-init.sh` was not run. The helper script applied hostname, timezone, packages, and SSH keys for root. The `jason` user is a separate step and is not done by that script.

## 3. Network & Access

| Path | Target |
|---|---|
| LAN name | `https://karakeep.yingson.com` (NPM host 53 → `192.168.30.33:3000`) |
| Direct | `http://192.168.30.33:3000` |
| Off-LAN | Tailscale to the LAN name. No Cloudflare hostname. Jason confirmed that on 2026-10-08. |
| UniFi | alias `karakeep-LXC`, fixed IP `192.168.30.33`, MAC `bc:24:11:bc:f5:e7` |

AdGuard rewrite `karakeep.yingson.com` → `192.168.30.182` is `enabled: true` and `dig` against AdGuard returns that address.

Same-host checks must use `http://127.0.0.1:3000`. `/etc/hosts` maps `karakeep.yingson.com` to the guest itself, so that name on the guest hits nothing on port 443.

Proxmox Lab group and the client icon were set by Jason on 2026-10-08.

## 4. Components

| Unit | Role | Listen |
|---|---|---|
| `karakeep-web` | Next.js UI | `0.0.0.0:3000` |
| `karakeep-workers` | Crawl, archive, search indexing | no public port |
| `karakeep-browser` | Headless Chromium | `127.0.0.1:9222` |
| `meilisearch` | Search index | `127.0.0.1:7700` |

Workers start after the browser and Meilisearch. The web unit starts after the workers.

## 5. Dependencies

| Depends on | For |
|---|---|
| `proxmox` | The guest |
| `adguard` | The name `karakeep.yingson.com` |
| `npm` | TLS on that name |
| `tailscale` | Off-LAN admin reach |
| `pbs` | Nightly guest snapshots (job is `all`) |

Nothing depends on `karakeep`. Blast radius is Low.

OpenRouter (`https://openrouter.ai/api/v1`, model `google/gemini-2.5-flash-lite`) is used for auto-tagging only. The archive, crawl, and screenshots keep working if OpenRouter is down. Tagging jobs wait until it answers. Page text for a tag call leaves the guest.

**Privacy.** Saving a bookmark sends the page text to OpenRouter, and OpenRouter passes it on to the model provider (Google, for `google/gemini-2.5-flash-lite`). The image model is set to the same model, so images can go the same way. The exact fields sent are not verified. The 844 bookmarks retagged on 2026-10-12 went the same way. Whether private or signed-in pages must stay out of OpenRouter is Jason's decision and is still open (review finding INT-01).

Other edges: the guest ships its journal to Loki (CT 138) through Alloy. The laptop import script (`scripts/import-to-karakeep.py`) and the Cursor key call the REST API. Whether Hermes calls Karakeep is not verified.

*Not applicable — NAS.* See §7.

## 6. Data Flow

A browser opens `https://karakeep.yingson.com`. NPM terminates TLS and forwards HTTP to `192.168.30.33:3000`. The web process reads and writes SQLite under `/opt/karakeep_data`. Saving a URL hands the job to the workers, which ask Chromium on localhost:9222 for a snapshot and send text to Meilisearch on localhost:7700.

No request leaves the guest except the page the user asked to archive, the tagging call to OpenRouter, and DNS/NTP for the guest itself.

## 7. Storage & Layout

| Path | What |
|---|---|
| `/opt/karakeep` | Application source and build (0.33.2) |
| `/opt/karakeep_data` | SQLite database, assets, screenshots |
| `/etc/karakeep/karakeep.env` | Runtime environment. Mode should stay restricted. Contains secrets. |
| `/etc/systemd/system/karakeep-*.service` | The three units |

SQLite (`better-sqlite3`) stays on the CT disk. NFS locking breaks it. The same directory holds the archives, so they stay with the database and are covered by the PBS guest snapshot rather than a NAS bind mount.

## 8. Configuration & Environment

The live file is `/etc/karakeep/karakeep.env`. Names are listed in [.env.example](.env.example). Values are not in git.

| Key | Value |
|---|---|
| `NEXTAUTH_URL` | `https://karakeep.yingson.com` |
| `NEXTAUTH_SECRET` | Session secret. Generated at install. |
| `DATA_DIR` | `/opt/karakeep_data` |
| `MEILI_ADDR` / `MEILI_MASTER_KEY` | Local search |
| `BROWSER_WEB_URL` | `http://127.0.0.1:9222` |
| `OPENAI_API_KEY` | OpenRouter key. Laptop copy is `C:\Users\thedu\.cursor\mcps\karakeep-openrouter.env`. Dashlane `vault://dashlane/yingson-labs/karakeep/openrouter-api-key`. |
| `OPENAI_BASE_URL` | `https://openrouter.ai/api/v1` |
| `INFERENCE_TEXT_MODEL` | `google/gemini-2.5-flash-lite` |
| `INFERENCE_IMAGE_MODEL` | `google/gemini-2.5-flash-lite` |

The laptop file `C:\Users\thedu\.cursor\mcps\karakeep.env` is only the Cursor URL and API key. Inference settings belong in the guest file. After editing that file, restart both `karakeep-web` and `karakeep-workers`. The AI Settings link is hidden until the web process sees `OPENAI_API_KEY`.

User Settings → **AI Settings** (`/settings/ai`): **Auto-tagging** on for new saves since the 2026-10-12 Gemini test, **Auto-summarization** off, **Tag Style** lowercase with hyphens. Curated tags are still the 26 Jason selected on 2026-10-08 (`github`, `x`, `reddit`, `tools`, `agents`, and the rest of that set). The guest env points text and image inference at OpenRouter `google/gemini-2.5-flash-lite`. Eight existing items were retagged that day and stayed inside those 26 tags, then the rest of the library was retagged the same day. 844 bookmarks show tagging success. 71 still have an AI tag outside the 26.

Rules fire when a bookmark is added. They do not retag the imported set:

| Rule | Match | Tag |
|---|---|---|
| Host github.com | URL contains `github.com` | `github` |
| Host x.com or twitter.com | URL contains `x.com` or `twitter.com` | `x` |
| Host reddit.com | URL contains `reddit.com` | `reddit` |
| Host youtube | URL contains `youtube.com` or `youtu.be` | `youtube` |

Smart lists **GitHub** (`#github`), **Tools** (`#tools`), **Agents** (`#agents`), and **Twitter** (`#x or #twitter`, added 2026-10-12) sit beside the manual **Discord links** list. Favourites, Archive, and highlights are per card and stay Jason's.

Vault references, when Jason has stored them:

- `vault://dashlane/yingson-labs/karakeep/root-password`
- `vault://dashlane/yingson-labs/karakeep/admin-password`
- `vault://dashlane/yingson-labs/karakeep/cursor-api-key`
- `vault://dashlane/yingson-labs/karakeep/openrouter-api-key` (the value of `OPENAI_API_KEY`)

Whether each of these Dashlane entries exists is not confirmed. Jason must confirm (review findings BAK-05, DOC-07, SEC-08). The live file `/etc/karakeep/karakeep.env` holds these names: `SERVER_VERSION`, `NEXTAUTH_SECRET`, `NEXTAUTH_URL`, `DATA_DIR`, `MEILI_ADDR`, `MEILI_MASTER_KEY`, `BROWSER_WEB_URL`, `DB_WAL_MODE`, `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `INFERENCE_TEXT_MODEL`, `INFERENCE_IMAGE_MODEL`. A rebuild from scratch needs `NEXTAUTH_SECRET`, `MEILI_MASTER_KEY` and the OpenRouter key; a PBS restore brings them back inside the guest.

The container root password currently exists only as `/root/karakeep-lxc-root.password` on the Proxmox host.

## 9. Deployment

Installed from the host with the community script `ct/karakeep.sh` (unattended, `mode=default`), CT id 136, static `192.168.30.33/24`, gateway `192.168.30.1`, bridge `vmbr0`, storage `local-lvm`, template storage `local`.

Updates later use the same script's update path inside the guest, or `update` from the helper script.

**Version check (read only).** `curl -s http://192.168.30.33:3000/api/version` prints the running app version without a login (0.33.2 on 2026-11-01). Compare it with the latest upstream release (`https://github.com/karakeep-app/karakeep/releases`). Version tracking: the app floats on the community script's update path (no pin), Node is pinned to 22 (v22.23.4 live), Meilisearch is 1.54.3 (live, 2026-11-01), the OS is Debian 13.7, and the apt package `alloy` is held at 1.21.2. Do not switch this guest to Docker Compose without a decision. Node is pinned to 22 because Node 24.19 crashes `better-sqlite3` (upstream issue 2989).

## 10. Backup & Recovery

The nightly PBS job includes every guest. The first snapshot of this guest is `ct/136/2026-10-08T17:30:26Z` (finished successfully, 2026-10-08). A restore has not been tested. That keeps the service off R4.

There is no separate database dump. The SQLite file is inside the guest disk, so a PBS snapshot of CT 136 is the backup. Restoring the guest restores the bookmarks.

## 11. Monitoring & Health

| Monitor | URL | Id |
|---|---|---|
| `karakeep (DNS)` | `https://karakeep.yingson.com/` | 115 |
| `karakeep (IP)` | `http://192.168.30.33:3000/` | 116 |

**Good check.** `/api/health` returns 200 with a fixed body and does not prove the workers or search work. Run `systemctl is-active karakeep-web karakeep-workers karakeep-browser meilisearch` and expect four lines of `active` (all four were active on 2026-11-01), plus a 200 from `/signin`.

Both returned `200 - OK` at 2026-10-08 17:31 UTC. Notification id 1 (Yingson Labs Discord `#alerts`). Jason confirmed the down and the up the same day.

Logs go to Loki (CT 138) through Grafana Alloy, installed 2026-10-23 on CT 136: the apt package held at 1.21.2 ships the journal. Labels `host=karakeep` and `service=karakeep`. Query them in Grafana Explore (Loki data source). Rollout record: `docs/ALLOY-ROLLOUT.md` in the loki repo. The Proxmox exporter (Prometheus job `pve`) records CPU, memory, disk and network for every guest, and the Grafana dashboards "Lab overview (test)" and "Service view (test)" (folder Command Center) show each one. Uptime Kuma monitors are also scraped by Prometheus (job `uptime-kuma`) with `host` and `service` labels.

## 12. API & Automation Profile

| Field | Value |
|---|---|
| API type | `rest` |
| Auth | `api-key`. Key is in the laptop env file, not in git. |
| MCP | `needs-wrapper`. Official `@karakeep/mcp` exists and can delete bookmarks, so it is not wired. Homarr has no Karakeep kind. |
| Tier | `read-only` |

The human UI is a login session. The Cursor key is in `C:\Users\thedu\.cursor\mcps\karakeep.env`. Do not copy it into git or chat.

Deleting bookmarks or `/opt/karakeep_data` is destructive. No token will be issued for that.

## 13. Security

Unprivileged container. Chromium is bound to localhost and started with `--no-sandbox` because it runs as root inside the container (the helper script's unit). It is not reachable off the guest.

The web UI is the only published port. Meilisearch and the browser debug port stay on localhost.

No Cloudflare hostname. Jason decided Tailscale only on 2026-10-08.

## 14. Known Issues & Constraints

- The install log on the Proxmox host is `/var/log/karakeep-ct-create.log`.
- `get_dhcp_reservation` did not return the MAC after `update_dhcp_reservation` succeeded and `create_dhcp_reservation` returned `api.err.MacUsed`. `search_clients` shows alias `karakeep-LXC` at `192.168.30.33`. The UniFi hostname field still said `arr-scratch` at creation time; the guest's own hostname is `karakeep`.
- `NEXTAUTH_URL` is `https://karakeep.yingson.com`.
- Swap is about 91 percent used (468 of 512 MiB on 2026-11-01) with memory pressure at 0.00. It holds cold pages, not live thrash. `LxcSwapFull` has fired for CT 136 since 2026-10-29. See WISH-186 and [BASELINES.md](BASELINES.md).
- The curated tag count is written as 26 here and as 25 in one changelog entry. Jason has not settled which is right (review finding DOC-04).

## 15. Operational Procedures

Restart, upgrade, and backup commands are in [docs/RUNBOOK.md](docs/RUNBOOK.md).

## 16. Open Items & Planned Changes

- A read-only Cursor wrapper, if one is wanted. The official server is not that wrapper.
- Gate 7 restore is not done. The service is not R4 without it. Gate 8 baselines were measured on 2026-11-01 as one sample ([BASELINES.md](BASELINES.md)).

## Related

- [docs/RUNBOOK.md](docs/RUNBOOK.md)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- [BASELINES.md](BASELINES.md)
- [docs/SPINUP-karakeep.md](docs/SPINUP-karakeep.md)
