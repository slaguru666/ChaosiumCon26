"""
Ringworld RPG Character Sheets — ChaosiumCon UK 2026
Events 95 & 96 — Crew of the Foolish Endeavour
Built with reportlab for precise print-ready PDF output.
"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white, black, Color
import math, os

# ─── Constants ────────────────────────────────────────────────────────────────
PW, PH = A4          # 595.28 × 841.89 pt
PAD = 6*mm         # page margin

# ─── Font registration ────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont('Orb',    '/tmp/font-orbitron-700.ttf'))
pdfmetrics.registerFont(TTFont('OrbB',   '/tmp/font-orbitron-900.ttf'))
pdfmetrics.registerFont(TTFont('Mono',   '/tmp/font-sharetechmono.ttf'))
pdfmetrics.registerFont(TTFont('Bar',    '/tmp/font-barlow-700.ttf'))
pdfmetrics.registerFont(TTFont('BarB',   '/tmp/font-barlow-900.ttf'))

# ─── Colour helpers ───────────────────────────────────────────────────────────
INK   = HexColor('#06060e')
LIGHT = HexColor('#f0f0f8')
MID   = HexColor('#c0c0d8')
PALE  = HexColor('#e8e8f4')

# ─── Skill base chances (from Explorer Book) ─────────────────────────────────
BASE = {
    # AGILITY
    'Archaic Melee Weapon':5,'Archaic Ranged Weapons':3,'Athletics':15,
    'Hide':10,'Sneak':5,'Unarmed Combat':0,'V.Sword / F.Laser':15,
    # COMMUNICATION
    'Bargain':10,'Debate':5,'Fast Talk':10,'Fine Arts':5,'Musicianship':5,
    'Orate':5,'Own Language':90,'Perform':5,'Psychology':0,
    # KNOWLEDGE
    'Anthropology':0,'Astronomy':0,'Biology':0,'Botany':0,'Chemistry':0,
    'Computers':0,'Emergency Treatment':1,'Engineering':0,'Farming':0,
    'History':5,'Law':0,'Mathematics':0,'Physics':0,'Planetology':0,
    'Second Language':0,'Strategy':0,'Theology':0,'Zoology':0,
    # PERCEPTION
    'Handgun Energy':5,'Handgun Projectile':3,
    'Heavy Weapon Energy':5,'Heavy Weapon Proj.':3,
    'Listen':5,'Observe':5,'Scent':0,'Search':5,'Track':5,
    # TECHNICAL
    'Aquatic Vehicle':0,'Atmospheric Craft':0,'Ground Vehicle':0,
    'Hyperdrive':0,'Personal Flyer':15,'Reaction Drive':0,
    'Reactionless Drive':0,'Repair':0,'Ringworld':0,'Weapons System':0,
}

SKILL_CATEGORIES = [
    ('AGILITY', ['Archaic Melee Weapon','Archaic Ranged Weapons','Athletics',
                 'Hide','Sneak','Unarmed Combat','V.Sword / F.Laser']),
    ('COMMUNICATION', ['Bargain','Debate','Fast Talk','Fine Arts','Musicianship',
                       'Orate','Own Language','Perform','Psychology']),
    ('KNOWLEDGE', ['Anthropology','Astronomy','Biology','Botany','Chemistry',
                   'Computers','Emergency Treatment','Engineering','Farming',
                   'History','Law','Mathematics','Physics','Planetology',
                   'Second Language','Strategy','Theology','Zoology']),
    ('PERCEPTION', ['Handgun Energy','Handgun Projectile','Heavy Weapon Energy',
                    'Heavy Weapon Proj.','Listen','Observe','Scent','Search','Track']),
    ('TECHNICAL', ['Aquatic Vehicle','Atmospheric Craft','Ground Vehicle',
                   'Hyperdrive','Personal Flyer','Reaction Drive',
                   'Reactionless Drive','Repair','Ringworld','Weapons System']),
]

def get_skill(char_skills, name):
    """Return trained value or base chance."""
    if name in char_skills:
        return char_skills[name]
    return BASE.get(name, 0)

# ─── Drawing helpers ──────────────────────────────────────────────────────────
def filled_rect(c, x, y, w, h, fill, stroke=None, lw=0):
    c.saveState()
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw if lw else 0.5)
    else:
        c.setLineWidth(0)
    c.rect(x, y, w, h, fill=1, stroke=1 if stroke else 0)
    c.restoreState()

def outline_rect(c, x, y, w, h, stroke, lw=1):
    c.saveState()
    c.setStrokeColor(stroke)
    c.setLineWidth(lw)
    c.setFillColor(Color(0,0,0,0))
    c.rect(x, y, w, h, fill=0, stroke=1)
    c.restoreState()

def text(c, txt, x, y, font, size, color, align='left'):
    c.saveState()
    c.setFont(font, size)
    c.setFillColor(color)
    if align=='left': c.drawString(x, y, txt)
    elif align=='right': c.drawRightString(x, y, txt)
    elif align=='centre': c.drawCentredString(x, y, txt)
    c.restoreState()

def hline(c, x1, x2, y, color, lw=0.5):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x1, y, x2, y)
    c.restoreState()

def dots(c, x1, x2, y, color):
    """Draw dotted fill between two x positions."""
    c.saveState()
    c.setFillColor(color)
    step = 3
    for px in range(int(x1), int(x2), step):
        c.circle(px, y+1, 0.4, fill=1, stroke=0)
    c.restoreState()

# ─── Section label helper ─────────────────────────────────────────────────────
def section_label(c, x, y, w, label, acc, font='OrbB', size=7):
    filled_rect(c, x, y, w, 10, acc)
    text(c, label, x+4, y+2.5, font, size, white)

# ─── HP tick boxes ────────────────────────────────────────────────────────────
def draw_hp_boxes(c, x, y, n, acc, box=5.5, gap=1.5):
    c.saveState()
    c.setStrokeColor(acc)
    c.setLineWidth(1)
    cx = x
    for i in range(n):
        c.setFillColor(Color(0,0,0,0))
        c.rect(cx, y, box, box, fill=0, stroke=1)
        if (i+1) % 5 == 0:
            # tick mark above every 5th
            c.setStrokeColor(acc)
            c.line(cx+box/2, y+box+1, cx+box/2, y+box+3)
        cx += box + gap
    c.restoreState()
    return cx  # end x position

# ─── Front page ───────────────────────────────────────────────────────────────
def draw_front(c, char, page_num, total_pages):
    A = char['acc']       # accent colour
    AD = char['acc_dark'] # dark accent

    # ── HEADER BAND ──────────────────────────────────────────────────────────
    # Full-width colour band at top
    header_h = 42*mm
    filled_rect(c, 0, PH-header_h, PW, header_h, A)

    # Character number (huge watermark)
    c.saveState()
    c.setFont('OrbB', 120)
    c.setFillColor(white)
    c.setFillAlpha(0.08)
    c.drawString(8*mm, PH-header_h+2*mm, str(char['num']))
    c.restoreState()

    # Portrait slot (right side, 40mm × 42mm)
    port_w = 40*mm
    port_h = header_h
    port_x = PW - port_w
    port_y = PH - header_h
    # Portrait image or placeholder
    if char.get('portrait_path') and os.path.exists(char['portrait_path']):
        try:
            c.drawImage(char['portrait_path'], port_x, port_y,
                       width=port_w, height=port_h,
                       preserveAspectRatio=True, anchor='n', mask='auto')
        except:
            filled_rect(c, port_x, port_y, port_w, port_h, AD)
    else:
        filled_rect(c, port_x, port_y, port_w, port_h, AD)
        # Placeholder crosshair
        cx, cy = port_x + port_w/2, port_y + port_h/2
        c.saveState()
        c.setStrokeColor(A)
        c.setLineWidth(0.8)
        c.setStrokeAlpha(0.4)
        c.line(cx-8*mm, cy, cx+8*mm, cy)
        c.line(cx, cy-8*mm, cx, cy+8*mm)
        c.rect(cx-10*mm, cy-10*mm, 20*mm, 20*mm, fill=0, stroke=1)
        c.restoreState()
        text(c, 'PORTRAIT', cx, cy-14*mm, 'Mono', 6, A, align='centre')
        text(c, 'TBD', cx, cy-17*mm, 'Mono', 5, A, align='centre')

    # Dark overlay strip behind text (left of portrait)
    name_area_w = PW - port_w - 2*PAD
    # Species badge
    filled_rect(c, PAD, PH - 8*mm, 28*mm, 5.5*mm, INK)
    text(c, char['species'].upper(), PAD+2*mm, PH-6.5*mm, 'Mono', 6, A)

    # Character name
    name_y = PH - header_h + 16*mm
    text(c, char['name'].upper(), PAD, name_y, 'OrbB', 18, white)
    # Role
    text(c, char['role'], PAD, name_y - 6*mm, 'Bar', 8.5, white)
    # Homeworld / context
    text(c, char.get('context',''), PAD, name_y - 11*mm, 'Mono', 6.5, HexColor('#ffffffaa'))

    # RINGWORLD masthead - very top strip
    filled_rect(c, 0, PH-3.5*mm, PW, 3.5*mm, INK)
    text(c, 'RINGWORLD', PAD, PH-2.8*mm, 'OrbB', 7, A)
    text(c, 'EXPLORER BOOK  ·  CHAOSIUMCON UK 2026  ·  EVENTS 95 & 96', 
         PW/2, PH-2.8*mm, 'Mono', 5.5, MID, align='centre')
    text(c, f'{page_num}/{total_pages}', PW-PAD, PH-2.8*mm, 'Mono', 5.5, MID, align='right')

    # Colour bar at bottom of header
    filled_rect(c, 0, PH-header_h-1.5*mm, PW, 1.5*mm, INK)

    # ── CHARACTERISTICS ───────────────────────────────────────────────────────
    stats_y = PH - header_h - 1.5*mm
    stats_h = 26*mm
    filled_rect(c, 0, stats_y - stats_h, PW, stats_h, INK)

    stats = [('STR',char['STR']),('CON',char['CON']),('SIZ',char['SIZ']),
             ('INT',char['INT']),('POW',char['POW']),('DEX',char['DEX']),
             ('APP',char['APP']),('EDU',char['EDU'])]

    box_w = (PW - 2*PAD) / 8
    for i, (lbl, val) in enumerate(stats):
        bx = PAD + i * box_w
        by = stats_y - stats_h + 1*mm
        bh = stats_h - 2*mm
        bw = box_w - 1.5
        # box
        outline_rect(c, bx, by, bw, bh, A, lw=1.2)
        # label
        text(c, lbl, bx + bw/2, by + bh - 7, 'OrbB', 9, A, align='centre')
        # value
        text(c, str(val), bx + bw/2, by + 4, 'OrbB', 23, white, align='centre')

    # ── DERIVED STATS ROW ─────────────────────────────────────────────────────
    der_y = stats_y - stats_h
    der_h = 12*mm
    filled_rect(c, 0, der_y - der_h, PW, der_h, HexColor('#0e0e1e'))
    hline(c, 0, PW, der_y - der_h, A, lw=1.5)

    hp = char['hp']
    dex = int(char['DEX'])
    con = int(char['CON'])
    intv = int(char['INT'])
    powv = int(char['POW'])

    ar_table = {range(1,5):7, range(5,9):6, range(9,13):5,
                range(13,17):4, range(17,21):3, range(21,25):2}
    ar = next((v for k,v in ar_table.items() if dex in k), 1)
    unc = math.ceil(hp * 0.25)

    derived = [
        ('HP MAX', str(hp)),
        ('MOVE', char.get('move','3m')),
        ('DAM BONUS', char['db']),
        ('ACT RANK', str(ar)),
        ('DODGE', f"{dex*3}%"),
        ('HEALTH', f"{con*3}%"),
        ('REASONING', f"{intv*3}%"),
        ('LUCK', f"{powv*3}%"),
        ('UNCONSCIOUS', f"≤{unc}HP"),
    ]
    dbox_w = (PW - 2*PAD) / len(derived)
    for i, (lbl, val) in enumerate(derived):
        dx = PAD + i * dbox_w
        dy = der_y - der_h + 1*mm
        dh = der_h - 2*mm
        dw = dbox_w - 1
        # Highlight HP MAX
        fill = A if lbl == 'HP MAX' else HexColor('#1a1a2e')
        outline_rect(c, dx, dy, dw, dh, A, lw=0.8)
        filled_rect(c, dx+0.4, dy+0.4, dw-0.8, dh-0.8, fill)
        lbl_col = INK if lbl == 'HP MAX' else A
        val_col = INK if lbl == 'HP MAX' else white
        text(c, lbl, dx + dw/2, dy + dh - 5, 'Orb', 4.8, lbl_col, align='centre')
        text(c, val, dx + dw/2, dy + 3.5, 'OrbB', 9, val_col, align='centre')

    # ── HP TRACKER ────────────────────────────────────────────────────────────
    hp_y = der_y - der_h
    hp_sec_h = 10*mm
    filled_rect(c, 0, hp_y - hp_sec_h, PW, hp_sec_h, HexColor('#0a0a18'))
    hline(c, 0, PW, hp_y - hp_sec_h, A, lw=1.5)
    text(c, 'HIT POINTS', PAD, hp_y - 4*mm, 'OrbB', 6.5, A)
    draw_hp_boxes(c, PAD + 26*mm, hp_y - hp_sec_h + 2.5*mm, hp, A)
    text(c, f'UNCONSCIOUS ≤ {unc}  ·  DYING at 0  ·  DEAD at −{con}',
         PW - PAD, hp_y - hp_sec_h + 3*mm, 'Mono', 5.5, MID, align='right')

    # ── SKILLS SECTION ────────────────────────────────────────────────────────
    sk_top = hp_y - hp_sec_h
    wpn_h  = 40*mm   # weapons
    notes_h = 34*mm  # equipment + personality
    foot_h  = 8*mm   # footer
    sk_bot  = wpn_h + notes_h + foot_h
    sk_h    = sk_top - sk_bot

    filled_rect(c, 0, sk_bot, PW, sk_h, white)
    hline(c, 0, PW, sk_bot + sk_h, A, lw=1.5)

    # Three skill columns
    col_w = (PW - 2*PAD - 2*3) / 3   # 3 columns, 3pt gaps
    col_xs = [PAD, PAD + col_w + 3, PAD + 2*(col_w + 3)]

    # Column assignment
    col_cats = [
        [SKILL_CATEGORIES[0], SKILL_CATEGORIES[1]],      # Agility + Communication
        [SKILL_CATEGORIES[2]],                            # Knowledge
        [SKILL_CATEGORIES[3], SKILL_CATEGORIES[4]],       # Perception + Technical
    ]

    # Draw column dividers
    for cx in col_xs[1:]:
        hline(c, cx-1.5, cx-1.5, sk_bot, A, lw=0.5)
        # actually draw vertical line
        c.saveState()
        c.setStrokeColor(A)
        c.setLineWidth(0.5)
        c.setStrokeAlpha(0.3)
        c.line(cx-1.5, sk_bot, cx-1.5, sk_bot+sk_h)
        c.restoreState()

    row_h    = 12.5    # pts per skill row
    cat_h    = 13      # pts for category header
    cat_gap  = 4       # gap before category

    char_skills = char['skills']

    for col_idx, cats in enumerate(col_cats):
        cx = col_xs[col_idx]
        cw = col_w
        cy = sk_bot + sk_h - 2   # start from top, going down

        for cat_name, skill_list in cats:
            cy -= cat_gap

            # Category header bar
            filled_rect(c, cx, cy - cat_h + 2, cw, cat_h, A)
            text(c, cat_name, cx + 3, cy - cat_h + 5.5, 'OrbB', 6.5, white)
            
            # Root max info on right of header
            root_max_map = {
                'AGILITY': f"max STR+DEX = {char['STR']}+{char['DEX']}",
                'COMMUNICATION': f"max INT+APP = {char['INT']}+{char['APP']}",
                'KNOWLEDGE': f"max INT+EDU = {char['INT']}+{char['EDU']}",
                'PERCEPTION': f"max POW+CON = {char['POW']}+{char['CON']}",
                'TECHNICAL': f"max DEX+INT = {char['DEX']}+{char['INT']}",
            }
            rm_text = root_max_map.get(cat_name, '')
            text(c, rm_text, cx+cw-2, cy-cat_h+5.5, 'Mono', 4.8, white, align='right')
            cy -= cat_h

            for skill_name in skill_list:
                val = get_skill(char_skills, skill_name)
                base = BASE.get(skill_name, 0)
                trained = val > base
                cy -= row_h

                # Alternate row shading
                if skill_list.index(skill_name) % 2 == 1:
                    filled_rect(c, cx, cy-0.5, cw, row_h, HexColor('#f0f0f8'))

                # Skill name
                name_color = INK if trained else HexColor('#888899')
                text(c, skill_name, cx+2, cy+2.5, 'Bar', 8, name_color)

                # Value percentage
                if trained:
                    pct_color = AD if val >= 70 else INK
                    font = 'OrbB'
                else:
                    pct_color = HexColor('#aaaacc')
                    font = 'Orb'
                text(c, f"{val}%", cx+cw-2, cy+2.5, font, 8, pct_color, align='right')

                # Dot leaders between name and value
                # Measure approximate text widths
                sk_name_end = cx + 2 + len(skill_name) * 4.4  # approx
                pct_start   = cx + cw - 2 - len(f"{val}%") * 5 - 6
                if pct_start > sk_name_end + 4:
                    hline(c, sk_name_end+3, pct_start, cy+3.5, HexColor('#ddddee'), lw=0.4)

    # ── WEAPONS ───────────────────────────────────────────────────────────────
    wpn_y = notes_h + foot_h
    filled_rect(c, 0, wpn_y, PW, wpn_h, PALE)
    hline(c, 0, PW, wpn_y + wpn_h, A, lw=1.5)
    filled_rect(c, 0, wpn_y + wpn_h - 9, PW, 9, A)
    text(c, 'WEAPONS & COMBAT', PAD, wpn_y + wpn_h - 6.5, 'OrbB', 8, white)

    # Weapons header line
    hdr_y = wpn_y + wpn_h - 20
    text(c, 'WEAPON NAME', PAD+2, hdr_y, 'OrbB', 7, HexColor('#666677'))
    text(c, 'SKILL %  /  DAMAGE  /  RANGE', PW-PAD, hdr_y, 'OrbB', 7,
         HexColor('#666677'), align='right')
    hline(c, PAD, PW-PAD, hdr_y - 2, MID, lw=0.6)

    row_y = hdr_y - 3
    for wi, wpn in enumerate(char['weapons']):
        row_y -= 10*mm
        wpn_bg = HexColor('#eeeefc') if wi % 2 == 0 else white
        filled_rect(c, PAD, row_y - 1*mm, PW - 2*PAD, 10*mm, wpn_bg)
        # Weapon name left, skill% right — top line
        if len(wpn) > 0:
            text(c, str(wpn[0]), PAD+3, row_y+5.5*mm, 'Bar', 10, INK)
        if len(wpn) > 1:
            text(c, str(wpn[1]), PW-PAD, row_y+5.5*mm, 'OrbB', 11, AD, align='right')
        # Damage · Range · Notes — bottom line
        details = []
        if len(wpn) > 2: details.append(f'DMG {wpn[2]}')
        if len(wpn) > 3: details.append(f'RNG {wpn[3]}')
        if len(wpn) > 4 and wpn[4]: details.append(str(wpn[4]))
        if details:
            text(c, '  ·  '.join(details), PAD+3, row_y+1.8*mm, 'Mono', 7,
                 HexColor('#444466'))
        hline(c, PAD, PW-PAD, row_y-1.5, HexColor('#ccccdd'), lw=0.3)

    # ── EQUIPMENT + PERSONALITY ───────────────────────────────────────────────
    notes_y = foot_h
    half_w = (PW - 2*PAD - 3) / 2
    
    # Equipment (left)
    filled_rect(c, 0, notes_y, half_w + PAD + 1.5, notes_h, INK)
    text(c, 'EQUIPMENT', PAD, notes_y + notes_h - 7, 'OrbB', 7.5, A)
    eq_lines = char['equip']
    ey = notes_y + notes_h - 16
    for eq in eq_lines:
        text(c, '▸ ' + eq, PAD, ey, 'Bar', 8, HexColor('#ccccee'))
        ey -= 9

    # Personality (right)
    rx = half_w + PAD + 3
    filled_rect(c, rx, notes_y, PW - rx, notes_h, A)
    text(c, 'CHARACTER', rx + 3, notes_y + notes_h - 7, 'OrbB', 7.5, white)
    pers_lines = char['personality']
    py = notes_y + notes_h - 16
    for line in pers_lines:
        text(c, line, rx + 3, py, 'Bar', 9, white)
        py -= 10

    # ── FOOTER ────────────────────────────────────────────────────────────────
    filled_rect(c, 0, 0, PW, foot_h, INK)
    hline(c, 0, PW, foot_h, A, lw=1)
    text(c, f'No.{char["num"]}  ·  {char["name"].upper()}  ·  {char["role"]}',
         PAD, 2.5*mm, 'Mono', 6, A)
    text(c, 'RINGWORLD RPG 1984  ·  CHAOSIUM INC.',
         PW-PAD, 2.5*mm, 'Mono', 6, HexColor('#666688'), align='right')

# ─── Back page ────────────────────────────────────────────────────────────────

def draw_puppeteer_hloc(c, char):
    """Pierson's Puppeteer hit location diagram — two heads, two forelegs, rear leg, body."""
    A   = char['acc']
    AD  = char['acc_dark']
    hp  = char['hp']
    con = int(char['CON'])

    hloc_y_top = PH - 10*mm
    hloc_h     = 130*mm
    hloc_y_bot = hloc_y_top - hloc_h

    filled_rect(c, 0, hloc_y_bot, PW, hloc_h, HexColor('#0a0a18'))
    hline(c, 0, PW, hloc_y_bot, A, lw=1.5)

    bar_h = 11
    bar_y = hloc_y_top - bar_h - 3
    filled_rect(c, 0, bar_y, PW, bar_h, A)
    text(c, "HIT LOCATIONS & DAMAGE  —  PIERSON'S PUPPETEER", PAD, bar_y+3, 'OrbB', 8, INK)

    body_hp    = math.ceil(hp * 0.40)
    neck_hp    = math.ceil(hp * 0.20)
    head_hp    = math.ceil(hp * 0.25)
    foreleg_hp = math.ceil(hp * 0.20)
    rearleg_hp = math.ceil(hp * 0.25)
    unc        = math.ceil(hp * 0.25)

    content_top = bar_y
    dia_w = 70*mm
    bx    = PAD + dia_w / 2
    body_cy = content_top - 65*mm

    # Barrel body
    c.saveState(); c.setStrokeColor(A); c.setLineWidth(2); c.setFillColor(Color(0,0,0,0))
    c.ellipse(bx-20*mm, body_cy-16*mm, bx+20*mm, body_cy+14*mm, fill=0, stroke=1)
    c.restoreState()
    text(c, 'BODY',          bx, body_cy+4*mm,   'OrbB', 10, A,     align='centre')
    text(c, f'{body_hp} HP', bx, body_cy-2*mm,   'OrbB', 11, white, align='centre')
    text(c, '01-07',         bx, body_cy-8*mm,   'Mono', 9,  MID,   align='centre')

    # Forelegs
    fl_top = body_cy - 16*mm
    fl_bh  = 32*mm; fl_bw = 12*mm
    for side, lbl, rng in [(-1,'R FORE','08-10'),(+1,'L FORE','11-12')]:
        fx = bx + side*28*mm
        c.saveState(); c.setStrokeColor(A); c.setLineWidth(1.8); c.setFillColor(Color(0,0,0,0))
        c.rect(fx-fl_bw/2, fl_top-fl_bh, fl_bw, fl_bh, fill=0, stroke=1)
        c.restoreState()
        text(c, lbl,              fx, fl_top-13*mm, 'OrbB', 9,  A,     align='centre')
        text(c, f'{foreleg_hp} HP',fx, fl_top-19*mm, 'OrbB', 10, white, align='centre')
        text(c, rng,              fx, fl_top-25*mm, 'Mono', 8,  MID,   align='centre')

    # Rear leg
    rl_bh = 32*mm; rl_bw = 12*mm
    c.saveState(); c.setStrokeColor(A); c.setLineWidth(1.8); c.setFillColor(Color(0,0,0,0))
    c.rect(bx-rl_bw/2, fl_top-rl_bh, rl_bw, rl_bh, fill=0, stroke=1)
    c.restoreState()
    text(c, 'REAR LEG',        bx, fl_top-13*mm, 'OrbB', 9,  A,     align='centre')
    text(c, f'{rearleg_hp} HP',bx, fl_top-19*mm, 'OrbB', 10, white, align='centre')
    text(c, '13-14',           bx, fl_top-25*mm, 'Mono', 8,  MID,   align='centre')

    # Necks (curved bezier)
    neck_base = body_cy + 14*mm
    neck_tip_l = (bx-22*mm, neck_base+32*mm)
    neck_tip_r = (bx+22*mm, neck_base+32*mm)
    c.saveState(); c.setStrokeColor(A); c.setLineWidth(9); c.setStrokeAlpha(0.15)
    c.bezier(bx-6*mm, neck_base, bx-14*mm, neck_base+16*mm,
             neck_tip_l[0]+4*mm, neck_tip_l[1]-6*mm, neck_tip_l[0], neck_tip_l[1])
    c.bezier(bx+6*mm, neck_base, bx+14*mm, neck_base+16*mm,
             neck_tip_r[0]-4*mm, neck_tip_r[1]-6*mm, neck_tip_r[0], neck_tip_r[1])
    c.restoreState()
    c.saveState(); c.setStrokeColor(A); c.setLineWidth(1.5)
    c.bezier(bx-6*mm, neck_base, bx-14*mm, neck_base+16*mm,
             neck_tip_l[0]+4*mm, neck_tip_l[1]-6*mm, neck_tip_l[0], neck_tip_l[1])
    c.bezier(bx+6*mm, neck_base, bx+14*mm, neck_base+16*mm,
             neck_tip_r[0]-4*mm, neck_tip_r[1]-6*mm, neck_tip_r[0], neck_tip_r[1])
    c.restoreState()
    # neck labels at midpoint
    for side, lbl, rng, tx, ty in [
        (-1,'L NECK','15-16', bx-26*mm, neck_base+15*mm),
        (+1,'R NECK','17-18', bx+26*mm, neck_base+15*mm),
    ]:
        text(c, lbl, tx, ty,       'OrbB', 7.5, A,   align='centre')
        text(c, f'{neck_hp}HP', tx, ty-5*mm, 'Mono', 7, white, align='centre')
        text(c, rng, tx, ty-9*mm, 'Mono', 7, MID,  align='centre')

    # Heads
    for hx, hy, lbl, rng in [
        (neck_tip_l[0], neck_tip_l[1], 'L HEAD', '20'),
        (neck_tip_r[0], neck_tip_r[1], 'R HEAD', '19'),
    ]:
        c.saveState(); c.setStrokeColor(A); c.setLineWidth(2); c.setFillColor(Color(0,0,0,0))
        c.ellipse(hx-9*mm, hy, hx+9*mm, hy+14*mm, fill=0, stroke=1)
        c.restoreState()
        text(c, lbl,           hx, hy+9*mm,  'OrbB', 9,  A,     align='centre')
        text(c, f'{head_hp} HP',hx, hy+4*mm,  'OrbB', 10, white, align='centre')
        text(c, rng,           hx, hy+0.5*mm,'Mono', 8,  MID,   align='centre')

    # Location table (right side) — reuse same column structure
    tbl_x = PAD + dia_w + 5*mm
    tbl_w = PW - tbl_x - PAD
    tbl_y = content_top - 20
    c1=tbl_x; c2=tbl_x+28*mm; c3=tbl_x+46*mm; c4=tbl_x+64*mm; c5=tbl_x+82*mm; c6=tbl_x+100*mm
    for lbl,cx in [('LOCATION',c1),('MELEE',c2),('RANGED',c3),('MAX HP',c4),('CURR HP',c5),('ARMOUR',c6)]:
        text(c, lbl, cx, tbl_y, 'OrbB', 7.5, A)
    hline(c, tbl_x, PW-PAD, tbl_y-3, A, lw=1.2)

    pup_locs = [
        ('Body',       '01-07','01-07', body_hp),
        ('Right Fore', '08-10','08-10', foreleg_hp),
        ('Left Fore',  '11-12','11-12', foreleg_hp),
        ('Rear Leg',   '13-14','13-14', rearleg_hp),
        ('Right Neck', '15-16','15-16', neck_hp),
        ('Left Neck',  '17-18','17-18', neck_hp),
        ('Right Head', '19',   '19',    head_hp),
        ('Left Head',  '20',   '20',    head_hp),
    ]
    row_h = 12*mm; ry = tbl_y - 3
    for i,(loc,m_rng,r_rng,loc_hp) in enumerate(pup_locs):
        ry -= row_h
        bg = HexColor('#0e0e22') if i%2==0 else HexColor('#09090f')
        filled_rect(c, tbl_x-1, ry, tbl_w+1, row_h-1, bg)
        mid_y = ry + row_h*0.42
        text(c, loc,         c1+2,    mid_y, 'Bar',  11,  white)
        text(c, m_rng,       c2+9*mm, mid_y, 'Mono', 9.5, MID,  align='centre')
        text(c, r_rng,       c3+9*mm, mid_y, 'Mono', 9.5, MID,  align='centre')
        text(c, str(loc_hp), c4+8*mm, mid_y, 'OrbB', 14,  A,    align='centre')
        bh = row_h-4*mm
        filled_rect(c, c5, ry+2*mm, 16*mm, bh, white)
        outline_rect(c, c5, ry+2*mm, 16*mm, bh, A, lw=1.2)
        filled_rect(c, c6, ry+2*mm, 16*mm, bh, white)
        outline_rect(c, c6, ry+2*mm, 16*mm, bh, A, lw=1.2)
        hline(c, tbl_x-1, PW-PAD, ry, HexColor('#181830'), lw=0.5)

    unc_y = ry - 5*mm
    filled_rect(c, tbl_x-1, unc_y, tbl_w+1, 14, HexColor('#1a0808'))
    outline_rect(c, tbl_x-1, unc_y, tbl_w+1, 14, A, lw=1.3)
    text(c, f'UNCONSCIOUS: HP ≤ {unc}   ·   DYING: HP = 0   ·   DEAD: HP = −{con}',
         tbl_x+4, unc_y+4.5, 'Mono', 7.5, A)

    tally_y = unc_y - 4*mm - 12*mm
    text(c, 'HP TALLY', tbl_x, tally_y+9, 'OrbB', 7.5, A)
    cr = 5; cstep = 14; row_start_x = tbl_x + 26*mm
    for i in range(20):
        cx_c = row_start_x + i*cstep + cr
        cy_c = tally_y + cr + 1
        c.saveState()
        c.setStrokeColor(A); c.setLineWidth(1.2)
        c.setFillColor(white)
        c.circle(cx_c, cy_c, cr, fill=1, stroke=1)
        c.setFont('Mono',5); c.setFillColor(HexColor('#8899aa'))
        c.drawCentredString(cx_c, cy_c-cr-3.5, str(i+1))
        c.restoreState()

