---
title: Service Review: karakeep, 2026-11-01
version: 1.0.0
status: active
last_edited_by: Claude Code
last_edited_date: 2026-11-01
audience: internal
tags: [yingson-labs, karakeep, service-review, findings]
summary: "Service Review run 1 for karakeep (CT 136), review only: 67 findings (high 3, medium 21, low 43). Checklist, scorecard, wishlist verdicts, sprint plan and questions for Jason."
doc_type: reference
scope: service
service_name: karakeep
parent_doc: lab-standards/ARCHITECTURE.md
agent_context: true
permission_tier: n-a
last_verified: 2026-11-01
run: review
run_number: 1
reviewer: claude-code
date: 2026-11-01
lab_standards_sha: 45dc495
repo_sha: 90baf74
app_version: 0.33.2
readiness_supported: R3
---

# Service Review: `karakeep` (CT 136), 2026-11-01

Page: PENDING. Review run, read only. Nothing was changed on any server. The findings list is in [FINDINGS.md](FINDINGS.md); this file holds everything else. Assembled by lane A from the verified parts of lanes D0, S, P, N and U (director-worker `2026-11-karakeep-service-review/parts`).

## Basis

- karakeep repo HEAD `90baf74` (2026-10-29). The working tree had 7 uncommitted files from another session (`.cursor/rules/lab-doc-contract.mdc`, `.env.example`, `ARCHITECTURE.md`, `CHANGELOG.md`, `CLAUDE.md`, `CURSOR.md`, `docs/RUNBOOK.md`) and one untracked rule file. They were not touched, not staged and not used as evidence. They were read as leads, and each DOC finding says what HEAD, the working tree and the live system show.
- lab-standards `45dc495` read at assembly. The lanes launched at `68a6376`; HEAD moved during the run.
- Live reads, SUDO READS: no. Every fact that needs sudo is labeled unverified.
- Lanes X0 and X (bookmark sweep and the WISH-244 use case) are held and are out of this review's findings.
- Method deviations by lanes: S ran three reads outside the allowlist (`grep` of `/etc/ssh/sshd_config`, `systemctl is-active`, `sudo -n -l`); U ran `node --version` and a resolver and `dpkg` read on the guest. See Overlaps and conflicts.

## Result

**67 findings:** critical 0, high 3, medium 21, low 43. 23 are `unverified` in their Checked field. Readiness supported by the live checks: **R3** (the inventory says R3, no conflict). Connected level: **C1**.

| Lane | Findings | Critical | High | Medium | Low |
|---|---|---|---|---|---|
| S (SEC) | 12 | 0 | 0 | 3 | 9 |
| P (PAT, BAK, HLT) | 15 | 0 | 1 | 6 | 8 |
| N (SPD, INT, MON) | 14 | 0 | 1 | 3 | 10 |
| U (DOC, USE, CC) | 26 | 0 | 1 | 9 | 16 |
| **Total** | 67 | 0 | 3 | 21 | 43 |

Highs: BAK-01 (no logical backup, PBS is the only copy, never restored), MON-01 (nothing alerts if the workers, Meilisearch or the browser stop), USE-03 (same fact as BAK-01). DOC-01 was ruled medium by the coordinator because a docs-only drift meets no Step 5 high trigger (lane U rated it high).

Top 5 to look at first: BAK-01, MON-01, INT-01 (page text goes to OpenRouter and on to Google, and no lab table says so), MON-05 (full bookmark URLs, some from sign-in sessions, are in Loki), PAT-02 with PAT-01 (browser security updates pending, two releases behind). SEC-01 and SEC-02 (root SSH login in the config, WISH-236) are next.

## Overlaps and conflicts raised (nothing merged, every ID kept)

Each pair below keeps both IDs and is cross-linked in Links. Lane A did not change any severity or meaning.

