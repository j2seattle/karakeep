---
title: Findings: karakeep
version: 1.0.0
status: active
last_edited_by: Claude Code
last_edited_date: 2026-11-01
audience: internal
tags: [yingson-labs, karakeep, service-review, findings]
summary: "Rolling list of Service Review findings for karakeep (CT 136). Run 1, 2026-11-01: 67 findings, none fixed yet. The dated review file holds the checklist, scorecard and sprint plan."
doc_type: reference
scope: service
service_name: karakeep
parent_doc: lab-standards/ARCHITECTURE.md
agent_context: true
permission_tier: n-a
last_verified: 2026-11-01
---

Page: PENDING

# Findings: karakeep

Process: lab-standards `docs/SERVICE-REVIEW.md` · Run log: lab-standards `service-reviews/review-log.jsonl` · Full review: [2026-11-01-service-review.md](2026-11-01-service-review.md)

| Run | Date | Kind | Counts | File |
|---|---|---|---|---|
| 1 | 2026-11-01 | review (read only, nothing changed on any server) | critical 0, high 4, medium 20, low 43 (67 total) | [2026-11-01-service-review.md](2026-11-01-service-review.md) |

Basis: karakeep HEAD `90baf74` (the working tree had 7 uncommitted files from another session, used as leads only), lab-standards `45dc495`. Every finding is `new`. IDs are never reused. Severity rulings by the coordinator are applied: BAK-01 high, BAK-02 medium, PAT-02 medium.

## Open findings

| ID | Sev | Title | Standard | Owner | Effort | Approval | Your call | Checked | State |
|---|---|---|---|---|---|---|---|---|---|
| BAK-01 | high | Karakeep has no logical backup and no written protect list; PBS is the only copy | Gate 7 | jason | L | remediate | Yes | verified | new |
| MON-01 | high | Nothing alerts if the workers, Meilisearch or the browser stop | LAB-STANDARDS §7 | chief | S | remediate | No | verified | new |
| DOC-01 | high | HEAD of the karakeep repo says tagging uses Ollama CT 112; live uses OpenRouter | SERVICE-REVIEW H | jason | S | none | Yes | verified | new |
| USE-03 | high | No logical backup (export) of the library | none | chief | M | remediate | No | verified | new |
| SEC-01 | medium | Root SSH login is enabled | LAB-STANDARDS §9 | jason | S | remediate | Yes | verified | new |
| SEC-02 | medium | Root password may exist and SSH password login is on by default | LAB-STANDARDS §9 | jason | S | remediate | Yes | unverified | new |
| SEC-03 | medium | Karakeep services and the browser run as root | LAB-STANDARDS §9 | jason | L | remediate | Yes | verified | new |
| PAT-01 | medium | Karakeep is two releases behind upstream, including a security release | LAB-DEC-022 | jason | M | destructive | Yes | verified | new |
| PAT-02 | medium | Three security updates are pending, two of them for the browser that renders saved pages | SERVICE-REVIEW A | jason | S | remediate | Yes | verified | new |
| BAK-02 | medium | The PBS backup has never been restored, and an upgrade whose rollback depends on it is pending | Gate 7 | jason | M | remediate | Yes | verified | new |
| BAK-04 | medium | No alert fires if the nightly PBS backup of CT 136 (or any guest) goes missing or stale | LAB-DEC-053 | a named lane (lab-wide: lane N or the prometheus repo) | S | remediate | No | verified | new |
| BAK-05 | medium | Whether the secrets needed to rebuild karakeep are in Dashlane is not known | Gate 7 | jason | S | none | Yes | unverified | new |
| HLT-02 | medium | Gate 8 baselines are all "not yet measured" | Gate 8 | jason | M | none | No | verified | new |
| SPD-05 | medium | BASELINES.md has no measured numbers (Gate 8 open) | Gate 8 | lane A | S | none | No | verified | new |
| INT-01 | medium | OpenRouter is a live dependency that no lab table declares; bookmark content already leaves the lab for tagging | SERVICE-REVIEW D | jason | S | none | Yes | unverified | new |
| MON-05 | medium | Full bookmark URLs, some from sign-in sessions, are shipped to Loki | none | jason | M | remediate | Yes | verified | new |
| DOC-02 | medium | lab-standards and Command Center data still say tagging calls Ollama; no OpenRouter dependency | SERVICE-REVIEW H | chief | S | none | No | verified | new |
| DOC-04 | medium | Working tree contradicts itself on the curated tag count (26 or 25) | SERVICE-REVIEW H | jason | S | none | Yes | unverified | new |
| DOC-07 | medium | Credential and vault references miss the OpenRouter key and the Hermes credential | SERVICE-REVIEW H | jason | S | none | Yes | unverified | new |
| USE-01 | medium | Karakeep exposes Prometheus metrics that nothing scrapes | LAB-DEC-061 | chief | M | remediate | Yes | verified | new |
| USE-02 | medium | Semantic search state is unknown; it is the main lever for the research library | none | jason | L | remediate | Yes | unverified | new |
| CC-03 | medium | Karakeep metrics are not scraped | LAB-DEC-061 | chief | M | remediate | No | verified | new |
| CC-05 | medium | OpenRouter spend cannot be split between Hermes and Karakeep | none | chief | M | none | No | unverified | new |
| CC-06 | medium | Generated dependency data in Command Center is stale | SERVICE-REVIEW H | chief | S | none | No | verified | new |
| SEC-04 | low | Port 3000 serves plain HTTP to the whole LAN, bypassing NPM and TLS | SERVICE-REVIEW B | jason | M | remediate | Yes | verified | new |
| SEC-05 | low | Host firewall state on CT 136 is unknown | SERVICE-REVIEW B | jason | S | none | No | unverified | new |
| SEC-06 | low | Unneeded services avahi and postfix are running | SERVICE-REVIEW B | jason | S | remediate | No | verified | new |
| SEC-07 | low | Whether new user sign-up is open is unknown | SERVICE-REVIEW B | jason | S | remediate | Yes | unverified | new |
| SEC-08 | low | No confirmed Dashlane copy for four secrets, and a plaintext root password file on the Proxmox host | LAB-STANDARDS §9 | jason | S | none | Yes | unverified | new |
| SEC-09 | low | The Cursor env file also holds the admin user and password | LAB-STANDARDS §9 | jason | S | none | Yes | verified | new |
| SEC-10 | low | No HSTS or frame protection headers from NPM host 53 | none | jason | S | remediate | No | verified | new |
| SEC-11 | low | Chromium sandbox flag and unprivileged container are doc claims only | LAB-STANDARDS §9 | jason | S | none | No | unverified | new |
| SEC-12 | low | Listeners with no known owner | SERVICE-REVIEW B | jason | S | none | No | unverified | new |
| PAT-03 | low | No automatic security patching on CT 136 | none | jason | S | remediate | Yes | verified | new |
| PAT-04 | low | `alloy` is held at 1.21.2 with no reason for staying held after the rollout | SERVICE-REVIEW A | jason | S | remediate | No | verified | new |
| PAT-05 | low | The version-tracking record is incomplete | LAB-STANDARDS §12 | jason | S | none | No | verified | new |
| BAK-03 | low | Per-guest PBS verify state for CT 136 cannot be seen | none | jason | S | none | No | unverified | new |
| HLT-01 | low | LxcSwapFull has been firing for CT 136 since 2026-10-29 and swap has stayed at about 92% or higher for 7 days | Gate 8 | jason | S | remediate | Yes | verified | new |
| HLT-03 | low | The SRE good-check has no stored reading | Gate 6 | lane N or chief | S | none | No | verified | new |
| HLT-04 | low | The Homarr tile and the 503-on-failure health behaviour were not checked | LAB-STANDARDS §7 | lane N or jason | S | none | No | unverified | new |
| HLT-05 | low | Load average reads 4.7 on a 2 vCPU guest while CPU pressure is low | none | lane N | S | none | No | verified | new |
| SPD-01 | low | Swap is nearly full on CT 136; RAM is not under pressure | Gate 8 | chief | S | remediate | No | verified | new |
| SPD-02 | low | Load average far above CPU use, cause not identified | none | chief | S | none | No | verified | new |
| SPD-03 | low | Kuma 115 (DNS path) has a 28 second response in 7 days; the IP path does not | SERVICE-REVIEW C | chief | S | none | No | verified | new |
| SPD-04 | low | Root disk grows about 110 MB a day | Gate 8 | chief | S | none | No | verified | new |
| INT-02 | low | OpenRouter spend cannot be tied to karakeep | SERVICE-REVIEW D | jason | S | none | Yes | verified | new |
| INT-03 | low | Dependency edges are not declared in both directions | SERVICE-REVIEW D | lane U | S | none | No | verified | new |
| INT-04 | low | The Discord link import is a manual laptop script (WISH-088) | none | jason | M | remediate | Yes | verified | moved to WISH-088 (existing) |
| MON-02 | low | The health check is shallow | LAB-STANDARDS §7 | upstream | L | none | No | unverified | new |
| MON-03 | low | Kuma only alerts on "down for 2 minutes"; slow and flapping on the name path is silent | LAB-DEC-078 | chief | S | none | No | unverified | new |
| MON-04 | low | Karakeep errors reach Loki but nothing alerts on them | none | chief | M | remediate | No | verified | new |
| DOC-03 | low | TOOLS.yaml OpenRouter `lab_use` names only Hermes | SERVICE-REVIEW H | chief | S | none | No | verified | new |
| DOC-05 | low | "three units" in health checks; live has four | SERVICE-REVIEW H | chief | S | none | No | verified | new |
| DOC-06 | low | Sync receipt `6a449af` is 244 commits behind lab-standards | SERVICE-REVIEW H | lane A | S | none | No | verified | new |
| DOC-08 | low | No LAB-STANDARDS section 12 upgrade backlog row for karakeep | LAB-STANDARDS §12 | lane A | S | none | No | verified | new |
| DOC-09 | low | App version is answerable live (public `/api/version`) but no doc says how to check it | SERVICE-REVIEW H | lane A | S | none | No | verified | new |
| DOC-10 | low | `last_verified` dates need a refresh after this review | SERVICE-REVIEW H | lane A | S | none | No | verified | new |
| DOC-11 | low | Doc claims this review could not check (privileged, onboot, features, port owners, Meilisearch version) | SERVICE-REVIEW H | jason | S | none | Yes | unverified | new |
| DOC-12 | low | Swap is 92% used and no doc mentions it | none | chief | S | none | No | verified | new |
| DOC-13 | low | Working tree leftovers: TROUBLESHOOTING names the Ollama variable; same day changelog entries have no times | SERVICE-REVIEW H | lane A | S | none | No | verified | new |
| USE-04 | low | Webhooks unused | none | chief | M | remediate | No | unverified | new |
| USE-05 | low | Per consumer API keys: only the Cursor key is documented | SERVICE-REVIEW I | jason | S | none | Yes | unverified | new |
| USE-06 | low | Lab slug tags as join keys | none | chief | M | remediate | Yes | unverified | new |
| CC-01 | low | Command Center does not use Karakeep public health and version endpoints | SERVICE-REVIEW J | chief | S | none | No | verified | new |
| CC-02 | low | No unit level state for the four units on the card | SERVICE-REVIEW J | chief | S | none | No | unverified | new |
| CC-04 | low | Deep links limited to the home page | SERVICE-REVIEW J | chief | S | none | No | unverified | new |
| CC-07 | low | No bookmark to lab service join | none | chief | L | none | Yes | unverified | new |

