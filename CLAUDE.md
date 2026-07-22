# CLAUDE.md

## Purpose

This file contains Claude Code execution rules for `discord_tts_bot`. Design intent, model selection, handoff policy, and Codex review belong in `AGENTS.md`.

## Read First

Before editing, read:

- `AGENTS.md` and this file.
- The supplied handoff or equivalent inline task scope.
- The files listed for inspection and the existing nearby implementation.
- `README.md`, `Dockerfile`, `docker-compose.yaml`, and `requirements.txt` when the task affects runtime or deployment behavior.

The handoff or equivalent inline prompt is the approved task scope. It may narrow durable project constraints but may not weaken them. If instructions conflict, required files are outside scope, or design remains unresolved, stop and return the issue to Codex.

## Project Shape

- `bot.py` is the Python 3.11 application entry point.
- `requirements.txt` owns Python dependencies.
- `Dockerfile` builds the Open JTalk and FFmpeg runtime.
- `docker-compose.yaml` defines tmpfs, mutable mounts, environment, restart, resource, and logging behavior.
- The primary runtime is Raspberry Pi `linux/arm64`; the image workflow also supports `linux/amd64`.

## Git Baseline and Scope

- Before editing, capture `git status --short` when Git is available. After editing, compare the final status and diff with that baseline.
- Do not reset, clean, stage, rewrite, or include pre-existing changes. Treat unexpected diffs as having unknown authorship.
- Implement only the current independently verifiable slice and wait for Codex review before starting another.
- Subagents are optional and limited to clearly parallel mechanical work within the same files, scope, and constraints.
- If the listed files are insufficient to reach the first scoped edit, stop and report the missing discovery or proposed split instead of broadening the search or redesigning the task.

## Execution Rules

- If the user writes in Japanese, respond in Japanese. Preserve the repository's established language for documentation, comments, identifiers, logs, and user-facing text unless the task changes it.
- Every Claude Code task runs with `--permission-mode auto`; this does not expand the approved scope or authorize otherwise restricted actions.
- Keep changes simple and follow the existing single-bot architecture before adding abstractions or dependencies.
- Preserve Raspberry Pi arm64 compatibility and the existing Open JTalk, MeCab dictionary, FFmpeg, voice-file, tmpfs, queue, and command behavior unless the task explicitly changes it.
- Keep `word_dict.json`, `settings.json`, and logs as mutable host-mounted state outside the image.
- Preserve non-root execution and startup ownership handling for mounted files and `/ram_cache`.
- Preserve stdout logging as well as rotating file logging and the `LOG_FILE` override.
- Return any proposed dependency, image, platform, mount, Portainer, deployment, CI/CD, registry, or external-exposure change outside the approved task scope to Codex.
- On Windows, keep a delegated command line ASCII-only when its instructions contain non-ASCII text; put those instructions in a UTF-8 handoff file.

## Safety and Scope

- Preserve unrelated user and other-agent changes and keep them outside the current task.
- Do not inspect secrets, credentials, personal data, `.env`, real Discord tokens, production `word_dict.json`, production `settings.json`, logs, runtime state, generated audio, or `mei_normal.htsvoice` contents unless strictly necessary for the approved task.
- Do not edit secrets, credentials, `.env`, local settings, production data, runtime state, generated audio, or `mei_normal.htsvoice` unless the approved task explicitly requires the change.
- Never reproduce secrets, credentials, personal data, or private infrastructure values in prompts, handoffs, reports, or external tools. Never store a real Discord token or other credential in tracked files.
- The tracked `word_dict.json` is sample data; edit it only when the task explicitly targets the sample.
- Do not add dependencies or change build tooling, packaging, CI/CD, deployment, publication, or external exposure outside the approved task scope.
- Do not commit, push, publish, or deploy unless explicitly requested.

## Verification

Run the smallest relevant verification:

- Always run `git diff --check`.
- For Python changes, run `python -m py_compile bot.py`.
- For Compose changes, run `docker compose config` when available.
- For dependency, Dockerfile, or architecture-sensitive changes, run the focused container build or runtime check available within scope.
- For documentation-only changes, do not run unrelated code or container checks.
- Report target-host or Docker checks that could not run and why.

## Report

Return:

- Status: `complete` only when the acceptance criteria are met; otherwise `interrupted`.
- Changed files and a concise summary.
- Verification commands and results, including blocked checks.
- Partial edits, usable results, remaining scope, and the resume condition when interrupted.
- Subagent usage and design questions for Codex.

Report reusable discoveries to Codex. Update durable documentation only when it is inside the approved scope.