def draw_back(c, char, page_num, total_pages):
    A = char['acc']
    AD = char['acc_dark']
    hp = char['hp']
    con = int(char['CON'])

    # ── BACK MASTHEAD ─────────────────────────────────────────────────────────
    mast_h = 10*mm
    filled_rect(c, 0, PH-mast_h, PW, mast_h, INK)
    filled_rect(c, 0, PH-1.5*mm, PW, 1.5*mm, A)
    text(c, char['name'].upper(), PAD, PH-7*mm, 'OrbB', 11, A)
    text(c, char['role'].upper() + '  ·  REVERSE', PW-PAD, PH-7*mm, 'Mono', 6.5, MID, align='right')

    # ── HIT LOCATION SECTION ──────────────────────────────────────────────────
    hloc_y_top = PH - mast_h
    hloc_h = 130*mm
    hloc_y_bot = hloc_y_top - hloc_h

    if char.get('species','').startswith("Pierson"):
        draw_puppeteer_hloc(c, char)
    else:
        filled_rect(c, 0, hloc_y_bot, PW, hloc_h, HexColor('#0a0a18'))
        hline(c, 0, PW, hloc_y_bot, A, lw=1.5)

        # Section header — 3mm gap below masthead bottom, text clear of bar
        bar_h = 11
        bar_y = hloc_y_top - bar_h - 3
        filled_rect(c, 0, bar_y, PW, bar_h, A)
        text(c, 'HIT LOCATIONS & DAMAGE', PAD, bar_y + 3, 'OrbB', 8, INK)

        arm_hp   = math.ceil(hp * 0.25)
        leg_hp   = math.ceil(hp * 0.30)
        head_hp  = math.ceil(hp * 0.30)
        abd_hp   = math.ceil(hp * 0.30)
        chest_hp = math.ceil(hp * 0.35)
        unc      = math.ceil(hp * 0.25)

        content_top = bar_y  # drawing starts below the header bar

        # ── Body diagram (left, 70mm wide) ────────────────────────────────
        dia_w = 70*mm
        bx    = PAD + dia_w / 2

        # HEAD
        by_head_c = content_top - 18*mm
        c.saveState()
        c.setStrokeColor(A); c.setLineWidth(2); c.setFillColor(Color(0,0,0,0))
        c.ellipse(bx-12*mm, by_head_c-9*mm, bx+12*mm, by_head_c+11*mm, fill=0, stroke=1)
        c.restoreState()
        text(c, 'HEAD',         bx, by_head_c+2*mm,  'OrbB', 10, A,     align='centre')
        text(c, f'{head_hp} HP',bx, by_head_c-3.5*mm,'OrbB', 11, white, align='centre')
        text(c, '19-20',        bx, by_head_c-8.5*mm,'Mono', 9,  MID,   align='centre')

        # Neck
        neck_top = by_head_c - 9*mm
        c.saveState(); c.setStrokeColor(A); c.setLineWidth(1.3); c.setFillColor(Color(0,0,0,0))
        c.rect(bx-4.5*mm, neck_top-7*mm, 9*mm, 7*mm, fill=0, stroke=1)
        c.restoreState()

        # CHEST
        chest_top = neck_top - 7*mm
        chest_w   = 36*mm
        chest_bh  = 30*mm
        c.saveState(); c.setStrokeColor(A); c.setLineWidth(2); c.setFillColor(Color(0,0,0,0))
        c.rect(bx-chest_w/2, chest_top-chest_bh, chest_w, chest_bh, fill=0, stroke=1)
        c.restoreState()
        text(c, 'CHEST',         bx, chest_top-11*mm, 'OrbB', 10, A,     align='centre')
        text(c, f'{chest_hp} HP',bx, chest_top-17*mm, 'OrbB', 11, white, align='centre')
        text(c, '11-15',         bx, chest_top-23*mm, 'Mono', 9,  MID,   align='centre')

        # ABDOMEN
        abd_top = chest_top - chest_bh
        abd_bh  = 20*mm
        abd_w   = 28*mm
        c.saveState(); c.setStrokeColor(A); c.setLineWidth(1.8); c.setFillColor(Color(0,0,0,0))
        c.rect(bx-abd_w/2, abd_top-abd_bh, abd_w, abd_bh, fill=0, stroke=1)
        c.restoreState()
        text(c, 'ABDOMEN',      bx, abd_top-7*mm,  'OrbB', 10, A,     align='centre')
        text(c, f'{abd_hp} HP', bx, abd_top-13*mm, 'OrbB', 11, white, align='centre')
        text(c, '07-10',        bx, abd_top-18*mm, 'Mono', 9,  MID,   align='centre')

        # ARMS
        arm_bh = 36*mm
        arm_bw = 13*mm
        gap    = 3*mm
        for side, lbl, rng in [(-1,'R ARM','16-17'),(+1,'L ARM','18-19')]:
            ax = bx + side*(chest_w/2 + gap + arm_bw/2)
            c.saveState(); c.setStrokeColor(A); c.setLineWidth(1.8); c.setFillColor(Color(0,0,0,0))
            c.rect(ax-arm_bw/2, chest_top-arm_bh, arm_bw, arm_bh, fill=0, stroke=1)
            c.restoreState()
            text(c, lbl,           ax, chest_top-14*mm, 'OrbB', 9,  A,     align='centre')
            text(c, f'{arm_hp} HP',ax, chest_top-20*mm, 'OrbB', 10, white, align='centre')
            text(c, rng,           ax, chest_top-26*mm, 'Mono', 8,  MID,   align='centre')

        # LEGS
        leg_top = abd_top - abd_bh
        leg_bh  = 38*mm
        leg_bw  = 14*mm
        sep     = 3*mm
        for side, lbl, rng in [(-1,'R LEG','01-03'),(+1,'L LEG','04-06')]:
            lx = bx + side*(leg_bw/2 + sep/2)
            c.saveState(); c.setStrokeColor(A); c.setLineWidth(1.8); c.setFillColor(Color(0,0,0,0))
            c.rect(lx-leg_bw/2, leg_top-leg_bh, leg_bw, leg_bh, fill=0, stroke=1)
            c.restoreState()
            text(c, lbl,           lx, leg_top-15*mm, 'OrbB', 9,  A,     align='centre')
            text(c, f'{leg_hp} HP',lx, leg_top-21*mm, 'OrbB', 10, white, align='centre')
            text(c, rng,           lx, leg_top-27*mm, 'Mono', 8,  MID,   align='centre')

        # ── Location table (right side) ───────────────────────────────────
        tbl_x  = PAD + dia_w + 5*mm
        tbl_w  = PW - tbl_x - PAD
        tbl_y  = content_top - 20

        # Col positions
        c1 = tbl_x
        c2 = tbl_x + 28*mm
        c3 = tbl_x + 46*mm
        c4 = tbl_x + 64*mm
        c5 = tbl_x + 82*mm
        c6 = tbl_x + 100*mm

        # Column headers
        for lbl, cx in [('LOCATION',c1),('MELEE',c2),('RANGED',c3),
                         ('MAX HP',c4),('CURR HP',c5),('ARMOUR',c6)]:
            text(c, lbl, cx, tbl_y, 'OrbB', 7.5, A)
        hline(c, tbl_x, PW-PAD, tbl_y - 3, A, lw=1.2)

        locs = [
            ('Head',     '19-20','20',    head_hp),
            ('Right Arm','13-15','16-17', arm_hp),
            ('Left Arm', '16-18','18-19', arm_hp),
            ('Chest',    '12',   '11-15', chest_hp),
            ('Abdomen',  '09-11','07-10', abd_hp),
            ('Right Leg','01-04','01-03', leg_hp),
            ('Left Leg', '05-08','04-06', leg_hp),
        ]

        row_h = 14*mm
        ry    = tbl_y - 3
        for i,(loc,m_rng,r_rng,loc_hp) in enumerate(locs):
            ry -= row_h
            bg = HexColor('#0e0e22') if i%2==0 else HexColor('#09090f')
            filled_rect(c, tbl_x-1, ry, tbl_w+1, row_h-1, bg)
            mid_y = ry + row_h * 0.42
            text(c, loc,          c1+2,        mid_y, 'Bar',  11,  white)
            text(c, m_rng,        c2+9*mm,     mid_y, 'Mono', 9.5, MID,  align='centre')
            text(c, r_rng,        c3+9*mm,     mid_y, 'Mono', 9.5, MID,  align='centre')
            text(c, str(loc_hp),  c4+8*mm,     mid_y, 'OrbB', 14,  A,    align='centre')
            bh = row_h - 4*mm
            filled_rect(c, c5, ry+2*mm, 16*mm, bh, white)
            outline_rect(c, c5, ry+2*mm, 16*mm, bh, A, lw=1.3)
            filled_rect(c, c6, ry+2*mm, 16*mm, bh, white)
            outline_rect(c, c6, ry+2*mm, 16*mm, bh, A, lw=1.3)
            hline(c, tbl_x-1, PW-PAD, ry, HexColor('#181830'), lw=0.5)

        # Unconscious / dying banner — clear gap above
        unc_y = ry - 5*mm
        filled_rect(c, tbl_x-1, unc_y, tbl_w+1, 14, HexColor('#1a0808'))
        outline_rect(c, tbl_x-1, unc_y, tbl_w+1, 14, A, lw=1.3)
        text(c, f'UNCONSCIOUS: HP ≤ {unc}   ·   DYING: HP = 0   ·   DEAD: HP = −{con}',
             tbl_x+4, unc_y+4.5, 'Mono', 7.5, A)

        # HP tally — 20 small white circles to cross out
        tally_y = unc_y - 4*mm - 12*mm
        text(c, 'HP TALLY', tbl_x, tally_y+9, 'OrbB', 7.5, A)
        cr = 5; cstep = 14; row_start_x = tbl_x + 26*mm
        for i in range(20):
            cx_c = row_start_x + i*cstep + cr
            cy_c = tally_y + cr + 1
            c.saveState()
            c.setStrokeColor(A); c.setLineWidth(1.2)
            c.setFillColor(white)
            c.circle(cx_c, cy_c, cr, fill=1, stroke=1)
            c.setFont('Mono', 5); c.setFillColor(HexColor('#8899aa'))
            c.drawCentredString(cx_c, cy_c-cr-3.5, str(i+1))
            c.restoreState()

        # Under-diagram label (bottom of diagram area)
        unc_lbl_y = hloc_y_bot + 2*mm
        filled_rect(c, PAD, unc_lbl_y, dia_w - 2*mm, 11, HexColor('#100608'))
        outline_rect(c, PAD, unc_lbl_y, dia_w - 2*mm, 11, A, lw=0.9)
        text(c, f'UNCONSIOUS ≤ {unc} HP', PAD + (dia_w-2*mm)/2,
             unc_lbl_y+3, 'OrbB', 7.5, A, align='centre')
    # ── COMBAT QUICK REFERENCE ────────────────────────────────────────────────
    cref_h = 34*mm
    cref_y = hloc_y_bot - cref_h
    filled_rect(c, 0, cref_y, PW, cref_h, HexColor('#0c0c1a'))
    hline(c, 0, PW, cref_y + cref_h, A, lw=1.5)
    section_label(c, 0, cref_y + cref_h - 9, PW, 'COMBAT QUICK REFERENCE', A, size=7)

    col1_x, col2_x, col3_x = PAD, PW*0.33, PW*0.66

    # Action ranking
    text(c, 'ACTION RANKING', col1_x, cref_y+cref_h-18, 'OrbB', 6, A)
    ar_data = [('DEX 1-4','AR 7'),('DEX 5-8','AR 6'),('DEX 9-12','AR 5'),
               ('DEX 13-16','AR 4'),('DEX 17-20','AR 3'),('DEX 21+','AR 2-1')]
    dex = int(char['DEX'])
    ay = cref_y + cref_h - 27
    for dex_rng, ar_val in ar_data:
        rng_parts = dex_rng.replace('DEX ','').split('-') if '-' in dex_rng else [dex_rng.replace('DEX ',''),dex_rng.replace('DEX ','')]
        lo = int(rng_parts[0].replace('+',''))
        hi = int(rng_parts[-1].replace('+','999'))
        active = lo <= dex <= hi
        row_col = A if active else HexColor('#333355')
        row_bg = HexColor('#1a1a30') if active else Color(0,0,0,0)
        if active:
            filled_rect(c, col1_x-1, ay-2, 45*mm, 9, HexColor('#1a1a30'))
        text(c, dex_rng, col1_x, ay, 'Mono', 6.5, A if active else HexColor('#666688'))
        text(c, f'◈ {ar_val}' if active else ar_val, col1_x+25*mm, ay, 'OrbB', 6.5 if active else 6, A if active else HexColor('#555577'))
        ay -= 8

    # Range modifiers
    text(c, 'RANGE MODIFIERS', col2_x, cref_y+cref_h-18, 'OrbB', 6, A)
    range_data = [('Point-blank (≤DEX m)','×1.5 (still=auto hit)'),
                  ('Short range','Normal skill %'),
                  ('Medium range','½ skill %'),
                  ('Long range','¼ skill %'),
                  ('No aim (snap)','¼ skill %'),
                  ('Half action rank aim','½ skill %')]
    ry2 = cref_y+cref_h-27
    for rng, mod in range_data:
        text(c, rng, col2_x, ry2, 'Bar', 7, HexColor('#aaaacc'))
        text(c, mod, col2_x + 33*mm, ry2, 'Mono', 6, HexColor('#ccccee'))
        ry2 -= 8

    # Combat rules
    text(c, 'COMBAT RULES', col3_x, cref_y+cref_h-18, 'OrbB', 6, A)
    rules = [
        'SPECIAL SUCCESS: roll ≤ skill÷5',
        'DODGE: DEX×3%, costs 1 impulse',
        'PARRY: roll weapon skill, 1 impulse',
        'SURPRISE: lose action rank impulses',
        'MELEE: full action rank to attack',
        'MOVE: 3m/impulse (Kzin: 5m/10m)',
    ]
    ry3 = cref_y+cref_h-27
    for rule in rules:
        text(c, rule, col3_x, ry3, 'Mono', 6, HexColor('#aaaacc'))
        ry3 -= 8

    # ── SCENARIO HOOKS ────────────────────────────────────────────────────────
    hook_h = 40*mm
    hook_y = cref_y - hook_h
    hline(c, 0, PW, cref_y, A, lw=1.5)
    half = (PW - 2*PAD - 3) / 2

    # Event 95 (left)
    filled_rect(c, 0, hook_y, PW/2, hook_h, white)
    filled_rect(c, 0, hook_y + hook_h - 9, PW/2, 9, A)
    text(c, 'EVENT 95 — A QUESTION OF SINGULARITY', PAD, hook_y+hook_h-6, 'OrbB', 6.5, white)
    h95_lines = char['hook95']
    hy = hook_y + hook_h - 17
    for line in h95_lines:
        text(c, line, PAD, hy, 'Bar', 7.5, HexColor('#222233'))
        hy -= 8.5

    # Event 96 (right)
    filled_rect(c, PW/2+1.5, hook_y, PW/2-1.5, hook_h, white)
    hline(c, PW/2, PW/2, hook_y, A, lw=1)
    c.saveState(); c.setStrokeColor(A); c.setLineWidth(1)
    c.line(PW/2, hook_y, PW/2, hook_y+hook_h); c.restoreState()
    filled_rect(c, PW/2+1.5, hook_y + hook_h - 9, PW/2-1.5, 9, A)
    text(c, 'EVENT 96 — IS LOVE THE ANSWER?', PW/2+PAD, hook_y+hook_h-6, 'OrbB', 6.5, white)
    hy = hook_y + hook_h - 17
    for line in char['hook96']:
        text(c, line, PW/2+PAD, hy, 'Bar', 7.5, HexColor('#222233'))
        hy -= 8.5

    # ── EQUIPMENT & NOTES ─────────────────────────────────────────────────────
    eq_h = hook_y
    eq_y = 8*mm
    eq_sec_h = eq_h - eq_y

    filled_rect(c, 0, eq_y, PW/2, eq_sec_h, INK)
    filled_rect(c, PW/2+1.5, eq_y, PW/2-1.5, eq_sec_h, HexColor('#f8f8ff'))
    hline(c, 0, PW, hook_y, A, lw=1.5)

    filled_rect(c, 0, eq_y+eq_sec_h-9, PW/2, 9, A)
    text(c, 'EQUIPMENT', PAD, eq_y+eq_sec_h-6, 'OrbB', 6.5, INK)
    ey = eq_y + eq_sec_h - 17
    for item in char['equip_detail']:
        text(c, '▸ ' + item, PAD, ey, 'Mono', 6.5, HexColor('#bbbbdd'))
        ey -= 8

    filled_rect(c, PW/2+1.5, eq_y+eq_sec_h-9, PW/2-1.5, 9, A)
    text(c, 'SESSION NOTES', PW/2+PAD, eq_y+eq_sec_h-6, 'OrbB', 6.5, INK)
    ny = eq_y + eq_sec_h - 17
    while ny > eq_y + 6:
        hline(c, PW/2+PAD, PW-PAD, ny, HexColor('#ccccdd'), lw=0.4)
        ny -= 10

    # ── BACK FOOTER ───────────────────────────────────────────────────────────
    filled_rect(c, 0, 0, PW, 8*mm, INK)
    hline(c, 0, PW, 8*mm, A, lw=1)
    text(c, f'No.{char["num"]} / RINGWORLD RPG 1984 / CHAOSIUMCON UK 2026',
         PAD, 2.5*mm, 'Mono', 6, A)
    text(c, f'{page_num}/{total_pages}',
         PW-PAD, 2.5*mm, 'Mono', 6, MID, align='right')