Fields in the table come from each part. Owner and Standard are reduced to one value in the Step 5 format; the part's longer wording stays in the detail below. Checked shows the first word of the part's Checked field, so a finding that is verified for one half and unverified for the other shows `verified` and says so in its detail.

## Finding details

Each block keeps the wording of the lane that wrote it (S for SEC, P for PAT, BAK and HLT, N for SPD, INT and MON, U for DOC, USE and CC). Lane A added only the cross-link line.

### SEC-01. Root SSH login is enabled

Category SEC · Severity medium · State new

- Standard: LAB-STANDARDS §9 · Severity: medium · Effort: S · Approval: remediate · Owner: jason · Checked: verified (config file; effective `sshd -T` not read)
- Evidence: `ssh karakeep "grep -v '^\s*#' /etc/ssh/sshd_config"` printed `PermitRootLogin yes`; `ls -la /etc/ssh/sshd_config.d` is empty; no `Match` block.
- Your call: yes. WISH-236 records that Jason deferred the fix to this review. That is not approval to change the server; the fix needs approval of SEC-01 by ID in a fix run.
- Fix: add `/etc/ssh/sshd_config.d/10-yingson-keyonly.conf` with `PermitRootLogin prohibit-password`, run `sshd -t`, reload, then confirm `ssh karakeep whoami` with the lab key first. Undo: delete the file and reload. Console (`pct enter`) is the fallback.
- Links: WISH-236 (defers the work to this review, not an approval), scanopy SEC-05 (same change, different service), WISH-001, WISH-002.

### SEC-02. Root password may exist and SSH password login is on by default

Category SEC · Severity medium · State new

- Standard: LAB-STANDARDS §9 · Severity: medium · Effort: S · Approval: remediate · Owner: jason · Checked: unverified
- Evidence: not shown. `passwd -S root` and `sshd -T` need sudo (not run). Sources that agree: WISH-236 (2026-10-31, `P` flag) and `karakeep/ARCHITECTURE.md` line 168.
- What would verify it: `ssh karakeep "sudo sshd -T | grep -E 'permitrootlogin|passwordauthentication|pubkeyauthentication'"` and `sudo passwd -S root` (values are flags only).
- Your call: yes. Allow the sudo reads, or accept it as unverified until the fix run?
- Fix: the same drop-in as SEC-01 plus `PasswordAuthentication no`. Optionally lock the root password (`passwd -l root`) after the key works. Undo: remove the drop-in, `passwd -u root`.
- Links: WISH-236, SEC-01.
- Cross-links (lane A): SEC-05 (the sudo reads), SEC-11, SEC-12, DOC-11

### SEC-03. Karakeep services and the browser run as root

Category SEC · Severity medium · State new

- Standard: LAB-STANDARDS §9 · Severity: medium · Effort: L · Approval: remediate · Owner: jason · Checked: verified
- Evidence: `ssh karakeep 'ps -eo pid,user,comm'` shows `node`, `meilisearch`, `chromium` under `root`. The `--no-sandbox` flag and the unprivileged container are split out as SEC-11.
- Why it matters: the browser renders untrusted web pages. A browser escape would land as root inside the guest. The unprivileged container (SEC-11) may limit the blast radius, but this is still more than least privilege.
- Your call: yes. Accept the community script's design, or plan a non-root user for the units (needs a plan, LAB-DEC-080)?
- Fix: a plan, not a quick change. Run the units as a dedicated user, which also lets Chromium keep its sandbox. Undo: restore the unit files from the PBS snapshot.
- Links: WISH-265 (proposed).
- Cross-links (lane A): SEC-11

### SEC-04. Port 3000 serves plain HTTP to the whole LAN, bypassing NPM and TLS

Category SEC · Severity low · State new

- Standard: SERVICE-REVIEW B · Severity: low · Effort: M · Approval: remediate · Owner: jason · Checked: verified
- Evidence: laptop `curl -s -o /dev/null -w "%{http_code}" http://192.168.30.33:3000/signin` returned 200; `/api/v1/bookmarks` returned 401. `ss -tlnu` shows `*:3000`.
- The reason is valid (NPM is the front door) but any LAN client can also use the IP over plain HTTP, which carries a session cookie or API key in the clear. `TROUBLESHOOTING.md` expects people to open the IP for diagnosis, so closing it is a choice.
- Your call: yes. Limit port 3000 to NPM (`192.168.30.182`) with a guest firewall rule, or accept?
- Fix: allow tcp 3000 from NPM only in nftables. Undo: remove the rule. Pairs with SEC-05.
- Links: SEC-05.

### SEC-05. Host firewall state on CT 136 is unknown

Category SEC · Severity low · State new

- Standard: SERVICE-REVIEW B · Severity: low · Effort: S · Approval: none · Owner: jason · Checked: unverified
- Evidence: `systemctl is-active nftables ufw` gives nftables active, ufw inactive; `/etc/nftables.conf` exists. The ruleset needs `sudo nft list ruleset` (not run).
- Your call: no. Part of the sudo-reads question in SEC-02.
- Fix: read the ruleset in the fix run, then decide with SEC-04.
- Links: SEC-04.
- Cross-links (lane A): SEC-02 (the sudo reads question), SEC-04

### SEC-06. Unneeded services avahi and postfix are running

Category SEC · Severity low · State new

- Standard: SERVICE-REVIEW B · Severity: low · Effort: S · Approval: remediate · Owner: jason · Checked: verified
- Evidence: `ss -tlnu` rows in section 2. `systemctl list-units --state=running` shows `avahi-daemon` and `postfix`. Neither is in the docs. Avahi answers mDNS on the LAN. Postfix is loopback only.
- Your call: no.
- Fix: if avahi and postfix are not needed, disable them in the fix run. Undo: re-enable them.
- Links: SEC-12.

### SEC-07. Whether new user sign-up is open is unknown

Category SEC · Severity low · State new

- Standard: SERVICE-REVIEW B · Severity: low · Effort: S · Approval: remediate · Owner: jason · Checked: unverified (a sign-up test needs a POST or root read of the env file)
- Evidence: not tested. The test needs a POST (forbidden in a review run) or the env file (root only). Paperclip had the same gap and closed it (WISH-135).
- Your call: yes. Should open sign-up be off? If a second account is wanted, a one-time toggle is needed.
- Fix: set the app's sign-up switch off in the guest env file and restart `karakeep-web`. Undo: switch it back on.
- Links: WISH-135 (same idea, Paperclip).

### SEC-08. No confirmed Dashlane copy for four secrets, and a plaintext root password file on the Proxmox host

Category SEC · Severity low · State new

- Standard: LAB-STANDARDS §9 · Severity: low · Effort: S · Approval: none · Owner: jason · Checked: unverified
- Evidence: `karakeep/ARCHITECTURE.md` line 168: the container root password exists only as `/root/karakeep-lxc-root.password` on the Proxmox host (not read, needs sudo). Vault refs for root, admin, Cursor key are in Table 2, and the OpenRouter ref (line 142) is not.
- Your call: yes. Which of root password, admin password, Cursor key and OpenRouter key are in Dashlane? If the root one is, the host file can be removed (it is the same secret kept in a second place).
- Fix: Jason confirms; then add the missing `vault://` ref to Table 2 and, if safe, remove the host file after a check that it is also in Dashlane. Undo: none needed after confirmation.
- Links: WISH-224 (no repo leak found, nothing added), SECRETS-RULE.md.
- Cross-links (lane A): BAK-05, DOC-07, USE-05 (same Dashlane question, different severities, see Overlaps)

