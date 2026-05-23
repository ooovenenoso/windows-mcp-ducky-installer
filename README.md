# Windows-MCP Ducky Installer

Authorized DuckyScript payload for installing [CursorTouch/Windows-MCP](https://github.com/CursorTouch/Windows-MCP) on a Windows lab machine and sending a minimal installation status message to a Discord webhook.

## Safety model

This repo is intended for systems you own or have explicit permission to administer.

The payload is intentionally gated by Windows user environment variables:

- `WINDOWS_MCP_INSTALL_AUTHORIZED=YES`
- `WINDOWS_MCP_DISCORD_WEBHOOK=<your Discord webhook URL>`

No webhook URL, token, API key, password, or secret is stored in the payload.

The Discord message includes only installation metadata:

- status
- Windows username
- computer name
- log path
- Windows-MCP executable path
- endpoint and transport
- error message if installation fails

It does **not** upload logs or secrets.

## Payload

- [`payloads/Install_Windows_MCP_Discord_Webhook.txt`](payloads/Install_Windows_MCP_Discord_Webhook.txt)

What it does:

1. Opens PowerShell.
2. Verifies explicit authorization through `WINDOWS_MCP_INSTALL_AUTHORIZED=YES`.
3. Reads the Discord webhook from `WINDOWS_MCP_DISCORD_WEBHOOK`.
4. Installs Python 3.13 with `winget` if Python is missing.
5. Installs `uv` if missing.
6. Installs `windows-mcp` with `uv tool install windows-mcp`.
7. Registers Windows-MCP with:

   ```powershell
   windows-mcp install --transport sse --host 127.0.0.1 --port 8000
   ```

8. Checks for the `windows-mcp-server` Scheduled Task.
9. Sends a Discord embed with success/failure metadata.

## Windows setup before running

Run these in PowerShell, then restart the PowerShell/user session so `setx` variables are available:

```powershell
setx WINDOWS_MCP_INSTALL_AUTHORIZED "YES"
setx WINDOWS_MCP_DISCORD_WEBHOOK "https://discord.com/api/webhooks/..."
```

## Validate locally

```bash
python scripts/validate_payloads.py
```

## Notes

- The payload is experimental until tested on physical hardware.
- Keep real Discord webhook URLs out of git history.
- If you adapt the payload, keep the explicit authorization gate and environment-based webhook configuration.
