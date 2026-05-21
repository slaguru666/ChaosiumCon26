# Scenario Library

A personal archive of RPG scenarios written and run by **timevans666** across all games and conventions over time.

This is separate from specific convention events. It exists so there is a permanent, searchable record of every scenario — what it was, when it was run, what worked, and what can be revisited or adapted.

---

## Organisation

Scenarios are filed by **game system**. Each system folder contains individual scenario files, plus a system-level reference sheet.

```
scenario-library/
├── call-of-cthulhu/       # CoC 7e scenarios (any era)
├── brp/                   # Generic BRP scenarios
├── ringworld/             # Ringworld RPG scenarios
├── stormbringer/          # Stormbringer / Elric scenarios
├── blade-runner-rpg/      # Blade Runner RPG (Free League) — LA 2037 default
└── other-games/           # Any other system
```

---

## Scenario Index

| Title | System | Era / Setting | First Run | Status |
|-------|--------|---------------|-----------|--------|
| [Power Failure](other-games/sla-power-failure.md) | SLA Industries | Mort, Downtown District 2 | not yet run | ready |
| [Directive 19](blade-runner-rpg/directive-19.md) | Blade Runner RPG | Los Angeles, 2037 | not yet run | ready |

---

## Scenario Status Key

| Status | Meaning |
|--------|---------|
| `draft` | Early development, not yet run |
| `ready` | Fully written, ready to run |
| `run` | Has been run at least once |
| `retired` | Not intended to run again |
| `adaptable` | Can be reused / reskinned for other events |

---

## File Structure Per Scenario

Each scenario has:
- `[system]-[title].md` — main scenario file (players may see premise/structure)
- `[system]-[title]-gm.md` — GM companion (NPC secrets, encounter notes, handout text)
- `art/[system]-[title]/` — maps and artwork (SVG floor plans, handouts)

---

## Adding a New Scenario

1. Choose the correct system folder
2. Create files using the naming convention above
3. Use `SCENARIO-LIBRARY-TEMPLATE.md` as starting point for the main file
4. Add a row to the index table above
5. Update the system folder README
6. Push to GitHub