| Items | What the parts say |
|---|---|
| BAK-01 / USE-03 | Same fact (no logical backup). Both high. Owners differ (jason versus chief), effort differs (L versus M). Treat as one fix. |
| USE-01 / CC-03 | Same evidence (`/api/metrics` returns 401, no `karakeep*` series). Both medium. |
| USE-06 / CC-07 | Slug tags as join keys, and the Command Center read that needs them. Both low. |
| HLT-01 / SPD-01 / DOC-12 | Swap near full. HLT-01 is the alert, SPD-01 the sizing view, DOC-12 the missing doc line. All low. Date conflict: P and N say `LxcSwapFull` has been active since 2026-10-29T11:36Z (Alertmanager); U's DOC-12 said 2026-10-28 (the day WISH-186 first saw 97 percent); DOC-12 now reads 2026-10-29T11:36Z, confirmed by the coordinator. |
| HLT-02 / SPD-05 | Both are the empty BASELINES.md, same fix, same medium. |
| HLT-05 / SPD-02 | Same load average reading, cause unverified in both. P left it to N. |
| DOC-02 / INT-01 / INT-03 / CC-06 / DOC-01 | The Ollama versus OpenRouter drift seen from five sides. Severities differ by design: DOC-01 medium (ruled down from high by the coordinator), INT-01 medium (the privacy decision), DOC-02 medium, INT-03 low, CC-06 medium. DOC-01 was rated high by U; the coordinator ruled it medium because a docs-only drift meets no Step 5 high trigger. |
| SEC-08 / BAK-05 / DOC-07 / USE-05 | One Dashlane question rated four ways (low, medium, medium, low). Jason's one answer closes all four. |
| PAT-05 / DOC-08 | Same missing LAB-STANDARDS section 12 upgrade backlog row. |
| BAK-04 and scanopy lab-standards/MON-01 | BAK-04 (no Prometheus rule for stale PBS backups) is the same gap already open as `lab-standards/MON-01` in scanopy's FINDINGS.md. Listed once lab-wide by P; kept here under its own ID. |
| HLT-03 / DOC-09 / MON-01 / DOC-05 / CC-02 | SRE good-check, the version check and the three-versus-four units claim all touch the same health definition. |
| INT-02 / CC-05 | Spend per consumer in OpenRouter. INT-02 verified the missing metric labels; CC-05 is unverified on per-key output. Compatible. |
| SEC-02 / SEC-05 / SEC-11 / SEC-12 / DOC-11 | All five rest on sudo reads that this run did not allow. One Your call (allow the sudo reads in a fix run) answers them. SEC-12 and U's USE-01 disagree on the owner of loopback ports 12345 and 34943: S guesses Grafana Alloy, U suggests the Karakeep worker metrics port. Both unverified. |
| MON-05 / security lane | N found full bookmark URLs (some with session parameters) in Loki and handed severity to lane S. S has no matching finding. Kept medium as N wrote it. Its Standard is shown as `none` because SECRETS-RULE rule 2 is not a Step 5 standard form. |
| Node version | P says the guest Node version has no allowlisted read (PAT-05, PAT-01); U read `node --version` on the guest and got v22.23.4 (Section H live facts). If U's read counts, PAT-05 and the Node CVE question in PAT-01 can be narrowed. `node --version` is not on the allowlist, so lane A did not promote it to a verified fact. |
| Count differences, same fact | Loki openrouter lines 316 (D0, all units) versus 312 (N, web unit only); error lines 245 (D0) versus 248 (P); disk 56 percent (D0, Proxmox view) versus 59 percent (guest `df`) versus 61 percent (node filesystem). These are scope or time differences, not conflicts. |
| Lane N reply count | N's reply said 15 findings but its file lists 14 (MON-06 is a plumbing table, not a finding). Recomputed: 14 (1 high, 3 medium, 10 low). |
| Wishlist ID collision | WISH-254 was taken by another session (Canvas prompt rewriter). Lane S's proposals were moved to WISH-265 and WISH-255. To record for the pilot. |

## Service card

Karakeep (bookmark archive). Saves links, notes and full copies of web pages so they can be found later, even if the page goes away. Jason's bookmark and web page archive. CT 136, 192.168.30.33, port 3000 behind NPM host 53 at `karakeep.yingson.com` (Tailscale only, no Cloudflare). Community script install, four native systemd units (karakeep-web, karakeep-workers, karakeep-browser, meilisearch), no Docker. App 0.33.2 (live `/api/version`). Debian 13, 2 vCPU, 4 GiB RAM, 512 MiB swap, 14.7 GiB disk. Kuma monitors 115 and 116. Owner: Librarian. Registry status active, readiness R3. Past runs: none, so this is the first review.

## Service pass checklist

