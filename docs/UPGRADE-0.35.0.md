---
title: Upgrade record 0.35.0 — karakeep
version: 0.1.0
status: active
last_edited_by: Claude Code
last_edited_date: 2026-11-16
parent: RUNBOOK.md
children: []
siblings: [TROUBLESHOOTING.md, ARCHITECTURE.md]
audience: ops
tags: [yingson-labs, karakeep, upgrade]
summary: "What was done, checked and learned when Karakeep on CT 136 went from 0.34.1 to 0.35.0 on 2026-11-16."
doc_type: runbook
scope: service
service_name: karakeep
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: [proxmox, pbs]
depended_on_by: []
agent_context: true
permission_tier: read-only
last_verified: 2026-11-16
---

# Upgrade record 0.35.0 — karakeep

Date: Mon 2026-11-16, 16:05 to 16:25 Pacific, inside the six-hour run (lane L5). Approval: Jason, Y1 (J-156), "Y1-Y5 i take your recommendations", the rule being the newest 0.35 patch on the day. Upstream was re-checked at 15:30 and 16:05: newest release v0.35.0 (2026-11-15), no 0.35.1, not a pre-release.

## Steps and results

| Step | Result |
|---|---|
| Snapshot | `pre_run6h_20261116_exp20261123` on CT 136 (15:04 Pacific, by the coordinator) |
| Kopia by hand before | `kopia-backup-karakeep.service` Result=success at 15:32 |
| Alert quiet | Alertmanager silence on `alertname=~"KarakeepUnit.*"` (Watchdog not matched), 16:00 to 17:34 |
| Counts before | 987 bookmarks, 50 tags, 19 lists (18 smart, 1 manual), 0 highlights |
| Update | `update` inside CT 136 (community-scripts helper, silent mode, no tty needed), 16:05:30 to 16:08:27 (about 3 minutes). Version 0.34.1 to 0.35.0 |
| Meilisearch | The updater also moved Meilisearch 1.56.0 to 1.57.0 (released the same day) with a dumpless in-place upgrade. It wrote a safety copy `/var/lib/meilisearch/pre-upgrade-1.56.0.tar.gz` (kept) |
| Drop-ins and perms | The three `10-user.conf` drop-ins survived and still call `karakeep-perms.sh`; units run as `karakeep`. Perms script run by hand, then web, workers and browser restarted at 16:10 |
| Counts after | 987 bookmarks, 50 tags, 19 lists, 0 highlights, 987 vectors in Meilisearch, `karakeep_semantic_search_ok` 1 |

## Checks

- `/api/version` says 0.35.0 by name and from inside the guest by raw IP. The laptop and the Proxmox host cannot reach `192.168.30.33:3000` (nftables allow list), as before.
- `karakeep-web`, `karakeep-workers`, `karakeep-browser` and `meilisearch` active, no restarts, no error lines in the journal after the restart. `karakeep.target` does not exist on this guest.
- `/api/health` and `/signin` return 200.
- Sign-ups: `DISABLE_SIGNUPS` is set and the public client config reports `disableSignups: true`.
- SSRF: `validateUrl` from `apps/workers/network.ts` refused 127.0.0.1, 192.168.30.1, 192.168.30.62, 10.0.0.1, 169.254.169.254, `[::1]` and two NAT64 forms, and allowed example.com.
- Semantic and hybrid search return results.
- Kuma monitors 115 and 116 up.
- Kopia by hand after the upgrade: Result=success at 16:19:54. The silence was expired at 16:22 and no Karakeep alert is firing.

## How to run the SSRF check again

On CT 136, as root, with the env file loaded: `node --experimental-strip-types --import <loader> <test>.mjs` from `/opt/karakeep/apps/workers`. The loader adds `.ts` to extensionless imports so `@karakeep/shared/config` resolves. The test script calls `validateUrl(url, false)` for each address and prints REFUSED or ALLOWED. The scripts are not kept on the guest.

## Traps seen

- The updater is not just Karakeep: it also upgrades Node 24 and Meilisearch. Read `lib/db.func` in community-scripts/core before the next one; a Meilisearch change is a dumpless upgrade that cannot be rolled back except from the tarball.
- Disk: free space on `/` went from 4.7 GB to 3.0 GB (the new build plus the 270 MB Meilisearch tarball). Remove the tarball after a quiet week.
- The old RUNBOOK sentence "Do not switch the guest to Node 24" is stale: the guest has run Node 24 since the 2026-11 patching.

## Rollback (not used)

Restore the PBS snapshot `pre_run6h_20261116_exp20261123`. It cannot bring back anything saved after 15:04 Pacific.
