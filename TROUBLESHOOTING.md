---
title: Troubleshooting — karakeep
version: 0.1.1
status: active
last_edited_by: Claude Code
last_edited_date: 2026-11-04
parent: ARCHITECTURE.md
children: []
siblings: [BASELINES.md, CHANGELOG.md]
audience: ops
tags: [yingson-labs, karakeep, troubleshooting]
summary: "Symptoms and fixes for Karakeep on CT 136."
doc_type: troubleshooting
scope: service
service_name: karakeep
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: [proxmox, adguard, npm, tailscale]
depended_on_by: [commandcenter, prometheus]
agent_context: true
permission_tier: read-only
last_verified: 2026-11-01
---

# Troubleshooting — karakeep

## The name loads NPM's default page

`karakeep.yingson.com` resolves via the wildcard to NPM. A resolve is not an NPM host. Check that a proxy host exists for the name and forwards to `192.168.30.33:3000`.

## The page opens on the IP and fails on the name

NPM or the certificate. Since 2026-11-01 the laptop can no longer open `http://192.168.30.33:3000` (the guest firewall lets in only the guest itself, NPM `.182`, Kuma `.130`, Prometheus `.62`, Command Center `.94`, Scanopy `.25` and Homarr `.107`). To test the app without NPM, run `ssh karakeep` and then `curl -s http://127.0.0.1:3000/api/health`. If that works and the name does not, fix NPM, not Karakeep.

To let a new reader in on port 3000, add its address to the set in `/etc/nftables.conf` on CT 136 and run `sudo nft -f /etc/nftables.conf`. Undo: remove the address from the file and reload. Dropped attempts show in `journalctl -k` with the prefix `kk3000-drop`.

## A service cannot reach port 3000

Same firewall. Homarr (`192.168.30.107`) is not on the list, so its tile pings fail. See ARCHITECTURE section 14.

## Sign-in succeeds and the next request is logged out

`NEXTAUTH_URL` in `/etc/karakeep/karakeep.env` is probably still `http://localhost:3000`. Set it to `https://karakeep.yingson.com` and restart `karakeep-web`.

## AI Settings is missing from User Settings

The link is rendered only when the web process sees `OPENAI_API_KEY`. This lab uses `OPENAI_API_KEY` with OpenRouter. Upstream also accepts `OLLAMA_BASE_URL`, which this lab does not set. Those lines live in `/etc/karakeep/karakeep.env` on CT 136, not in the laptop `karakeep.env`. Restart `karakeep-web` after adding them, then open `https://karakeep.yingson.com/settings/ai`. A reload of the old process will not show the page.

## Workers are down and new bookmarks never archive

```bash
sudo systemctl status karakeep-workers karakeep-browser meilisearch
```

Workers wait for the browser and Meilisearch. A Chromium crash loops `karakeep-browser`. `journalctl -u karakeep-browser -n 50` is the next read. Do not expose port 9222 to fix it.

## Search returns nothing for old bookmarks

Meilisearch may be down or the index was wiped. `systemctl status meilisearch`. Rebuilding the index is an app action after the process is up. Do not delete `/opt/karakeep_data` to "fix" search.

## SQLite errors after a disk move

The database was put on NFS. Move `/opt/karakeep_data` back to the local disk. Do not bind-mount that directory to the NAS.