| Row | What it says |
|---|---|
| **Readiness** | R3 supported by the live checks (inventory says R3, no conflict). Open gates: Gate 7 (no protect list, never restored: BAK-01, BAK-02, owner jason) and Gate 8 (BASELINES all "not yet measured": HLT-02, SPD-05, lane A writes after approval). Also unverified: Homarr tile (HLT-04), SRE good-check reading not stored (HLT-03). Standards line: `Standards: R3 gates 1 to 6 met except the unverified items; Gates 7 and 8 Deferred.` File-level list: Kopia paths none yet; proposed for the fix run: the SQLite database through its backup API to a staging folder, the asset folder and `/etc/karakeep` (exact paths unverified, root only). PBS already has the whole guest: newest 2026-11-01 10:18 UTC, 10 snapshots, nightly. External drive: nothing for this service. Left before R4: a protect list or explicit "no additions", one logged scratch restore with an app check (Gate 7), BASELINES filled with thresholds (Gate 8). |
| **Updates** | Running 0.33.2 (read from the service). Upstream stable 0.34.1 (2026-10-22), two releases behind. Not applied. A security fix leads: 0.34.1 is a security release (Node CVEs in the Docker image, applicability to this native install unverified) and 3 apt security updates are pending, two for Chromium (PAT-01, PAT-02). 0.34.0 has a one-way auth migration that signs everyone out once; rollback is a restore of an untested snapshot. |
| **API** | REST, api-key auth, tier read-only. Cursor has a key (laptop `karakeep.env`, `vault://dashlane/yingson-labs/karakeep/cursor-api-key`), and that file also holds the admin user and password names (SEC-09). Hermes has a laptop file `karakeep-hermes.env`; the CT 139 copy is unverified. A separate OpenRouter key file exists for tagging. Claude Code has none. Every `/api/v1/*` path tested returned 401 without a key. |
| **MCP** | Do not add the official `@karakeep/mcp` (it has delete tools). Add later, only as a read-only search and get wrapper behind the gateway (WISH-078, LAB-DEC-043). |
| **Restore** | Not tested. No karakeep line in `restore-tests/restore-log.jsonl` (42 lines at D0's read, 43 at P's). No restore steps in the runbook. BAK-02. |
| **Suggestions** | 1. Prometheus metrics and a Command Center card, with a fixed metrics token and a read-only key (USE-01, WISH-260, WISH-258). 2. Hermes and the Chief search the archive through a read-only wrapper (WISH-258, WISH-078). Not started in the review. |
| **Connected** | **C1** (feeds Command Center: the service card, Kuma status and guest metrics are on a page). This is lane A's reading of the C0 to C4 rule. Missing for C2: an alert on the units (MON-01), a freshness alert on the PBS backup (BAK-04), and silence detection for the Discord importer (INT-04). C3 and C4 need a shared join key from bookmarks to lab slugs and an agent key (USE-06, WISH-258). |

## What it could send to Command Center, and do for the rest of the lab

From lane N sections J and D8 and lane U section J. All ideas, nothing started. Each is in the proposed WISH text (WISH-258, WISH-259, WISH-260, WISH-261) in the coordinator file.

- **See:** `/api/health` and `/api/version` (no secret, 60 s and 1 h), four unit states from Prometheus, queue depth and failed jobs from `/api/metrics` (needs USE-01), PBS freshness (exists), library counts from the API (needs a read key; held with X0).
- **Reach:** deep links to lists, tags and the admin jobs page (routes unverified, CC-04). Kuma 115 and 116, NPM host 53, PBS group for CT 136.
- **Join keys:** present are slug `karakeep`, guest 136, hostname, IP, Kuma 115 and 116, Loki and Prometheus `service` label. Missing: a bookmark or tag that maps to a TOOLS.yaml slug (USE-06, CC-07).
- **Correlate:** Kuma 115 down and 116 up points at NPM or AdGuard; both down with the unit series fine points at the web unit; a swap, worker state and OOM alert joined into one; tagging failures joined with OpenRouter balance.
- **Push or pull:** pull `/api/health` and `/api/version`; alerts go through a Prometheus scrape of `/api/metrics` (LAB-DEC-061). Library content stays out of Command Center unless Jason approves.
- **For the rest of the lab:** Hermes saves and searches links read-only first (M); the Discord importer without the laptop (WISH-088, M); release notes matched to saved bookmarks (M); bookmark text into Open Brain (L); an alert evidence link per slug (S after the tags exist). None of these approve a build.

## Standards scorecard

