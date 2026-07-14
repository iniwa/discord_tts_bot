# AGENTS.md

## Purpose
This file is the Codex-side working agreement for `discord_tts_bot`.

Codex uses this file to preserve design intent, decide whether work should stay in Codex or be handed off to Claude Code, and review implementation results.
Claude Code uses `CLAUDE.md` for execution rules.

## Project Summary
- Project name: `discord_tts_bot`
- Purpose: Simple lightweight Discord TTS bot intended to run on Raspberry Pi via Docker.
- Summary from project docs: Simple lightweight Discord TTS bot intended to run on Raspberry Pi via Docker.
- Runtime target: Raspberry Pi Docker linux/arm64
- Repository path: `D:\Git\discord_tts_bot`
- Stack: Python, discord.py, Open JTalk, Docker

## Base References
- Codex base: `D:/Git/CLAUDEmdStrage/_base/AGENTS.md`
- Claude Code base for Windows/local projects: `D:/Git/CLAUDEmdStrage/_base/CLAUDE_windows.md`
- Claude Code base for Raspberry Pi Docker projects: `D:/Git/CLAUDEmdStrage/_base/CLAUDE_docker.md`

## Role Split / Model Policy
- GPT-5.6 Terra (`gpt-5.6-terra`) or Sol (`gpt-5.6-sol`) owns requirements and design. Prefer Sol for substantial ambiguity, risk, or cross-boundary reasoning.
- After design is fixed, GPT-5.6 Luna Max (`gpt-5.6-luna-max`) coordinates implementation through small, sequential handoffs: one independently verifiable route, subsystem boundary, or lifecycle path plus its direct regression tests.
- Claude Code Sonnet 5 performs delegated edits and verification at effort medium from the repository root: `claude -p --model sonnet --permission-mode auto "<handoff/task prompt>"`.
- Handoffs state the goal, files, constraints, non-goals, verification, and concrete data sources so Sonnet needs no design judgment. Claude Code implements only the current slice and returns design questions to Codex.
- Luna Max reviews each result before preparing the next slice. Material design questions return to Terra/Sol instead of changing the approved design.
- Codex may keep small or design-sensitive changes in one context. Fable 5 is only a medium-effort second opinion for difficult design decisions.
- Claude Code subagents are optional and limited to clearly parallel mechanical work; they inherit the handoff and may not expand scope, change design, add dependencies, alter deployment or external exposure, or touch secrets.
- On Windows, keep delegated command lines ASCII-only, put non-ASCII instructions in a UTF-8 handoff file, and close background `codex exec` stdin with `$null |`. If an intended model is unavailable, use an available model only when the work remains safe and report the limitation.

## Decision Rule
Keep work in Codex when:
- requirements are ambiguous
- design intent or responsibility boundaries may change
- the task is small enough to edit and review in one context
- the main value is planning, review, or documentation consistency

Hand off to Claude Code when:
- goal, files, constraints, non-goals, and verification are clear
- the task is mostly implementation or mechanical editing
- the allowed edit scope can be stated explicitly
- Claude Code tooling or iteration speed is useful

## Project-Specific Guidance
- Use Raspberry Pi / Docker guidance from `D:/Git/CLAUDEmdStrage/_base`.
- Preserve `linux/arm64` compatibility unless the project explicitly supports more architectures.
- Do not change deployment, image naming, Portainer, or external exposure behavior without explicit approval.

## Files To Inspect First
- README.md
- bot.py
- requirements.txt
- Dockerfile
- docker-compose.yaml

## Files Claude Code May Edit In Scoped Tasks
- bot.py
- requirements.txt
- Dockerfile
- docker-compose.yaml

## Constraints
- Keep the bot simple and lightweight.
- Preserve Raspberry Pi / arm64 compatibility.
- Do not include real Discord tokens or secrets.
- Keep voice assets and dictionaries out of unrelated refactors.
- Do not commit automatically unless explicitly requested.
- Do not revert user or other-agent changes unless explicitly requested.
- Do not edit secrets, credentials, `.env`, local runtime data, or generated heavy artifacts unless explicitly requested.

## Handoff Template
When Codex hands work to Claude Code, create `docs/handoffs/YYYY-MM-DD-<short-task>.md`. Create the `docs/handoffs/` directory if it does not exist. Use this format in that file.

```md
Read AGENTS.md, CLAUDE.md, and this handoff file before implementation.
If implementation would violate constraints or require files outside this handoff, stop and ask before editing.

## Goal
...

## Background
...

## Files To Inspect
- ...

## Files To Edit
- ...

## Constraints
- ...

## Non Goals
- ...

## Verification
- ...

## Expected Report
- Changed files
- Summary
- Verification results
- Blocked checks
- Design questions for Codex
```

## Codex Review Checklist
After Claude Code returns, review:
- Did the diff stay inside the handoff?
- Did any file outside `Files To Edit` change? If yes, was it necessary?
- Did the implementation preserve stated constraints and non-goals?
- Did it introduce dependencies, build tooling, packaging, CI/CD, deployment changes, or external exposure changes unexpectedly?
- Did it touch secrets, credentials, `.env`, local settings, or runtime data?
- Did verification run, and are blocked checks explained?
- Does any discovery need to become a new `AGENTS.md` or `docs/*.md` decision?

## Knowledge Persistence
- Use `AGENTS.md` for durable workflow and design decisions.
- Use `docs/*.md` for reusable technical notes, architecture details, procedures, and project-specific knowledge.
- Before meaningful work, check relevant existing docs.
- Do not silently encode durable design decisions only in code.

## Design Record Scope
Keep `AGENTS.md` focused on short, durable rules that future Codex and Claude Code sessions must follow.

Do not add `Alternatives Considered` as a default Decision Log heading. When rejected options or longer background matter, summarize only the durable rule in `AGENTS.md` and put the detail under `docs/decisions/`.