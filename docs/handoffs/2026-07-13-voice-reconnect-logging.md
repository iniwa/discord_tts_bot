Read AGENTS.md, CLAUDE.md, and this handoff file before implementation.
If implementation would violate constraints or require files outside this handoff, stop and ask before editing.

## Goal

Make Discord voice-disconnect diagnostics persist on the host and prevent an automatically retried voice disconnect from being reported as an ERROR.

## Background

The bot currently configures only standard output logging in `bot.py`. Although the Compose configuration rotates Docker's `json-file` logs, the recent traceback was no longer available when it was needed. The bot currently receives frequent library log records in this form:

```text
[ERROR] Disconnected from voice... Reconnecting in 1.67s.
Traceback (most recent call last):
```

This record is emitted by `discord.py` before its automatic reconnect attempt. A reconnectable interruption is operationally distinct from a terminal error. Retain diagnostics for later investigation while leaving genuine failures visible as ERROR.

## Files To Inspect

- README.md
- bot.py
- Dockerfile
- docker-compose.yaml

## Files To Edit

- README.md
- bot.py
- Dockerfile
- docker-compose.yaml

## Constraints

- Keep the bot simple, lightweight, and compatible with Raspberry Pi Docker (`linux/arm64`).
- Add no third-party Python dependencies.
- Preserve stdout logging so `docker logs` continues to work.
- Add a host-persisted application log directory through the sample Compose configuration, using a relative `./logs` host path.
- Use bounded, UTF-8 rotating application logs. The expected default is 10 MiB per file with three backup files (at most roughly 40 MiB total); document the retention clearly.
- Make the application log path configurable with `LOG_FILE`, defaulting to `/app/logs/discord_tts_bot.log`.
- Ensure the container creates `/app/logs` and gives the existing non-root `appuser` permission to write it before Python starts.
- Change only the recoverable `discord.voice_client` log record whose message begins `Disconnected from voice... Reconnecting in` from ERROR to WARNING at output time. Do not suppress its traceback, and do not downgrade unrelated `discord.py`, playback, Open JTalk, startup, or failed-reconnection errors.
- If creation of the application log file fails, the bot must still start and log that failure to stdout.
- Do not change deployment/exposure behavior, image naming, dependencies, voice assets, dictionaries, secrets, `.env`, or runtime data.

## Non Goals

- Do not implement a custom Discord reconnection loop or change discord.py reconnection timing/backoff.
- Do not claim a reconnect has succeeded before discord.py reports it.
- Do not alter existing Docker `json-file` logging settings.
- Do not add monitoring services, remote logging, or alerting integrations.
- Do not commit changes.

## Verification

- Run `python -m py_compile bot.py`.
- Run `docker compose config` to validate the Compose file, if Docker Compose is available; otherwise report the limitation.
- Review the diff to ensure edits stay within the four allowed files and no user changes are reverted.

## Expected Report

- Changed files
- Summary
- Verification results
- Blocked checks
- Design questions for Codex