| Section | Match | Did not match | Unverified | Note |
|---|---|---|---|---|
| B Security | 6 | 5 | 5 | 1 n/a. 17 rows. Source S. |
| A Patching | 1 | 4 | 0 | One "partly" (held package) counted as did not match. 5 rows. Source P. |
| F Backups | 1 | 4 | 2 | 1 n/a. 8 rows. Source P. |
| G Health and readiness | 7 | 2 | 2 | One "partly, unverified" counted as unverified. 11 rows. Source P. |
| C Speed | 3 | 1 | 4 | Source N. |
| D Integrations | 2 | 2 | 3 | Source N. |
| E Monitoring | 5 | 2 | 5 | Source N. |
| H Doc drift | 9 | 9 | 1 | Source U. 19 rows. |
| I Full use | 2 | 2 | 2 | Source U. |
| J Command Center | 2 | 4 | 3 | Source U. |
| **Total** | **38** | **35** | **27** | 2 n/a, 102 rows. Run log object: match 38, no 35, unverified 27. |

## Wishlist verdicts (from D0, Step 2)

| WISH | Verdict | Reason |
|---|---|---|
| WISH-236 | fold in | SSH key-only and root login on CT 136. Joins SEC-01 and SEC-02. Config file confirms `PermitRootLogin yes`; effective values and the root password are unverified (need sudo). Jason deferred the fix to this review; that is not approval to change the server. |
| WISH-244 | keep as idea | Karakeep as the research library. Use-case track (X0, X). Its check-first items stay unverified. INT-01 shows tagging already sends text to OpenRouter. |
| WISH-088 | fold in later | Discord link import is a laptop script (INT-04). Waits on where the archive runs. |
| WISH-014 | fold in | Kopia protect lists. Joins BAK-01 and USE-03. No Kopia source for karakeep. |
| WISH-078 | fold in later | Read-only MCP wrapper. The official MCP has delete tools. See the MCP row. |
| WISH-189 | keep as idea | LiteLLM router. Not for this plan. Tagging is on OpenRouter, so karakeep is no longer an Ollama client. |
| WISH-060 | keep as idea | Two Ollama engines. Karakeep tagging no longer calls CT 112. |
| WISH-169 | fold in | Patch debt. Joins PAT-02 and PAT-03. The 2026-10-28 `apt upgrade` snapshot is due for deletion 2026-11-04. |
| WISH-186 | fold in later | Swap full. Joins HLT-01 and SPD-01. Waits on Jason's approval of the rule tuning. |
| WISH-081 | none | Pilot record for this run. |
| New | proposed | WISH-255, 256, 257, 258, 259, 260, 261, 265, plus additions to 014, 078, 088, 244, 060, 189. Text is in the coordinator file. WISH-153 (PBS verify per snapshot) is linked from BAK-03. |

No wishlist item shows as done live. No state change is made in this run.

## What works

Name is Tailscale only and not in public DNS. Certificate valid to 2027-01-24, HTTP redirects to HTTPS. All four units active, no failed units, both Kuma monitors up, `verify-kuma-monitors.py` PASS. Every API path tried needs a key. `/api/health` returns 200, `/api/version` answers. Meilisearch and the Chromium debug port are on loopback. Secret folders are 700 root. No secret-shaped string in git history. Nightly PBS backup runs (newest 2026-11-01, 10 snapshots, store verify clean). Logs reach Loki and `TelemetryMissing` covers the host. Guest baseline matches (hostname, time zone, clock, `jason` and one key, cron). No password logins or guesses in 7 days of logs. The SRE good-check passes when run now.

## Not checked, and why

- Needs sudo (SUDO READS: no): privileged flag, `backup=0`, `pct listsnapshot`, `sshd -T`, `passwd -S root`, listening-port owners, `nft list ruleset`, the env file mode and contents, `/opt/karakeep_data` size, the `--no-sandbox` flag.
- Needs a login or key: library counts, tags, lists, rules, semantic search, summarization, webhook and API key pages, the sign-up state, tagging model values, key equality between Cursor and Hermes.
- Meilisearch version (401 without a key). Node CVE applicability to this install.
- Off-LAN reach through Tailscale and the real public path.
- Homarr tile, UniFi reservation and server VLAN rules, NPM host 53 record and access list, Alertmanager receiver config, Kuma retries and interval, GitHub mirror, Loki alert rules (ruler returned 400), per-guest PBS verify state, Kopia and Alertmanager paths for PBS freshness.
- Feature behavior that needs a login, and `/api/health` returning 503 (needs a stop; ground rule 9). Discord down and up retest.
- Dashlane copies of any secret (only Jason knows).
- Lane X0 and lane X are held and out of this review's findings. WISH-244 stays an idea.
- Samples, not full reads: Loki error and URL samples (100 to 1000 lines), lab-standards CHANGELOG (244 commits since the sync receipt not read in full).
- Upstream docs read only on the landing and environment variable pages (U); 0.33.2 specifics are unverified.

