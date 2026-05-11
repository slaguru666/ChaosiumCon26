# GM Companion App — Design Template

## Purpose
An interactive, touch-optimised web application for running tabletop RPG scenarios at the table.
Designed for tablet or touchscreen laptop. No internet connection required during play.
Single HTML file per scenario — self-contained, portable, offline-ready.

---

## Design Principles
- **Touch-first:** All interactive elements minimum 48x48px tap targets
- **Low light friendly:** Dark theme default, dim mode available
- **One hand operable:** Key actions reachable with thumb on tablet
- **No scrolling during play:** Everything fits a screen at a time; navigation by tap
- **Distraction-free:** Clean, minimal UI — nothing that pulls the GM's eye away from the table
- **Instant access:** Any element reachable in 2 taps maximum

---

## Application Screens / Panels

### 1. SESSION DASHBOARD (Home Screen)
- Scenario title and system
- **Live session timer** with act checkpoint alerts (colour-coded: green / amber / red)
- Act progress indicator (visual bar showing current act and time remaining)
- Quick-jump buttons to each act
- One-tap access to: Handouts | Artwork | NPC List | Clue Tracker

### 2. ACT NAVIGATOR
- Swipeable / tappable panels: Introduction → Act 1 → Act 2 → Act 3 → Epilogue
- Current act summary always visible
- Pacing note visible at bottom of each act panel
- Fast-track button (tap to jump to climax if running late)

### 3. LOCATION CARDS
- Card-based layout, one location per card
- Tap card to expand: full description, atmosphere, secrets
- Tag indicating which act the location belongs to
- Link to associated artwork

### 4. NPC CARDS
- Portrait placeholder (artwork asset if available)
- Front of card: Name, role, disposition indicator (colour: green=friendly, amber=neutral, red=hostile, purple=hidden agenda)
- Tap to flip/expand: Physical description, motivation, what they know
- Secondary tap: Stat block (collapsible)
- HP tracker per NPC (tap +/- buttons)

### 5. CLUE TRACKER
- Visual trail map showing clue chain (Act 1 → Act 2 → Act 3)
- Each clue: tap to mark as Found / Missed
- Essential clues highlighted — if missed, fallback text auto-displays
- Optional clues shown as side branches on the trail
- Trail updates visually as clues are found

### 6. HANDOUT VIEWER
- Full-screen handout display — designed to be turned to face players or shown on a second screen
- Handouts categorised by act
- Tap to display, tap again to return to GM view
- Handout styled to match scenario period (e.g., yellowed paper for 1920s CoC, telex printout for BRP modern)
- Optional: QR code on handout links player to image on their phone

### 7. ARTWORK / ATMOSPHERE GALLERY
- Full-screen artwork display
- Categorised: Cover | Locations | NPCs | Handout Art | Atmosphere
- Tap to fullscreen — ideal for setting the scene
- Swipe through images within a category

### 8. MECHANICS QUICK REFERENCE
- System-specific reference panel (pulls from asset library)
- Skill list, difficulty levels, sanity table, combat sequence
- Searchable / filterable
- Inline during NPC cards (stat block uses same reference)

### 9. SESSION TIMER
- Prominent countdown per act
- Soft alert at halfway through each act
- Amber alert at 10 minutes remaining in act
- Red alert at act end — pacing note auto-surfaces
- Option to pause (comfort break)
- Overall session timer running throughout

### 10. GM NOTES PAD
- Freeform scratchpad — sticky note style
- Notes persist per act
- Quick save to scenario file

### 11. PLAYER CHARACTER TRACKER
- One card per player character
- HP / MP / Sanity (system appropriate) tracked with +/- buttons
- Status tags: Injured | Insane | Dead | Unconscious

---

## Screen Layout (Tablet Portrait — Primary View)

```
┌─────────────────────────────────┐
│  [Scenario Title]    [⏱ 1:23]  │  ← Header: title + timer
│  ████████░░░░░░░░  Act 2 / 90m  │  ← Progress bar
├─────────────────────────────────┤
│                                 │
│     MAIN CONTENT PANEL          │  ← Current act / selected card
│     (Act summary / NPC /        │
│      Location / Clue etc.)      │
│                                 │
│                                 │
├─────────────────────────────────┤
│ [📍Loc] [👤NPC] [🔍Clue] [📄HO] │  ← Bottom nav row (thumb reach)
│ [🎨Art] [⚡Hook] [📋Notes] [⚙️] │  ← Second nav row
└─────────────────────────────────┘
```

---

## Technical Approach
- Single HTML file per scenario (HTML + CSS + JS, no dependencies)
- All artwork embedded as base64 or referenced from local folder
- Works fully offline
- Responsive: 768px+ (tablet portrait) primary, 1024px+ (landscape laptop) secondary
- Local storage for session state (HP tracking, clues found, timer)
- Print stylesheet included for paper fallback

---

## File Structure Per Scenario App

```
app/
└── event-[##]-[title]/
    ├── index.html          ← The GM app (self-contained)
    ├── assets/
    │   ├── art-01.png
    │   ├── art-02.png
    │   └── ...
    └── handouts/
        ├── H00-A.png
        ├── H01-A.png
        └── ...
```

---

## Build Order (per scenario)
1. Complete scenario document (markdown)
2. Generate artwork assets
3. Build HTML app from this template
4. Test on tablet / touchscreen
5. Push complete app to GitHub

