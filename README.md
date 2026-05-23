# Windows-MCP Ducky Installer

Hardcoded-only DuckyScript payload for installing [CursorTouch/Windows-MCP](https://github.com/CursorTouch/Windows-MCP) on an authorized Windows lab machine and sending install status to Discord.

## Safety model

This repo is intended only for systems you own or have explicit permission to administer.

The main payload is now the hardcoded flow only:

- no `setx`
- no Windows environment variables
- no opt-in prompt
- webhook is assigned directly in the payload as `$webhook`

The committed repo keeps a safe placeholder so a real Discord webhook is not leaked publicly. Before use, replace:

```powershell
PASTE_DISCORD_WEBHOOK_URL_HERE
```

with your Discord webhook URL inside:

```text
payloads/Install_Windows_MCP_Discord_Webhook.txt
```

## What it does

1. Opens PowerShell.
2. Uses the hardcoded `$webhook` value from the payload.
3. Installs Python 3.13 with `winget` if Python is missing.
4. Installs `uv` if missing.
5. Installs `windows-mcp` with `uv tool install windows-mcp`.
6. Registers Windows-MCP with:

   ```powershell
   windows-mcp install --transport sse --host 127.0.0.1 --port 8000
   ```

7. Checks for the `windows-mcp-server` Scheduled Task.
8. Sends a Discord embed with success/failure metadata.

## Discord report contents

The Discord message includes only installation metadata:

- status
- Windows username
- computer name
- log path
- Windows-MCP executable path
- endpoint and transport
- error message if installation fails

It does **not** upload logs, browser data, passwords, tokens, or files.

## Validate locally

```bash
python scripts/validate_payloads.py
```

## Important

Do not commit or publish a real Discord webhook URL unless the repository is private and you are intentionally accepting that exposure risk.
