# AGENTS.md — CTF workspace instructions

## Canonical disk layout (siblings under `D:\download\`)

| Path | Role |
|------|------|
| `D:\download\CTFTimeWriteup` | This repo — event writeups |
| `D:\download\ctf-ai-system` | Full CTF AI skill pack |
| `D:\download\hexstrike-ai` | HexStrike AI (API + MCP) |

See also `D:\download\PROJECTS.md`.

## Primary skill pack

**Load / obey:** Grok skill `ctf-ai-system` → `D:\download\ctf-ai-system` (junction under `~\.grok\skills\`).

Entry files:

| File | Role |
|------|------|
| `ctf-ai-system/SKILL.md` | Skill entry + map |
| `ctf-ai-system/PROMPTS/ctf_solver_master_prompt.md` | Read before starting a challenge; full solve/research/HexStrike/capture workflow |
| `ctf-ai-system/SYSTEM_PROMPT.md` | How to solve |
| `ctf-ai-system/AGENT_RULES.md` | Speed + evidence rules |
| `ctf-ai-system/KNOWLEDGE/sources_index.md` | What we already know |

Before solving any new challenge, read the canonical master prompt at
`D:\download\ctf-ai-system\PROMPTS\ctf_solver_master_prompt.md`. Do not copy
the full prompt into this repository; `ctf-ai-system` is the single source of truth.

## Event writeups

Per-event folders (same challenge layout: `category/challenge/{chalenge.md,files,solve,writeup}`):

- `BushBash2026/`
- `L3akCTF2026/`
- `LIT2026/`
- `KaliCTF2026/` — Kali Team - CTF 26 (https://kali-team.online/challenges)
- `UIUCTF2026/`
- `HTB-TryOut/` — HackTheBox CTF Try Out (categories: `rev/`, `web/`, `pwn/`, ...)

## Output location (HARD RULE)

Write ALL solve output into the EXISTING challenge folder for the task, using the
canonical layout `<event>/<category>/<challenge>/{solve/,writeup/,final_flag.txt}`.

- Use the real challenge folder that already holds `chalenge.md`. Write with paths
  RELATIVE to it (`solve/solve.py`, `writeup/writeup.md`).
- NEVER invent new event/challenge folders, and NEVER name a folder after lore/flavor
  text in the challenge description (e.g. a device or story name). Use the folder that
  already exists.
- The writeup title = the real challenge name (the folder name), not a name guessed
  from the story.
- Check the current working directory before the first Write.

## After every solve

1. Event writeup path  
2. `D:\download\ctf-ai-system\OUTPUT\<id>\`  
3. `D:\download\ctf-ai-system\KNOWLEDGE\cards\<id>.yaml`  
4. Update `sources_index.md`  

## Do not

- Full-scan with HexStrike by default  
- Fabricate flags  
- Skip knowledge capture  
- Clone HexStrike / ctf-ai-system into temporary Grok worktrees  