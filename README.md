# RPG GM Repository — timevans666

A working repository for **scenario development, GM resources, and play history** across multiple game systems and conventions.

---

## What's in Here

This repo has two distinct areas:

### 1. Convention Events

Scenario prep files tied to specific conventions. Each convention has its own section.

#### ChaosiumCon UK 2026 — `scenarios/`

| Event | Title | System | Day | Time |
|-------|-------|--------|-----|------|
| 91 | BRP – The Night Crawler | BRP | Fri Day 2 | 7:00–10:50pm |
| 92 | CoC 1980 – Last Train to Coney Island | Call of Cthulhu | Sun Day 4 | 7:00–10:50pm |
| 93 | CoC 1920s – Not Another Telegram | Call of Cthulhu | Sat Day 3 | 7:00–10:50pm |
| 94 | CoC Gaslight – The Curious Case of the Yorkshire | Call of Cthulhu | TBC | TBC |
| 95 | Ringworld RPG – A Question of Singularity | Ringworld RPG | Fri Day 2 | 2:00–5:50pm |
| 96 | Ringworld RPG – Is Love the Answer? | Ringworld RPG | Sat Day 3 | 2:00–5:50pm |
| 159 | BRP – Day One | BRP | Sun Day 4 | 2:00–5:50pm |

*As new conventions are added, they will appear here as separate entries alongside their own folders.*

---

### 2. Scenario Library — `scenario-library/`

A permanent personal archive of RPG scenarios across all games — not tied to any specific event. Organised by game system. Use this to track what exists, what has been run, and what could be revisited or adapted.

```
scenario-library/
├── call-of-cthulhu/
├── brp/
├── ringworld/
├── stormbringer/
└── other-games/
```

See [`scenario-library/README.md`](scenario-library/README.md) for the full index and filing guide.

---

## Repository Structure

```
ChaosiumCon26/
├── README.md
├── SCENARIO-TEMPLATE.md          # Template for convention event scenario files
├── sync.sh                       # Push changes to GitHub
├── session-start.sh              # Pull latest at start of each session
│
├── scenarios/                    # ChaosiumCon UK 2026 event scenarios
│   ├── event-91-brp-the-night-crawler.md
│   ├── event-92-coc-1980-last-train-to-coney-island.md
│   ├── event-93-coc-1920s-not-another-telegram.md
│   ├── event-94-coc-gaslight-curious-case-yorkshire.md
│   ├── event-95-ringworld-question-of-singularity.md
│   ├── event-96-ringworld-is-love-the-answer.md
│   ├── event-159-brp-day-one.md
│   ├── art/                      # Scenario artwork and SVGs
│   └── gm-docs/                  # GM companion apps
│
├── asset-library/                # System reference sheets
│   ├── coc-7e/
│   ├── brp-modern/
│   ├── ringworld-1984/
│   └── stormbringer-1e/
│
└── scenario-library/             # Personal scenario archive (all games, all time)
    ├── README.md
    ├── SCENARIO-LIBRARY-TEMPLATE.md
    ├── call-of-cthulhu/
    ├── brp/
    ├── ringworld/
    ├── stormbringer/
    └── other-games/
```

---

## Working with Claude

### Each session:
1. Claude pulls the latest from GitHub at the start
2. We work on scenarios, assets, or the library
3. Claude pushes after every meaningful change

### What can be worked on:
- **Convention event scenario development** — building out `scenarios/event-XX-*` files
- **GM apps** — HTML tools, character pickers, random generators
- **Scenario artwork** — SVG illustrations for handouts or atmosphere
- **Scenario library** — filing new scenarios, updating play history, indexing what exists

---

*Repo: https://github.com/slaguru666/ChaosiumCon26*