### SEC-09. The Cursor env file also holds the admin user and password

Category SEC · Severity low · State new

- Standard: LAB-STANDARDS §9 · Severity: low · Effort: S · Approval: none · Owner: jason · Checked: verified (names only; the file was not opened)
- Evidence: `grep -o '^[A-Z_][A-Z0-9_]*=' karakeep.env` prints `KARAKEEP_ADMIN_USER` and `KARAKEEP_ADMIN_PASSWORD`. `ARCHITECTURE.md` line 147 says the file is only the URL and API key.
- Why: an agent with the Cursor file can sign in as the admin, which goes past the read-only API key tier.
- Your call: yes. Remove the two admin names from the Cursor file, or fix the doc to say they are there?
- Fix: Jason deletes those two lines, keeps the password in Dashlane. Undo: paste them back.
- Links: LAB-STANDARDS §9, PERMISSION-TIERS.md.

### SEC-10. No HSTS or frame protection headers from NPM host 53

Category SEC · Severity low · State new

- Standard: none · Severity: low · Effort: S · Approval: remediate · Owner: jason · Checked: verified
- Evidence: `curl -sI https://karakeep.yingson.com/signin` showed `HTTP/1.1 200 OK` and `Server: openresty`, and none of `Strict-Transport-Security`, `X-Frame-Options`, `Content-Security-Policy`, `X-Content-Type-Options` (my grep matched on those names only). Low value for a Tailscale only name.
- Your call: no.
- Fix: NPM host 53 "HSTS" toggle and a custom header block. Undo: switch off.
- Links: none.

### SEC-11. Chromium sandbox flag and unprivileged container are doc claims only

Category SEC · Severity low · State new

- Standard: LAB-STANDARDS §9 · Severity: low · Effort: S · Approval: none · Owner: jason · Checked: unverified (`sudo systemctl cat karakeep-browser` for `--no-sandbox`, and `sudo pct config 136` for `unprivileged: 1`)
- Evidence: `karakeep/ARCHITECTURE.md` line 208 says unprivileged container and `--no-sandbox`. `systemctl cat` returns Permission denied for `jason`.
- Your call: no. Part of the sudo-reads question in SEC-02.
- Fix: read both in the fix run. Links: SEC-03, WISH-265.
- Cross-links (lane A): DOC-11, SEC-02

### SEC-12. Listeners with no known owner

Category SEC · Severity low · State new

- Standard: SERVICE-REVIEW B · Severity: low · Effort: S · Approval: none · Owner: jason · Checked: unverified (`sudo ss -tlnup` names the owners of udp 46549 and 55753, tcp 12345 and 34943)
- Evidence: `ss -tlnu` rows in section 2. tcp 12345 is probably Alloy's default port, unproven.
- Your call: no.
- Fix: read the owners, document each in ARCHITECTURE. Links: SEC-06.
- Cross-links (lane A): DOC-11, USE-01 (the worker metrics port may be one of the loopback ports)

### PAT-01. Karakeep is two releases behind upstream, including a security release

Category PAT · Severity medium · State new

- Category PAT · Standard: LAB-DEC-022 · Owner: jason · Severity: **medium** · Effort: M (restart, migration, backup first) · Checked: verified for versions, **unverified** for whether the Node CVEs reach a native Node 22 install · Approval: destructive (upgrade) · Your call: **Yes.** Upgrade now or wait? The upgrade signs everyone out once, lowercases emails, and its rollback is an untested restore.
- Evidence: `/api/version` 0.33.2 on the guest; GitHub releases latest v0.34.1 (2026-10-22), notes above. Reachable by LAN and Tailscale only (LAB-STANDARDS section 11), which lowers exposure.
- Fix: do BAK-02 first (PBS snapshot, scratch restore, app check), then the community-script update, then re-check `/api/version` and the sign-in. Undo: restore the pre-upgrade snapshot.
- Links: LAB-STANDARDS section 12, SERVICE-REVIEW fix run, BAK-02. State: new.

### PAT-02. Three security updates are pending, two of them for the browser that renders saved pages

Category PAT · Severity medium · State new

- Category PAT · Standard: SERVICE-REVIEW A · Owner: jason · Severity: **medium** (not high: karakeep is not public, public DNS returns NXDOMAIN and access is LAN and Tailscale only, so "exposed service missing a security fix" does not apply) · Effort: S (no guest restart; the `karakeep-browser` unit needs a restart to load new Chromium, so say M if that is counted) · Checked: verified · Approval: remediate · Your call: Yes, apply now or batch with PAT-01?
- Evidence: `apt list --upgradable` on the guest lists chromium and chromium-common 156.0.8078.73-1~deb13u1 and libnss3 2:3.110-1+deb13u5, all from `stable-security`. `apt_security_upgrades_pending` is 3. `unattended-upgrades` not installed. Running Chromium PID 12257 is 24 days old.
- Fix: `sudo apt-get upgrade` for those packages in a fix run, then restart `karakeep-browser`. Undo: PBS snapshot first; apt downgrade by version if needed.
- Links: PAT-03, WISH-256 (proposed). State: new.
- Cross-links (lane A): PAT-01, PAT-03, BAK-02 (snapshot first)

### PAT-03. No automatic security patching on CT 136

Category PAT · Severity low · State new

- Category PAT · Standard: none · Owner: jason · Severity: low · Effort: S · Checked: verified (`dpkg -l unattended-upgrades` returns "no packages found") · Approval: remediate · Your call: Yes. Does the lab want unattended security updates on guests, or a patch day?
- Evidence: package absent, `/etc/apt/apt.conf.d` has only 01autoremove, 20listchanges, 70debconf, so pending updates wait for a person. Other guests were not checked; this may be a lab-wide choice.
- Fix: a lab decision first. Proposed WISH-256.
- State: new.

### PAT-04. `alloy` is held at 1.21.2 with no reason for staying held after the rollout

Category PAT · Severity low · State new

- Category PAT · Standard: SERVICE-REVIEW A · Owner: jason · Severity: low · Effort: S · Checked: verified · Approval: remediate · Your call: no
- Evidence: `apt-mark showhold` prints `alloy`; candidate 1.21.3-1. `loki/docs/ALLOY-ROLLOUT.md` lines 38 and 49 say "pinned to 1.21.2-1 and held". The hold is documented as the rollout pin, not as a reason to stay.
- Fix: loki repo decides (lane N or the loki owner); record the reason or lift the hold in the lab-wide Alloy bump. Not a karakeep-only fix.
- State: new.

### PAT-05. The version-tracking record is incomplete

Category PAT · Severity low · State new

- Category PAT · Standard: `LAB-STANDARDS §12` · Owner: jason (doc-only, lane A or U writes it) · Severity: low · Effort: S · Checked: verified for the missing backlog row (D0 grep plus my read of the table) and for TOOLS.yaml fields; **unverified** for Meilisearch and Node versions (401, and no allowlisted read) · Approval: none · Your call: no
- Evidence: no karakeep row in the section 12 upgrade backlog; TOOLS.yaml has `version: 0.33.2` and `source`, with no pinning or version-checked fields. Meilisearch 1.54.3 (doc) and Node 22 (doc) are not confirmed live.
- Fix: add the backlog row above; record "floating (script update path), Node 22" and a checked date `2026-11-01`. Lane A writes karakeep; lab-standards text is returned in the final reply.
- State: new.
- Cross-links (lane A): DOC-08 (same missing section 12 row)

### BAK-01. Karakeep has no logical backup and no written protect list; PBS is the only copy

Category BAK · Severity high · State new

- Category BAK · Standard: Gate 7 · Owner: jason (decision), then a named lane · Severity: **high** (backup gap on data Jason would miss: the whole library and weeks of tag work) · Effort: L (needs a plan: Kopia client plus a SQLite dump; LAB-DEC-080 means a plan, not a build) · Checked: verified · Approval: remediate · Your call: **Yes.** Add Kopia to CT 136, or write "no additions" and accept PBS only?
- Evidence: no Kopia source (`kopia_source_*` empty for karakeep); no protect list in LAB-STANDARDS section 6; ARCHITECTURE.md section 10 says "no separate database dump". PBS snapshots of a running SQLite are crash-consistent, not application-consistent. The PBS datastore is on the NAS, so one NAS failure removes both the live data's copy and the backup store (LAB-DEC-029).
- Fix: write the protect list (SQLite via backup API, assets, `/etc/karakeep`), enroll the Kopia client, then a freshness check. Undo: remove the client.
- Links: WISH-014, WISH-010, LAB-DEC-053, LAB-DEC-088. State: new, linked to WISH-014.
- Cross-links (lane A): USE-03 (same fact, rated high in both)

### BAK-02. The PBS backup has never been restored, and an upgrade whose rollback depends on it is pending

Category BAK · Severity medium · State new

