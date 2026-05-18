#!/usr/bin/env python3
"""Stormbringer: The Storm of Kelen's Pact — Character Sheet PDF v2 (with portraits)"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak,
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, Image as RLImage
)
from reportlab.platypus.flowables import Flowable

# ── COLOURS ────────────────────────────────────────────────────────────────
PARCHMENT      = colors.HexColor('#F2ECD8')
PARCHMENT_DARK = colors.HexColor('#E8DFC4')
CRIMSON        = colors.HexColor('#7A0000')
CRIMSON_LIGHT  = colors.HexColor('#9B1010')
GOLD           = colors.HexColor('#8B6914')
GOLD_LIGHT     = colors.HexColor('#C49A1A')
INK            = colors.HexColor('#1A1008')
INK_LIGHT      = colors.HexColor('#3D2B10')
SHADOW         = colors.HexColor('#1A0808')
RULE_COLOR     = colors.HexColor('#6B4C1A')
DEMON_BG       = colors.HexColor('#1A0A08')
DEMON_BORDER   = colors.HexColor('#8B0000')
STAT_HEADER    = colors.HexColor('#4A0A0A')
STAT_ROW       = colors.HexColor('#F8F2E4')
STAT_ALT       = colors.HexColor('#EDE4CE')
WHITE          = colors.white

PAGE_W, PAGE_H = A4
MARGIN = 17 * mm

# ── IMAGE PATHS ─────────────────────────────────────────────────────────────
IMG_BASE = '/mnt/user-data/uploads/'
PORTRAITS = {
    'Davin Kell':              IMG_BASE + 'slaguru6666_Portrait_of_a_mercenary_warrior_Ilmioran_mid-thir_8f2350d5-3c94-427c-8a15-907aca7f9bef_0_Medium.jpeg',
    'Ysolde of Vilmir':        IMG_BASE + 'slaguru6666_Portrait_of_a_young_Vilmirian_woman_scholar-sorce_9eafe360-7808-4b56-80ae-0b1acd8c1e21_1_Medium.jpeg',
    'Cray':                    IMG_BASE + 'slaguru6666_Portrait_of_a_young_woman_thief_from_Nadsokor_the_07aa47cd-ad56-4fe6-b277-9c81d5861791_0_Medium.jpeg',
    'Sarath the Twice-Turned': IMG_BASE + 'slaguru6666_Portrait_of_a_heavyset_man_in_his_forties_Pan_Tan_d937185c-9eed-4bbc-9b69-8cb28eb5882c_2_Medium.jpeg',
    'Captain Brenn':           IMG_BASE + 'slaguru6666_Portrait_of_a_Tarkeshite_sea_captain_late_thirtie_a95be513-e159-4beb-ba5e-522c1024ad50_2_Medium.jpeg',
    'Lian':                    IMG_BASE + 'slaguru6666_Portrait_of_a_young_Ilmioran_devotee_of_Law_mid-t_098976e0-2bbc-47cd-8dd0-2552786a2bac_1_Medium.jpeg',
}
IMG_RATIO = 640 / 427  # height/width

# ── STYLES ──────────────────────────────────────────────────────────────────
def make_styles():
    return {
        'doc_title':       ParagraphStyle('doc_title', fontName='Times-BoldItalic', fontSize=28, textColor=CRIMSON, alignment=TA_CENTER, leading=34, spaceAfter=4),
        'doc_subtitle':    ParagraphStyle('doc_subtitle', fontName='Times-Italic', fontSize=13, textColor=GOLD, alignment=TA_CENTER, leading=18, spaceAfter=2),
        'doc_byline':      ParagraphStyle('doc_byline', fontName='Helvetica', fontSize=9, textColor=INK_LIGHT, alignment=TA_CENTER, leading=13),
        'cover_char_name': ParagraphStyle('cover_char_name', fontName='Times-Bold', fontSize=11, textColor=INK, leading=16),
        'toc_sub':         ParagraphStyle('toc_sub', fontName='Helvetica', fontSize=9, textColor=GOLD, leading=13),
        'rules_head':      ParagraphStyle('rules_head', fontName='Times-Bold', fontSize=10, textColor=CRIMSON, alignment=TA_CENTER, leading=14, spaceBefore=4, spaceAfter=3),
        'cover_note':      ParagraphStyle('cover_note', fontName='Times-Italic', fontSize=9, textColor=INK_LIGHT, alignment=TA_CENTER, leading=13),
        'body':            ParagraphStyle('body', fontName='Times-Roman', fontSize=9, textColor=INK, leading=13, spaceAfter=3, alignment=TA_JUSTIFY),
        'body_sm':         ParagraphStyle('body_sm', fontName='Times-Roman', fontSize=8, textColor=INK, leading=11, spaceAfter=2, alignment=TA_JUSTIFY),
        'demon_title':     ParagraphStyle('demon_title', fontName='Times-BoldItalic', fontSize=11, textColor=GOLD_LIGHT, leading=14, spaceBefore=1),
        'demon_label':     ParagraphStyle('demon_label', fontName='Helvetica-Bold', fontSize=7.5, textColor=GOLD_LIGHT, leading=11, spaceAfter=1),
        'demon_body':      ParagraphStyle('demon_body', fontName='Times-Roman', fontSize=8.5, textColor=colors.HexColor('#E8D8C0'), leading=12, spaceAfter=2, alignment=TA_JUSTIFY),
        'hook_label':      ParagraphStyle('hook_label', fontName='Helvetica-Bold', fontSize=8, textColor=CRIMSON, leading=11),
        'hook_body':       ParagraphStyle('hook_body', fontName='Times-Italic', fontSize=8.5, textColor=INK, leading=12, spaceAfter=2, alignment=TA_JUSTIFY),
        'quote':           ParagraphStyle('quote', fontName='Times-Italic', fontSize=9, textColor=CRIMSON_LIGHT, alignment=TA_CENTER, leading=13, spaceBefore=3),
        'italic_sm':       ParagraphStyle('italic_sm', fontName='Times-Italic', fontSize=8, textColor=INK_LIGHT, leading=11, alignment=TA_JUSTIFY),
        'portrait_name':   ParagraphStyle('portrait_name', fontName='Times-BoldItalic', fontSize=7.5, textColor=GOLD_LIGHT, alignment=TA_CENTER, leading=10),
    }

# ── CUSTOM FLOWABLES ────────────────────────────────────────────────────────
class OrnamentalRule(Flowable):
    def __init__(self, width, color=GOLD):
        super().__init__()
        self._c = color
        self.width  = width
        self.height = 8
    def wrap(self, aW, aH): return (self.width, self.height)
    def draw(self):
        c = self.canv
        c.setFillColor(self._c); c.setStrokeColor(self._c); c.setLineWidth(0.5)
        mid = self.width / 2
        c.line(0, 4, mid-8, 4); c.line(mid+8, 4, self.width, 4)
        for x in [0, mid, self.width]:
            c.saveState(); c.translate(x,4); c.rotate(45)
            c.rect(-2.5,-2.5,5,5,fill=1,stroke=0); c.restoreState()

class CharacterHeader(Flowable):
    def __init__(self, name, archetype, nationality, allegiance, width):
        super().__init__()
        self._n=name; self._arc=archetype; self._nat=nationality; self._all=allegiance
        self.width=width; self.height=52
    def wrap(self, aW, aH): return (self.width, self.height)
    def draw(self):
        c=self.canv; w,h=self.width,self.height
        c.setFillColor(SHADOW); c.roundRect(0,0,w,h,3,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#3A0808')); c.roundRect(2,2,w-4,h-4,2,fill=1,stroke=0)
        c.setStrokeColor(GOLD); c.setLineWidth(1.0); c.roundRect(1,1,w-2,h-2,3,fill=0,stroke=1)
        c.setStrokeColor(CRIMSON); c.setLineWidth(0.4); c.line(12,h-30,w-12,h-30)
        c.setFillColor(WHITE); c.setFont('Times-BoldItalic',20); c.drawString(12,h-22,self._n)
        c.setFillColor(GOLD_LIGHT); c.setFont('Helvetica',8.5)
        c.drawString(12,h-38,f"{self._arc}  \u00b7  {self._nat}")
        c.setFillColor(colors.HexColor('#C8A870')); c.setFont('Helvetica',7.5)
        c.drawRightString(w-10,h-38,f"Allegiance: {self._all}")
        c.setFillColor(GOLD)
        for cx,cy in [(6,h-6),(w-6,h-6),(6,6),(w-6,6)]:
            c.saveState(); c.translate(cx,cy); c.rotate(45)
            c.rect(-2,-2,4,4,fill=1,stroke=0); c.restoreState()

class StatBlock(Flowable):
    def __init__(self, stats, derived, width):
        super().__init__()
        self._s=stats; self._d=derived; self.width=width; self.height=56
    def wrap(self, aW, aH): return (self.width, self.height)
    def draw(self):
        c=self.canv; w=self.width; n=len(self._s); bw=(w-4)/n
        for i,(label,val) in enumerate(self._s):
            x=i*bw+2
            c.setFillColor(STAT_HEADER); c.rect(x,22,bw-1,12,fill=1,stroke=0)
            c.setFillColor(PARCHMENT_DARK); c.rect(x,8,bw-1,14,fill=1,stroke=0)
            c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.5); c.rect(x,8,bw-1,26,fill=0,stroke=1)
            c.setFillColor(GOLD_LIGHT); c.setFont('Helvetica-Bold',7)
            c.drawCentredString(x+(bw-1)/2,28,label)
            c.setFillColor(INK); c.setFont('Times-Bold',13)
            c.drawCentredString(x+(bw-1)/2,11,str(val))
        x_pos=2
        for lbl,val in self._d:
            c.setFillColor(CRIMSON); c.setFont('Helvetica-Bold',7.5)
            c.drawString(x_pos,1,lbl+": ")
            tw=c.stringWidth(lbl+": ",'Helvetica-Bold',7.5)
            c.setFillColor(INK); c.setFont('Times-Bold',7.5)
            c.drawString(x_pos+tw,1,str(val))
            x_pos+=tw+c.stringWidth(str(val),'Times-Bold',7.5)+12

class SectionBanner(Flowable):
    def __init__(self, text, width, bg=STAT_HEADER):
        super().__init__()
        self._t=text; self._bg=bg; self.width=width; self.height=16
    def wrap(self, aW, aH): return (self.width, self.height)
    def draw(self):
        c=self.canv
        c.setFillColor(self._bg); c.rect(0,0,self.width,16,fill=1,stroke=0)
        c.setStrokeColor(GOLD); c.setLineWidth(0.5); c.rect(0,0,self.width,16,fill=0,stroke=1)
        c.setFillColor(WHITE); c.setFont('Times-Bold',9.5); c.drawString(8,4.5,self._t.upper())

class HitPointTrack(Flowable):
    """Row of numbered HP boxes the player crosses off during play."""
    BOX = 15
    GAP = 3

    def __init__(self, max_hp, width):
        super().__init__()
        self.max_hp = max_hp
        self.width  = width
        bpr         = int(width / (self.BOX + self.GAP))
        self.bpr    = bpr
        self.rows   = (max_hp + bpr - 1) // bpr
        self.height = 18 + self.rows * (self.BOX + 10 + self.GAP)

    def wrap(self, aW, aH): return (self.width, self.height)

    def draw(self):
        c=self.canv; B,G=self.BOX,self.GAP
        max_hp=self.max_hp; bpr=self.bpr; w=self.width
        top=self.height-2

        # label row
        c.setFillColor(CRIMSON); c.setFont('Times-Bold',9)
        c.drawString(0,top-12,"HIT POINTS")
        c.setFillColor(GOLD); c.setFont('Helvetica-Bold',8)
        c.drawRightString(w,top-12,f"MAX  {max_hp}")
        c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4)
        c.line(0,top-15,w,top-15)

        y_start=top-18
        for i in range(max_hp):
            row=i//bpr; col=i%bpr
            items_in_row=min(bpr,max_hp-row*bpr)
            row_total_w=items_in_row*(B+G)-G
            start_x=(w-row_total_w)/2
            x=start_x+col*(B+G)
            y=y_start-row*(B+10+G)
            hp_val=max_hp-i

            # shadow
            c.setFillColor(colors.HexColor('#C8A870'))
            c.rect(x+1,y-1,B,B,fill=1,stroke=0)
            # box
            c.setFillColor(PARCHMENT); c.setStrokeColor(CRIMSON); c.setLineWidth(0.9)
            c.rect(x,y,B,B,fill=1,stroke=1)
            # corner tick marks
            c.setStrokeColor(colors.HexColor('#D0B090')); c.setLineWidth(0.3); tick=3
            c.line(x,y+B-tick,x+tick,y+B-tick); c.line(x,y,x+tick,y)
            c.line(x+B-tick,y+B,x+B,y+B);      c.line(x+B-tick,y,x+B,y)
            # number
            c.setFillColor(INK_LIGHT); c.setFont('Helvetica-Bold',7)
            c.drawCentredString(x+B/2,y+(B-6)/2,str(hp_val))

        # milestone labels (every 5)
        for i in range(max_hp):
            hp_val=max_hp-i
            if hp_val%5==0:
                row=i//bpr; col=i%bpr
                items_in_row=min(bpr,max_hp-row*bpr)
                row_total_w=items_in_row*(B+G)-G
                start_x=(w-row_total_w)/2
                x=start_x+col*(B+G)
                y=y_start-row*(B+10+G)
                c.setFillColor(GOLD); c.setFont('Helvetica',5.5)
                c.drawCentredString(x+B/2,y-7,str(hp_val))

class BackPageHeader(Flowable):
    """Slim banner for the back page — identifies the character sheet."""
    def __init__(self, name, archetype, width):
        super().__init__()
        self._n=name; self._arc=archetype; self.width=width; self.height=28
    def wrap(self, aW, aH): return (self.width, self.height)
    def draw(self):
        c=self.canv; w,h=self.width,self.height
        c.setFillColor(SHADOW); c.roundRect(0,0,w,h,3,fill=1,stroke=0)
        c.setStrokeColor(GOLD); c.setLineWidth(0.8)
        c.roundRect(1,1,w-2,h-2,2,fill=0,stroke=1)
        c.setFillColor(WHITE); c.setFont('Times-BoldItalic',14)
        c.drawString(10,h-19,self._n)
        nw=c.stringWidth(self._n,'Times-BoldItalic',14)
        c.setFillColor(GOLD_LIGHT); c.setFont('Helvetica',8)
        c.drawString(14+nw,h-18,f"\u00b7  {self._arc}  \u00b7  Background & Notes")
        c.setFillColor(GOLD)
        for cx,cy in [(5,h-5),(w-5,h-5),(5,5),(w-5,5)]:
            c.saveState(); c.translate(cx,cy); c.rotate(45)
            c.rect(-1.5,-1.5,3,3,fill=1,stroke=0); c.restoreState()

class NotesBlock(Flowable):
    """Blank ruled lines for player notes."""
    def __init__(self, width, lines=6):
        super().__init__()
        self.width=width; self.lines=lines; self.height=lines*16+4
    def wrap(self, aW, aH): return (self.width, self.height)
    def draw(self):
        c=self.canv; c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4)
        for i in range(self.lines):
            y=self.height-(i+1)*16+4; c.line(0,y,self.width,y)

# ── PAGE BACKGROUNDS ─────────────────────────────────────────────────────────
def draw_cover_bg(c, doc):
    c.saveState(); w,h=A4
    c.setFillColor(colors.HexColor('#241008')); c.rect(0,0,w,h,fill=1,stroke=0)
    c.setFillColor(PARCHMENT); c.roundRect(20,20,w-40,h-40,5,fill=1,stroke=0)
    c.setStrokeColor(colors.HexColor('#DDD0B0')); c.setLineWidth(0.15)
    for y in range(20,int(h)-20,7): c.line(20,y,w-20,y)
    c.setFillColor(CRIMSON)
    c.rect(20,h-90,w-40,70,fill=1,stroke=0); c.rect(20,20,w-40,50,fill=1,stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(2.0); c.roundRect(20,20,w-40,h-40,5,fill=0,stroke=1)
    c.setLineWidth(0.6); c.roundRect(25,25,w-50,h-50,3,fill=0,stroke=1)
    c.setLineWidth(1.0)
    for y in [h-90,h-20,70,20]: c.line(20,y,w-20,y)
    c.restoreState()

def draw_page_bg(c, doc):
    c.saveState(); w,h=A4
    c.setFillColor(PARCHMENT); c.rect(0,0,w,h,fill=1,stroke=0)
    c.setStrokeColor(colors.HexColor('#DDD0B0')); c.setLineWidth(0.2)
    for y in range(0,int(h),8): c.line(0,y,w,y)
    c.setStrokeColor(RULE_COLOR); c.setLineWidth(1.5); c.rect(8,8,w-16,h-16,fill=0,stroke=1)
    c.setStrokeColor(GOLD); c.setLineWidth(0.4); c.rect(11,11,w-22,h-22,fill=0,stroke=1)
    c.setFont('Times-Italic',8); c.setFillColor(INK_LIGHT)
    c.drawCentredString(w/2,14,"The Storm of Kelen's Pact  \u00b7  Stormbringer 1st Edition  \u00b7  ChaosiumCon 2026")
    c.restoreState()

# ── CHARACTER DATA ────────────────────────────────────────────────────────────
CHARS = [
  { 'name':'Davin Kell','archetype':'The Mercenary','nationality':'Ilmioran','allegiance':'Balance 12 / Law 4 / Chaos 3',
    'physical':'Mid-thirties. Broad-shouldered. Close-cropped dark hair going grey at the temples. A jaw scar from a Tarkeshite blade. Moves with the economical stillness of someone who has stopped making fights look dramatic.',
    'stats':[('STR','15'),('CON','14'),('SIZ','14'),('INT','11'),('POW','12'),('DEX','14'),('APP','11')],
    'derived':[('HP','16'),('MP','12'),('DB','+1D4'),('SR','28'),('Move','10')],
    'skills':[('Broadsword (ATK)','65%'),('Broadsword (PAR)','55%'),('Shield (PAR)','55%'),('Dagger (ATK)','40%'),('Dodge','55%'),('Spot Hidden','45%'),('Listen','40%'),('Search','35%'),('Ride','50%'),('Climb','50%'),('Jump','40%'),('First Aid','35%'),('Evaluate Treasure','30%'),('Bargain','30%'),('Track','25%'),('Insight','35%'),('World Lore','25%'),('Stealth','20%')],
    'equipment':['Broadsword (1D8+1+DB) — heavy, well-balanced, scratched but not nicked','Dagger (1D4+2) — belt-worn','Medium shield (+20% parry bonus)','Chainmail hauberk (armour 1D6-1)','Three days trail rations','Purse: 3 silver + 8 copper emergency money','Kelen\'s half-pay receipt in boot — four silver owed'],
    'demon_name':'"Cold Comfort"','demon_type':'Demon of Combat — bound in the broadsword crossguard',
    'demon_stats':'STR 13 | POW 12 | INT 5',
    'demon_abilities':[('+1D4 damage','On attack rolls succeeding by 20% or more.'),('Deflect (1/combat)','Negates one hit against Davin — no parry roll. Attacker re-rolls. Cold shock up the arm.'),('Early warning','Crossguard is cold when living enemies are within ten yards.'),('Cost','After Deflect: -10% to all non-combat skill rolls for the remainder of the scene.')],
    'demon_note':'Davin believes the sword is merely lucky. Won it in a dice game. Does not know it is demon-bound.',
    'background':'Ten years in a Lormyrian mercenary company, disbanded after a catastrophic contract dispute. Five years freelancing the Eastern Marches since. Not complicated — good at fighting, decided that is enough of a life. Six months ago Kelen hired him to escort supplies to the moor treeline, paid half, and never came back.',
    'hook':'Davin is owed four silver by Kelen. He took this job to collect — and because something is wrong out there and he was part of getting it started.',
    'quote':'"I\'ll need the rest of the silver when it\'s done. That was the arrangement."'},

  { 'name':'Ysolde of Vilmir','archetype':'The Scholar-Sorcerer','nationality':'Vilmirian','allegiance':'Balance 8 / Law 10 / Chaos 1',
    'physical':'Late twenties. Precise and angular. Hair pinned back with functional iron clips. Ink-stained fingers. Catalogues everything, including catastrophes, as they happen.',
    'stats':[('STR','9'),('CON','11'),('SIZ','10'),('INT','16'),('POW','16'),('DEX','12'),('APP','13')],
    'derived':[('HP','11'),('MP','16'),('DB','None'),('SR','22'),('Move','10')],
    'skills':[('Knife (ATK)','30%'),('Knife (PAR)','25%'),('Dodge','36%'),('Summon Demon','45%'),('Bind Demon','40%'),('Banish Demon','35%'),('Lore (Melnibonean)','65%'),('Lore (Demon)','60%'),('Lore (Young Kingdoms)','55%'),('Read/Write (High Speech)','70%'),('Read/Write (Low Speech)','60%'),('Insight','60%'),('Bargain','55%'),('Persuade','45%'),('Spot Hidden','45%'),('Evaluate Treasure','45%'),('First Aid','30%'),('Swim','25%')],
    'equipment':['Knife (1D4) — a scholar\'s tool, barely a weapon','Scroll-case with three years of research notes','Ritual component kit (+10% to one summoning/binding attempt, single use)','Inkhorn, three quills, spare vellum','Reading glass (brass-framed magnifying lens)','Two candles and a tinderbox','Purse: 5 silver','Small leather journal: notes from six field sites'],
    'demon_name':'"The Copper Mirror"','demon_type':'Demon of Knowledge (Intellect) — bound in a small hand mirror',
    'demon_stats':'INT 16 | POW 10 | CHA 8',
    'demon_abilities':[('One question/session','Answers truthfully on Melnibonean history, demon lore, magical theory, or entities observed.'),('The second truth','Always volunteers one additional truth not asked for. GM chooses — it will be relevant.'),('Visions','Reflection sometimes shows scenes from the past rather than the present.'),('+ 15% Lore','While consulting the mirror, all Lore rolls in that scene gain +15%.')],
    'demon_note':'Ysolde bound it herself under supervision. She calls it Pellucid — a name she does not share.',
    'background':'Minor Vilmirian nobility. Recruited into academic sorcery at nineteen. Specialism: Melnibonean material culture. Has researched the Spire for three years. Automatically succeeds on Lore rolls about the Spire, Melnibonean binding techniques, or the demon Vorak — no roll required.',
    'hook':'Ysolde has researched this Spire for three years. This is fieldwork as much as altruism. She will document everything — including her own terror, which she will not name as such.',
    'quote':'"I need you to describe exactly what you saw. Every detail. Don\'t edit for impact."'},

  { 'name':'Cray','archetype':'The Cutpurse','nationality':'Nadsokor (Beggar Kingdom)','allegiance':'Balance 14 / Law 3 / Chaos 6',
    'physical':'Compact and quick. Looks younger than she is. Dark eyes that move independently of her face. The kind of stillness that is not peace but readiness.',
    'stats':[('STR','10'),('CON','12'),('SIZ','9'),('INT','14'),('POW','12'),('DEX','17'),('APP','11')],
    'derived':[('HP','12'),('MP','12'),('DB','None'),('SR','26'),('Move','11')],
    'skills':[('Dagger (ATK)','55%'),('Dagger (PAR)','45%'),('Dodge','51%'),('Stealth','70%'),('Hide','65%'),('Pick Lock','65%'),('Fast Talk','65%'),('Bargain','45%'),('Spot Hidden','60%'),('Listen','55%'),('Sleight of Hand','60%'),('Climb','55%'),('Jump','50%'),('Swim','40%'),('Evaluate Treasure','50%'),('Search','40%'),('Insight','50%'),('Track','30%')],
    'equipment':['Two daggers (1D4+2 each) — kept sharp, balance-tested','Lockpick set (seven picks, two tension bars, oiled leather)','Dark wool cloak','30ft braided rope','Small copper mirror (for looking around corners)','12 silver hidden in left boot heel / 3 silver decoy in belt pouch','A piece of blue-and-grey woven fabric inside her jacket — shown to no one'],
    'demon_name':'"The Black Pins"','demon_type':'Demon of Stealth — bound across five iron hairpins',
    'demon_stats':'DEX 15 | INT 9 | POW 8',
    'demon_abilities':[('+20% Stealth (passive)','Stealth 70% becomes 90% while pins are worn.'),('Silent movement (1/session)','Complete silence for 10 rounds regardless of surface. No roll required.'),('Warmth warning','Pins feel slightly warm when someone is actively searching for Cray.'),('Cost — memory bleed','Occasionally hears one word from the dead woman who owned them. Not yet connected to the pins.')],
    'demon_note':'Cray does not know the pins are demon-bound. She believes they simply help her move quietly.',
    'background':'Grew up in Nadsokor. Left at seventeen, has been moving ever since. Freelance information broker, courier, occasional retrieval specialist. Three months ago, Sevel vanished near the Eastern Moors. She connected this to Kelen. Nobody else has.',
    'hook':'[PRIVATE] Cray knew Sevel — Tally\'s older brother. He vanished near the moors three months ago. She is not here for the money. In the Binding Hall she finds fabric from his cloak — tell her privately.',
    'quote':'"I\'m not here for reasons. I\'m here for the money. Can we move on?"'},

  { 'name':'Sarath the Twice-Turned','archetype':'The Former Cultist','nationality':'Pan Tang-born, self-exiled','allegiance':'Balance 16 / Law 11 / Chaos 14',
    'physical':'Forties. Heavyset. Greying beard. Faded Chaos-brand of the Cult of Xiombarg on his left forearm — never tried to remove it, which people find unsettling.',
    'stats':[('STR','11'),('CON','13'),('SIZ','11'),('INT','15'),('POW','15'),('DEX','12'),('APP','10')],
    'derived':[('HP','13'),('MP','15'),('DB','None'),('SR','23'),('Move','10')],
    'skills':[('Scimitar (ATK)','50%'),('Scimitar (PAR)','45%'),('Dagger (ATK)','40%'),('Dodge','45%'),('Lore (Chaos)','70%'),('Lore (Demon)','65%'),('Summon Demon','50%'),('Bind Demon','35%'),('Banish Demon','40%'),('Insight','60%'),('Spot Hidden','45%'),('Listen','40%'),('Persuade','40%'),('World Lore','50%'),('Read/Write (High Speech)','55%'),('First Aid','35%'),('Stealth','30%'),('Climb','40%')],
    'equipment':['Scimitar (1D8+1) — Melnibonean manufacture, old, obsessively maintained','Dagger (1D4+2) — concealed in boot','Leather armour, well-fitted (armour 1D6-2)','Demon-binding scroll (ONE USE): binds demon POW 15 or lower, costs 1D4 permanent POW','Small clay pot of lamp oil','Purse: 4 silver / pewter flask of good spirits','Iron bracelet on left wrist — see demon item'],
    'demon_name':'"The Chain of Regret"','demon_type':'Demon of Warding (Balance-aligned) — bound in an iron bracelet',
    'demon_stats':'CON 14 | POW 13 | STR 10',
    'demon_abilities':[('+2 armour (passive)','Bracelet provides 2 points of armour to the arm. Stacks with worn armour.'),('Negate corruption (1/scenario)','Negates one Chaos corruption or possession attempt. POW 13 vs effect\'s POW. Burning sensation.'),('Cannot be removed','Bind Demon roll (35%) required. The demon refuses, politely. He has tried twice.'),('Cost — witness','The demon knows everything Sarath has done since he put it on. It has never commented. He finds this worse than judgment.')],
    'demon_note':'Sarath knows everything about the bracelet. A Balance-aligned sorcerer gave it to him in Tanelorn six years ago.',
    'background':'Raised in Pan Tang\'s administered territories. Joined the Cult of Xiombarg at twenty-three. Served eleven years. His cult-master performed a binding that went wrong. The demon did not unmake the man quickly. Sarath watched for four hours. Left that evening.',
    'hook':'[PRIVATE] Sarath recognises the storm pattern as a failed high-grade binding — no roll required. He knows more about Vorak than he has admitted. His binding scroll is a last resort: 1D4 permanent POW. Let the player decide.',
    'quote':'"I\'m not going to tell you what I\'ve done. I\'ll tell you what I know. They are not the same thing."'},

  { 'name':'Captain Brenn','archetype':'The Sailor','nationality':'Tarkeshite','allegiance':'Balance 10 / Law 6 / Chaos 4',
    'physical':'Late thirties. Weathered. Rope-burned palms. A Tarkeshite merchant\'s ring on his right hand. The ship sank two years ago — he kept the ring.',
    'stats':[('STR','13'),('CON','15'),('SIZ','13'),('INT','12'),('POW','11'),('DEX','13'),('APP','12')],
    'derived':[('HP','16'),('MP','11'),('DB','+1D4'),('SR','26'),('Move','10')],
    'skills':[('Cutlass (ATK)','60%'),('Cutlass (PAR)','50%'),('Dagger (ATK)','45%'),('Dodge','39%'),('Navigate','65%'),('Spot Hidden','55%'),('Listen','50%'),('Climb','55%'),('Swim','70%'),('Jump','50%'),('Persuade','50%'),('Bargain','45%'),('Fast Talk','35%'),('Evaluate Treasure','35%'),('First Aid','40%'),('World Lore','40%'),('Track','25%'),('Stealth','20%')],
    'equipment':['Cutlass (1D8+DB) — working sailor\'s blade, balanced for one hand','Pistol crossbow (1D6, 10 yards, 3 bolts — re-cock after each shot)','Dagger (1D4+2)','Heavy leather coat (armour 1D6-2)','Flask of Tarkeshite spirits — half-full / coiled 50ft rope','Gold merchant\'s ring — right hand','Purse: 6 silver (negotiated a better rate than the others)'],
    'demon_name':'"The True Compass"','demon_type':'Demon of Seeking (Intellect) — bound in a brass nautical compass',
    'demon_stats':'INT 13 | POW 11 | DEX 9',
    'demon_abilities':[('True north (passive)','Accurate through magical interference and underground. No roll for standard navigation.'),('Seeking','Concentrate 1 round. Points toward what Brenn most WANTS to find — not what he asks for.'),('Range','Approximately one mile in the open; less through stone.'),('Cost — honesty','Two years ago it pointed toward the sea, not his drowning crew. He found four. He lost twelve.')],
    'demon_note':'Brenn knows the navigation function. He suspects the seeking function works on principles he does not understand. He is right to be cautious about what he most wants.',
    'background':'Captained a Tarkeshite merchant vessel for twelve years. It sank two years ago in a storm that had no reason to exist where it did. Got four crew out. Left twelve. Not broken — changed. Working short-haul river contracts since.',
    'hook':'Brenn has already decided this situation is not manageable. He will stay because someone will need to carry an injured person out, and he is the most capable here. He has accepted this without being asked.',
    'quote':'"Tell me where we\'re going. I\'ll figure out the rest when we get there."'},

  { 'name':'Lian','archetype':'The Devotee of Law','nationality':'Ilmioran','allegiance':'Law 18 / Balance 4 / Chaos 0',
    'physical':'Mid-twenties. Earnest expression. Short-cropped hair. White travel cloak with Law sigil embroidered at the hem. Looks too young for this. Is too young for this.',
    'stats':[('STR','10'),('CON','12'),('SIZ','10'),('INT','14'),('POW','14'),('DEX','13'),('APP','14')],
    'derived':[('HP','12'),('MP','14'),('DB','None'),('SR','23'),('Move','10')],
    'skills':[('Spear (ATK)','45%'),('Spear (PAR)','40%'),('Dagger (ATK)','30%'),('Dodge','39%'),('Insight','65%'),('Healing','55%'),('Persuade','50%'),('Oratory','45%'),('Spot Hidden','50%'),('Listen','45%'),('Search','40%'),('World Lore','50%'),('Lore (Law)','60%'),('Lore (Chaos)','35%'),('First Aid','45%'),('Read/Write (Low Speech)','55%'),('Read/Write (High Speech)','40%'),('Divine Intervention','25%')],
    'equipment':['Spear (1D8+1) — standard infantry, silver-chased socket (decorative)','Dagger (1D4+2)','White travel cloak with silver Law sigil at hem','White-and-silver Law medallion (worn openly): +10% Insight vs Chaos corruption','Healer\'s kit: 3 uses, 1D6 HP each — requires uninterrupted attention + Healing roll','Two days preserved rations / small journal of prayers and field notes','Purse: 4 silver (Church per diem, meticulously accounted)'],
    'demon_name':'"The Law\'s Lantern"','demon_type':'Demon of Order (NOT Chaos-aligned) — bound in a silver-and-brass lantern',
    'demon_stats':'POW 14 | INT 12 | CON 11',
    'demon_abilities':[('Undying flame (passive)','Cannot be extinguished by natural means — wind, rain, magical darkness.'),('Revelation','Chaos-tainted entities and objects emit faint blue luminescence in the lantern\'s light. Highly attuned beings (POW 16+) resist: POW vs POW 14.'),('Warding','Chaos entities approaching Lian must make POW vs POW 14 or feel strong reluctance (costs an action).'),('Cost — judgment','When Lian does something the demon considers contrary to Law, the lantern dims visibly. The GM\'s tool. Has happened twice already.')],
    'demon_note':'The Church calls this a "bound principle of order, not Chaos sorcery." Lian accepts this. Lian suspects the Church\'s answer may be convenient.',
    'background':'Born to a minor Ilmioran merchant family. Recruited into the Church\'s investigative branch at twenty-one. Genuine commitment — not institutional, actual. This is their first real field assignment. They prepared extensively. Preparation did not cover what Chaos actually smells like.',
    'hook':'[PRIVATE] Every resolution in Act Three compromises Law\'s principles. Lian carries the moral weight of the scenario. Divine Intervention (25%) is an emergency exit. Do not make it easy. Do not make it impossible.',
    'quote':'"Law\'s mercy. I didn\'t think it would — I prepared for difficult. This is something else."'},
]

# ── BUILD ─────────────────────────────────────────────────────────────────────
def build_pdf(path):
    S   = make_styles()
    UW  = PAGE_W - 2*MARGIN        # usable width  ~499pt
    LW  = UW * 0.615               # left col (stats/skills)
    RW  = UW * 0.385               # right col (portrait)
    SKH = (LW - 4*mm) / 2         # half-width for skill sub-cols

    doc = BaseDocTemplate(path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN+4*mm, bottomMargin=MARGIN+8*mm)

    cover_frame   = Frame(0, 0, PAGE_W, PAGE_H, id='cover')
    content_frame = Frame(MARGIN, MARGIN+8*mm, UW, PAGE_H-2*MARGIN-12*mm, id='content')
    doc.addPageTemplates([
        PageTemplate(id='cover',  frames=[cover_frame],   onPage=draw_cover_bg),
        PageTemplate(id='normal', frames=[content_frame], onPage=draw_page_bg),
    ])

    story = []

    # ── COVER ───────────────────────────────────────────────────────────────
    story.append(Spacer(1,72))
    story.append(Paragraph("THE STORM OF KELEN'S PACT", S['doc_title']))
    story.append(Spacer(1,6))
    story.append(Paragraph("Player Character Reference", S['doc_subtitle']))
    story.append(Spacer(1,4))
    story.append(Paragraph("Stormbringer  \u00b7  First Edition  \u00b7  ChaosiumCon 2026", S['doc_byline']))
    story.append(Spacer(1,14))
    story.append(OrnamentalRule(UW))
    story.append(Spacer(1,10))

    # Cover — portrait thumbnails at fixed compact size
    thumb_w = 95
    thumb_h = thumb_w * IMG_RATIO
    cover_rows = []
    for i in range(0, 6, 3):
        img_row = []
        for char in CHARS[i:i+3]:
            img = RLImage(PORTRAITS[char['name']], width=thumb_w, height=thumb_h)
            cell = Table([[img],[Paragraph(f"<b>{char['name']}</b>", S['portrait_name'])],
                                [Paragraph(char['archetype'], S['toc_sub'])]],
                         colWidths=[thumb_w])
            cell.setStyle(TableStyle([
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
                ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
            ]))
            img_row.append(cell)
        cover_rows.append(img_row)

    cover_grid = Table(cover_rows, colWidths=[UW/3]*3)
    cover_grid.setStyle(TableStyle([
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LINEBELOW',(0,0),(-1,0),0.5,RULE_COLOR),
    ]))
    story.append(cover_grid)
    story.append(Spacer(1,10))
    story.append(OrnamentalRule(UW))
    story.append(Spacer(1,8))

    story.append(Paragraph("COMBAT &amp; MECHANICS QUICK REFERENCE", S['rules_head']))
    rules = [['HP = CON +/- SIZ modifier','MP = POW','Dodge = DEX x 3%'],
             ['SIZ 9-12: no modifier | >12: +1/pt | <9: -1/pt','DB 2-12: -1D4  |  13-16: -1D2','DB 17-24: None'],
             ['Strike Rank = DEX + SIZ','DB 25-32: +1D4','DB 33-40: +1D6']]
    rlt = Table([[Paragraph(c, S['doc_byline']) for c in row] for row in rules],colWidths=[UW/3]*3)
    rlt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),PARCHMENT_DARK),('GRID',(0,0),(-1,-1),0.4,RULE_COLOR),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(rlt)
    story.append(Spacer(1,8))
    story.append(Paragraph("Hand out character sheets face-down. Let players choose by archetype — not by stats.", S['cover_note']))
    story.append(Spacer(1,3))
    story.append(Paragraph("GM: <b>Cray</b> and <b>Sarath</b> both have private hooks that change specific interactions.", S['cover_note']))

    story.append(NextPageTemplate('normal'))
    story.append(PageBreak())

    # ── CHARACTER PAGES (front + back per character) ─────────────────────────
    for char in CHARS:
        max_hp = int(next(v for k,v in char['derived'] if k=='HP'))

        # ── FRONT PAGE ──────────────────────────────────────────────────────
        story.append(CharacterHeader(char['name'], char['archetype'],
                                     char['nationality'], char['allegiance'], UW))
        story.append(Spacer(1,3))

        port_w  = RW - 4
        port_h  = port_w * IMG_RATIO
        portrait = RLImage(PORTRAITS[char['name']], width=port_w, height=port_h)

        sk = char['skills']
        if len(sk) % 2: sk = sk + [('','')]
        mid = len(sk)//2
        sk_rows = []
        for (la,lv),(ra,rv) in zip(sk[:mid], sk[mid:]):
            sk_rows.append([Paragraph(la,S['body_sm']),Paragraph(f"<b>{lv}</b>",S['body_sm']),
                            Paragraph(ra,S['body_sm']),Paragraph(f"<b>{rv}</b>",S['body_sm'])])
        skt = Table(sk_rows, colWidths=[SKH*0.72,SKH*0.28,SKH*0.72,SKH*0.28])
        skt.setStyle(TableStyle([
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[STAT_ROW,STAT_ALT]),
            ('LINEBELOW',(0,0),(-1,-1),0.3,RULE_COLOR),
            ('LINEAFTER',(1,0),(1,-1),0.6,RULE_COLOR),
            ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),3),
            ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),
            ('ALIGN',(1,0),(1,-1),'RIGHT'),('ALIGN',(3,0),(3,-1),'RIGHT'),
        ]))

        # Left col: stats + skills — physical description lives on back page
        left_items = [
            [SectionBanner("Characteristics", LW-4)],
            [Spacer(1,2)],
            [StatBlock(char['stats'], char['derived'], LW-4)],
            [Spacer(1,3)],
            [SectionBanner("Skills", LW-4)],
            [Spacer(1,2)],
            [skt],
        ]
        left_inner = Table(left_items, colWidths=[LW-4])
        left_inner.setStyle(TableStyle([
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
        ]))

        two_col = Table([[left_inner, portrait]], colWidths=[LW, RW])
        two_col.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
            ('ALIGN',(1,0),(1,-1),'RIGHT'),
            ('LINEBEFORE',(1,0),(1,-1),0.5,GOLD),
        ]))
        story.append(two_col)
        story.append(Spacer(1,4))

        # Equipment — 1pt row padding
        story.append(SectionBanner("Equipment", UW))
        story.append(Spacer(1,2))
        eqt = Table([[Paragraph(f"\u2022 {item}",S['body_sm'])] for item in char['equipment']], colWidths=[UW])
        eqt.setStyle(TableStyle([
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[STAT_ROW,STAT_ALT]),
            ('LINEBELOW',(0,0),(-1,-1),0.3,RULE_COLOR),
            ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),4),
            ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),
        ]))
        story.append(eqt)
        story.append(Spacer(1,4))

        # Demon item — tighter padding, no inner spacers
        story.append(SectionBanner("Demon-Bound Item", UW, bg=colors.HexColor('#3A0808')))
        story.append(Spacer(1,2))
        dc = [Paragraph(char['demon_name'],S['demon_title']),
              Paragraph(char['demon_type'],S['demon_label']),
              Paragraph(f"Demon char.:  {char['demon_stats']}",S['demon_body'])]
        for abn, abd in char['demon_abilities']:
            dc.append(Paragraph(f"<b>{abn}:</b>  {abd}",S['demon_body']))
        dc.append(Paragraph(f"<i>{char['demon_note']}</i>",S['demon_body']))
        di = Table([[el] for el in dc], colWidths=[UW-16])
        di.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DEMON_BG),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
        do = Table([[di]], colWidths=[UW])
        do.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),DEMON_BG),
            ('BOX',(0,0),(0,0),1.2,DEMON_BORDER),
            ('LEFTPADDING',(0,0),(0,0),8),('RIGHTPADDING',(0,0),(0,0),8),
            ('TOPPADDING',(0,0),(0,0),4),('BOTTOMPADDING',(0,0),(0,0),4)]))
        story.append(do)
        story.append(Spacer(1,5))

        # HP Track — no section banner (the Flowable draws its own label)
        story.append(HitPointTrack(max_hp, UW))

        story.append(PageBreak())

        # ── BACK PAGE ────────────────────────────────────────────────────────
        story.append(BackPageHeader(char['name'], char['archetype'], UW))
        story.append(Spacer(1,6))
        story.append(Paragraph(f"<i>{char['physical']}</i>", S['italic_sm']))
        story.append(Spacer(1,8))

        # Background
        story.append(SectionBanner("Background", UW))
        story.append(Spacer(1,5))
        story.append(Paragraph(char['background'], S['body']))
        story.append(Spacer(1,6))

        # Personal hook
        ht = Table([[Paragraph("PERSONAL HOOK:",S['hook_label']),
                     Paragraph(char['hook'],S['hook_body'])]],
                   colWidths=[26*mm, UW-26*mm])
        ht.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),PARCHMENT_DARK),
            ('BOX',(0,0),(-1,-1),0.8,CRIMSON),('LINEBEFORE',(0,0),(0,-1),3,CRIMSON),
            ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
            ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        story.append(ht)
        story.append(Spacer(1,8))

        # Quote
        story.append(OrnamentalRule(UW))
        story.append(Paragraph(char['quote'], S['quote']))
        story.append(OrnamentalRule(UW))
        story.append(Spacer(1,10))

        # Notes
        story.append(SectionBanner("Notes", UW))
        story.append(Spacer(1,6))
        story.append(NotesBlock(UW, lines=8))

        story.append(PageBreak())

    doc.build(story)
    print(f"Done: {path}")

build_pdf('/mnt/user-data/outputs/stormbringer-kelen-pact-characters-v3.pdf')
