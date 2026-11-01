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

## Kopia backup (logical copy)

Runs by itself at 05:00 Pacific (`kopia-backup-karakeep.timer`). Check it on the guest: `systemctl list-timers kopia-backup-karakeep.timer` and `systemctl status kopia-backup-karakeep.service` (look for `status=0/SUCCESS`). Freshness: Prometheus `kopia:source_snapshot_age:seconds{client="karakeep@ct136"}` for the two sources, and the `KopiaSourceStale` alert. A manual run: `ssh karakeep "sudo systemctl start kopia-backup-karakeep.service"`. What is saved: see ARCHITECTURE section 10. Run it before any upgrade.

## Restore from PBS to a scratch CT (tested 2026-11-01)

Run at `jason@proxmox` as one script (`ssh proxmox 'sudo bash -s' < restore-test.sh`). Never touch live CT 136. A scratch restore is not R4 on its own.

1. List backups: `pvesm list pbs-backups --vmid 136`. Pick the newest.
2. Restore to a free scratch ID with a new MAC: `pct restore 197 pbs-backups:backup/ct/136/<time> --storage local-lvm --unique 1 --start 0` (about 2.5 minutes).
3. Before the first start, remove the network so the copy cannot clash with live CT 136 (same IP): `pct set 197 --delete net0 --onboot 0 --hostname karakeep-restoretest`.
4. `pct start 197`, wait about 30 seconds.
5. Inside (`pct exec 197 -- ...`): `karakeep-web`, `karakeep-workers`, `karakeep-browser` and `meilisearch` are active; `curl http://127.0.0.1:3000/api/health` is 200; `/signin` is 200; `/api/version` answers. There is no `sqlite3` binary, so use python3 read only: `sqlite3.connect("file:/opt/karakeep_data/db.db?mode=ro", uri=True)`, then `pragma integrity_check` and `select count(*) from bookmarks`.
6. Destroy: `pct stop 197; pct destroy 197 --purge 1`. Confirm `pct list` has no 197 and `lvs | grep vm-197` is empty.
7. Append one line to `lab-standards/restore-tests/restore-log.jsonl`.

Result 2026-11-01: backup `ct/136/2026-11-01T10:18:40Z`, integrity ok, 947 bookmarks, 1 user. To rebuild from the Kopia copy instead, restore the `db.sqlite3` and `etc-karakeep` snapshot of `/var/backups/kopia/karakeep` and the assets snapshot with `kopia restore` into a scratch location (not yet rehearsed).

## Tagging, rules, and lists

AI Settings: auto-tagging on for new saves, lowercase hyphens, summarization off, Jason's 26 curated tags still selected. Text and image inference use OpenRouter `google/gemini-2.5-flash-lite`. Host rules for github, x/twitter, reddit, and youtube run on new bookmarks only. Smart lists **GitHub**, **Tools**, **Agents**, and **Twitter** (`#x or #twitter`) follow those tags. Eight items were retagged on 2026-10-12, then the rest of the library the same day. 844 bookmarks finished success. Do not run another library-wide retag unless Jason asks. Favourites, Archive, and highlights are chosen on each card.

## Check the version

Read only, no login: `curl -s https://karakeep.yingson.com/api/version` (the laptop cannot use the IP any more, see TROUBLESHOOTING) prints the running app version (0.33.2 on 2026-11-01). Compare it with the latest release at `https://github.com/karakeep-app/karakeep/releases`.

## Upgrade

Use the community-script update path. It stops the app units, pulls the GitHub release, rebuilds on Node 22, migrates the database, and starts the units. Take a PBS snapshot first. Do not switch the guest to Node 24.
