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

## Option A: environment-gated payload

Run these in PowerShell, then restart the PowerShell/user session so `setx` variables are available:

```powershell
setx WINDOWS_MCP_INSTALL_AUTHORIZED "YES"
setx WINDOWS_MCP_DISCORD_WEBHOOK "https://discord.com/api/webhooks/..."
```

Then use:

```text
payloads/Install_Windows_MCP_Discord_Webhook.txt
```

## Option B: plug-and-play hardcoded payload

For a fully autonomous payload, generate a local artifact with the Discord webhook hardcoded:

```bash
python scripts/build_plug_and_play_payload.py \
  --webhook "https://discord.com/api/webhooks/..."
```

Output:

```text
dist/Install_Windows_MCP_Discord_Webhook_PLUG_AND_PLAY.txt
```

That generated `dist/` file is the plug-and-play payload. It does not require Windows environment variables.

Important: `dist/` is gitignored because the generated payload contains your real Discord webhook URL. Do not commit it or publish it.

## Validate locally

```bash
python scripts/validate_payloads.py
python scripts/build_plug_and_play_payload.py --webhook "https://discord.com/api/webhooks/123456789012345678/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
```

## Notes

- The payload is experimental until tested on physical hardware.
- Keep real Discord webhook URLs out of git history.
- Use the committed environment-gated payload for public sharing.
- Use the generated `dist/` payload for private, plug-and-play deployment.
