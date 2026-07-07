# CLAUDE.md

## Project Overview
- Purpose: Simple lightweight Discord TTS bot intended to run on Raspberry Pi via Docker.
- Runtime target: Raspberry Pi Docker linux/arm64
- Stack: Python, discord.py, Open JTalk, Docker

## Coding Style
- Write lightweight, efficient code. Prefer minimal dependencies.
- Follow existing project patterns before adding new abstractions.

## Codex / Claude Code Workflow
- This `CLAUDE.md` is for Claude Code execution rules.
- Codex handoffs should normally be saved under `docs/handoffs/`; when a handoff file path is provided, read it before editing.
- If the project also has `AGENTS.md`, treat it as the Codex-side source of design intent, handoff rules, and review criteria.
- When the user provides a Codex handoff, follow that handoff first, then this file, then local project conventions.
- If the task is ambiguous, requires changing documented design intent, or needs files outside the handoff, stop and ask before editing.
- Do not commit automatically unless explicitly requested.
- Report changed files, summary, verification results, blocked checks, and any design questions that should return to Codex.

## Model Policy
- Run in auto mode (automatic model selection). No fixed coordinator model or default subagent delegation.
- Codex handoffs are written to be completable without design judgment. If a design decision turns out to be required, stop and return the question to Codex.
- Do not change documented design intent, add dependencies, or alter build/deploy/external exposure without explicit instruction.
- If the environment cannot follow this premise, continue with the available model and report the limitation.

## Environment
- Primary environment: Raspberry Pi Docker / linux/arm64
- Working in `D:/Git/` means Home Sub PC.
- Working in `C:/Git/` means Home Main PC.
- Working in `C:/Users/**/Documents/git/` means Remote PC with limited environment.
- Raspberry Pi is accessible via `ssh iniwapi` for reading code/logs.
- Preserve Docker and arm64 deployment behavior unless explicitly requested.

## Important Files
- README.md
- bot.py
- requirements.txt
- Dockerfile
- docker-compose.yaml

## Protected Files
- Do not edit or delete: `.env`, real `word_dict.json` / `settings.json` runtime data, `mei_normal.htsvoice`, secrets.
- Repo copies of `word_dict.json` are sample data; production data lives on the Raspberry Pi host.

## Verification
- Run the checks listed in the Codex handoff.
- Baseline check when no handoff specifies one: `python -m py_compile bot.py`
- If verification cannot be run, report the reason.

## Reporting
- Changed files
- Summary
- Verification results
- Blocked checks
- Design questions for Codex

## Tooling
- Use **Serena MCP** tools for code navigation and editing to maximize efficiency (symbol search, overview, replace, insert, etc.)
- Use **Tavily MCP** tools for web search and research:
  - `tavily_search` — General web search for documentation, error messages, library usage, etc.
  - `tavily_crawl` — Crawl a specific website for detailed information
  - `tavily_extract` — Extract structured content from a URL
  - `tavily_research` — In-depth research on a topic (use for complex or multi-faceted questions)

## Knowledge Persistence
Durable project workflow decisions belong in AGENTS.md. Surface implementation discoveries that should guide future sessions so Codex can decide whether to record them.
Detailed design history belongs in `docs/decisions/`. Keep `AGENTS.md` focused on short, durable rules; do not add `Alternatives Considered` as a default Decision Log heading there.