## Sprint plan

Nothing here is approved. Reply with IDs or sprints. A new service or guest still needs its own approved plan (LAB-DEC-080).

| Sprint | IDs and what changes | Jason must approve | Rough time | How to check | How to undo |
|---|---|---|---|---|---|
| **0 Doc fixes** (approval none) | DOC-01 (after Jason's answer on the 7 working tree files), DOC-02, DOC-03, DOC-05, DOC-06, DOC-08, DOC-09, DOC-10, DOC-12, DOC-13, PAT-05, INT-03, HLT-02 and SPD-05 (write BASELINES from the measured numbers), HLT-03 (store the SRE reading), CC-06 (re-run the generator after DOC-02). Waiting on answers: DOC-04 (tag count), DOC-07 and SEC-08 (Dashlane), SEC-09 (admin lines in the Cursor env file), DOC-11 (sudo reads). | Jason: the 7 working tree files, 25 or 26 tags, Dashlane, sudo reads | About 2 hours | `validate-docs.py` passes; every doc says OpenRouter, four units, 0.33.2 | `git revert` |
| **1 Small reversible changes** (remediate) | MON-01 (Prometheus unit-state rule), BAK-04 (lab-wide PBS age rule), HLT-01 (WISH-186 rule tuning or a swap baseline), SEC-06 (disable avahi and postfix if unneeded), SEC-07 (sign-up off, one restart of karakeep-web), PAT-03 and PAT-04 (decisions, then small changes), MON-03 (optional response-time alert), MON-04 (optional Loki rule). | Each ID | About half a day | Rule loads and a test alert reaches `#alerts`; `ss -tlnu` and `systemctl` show the change | Remove the rule; re-enable the units; switch sign-up back on |
| **2 Patching** (after hours, snapshot first) | BAK-02 first (restore the newest snapshot to a scratch CT with the network removed, check health, sign-in and bookmark count, destroy, log it, write restore steps), then PAT-02 (Chromium, libnss3, tzdata; restart karakeep-browser), then PAT-01 (community-script update to 0.34.1, which signs everyone out once and lowercases emails). | Jason approves each by ID; PAT-01 is destructive | About half a day for the restore test, 1 to 2 hours for the upgrade | `/api/version` shows 0.34.1, sign-in works, `apt list --upgradable` shows no security items, `restore-log.jsonl` has a karakeep line | Restore the pre-upgrade PBS snapshot; apt downgrade by version |
| **3 Security and exposure** (each its own approval) | SEC-01 and SEC-02 (SSH drop-in, console fallback ready, WISH-236), SEC-10 (NPM headers), SEC-04 with SEC-05 (limit port 3000 to NPM after reading the ruleset), MON-05 (drop query strings from `checkUrl` log lines in Alloy, decide about rotation), SEC-11 and SEC-12 (the sudo reads), SEC-03 (non-root plan, WISH-265; needs a plan first). | Each change separately; SEC-03 needs a plan | SEC-01 and SEC-02 under 30 minutes; the rest 1 to 3 hours; SEC-03 a project | `sshd -T` shows the new values and `ssh karakeep whoami` still works with the lab key; curl to port 3000 from a non-NPM host fails | Delete the drop-in and reload; remove the nftables rule; restore the Alloy config |
| **4 Integrations and larger work** (each a WISH) | BAK-01 (protect list, Kopia client, SQLite dump, freshness monitor; needs a plan), USE-03, USE-01 and CC-03 (metrics token and scrape), CC-01, CC-02, CC-04 (Command Center reads and links), CC-05 and INT-02 (own OpenRouter key and per-key label), INT-01 (privacy decision and options), INT-04 (importer off the laptop), USE-02 (semantic search with WISH-244), USE-04 and USE-06 and CC-07 (webhooks and slug tags), USE-05, MON-02, SPD-02, SPD-03, SPD-04 and HLT-05 (investigations for a later run), BAK-03 and HLT-04 (waiting on WISH-153 and a Homarr look). | Each plan | Days, spread across sessions | One clean run and a freshness monitor for any backup job (LAB-DEC-053); metrics series exist; card shows data | Per item; remove the job, client, key or scrape |

Sprint note: CC-01, CC-02, CC-04, CC-05 and CC-07 carry approval `none` in lane U's table but are Command Center code or data changes, not doc fixes, so they sit in Sprint 4.

## Your call (questions for Jason, deduplicated)

1. The 7 uncommitted karakeep files (the move to OpenRouter and the Twitter list): who commits them and when? Until then HEAD says Ollama (DOC-01). Options from D0: the other session commits, the review waits, or the review uses HEAD and says so (this one did the last).
2. Curated tag count: 25 or 26? The working tree CHANGELOG says both (DOC-04).
3. Allow sudo reads (`pct config 136`, `sshd -T`, `passwd -S root`, `ss -tlnup`, `nft list ruleset`, `systemctl cat`, the env file variable names) in a fix run, or accept them as unverified (SEC-02, SEC-05, SEC-11, SEC-12, DOC-11, and D0's list)? Lane S also ran `sudo -n -l` in a no-sudo run; say whether that is acceptable for future reviews.
4. Approve the SSH drop-in by ID (SEC-01, SEC-02, WISH-236): `PermitRootLogin prohibit-password` and `PasswordAuthentication no`, lock the root password afterwards?
5. SEC-03: accept the community script's design (services and Chromium as root) or plan a non-root user (WISH-265)?
6. SEC-04: limit port 3000 to NPM with a guest firewall rule, or accept plain HTTP to the whole LAN?
7. SEC-07: should open sign-up be off? A second account would need a one-time toggle.
8. Dashlane (SEC-08, BAK-05, DOC-07, USE-05): which of root password, admin password, Cursor key, Hermes key, OpenRouter key and NEXTAUTH_SECRET have a copy? If the root password does, can `/root/karakeep-lxc-root.password` on the Proxmox host be removed?
9. SEC-09: remove `KARAKEEP_ADMIN_USER` and `KARAKEEP_ADMIN_PASSWORD` from the Cursor env file, or change the doc to say they are there?
10. PAT-01: upgrade to 0.34.1 now or wait? It signs everyone out once, lowercases emails, and its rollback is a restore that has never been tested.
11. PAT-02: apply the three security updates (two for Chromium) now, or batch them with PAT-01?
12. PAT-03: does the lab want unattended security updates on guests, or a fixed patch day (WISH-256)?
13. BAK-01: add Kopia to CT 136 (a logical copy of the database, assets and config), or write "no additions" and accept the PBS snapshot as the only copy?
14. BAK-02: OK to restore the newest snapshot to a scratch CT with the network removed, then destroy it?
15. HLT-01: approve the WISH-186 `LxcSwapFull` rule tuning, or give CT 136 more RAM, or record swap at about 90 percent with no pressure as the Gate 8 baseline?
16. INT-01: is it acceptable that page text (and possibly images) goes to OpenRouter and on to Google for tagging? Options: keep and document it; go back to local Ollama; or keep OpenRouter and exclude private or logged-in URLs.
17. INT-02 and CC-05: does karakeep have its own OpenRouter key and limit? If not, create one.
18. INT-04: where should the Discord importer run if not the laptop (WISH-088)?
19. MON-05: should query strings of checked bookmark URLs be dropped from Loki, and should anything be rotated? Lane N did not copy or print the URLs.
20. USE-01: OK to set a fixed `PROMETHEUS_AUTH_TOKEN` (needs a restart) so the metrics can be scraped?
21. USE-02: turn on semantic search? Decide with WISH-244 and lane X.
22. USE-06 and CC-07: do you want lab slug tags in Karakeep at all?
23. D0 question: add `jason` to `systemd-journal` on CT 136 so `journalctl -u karakeep-*` works? Loki covers the logs today.

## Run record

One line for `lab-standards/service-reviews/review-log.jsonl` is returned to the coordinator (lane A does not write lab-standards). Counts: critical 0, high 3, medium 21, low 43; new 67; fixed 0; regressed 0; unverified 23; standards match 38, no 35, unverified 27.

Review only. Nothing was changed on any server. Reply with the IDs or sprints you approve.
