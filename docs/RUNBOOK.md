---
title: Runbook — karakeep
version: 0.1.0
status: active
last_edited_by: Cursor Grok
last_edited_date: 2026-10-08
parent: ARCHITECTURE.md
children: []
siblings: [TROUBLESHOOTING.md, ARCHITECTURE.md]
audience: ops
tags: [yingson-labs, karakeep, runbook]
summary: "Restart, status, and backup steps for Karakeep on CT 136."
doc_type: runbook
scope: service
service_name: karakeep
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: [proxmox, pbs]
depended_on_by: []
agent_context: true
permission_tier: read-only
last_verified: 2026-10-08
---

# Runbook — karakeep

SSH as `jason` once the Host block exists: `ssh karakeep`. Until then, from the laptop: `ssh proxmox`, then `sudo pct exec 136 -- …`. Commands inside the guest do not need a second sudo when `pct exec` is already root. Commands Jason runs himself on the Proxmox host need `sudo`.

## Status

```bash
sudo pct exec 136 -- systemctl is-active karakeep-web karakeep-workers karakeep-browser meilisearch
sudo pct exec 136 -- curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:3000/
```

## Restart

Order matters. Browser and search first, then workers, then web.

```bash
sudo pct exec 136 -- systemctl restart karakeep-browser meilisearch
sudo pct exec 136 -- systemctl restart karakeep-workers
sudo pct exec 136 -- systemctl restart karakeep-web
```

## Guest reboot

```bash
sudo pct reboot 136
```

`onboot: 1` is set. A Proxmox reboot starts this guest without a manual start.

## Backup

The nightly PBS job includes every guest. A one-shot backup, on the Proxmox host:

```bash
sudo vzdump 136 --storage pbs-backups --mode snapshot --notes-template 'karakeep manual'
```

Confirm `TASK OK` in the task log. A snapshot existing is not a tested restore.

## Upgrade

Use the community-script update path. It stops the three units, pulls the GitHub release, rebuilds on Node 22, migrates the database, and starts the units. Take a PBS snapshot first. Do not switch the guest to Node 24.
