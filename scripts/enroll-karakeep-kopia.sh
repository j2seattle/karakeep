#!/bin/bash
# Run on the Proxmox host as root: sudo bash enroll-karakeep-kopia.sh
# Enrolls Karakeep (CT 136) as Kopia client karakeep@ct136, same pattern as
# kopia/scripts/enroll-paperclip-hermes.sh. The user password is made on CT 135 and
# moves to CT 136 by pct pull and push. It is never printed. The repository
# encryption password is not used on CT 136.
set -euo pipefail
CFG=/root/.config/kopia/repository.config
id=136
user=karakeep
host=ct136
file=/etc/kopia/user-karakeep.password

tmp=$(mktemp -d); chmod 700 "$tmp"; trap 'rm -rf "$tmp"' EXIT

add_user() {
  local name="$1"
  if pct exec 135 -- kopia server user list --config-file=$CFG | grep -qx "$name"; then echo "user exists $name"; return; fi
  pct exec 135 -- bash -lc "export KOPIA_PASSWORD=\$(cat /etc/kopia/repo.password); kopia server users add --config-file=$CFG --user-password=\"\$(cat '$file')\" '$name'"
  echo "user added $name"
}

# password file on CT 135 (made once)
pct exec 135 -- bash -lc "test -s '$file' || { umask 077; openssl rand -base64 24 | tr -d '\n' > '$file'; chmod 600 '$file'; }"

# kopia client package, same source and version as CT 116
if ! pct exec $id -- test -x /usr/bin/kopia; then
  pct pull 116 /usr/share/keyrings/kopia-keyring.gpg "$tmp/k.gpg"
  pct pull 116 /etc/apt/sources.list.d/kopia.list "$tmp/k.list"
  pct exec $id -- install -d -m 755 /usr/share/keyrings /etc/apt/sources.list.d
  pct push $id "$tmp/k.gpg" /usr/share/keyrings/kopia-keyring.gpg
  pct push $id "$tmp/k.list" /etc/apt/sources.list.d/kopia.list
  pct exec $id -- bash -lc "apt-get update -qq && apt-get install -y kopia=0.23.1 && apt-mark hold kopia"
fi

guest_host="$(pct exec $id -- hostname)"
add_user "$user@$host"
add_user "root@${guest_host}"
pct exec $id -- install -d -m 700 /etc/kopia /var/backups/kopia /root/.config/kopia
pct pull 135 "$file" "$tmp/user.password"; pct push $id "$tmp/user.password" /etc/kopia/user.password
pct pull 135 /etc/kopia/cert.sha256 "$tmp/cert"; pct push $id "$tmp/cert" /etc/kopia/cert.sha256
pct exec $id -- chmod 600 /etc/kopia/user.password
pct exec 135 -- bash /usr/local/sbin/refresh-server.sh
pct exec $id -- bash -lc "export KOPIA_PASSWORD=\$(cat /etc/kopia/user.password); fp=\$(tr -d '[:space:]' < /etc/kopia/cert.sha256); kopia repository connect server --config-file=$CFG --url=https://192.168.30.32:51515 --server-cert-fingerprint=\"\$fp\"; kopia repository set-client --config-file=$CFG --username='$user' --hostname='$host'; kopia --config-file=$CFG repository status | grep -E 'Config file|Server URL|Hostname|Username'"
echo "enrolled $user@$host"
