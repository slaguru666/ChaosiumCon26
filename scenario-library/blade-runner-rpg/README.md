# Blade Runner RPG — Scenario Library

Scenarios for **The Blade Runner Roleplaying Game** (Free League Publishing, Year Zero Engine), set in the world of Blade Runner 2019 / 2049.

Default setting year: **2037** — ten years after the Blackout, twelve years before *Blade Runner 2049*. The Wallace Corporation monopoly is established. Replicants are legal under license. Most Nexus-8s are presumed retired. The LAPD Rep-Detect division — Blade Runners — hunts the ones that aren't.

---

## Scenario Index

| File | Title | Players | Duration | Tone | Status |
|------|-------|---------|----------|------|--------|
| [`directive-19.md`](directive-19.md) | **Directive 19** | 6 | 3.5 hrs | Cold noir, slow-burn investigation, action mid-act, escape ending | Ready |

---

## Companion Apps

GM HTML apps live under `apps/[scenario-name]/index.html`. They are single-file, offline-capable, designed for tablet or laptop at the table.

| App | Scenario |
|-----|----------|
| [`apps/directive-19/index.html`](apps/directive-19/index.html) | Directive 19 |

---

## Art

Scenario-specific artwork lives in `art/[scenario-name]/`. Midjourney generation prompts live at [`art/midjourney-prompts.md`](art/midjourney-prompts.md). Style guide for Blade Runner RPG scenarios: **Moebius / Syd Mead influence, ink linework with colour wash, 1980s European sci-fi comics aesthetic.** Not photorealistic. Heavy chiaroscuro with neon accent lighting. Blueprint scenery maps use a separate **LAPD evidence-archive blueprint** style — white and pale cyan technical lines on Prussian-blue ground, with case-file stamping.

---

## System Mechanics Quick Reference

The Blade Runner RPG uses a custom Year Zero Engine variant. Inline mechanics callouts in scenarios use the `[BR: ...]` tag format:

- `[BR: Manipulation]` — convince, deceive, intimidate verbally
- `[BR: Insight]` — read another's intent or emotional state
- `[BR: Observation]` — notice details, spot hidden
- `[BR: Connect]` — work contacts, pull in favours
- `[BR: Tech]` — interface with technology, hack, repair
- `[BR: Medical Aid]` — patch wounds, identify causes of death
- `[BR: Stamina / Force]` — endure, intimidate physically
- `[BR: Mobility / Stealth]` — move unseen, evade
- `[BR: Firearms / Close Combat]` — combat
- `[BR: Driving]` — vehicle handling
- `[BR: Stress test]` — accumulated pressure, used after a failed roll
- `[BR: V-K]` — Voigt-Kampff replicant detection test
- `[BR: Humanity]` — replicant identity / Empathy roll under pressure

Skills roll dice pool = Attribute (A/B/C/D = 12/10/8/6) + Skill (A/B/C/D = 12/10/8/6) as D6s; count 6s as successes. One success = pass. Stress dice are added in stressful situations and can cause Stress accumulation on a 1.

---

## Filing Convention

Use [`../SCENARIO-LIBRARY-TEMPLATE.md`](../SCENARIO-LIBRARY-TEMPLATE.md) as the base, but extend toward the full convention template (see [`/SCENARIO-TEMPLATE.md`](../../SCENARIO-TEMPLATE.md)) when building scenarios with 6 pre-gens, three-act structure, and HTML companion apps.
