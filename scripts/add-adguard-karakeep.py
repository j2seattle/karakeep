#!/usr/bin/env python3
"""Add an enabled explicit rewrite for karakeep.yingson.com. Run on CT 105.

Does not restart AdGuard. Restart AdGuardHome after this returns so the row loads.
The wildcard already answers; this rewrite is the one that survives a wildcard edit.
"""
from pathlib import Path

YAML = Path("/opt/AdGuardHome/AdGuardHome.yaml")
DOMAIN = "karakeep.yingson.com"
BLOCK = (
    f"    - domain: {DOMAIN}\n"
    "      answer: 192.168.30.182\n"
    "      enabled: true\n"
)


def main() -> None:
    text = YAML.read_text(encoding="utf-8")
    if f"domain: {DOMAIN}" in text:
        chunk = text.split(f"domain: {DOMAIN}", 1)[1].split("- domain:", 1)[0]
        if "enabled: false" in chunk:
            raise SystemExit(f"{DOMAIN} exists but is disabled")
        print(f"rewrite already present: {DOMAIN}")
        return
    needle = "  rewrites:\n"
    idx = text.find(needle)
    if idx < 0:
        raise SystemExit("no rewrites key")
    insert_at = idx + len(needle)
    YAML.write_text(text[:insert_at] + BLOCK + text[insert_at:], encoding="utf-8")
    print(f"inserted {DOMAIN}")


if __name__ == "__main__":
    main()
