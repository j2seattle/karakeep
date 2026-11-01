<#
PAT-01: upgrade Karakeep from 0.33.2 to 0.34.1 on CT 136. Run by Jason from laptop PowerShell.
Written by lane GUEST (2026-11-01). It has NOT been run. The upgrade is a destructive-tier
change, so an agent does not run it.

What it does, in order (each step stops the script if it fails):
  1. Reads the current version, the four units and the bookmark count.
  2. Takes a fresh Proxmox snapshot of CT 136 (name below, expires in 14 days, LAB-DEC-079).
  3. Runs a Kopia backup on CT 136 first, so the database copy is fresh.
  4. Runs the community-script updater inside the guest (`update`). This needs a terminal.
     If it asks a question, answer it. It stops the units, pulls the release, rebuilds on
     Node 22, migrates the database and starts the units. The upgrade signs everyone out once
     and lowercases emails (FINDINGS PAT-01). Whether `update` asks questions is unverified.
  5. Checks: /api/version, units active, /api/health 200, sign-in 200 through the name,
     bookmark count not lower than before. Then look at Kuma monitors 115 and 116.

Undo (if a check fails): roll back to the snapshot. This puts the whole guest back as it was
at snapshot time and loses anything saved since. Ask the coordinator first if unsure.
    ssh proxmox "sudo pct rollback 136 <snapshot name printed by this script>"
    ssh proxmox "sudo pct start 136"      # only if it is stopped after the rollback

After the upgrade, check these, because the updater may rewrite them:
  - unit files: SEC-03 plan is in director-worker parts/sec03-plan.md
  - DISABLE_SIGNUPS=true and PROMETHEUS_AUTH_TOKEN still in /etc/karakeep/karakeep.env (names only)
  - the nftables rule for port 3000 is still loaded
This script prints no secret.
#>
$ErrorActionPreference = 'Stop'
$today = Get-Date -Format 'yyyyMMdd'
$exp   = (Get-Date).AddDays(14).ToString('yyyyMMdd')
$snap  = "pre_karakeep_pat01_${today}_exp${exp}"

function Run($label, [scriptblock]$b) {
    Write-Host "== $label" -ForegroundColor Cyan
    & $b
    if ($LASTEXITCODE -ne 0) { throw "Step failed: $label (exit $LASTEXITCODE)" }
}

$countCmd = "sudo python3 -c ""import sqlite3;print(sqlite3.connect('file:/opt/karakeep_data/db.db?mode=ro',uri=True).execute('select count(*) from bookmarks').fetchone()[0])"""

Run 'Current version' { ssh karakeep 'curl -s http://localhost:3000/api/version' }
$before = ssh karakeep $countCmd
Write-Host "Bookmarks before: $before"
Run 'Units before' { ssh karakeep 'systemctl is-active karakeep-web karakeep-workers karakeep-browser meilisearch' }

$ok = Read-Host "Take snapshot $snap and run the upgrade now? Type yes"
if ($ok -ne 'yes') { Write-Host 'Stopped. Nothing changed.'; return }

Run "Snapshot $snap" { ssh proxmox "sudo pct snapshot 136 $snap --description 'before karakeep 0.34.1 upgrade, expires $exp (LAB-DEC-079)'" }
Run 'Fresh Kopia backup' { ssh karakeep 'sudo systemctl start kopia-backup-karakeep.service' }

Write-Host '== Upgrade (interactive terminal)' -ForegroundColor Cyan
ssh -t karakeep 'sudo bash -lc update'
if ($LASTEXITCODE -ne 0) { throw "update returned $LASTEXITCODE. Do not continue. Roll back: ssh proxmox ""sudo pct rollback 136 $snap""" }

Start-Sleep -Seconds 20
Run 'Version after' { ssh karakeep 'curl -s http://localhost:3000/api/version' }
Run 'Units after'   { ssh karakeep 'systemctl is-active karakeep-web karakeep-workers karakeep-browser meilisearch alloy' }
Run 'Health'        { ssh karakeep 'curl -s -o /dev/null -w "health:%{http_code}\n" http://localhost:3000/api/health' }
Write-Host '== Sign-in page through the name' -ForegroundColor Cyan
(Invoke-WebRequest -UseBasicParsing https://karakeep.yingson.com/signin).StatusCode
$after = ssh karakeep $countCmd
Write-Host "Bookmarks after: $after (before: $before)"
if ([int]$after -lt [int]$before) { Write-Host 'COUNT DROPPED. Roll back.' -ForegroundColor Red }
Run 'Kept settings (counts only)' { ssh karakeep 'sudo grep -c "^DISABLE_SIGNUPS=true" /etc/karakeep/karakeep.env; sudo grep -c "^PROMETHEUS_AUTH_TOKEN=" /etc/karakeep/karakeep.env; sudo nft list chain inet filter input | grep -c "dport 3000"' }
Write-Host "Check Kuma monitors 115 and 116 are up, then report. Delete snapshot $snap after a week of normal running."
