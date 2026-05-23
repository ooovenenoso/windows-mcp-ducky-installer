#!/usr/bin/env python3
"""Build a local plug-and-play DuckyScript with a hardcoded Discord webhook.

The generated file is intentionally written under dist/ (gitignored) because
Discord webhook URLs are secrets. Do not commit generated output.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "payloads" / "Install_Windows_MCP_Discord_Webhook.txt"
DEFAULT_OUTPUT = ROOT / "dist" / "Install_Windows_MCP_Discord_Webhook_PLUG_AND_PLAY.txt"
DISCORD_WEBHOOK_RE = re.compile(r"^https://(?:discord(?:app)?\.com|canary\.discord\.com)/api/webhooks/\d+/[A-Za-z0-9_-]+")


def ps_single_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def build_payload(webhook: str) -> str:
    if not DISCORD_WEBHOOK_RE.match(webhook):
        raise SystemExit("Webhook must be a full Discord webhook URL.")

    text = SOURCE.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: list[str] = []
    skip_next_delay = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Rewrite header notes for the generated plug-and-play artifact.
        if line.startswith("REM Requires WINDOWS_MCP_INSTALL_AUTHORIZED"):
            out.append("REM Plug-and-play generated payload: Discord webhook is hardcoded locally.")
            out.append("REM Keep this generated file private; Discord webhook URLs are secrets.")
            i += 1
            continue

        # Remove the environment consent gate for the generated artifact.
        if line == "STRING $consent = $env:WINDOWS_MCP_INSTALL_AUTHORIZED":
            i += 4  # line, ENTER, DELAY, if (...) line
            continue

        # Replace environment webhook read with a hardcoded local secret.
        if line == "STRING $webhook = $env:WINDOWS_MCP_DISCORD_WEBHOOK":
            out.append(f"STRING $webhook = {ps_single_quote(webhook)}")
            i += 1
            continue

        # The hardcoded payload no longer needs the missing-env check.
        if line.startswith("STRING if ([string]::IsNullOrWhiteSpace($webhook))"):
            i += 2  # line + ENTER; leave following DELAY in place harmlessly
            continue

        # Update validation error wording.
        if "WINDOWS_MCP_DISCORD_WEBHOOK is not a Discord webhook URL" in line:
            out.append("STRING if ($webhook -notmatch '^https://(discord(app)?\\.com|canary\\.discord\\.com)/api/webhooks/') { throw 'Hardcoded webhook is not a Discord webhook URL.' }")
            i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a local plug-and-play DuckyScript with a hardcoded Discord webhook.")
    parser.add_argument("--webhook", required=True, help="Full Discord webhook URL to hardcode into the generated payload")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help=f"Output path (default: {DEFAULT_OUTPUT})")
    args = parser.parse_args()

    payload = build_payload(args.webhook.strip())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(payload, encoding="utf-8")
    print(f"Wrote {args.output}")
    print("Do not commit this generated file; it contains a Discord webhook URL.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
