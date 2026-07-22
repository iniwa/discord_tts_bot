# AGENTS.md

## Purpose

This is the Codex-side working agreement for `discord_tts_bot`, a lightweight self-hosted Discord text-to-speech bot.

`AGENTS.md` owns design intent, model and handoff policy, Codex review, and documentation lifecycle. `CLAUDE.md` owns implementation, verification, and reporting rules.

## Project Facts

- Runtime: Python 3.11 in Docker, primarily on Raspberry Pi `linux/arm64`.
- Entry point: `bot.py`.
- Core stack: discord.py, Open JTalk, MeCab dictionary data, FFmpeg, and lightweight Python dependencies in `requirements.txt`.
- Container definitions: `Dockerfile` and `docker-compose.yaml`.
- The published image workflow supports `linux/amd64` and `linux/arm64`; Raspberry Pi compatibility must remain intact.
- Open JTalk dictionary, voice data, and temporary audio are copied into the `/ram_cache` tmpfs at runtime.
- `word_dict.json`, `settings.json`, and application logs are mutable host-mounted data in production. The tracked `word_dict.json` is sample data.
- Logging must remain available on stdout and through the rotating file handler.

## Instruction Precedence

When instructions conflict, apply them in this order:

1. Runtime, tool, organization, and safety policy.
2. Explicit user instructions that change project policy.
3. Durable project instructions.
4. Other instructions for the current user task and the approved task scope.

The active handoff or equivalent inline prompt is the approved task scope. Verified project facts override generation-source defaults. Only an explicit user instruction to change project policy may revise a durable project rule; other task instructions and approved scopes may narrow durable rules but may not weaken them. Report unresolved conflicts instead of guessing.

## Model and Role Policy

- Use GPT-5.3-Codex-Spark (`gpt-5.3-codex-spark`) proactively, when available, for low-risk, well-scoped, independently verifiable supporting work that requires no material design judgment or source-code implementation.
- GPT-5.6 Terra (`gpt-5.6-terra`) or Sol (`gpt-5.6-sol`) owns requirements and design. Whenever Terra is used, set its reasoning level to `high`. Prefer Sol for substantial ambiguity, risk, or cross-boundary reasoning.
- Run every Claude Code task with `--permission-mode auto`.
- After design is fixed, delegate source-code implementation first to Claude Code Sonnet at effort medium from the repository root: `claude -p --model sonnet --effort medium --permission-mode auto "<handoff/task prompt>"`.
- Only when Sonnet is unavailable because of usage limits or service availability, use GPT-5.6 Luna (`gpt-5.6-luna`) with reasoning level `max` for the same implementation slice.
- Implementation failure, failed verification, or a design question is not model unavailability; return it to Codex.
- Apply this policy to every coordinating Codex model and its subagents. Do not create coordinator-specific exceptions unless the user explicitly changes project policy.
- Codex may keep requirements, design, read-only investigation, review, synthesis, and small documentation-consistency changes in one context.
- Claude Code subagents are optional and limited to clearly parallel mechanical work inside the approved task scope. They inherit its constraints.

## Durable Project Rules

- Keep the bot simple, lightweight, and compatible with Raspberry Pi `linux/arm64`.
- Preserve the existing Open JTalk, dictionary, voice-file, FFmpeg, tmpfs, queue, and Discord command behavior unless the approved task changes it.
- Keep mutable state outside the image. Preserve the established host mounts for `word_dict.json`, `settings.json`, and logs.
- Preserve non-root container execution and the startup ownership handling required by mounted files and `/ram_cache`.
- Preserve stdout logging alongside rotating file logging and its `LOG_FILE` override.
- Do not change image naming, GHCR publication, supported platforms, Compose/Portainer deployment, mounts, restart behavior, resource limits, or external exposure unless explicitly requested.

## Safety and Approval Boundaries

- Preserve unrelated user and other-agent changes. Treat unexpected diffs as having unknown authorship and keep them outside the current task unless confirmed.
- Do not inspect secrets, credentials, personal data, `.env`, real Discord tokens, production dictionaries or settings, logs, runtime state, generated audio, or `mei_normal.htsvoice` contents unless strictly necessary for the approved task.
- Do not edit secrets, credentials, `.env`, local settings, production data, runtime state, generated audio, or `mei_normal.htsvoice` unless the approved task explicitly requires the change.
- Never reproduce secrets, credentials, personal data, or private infrastructure values in prompts, handoffs, reports, or external tools. Never store a real Discord token or other credential in tracked files.
- Do not add dependencies or change build tooling, packaging, CI/CD, deployment, publication, or external exposure outside the approved task scope.
- Do not commit, push, publish, or deploy unless explicitly requested.

## Handoff Workflow

- Keep policy, design, review, read-only investigation, and small documentation corrections in Codex.
- One handoff covers one cohesive, independently verifiable change and its direct regression coverage when applicable. Run unresolved discovery as a separate read-only slice.
- State the goal, files to inspect and edit, constraints, non-goals, concrete data sources, acceptance criteria, verification, and expected report.
- Treat a delegation that ends before meeting its acceptance criteria as interrupted. Record usable partial results, verification, remaining scope, and the resume condition; narrow the behavior, files, and verification before rerunning it.
- The implementer works only on the current slice and returns design questions to Codex. Codex reviews the report and diff before starting another slice.
- Keep active or blocked handoffs in `docs/handoffs/`. Move a handoff to `docs/handoffs/archive/` only after implementation, verification, review, required runtime work, and follow-up are complete.

## Verification and Review

Use the smallest check that demonstrates the scoped change:

- Run `git diff --check` for every change.
- Run `python -m py_compile bot.py` for Python changes.
- Run `docker compose config` for Compose changes when Docker Compose is available.
- For dependency, Dockerfile, or architecture-sensitive changes, perform the focused container build or runtime check available in the approved environment and report any target-host check that remains blocked.

During review, compare the final status and diff with the captured Git baseline. Confirm that the diff stayed in scope, preserved arm64 and mutable-data boundaries, introduced no unapproved dependency or deployment change, kept secrets and heavy assets untouched, and reported blocked or interrupted verification explicitly.

## Documentation Lifecycle

- Keep this file limited to short, current, durable rules and links.
- Put detailed decisions and evidence in `docs/decisions/`.
- Keep current decision guidance active; archive it only when fully implemented and no longer needed.
- Put reusable procedures in an appropriate `docs/` location.
- Do not rewrite completed handoffs or archived decisions merely to match a newer shared policy.
