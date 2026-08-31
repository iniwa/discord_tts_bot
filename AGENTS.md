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

- Before implementation, classify the initial route from acceptance evidence as `small-primary` for small or transfer-negative work, `bounded` for settled multi-step work with one verifiable writer, `adaptive` when unresolved native/platform/runtime or cross-subsystem behavior is material, or `non-implementation` for analysis, design, review, or operations. This does not force delegation; reclassify only after a material scope change or contract reset.
- Reintegrate through the stable diff and verification evidence; do not repeat delegated discovery merely to re-establish context.
- Identify a genuinely independent phase with its own acceptance and verification as a fresh Codex task or chat boundary.
- Use GPT-5.6 Sol as the preferred main worker; the user's actual runtime model and reasoning choice remains authoritative. Sol owns intent, design, approval boundaries, integration, and user communication and can directly finish small or transfer-negative work. Use configured Luna roles (`bounded_explorer`/`bounded_implementer`) for bounded work and Terra roles (`adaptive_implementer`/`bounded_reviewer`) for adaptive implementation or risk-justified review; do not force delegation or pin the main reasoning level in project instructions.
- Keep requirements, design, and small documentation corrections in the primary context. Ordinary delegation uses native Codex agents: one `bounded_implementer` for settled cohesive work when transfer helps, or `adaptive_implementer` directly when acceptance depends on unresolved platform, native lifecycle, or cross-layer behavior.
- Use `bounded_explorer` agents only for genuinely independent read-only discovery. Use a `bounded_reviewer` only for a concrete material correctness, security, compatibility, or verification risk, and only after the writer's stable self-review gate. If implementation changes after review starts, treat that review as diagnostic and run one fresh final review only when risk warrants it.
- Keep one active writer for overlapping files. After a second correction round, or two blocked/partial returns, reset the primary contract before continuing. If custom roles are not observable, keep the work in the primary context or use an observable equivalent.
- Claude Code is not an approved execution route unless the user explicitly changes project policy.
- Prefer the smallest correct change and reuse existing or platform-native capabilities before adding dependencies or abstractions.

## Durable Project Rules

- Keep the bot simple, lightweight, and compatible with Raspberry Pi `linux/arm64`.
- Preserve the existing Open JTalk, dictionary, voice-file, FFmpeg, tmpfs, queue, and Discord command behavior unless the approved task changes it.
- Keep mutable state outside the image. Preserve the established host mounts for `word_dict.json`, `settings.json`, and logs.
- Preserve non-root container execution and the startup ownership handling required by mounted files and `/ram_cache`.
- Preserve stdout logging alongside rotating file logging and its `LOG_FILE` override.
- Do not change image naming, GHCR publication, supported platforms, Compose/Portainer deployment, mounts, restart behavior, resource limits, or external exposure unless explicitly requested.

## Safety and Approval Boundaries

Personal-use iteration is the default unless the user or verified project
requirements establish stronger obligations. Use the smallest normal-path
implementation, a brief useful check, then the known existing target and
procedure for routine reversible deployment/application and necessary restart,
smoke normal use,
fix observed errors, and finish when requested normal operation works. Do not
require speculative edge-case matrices, hardening, abstractions, new tests, or
a full suite for ordinary changes. Required safety, data, and approval gates
still precede application; a required pre-application review receives the
stable source/diff and pre-application checks first, with runtime not run or
passed. The initial implementation or fix request supplies standing permission
for this bounded routine cycle, so no fresh confirmation is needed. This does
not infer Git commit/push/merge, publication/release/registry or hosted-config
changes, credentials/permissions/exposure, destructive data or migrations, new
targets or cost, or project-specific protected operations. If a target or
check is unavailable, report readiness separately; record only required
deferred checks in the existing issue or ledger with verification, approval,
and resume conditions.

- Preserve unrelated user and other-agent changes. Treat unexpected diffs as having unknown authorship and keep them outside the current task unless confirmed.
- Do not inspect secrets, credentials, personal data, `.env`, real Discord tokens, production dictionaries or settings, logs, runtime state, generated audio, or `mei_normal.htsvoice` contents unless strictly necessary for the approved task.
- Do not edit secrets, credentials, `.env`, local settings, production data, runtime state, generated audio, or `mei_normal.htsvoice` unless the approved task explicitly requires the change.
- Never reproduce secrets, credentials, personal data, or private infrastructure values in prompts, handoffs, reports, or external tools. Never store a real Discord token or other credential in tracked files.
- Do not add dependencies or change build tooling, packaging, CI/CD, deployment procedure or configuration, publication, or external exposure outside the approved task scope.
- Do not commit, push, or publish unless explicitly requested. Routine reversible deployment/application and necessary restart may use the bounded personal-use allowance above on the established target and known procedure; other deployment requires explicit authorization.

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
