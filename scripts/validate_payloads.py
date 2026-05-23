#!/usr/bin/env python3
"""Validate DuckyScript payloads for safety and basic syntax."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOADS = sorted((ROOT / "payloads").glob("*.txt"))
ALLOWED_COMMANDS = {
    "REM", "DELAY", "GUI", "STRING", "ENTER", "LEFTARROW", "RIGHTARROW",
    "UPARROW", "DOWNARROW", "CTRL", "ALT", "SHIFT", "TAB", "SPACE",
}
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}", re.IGNORECASE),
    re.compile(r"https://(?:discord(?:app)?\.com|canary\.discord\.com)/api/webhooks/\d+/[A-Za-z0-9_-]+", re.IGNORECASE),
]


def validate_payload(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines:
        return [f"{path}: empty payload"]

    lower = text.lower()
    if "authorized" not in lower and "explicit permission" not in lower:
        errors.append(f"{path}: missing authorized-use reminder")
    if "WINDOWS_MCP_INSTALL_AUTHORIZED" not in text:
        errors.append(f"{path}: missing explicit authorization environment gate")
    if "WINDOWS_MCP_DISCORD_WEBHOOK" not in text:
        errors.append(f"{path}: missing Discord webhook environment variable")
    if "windows-mcp install" not in text:
        errors.append(f"{path}: missing Windows-MCP install command")

    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path}: possible embedded secret or real Discord webhook URL")

    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        command = line.split(maxsplit=1)[0]
        if command not in ALLOWED_COMMANDS:
            errors.append(f"{path}:{number}: unknown DuckyScript command {command!r}")

    return errors


def main() -> int:
    if not PAYLOADS:
        print("No payloads found.", file=sys.stderr)
        return 1

    errors: list[str] = []
    for payload in PAYLOADS:
        errors.extend(validate_payload(payload))

    if errors:
        print("Payload validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(PAYLOADS)} payload(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
