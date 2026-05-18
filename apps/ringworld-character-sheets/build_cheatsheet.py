"""
Ringworld RPG — Double-Sided GM/Player Cheat Sheet
ChaosiumCon UK 2026 — Events 95 & 96
Built with reportlab.
"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color, white, black
import math

PW, PH = A4   # 595 × 841 pt
PAD = 6*mm

pdfmetrics.registerFont(TTFont('Orb',  '/tmp/font-orbitron-700.ttf'))
pdfmetrics.registerFont(TTFont('OrbB', '/tmp/font-orbitron-900.ttf'))
pdfmetrics.registerFont(TTFont('Mono', '/tmp/font-sharetechmono.ttf'))
pdfmetrics.registerFont(TTFont('Bar',  '/tmp/font-barlow-700.ttf'))
pdfmetrics.registerFont(TTFont('BarB', '/tmp/font-barlow-900.ttf'))

GOLD   = HexColor('#ffaa00')   # cheat sheet accent — gold
GOLDD  = HexColor('#9a6600')
INK    = HexColor('#06060e')
LIGHT  = HexColor('#f2f2f0')
MID    = HexColor('#aaaacc')
DARK   = HexColor('#0e0e1e')
DARK2  = HexColor('#14141e')
STRIPE = HexColor('#1a1a2a')
RED    = HexColor('#cc2200')

# ── helpers ───────────────────────────────────────────────────────────────────
def fr(c, x, y, w, h, fill):
    c.saveState(); c.setFillColor(fill)
    c.rect(x, y, w, h, fill=1, stroke=0); c.restoreState()
def or_(c, x, y, w, h, col, lw=1):
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(lw); c.setFillColor(Color(0,0,0,0))
    c.rect(x, y, w, h, fill=0, stroke=1); c.restoreState()
def hl(c, x1, x2, y, col, lw=0.5):
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(lw)
    c.line(x1, y, x2, y); c.restoreState()
def vl(c, x, y1, y2, col, lw=0.5):
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(lw)
    c.line(x, y1, x, y2); c.restoreState()
def tx(c, t, x, y, font, size, col, align='left'):
    c.saveState(); c.setFont(font, size); c.setFillColor(col)
    if align == 'left':   c.drawString(x, y, t)
    elif align == 'right': c.drawRightString(x, y, t)
    elif align == 'centre':c.drawCentredString(x, y, t)
    c.restoreState()

def bar(c, x, y, w, h, label, acc=GOLD, font_size=7):
    fr(c, x, y, w, h, acc)
    tx(c, label, x+4, y+h*0.3, 'OrbB', font_size, INK)

def section(c, x, y, w, label, acc=GOLD):
    """Draw a section header bar and return the y just below it."""
    h = 11
    fr(c, x, y-h, w, h, acc)
    tx(c, label, x+4, y-h+3, 'OrbB', 7.5, INK)
    return y - h - 2   # content starts here

def row_bg(c, x, y, w, h, i):
    fr(c, x, y, w, h, STRIPE if i%2 else DARK2)

# ── FRONT PAGE ────────────────────────────────────────────────────────────────
def draw_front(c):
    # ── MASTHEAD ─────────────────────────────────────────────────────────────
    mh = 14*mm
    fr(c, 0, PH-mh, PW, mh, INK)
    fr(c, 0, PH-1.5*mm, PW, 1.5*mm, GOLD)
    tx(c, 'RINGWORLD', PAD, PH-10*mm, 'OrbB', 18, GOLD)
    tx(c, 'REFERENCE SHEET', PAD+73*mm, PH-10*mm, 'Orb', 11, white)
    tx(c, '1984 CHAOSIUM  ·  KNOWN SPACE  ·  2851 A.D.', PW-PAD, PH-9*mm, 'Mono', 6.5, MID, 'right')
    tx(c, 'GAME MASTER & PLAYER REFERENCE', PW-PAD, PH-5*mm, 'Orb', 6, HexColor('#666644'), 'right')
    tx(c, 'FRONT', PAD, PH-5*mm, 'Mono', 5.5, HexColor('#555533'))

    # ── Layout: 3 columns ─────────────────────────────────────────────────────
    top    = PH - mh - 2
    bottom = 8*mm
    total  = top - bottom
    cw     = (PW - 2*PAD - 2*3) / 3
    col_x  = [PAD, PAD+cw+3, PAD+2*(cw+3)]
    c1, c2, c3 = col_x

    # ─────────────────────────── COLUMN 1 ────────────────────────────────────
    y = top

    # ── CORE MECHANIC ────────────────────────────────────────────────────────
    y = section(c, c1, y, cw, 'THE CORE MECHANIC')
    fr(c, c1, y-32*mm, cw, 32*mm, DARK)
    ty = y - 4*mm
    tx(c, 'Roll D100  ≤  Skill %  =  SUCCESS', c1+3, ty, 'Mono', 7.5, GOLD)
    ty -= 8
    tx(c, 'Roll D100  >  Skill %  =  FAILURE', c1+3, ty, 'Mono', 7.5, MID)
    ty -= 10
    hl(c, c1+2, c1+cw-2, ty, GOLD, 0.6)
    ty -= 7
    tx(c, 'SPECIAL SUCCESS', c1+3, ty, 'OrbB', 6.5, GOLD)
    tx(c, '≤ Skill ÷ 5  (round down)', c1+cw-2, ty, 'Mono', 6.5, white, 'right')
    ty -= 8
    tx(c, 'SPECIAL FAILURE', c1+3, ty, 'OrbB', 6.5, RED)
    tx(c, 'Top 1/20th of failure range', c1+cw-2, ty, 'Mono', 6.5, MID, 'right')
    ty -= 8
    tx(c, '00 always fumbles regardless of skill', c1+3, ty, 'Mono', 6, MID)
    ty -= 9
    hl(c, c1+2, c1+cw-2, ty, GOLD, 0.6)
    ty -= 7
    tx(c, 'OPPOSED ROLLS', c1+3, ty, 'OrbB', 6.5, GOLD)
    tx(c, '50% + (active×5) − (passive×5)', c1+cw-2, ty, 'Mono', 6, white, 'right')
    y -= 32*mm

    # ── ACTION RANKING ───────────────────────────────────────────────────────
    y -= 2
    y = section(c, c1, y, cw, 'ACTION RANKING & MOVEMENT')
    fr(c, c1, y-57*mm, cw, 57*mm, DARK)
    ty = y - 4*mm

    # headers
    for lbl, lx in [('DEX', c1+3), ('ACTION RANK', c1+22*mm), ('MOVE', c1+cw-18*mm)]:
        tx(c, lbl, lx, ty, 'OrbB', 6, GOLD)
    ty -= 3; hl(c, c1+2, c1+cw-2, ty, GOLD, 0.7)

    ar_data = [
        ('1–4',  '7 impulses', '3m/imp'),
        ('5–8',  '6 impulses', '3m/imp'),
        ('9–12', '5 impulses', '3m/imp'),
        ('13–16','4 impulses', '3m/imp'),
        ('17–20','3 impulses', '3m/imp'),
        ('21–24','2 impulses', '3m/imp'),
        ('25+',  '1 impulse',  '3m/imp'),
    ]
    for i, (dex, ar, mv) in enumerate(ar_data):
        ty -= 6.5
        row_bg(c, c1, ty-2, cw, 7, i)
        tx(c, dex, c1+3, ty, 'Mono', 7, white)
        tx(c, ar,  c1+22*mm, ty, 'Bar', 8, GOLD)
        tx(c, mv,  c1+cw-2, ty, 'Mono', 6, MID, 'right')

    ty -= 10; hl(c, c1+2, c1+cw-2, ty, GOLD, 0.5)
    ty -= 7
    tx(c, 'MAJOR ACTION: draw/put away weapon, aim, melee attack,', c1+3, ty, 'Mono', 5.8, MID)
    ty -= 7.5
    tx(c, '  use perception skill, unarmed combat, stand from prone', c1+3, ty, 'Mono', 5.8, MID)
    ty -= 7.5
    tx(c, 'MINOR ACTION: fire ranged weapon, fall, rise from kneeling', c1+3, ty, 'Mono', 5.8, MID)
    ty -= 7.5
    tx(c, 'SPRINT: up to 6m/impulse (fatigues in CON impulses)', c1+3, ty, 'Mono', 5.8, HexColor('#998855'))
    y -= 57*mm

    # ── DAMAGE MODIFIER ──────────────────────────────────────────────────────
    y -= 2
    y = section(c, c1, y, cw, 'DAMAGE MODIFIER  (STR + MAS)')
    fr(c, c1, y-52*mm, cw, 52*mm, DARK)
    ty = y - 4*mm

    for lbl, lx in [('STR+MAS', c1+3), ('MODIFIER', c1+cw-22*mm)]:
        tx(c, lbl, lx, ty, 'OrbB', 6, GOLD)
    ty -= 3; hl(c, c1+2, c1+cw-2, ty, GOLD, 0.7)

    dm_data = [
        ('02–08', '−1D6', RED),
        ('09–16', '−1D3', HexColor('#cc6600')),
        ('17–24', 'None', MID),
        ('25–32', '+1D3', HexColor('#88cc00')),
        ('33–40', '+1D6', HexColor('#44cc44')),
        ('41–50', '+2D6', GOLD),
        ('51–60', '+3D6', GOLD),
        ('61–70', '+4D6', GOLD),
        ('71+',   '+1D6 per 10 pts', HexColor('#ffdd88')),
    ]
    for i, (rng, mod, col) in enumerate(dm_data):
        ty -= 6.5
        row_bg(c, c1, ty-2, cw, 7, i)
        tx(c, rng, c1+3, ty, 'Mono', 7, white)
        tx(c, mod, c1+cw-2, ty, 'OrbB', 7.5, col, 'right')
    ty -= 9
    tx(c, 'Melee/unarmed only. Missile weapons do not use this.', c1+3, ty, 'Mono', 5.8, MID)
    y -= 52*mm

    # ── HIT POINTS & WOUNDS ─────────────────────────────────────────────────
    y -= 2
    y = section(c, c1, y, cw, 'HIT POINTS & WOUNDS')
    fr(c, c1, y-38*mm, cw, 38*mm, DARK)
    ty = y - 4*mm

    tx(c, 'GENERAL HP', c1+3, ty, 'OrbB', 6.5, GOLD)
    tx(c, '= CON + MAS', c1+cw-2, ty, 'Mono', 7, white, 'right')
    ty -= 8
    hl(c, c1+2, c1+cw-2, ty, GOLD, 0.5)
    ty -= 7

    wp_data = [
        ('UNCONSCIOUS', '≤ ¼ HP (round up)', HexColor('#cc8800')),
        ('DYING',       'HP = 0 or below',   RED),
        ('DEAD',        'HP = −CON',          HexColor('#880000')),
    ]
    for label, cond, col in wp_data:
        row_bg(c, c1, ty-2, cw, 8, 0)
        tx(c, label, c1+3, ty, 'OrbB', 7, col)
        tx(c, cond, c1+cw-2, ty, 'Mono', 7, white, 'right')
        ty -= 9

    ty -= 4; hl(c, c1+2, c1+cw-2, ty, GOLD, 0.5); ty -= 7
    tx(c, 'Dying: receive treatment in CON impulses or die', c1+3, ty, 'Mono', 5.8, MID)
    ty -= 7
    tx(c, 'Location HP lost? Roll on wound table (GM book)', c1+3, ty, 'Mono', 5.8, MID)
    ty -= 7
    tx(c, 'Loc damage does NOT reduce general HP directly', c1+3, ty, 'Mono', 5.8, MID)
    y -= 38*mm

    # ── DERIVED ATTRIBUTES ───────────────────────────────────────────────────
    y -= 2
    remaining = y - bottom - 2
    y = section(c, c1, y, cw, 'DERIVED ATTRIBUTES')
    fr(c, c1, y-remaining, cw, remaining, DARK)
    ty = y - 4*mm

    derived = [
        ('General HP',  'CON + MAS'),
        ('Health Roll', 'CON × 3%'),
        ('Reasoning',   'INT × 3%'),
        ('Luck Roll',   'POW × 3%'),
        ('Dodge Roll',  'DEX × 3%'),
        ('Power Points','= POW'),
        ('Action Rank', 'See table above'),
        ('Damage Bonus','See STR+MAS table'),
    ]
    for i, (attr, form) in enumerate(derived):
        row_bg(c, c1, ty-2, cw, 8, i)
        tx(c, attr, c1+3, ty, 'Bar', 8.5, white)
        tx(c, form, c1+cw-2, ty, 'Mono', 6.8, GOLD, 'right')
        ty -= 9

    # ─────────────────────────── COLUMN 2 ────────────────────────────────────
    y = top

    # ── SKILL ROLLS ──────────────────────────────────────────────────────────
    y = section(c, c2, y, cw, 'SKILL CATEGORIES & ROOT MAXIMA')
    fr(c, c2, y-42*mm, cw, 42*mm, DARK)
    ty = y - 4*mm

    cats = [
        ('AGILITY',      'Root Max = STR + DEX', [
            'Archaic Melee Weapon (05%)',
            'Archaic Ranged Weapons (03%)',
            'Athletics (15%)',
            'Hide (10%) / Sneak (05%)',
            'Unarmed Combat (00%)',
            'V. Sword / F. Laser (15%)',
        ]),
        ('COMMUNICATION','Root Max = INT + APP', [
            'Bargain (10%) / Debate (05%)',
            'Fast Talk (10%) / Orate (05%)',
            'Own Language (INT×5)',
            'Psychology (00%) / Perform (05%)',
        ]),
    ]
    for cat_name, root, skills in cats:
        fr(c, c2, ty-8, cw, 8, GOLD)
        tx(c, cat_name, c2+3, ty-5.5, 'OrbB', 6.5, INK)
        tx(c, root, c2+cw-2, ty-5.5, 'Mono', 5.5, INK, 'right')
        ty -= 9
        for sk in skills:
            tx(c, '▸ ' + sk, c2+3, ty, 'Bar', 7.5, white)
            ty -= 7.5
        ty -= 2
    y -= 42*mm

    # ── KNOWLEDGE ─────────────────────────────────────────────────────────────
    y -= 2
    y = section(c, c2, y, cw, 'KNOWLEDGE  (Root Max = INT + EDU)')
    fr(c, c2, y-42*mm, cw, 42*mm, DARK)
    ty = y - 4*mm
    know_skills = [
        'Anthropology (00%)','Astronomy (00%)','Biology (00%)',
        'Botany (00%)','Chemistry (00%)','Computers (00%)',
        'Emergency Treatment (01%)','Engineering (00%)',
        'Farming (00%)','History (05%)','Law (00%)',
        'Mathematics (00%)','Physics (00%)','Planetology (00%)',
        'Second Languages (00%)','Strategy (00%)',
        'Theology (00%)','Zoology (00%)',
    ]
    half = len(know_skills)//2 + len(know_skills)%2
    col_a = know_skills[:half]; col_b = know_skills[half:]
    cx_a = c2+2; cx_b = c2+cw/2+2
    sty = ty
    for sk in col_a:
        tx(c, '▸ ' + sk, cx_a, sty, 'Bar', 6.8, white); sty -= 6.5
    sty2 = ty
    for sk in col_b:
        tx(c, '▸ ' + sk, cx_b, sty2, 'Bar', 6.8, white); sty2 -= 6.5
    y -= 42*mm

    # ── PERCEPTION ────────────────────────────────────────────────────────────
    y -= 2
    y = section(c, c2, y, cw, 'PERCEPTION  (Root Max = POW + CON)')
    fr(c, c2, y-23*mm, cw, 23*mm, DARK)
    ty = y - 4*mm
    perc = [
        'Handgun Energy (05%)','Handgun Projectile (03%)',
        'Heavy Weapon Energy (05%)','Heavy Weapon Proj. (03%)',
        'Listen (05%)','Observe (05%)','Scent (00%)','Search (05%)','Track (05%)',
    ]
    for i, sk in enumerate(perc):
        col_sk = c2+2 if i < 5 else c2+cw/2+2
        ys_k = ty - (i%5)*6.5
        tx(c, '▸ ' + sk, col_sk, ys_k, 'Bar', 6.8, white)
    y -= 23*mm

    # ── TECHNICAL ─────────────────────────────────────────────────────────────
    y -= 2
    y = section(c, c2, y, cw, 'TECHNICAL  (Root Max = DEX + INT)')
    fr(c, c2, y-27*mm, cw, 27*mm, DARK)
    ty = y - 4*mm
    tech = [
        'Aquatic Vehicle (00%)','Atmospheric Craft (00%)',
        'Ground Vehicle (00%)','Hyperdrive (00%)',
        'Personal Flyer (15%)','Reaction Drive (00%)',
        'Reactionless Drive (00%)','Repair (00%)',
        'Ringworld (00%)','Weapons System (00%)',
    ]
    for i, sk in enumerate(tech):
        col_sk = c2+2 if i < 5 else c2+cw/2+2
        ys_k = ty - (i%5)*6.5
        tx(c, '▸ ' + sk, col_sk, ys_k, 'Bar', 6.8, white)
    y -= 27*mm

    # ── INCREASING SKILLS ─────────────────────────────────────────────────────
    y -= 2
    y = section(c, c2, y, cw, 'INCREASING SKILLS')
    fr(c, c2, y-24*mm, cw, 24*mm, DARK)
    ty = y - 4*mm
    inc = [
        'Experience: GM awards at session end',
        'Training: hours = current skill value',
        'Teacher: halves training time',
        'Simweb: halves training time (not STR/CON)',
        'Research: INT×3% weekly, adds D6 per success',
        'Skills can exceed 100% — scale effects up',
    ]
    for s in inc:
        tx(c, '▸ ' + s, c2+3, ty, 'Mono', 6, MID); ty -= 7
    y -= 24*mm

    # ── RINGWORLD SPECIFICS ───────────────────────────────────────────────────
    y -= 2
    remaining2 = y - bottom - 2
    y = section(c, c2, y, cw, 'RINGWORLD  SPECIFICS')
    fr(c, c2, y-remaining2, cw, remaining2, DARK)
    ty = y - 4*mm
    rw = [
        ('Ringworld Radius', '~153,000,000 km'),
        ('Day length',       '30 UNS hours'),
        ('Daylight',         '21 of 30 hours'),
        ('Twilight',         '45 min each end'),
        ('Surface area',     '~3 million Earths'),
        ('Scrith (floor)',   'Invulnerable material'),
        ('Spin gravity',     '0.992g at inner surface'),
        ('Rim walls',        '1,600 km high'),
        ('Grid',             'Superconductor power net'),
        ('Stepping discs',   'Teleport; locked to grid'),
    ]
    for i, (attr, val) in enumerate(rw):
        row_bg(c, c2, ty-2, cw, 8, i)
        tx(c, attr, c2+3, ty, 'Bar', 8, white)
        tx(c, val, c2+cw-2, ty, 'Mono', 6.5, GOLD, 'right')
        ty -= 9

    # ─────────────────────────── COLUMN 3 ────────────────────────────────────
    y = top

    # ── HIT LOCATION ────────────────────────────────────────────────────────
    y = section(c, c3, y, cw, 'HIT LOCATIONS (D20)')
    fr(c, c3, y-52*mm, cw, 52*mm, DARK)
    ty = y - 4*mm

    # headers
    for lbl, lx in [('LOCATION', c3+2), ('MELEE', c3+30*mm), ('RANGED', c3+cw-16*mm)]:
        tx(c, lbl, lx, ty, 'OrbB', 6, GOLD)
    ty -= 3; hl(c, c3+2, c3+cw-2, ty, GOLD, 0.7)

    locs = [
        ('Right Leg',  '01–04', '01–03'),
        ('Left Leg',   '05–08', '04–06'),
        ('Abdomen',    '09–11', '07–10'),
        ('Chest',      '12',    '11–15'),
        ('Right Arm',  '13–15', '16–17'),
        ('Left Arm',   '16–18', '18–19'),
        ('Head',       '19–20', '20'),
    ]
    for i, (loc, mel, rng) in enumerate(locs):
        ty -= 7
        row_bg(c, c3, ty-2, cw, 7.5, i)
        tx(c, loc, c3+3, ty, 'Bar', 8.5, white)
        tx(c, mel, c3+31*mm, ty, 'Mono', 6.8, MID, 'centre')
        tx(c, rng, c3+cw-12*mm, ty, 'Mono', 6.8, MID, 'centre')
    ty -= 9
    tx(c, 'Melee: head=19-20  vs  Ranged: head=20 only', c3+3, ty, 'Mono', 5.5, HexColor('#887755'))
    y -= 52*mm

    # ── LOCATION HP TABLE ───────────────────────────────────────────────────
    y -= 2
    y = section(c, c3, y, cw, 'HIT POINTS PER LOCATION')
    fr(c, c3, y-36*mm, cw, 36*mm, DARK)
    ty = y - 4*mm
    tx(c, 'General HP', c3+3, ty, 'OrbB', 6, GOLD)
    tx(c, 'Arm / Leg', c3+28*mm, ty, 'OrbB', 6, GOLD, 'centre')
    tx(c, 'Chest', c3+cw-2, ty, 'OrbB', 6, GOLD, 'right')
    ty -= 3; hl(c, c3+2, c3+cw-2, ty, GOLD, 0.7)

    hp_table = [
        (11, '3', '4'),  (12, '3', '4'),  (13, '4', '5'),
        (14, '4', '5'),  (15, '4', '5'),  (16, '4', '6'),
        (17, '5', '6'),  (18, '5', '6'),  (19, '5', '7'),
        (20, '5', '7'),
    ]
    for i, (ghp, arm, chest) in enumerate(hp_table):
        ty -= 6
        row_bg(c, c3, ty-2, cw, 7, i)
        tx(c, f'HP {ghp}', c3+3, ty, 'Mono', 6.5, white)
        tx(c, arm, c3+28*mm, ty, 'OrbB', 7, GOLD, 'centre')
        tx(c, chest, c3+cw-2, ty, 'OrbB', 7, GOLD, 'right')
    y -= 36*mm

    # ── RESISTANCE TABLE ────────────────────────────────────────────────────
    y -= 2
    y = section(c, c3, y, cw, 'RESISTANCE TABLE  (50 + act×5 − pas×5)')
    fr(c, c3, y-50*mm, cw, 50*mm, DARK)
    ty = y - 5*mm

    # Mini resistance table — active 1-15 vs passive 1-10
    actives  = list(range(1, 16))
    passives = list(range(1, 11))
    cell_w = (cw - 14*mm) / len(actives)
    cell_h = 5.5

    tx(c, 'P\\A', c3+2, ty, 'Mono', 4.5, GOLD)
    for ai, av in enumerate(actives):
        tx(c, str(av), c3+14*mm+ai*cell_w+cell_w/2, ty, 'Mono', 4.5, MID, 'centre')
    ty -= 5

    for pi, pv in enumerate(passives):
        row_bg(c, c3, ty-3, cw, cell_h, pi)
        tx(c, str(pv), c3+2, ty, 'Mono', 5, MID)
        for ai, av in enumerate(actives):
            pct = max(5, min(95, 50 + (av-pv)*5))
            if pct >= 75: col = GOLD
            elif pct >= 50: col = white
            elif pct >= 25: col = MID
            else: col = RED
            tx(c, str(pct), c3+14*mm+ai*cell_w+cell_w/2, ty, 'Mono', 4.5, col, 'centre')
        ty -= cell_h

    ty -= 6
    tx(c, 'Roll ≤ result = active factor succeeds', c3+3, ty, 'Mono', 5.8, MID)
    y -= 50*mm

    # ── KNOWN SPACE SPECIES ─────────────────────────────────────────────────
    y -= 2
    remaining3 = y - bottom - 2
    y = section(c, c3, y, cw, 'KNOWN SPACE SPECIES')
    fr(c, c3, y-remaining3, cw, remaining3, DARK)
    ty = y - 4*mm

    species = [
        ('Human (Earth/average)',  'STR/CON/SIZ/INT: 2D6+6  ·  APP: 2D6+6'),
        ('Human (Jinx, heavy-g)',  'STR/CON/SIZ: 2D6+9, short & dense'),
        ('Human (We Made It)',     'STR/CON: 2D6+6, tall & willowy, mobile ears'),
        ("Kzin",                   'STR/SIZ: 2D6+12. Move 5m/imp, sprint 10m'),
        ("Pierson's Puppeteer",    'STR: 2D6+3. Two heads. 3-legged. Non-violent'),
        ('Pak Protector',          'Rare. Ancient. STR 30+. Cannot be reasoned with'),
    ]
    for i, (sp, detail) in enumerate(species):
        row_bg(c, c3, ty-12, cw, 13, i)
        tx(c, sp, c3+3, ty, 'OrbB', 6.5, GOLD)
        ty -= 7.5
        tx(c, detail, c3+3, ty, 'Mono', 5.5, MID)
        ty -= 8

    # ── FOOTER ───────────────────────────────────────────────────────────────
    fr(c, 0, 0, PW, 8*mm, INK)
    hl(c, 0, PW, 8*mm, GOLD, 1)
    tx(c, 'RINGWORLD RPG  ·  CHAOSIUM 1984  ·  PRINT DOUBLE-SIDED', PAD, 2.5*mm, 'Mono', 6, GOLD)
    tx(c, 'ChaosiumCon UK 2026  ·  Events 95 & 96', PW-PAD, 2.5*mm, 'Mono', 6, MID, 'right')


# ── BACK PAGE ─────────────────────────────────────────────────────────────────
def draw_back(c):
    # ── MASTHEAD ─────────────────────────────────────────────────────────────
    mh = 14*mm
    fr(c, 0, PH-mh, PW, mh, INK)
    fr(c, 0, PH-1.5*mm, PW, 1.5*mm, GOLD)
    tx(c, 'RINGWORLD', PAD, PH-10*mm, 'OrbB', 18, GOLD)
    tx(c, 'COMBAT & WEAPONS REFERENCE', PAD+73*mm, PH-10*mm, 'Orb', 9.5, white)
    tx(c, '1984 CHAOSIUM  ·  KNOWN SPACE  ·  2851 A.D.', PW-PAD, PH-9*mm, 'Mono', 6.5, MID, 'right')
    tx(c, 'BACK', PAD, PH-5*mm, 'Mono', 5.5, HexColor('#555533'))

    top    = PH - mh - 2
    bottom = 8*mm
    cw     = (PW - 2*PAD - 2*3) / 3
    col_x  = [PAD, PAD+cw+3, PAD+2*(cw+3)]
    c1, c2, c3 = col_x

    # ─────────────────────────── COLUMN 1 ────────────────────────────────────
    y = top

    # ── COMBAT SEQUENCE ─────────────────────────────────────────────────────
    y = section(c, c1, y, cw, 'COMBAT SEQUENCE')
    fr(c, c1, y-52*mm, cw, 52*mm, DARK)
    ty = y - 4*mm
    steps = [
        ('1', 'STATE INTENT', 'Declare target & weapon on impulse 1 of AR'),
        ('2', 'MOVE',         '3m per impulse; sprint 6m (CON impulse limit)'),
        ('3', 'AIM',          'Full AR to aim; half AR for ½ skill; no aim = ¼ skill'),
        ('4', 'ROLL',         'D100 ≤ skill% = hit; roll on hit location table'),
        ('5', 'DAMAGE',       'Roll damage; apply armour; subtract from location HP'),
        ('6', 'WOUND',        'Check location wound table; check general HP level'),
        ('7', 'DODGE',        'DEX×3% vs incoming melee; costs 1 impulse; roll D100'),
        ('8', 'PARRY',        'Roll weapon skill; excess damage hits weapon'),
    ]
    for i, (n, hdr, detail) in enumerate(steps):
        row_bg(c, c1, ty-12, cw, 13, i)
        fr(c, c1, ty-12, 7*mm, 13, GOLD)
        tx(c, n, c1+3.5*mm, ty-5.5, 'OrbB', 7.5, INK, 'centre')
        tx(c, hdr, c1+8*mm, ty-2, 'OrbB', 6.5, GOLD)
        tx(c, detail, c1+8*mm, ty-9, 'Mono', 5.8, MID)
        ty -= 14
    y -= 52*mm

    # ── RANGE MODIFIERS ─────────────────────────────────────────────────────
    y -= 2
    y = section(c, c1, y, cw, 'RANGE MODIFIERS')
    fr(c, c1, y-38*mm, cw, 38*mm, DARK)
    ty = y - 4*mm

    range_data = [
        ('Point-Blank', '≤ DEX in metres', '×1.5 skill (still target = auto-hit)'),
        ('Short',       'Weapon short range', 'Normal skill %'),
        ('Medium',      'Weapon medium range','½ normal skill %'),
        ('Long',        'Weapon long range',  '¼ normal skill %'),
        ('Snap (no aim)','Any range',         '¼ normal skill %'),
        ('Half AR aim', 'Any range',          '½ normal skill %'),
    ]
    for lbl, lx in [('RANGE',c1+2),('DISTANCE',c1+20*mm),('MODIFIER',c1+cw-2)]:
        tx(c, lbl, lx, ty, 'OrbB', 6, GOLD, 'left' if lx!=c1+cw-2 else 'right')
    ty -= 3; hl(c, c1+2, c1+cw-2, ty, GOLD, 0.7)
    for i, (rng, dist, mod) in enumerate(range_data):
        ty -= 8
        row_bg(c, c1, ty-2, cw, 8.5, i)
        tx(c, rng, c1+3, ty, 'Bar', 8.5, GOLD)
        tx(c, dist, c1+21*mm, ty, 'Mono', 5.5, MID)
        tx(c, mod, c1+cw-2, ty, 'Mono', 6, white, 'right')
    ty -= 9
    tx(c, 'Moving target angling: ½ skill. Head-on/retreating: normal.', c1+3, ty, 'Mono', 5.5, HexColor('#887755'))
    y -= 38*mm

    # ── KNOWN SPACE WEAPONS ─────────────────────────────────────────────────
    y -= 2
    y = section(c, c1, y, cw, 'KNOWN SPACE WEAPONS')
    fr(c, c1, y-70*mm, cw, 70*mm, DARK)
    ty = y - 4*mm

    for lbl, lx in [('WEAPON',c1+2),('SKILL CAT',c1+29*mm),('DMG',c1+46*mm),('RANGE (S/M/L)',c1+cw-2)]:
        tx(c, lbl, lx, ty, 'OrbB', 5.5, GOLD, 'left' if lx!=c1+cw-2 else 'right')
    ty -= 3; hl(c, c1+2, c1+cw-2, ty, GOLD, 0.7)

    weapons = [
        ('Variable Sword',     'Agility', '1D6+4+DB', 'touch–5m'),
        ('Flashlight-Laser',   'Agility', '2D6+2',   '25/100/500m'),
        ('Hand Beamer',        'HG-Energy','1D4+6',  '15/60/200m'),
        ('Laser Pistol',       'HG-Energy','1D6+6',  '20/80/300m'),
        ('Kzin Beam Pistol',   'HG-Energy','1D6+8',  '20/80/300m'),
        ('Sonic Stunner',      'HG-Energy','Stun',    '5/20/50m'),
        ('E-M Stunner',        'HG-Energy','Stun',    '20/60/150m'),
        ('ARM Needle Gun',     'HG-Proj.', '1D3+*',  '10/40/100m'),
        ('Tangler',            'HG-Proj.', 'Immob.',  '5/15/40m'),
        ('Laser Rifle',        'HW-Energy','1D10+15', '50/200/1km'),
        ('Gravity Planer',     'HW-Energy','3D6',     '5/20m cone'),
        ('Kzin Claws ×2',      'Unarmed',  'STR+1D6+DB','touch'),
        ('Archaic Sword',      'Arch.Mel.','1D8+DB',  'touch'),
    ]
    for i, (wpn, cat, dmg, rng) in enumerate(weapons):
        ty -= 7
        row_bg(c, c1, ty-2, cw, 7.5, i)
        tx(c, wpn, c1+3, ty, 'Bar', 7.5, white)
        tx(c, cat, c1+29*mm, ty, 'Mono', 5.5, MID)
        tx(c, dmg, c1+46*mm, ty, 'OrbB', 6.5, GOLD)
        tx(c, rng, c1+cw-2, ty, 'Mono', 5.5, MID, 'right')
    ty -= 8
    tx(c, '* ARM needle gun: paralytic/sedative payload, silent', c1+3, ty, 'Mono', 5.2, HexColor('#887755'))
    y -= 70*mm

    # ── WOUND EFFECTS BY LOCATION ───────────────────────────────────────────
    y -= 2
    remaining1 = y - bottom - 2
    y = section(c, c1, y, cw, 'WOUND EFFECTS BY LOCATION')
    fr(c, c1, y-remaining1, cw, remaining1, DARK)
    ty = y - 4*mm

    wound_locs = [
        ('Right/Left LEG', 'At 0 HP: collapses, must crawl'),
        ('ABDOMEN',        'At 0 HP: collapses; no further actions'),
        ('CHEST',          'At 0 HP: falls unconscious immediately'),
        ('RIGHT ARM',      'At 0 HP: arm useless; -20% all actions'),
        ('LEFT ARM',       'At 0 HP: arm useless; -20% all actions'),
        ('HEAD',           'At 0 HP: unconscious; roll CON×1 or die'),
    ]
    for i, (loc, effect) in enumerate(wound_locs):
        row_bg(c, c1, ty-12, cw, 13, i)
        tx(c, loc, c1+3, ty-2, 'OrbB', 6, GOLD)
        tx(c, effect, c1+3, ty-9, 'Mono', 5.5, MID)
        ty -= 14

    # ─────────────────────────── COLUMN 2 ────────────────────────────────────
    y = top

    # ── TECHNOLOGY REFERENCE ────────────────────────────────────────────────
    y = section(c, c2, y, cw, 'TECHNOLOGY  —  KNOWN SPACE')
    fr(c, c2, y-38*mm, cw, 38*mm, DARK)
    ty = y - 4*mm

    tech_items = [
        ('Flashlight-Laser',   '3 settings: torch / stun / cut-weld / beam'),
        ('Sonic Stunner',      'MAS-based stun; adjustable to target MAS'),
        ('Stepping Disc',      'Teleport; locked to Ringworld grid; instant'),
        ('Personal Flyer',     'Flash crowd transport; max ~300kph'),
        ('Tangler',            'Web immobilises; dissolves in hours'),
        ('ARM Needle Gun',     'Paralytic/sedative dart; silent; no recoil'),
        ('Gravity Planer',     'Engineering tool; cone; ignores armour'),
        ('Variable Sword',     'Monomolecular blade on wire; cuts scrith'),
        ('Diffusion Field',    'Quarters energy weapon damage (personal)'),
        ('Sonic Fold',         'Silence barrier; stops stunner beams'),
    ]
    for i, (item, desc) in enumerate(tech_items):
        row_bg(c, c2, ty-10, cw, 11, i)
        tx(c, item, c2+3, ty, 'OrbB', 6, GOLD)
        ty -= 6.5
        tx(c, desc, c2+3, ty, 'Mono', 5.5, MID)
        ty -= 5
    y -= 38*mm

    # ── CITY BUILDER / RINGWORLD TECHNOLOGY ─────────────────────────────────
    y -= 2
    y = section(c, c2, y, cw, 'RINGWORLD  TECHNOLOGY')
    fr(c, c2, y-26*mm, cw, 26*mm, DARK)
    ty = y - 4*mm

    rw_tech = [
        ('Scrith',         'Invulnerable. Cannot be cut, burned, or moved'),
        ('Superconductor', 'Grid powers everything; stepping discs need it'),
        ('Floater Car',    'Repulsor-driven; max 100m altitude; 6000kph'),
        ('Grid Tram',      'Superconductor rail; up to 20,000kph'),
        ('Sunflower Field','Energy collector; lethal if entered at night'),
        ('Spill Mountain', 'Impact crater; inverted; ~20km high'),
    ]
    for i, (item, desc) in enumerate(rw_tech):
        row_bg(c, c2, ty-10, cw, 11, i)
        tx(c, item, c2+3, ty, 'OrbB', 6, HexColor('#ffcc55'))
        ty -= 6.5
        tx(c, desc, c2+3, ty, 'Mono', 5.5, MID)
        ty -= 5
    y -= 26*mm

    # ── PSIONICS QUICK REFERENCE ────────────────────────────────────────────
    y -= 2
    y = section(c, c2, y, cw, 'PSIONICS  (POW-based)')
    fr(c, c2, y-26*mm, cw, 26*mm, DARK)
    ty = y - 4*mm
    tx(c, 'Psionic abilities checked via POW×3% (Luck Roll)', c2+3, ty, 'Mono', 6, MID)
    ty -= 8
    tx(c, 'Using psionically-operated devices requires no ability', c2+3, ty, 'Mono', 6, MID)
    ty -= 9; hl(c, c2+2, c2+cw-2, ty, GOLD, 0.5); ty -= 6
    psi_types = [
        'Telekinesis  ·  Telepathy  ·  Teleportation',
        'Healing  ·  Precognition  ·  Emotion Control',
    ]
    for p in psi_types:
        tx(c, p, c2+cw/2, ty, 'Bar', 8.5, GOLD, 'centre'); ty -= 8
    ty -= 4
    tx(c, 'Roll POW×3% to activate; GM determines range/effect', c2+3, ty, 'Mono', 6, MID)
    y -= 26*mm

    # ── KNOWN SPACE FACTBOOK ─────────────────────────────────────────────────
    y -= 2
    y = section(c, c2, y, cw, 'KNOWN SPACE  —  FACTBOOK')
    fr(c, c2, y-50*mm, cw, 50*mm, DARK)
    ty = y - 4*mm

    facts = [
        ('ARM',          'Amalgamated Regional Militia — Earth police/spy'),
        ('Hyperdrive',   '1 light-year per 3 days; no inertial effects'),
        ('Reactionless', 'Thrusters; 1g constant; manoeuvre in atmosphere'),
        ('Year 2851',    'Humanity dominant. Kzin defeated 4× in wars'),
        ('Trinoc',       'Cautiously neutral. Three-legged triplex beings'),
        ('Outsiders',    'Immune to light. Sell hyperdrive knowledge'),
        ('Pak',          'Ancient progenitor race. Protectors terrifying'),
        ('City Builders','Unknown Ringworld makers; called "Ringworlders"'),
        ('Stasis Box',   'Pre-dates universe; contents perfectly preserved'),
        ('Credit/Star',  'United Nations Standard currency. 1 Star = ~$1000'),
    ]
    for i, (term, desc) in enumerate(facts):
        row_bg(c, c2, ty-10, cw, 11, i)
        tx(c, term, c2+3, ty, 'OrbB', 6.5, GOLD)
        ty -= 6.5
        tx(c, desc, c2+3, ty, 'Mono', 5.5, MID)
        ty -= 5
    y -= 50*mm

    # ── NPC REACTION TABLE ───────────────────────────────────────────────────
    y -= 2
    remaining2 = y - bottom - 2
    y = section(c, c2, y, cw, 'NPC REACTION  (2D6 + APP mod)')
    fr(c, c2, y-remaining2, cw, remaining2, DARK)
    ty = y - 4*mm

    reactions = [
        ('2–3',   'Hostile.    Immediate attack or flight'),
        ('4–5',   'Unfriendly. Will not cooperate; may threaten'),
        ('6–8',   'Neutral.    Waits for approach/bribe/offer'),
        ('9–10',  'Friendly.   Willing to talk; moderate help'),
        ('11–12', 'Helpful.    Aid freely; may become ally'),
    ]
    for i, (roll, result) in enumerate(reactions):
        ty -= 7
        row_bg(c, c2, ty-2, cw, 8, i)
        tx(c, roll, c2+3, ty, 'OrbB', 7, GOLD)
        tx(c, result, c2+18*mm, ty, 'Mono', 6.5, white)
    ty -= 10
    tx(c, 'Modify by APP bonus, situation, species relations', c2+3, ty, 'Mono', 5.8, HexColor('#887755'))

    # ─────────────────────────── COLUMN 3 ────────────────────────────────────
    y = top

    # ── ARMOUR & PROTECTION ─────────────────────────────────────────────────
    y = section(c, c3, y, cw, 'ARMOUR & PROTECTION')
    fr(c, c3, y-30*mm, cw, 30*mm, DARK)
    ty = y - 4*mm

    armour = [
        ('Cloth/light clothing',     '1 AP'),
        ('Leather / heavy padding',  '2 AP'),
        ('Light body armour',        '3–4 AP'),
        ('Heavy armour / suit',      '5–8 AP'),
        ('Hullmetal (vehicle)',       '20+ AP'),
        ('Scrith',                   'Invulnerable'),
    ]
    for lbl, lx in [('ARMOUR TYPE',c3+2),('AP',c3+cw-2)]:
        tx(c, lbl, lx, ty, 'OrbB', 6, GOLD, 'left' if lbl!='AP' else 'right')
    ty -= 3; hl(c, c3+2, c3+cw-2, ty, GOLD, 0.7)
    for i, (arm, ap) in enumerate(armour):
        ty -= 7
        row_bg(c, c3, ty-2, cw, 7.5, i)
        tx(c, arm, c3+3, ty, 'Bar', 8.5, white)
        tx(c, ap, c3+cw-2, ty, 'OrbB', 7, GOLD, 'right')
    ty -= 8
    tx(c, 'AP reduces damage to that location. Excess carries through.', c3+3, ty, 'Mono', 5.5, HexColor('#887755'))
    y -= 30*mm

    # ── EXPERIENCE & IMPROVEMENT ────────────────────────────────────────────
    y -= 2
    y = section(c, c3, y, cw, 'EXPERIENCE & IMPROVEMENT')
    fr(c, c3, y-32*mm, cw, 32*mm, DARK)
    ty = y - 4*mm
    exp_rules = [
        'GM awards D6 experience at session end',
        'Spend pts: 1 exp = +1% to any used skill',
        'Training: hours = current skill percentage',
        'Teacher halves training time needed',
        'Simweb halves time (not physical stats)',
        'Characteristics: 25hrs × current value, roll D3−1',
        'Skill over 100%: special success threshold rises',
        'Max skill: 1000%+ (00 always fails regardless)',
    ]
    for s in exp_rules:
        tx(c, '▸ ' + s, c3+3, ty, 'Mono', 6, MID); ty -= 7.5
    y -= 32*mm

    # ── GAMESMASTER NOTES ────────────────────────────────────────────────────
    y -= 2
    y = section(c, c3, y, cw, 'GAMESMASTER QUICK NOTES')
    fr(c, c3, y-28*mm, cw, 28*mm, DARK)
    ty = y - 4*mm
    gm_notes = [
        'Health Roll: CON×3 vs poison/disease/environment',
        'Reasoning: INT×3 vs memory, unfamiliar equipment',
        'Luck: POW×3 vs pure chance events',
        'Resistance: 50+(act×5)-(pas×5) for char vs char',
        'Characteristic damage: lost CON reduces health roll',
        'Stunner: target MAS determines stun duration',
        'Variable Sword: special success = dismemberment',
        'Puppeteer nerve weapon: targets POW vs CON=16',
    ]
    for s in gm_notes:
        tx(c, '▸ ' + s, c3+3, ty, 'Mono', 6, MID); ty -= 7.5
    y -= 28*mm

    # ── FOOLISH ENDEAVOUR CREW ───────────────────────────────────────────────
    y -= 2
    y = section(c, c3, y, cw, 'CREW  —  FOOLISH ENDEAVOUR  (Events 95/96)')
    fr(c, c3, y-50*mm, cw, 50*mm, DARK)
    ty = y - 4*mm

    crew = [
        ('#1 Mira Chen',        HexColor('#00c8ff'), 'Xenobiologist · Earth human · HP 11'),
        ('#2 Yashti Korr',      HexColor('#ff6600'), 'Security · Wunderland human · HP 14'),
        ('#3 RR\'raan',         HexColor('#ff2222'), 'Combat · Kzin · HP 18 · DB +2D6'),
        ('#4 Whisper',          HexColor('#aa00ff'), 'Intel · Puppeteer · HP 12'),
        ('#5 Tomas Veld',       HexColor('#ffbb00'), 'Engineer · Jinx human · HP 13'),
        ('#6 Sola Reyes',       HexColor('#00cc55'), 'Navigator · We Made It · HP 12'),
    ]
    for i, (name, col, detail) in enumerate(crew):
        row_bg(c, c3, ty-12, cw, 13, i)
        fr(c, c3, ty-12, 3*mm, 13, col)
        tx(c, name, c3+4*mm, ty-2, 'OrbB', 6.5, col)
        tx(c, detail, c3+4*mm, ty-9, 'Mono', 5.5, MID)
        ty -= 14
    y -= 50*mm

    # ── SCENARIO QUICK REFERENCE ─────────────────────────────────────────────
    y -= 2
    remaining3 = y - bottom - 2
    y = section(c, c3, y, cw, 'SCENARIOS  —  QUICK REFERENCE')
    fr(c, c3, y-remaining3, cw, remaining3, DARK)
    ty = y - 4*mm

    fr(c, c3, ty-8, cw, 8, HexColor('#1a0800'))
    tx(c, 'EVENT 95  —  A QUESTION OF SINGULARITY', c3+3, ty-5.5, 'OrbB', 6, GOLD)
    ty -= 10
    e95 = [
        'Weather Spire · quiet zone · no biology',
        'Marr the trapped researcher (Kzin)',
        'Loop / singularity mechanic — time repeats',
        'Decision: release, redirect, or contain',
        'Not a combat scenario. Knowledge wins.',
    ]
    for s in e95:
        tx(c, '▸ ' + s, c3+3, ty, 'Mono', 5.8, MID); ty -= 7
    ty -= 6

    fr(c, c3, ty-8, cw, 8, HexColor('#000818'))
    tx(c, 'EVENT 96  —  IS LOVE THE ANSWER?', c3+3, ty-5.5, 'OrbB', 6, GOLD)
    ty -= 10
    e96 = [
        'Serenthis the Rememberer · vault · encoding',
        'Ghresh-Ka: Kzin warlord approaching',
        'Storm deadline: 2-hour extraction window',
        'Bond: Mira (or highest Linguistics)',
        'Kzin honour challenge: 1/combat, unique gambit',
    ]
    for s in e96:
        tx(c, '▸ ' + s, c3+3, ty, 'Mono', 5.8, MID); ty -= 7

    # ── FOOTER ───────────────────────────────────────────────────────────────
    fr(c, 0, 0, PW, 8*mm, INK)
    hl(c, 0, PW, 8*mm, GOLD, 1)
    tx(c, 'RINGWORLD RPG  ·  CHAOSIUM 1984  ·  PRINT DOUBLE-SIDED FLIP ON SHORT EDGE', PAD, 2.5*mm, 'Mono', 6, GOLD)
    tx(c, 'ChaosiumCon UK 2026  ·  Events 95 & 96', PW-PAD, 2.5*mm, 'Mono', 6, MID, 'right')


# ── Generate ──────────────────────────────────────────────────────────────────
OUT = '/home/claude/ChaosiumCon26/apps/ringworld-character-sheets/ringworld-cheatsheet.pdf'
cv = rl_canvas.Canvas(OUT, pagesize=A4)
draw_front(cv); cv.showPage()
draw_back(cv);  cv.showPage()
cv.save()

import os
print(f'Saved: {OUT}')
print(f'Size: {os.path.getsize(OUT):,} bytes')
