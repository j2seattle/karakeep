---
title: Librarian semantic watch, staged steps
version: 1.0.0
status: active
last_edited_by: Claude Code (run 2026-11-28-big-push, lane KNOW)
last_edited_date: 2026-11-28
parent: ../../README.md
children: []
siblings: []
audience: internal
tags: [yingson-labs, karakeep, librarian, paperclip, staged]
summary: "Staged steps for the Librarian watch: what was verified about Paperclip's webhook trigger and Karakeep's webhook sender, and the order in which the coordinator and Jason run the scripts."
doc_type: runbook
scope: service
service_name: karakeep
parent_doc: lab-standards/ARCHITECTURE.md
depends_on: [paperclip, hermes]
depended_on_by: []
agent_context: true
permission_tier: read-only
last_verified: 2026-11-28
---

# Librarian semantic watch: staged steps

Plan: `lab-standards/docs/proposals/librarian-semantic-watch.md` (approved, LAB-DEC-218). Written 2026-11-28 by lane KNOW of run 2026-11-28-big-push. Nothing in this folder was run. Order, and who runs each:

| # | Step | Who | Needs first |
|---|---|---|---|
| 1 | Aegis intake gate live and tested with five planted pages (plan phase 2) | lane AGENTS or the coordinator | the gate plan |
| 2 | Paperclip routine "Librarian: analyze new bookmark" with a webhook trigger in `bearer` mode, assigned to the Librarian, one run at a time | lane AGENTS or the coordinator (Chief issue, Draft only) | step 1 |
| 3 | `ct130-install-duty.sh` on CT 130 | the coordinator | AGENTS says "CT130 DONE" |
| 4 | Snapshot CT 136, then `ct136-allow-paperclip-webhook.sh` | the coordinator or Claude Code | step 2, outside quiet hours |
| 5 | `create-karakeep-webhook.ps1` on the laptop (masked prompt) | Jason, about 3 minutes | steps 2 and 4 |
| 6 | Save one test link and see its analysis in the Paperclip issue | Claude Code | step 5 |

## What was verified (2026-11-28)

- No new receiver service is needed. The installed Paperclip server on CT 128 has `POST /api/routine-triggers/public/<publicId>/fire` (file `@paperclipai/server/dist/routes/routines.js`). A webhook trigger in `bearer` mode accepts the call when `Authorization` equals `Bearer <trigger secret>`, which is what Karakeep sends when the webhook has a token. The route answers 202 and the body may be any JSON object. This answers the plan's phase 1 question, so LAB-DEC-080 does not require a separate plan for a receiver.
- CT 136 can open a connection to `192.168.30.34:3100` (Paperclip). Checked from inside CT 136.
- Karakeep's webhook body holds `jobId`, `bookmarkId`, `userId`, `url`, `type`, `operation` and no page text (v0.35.0 `webhookWorker.ts`). The worker retries per `webhook.retryTimes` and times out per `webhook.timeoutSec`.
- Karakeep sends webhooks through the same URL guard as its crawler (`apps/workers/network.ts`): a private address is refused unless the host is in `CRAWLER_ALLOWED_INTERNAL_HOSTNAMES`. The live env has no such line (checked by name). Step 4 adds `192.168.30.34` only.
- `webhooks.create` takes `{url, events, token}`, events include `ai tagged` (v0.35.0 `packages/shared/types/webhooks.ts`). Karakeep has 0 webhooks today (read from `db.db`) and 5 API keys.
- Per source (read from `db.db`, counts only): api 818, mobile 184, none 33, extension 3; types asset 310, link 728. Embeddings success 1,037 of 1,038 (one with no status, source none). Tagging success 1,036, one failure and one null (both source none). This is the per-source count the plan listed as "not checked".

## Not verified

- Whether Paperclip's routine concurrency can enforce "one at a time" and a daily budget of 25 (check the routine settings when it is made; otherwise the duty file's own limit applies).
- Whether the laptop API key's scopes allow `webhooks.create` (the script reports and falls back to the Settings page).
- Whether the public trigger path needs the Paperclip company or board header on this install (it is a public route in the code; confirm with the first test call).
