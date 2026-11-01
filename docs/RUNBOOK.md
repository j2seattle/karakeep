---
title: Runbook — karakeep
version: 0.1.0
status: active
last_edited_by: Claude Code
last_edited_date: 2026-11-01
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
last_verified: 2026-11-01
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

## Restart after an env change

`/etc/karakeep/karakeep.env` is read when each unit starts. From the laptop, this needs `sudo` on the guest:

```text
ssh karakeep "sudo systemctl restart karakeep-workers karakeep-web"
```

Restart the web unit as well as the workers. User Settings hides **AI Settings** until the web process has `OPENAI_API_KEY` in its environment.

## Import new Discord links

New JSON files land in `C:\Users\thedu\discord-link-archive\items`. From the laptop, no sudo:

```text
python "C:\Development\Yingson Labs\karakeep\scripts\import-to-karakeep.py"
```

The script reads `C:\Users\thedu\.cursor\mcps\karakeep.env` and skips ids already recorded in `C:\Users\thedu\discord-link-archive\import-state.json`.

## Tagging, rules, and lists

AI Settings: auto-tagging on for new saves, lowercase hyphens, summarization off, Jason's 26 curated tags still selected. Text and image inference use OpenRouter `google/gemini-2.5-flash-lite`. Host rules for github, x/twitter, reddit, and youtube run on new bookmarks only. Smart lists **GitHub**, **Tools**, **Agents**, and **Twitter** (`#x or #twitter`) follow those tags. Eight items were retagged on 2026-10-12, then the rest of the library the same day. 844 bookmarks finished success. Do not run another library-wide retag unless Jason asks. Favourites, Archive, and highlights are chosen on each card.

## Check the version

Read only, no login: `curl -s http://192.168.30.33:3000/api/version` prints the running app version (0.33.2 on 2026-11-01). Compare it with the latest release at `https://github.com/karakeep-app/karakeep/releases`.

## Upgrade

Use the community-script update path. It stops the app units, pulls the GitHub release, rebuilds on Node 22, migrates the database, and starts the units. Take a PBS snapshot first. Do not switch the guest to Node 24.