- Category BAK · Standard: Gate 7 · Owner: jason (approval), then a named lane · Severity: **medium** (no high trigger fits: PBS backups exist and run; the untested restore matters because PAT-01 uses it as the rollback) · Effort: M · Checked: verified · Approval: remediate (scratch CT, network removed, then destroyed; needs Jason's OK, SERVICE-REVIEW ground rule 9) · Your call: **Yes.** OK to restore the newest snapshot to a scratch CT?
- Evidence: no karakeep line in `restore-tests/restore-log.jsonl` (43 lines). The runbook has no restore steps. Scanopy did this on 2026-10-31 as the pattern (scratch CT, net0 removed, app check, destroyed).
- Fix: restore the newest snapshot to a scratch CT with the network removed, check `/api/health`, sign-in and the bookmark count, destroy it, log it, and write the restore steps into the runbook. A scratch restore is not R4 on its own.
- Links: Gate 7, PAT-01. State: new.

### BAK-03. Per-guest PBS verify state for CT 136 cannot be seen

Category BAK · Severity low · State new

- Category BAK · Standard: none (WISH-153) · Owner: jason · Severity: low · Effort: S · Checked: **unverified** · Approval: none · Your call: no
- Evidence: Prometheus has store-wide `pbs_snapshots_unverified` (0) and `pbs_snapshots_verify_failed` (0) and `verify-weekly` ok. No per-guest series. `pvesm list` or the PBS UI would show it (sudo or PBS login).
- Fix: WISH-153 adds a per-snapshot view. Until then, rely on the store-wide counts.
- Links: WISH-153. State: new.

### BAK-04. No alert fires if the nightly PBS backup of CT 136 (or any guest) goes missing or stale

Category BAK · Severity medium · State new

- Category BAK · Standard: LAB-DEC-053 · Owner: a named lane (lab-wide, lane N or the prometheus repo) · Severity: **medium** (a failure that would not alert; kept at medium because PBS tracks job health and nothing has failed) · Effort: S · Checked: verified for Prometheus rules; **unverified** for any Kuma or Alertmanager path outside Prometheus rules · Approval: remediate · Your call: no
- Evidence: the live Prometheus rules list has no expression using `pbs_group_last_backup_timestamp_seconds`, `pbs_job_last_run_ok` or `pve_not_backed_up_total`. The metrics exist and are healthy now. INC-20260415-01 was a silent backup failure.
- Fix: an alert such as `time() - pbs_group_last_backup_timestamp_seconds > 36h` for any group, routed through Alertmanager to `#alerts`. Lab-wide, so listed once here and not repeated per service.
- Links: INC-20260415-01, WISH-257 (proposed). State: new.
- Cross-links (lane A): scanopy FINDINGS lab-standards/MON-01 (same missing PBS age rule, already open)

### BAK-05. Whether the secrets needed to rebuild karakeep are in Dashlane is not known

Category BAK · Severity medium · State new

- Category BAK · Standard: Gate 7 · Owner: jason · Severity: medium · Effort: S · Checked: **unverified** (ask Jason, per SERVICE-REVIEW F) · Approval: none · Your call: **Yes.** Do Dashlane copies exist for the admin login, NEXTAUTH_SECRET and the OpenRouter key (names only, no values)?
- Evidence: inventory names a vault ref for the root password only. `/etc/karakeep` is root only, so I could not list its variable names without sudo.
- Fix: Jason confirms, and the vault paths are written in the docs. A restore from PBS brings the secrets back, but a rebuild from scratch would not.
- Links: VAULT-REFERENCE-CONVENTION. State: new.
- Cross-links (lane A): SEC-08, DOC-07, USE-05

### HLT-01. LxcSwapFull has been firing for CT 136 since 2026-10-29 and swap has stayed at about 92% or higher for 7 days

Category HLT · Severity low · State new

- Category HLT · Standard: Gate 8 · Owner: jason (approves the rule change, WISH-186) · Severity: low · Effort: S (alert tuning) or M (more RAM, needs a restart) · Checked: verified · Approval: remediate · Your call: **Yes.** Approve the WISH-186 rule tuning, or give the guest more RAM?
- Evidence: Alertmanager `LxcSwapFull` active since 2026-10-29T11:36:42Z; swap 493,563,904 of 536,870,912 bytes (92%); min over 7 days 492,687,360 bytes; `free -m` 805 MiB used, 2428 free, 3290 available; memory PSI 0.00; `GuestSwapHigh` (needs swap-in over 50 pages/s) is not firing. That reads as old pages parked in swap, not pressure, which matches the lane AO finding in `HANDOFF-2026-10-28.md` (97% on 10-28). 4 GiB RAM, two workers and a Chromium: 7-day peak memory was 4.0 GiB (D0), so a spike can still push it. Lane N's SPD section may add the speed view; this finding covers the alert and health.
- Fix: approve the WISH-186 rule, or record a Gate 8 swap baseline of "stable at about 90% with PSI 0", or raise RAM. Undo: revert the rule.
- Links: WISH-186, YIN-174, Gate 8. State: new.
- Cross-links (lane A): SPD-01 (sizing view), DOC-12 (doc line)

### HLT-02. Gate 8 baselines are all "not yet measured"

Category HLT · Severity medium · State new

- Category HLT · Standard: Gate 8 · Owner: jason or a named lane · Severity: medium (blocks R4; no baseline means no warning or critical value to alert on) · Effort: M · Checked: verified (`BASELINES.md`, 48 lines, every field "not yet measured") · Approval: none · Your call: no
- Evidence: `karakeep/BASELINES.md` lines 36 to 54. This review's own reads (swap 92%, disk 59%, RAM 805 MiB used, CPU PSI 0.14, load) can seed it.
- Fix: write one idle window with thresholds. Lane A writes it into karakeep.
- Links: Gate 8, HLT-01. State: new.
- Cross-links (lane A): SPD-05 (same BASELINES fix)

### HLT-03. The SRE good-check has no stored reading

Category HLT · Severity low · State new

- Category HLT · Standard: Gate 6 · Owner: a named lane (lane N) or chief · Severity: low · Effort: S · Checked: verified · Approval: none · Your call: no
- Evidence: `SRE-AGENT-CATALOG.md:185` says "Reading not stored as a catalog baseline". I ran the check today and it passes (200 on `/signin`, three units active), so the reading can be stored now.
- Fix: store the 2026-11-01 reading. `watch: no` stays until then.
- State: new.
- Cross-links (lane A): DOC-09, DOC-05, MON-01

### HLT-04. The Homarr tile and the 503-on-failure health behaviour were not checked

Category HLT · Severity low · State new

- Category HLT · Standard: `LAB-STANDARDS §7` · Owner: lane N or jason · Severity: low · Effort: S · Checked: **unverified** · Approval: none · Your call: no
- Evidence: no allowlisted live read for Homarr; `/api/health` 200 seen but 503 not testable without stopping a unit (ground rule 9).
- Fix: Jason opens YingsonDash and confirms the tile.
- Links: LAB-STANDARDS §8 (Homarr tile). State: new.

### HLT-05. Load average reads 4.7 on a 2 vCPU guest while CPU pressure is low

Category HLT · Severity low · State new

- Category HLT · Standard: none · Owner: lane N (SPD) · Severity: low · Effort: S · Checked: verified for the reading, **unverified** for the cause · Approval: none · Your call: no
- Evidence: `uptime` 10:05, load 4.71, 5.28, 5.52; `/proc/pressure/cpu` some avg300 0.14; `ps` shows no busy process. In an LXC the load average can come from the host. Left to SPD to confirm or drop.
- State: new.
- Cross-links (lane A): SPD-02 (same load reading)

### SPD-01. Swap is nearly full on CT 136; RAM is not under pressure

Category SPD · Severity low · State new

- Standard: Gate 8. Owner: chief (lane P owns the alert; this is the sizing view). Severity: low. Effort: S. Approval: remediate. Your call: no.
- Evidence: `free -m` on the guest: swap 470 of 512 MiB used, 41 free; Mem available 3290 of 4096 MiB. Prometheus `min_over_time(node_memory_SwapFree_bytes[7d])` = 0, so swap hit full at least once this week. `/proc/pressure/memory` avg10/60/300 all 0.00. `vmstat 1 3`: si 33/4/0, so swap-in is near zero. Alertmanager: `LxcSwapFull` (severity info) firing for `vmid 136` since 2026-10-29T11:36Z; `GuestSwapHigh` (needs swap-in rate above 50 pages/s) not firing.
- Reading: the swap holds cold pages, not live thrash. The 4 GiB RAM size is not the limit. Whether to grow swap or lower swappiness is a guess until measured (unverified). Largest residents: node 354 MB, next-server 234 MB, meilisearch 177 MB, chromium 160 MB plus children (`ps` sorted by %mem).
- Checked: verified. Fix: lane P decides the alert. For sizing, leave RAM at 4 GiB, and record "swap holds cold pages" in BASELINES. Undo: n/a.
- Links: LxcSwapFull alert, WISH-186. State: new.
- Cross-links (lane A): HLT-01, DOC-12

### SPD-02. Load average far above CPU use, cause not identified

Category SPD · Severity low · State new

- Standard: none. Owner: chief. Severity: low. Effort: S. Approval: none. Your call: no.
- Evidence: `uptime` load 4.43, 5.18, 5.62 on 2 vCPU; Prometheus `node_load5` 7-day max 40.63, mean 6.30. `vmstat 1 3`: CPU idle 83 to 93 percent, wa 0 to 1, but cs 80k to 89k per second and in 36k to 50k per second. `/proc/pressure/io` avg300 0.09, cpu avg300 0.09. No process in D state in one `ps` sample. D0 7-day CPU average 1.50 percent, peak 88 percent.
- Reading: the load number looks inflated for a guest this idle. A context switch rate near 85k per second on an idle guest is unusual. The cause (chromium, Next.js timers, Alloy, or the LXC load-average accounting) is unverified. Finding it needs `pidstat` or `perf`, which are not on the allowlist.
- Checked: verified (numbers); cause unverified. Fix: a later run with `pidstat -w` allowed, read only. Links: none. State: new.
- Cross-links (lane A): HLT-05

### SPD-03. Kuma 115 (DNS path) has a 28 second response in 7 days; the IP path does not

Category SPD · Severity low · State new

- Standard: SERVICE-REVIEW C. Owner: chief. Severity: low. Effort: S. Approval: none. Your call: no.
- Evidence: Prometheus `max_over_time(monitor_response_time[7d])`: 115 = 27918 ms, 116 = 209 ms (re-queried 2026-11-01 18:26 UTC; the 7-day window moves, so the value can change; an earlier read this session gave 306 ms). Averages 43 ms and 29 ms. `changes(monitor_status[7d])`: 115 = 5, 116 = 0. `avg_over_time(monitor_status[7d])` for 115 = 1.0006 (a value above 1 means some samples were pending, status 2); no down alert fired. Kuma state now: 115 up 28 ms, 116 up 42 ms, cert 84 days.
- Reading: the name path adds a failure source (AdGuard, NPM 53, TLS) that the IP path lacks. The app answered fine on the IP path at the same time. The timestamp of the spike was not recovered (a range query for samples over 5000 ms returned nothing in my window, so the spike may sit at a step boundary); cause unverified.
- Checked: verified (numbers); cause unverified. Fix: read Kuma's heartbeat history for monitor 115 in a later run. Links: MON-03. State: new.

### SPD-04. Root disk grows about 110 MB a day

Category SPD · Severity low · State new

- Standard: Gate 8. Owner: chief (lane P owns BAK and sizing alerts). Severity: low. Effort: S. Approval: none. Your call: no.
- Evidence: `df -h /` on the guest: 15G, 8.2G used, 5.8G avail, 59 percent. D0 recorded 56 percent earlier today. Prometheus `delta(node_filesystem_avail_bytes{mountpoint="/"}[7d])` = -771 MB (about 110 MB a day). `GuestRootDiskHigh` fires above 85 percent for 15 minutes, which is about 4.5 GB of headroom, so roughly 40 days at this rate. `du` of `/opt/karakeep_data` is not readable by jason (shows 4 KB; root only), so what is growing is unverified.
- Reading: expected for a growing archive (full page copies, screenshots, Meilisearch). The alert exists and would fire. Over-sizing is not an issue here; the disk is the tightest resource.
- Checked: verified (numbers); cause unverified. Fix: lane P decides whether to grow the disk. Record the growth rate in BASELINES. Links: LAB-DEC-062. State: new.

### SPD-05. BASELINES.md has no measured numbers (Gate 8 open)

Category SPD · Severity medium · State new

- Standard: Gate 8. Owner: a named agent lane (lane A, the only writer to karakeep). Severity: medium. Effort: S. Approval: none. Your call: no.
- Evidence: `karakeep/BASELINES.md` (HEAD and working tree) says "not yet measured" for health, CPU, RAM, disk and swap, and "Do not invent a threshold from the 4 GB allocation".
- Numbers this run measured, for the file (labelled as one sample, laptop on LAN, 5 runs each):

| Metric | Value | Source |
|---|---|---|
| Name path `/signin` total | 67, 81, 131, 159, 216 ms; median 131 ms | `curl -w` x5 to `https://karakeep.yingson.com/signin` |
| IP path `/signin` total | 22, 54, 65, 92, 110 ms; median 65 ms | `curl -w` x5 to `http://192.168.30.33:3000/signin` |
| NPM and TLS cost | about 66 ms median (name minus IP), TLS handshake about 20 to 50 ms inside it | same runs |
| `/api/health` total | 23, 51, 163 ms (3 runs); body `{"status":"ok","message":"Web app is working"}` | curl |
| Kuma response, 7 d average | 115: 43 ms, 116: 29 ms | Prometheus |
| Memory available | 3.29 GiB of 4 GiB (guest); 7-day minimum 3.24 GiB | `free`, Prometheus |
| Swap used | 470 of 512 MiB; 7-day minimum free 0 | SPD-01 |
| Load average | 1.50 percent CPU mean (D0); load5 mean 6.30, max 40.63 | Prometheus |
| Disk | 59 percent, growth about 110 MB a day | SPD-04 |

- Checked: verified. Fix: lane A writes these into BASELINES and sets `last_verified`. The load figures are a caution (SPD-02), not a threshold. Links: BASELINES-SCHEMA. State: new.
- Cross-links (lane A): HLT-02

### INT-01. OpenRouter is a live dependency that no lab table declares; bookmark content already leaves the lab for tagging

Category INT · Severity medium · State new

- Standard: SERVICE-REVIEW D. Owner: jason (decision), lane U (docs). Severity: medium. Effort: S for the doc; the privacy decision is Jason's. Approval: none. Your call: yes.
- Evidence: Loki 7 days, `{service="karakeep",unit="karakeep-web.service"} |~ "(?i)openrouter"` = 312 lines (D0 counted 316 across all units, and 0 for `11434`). `SERVICE-DEPENDENCIES.md:137` says Ollama CT 112 for tagging, and the `TOOLS.yaml` OpenRouter `lab_use` names only Hermes. The working tree `ARCHITECTURE.md` and `RUNBOOK.md` say OpenRouter `google/gemini-2.5-flash-lite` for text and images (RUNBOOK Tagging section, line 85 of the working tree). The guest env cannot be read, so the live model name, and exactly which fields are sent, are unverified. Whether images are sent is also unverified (the working tree says the image model is set).
- What this means: saving a bookmark sends page text, and possibly images, to OpenRouter and from there to Google. The 844 bookmarks retagged on 2026-10-12 went the same way (working-tree CHANGELOG, a lead). WISH-244 already asks whether agents may read bookmark text; the tagging path answers part of it today.
- Checked: unverified for what is sent (model name, fields, images); the OpenRouter log lines are verified. Env file read needs sudo on CT 136.
- Fix: lane U adds OpenRouter to karakeep's row in SERVICE-DEPENDENCIES (Ollama removed) and to the OpenRouter `lab_use`. Jason decides whether bookmarks of any kind must stay out of OpenRouter (for example private or logged-in pages, see MON-05). Undo: n/a. Links: WISH-244, WISH-189, WISH-060, D0 section 3. State: new.
- Cross-links (lane A): DOC-01, DOC-02, INT-03, CC-06 (the Ollama versus OpenRouter drift)

### INT-02. OpenRouter spend cannot be tied to karakeep

Category INT · Severity low · State new

- Standard: SERVICE-REVIEW D (one key per consumer). Owner: jason. Severity: low. Effort: S. Approval: none. Your call: yes (does karakeep have its own OpenRouter key?).
- Evidence: Prometheus series for `job="openrouter"` carry only the labels `host="hermes"`, `scope="personal"`, `service="openrouter"`, `instance`, `job`, `reset`, `alertname`, `alertstate`, `severity` (the last three only on ALERTS series). There is no per-key or per-consumer label. `openrouter_balance_usd` is one account value (45.31 at read time). Alerts that exist: `OpenRouterBalanceLow`, `OpenRouterBalanceCritical`, `OpenRouterDailySpendHigh` (above 1.5 USD a day), `OpenRouterKeyLimitHigh` (above 0.8 of the key limit). The laptop has `karakeep-openrouter.env` (name only listed), but whether the guest uses the same key as Hermes is unverified.
- Reading: a runaway library retag would show up as account spend, not as karakeep spend. The 844-item retag cost is not recoverable from these metrics.
- Checked: verified for the metric labels; unverified whether karakeep has its own key (guest env read needs sudo).
- Fix: a separate OpenRouter key for karakeep with its own limit, and a per-key label in the exporter (WISH-259). Links: WISH-259, INT-01. State: new.
- Cross-links (lane A): CC-05 (same spend question)

### INT-03. Dependency edges are not declared in both directions

Category INT · Severity low · State new

- Standard: SERVICE-REVIEW D (edges both ways). Owner: lane U. Severity: low. Effort: S. Approval: none. Your call: no.
- Evidence: `SERVICE-DEPENDENCIES.md:137` says "Nothing else calls Karakeep" and lists no OpenRouter, Loki or Alloy. Live: the laptop holds `karakeep.env`, `karakeep-hermes.env` and `karakeep-openrouter.env` under `~/.cursor/mcps` (names only), so at least Hermes and Cursor have or are meant to have a credential. `SERVICE-INVENTORY.md:295` lists the API as `rest`, `api-key`, MCP `needs-wrapper`, tier `read-only`. Live: `GET /api/v1/bookmarks` without a key returns 401 on `192.168.30.33:3000`, so the API answers and wants a key. Logs flow to Loki through Alloy (unit `alloy.service` active; Loki `service="karakeep"` present, D0). The Discord link archive on the laptop feeds Karakeep by script (INT-04).
- Checked: verified for the 401 and the SERVICE-DEPENDENCIES text; unverified whether Hermes calls karakeep (CT 139 credential read needs root).
- Fix: lane U adds edges: karakeep to OpenRouter, to Loki (Alloy), and from the laptop import script and Hermes (read key). Whether Hermes actually calls Karakeep today is unverified (CT 139 credential store is root only). Links: INT-01. State: new.
- Cross-links (lane A): DOC-02, DOC-07

### INT-04. The Discord link import is a manual laptop script (WISH-088)

Category INT · Severity low · State moved to WISH-088 (existing)

- Standard: none. Owner: jason (decision on where it runs). Severity: low. Effort: M. Approval: remediate (new schedule). Your call: yes.
- Evidence: `RUNBOOK.md` "Import new Discord links": run `python ...\scripts\import-to-karakeep.py` on the laptop. The script reads the Discord JSON dump at `C:\Users\thedu\discord-link-archive\items` (845 files today), uses the REST API with a bearer key from `karakeep.env`, creates a list named "Discord links", and records progress in `import-state.json` (860 ids recorded as done, file last changed 2026-10-21). It prints counts only. Nothing alerts when the importer has not run; no schedule exists. The producer is the "Grok bot" that writes the JSON files (script docstring); where that bot runs is not documented in this repo (unverified).
- Reading: the weak points are the laptop dependency, the single API key on the laptop, and silence when it stops. A scheduled run belongs next to whatever hosts the Discord archive; moving it needs a plan (LAB-DEC-080).
- Checked: verified for the script, counts and runbook text; unverified where the Grok bot runs (needs Jason).
- Fix: see WISH-088 (add the points above) and the Hermes route in the section D8 list. Do not build in a review run. State: moved to WISH-088 (existing).

### MON-01. Nothing alerts if the workers, Meilisearch or the browser stop

Category MON · Severity high · State new

- Standard: LAB-STANDARDS §7. Owner: chief. Severity: high (a failure that would not alert). Effort: S. Approval: remediate (new alert rule on the Prometheus host). Your call: no.
- Evidence: Kuma 115 and 116 are `http` monitors with no keyword, URLs `https://karakeep.yingson.com/` and `http://192.168.30.33:3000/` (`karakeep/scripts/add-kuma-karakeep.py` lines 6 to 22, monitor 116 at lines 23 to 29; live status both up per Prometheus `monitor_status`). `GET /api/health` returns a fixed `{"status":"ok","message":"Web app is working"}` with 200 (checked 3 times); it does not touch SQLite, Meilisearch or the worker queue (no live evidence that it does; the body says only the web app). The web process answers while the workers and Meilisearch can be stopped; then saves never crawl and search is empty (TROUBLESHOOTING sections "workers down", "search returns nothing"). Prometheus has `node_systemd_unit_state{service="karakeep"}` = 1 for `karakeep-web`, `karakeep-workers`, `karakeep-browser`, `meilisearch` and `alloy`, but the alert list (the full alerting rule list was read) has no rule on those unit states. The SRE catalog good-check also lists the three units, with no stored reading (`SRE-AGENT-CATALOG.md:185`).
- Checked: verified (monitor types, health body, unit-state series, rule list); the SRE good-check reading is not stored.
- Fix: a Prometheus rule such as `node_systemd_unit_state{service="karakeep",state="active",name=~"karakeep-.*|meilisearch.service"} == 0` for 5 minutes, severity warning, to Alertmanager (LAB-DEC-061). Undo: remove the rule. Links: WISH-259. State: new.
- Cross-links (lane A): CC-02, DOC-05, HLT-03

### MON-02. The health check is shallow

Category MON · Severity low · State new

- Standard: LAB-STANDARDS §7 (`/health` 200 and 503). Owner: upstream. Severity: low. Effort: L. Approval: none. Your call: no.
- Evidence: see MON-01. The 503 path was not tested (cannot stop the service, Ground rule 9), so whether `/api/health` ever returns 503 is unverified. No stored baseline for the good-check.
- Checked: unverified for the 503 path (stopping the service is forbidden, Ground rule 9); the 200 body is verified.
- Fix: until a deeper check exists, MON-01 covers the gap from the outside. A Kuma keyword monitor on `/api/health` would add little (static body). A deeper read-only probe (queue depth, last crawl time) is WISH-259. State: new.

### MON-03. Kuma only alerts on "down for 2 minutes"; slow and flapping on the name path is silent

Category MON · Severity low · State new

- Standard: LAB-DEC-078. Owner: chief. Severity: low. Effort: S. Approval: none. Your call: no.
- Evidence: `KumaMonitorDown` is `monitor_status == 0` for 120 s, warning. Monitor 115 shows 5 status changes and one 27.9 s response in 7 days (SPD-03) and no alert fired. Kuma retries and interval are not readable by an allowed path here (the script copies template monitor 69; the template values are unverified). The LAB-DEC-078 target is retries 2 at 60 s.
- Checked: unverified for Kuma retries and interval (needs the approved Kuma read path); rule text and status changes are verified.
- Fix: read template 69 and monitors 115 and 116 through the approved Kuma read path in a later run; a response-time alert is optional. State: new.

### MON-04. Karakeep errors reach Loki but nothing alerts on them

Category MON · Severity low · State new

- Standard: none. Owner: chief. Severity: low. Effort: M. Approval: remediate. Your call: no.
- Evidence: Loki 7 days, `service="karakeep"` by unit: karakeep-web 53,783 lines, workers 1,201, meilisearch 383, browser 62. Error shapes in the samples: `TypeError: Invalid state: Controller is already closed` as `uncaughtException` in the web unit (6 in a 500-line error sample); `[Crawler] Failed to download and store image` (3); crawler `Blocking sub-request to disallowed URL ... Refusing to access disallowed resolved address` (22 in a 1000-line sample). D0 also saw `failed to report usage ... dial tcp 0.0.0.0:443`. The hostname for the crawler warnings resolves to a blocked or private address; this is consistent with AdGuard answering blocked names with `0.0.0.0`, but that is an inference, unverified. The Loki ruler endpoint returned HTTP 400 for `/loki/api/v1/rules`, so whether Loki alert rules exist is unverified.
- Checked: verified for the Loki samples; unverified for Loki alert rules (ruler endpoint returned 400) and for the 0.0.0.0 inference.
- Fix: none needed now. If wanted, a Loki rule on `uncaughtException` count. State: new.

### MON-05. Full bookmark URLs, some from sign-in sessions, are shipped to Loki

Category MON · Severity medium · State new

- Standard: SECRETS-RULE rule 2 (a URL that carries a token). Owner: jason with lane S. Severity: medium. Effort: M. Approval: remediate. Your call: yes.
- Evidence: the karakeep-web unit logs every request line, including `GET /api/trpc/bookmarks.checkUrl?...input=...url...`. In a 7-day, 500-line sample I saw check requests for a document-signing session URL (23 repeats) and an HR portal URL with an error-reason parameter (5). I did not read the full URLs and did not copy them here. Coordinator check, 2026-11-01, 5000-line sample, parameter names only: `sessionid` 4 hits, `nonce` 124, `hash` 124; 19 distinct hosts. Values not read. These are third-party sites, not lab credentials. Loki retention for this stream is unverified.
- Reading: a saved or probed URL can carry a session token. Loki is a lab store, but tokens in it are against the rule. Hand-off to lane S for severity.
- Checked: verified that such URLs are in Loki (sample); unverified for Loki retention and for whether any token is live (values not read).
- Fix: drop or hash `query` strings of `checkUrl` in the Alloy pipeline for `karakeep-web`, and decide about rotating anything real. Undo: restore the Alloy config. Links: lane S. State: new.
- Cross-links (lane A): the SEC lane has no matching finding, N handed severity to S; kept medium as written, see Overlaps; SECRETS-RULE rule 2 is the rule it breaks (Standard shown as none because that rule is not one of the Step 5 standard forms)

### DOC-01. HEAD of the karakeep repo says tagging uses Ollama CT 112; live uses OpenRouter

Category DOC · Severity high · State new

- Standard: SERVICE-REVIEW H · Owner: jason, then lane A · Severity: high · Effort: S · Approval: none
- Evidence: `git show HEAD:ARCHITECTURE.md` lines 110, 118; Loki 7 day: 316 openrouter lines, 0 lines with 11434 (D0)
- Checked: verified (Loki log lines; the configured values in the root-only env file would verify directly)
- Your call: Yes: who commits the 7 working tree files
- Fix: Commit the working tree edits after DOC-04 is settled. Undo: git revert
- Links: DOC-04, DOC-02, WISH-189
- State: new
- Detail: HEAD says Ollama `llama3.1:8b` in `ARCHITECTURE.md` §5 (line 110), §6 (line 118), §8 (lines 142 to 144, 149), `CLAUDE.md` (Tagging row, line 65), `CURSOR.md` (line 30), `docs/RUNBOOK.md` (line 85), `.env.example` (lines 11 to 14) and the HEAD changelog. WT replaces all of these with OpenRouter `google/gemini-2.5-flash-lite` for text and images, adds `INFERENCE_IMAGE_MODEL`, and adds the note that page text leaves the guest. Live: Loki shows openrouter log lines and no 11434 lines (indirect; the guest env file is root only, so the configured values are unverified). WT agrees with live; HEAD is stale. Fix: commit the WT edits after DOC-04 is settled. Undo: git revert. This lane does not commit them.
- Cross-links (lane A): INT-01 (the Ollama versus OpenRouter drift)

### DOC-02. lab-standards and Command Center data still say tagging calls Ollama; no OpenRouter dependency

Category DOC · Severity medium · State new

- Standard: SERVICE-REVIEW H · Owner: chief · Severity: medium · Effort: S · Approval: none
- Evidence: SERVICE-DEPENDENCIES.md:137; CHANGELOG.md:355; service-meta.json lines 1389 to 1409
- Checked: verified
- Your call: no
- Fix: Replace Ollama with OpenRouter, add the dependency, regenerate service-meta.json. Undo: git revert
- Links: DOC-01, CC-06
- State: new
- Detail: `lab-standards/SERVICE-DEPENDENCIES.md:137` ("Ollama (CT 112) for auto-tagging only", "Tagging calls `192.168.30.104:11434`"), `lab-standards/CHANGELOG.md:355` ("karakeep tagging uses Ollama on CT 112"), and `commandcenter/src/lib/server/service-meta.json` lines 1389 to 1409 (the same sentence on all five dependency rows; it is generated from SERVICE-DEPENDENCIES, so fixing the source and regenerating fixes it). Fix: replace Ollama with OpenRouter (external, paid) in the dependency row and add the dependency. Blast radius stays Low (archive and search keep working). Add the privacy note: page text leaves the guest.
- Cross-links (lane A): INT-01, INT-03

### DOC-03. TOOLS.yaml OpenRouter `lab_use` names only Hermes

Category DOC · Severity low · State new

- Standard: SERVICE-REVIEW H · Owner: chief · Severity: low · Effort: S · Approval: none
- Evidence: TOOLS.yaml line 801
- Checked: verified
- Your call: no
- Fix: Extend `lab_use` to name Karakeep tagging. Undo: git revert
- Links: DOC-02, CC-05
- State: new
- Detail: `TOOLS.yaml` OpenRouter entry (line 798 onward): `lab_use: Pays for the models that the Hermes agents call.` Karakeep is a second consumer. Fix: extend `lab_use`.

### DOC-04. Working tree contradicts itself on the curated tag count (26 or 25)

Category DOC · Severity medium · State new

- Standard: SERVICE-REVIEW H · Owner: jason · Severity: medium · Effort: S · Approval: none
- Evidence: WT CHANGELOG.md entries "26 to 25" and "The 26 curated tags were kept"; WT ARCHITECTURE.md section 8 says 26
- Checked: unverified (the settings page in Karakeep, behind a login, would verify the real count; the contradiction itself is seen)
- Your call: Yes: 25 or 26
- Fix: Jason picks, then fix every doc to that number. Undo: git revert
- Links: DOC-01
- State: new
- Detail: WT `CHANGELOG.md` has "Removed `tools` from the curated tags (26 to 25)" and in the next entry "The 26 curated tags were kept". WT `ARCHITECTURE.md` §8, `CLAUDE.md`, `CURSOR.md` and `RUNBOOK.md` say 26 and "still selected", and the Tools smart list on `#tools` is still listed. Live is not readable without a login, so the truth is unverified. Conflict: both sides recorded, Jason decides.

### DOC-05. "three units" in health checks; live has four

Category DOC · Severity low · State new

- Standard: SERVICE-REVIEW H · Owner: chief · Severity: low · Effort: S · Approval: none
- Evidence: CLAUDE.md:55, RUNBOOK.md:89, SRE-AGENT-CATALOG.md:185; `systemctl is-active` on four units returns active x4
- Checked: verified
- Your call: no
- Fix: Say four units (add meilisearch) in all three. Undo: git revert
- Links: none
- State: new
- Detail: `CLAUDE.md:55`, `docs/RUNBOOK.md:89` and `lab-standards/SRE-AGENT-CATALOG.md:185` say three units (web, workers, browser). `ARCHITECTURE.md` §4 lists four, and live `systemctl is-active` returns active for all four. A check that skips Meilisearch misses a search outage. Fix: four units in all three places.
- Cross-links (lane A): MON-01, CC-02

### DOC-06. Sync receipt `6a449af` is 244 commits behind lab-standards

Category DOC · Severity low · State new

- Standard: SERVICE-REVIEW H · Owner: lane A · Severity: low · Effort: S · Approval: none
- Evidence: CLAUDE.md sync table; D0 section Basis
- Checked: verified
- Your call: no
- Fix: Read the lab-standards CHANGELOG since that SHA, bump the receipt. Undo: git revert
- Links: none
- State: new
- Detail: `CLAUDE.md` sync receipt `6a449af` (2026-10-08); D0 counted 244 lab-standards commits since. Fix: read the CHANGELOG since that SHA, then bump "Last reconciled".

### DOC-07. Credential and vault references miss the OpenRouter key and the Hermes credential

Category DOC · Severity medium · State new

- Standard: SERVICE-REVIEW H · Owner: jason · Severity: medium · Effort: S · Approval: none
- Evidence: SERVICE-INVENTORY.md:295 lists root-password, admin-password, cursor-api-key; WT ARCHITECTURE.md names openrouter-api-key; no lab-standards mention of karakeep-hermes
- Checked: unverified (a Dashlane check by Jason would verify the entries exist)
- Your call: Yes: do the entries exist
- Fix: Add the references to the inventory API row. Undo: git revert
- Links: USE-05
- State: new
- Detail: `SERVICE-INVENTORY.md:295` lists vault refs `root-password`, `admin-password`, `cursor-api-key` only. WT `ARCHITECTURE.md` names `vault://dashlane/yingson-labs/karakeep/openrouter-api-key` and the laptop file `karakeep-openrouter.env`. D0 saw the laptop files `karakeep-hermes.env`, `karakeep-openrouter.env`, `karakeep.env` (names only). A `karakeep-hermes` search over lab-standards `*.md` and `*.yaml` found no mention. Fix: add the OpenRouter and Hermes references to the inventory API row and say which key belongs to which consumer. Whether Dashlane entries exist: only Jason can say.
- Cross-links (lane A): SEC-08, BAK-05, USE-05

### DOC-08. No LAB-STANDARDS section 12 upgrade backlog row for karakeep

Category DOC · Severity low · State new

- Standard: LAB-STANDARDS §12 · Owner: lane A · Severity: low · Effort: S · Approval: none
- Evidence: D0 section 4: 0 karakeep hits in the table
- Checked: verified
- Your call: no
- Fix: Add a row: running 0.33.2, upstream stable from lane P, Not applied. Undo: git revert
- Links: none
- State: new
- Detail: D0 grep: no karakeep row in the LAB-STANDARDS §12 table. Add one: running 0.33.2, upstream stable (lane P supplies it), "Not applied".
- Cross-links (lane A): PAT-05

### DOC-09. App version is answerable live (public `/api/version`) but no doc says how to check it

Category DOC · Severity low · State new

- Standard: SERVICE-REVIEW H · Owner: lane A · Severity: low · Effort: S · Approval: none
- Evidence: `curl http://192.168.30.33:3000/api/version` returns 0.33.2
- Checked: verified
- Your call: no
- Fix: Write the check into RUNBOOK.md and the SRE catalog good-check. Undo: git revert
- Links: CC-01
- State: new
- Detail: D0 listed the running version as unknown. The public `/api/version` endpoint answers it without login: 0.33.2, matching `TOOLS.yaml:565` and `SERVICE-INVENTORY.md:90`. No mismatch, but write the check into `RUNBOOK.md` and the SRE catalog good-check. Meilisearch 1.54.3 stays unverified (401 without a key).

### DOC-10. `last_verified` dates need a refresh after this review

Category DOC · Severity low · State new

- Standard: SERVICE-REVIEW H · Owner: lane A · Severity: low · Effort: S · Approval: none
- Evidence: HEAD 2026-10-08, WT 2026-10-12
- Checked: verified
- Your call: no
- Fix: Refresh the docs whose facts this review confirmed, on the fix run date. Undo: git revert
- Links: DOC-01
- State: new
- Detail: HEAD docs `last_verified` 2026-10-08, WT 2026-10-12. The WT date claims checks of OpenRouter facts that cannot be fully verified. After the fix run, refresh the docs whose facts this review confirmed: version, four units, listeners, NPM and Kuma ids (D0), Alloy hold, resolver, Node 22. None is over 180 days.

### DOC-11. Doc claims this review could not check (privileged, onboot, features, port owners, Meilisearch version)

Category DOC · Severity low · State new

- Standard: SERVICE-REVIEW H · Owner: jason · Severity: low · Effort: S · Approval: none
- Evidence: ARCHITECTURE.md sections 2 and 13; D0 section 2
- Checked: unverified (`sudo pct config 136` and `ss -tlnup` would verify)
- Your call: Yes: allow sudo reads in the fix run, or accept
- Fix: Run the sudo reads in the fix run and name the owners in section 13. Undo: no change made
- Links: WISH-236
- State: new
- Detail: Not checked: "unprivileged", `onboot: 1`, `nesting=1,keyctl=1` (need `pct config`, sudo); `/var/log/karakeep-ct-create.log` is documented as on the Proxmox host (the guest has no such file, consistent with the doc; the host was not checked); Meilisearch version. Unexplained listeners (D0): loopback 25, 12345, 34943 and UDP 46549, 5353. `ARCHITECTURE.md` §13 says the web UI is the only published port, true for TCP only. Fix: sudo reads in a fix run, then name the owners in §13.
- Cross-links (lane A): SEC-11, SEC-12, SEC-02

### DOC-12. Swap is 92% used and no doc mentions it

Category DOC · Severity low · State new

- Standard: none · Owner: chief · Severity: low · Effort: S · Approval: none
- Evidence: `ssh karakeep free -m`: swap 470 of 512 MB; WISH-186; LxcSwapFull fired 2026-10-28
- Checked: verified
- Your call: no
- Fix: Add one Known Issues line pointing to WISH-186. Undo: git revert
- Links: WISH-186
- State: new
- Detail: Live `free -m`: swap 470 of 512 MB, memory 802 of 4096 MB used. `LxcSwapFull` fired for CT 136 on 2026-10-28 (WISH-186). `ARCHITECTURE.md` §14 Known Issues does not mention it. Fix: one line pointing to WISH-186.
- Cross-links (lane A): HLT-01, SPD-01

### DOC-13. Working tree leftovers: TROUBLESHOOTING names the Ollama variable; same day changelog entries have no times

Category DOC · Severity low · State new

- Standard: SERVICE-REVIEW H · Owner: lane A · Severity: low · Effort: S · Approval: none
- Evidence: WT TROUBLESHOOTING.md:40; WT CHANGELOG.md on/off entries
- Checked: verified
- Your call: no
- Fix: Reword the variable line, add "earlier that day" to the entries. Undo: git revert
- Links: DOC-01
- State: new
- Detail: WT `TROUBLESHOOTING.md:40` says the AI link appears when `OPENAI_API_KEY` or `OLLAMA_BASE_URL` is set (still true upstream; the lab uses the first). WT `CHANGELOG.md` has "Auto-tagging is off" and "Auto-tagging is on again" on the same date with no times, which reads as a contradiction. Fix: add "earlier that day" or a time.

### USE-01. Karakeep exposes Prometheus metrics that nothing scrapes

Category USE · Severity medium · State new

- Standard: LAB-DEC-061 · Owner: chief · Severity: medium · Effort: M · Approval: remediate
- Evidence: `GET /api/metrics` returns 401; `count({__name__=~"karakeep.*"})` is empty
- Checked: verified
- Your call: Yes: ok to set a metrics token
- Fix: Set a fixed `PROMETHEUS_AUTH_TOKEN`, scrape with a vault file bearer token, add a freshness rule. Needs a restart. Undo: remove the scrape job and the env line
- Links: WISH-260, CC-03
- State: new
- Detail: Fix: set `PROMETHEUS_AUTH_TOKEN` to a stored secret, scrape `/api/metrics` with a bearer token read from a vault file, add a freshness rule. Needs a restart. Undo: remove the scrape job and the env line. Metric names are unknown until a token exists.
- Cross-links (lane A): CC-03 (same evidence)

### USE-02. Semantic search state is unknown; it is the main lever for the research library

Category USE · Severity medium · State new

- Standard: none · Owner: jason · Severity: medium · Effort: L · Approval: remediate
- Evidence: Upstream env page: `SEMANTIC_SEARCH_ENABLED`, `EMBEDDING_*`; guest values unreadable
- Checked: unverified (the guest env file, root only, would verify)
- Your call: Yes, with WISH-244
- Fix: Decide in lane X, then set an embedding model and reindex. Undo: unset the variables
- Links: WISH-244
- State: new
- Detail: Check first: the guest embedding settings and whether an index exists. Lane X owns the proposal.

### USE-03. No logical backup (export) of the library

Category USE · Severity high · State new

- Standard: none · Owner: chief · Severity: high · Effort: M · Approval: remediate
- Evidence: ARCHITECTURE.md section 10; D0 preflight: no Kopia source; no restore test
- Checked: verified
- Your call: no
- Fix: Scheduled export plus a Kopia source and a restore test. Undo: remove the job
- Links: WISH-014
- State: new
- Detail: The only backup is the PBS snapshot of the guest and no restore test exists (D0). Same ground as WISH-014 and lane P. Severity follows lane P.
- Cross-links (lane A): BAK-01 (same fact, rated high in both)

### USE-04. Webhooks unused

Category USE · Severity low · State new

- Standard: none · Owner: chief · Severity: low · Effort: M · Approval: remediate
- Evidence: Upstream `WEBHOOK_*` variables; no lab doc mentions a webhook
- Checked: unverified (the Karakeep webhook settings page would verify)
- Your call: no
- Fix: Add a webhook to Discord or Command Center, with its own secret. Undo: delete the webhook
- Links: WISH-261
- State: new

### USE-05. Per consumer API keys: only the Cursor key is documented

Category USE · Severity low · State new

- Standard: SERVICE-REVIEW I · Owner: jason · Severity: low · Effort: S · Approval: none
- Evidence: SERVICE-INVENTORY.md:295; D0 laptop file names
- Checked: unverified (the Karakeep API keys page would verify)
- Your call: Yes: see DOC-07
- Fix: One key per consumer, one vault entry each. Undo: revoke the key
- Links: DOC-07
- State: new
- Cross-links (lane A): SEC-08, BAK-05, DOC-07

### USE-06. Lab slug tags as join keys

Category USE · Severity low · State new

- Standard: none · Owner: chief · Severity: low · Effort: M · Approval: remediate
- Evidence: No source of tag names readable without a login
- Checked: unverified (the tag list, via X0 or a login, would verify)
- Your call: Yes: want it at all
- Fix: Generate tags from TOOLS.yaml slugs by script or rule. Undo: delete the tags
- Links: WISH-261, CC-07
- State: new
- Detail: Tags named after `TOOLS.yaml` slugs would let Command Center join a bookmark to a service card. Values should be generated from the manifest, not typed. Depends on lane X.
- Cross-links (lane A): CC-07

### CC-01. Command Center does not use Karakeep public health and version endpoints

Category CC · Severity low · State new

- Standard: SERVICE-REVIEW J · Owner: chief · Severity: low · Effort: S · Approval: none
- Evidence: `/api/health` 200 and `/api/version` 0.33.2 on the laptop; grep of commandcenter `src/lib/server` for karakeep finds only icon, meta and tools data
- Checked: verified
- Your call: no
- Fix: Add a GET of `/api/health` (60 s) and `/api/version` (1 h) to the services source and show it on the card. Undo: remove the call
- Links: WISH-260, DOC-09
- State: new

### CC-02. No unit level state for the four units on the card

Category CC · Severity low · State new

- Standard: SERVICE-REVIEW J · Owner: chief · Severity: low · Effort: S · Approval: none
- Evidence: health.ts has no karakeep unit rule; series coverage for the four units not queried
- Checked: unverified (`node_systemd_unit_state{name=~"karakeep.*|meilisearch.*"}` on Prometheus would verify)
- Your call: no
- Fix: If the series exist, add a four unit tile; otherwise add them to the Alloy unix integration. Undo: remove the tile
- Links: DOC-05
- State: new

### CC-03. Karakeep metrics are not scraped

Category CC · Severity medium · State new

- Standard: LAB-DEC-061 · Owner: chief · Severity: medium · Effort: M · Approval: remediate
- Evidence: Same evidence as USE-01
- Checked: verified
- Your call: no
- Fix: As USE-01. Undo: as USE-01
- Links: USE-01, WISH-260
- State: new
- Cross-links (lane A): USE-01

### CC-04. Deep links limited to the home page

Category CC · Severity low · State new

- Standard: SERVICE-REVIEW J · Owner: chief · Severity: low · Effort: S · Approval: none
- Evidence: Only `/signin` tested (200); other routes need a login
- Checked: unverified (a logged in click through of lists, tags and admin pages would verify the URLs)
- Your call: no
- Fix: After the URLs are known, add links for lists, tags and the admin jobs page to the card. Undo: remove the links
- Links: none
- State: new

### CC-05. OpenRouter spend cannot be split between Hermes and Karakeep

Category CC · Severity medium · State new

- Standard: none · Owner: chief · Severity: medium · Effort: M · Approval: none
- Evidence: TOOLS.yaml openrouter-exporter on CT 130; per key output not checked
- Checked: unverified (the exporter metrics on Prometheus would verify)
- Your call: no
- Fix: If it reports per key, label by consumer and show Karakeep on the card. Undo: remove the label
- Links: DOC-03, DOC-07
- State: new
- Detail: The OpenRouter exporter runs on CT 130 (`TOOLS.yaml`). Whether it reports usage per key, and whether Karakeep has its own OpenRouter key, is unverified (doc says a separate key). If per key usage exists, the card can show Karakeep tagging cost (doc claim: about $0.16 for the 844 item retag).
- Cross-links (lane A): INT-02

### CC-06. Generated dependency data in Command Center is stale

Category CC · Severity medium · State new

- Standard: SERVICE-REVIEW H · Owner: chief · Severity: medium · Effort: S · Approval: none
- Evidence: service-meta.json lines 1389 to 1409
- Checked: verified
- Your call: no
- Fix: After DOC-02, re-run the generator. Undo: git revert
- Links: DOC-02
- State: new
- Detail: After DOC-02, the generator for `service-meta.json` must be re-run. The `commandcenter/src/lib/server` folder also holds Syncthing sync-conflict copies of some files; I did not read them.
- Cross-links (lane A): DOC-02

### CC-07. No bookmark to lab service join

Category CC · Severity low · State new

- Standard: none · Owner: chief · Severity: low · Effort: L · Approval: none
- Evidence: No tag or list holds a slug that is readable without a login
- Checked: unverified (X0 tag list would verify)
- Your call: Yes: with USE-06
- Fix: Needs USE-06 first, then a Command Center read of bookmark tags by slug, bookmark scope key, read only. Undo: remove the read and the key
- Links: USE-06, WISH-261, WISH-244
- State: new
- Cross-links (lane A): USE-06
