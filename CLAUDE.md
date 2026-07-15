# CLAUDE.md

## Purpose

This file contains Claude Code execution rules for `discord_tts_bot`. Design intent, model selection, handoff policy, and Codex review belong in `AGENTS.md`.

## Read First

Before editing, read:

- `AGENTS.md` and this file.
- The supplied handoff, when present.
- The files listed for inspection and the existing nearby implementation.
- `README.md`, `Dockerfile`, `docker-compose.yaml`, and `requirements.txt` when the task affects runtime or deployment behavior.

If the instructions conflict, required files are outside the approved scope, or design remains unresolved, stop and return the issue to Codex.

## Project Shape

- `bot.py` is the Python 3.11 application entry point.
- `requirements.txt` owns Python dependencies.
- `Dockerfile` builds the Open JTalk and FFmpeg runtime.
- `docker-compose.yaml` defines tmpfs, mutable mounts, environment, restart, resource, and logging behavior.
- The primary runtime is Raspberry Pi `linux/arm64`; the image workflow also supports `linux/amd64`.

## Execution Rules

- Implement only the current independently verifiable slice and wait for Codex review before starting another.
- Keep changes simple and follow the existing single-bot architecture before adding abstractions or dependencies.
- Preserve Raspberry Pi arm64 compatibility and the existing Open JTalk, MeCab dictionary, FFmpeg, voice-file, tmpfs, queue, and command behavior unless the task explicitly changes it.
- Keep `word_dict.json`, `settings.json`, and logs as mutable host-mounted state outside the image.
- Preserve non-root execution and startup ownership handling for mounted files and `/ram_cache`.
- Preserve stdout logging as well as rotating file logging and the `LOG_FILE` override.
- Return any proposed dependency, image, platform, mount, Portainer, deployment, CI/CD, registry, or external-exposure change outside the approved handoff to Codex.
- On Windows, keep a delegated command line ASCII-only when its instructions contain non-ASCII text; put those instructions in a UTF-8 handoff file.

## Safety and Scope

- Preserve unrelated user and other-agent changes. Treat unexpected diffs as having unknown authorship and exclude them from the task.
- Do not read, edit, or expose `.env`, real Discord tokens, production `word_dict.json`, production `settings.json`, logs, runtime state, or generated audio.
- The tracked `word_dict.json` is sample data; edit it only when the task explicitly targets the sample.
- Do not modify or replace `mei_normal.htsvoice` in unrelated work.
- Do not add dependencies or change build, packaging, deployment, publication, or external exposure unless the approved task explicitly requires it.
- Do not commit, push, publish, or deploy unless explicitly requested.

## Verification

Run the smallest relevant verification:

- Always run `git diff --check`.
- For Python changes, run `python -m py_compile bot.py`.
- For Compose changes, run `docker compose config` when available.
- For dependency, Dockerfile, or architecture-sensitive changes, run the focused container build or runtime check available within scope.
- Report target-host or Docker checks that could not run and why.

## Report

Return:

- Changed files.
- Concise summary.
- Verification commands and results.
- Blocked checks.
- Subagent usage.
- Design questions for Codex.

Report reusable discoveries to Codex. Update durable documentation only when it is inside the approved scope.