# ══════════════════════════════════════════════════════════════════════════════
# CHARACTER DATA
# ══════════════════════════════════════════════════════════════════════════════
from reportlab.lib.colors import HexColor as H2  # local alias

CHARACTERS = [
  {
    'num':1,'name':'Dr. Mira Chen',
    'role':'Xenobiologist · Lead Scientist',
    'species':'Human · Earth','context':'Survey team, Foolish Endeavour',
    'acc':HexColor('#00c8ff'),'acc_dark':HexColor('#00507a'),
    'STR':'09','CON':'11','SIZ':'10','INT':'18','POW':'13','DEX':'11','APP':'13','EDU':'18',
    'hp':11,'move':'3m/impulse','db':'None','pp':'13',
    'portrait_path':'/home/claude/ChaosiumCon26/scenarios/art/event-96/portrait-mira-chen.jpg',
    'skills':{
        'Athletics':20,'Hide':10,'Sneak':5,'Unarmed Combat':10,
        'Bargain':25,'Debate':30,'Fast Talk':18,'Orate':15,
        'Own Language':90,'Psychology':42,'Persuade':55,
        'Anthropology':48,'Astronomy':22,'Biology':72,'Botany':35,
        'Chemistry':40,'Computers':50,'Emergency Treatment':45,
        'Engineering':10,'History':30,'Linguistics':65,'Medicine':70,
        'Physics':18,'Research':75,'Science (Xenobiology)':85,
        'Strategy':15,'Zoology':55,'Second Language':20,
        'Awareness':60,'Observe':52,'Search':35,'Listen':32,
        'Personal Flyer':15,'Repair':10,'Ringworld':5,
    },
    'weapons':[
        ('Sonic Stunner','30%','Stun (non-lethal)','5 / 20 / 50m','Cone effect; non-lethal'),
        ('Field Syringe','20%','Sedative / Special','Touch only','Medical tool'),
    ],
    'equip':[
        'Medical kit','Portable bio-scanner','Recording equipment',
        'Personal data tablet','Field sample containers','Comdisc (ship link)',
        'Emergency beacon',
    ],
    'equip_detail':[
        'Medical kit (full surgical)','Bio-scanner (portable)','Data tablet',
        'Recording equipment','Field sample containers × 12',
        'Comdisc (ship link)','Emergency beacon','Survey pack',
    ],
    'personality':[
        '"The absence of biology IS the data."',
        'Precise, methodical, narrates aloud.',
        'Will care about Serenthis before',
        'she realises she is doing it.',
    ],
    'hook95':['Your bio-scanner shows the zone\'s ecological void as sharply as a',
              'wound. Linguistics translates system logs. Medicine reads Marr\'s',
              'condition. In Act Three the system displays your xenobiological',
              'profile — it catalogued you as a variable the moment you arrived.',
              '▸ KEY: Science (Xenobiology) · Linguistics · Medicine'],
    'hook96':['Serenthis calls you by name before you introduce yourself. Your',
              'training recognises neurological encoding, not just language. Something',
              'has been written into her. The bond runs through you.',
              '▸ KEY: Linguistics · Awareness · Persuade in Act 3'],
  },
  {
    'num':2,'name':'Lt. Yashti Korr',
    'role':'Military Liaison · Security Lead',
    'species':'Human · Wunderland','context':'Former ARM officer, survey secondment',
    'acc':HexColor('#ff6600'),'acc_dark':HexColor('#884400'),
    'STR':'14','CON':'15','SIZ':'13','INT':'14','POW':'12','DEX':'15','APP':'12','EDU':'14',
    'hp':14,'move':'3m/impulse','db':'+1D4','pp':'12',
    'portrait_path':'/home/claude/ChaosiumCon26/scenarios/art/event-96/portrait-yashti-korr.jpg',
    'skills':{
        'Athletics':45,'Sneak':50,'Hide':45,'Unarmed Combat':62,
        'V.Sword / F.Laser':75,
        'Bargain':28,'Debate':22,'Fast Talk':38,'Own Language':85,'Psychology':42,'Persuade':45,
        'Computers':40,'Emergency Treatment':52,'History':32,'Law':45,'Strategy':55,
        'Handgun Energy':75,'Handgun Projectile':68,'Heavy Weapon Energy':50,
        'Heavy Weapon Proj.':42,'Listen':55,'Observe':65,'Search':60,'Track':48,
        'Ground Vehicle':50,'Atmospheric Craft':38,'Personal Flyer':35,'Repair':22,
        'Weapons System':40,'Ringworld':5,
    },
    'weapons':[
        ('Flashlight-Laser','75%','2D6+2','25 / 100 / 500m','3 power settings'),
        ('ARM Needle Gun','65%','1D3 + paralytic','10 / 40 / 100m','Silent; preferred'),
        ('Combat Knife','65%','1D4+1D4','Touch','Last option'),
    ],
    'equip':['Flashlight-laser','ARM needle gun','Combat knife',
             'Body armour AP2 (torso)','Comms unit','Restraints','Basic medkit'],
    'equip_detail':['Flashlight-laser (3 settings)','ARM needle gun + 12 darts',
                    'Combat knife','Body armour AP2 (torso only)','Comms unit',
                    'Restraints × 4','Basic field medkit','Emergency beacon'],
    'personality':[
        '"Dangerous moment isn\'t when things',
        'go wrong. It\'s when everyone decides',
        'they\'re fine." The needle gun is',
        'preferred. Wunderland aristocracy.',
    ],
    'hook95':['Awareness makes you first to notice repetition. You\'ll set perimeters',
              'when no one else thinks to. In Act Three, when Vorn orders withdrawal,',
              'the crew looks to you: follow orders, or stay for the science?',
              '▸ KEY: Awareness · Tactics · Combat if loops turn physical'],
    'hook96':['You read Ghresh-Ka before the crew does — converging, not hostile yet.',
              'If RR\'raan challenges him directly, back them. It\'s the only gambit.',
              'Your job if it goes to a fight is to buy time, not to win.',
              '▸ KEY: Tactics · Awareness · First Aid if crew hit'],
  },
  {
    'num':3,'name':"RR'raan",
    'role':'Combat Specialist · Kzin Noble',
    'species':'Kzin · Patriarchy','context':'Eighth-litter, minor noble house',
    'acc':HexColor('#ff2222'),'acc_dark':HexColor('#880000'),
    'STR':'22','CON':'16','SIZ':'20','INT':'13','POW':'11','DEX':'16','APP':'08','EDU':'11',
    'hp':18,'move':'5m / 10m sprint','db':'+2D6','pp':'11',
    'portrait_path':'/home/claude/ChaosiumCon26/scenarios/art/event-96/portrait-rraan.jpg',
    'skills':{
        'Athletics':72,'Sneak':50,'Hide':45,'Unarmed Combat':78,
        'V.Sword / F.Laser':70,'Archaic Melee Weapon':35,
        'Own Language':90,'Psychology':38,'Bargain':22,'Persuade':30,
        'History':38,'Strategy':50,'Zoology':40,'Planetology':25,'Emergency Treatment':25,
        'Handgun Energy':65,'Heavy Weapon Energy':55,'Listen':70,
        'Observe':65,'Search':60,'Track':75,'Scent':68,
        'Personal Flyer':35,'Atmospheric Craft':30,'Ground Vehicle':28,
        'Repair':20,'Weapons System':40,'Ringworld':8,
    },
    'weapons':[
        ('Kzin Claws × 2','80%','STR+1D6+2D6','Touch','Both hit = hold; 1D8+2/rnd auto'),
        ('Variable Sword','70%','1D6+4+2D6','Touch–5m','Molecular blade; cuts scrith'),
        ('Kzin Beam Pistol','65%','1D6+8','20 / 80 / 300m','Kzin military sidearm'),
    ],
    'equip':['Kzin fighting claws (natural)','Variable sword','Kzin beam pistol',
             'Personal comm unit','Kzin ration pack','Grapple line'],
    'equip_detail':['Kzin fighting claws (natural weapon)','Variable sword',
                    'Kzin beam pistol + 2 power cells','Personal comm unit',
                    'Kzin ration pack (4 days)','Grapple line (20m)',
                    '[Kzin laser carbine stored shipboard]'],
    'personality':[
        '"This is science." Keeps saying it',
        'because the humans need him to.',
        'Patience is real. Frustration also.',
        'Kzin honour = a weapon humans can\'t use.',
    ],
    'hook95':['The quiet zone registers as total absence of biological signal — your',
              'prey-senses detect it before instruments. Track + Awareness in Act 1.',
              'In Act Three: a threat you cannot fight. The frustration is yours.',
              '▸ KEY: Scent + Awareness · Tracking · CON×5 for descent'],
    'hook96':['Ghresh-Ka is Kzin. Patient — you read it as contempt. Act Three:',
              'challenge him one-on-one, Kzin honour code. Pauses his force.',
              'Buys the crew time. May get you killed. May not. Your choice.',
              '▸ KEY: Intimidate (the challenge) · Combat if honour demands'],
  },
  {
    'num':4,'name':'Whisper-of-Distant-Worlds',
    'role':'Intelligence Analyst · Puppeteer',
    'species':"Pierson's Puppeteer",'context':'Two heads · Three legs · Ship analyst',
    'acc':HexColor('#aa00ff'),'acc_dark':HexColor('#5c0099'),
    'STR':'07','CON':'12','SIZ':'12','INT':'19','POW':'15','DEX':'14','APP':'10','EDU':'19',
    'hp':12,'move':'3m/impulse','db':'None','pp':'15',
    'portrait_path':'/home/claude/ChaosiumCon26/scenarios/art/event-96/portrait-whisper.jpg',
    'skills':{
        'Athletics':22,'Sneak':30,'Hide':25,'Unarmed Combat':5,
        'Bargain':78,'Debate':65,'Fast Talk':80,'Own Language':95,'Orate':55,
        'Persuade':85,'Psychology':82,
        'Anthropology':70,'Astronomy':45,'Biology':40,'Chemistry':30,
        'Computers':80,'Engineering':20,'History':55,'Law':60,
        'Mathematics':65,'Physics':60,'Planetology':30,'Research':75,
        'Strategy':70,'Zoology':45,'Second Language':65,
        'Handgun Energy':10,'Listen':60,'Observe':72,'Search':58,
        'Atmospheric Craft':25,'Hyperdrive':40,'Personal Flyer':35,
        'Reactionless Drive':35,'Repair':15,'Ringworld':12,
    },
    'weapons':[
        ('Restraint Field','45%','Immobilize','5 / 15m cone','Puppeteer non-lethal'),
        ('Rear Hoof Kick','35%','1D6+2','Touch','Emergency; never admits'),
        ('Stepping Disc','95%','Escape','Instant','Teleport; 1/scene'),
    ],
    'equip':['Personal data systems','Multi-freq comms array',
             'Stepping disc harness','Restraint field generator','Analysis kit'],
    'equip_detail':['Personal data systems (full)','Multi-freq comms array',
                    'Stepping disc harness (escape)','Restraint field generator',
                    'Analysis kit','Stun capsules × 3','[No conventional weapons]'],
    'personality':[
        '"I\'ve already accounted for that."',
        'Will not fight. Will talk, flatter,',
        'manipulate. Timing is everything.',
        'Knows more than it shares. Always.',
    ],
    'hook95':['You identify the constructing singularity before anyone else does.',
              'Computer + Science (Physics) cracks the system logs in Act Two.',
              'In Act Three you understand the system\'s logic better than anyone.',
              '▸ KEY: Computer · Science (Physics) · Tactics for Act 3'],
    'hook96':['You recognise what Serenthis is — Protector-class encoded Rememberer.',
              'You will not share this immediately. Time it for maximum effect.',
              'Persuade and Fast Talk are the crew\'s tool against Ghresh-Ka.',
              '▸ KEY: Persuade / Fast Talk · Research · Awareness: Serenthis'],
  },
  {
    'num':5,'name':'Tomas Veld',
    'role':'Chief Engineer · Secondary Pilot',
    'species':'Human · Jinx','context':'Heavy-gravity build; ship engineer',
    'acc':HexColor('#ffbb00'),'acc_dark':HexColor('#886600'),
    'STR':'13','CON':'14','SIZ':'12','INT':'15','POW':'12','DEX':'14','APP':'11','EDU':'16',
    'hp':13,'move':'3m/impulse','db':'+1D4','pp':'12',
    'portrait_path':'/home/claude/ChaosiumCon26/scenarios/art/event-96/portrait-tomas-veld.jpg',
    'skills':{
        'Athletics':35,'Sneak':15,'Unarmed Combat':25,
        'Own Language':75,'Bargain':35,'Fast Talk':22,'Psychology':28,
        'Chemistry':48,'Computers':60,'Emergency Treatment':45,
        'Engineering':80,'History':30,'Mathematics':65,'Physics':55,
        'Planetology':35,'Repair':75,'Strategy':38,
        'Handgun Energy':45,'Observe':45,'Search':40,'Listen':35,
        'Aquatic Vehicle':15,'Atmospheric Craft':55,'Ground Vehicle':55,
        'Hyperdrive':40,'Personal Flyer':25,'Reaction Drive':48,
        'Reactionless Drive':72,'Ringworld':8,'Weapons System':45,
    },
    'weapons':[
        ('Flashlight-Laser','45%','2D6+2','25 / 100 / 500m','Cutting/defence'),
        ('Gravity Planer','50%','3D6','5 / 20m cone','Tool; area effect'),
    ],
    'equip':["Engineer's toolkit",'Portable power cell','Flashlight-laser',
             'Gravity planer','Diagnostic scanner','Hard environment suit'],
    'equip_detail':["Engineer's toolkit (full)",'Portable power cell (2)',
                    'Flashlight-laser','Gravity planer (engineering tool)',
                    'Diagnostic scanner','Repair materials × 3',
                    'Hard environment suit','Comdisc'],
    'personality':[
        '"It\'s a power draw I don\'t recognise.',
        'That\'s a problem." Doesn\'t argue',
        'about what can\'t change. Does argue',
        'about what can. Loves the Ringworld.',
    ],
    'hook95':['Your Engineering immediately flags the Spire drawing power far beyond',
              'stated function. Science (Physics) + Computer crack the logs together.',
              'In Act Three, you can feed the system the structural data it needs.',
              '▸ KEY: Engineering · Science (Physics) + Computer · Pilot for exit'],
    'hook96':['The vault power draw is active. Engineering tells you it is running.',
              'Vorn\'s weather warning is your cue to calculate extraction windows.',
              'You\'ll be flying the landing craft home through whatever the storm is.',
              '▸ KEY: Engineering · Pilot for Act 3 extraction · Repair if needed'],
  },
  {
    'num':6,'name':'Sola Reyes',
    'role':'Survey Specialist · Navigator',
    'species':'Human · We Made It','context':'17 Ringworld survey missions',
    'acc':HexColor('#00cc55'),'acc_dark':HexColor('#006622'),
    'STR':'11','CON':'12','SIZ':'11','INT':'16','POW':'13','DEX':'13','APP':'14','EDU':'17',
    'hp':12,'move':'3m/impulse','db':'None','pp':'13',
    'portrait_path':'/home/claude/ChaosiumCon26/scenarios/art/event-96/portrait-sola-reyes.jpg',
    'skills':{
        'Athletics':50,'Sneak':30,'Hide':28,'Unarmed Combat':15,
        'Own Language':80,'Linguistics':35,'Bargain':35,'Psychology':28,'Fast Talk':22,
        'Astronomy':62,'Biology':40,'Botany':32,'Chemistry':22,
        'Computers':55,'Emergency Treatment':38,'History':45,
        'Mathematics':42,'Physics':30,'Planetology':70,'Research':65,
        'Strategy':28,'Zoology':45,
        'Handgun Energy':40,'Handgun Projectile':35,'Listen':58,
        'Observe':72,'Scent':18,'Search':65,'Track':55,
        'Aquatic Vehicle':22,'Atmospheric Craft':48,'Ground Vehicle':45,
        'Personal Flyer':35,'Repair':30,'Ringworld':22,
    },
    'weapons':[
        ('Sidearm Pistol','40%','1D8','20 / 80 / 250m','Standard survey issue'),
        ('Sonic Stunner','35%','Stun (non-lethal)','5 / 20 / 50m','Field non-lethal'),
    ],
    'equip':['Survey instruments (full kit)','Portable mapping unit',
             'Sidearm pistol','Sonic stunner','Geological sample kit','Climbing gear'],
    'equip_detail':['Survey instruments (full kit)','Portable mapping unit',
                    'Sidearm pistol','Sonic stunner','Emergency flare gun × 4',
                    'Geological sample kit','Climbing gear (20m line + gear)',
                    'Emergency shelter'],
    'personality':[
        '"That shouldn\'t be there." Doesn\'t',
        'talk much. Notices everything.',
        '17 Ringworld surveys. Still looks',
        'at the arc overhead every time.',
    ],
    'hook95':['The quiet zone is a perfect geometrical absence — nothing matches it.',
              'Your Awareness spots the overlapping footprints before anyone else.',
              'In Act Three the system\'s display of your data is cartographic.',
              '▸ KEY: Awareness · Navigation for zone tracking · Planetology'],
    'hook96':['Survival (Ringworld) is the crew\'s critical skill when weather drops.',
              'When Vorn gives the two-hour window, you calculate if it\'s achievable.',
              'Your Navigation makes you the extraction planner.',
              '▸ KEY: Survival (Ringworld) · Navigation · Awareness: Ghresh-Ka'],
  },
]

# ── Generate PDF ──────────────────────────────────────────────────────────────
out_path = '/home/claude/ChaosiumCon26/apps/ringworld-character-sheets/character-sheets.pdf'
c = rl_canvas.Canvas(out_path, pagesize=A4)
total = len(CHARACTERS) * 2

for i, char in enumerate(CHARACTERS):
    draw_front(c, char, i*2+1, total)
    c.showPage()
    draw_back(c, char, i*2+2, total)
    c.showPage()
    print(f"Done: {char['name']}")

c.save()
print(f"\nSaved: {out_path}")
import os
print(f"Size: {os.path.getsize(out_path):,} bytes")
