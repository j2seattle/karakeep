---
title: Troubleshooting — karakeep
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-08
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
depends_on: [proxmox, npm, adguard]
depended_on_by: []
agent_context: true
permission_tier: read-only
last_verified: 2026-10-08
---

# Troubleshooting — karakeep

## The name loads NPM's default page

`karakeep.yingson.com` resolves via the wildcard to NPM. A resolve is not an NPM host. Check that a proxy host exists for the name and forwards to `192.168.30.33:3000`.

## The page opens on the IP and fails on the name

NPM or the certificate. Direct `http://192.168.30.33:3000` bypasses both. If the IP works and the name does not, fix NPM, not Karakeep.

## Sign-in succeeds and the next request is logged out

`NEXTAUTH_URL` in `/etc/karakeep/karakeep.env` is probably still `http://localhost:3000`. Set it to `https://karakeep.yingson.com` and restart `karakeep-web`.

## AI Settings is missing from User Settings

The link is rendered only when the web process sees `OPENAI_API_KEY` or `OLLAMA_BASE_URL`. Those lines live in `/etc/karakeep/karakeep.env` on CT 136, not in the laptop `karakeep.env`. Restart `karakeep-web` after adding them, then open `https://karakeep.yingson.com/settings/ai`. A reload of the old process will not show the page.

## Workers are down and new bookmarks never archive

```bash
sudo systemctl status karakeep-workers karakeep-browser meilisearch
```

Workers wait for the browser and Meilisearch. A Chromium crash loops `karakeep-browser`. `journalctl -u karakeep-browser -n 50` is the next read. Do not expose port 9222 to fix it.

## Search returns nothing for old bookmarks

Meilisearch may be down or the index was wiped. `systemctl status meilisearch`. Rebuilding the index is an app action after the process is up. Do not delete `/opt/karakeep_data` to "fix" search.

## SQLite errors after a disk move

The database was put on NFS. Move `/opt/karakeep_data` back to the local disk. Do not bind-mount that directory to the NAS.
