# karakeep

Karakeep archives bookmarks, pages, and screenshots for the lab. It runs on CT 136 at `192.168.30.33` and is reached at `https://karakeep.yingson.com`.

**Readiness:** R3. Tailscale only. Not R4.

| | |
|---|---|
| Guest | CT 136, unprivileged, `onboot: 1` |
| Address | `192.168.30.33` (UniFi alias `karakeep-LXC`) |
| Web | port 3000 |
| Version | 0.33.2 (community-scripts install, 2026-10-08) |
| SSH | `ssh karakeep` once the laptop Host block is in place |
| Data | `/opt/karakeep_data` on the CT disk (SQLite — not NFS) |

First visit asks for the admin account. That account is Jason's to create. The root password for the container is on the Proxmox host at `/root/karakeep-lxc-root.password` (mode 600). Copy it into Dashlane as `vault://dashlane/yingson-labs/karakeep/root-password`, then delete the file. Do not paste it into chat.

Day-to-day commands are in [docs/RUNBOOK.md](docs/RUNBOOK.md). The technical reference is [ARCHITECTURE.md](ARCHITECTURE.md).
