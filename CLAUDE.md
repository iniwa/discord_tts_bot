# CLAUDE.md

## Project Overview
- Purpose: Simple lightweight Discord TTS bot intended to run on Raspberry Pi via Docker.
- Runtime target: Raspberry Pi Docker linux/arm64
- Stack: Python, discord.py, Open JTalk, Docker

## Coding Style
- Write lightweight, efficient code. Prefer minimal dependencies.
- Follow existing project patterns before adding new abstractions.

## Codex / Claude Code Workflow
- Treat `AGENTS.md` as the Codex-side source of design intent and this file as Claude Code execution rules. Follow a supplied handoff first, then this file, then local conventions.
- Terra/Sol owns requirements and design. After design is fixed, Luna Max coordinates small sequential handoffs; Claude Code Sonnet 5 performs the delegated edits and verification.
- Standard delegated execution from the repository root is `claude -p --model sonnet --permission-mode auto "<handoff/task prompt>"`. On Windows, keep the command line ASCII-only and read non-ASCII instructions from a UTF-8 handoff file.
- Implement and report only the current independently verifiable slice. Wait for Luna Max review before a later slice.
- If the handoff is ambiguous, conflicts with documented design, or requires files outside its scope, stop and return the question to Codex. Small, clearly scoped fixes may be requested directly.
- Subagents are optional and limited to clearly parallel mechanical work within the same constraints. If an intended model is unavailable, continue only when safe and report the limitation.
- Do not commit unless explicitly requested.

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
