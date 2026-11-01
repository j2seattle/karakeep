---
title: Baselines — karakeep
version: 0.1.0
status: active
last_edited_by: Claude Code
last_edited_date: 2026-11-01
parent: ARCHITECTURE.md
children: []
siblings: [TROUBLESHOOTING.md, CHANGELOG.md]
audience: ops
tags: [yingson-labs, karakeep, baselines]
summary: "Healthy-state ranges for karakeep, measured on 2026-11-01 from one sample. Thresholds are proposals from that sample."
doc_type: baselines
scope: service
service_name: karakeep
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: [proxmox]
depended_on_by: []
agent_context: true
permission_tier: read-only
last_verified: 2026-11-01
---

# Baselines — Karakeep

**Slug:** `karakeep` · **Last full review:** 2026-11-01

Every value here was observed on 2026-11-01 (Service Review run 1 and the fix run). It is one sample, not a long baseline. Thresholds marked "proposed" are drawn from that sample and from alert rules that already exist. Re-measure at the next review.

## Measurement environment

| Field | Value |
|---|---|
| **Host** | CT 136, 2 vCPU / 4 GB RAM / 15 GB disk |
| **App version** | 0.33.2 (`curl http://192.168.30.33:3000/api/version`) |
| **Typical load** | Idle archive. 7 day CPU mean 1.5 percent, peak 88 percent (Prometheus). Load average 4.7 to 5.9 on 2 vCPU while CPU pressure is about 0.1 (cause not found, see Notes). |
| **Measured over** | One window on 2026-11-01 (laptop on the LAN, 5 runs each), plus 7 day Prometheus queries |

## Health endpoint

- **Normal range:** `/api/health` and `/signin` on the IP path answer 200 in 20 to 110 ms. Through NPM and TLS (`https://karakeep.yingson.com/signin`) 70 to 220 ms. Median on the IP path 40 to 65 ms, on the name path about 130 ms. NPM and TLS add about 66 ms at the median.
- **Warning threshold (proposed):** a 200 that takes over 1 second on the IP path more than once in 5 runs, or any non-200.
- **Critical threshold (proposed):** no 200 from `/api/health` for 2 minutes (Kuma monitors 115 and 116 already alert on that). A 200 does not prove the workers or Meilisearch are up, so also check the four units with `systemctl is-active` (see Notes).
- **Measurement source:** `curl -s -o /dev/null -w '%{http_code} %{time_total}
' http://192.168.30.33:3000/api/health` from the laptop, five runs. The body is the fixed text `{"status":"ok","message":"Web app is working"}`.
- **Known false-positive conditions:** the first request after idle can take about 1 second (seen once in each of two runs on 2026-11-01). Kuma monitor 115 (name path) logged one 27.9 s response in 7 days, cause not found, while the IP path stayed fast.
- **Last verified:** 2026-11-01

## Resource ranges

| Metric | Idle | Warning | Critical |
|---|---|---|---|
| CPU | 7 day mean 1.5 percent. CPU pressure (some, avg300) 0.11. Idle 80 to 90 percent in `vmstat` | proposed: pressure avg300 above 10 for 15 minutes | proposed: above 50 for 15 minutes |
| RAM | 815 MiB used, 3280 MiB available of 4096 MiB. 7 day minimum available 3.24 GiB. Memory pressure 0.00 | proposed: available under 1 GiB | proposed: available under 400 MiB, or any memory pressure above 5 |
| Disk | `/` 59 percent (8.2 GiB of 15 GiB), growing about 110 MB a day | 85 percent for 15 minutes (`GuestRootDiskHigh`, existing rule). About 40 days at the current rate | proposed: 95 percent |
| Swap | 468 of 512 MiB used (about 91 percent), stable for 7 days with swap-in near zero. Cold pages, not pressure | `GuestSwapHigh` (swap-in above 50 pages/s, existing rule) | proposed: swap-in above 50 pages/s together with memory pressure above 5 |

## Notes

- Swap sits at about 90 percent with memory pressure at 0.00. This is cold pages parked in swap. `LxcSwapFull` has fired for CT 136 since 2026-10-29 (WISH-186).
- Load average reads high for the CPU use, and the context switch rate is near 85 thousand a second. The cause is not found (finding SPD-02). Do not use load average as a threshold.
- IO pressure (some, avg300) is 0.30 and full 0.24, the highest of the three, still low.
- The disk is the tightest resource. Growth is from page copies, screenshots and Meilisearch. `/opt/karakeep_data` is root only, so the split is not measured.
- Memory peaked at 4.0 GiB used in the 7 day window once, so a spike can still push the guest into swap.
- The four units to check are `karakeep-web`, `karakeep-workers`, `karakeep-browser` and `meilisearch`. All four were active on 2026-11-01.
