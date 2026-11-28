# create-karakeep-webhook.ps1: create the ONE Karakeep webhook for the Librarian watch (plan decision 1, approved LAB-DEC-218).
# Run on the laptop in PowerShell, after the Paperclip routine with a webhook trigger exists (lane AGENTS or the coordinator makes it)
# and scripts/librarian/ct136-allow-paperclip-webhook.sh has run. Karakeep then calls Paperclip when a new link has been read and tagged.
#
# Before you run it, have two things from Paperclip's routine page (its webhook trigger):
#   - the public id (a short code in the trigger URL; not a secret)
#   - the trigger secret (shown once when the trigger is made; save it in Dashlane first)
# What to expect: a prompt for the public id (visible), then a masked prompt for the secret (one * per character, about 40 to 64 characters).
# Success looks like:  token length 48 | webhooks.create 200 | webhooks.list: 1 webhook, events ai tagged, token set
# Failure looks like:  a line starting FAILED. Nothing is changed if a check fails before the create call.
#
# Unverified: the exact tRPC body (superjson "json" wrapper) and that the laptop's API key may create webhooks. If create fails, make the
# same webhook by hand: Karakeep, Settings, Webhooks, new: the URL built below, event "ai tagged", and the token.
$ErrorActionPreference = 'Stop'
. "C:\Development\Yingson Labs\lab-standards\scripts\laptop\Read-MaskedSecret.ps1"
$envFile = "C:\Users\thedu\.cursor\mcps\karakeep.env"
$cfg = @{}
foreach ($l in Get-Content $envFile) { if ($l -match '^\s*([A-Z_]+)\s*=\s*(.*)$') { $cfg[$Matches[1]] = $Matches[2].Trim('"').Trim("'") } }
if (-not $cfg['KARAKEEP_URL'] -or -not $cfg['KARAKEEP_API_KEY']) { Write-Host "FAILED: KARAKEEP_URL or KARAKEEP_API_KEY missing in $envFile"; exit 1 }
$base = $cfg['KARAKEEP_URL'].TrimEnd('/')
$hdr = @{ Authorization = "Bearer $($cfg['KARAKEEP_API_KEY'])" }
$routineId = Read-Host "Paperclip webhook public id"
if ($routineId -notmatch '^[A-Za-z0-9_-]{6,80}$') { Write-Host "FAILED: that does not look like a public id"; exit 1 }
$tok = Read-MaskedSecret "Paste the Paperclip trigger secret, then Enter"
if (-not $tok -or $tok.Length -lt 16) { Write-Host "FAILED: secret missing or shorter than 16 characters"; exit 1 }
Write-Host "token length $($tok.Length)"
$url = "http://192.168.30.34:3100/api/routine-triggers/public/$routineId/fire"
$list = Invoke-RestMethod -Uri "$base/api/trpc/webhooks.list" -Headers $hdr -TimeoutSec 30
$existing = @($list.result.data.json.webhooks).Count
if ($existing -gt 0) { Write-Host "FAILED: $existing webhook(s) already exist. Not adding a second. Check Settings, Webhooks."; exit 1 }
$body = @{ json = @{ url = $url; events = @("ai tagged"); token = $tok } } | ConvertTo-Json -Depth 5 -Compress
try {
    $r = Invoke-WebRequest -Uri "$base/api/trpc/webhooks.create" -Method Post -Headers $hdr -ContentType "application/json" -Body $body -UseBasicParsing -TimeoutSec 30
    Write-Host "webhooks.create $([int]$r.StatusCode)"
} catch {
    $code = if ($_.Exception.Response) { [int]$_.Exception.Response.StatusCode } else { -1 }
    Write-Host "FAILED: webhooks.create returned $code. Make it by hand in Settings, Webhooks (see header)."
    $tok = $null; $body = $null
    exit 1
}
$tok = $null; $body = $null
$list = Invoke-RestMethod -Uri "$base/api/trpc/webhooks.list" -Headers $hdr -TimeoutSec 30
$w = @($list.result.data.json.webhooks)
Write-Host "webhooks.list: $($w.Count) webhook, events $($w[0].events -join ','), token set: $($w[0].hasToken)"
Write-Host "Next: save one test link in Karakeep and check the Paperclip routine run list for a run within a few minutes."
