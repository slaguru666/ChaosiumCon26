#!/usr/bin/env python3
"""BRP Character Sheets v2 — Night Crawler (Event 91) & Day One (Event 159)"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak,
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# ── FONTS ─────────────────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont('Rajdhani',      '/tmp/rajdhani-bold.ttf'))
pdfmetrics.registerFont(TTFont('ShareTechMono', '/tmp/sharetechmono.ttf'))

PAGE_W, PAGE_H = A4
MARGIN = 17 * mm
UW = PAGE_W - 2 * MARGIN          # ≈ 499 pt

# ═══════════════════════════════════════════════════════════════════════════════
# THEMES  — Every colour used on a light background is dark; every colour used
#           on a dark background is light. Cyan is ONLY used on dark BGs or as
#           a border/decorative element. Rule: if in doubt, go darker.
# ═══════════════════════════════════════════════════════════════════════════════

class T: pass   # theme namespace

def night_crawler_theme():
    t = T()
    t.name = 'nc'
    # ── Page ──
    t.page_bg         = colors.HexColor('#EDF1F7')   # cool light grey — clean, printable
    t.parchment       = colors.HexColor('#EDF1F7')
    t.parchment_dark  = colors.HexColor('#DFE5F0')
    # ── Header banner (dark) ──
    t.header_bg       = colors.HexColor('#050A14')
    t.header_inner    = colors.HexColor('#0B1428')
    t.header_border   = colors.HexColor('#00D4FF')   # cyan border on dark = fine
    t.header_name     = colors.white
    t.header_sub      = colors.HexColor('#7BDCFF')   # light cyan on dark = fine
    t.header_right    = colors.HexColor('#A8D8F0')
    # ── Section banners (dark) ──
    t.banner_bg       = colors.HexColor('#0D1A2E')
    t.banner_text     = colors.white
    t.banner_special  = colors.HexColor('#0A0520')   # darker purple-navy for augment
    # ── Stat characteristic boxes ──
    t.stat_hdr_bg     = colors.HexColor('#0D1A2E')   # dark header row
    t.stat_hdr_text   = colors.HexColor('#00D4FF')   # cyan text on dark = fine (16:1)
    t.stat_cell_bg    = colors.HexColor('#DFE5F0')   # light cell
    t.stat_cell_text  = colors.HexColor('#050A14')   # near-black on light = fine
    # ── Derived stats strip (dark strip so cyan is readable) ──
    t.derived_bg      = colors.HexColor('#0D1A2E')
    t.derived_label   = colors.HexColor('#00D4FF')   # cyan on dark = fine
    t.derived_val     = colors.white
    # ── Skill / equipment rows ──
    t.row1            = colors.HexColor('#EDF1F7')
    t.row2            = colors.HexColor('#DFE5F0')
    t.row_text        = colors.HexColor('#0A0F20')   # near-black on light = fine (13:1)
    t.rule            = colors.HexColor('#1E3A5F')
    # ── Augment box (very dark) ──
    t.special_bg      = colors.HexColor('#040810')
    t.special_border  = colors.HexColor('#0088CC')
    t.special_title   = colors.HexColor('#7BDCFF')   # light cyan on near-black = fine
    t.special_label   = colors.HexColor('#00B4E0')
    t.special_body    = colors.HexColor('#C0D8F0')   # light blue on near-black = fine
    # ── HP track ──
    t.hp_label        = colors.HexColor('#0D1A2E')   # dark navy on light page = fine (14:1)
    t.hp_max          = colors.HexColor('#0D1A2E')
    t.hp_box_fill     = colors.HexColor('#E4F0FF')   # very light blue
    t.hp_box_5th      = colors.HexColor('#B8D4F4')   # slightly darker for every-5th
    t.hp_box_border   = colors.HexColor('#0066AA')   # dark blue border = visible
    t.hp_num          = colors.HexColor('#050A14')   # near-black in box = fine
    # ── SAN track ──
    t.san_label       = colors.HexColor('#1A3020')
    t.san_box_fill    = colors.HexColor('#E4F4EA')
    t.san_box_5th     = colors.HexColor('#B4DCC0')
    t.san_box_border  = colors.HexColor('#1A7040')
    t.san_num         = colors.HexColor('#0A200F')
    # ── Portrait placeholder ──
    t.port_bg         = colors.HexColor('#0D1A2E')
    t.port_border     = colors.HexColor('#00D4FF')
    t.port_text       = colors.HexColor('#3A5878')   # dim text inside placeholder
    t.port_label      = colors.HexColor('#00D4FF')
    # ── Hook box (dark) ──
    t.hook_bg         = colors.HexColor('#0A1525')
    t.hook_border     = colors.HexColor('#0088CC')
    t.hook_bar        = colors.HexColor('#00D4FF')
    t.hook_label      = colors.HexColor('#00D4FF')   # cyan on dark = fine
    t.hook_body       = colors.HexColor('#C0D8F0')   # light on dark = fine
    # ── Back header (dark) ──
    t.back_bg         = colors.HexColor('#050A14')
    t.back_border     = colors.HexColor('#00D4FF')
    t.back_sub        = colors.HexColor('#7BDCFF')
    # ── Body/italic (on light page) ──
    t.body            = colors.HexColor('#0A0F20')   # near-black on light
    t.italic          = colors.HexColor('#2A3A50')   # dark blue-grey on light = fine (7:1)
    t.quote           = colors.HexColor('#0055AA')   # dark blue on light = fine (5:1)
    # ── Cover (dark cover page) ──
    t.cover_row1      = colors.HexColor('#0D1A2E')
    t.cover_row2      = colors.HexColor('#111E38')
    t.cover_name      = colors.white
    t.cover_arch      = colors.HexColor('#7BDCFF')   # light cyan on dark = fine
    t.cover_meta      = colors.HexColor('#A0C0E0')
    t.cover_note      = colors.HexColor('#A0C0E0')
    t.cover_title     = colors.HexColor('#00D4FF')   # cyan on dark = fine
    t.cover_sub       = colors.HexColor('#7BDCFF')
    t.cover_byline    = colors.HexColor('#A0C0E0')
    t.cover_rule_body = colors.white           # was #C0D8F0 — white ensures max contrast on dark rows
    t.accent          = colors.HexColor('#00D4FF')   # purely for borders/decorative
    t.footer          = colors.HexColor('#1E3A5F')
    t.footer_text     = "The Night Crawler  ·  BRP  ·  Event 91  ·  ChaosiumCon 2026"
    t.special_label_str = "AUGMENT"
    t.back_note       = "Neo-Ashford 2087  ·  Background & Notes"
    # ── Fonts ──
    t.font_head       = 'Rajdhani'
    t.font_body       = 'ShareTechMono'
    t.font_body_bold  = 'ShareTechMono'   # no bold variant; use caps instead
    return t

def day_one_theme():
    t = T()
    t.name = 'd1'
    t.page_bg         = colors.HexColor('#F3EDE3')
    t.parchment       = colors.HexColor('#F3EDE3')
    t.parchment_dark  = colors.HexColor('#E8E0D0')
    t.header_bg       = colors.HexColor('#141414')
    t.header_inner    = colors.HexColor('#1E1E1E')
    t.header_border   = colors.HexColor('#CC2200')
    t.header_name     = colors.white
    t.header_sub      = colors.HexColor('#FFAA90')
    t.header_right    = colors.HexColor('#FFCCBB')
    t.banner_bg       = colors.HexColor('#242424')
    t.banner_text     = colors.white
    t.banner_special  = colors.HexColor('#4A0800')
    t.stat_hdr_bg     = colors.HexColor('#242424')
    t.stat_hdr_text   = colors.HexColor('#FF9977')   # warm orange on dark = fine
    t.stat_cell_bg    = colors.HexColor('#E8E0D0')
    t.stat_cell_text  = colors.HexColor('#1A0808')
    t.derived_bg      = colors.HexColor('#242424')
    t.derived_label   = colors.HexColor('#FF9977')   # on dark = fine
    t.derived_val     = colors.white
    t.row1            = colors.HexColor('#F3EDE3')
    t.row2            = colors.HexColor('#E8E0D0')
    t.row_text        = colors.HexColor('#1A0808')
    t.rule            = colors.HexColor('#8B3300')
    t.special_bg      = colors.HexColor('#180808')
    t.special_border  = colors.HexColor('#CC2200')
    t.special_title   = colors.HexColor('#FFAA90')
    t.special_label   = colors.HexColor('#FF7755')
    t.special_body    = colors.HexColor('#FFD0C0')
    t.hp_label        = colors.HexColor('#5A0000')   # dark red on light = fine (7:1)
    t.hp_max          = colors.HexColor('#5A0000')
    t.hp_box_fill     = colors.HexColor('#FFF0EE')
    t.hp_box_5th      = colors.HexColor('#FFCCC0')
    t.hp_box_border   = colors.HexColor('#AA1100')
    t.hp_num          = colors.HexColor('#3A0808')
    t.san_label       = colors.HexColor('#1A3020')
    t.san_box_fill    = colors.HexColor('#F0F8F0')
    t.san_box_5th     = colors.HexColor('#C8E8C8')
    t.san_box_border  = colors.HexColor('#2A6040')
    t.san_num         = colors.HexColor('#0A200F')
    t.port_bg         = colors.HexColor('#242424')
    t.port_border     = colors.HexColor('#CC2200')
    t.port_text       = colors.HexColor('#5A4040')
    t.port_label      = colors.HexColor('#CC2200')
    t.hook_bg         = colors.HexColor('#F8EDE8')
    t.hook_border     = colors.HexColor('#CC2200')
    t.hook_bar        = colors.HexColor('#CC2200')
    t.hook_label      = colors.HexColor('#8B0000')   # dark red on very light = fine (8:1)
    t.hook_body       = colors.HexColor('#2A0808')   # near-black warm on light = fine
    t.back_bg         = colors.HexColor('#141414')
    t.back_border     = colors.HexColor('#CC2200')
    t.back_sub        = colors.HexColor('#FFAA90')
    t.body            = colors.HexColor('#1A0808')
    t.italic          = colors.HexColor('#4A2A20')
    t.quote           = colors.HexColor('#8B0000')   # dark red on light = fine
    t.cover_row1      = colors.HexColor('#2A2A2A')
    t.cover_row2      = colors.HexColor('#363636')
    t.cover_name      = colors.white
    t.cover_arch      = colors.HexColor('#FFAA90')
    t.cover_meta      = colors.HexColor('#D0C0B0')
    t.cover_note      = colors.HexColor('#D0C0B0')
    t.cover_title     = colors.HexColor('#CC2200')
    t.cover_sub       = colors.HexColor('#8B3300')
    t.cover_byline    = colors.HexColor('#2A2A2A')
    t.cover_rule_body = colors.white           # was #2A2A2A — was same as row bg, completely invisible!
    t.accent          = colors.HexColor('#CC2200')
    t.footer          = colors.HexColor('#8B3300')
    t.footer_text     = "Day One  ·  BRP  ·  Event 159  ·  ChaosiumCon 2026"
    t.special_label_str = "WHAT YOU KNOW"
    t.back_note       = "London, 17 May 2026  ·  Background & Notes"
    t.font_head       = 'Times-Bold'
    t.font_body       = 'Times-Roman'
    t.font_body_bold  = 'Times-Bold'
    return t

# ═══════════════════════════════════════════════════════════════════════════════
# STYLES
# ═══════════════════════════════════════════════════════════════════════════════

def make_styles(t):
    fh, fb, fbb = t.font_head, t.font_body, t.font_body_bold
    return {
        'cover_title': ParagraphStyle('ct', fontName=fh,  fontSize=26, textColor=t.cover_title,  alignment=TA_CENTER, leading=32, spaceAfter=4),
        'cover_sub':   ParagraphStyle('cs', fontName=fh,  fontSize=12, textColor=t.cover_sub,    alignment=TA_CENTER, leading=16, spaceAfter=2),
        'cover_byline':ParagraphStyle('cb', fontName=fb,  fontSize=8,  textColor=t.cover_byline, alignment=TA_CENTER, leading=12),
        'cover_name':  ParagraphStyle('cn', fontName=fh,  fontSize=11, textColor=t.cover_name,   leading=15),
        'cover_arch':  ParagraphStyle('ca', fontName=fb,  fontSize=9,  textColor=t.cover_arch,   leading=13),
        'cover_meta':  ParagraphStyle('cm', fontName=fb,  fontSize=8,  textColor=t.cover_meta,   leading=12),
        'cover_rule':  ParagraphStyle('cr', fontName='Helvetica-Bold', fontSize=8.5,textColor=t.cover_rule_body, alignment=TA_CENTER, leading=12),
        'cover_note':  ParagraphStyle('co', fontName='Times-Italic', fontSize=9, textColor=t.cover_note, alignment=TA_CENTER, leading=13),
        'rules_head':  ParagraphStyle('rh', fontName=fh,  fontSize=10, textColor=t.accent,       alignment=TA_CENTER, leading=14, spaceBefore=4, spaceAfter=3),
        'body':        ParagraphStyle('b',  fontName=fb,  fontSize=9,  textColor=t.body,         leading=13, spaceAfter=3, alignment=TA_JUSTIFY),
        'body_sm':     ParagraphStyle('bs', fontName=fb,  fontSize=8,  textColor=t.row_text,     leading=11, spaceAfter=0),
        'body_sm_bold':ParagraphStyle('bb', fontName=fbb, fontSize=8,  textColor=t.row_text,     leading=11, spaceAfter=0),
        'sp_title':    ParagraphStyle('st', fontName=fh,  fontSize=11, textColor=t.special_title, leading=14, spaceBefore=1),
        'sp_label':    ParagraphStyle('sl', fontName=fbb, fontSize=7.5,textColor=t.special_label, leading=11, spaceAfter=1),
        'sp_body':     ParagraphStyle('sb', fontName=fb,  fontSize=8.5,textColor=t.special_body,  leading=12, spaceAfter=2, alignment=TA_JUSTIFY),
        'hook_label':  ParagraphStyle('hl', fontName=fh,  fontSize=9,  textColor=t.hook_label,   leading=12),
        'hook_body':   ParagraphStyle('hb', fontName='Times-Italic', fontSize=8.5, textColor=t.hook_body, leading=12, alignment=TA_JUSTIFY),
        'quote':       ParagraphStyle('q',  fontName='Times-BoldItalic', fontSize=9, textColor=t.quote, alignment=TA_CENTER, leading=13, spaceBefore=3),
        'italic_sm':   ParagraphStyle('is', fontName='Times-Italic', fontSize=8, textColor=t.italic, leading=11, alignment=TA_JUSTIFY),
        'notes_head':  ParagraphStyle('nh', fontName=fh,  fontSize=9,  textColor=t.banner_text,  leading=13),
        'wt_hdr':      ParagraphStyle('wth',fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white,  leading=10),
        'wt_body':     ParagraphStyle('wtb',fontName=fb,  fontSize=7.5, textColor=t.row_text,     leading=10),
        'wt_body_c':   ParagraphStyle('wtc',fontName=fbb, fontSize=7.5, textColor=t.row_text,     leading=10, alignment=TA_CENTER),
        'wt_dodge':    ParagraphStyle('wtd',fontName='Helvetica-Bold', fontSize=8.5, textColor=t.derived_label, leading=12),
    }

# ═══════════════════════════════════════════════════════════════════════════════
# FLOWABLES
# ═══════════════════════════════════════════════════════════════════════════════

class OrnRule(Flowable):
    def __init__(self, width, t): super().__init__(); self._t=t; self.width=width; self.height=8
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; c.setFillColor(self._t.accent); c.setStrokeColor(self._t.accent); c.setLineWidth(0.5)
        mid=self.width/2
        c.line(0,4,mid-8,4); c.line(mid+8,4,self.width,4)
        for x in [0,mid,self.width]:
            c.saveState(); c.translate(x,4); c.rotate(45); c.rect(-2.5,-2.5,5,5,fill=1,stroke=0); c.restoreState()

class CharHeader(Flowable):
    def __init__(self, name, arch, meta, allg, width, t):
        super().__init__(); self._n=name; self._a=arch; self._m=meta; self._g=allg; self.width=width; self.height=52; self._t=t
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; t=self._t; w,h=self.width,self.height
        c.setFillColor(t.header_bg); c.roundRect(0,0,w,h,3,fill=1,stroke=0)
        c.setFillColor(t.header_inner); c.roundRect(2,2,w-4,h-4,2,fill=1,stroke=0)
        c.setStrokeColor(t.header_border); c.setLineWidth(1.2); c.roundRect(1,1,w-2,h-2,3,fill=0,stroke=1)
        # Thin inner accent line
        c.setStrokeColor(t.accent); c.setLineWidth(0.4); c.line(12,h-30,w-12,h-30)
        # Name
        c.setFillColor(t.header_name); c.setFont(t.font_head,20); c.drawString(12,h-22,self._n)
        # Archetype · setting
        c.setFillColor(t.header_sub); c.setFont('Helvetica',8.5)
        c.drawString(12,h-38,f"{self._a}  ·  {self._m}")
        # Allegiance right
        c.setFillColor(t.header_right); c.setFont('Helvetica',7.5)
        c.drawRightString(w-10,h-38,self._g)
        # Corner diamonds
        c.setFillColor(t.accent)
        for cx,cy in [(6,h-6),(w-6,h-6),(6,6),(w-6,6)]:
            c.saveState(); c.translate(cx,cy); c.rotate(45); c.rect(-2,-2,4,4,fill=1,stroke=0); c.restoreState()

class StatBlock(Flowable):
    """Seven characteristic boxes + dark derived-stats strip below.
    Header band split: label (top) · thin rule · stat×5% (bottom).
    Coordinates tuned so ×5 and main value never overlap."""
    def __init__(self, stats, derived, width, t):
        super().__init__(); self._s=stats; self._d=derived; self.width=width; self._t=t
        self.height = 70  # 44pt box + 14pt derived strip + 12pt top padding
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; t=self._t; w=self.width; n=len(self._s); bw=(w-4)/n
        BOX_H = 44   # top of box
        HDR_H = 16   # was 20 — now 16, giving light cell 14pt instead of 10pt

        for i,(label,val) in enumerate(self._s):
            x=i*bw+2
            try:    pct_str = f"{int(val)*5}%"
            except: pct_str = ''

            # Dark header (16pt: y=28 to y=44)
            c.setFillColor(t.stat_hdr_bg)
            c.rect(x, BOX_H-HDR_H, bw-1, HDR_H, fill=1, stroke=0)

            # Light value cell (14pt: y=14 to y=28) — 4pt taller than before
            c.setFillColor(t.stat_cell_bg)
            c.rect(x, 14, bw-1, BOX_H-HDR_H-14, fill=1, stroke=0)

            # Full box border (y=14 to y=44)
            c.setStrokeColor(t.rule); c.setLineWidth(0.5)
            c.rect(x, 14, bw-1, BOX_H-14, fill=0, stroke=1)

            # Thin divider at y=36 (midpoint of 16pt header)
            c.setStrokeColor(t.accent); c.setLineWidth(0.3)
            c.line(x+3, BOX_H-8, x+bw-4, BOX_H-8)   # y=36

            # Label — upper header band (y=36–44, baseline y=38)
            c.setFillColor(t.stat_hdr_text); c.setFont('Helvetica-Bold', 7)
            c.drawCentredString(x+(bw-1)/2, BOX_H-6, label)   # y=38

            # ×5 percentile — lower header band (y=28–36, baseline y=30)
            # cap top ≈y=34.7, divider at y=36 → 1.3pt clearance ✓
            if pct_str:
                c.setFillColor(t.stat_hdr_text); c.setFont('Helvetica-Bold', 6.5)
                c.drawCentredString(x+(bw-1)/2, BOX_H-14, pct_str)  # y=30

            # Main stat value — light cell baseline y=16
            # cap top ≈y=26, header bottom y=28 → 1.9pt clearance ✓
            c.setFillColor(t.stat_cell_text); c.setFont(t.font_head, 14)
            c.drawCentredString(x+(bw-1)/2, 16, str(val))

        # Dark derived stats strip (unchanged)
        c.setFillColor(t.derived_bg); c.rect(0,0,w,13,fill=1,stroke=0)
        c.setStrokeColor(t.rule); c.setLineWidth(0.3); c.rect(0,0,w,13,fill=0,stroke=1)
        x_pos=6
        for lbl,val in self._d:
            c.setFillColor(t.derived_label); c.setFont('Helvetica-Bold',7)
            c.drawString(x_pos,3,lbl+':')
            lw=c.stringWidth(lbl+':'  ,'Helvetica-Bold',7)
            c.setFillColor(t.derived_val); c.setFont('Helvetica-Bold',8)
            c.drawString(x_pos+lw+2,2.5,str(val))
            vw=c.stringWidth(str(val),'Helvetica-Bold',8)
            x_pos+=lw+vw+12

class SectionBanner(Flowable):
    def __init__(self, text, width, t, special=False):
        super().__init__(); self._text=text; self.width=width; self._t=t; self._sp=special; self.height=16
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; t=self._t
        bg=t.banner_special if self._sp else t.banner_bg
        c.setFillColor(bg); c.rect(0,0,self.width,16,fill=1,stroke=0)
        c.setStrokeColor(t.accent); c.setLineWidth(0.5); c.rect(0,0,self.width,16,fill=0,stroke=1)
        c.setFillColor(t.banner_text); c.setFont(t._t.font_head if hasattr(t,'_t') else 'Helvetica-Bold',9)
        c.setFont('Helvetica-Bold',9); c.drawString(8,4.5,self._text.upper())

class HPTrack(Flowable):
    """Clean HP tracker: 20pt boxes, every-5th-shaded, NO milestone text, numbers at 9pt."""
    BOX=20; GAP=4
    def __init__(self, max_hp, width, t, label="HIT POINTS", fill=None, fill5=None, border=None, num=None):
        super().__init__()
        self.max_hp=max_hp; self.width=width; self._t=t
        self._label=label
        self._fill  = fill  or t.hp_box_fill
        self._fill5 = fill5 or t.hp_box_5th
        self._border= border or t.hp_box_border
        self._num   = num   or t.hp_num
        self._label_col = t.hp_label
        self._max_col   = t.hp_max
        B,G=self.BOX,self.GAP
        bpr=int(width/(B+G)); self.bpr=max(bpr,1)
        rows=(max_hp+self.bpr-1)//self.bpr
        # Height: 20pt label area + rows*(box+gap) - last gap
        self.height=20+rows*(B+G)
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; B,G=self.BOX,self.GAP
        max_hp=self.max_hp; bpr=self.bpr; w=self.width; top=self.height
        # Label row
        c.setFillColor(self._label_col); c.setFont('Helvetica-Bold',9)
        c.drawString(0,top-13,self._label)
        c.setFillColor(self._max_col); c.setFont('Helvetica-Bold',9)
        c.drawRightString(w,top-13,f"MAX  {max_hp}")
        c.setStrokeColor(self._border); c.setLineWidth(0.4)
        c.line(0,top-16,w,top-16)

        y_start=top-20  # top of first row of boxes

        for i in range(max_hp):
            row=i//bpr; col=i%bpr
            items_this_row=min(bpr, max_hp-row*bpr)
            row_w=items_this_row*(B+G)-G
            start_x=(w-row_w)/2
            x=start_x+col*(B+G)
            y=y_start-row*(B+G)
            hp_val=max_hp-i

            # Shadow
            c.setFillColor(colors.HexColor('#B0B8C8') if self._t.name=='nc' else colors.HexColor('#C8A090'))
            c.rect(x+1.5,y-1.5,B,B,fill=1,stroke=0)
            # Box fill — every 5th gets slightly different shade
            fill=self._fill5 if (hp_val%5==0) else self._fill
            c.setFillColor(fill)
            c.setStrokeColor(self._border); c.setLineWidth(1.0)
            c.rect(x,y,B,B,fill=1,stroke=1)
            # Number — 9pt, centered
            c.setFillColor(self._num); c.setFont('Helvetica-Bold',9)
            c.drawCentredString(x+B/2, y+(B-7)/2, str(hp_val))

class PortraitPlaceholder(Flowable):
    """Reserved portrait space — to be replaced with Midjourney art."""
    def __init__(self, char_name, width, height, t):
        super().__init__(); self._name=char_name; self.width=width; self.height=height; self._t=t
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; t=self._t; w,h=self.width,self.height
        # Background
        c.setFillColor(t.port_bg); c.roundRect(0,0,w,h,4,fill=1,stroke=0)
        # Border
        c.setStrokeColor(t.port_border); c.setLineWidth(1.0); c.roundRect(0,0,w,h,4,fill=0,stroke=1)
        # Crosshatch
        c.setStrokeColor(t.port_text); c.setLineWidth(0.25)
        for y in range(0,int(h)+1,14):
            c.line(0,y,w,y)
        for x in range(0,int(w)+1,14):
            c.line(x,0,x,h)
        # Solid bg over crosshatch for text
        c.setFillColor(t.port_bg)
        mid_y=h/2; text_h=60
        c.rect(4,mid_y-text_h/2,w-8,text_h,fill=1,stroke=0)
        # Portrait reserved text
        c.setFillColor(t.port_label); c.setFont('Helvetica-Bold',9)
        c.drawCentredString(w/2,mid_y+18,"PORTRAIT")
        c.drawCentredString(w/2,mid_y+6,"RESERVED")
        c.setFillColor(t.port_text); c.setFont('Helvetica',7.5)
        c.drawCentredString(w/2,mid_y-8,self._name)
        c.setFont('Helvetica',7); c.drawCentredString(w/2,mid_y-20,"Midjourney art")
        # Corner marks
        c.setStrokeColor(t.port_border); c.setLineWidth(1.0); sz=8
        for x0,y0,dx,dy in [(1,h-1,1,-1),(w-1,h-1,-1,-1),(1,1,1,1),(w-1,1,-1,1)]:
            c.line(x0,y0,x0+dx*sz,y0); c.line(x0,y0,x0,y0+dy*sz)

class BackHeader(Flowable):
    def __init__(self, name, arch, width, t):
        super().__init__(); self._n=name; self._a=arch; self.width=width; self.height=28; self._t=t
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; t=self._t; w,h=self.width,self.height
        c.setFillColor(t.back_bg); c.roundRect(0,0,w,h,3,fill=1,stroke=0)
        c.setStrokeColor(t.back_border); c.setLineWidth(0.8); c.roundRect(1,1,w-2,h-2,2,fill=0,stroke=1)
        c.setFillColor(colors.white); c.setFont(t.font_head,14); c.drawString(10,h-19,self._n)
        nw=c.stringWidth(self._n,t.font_head,14)
        c.setFillColor(t.back_sub); c.setFont('Helvetica',8)
        c.drawString(14+nw,h-18,f"·  {self._a}  ·  {t.back_note}")
        c.setFillColor(t.accent)
        for cx,cy in [(5,h-5),(w-5,h-5),(5,5),(w-5,5)]:
            c.saveState(); c.translate(cx,cy); c.rotate(45); c.rect(-1.5,-1.5,3,3,fill=1,stroke=0); c.restoreState()

class NotesBlock(Flowable):
    def __init__(self, width, t, lines=7):
        super().__init__(); self.width=width; self._t=t; self.lines=lines; self.height=lines*16+4
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; c.setStrokeColor(self._t.rule); c.setLineWidth(0.4)
        for i in range(self.lines): c.line(0,self.height-(i+1)*16+4,self.width,self.height-(i+1)*16+4)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE BACKGROUNDS
# ═══════════════════════════════════════════════════════════════════════════════

def make_cover_bg(t):
    def fn(c,doc):
        c.saveState(); w,h=A4
        if t.name=='nc':
            c.setFillColor(colors.HexColor('#040810')); c.rect(0,0,w,h,fill=1,stroke=0)
            c.setFillColor(colors.HexColor('#080F1E')); c.roundRect(20,20,w-40,h-40,5,fill=1,stroke=0)
            # Grid
            c.setStrokeColor(colors.HexColor('#0C1E38')); c.setLineWidth(0.2)
            for y in range(20,int(h)-20,16): c.line(20,y,w-20,y)
            for x in range(20,int(w)-20,24): c.line(x,20,x,h-20)
        else:
            c.setFillColor(colors.HexColor('#1A1A1A')); c.rect(0,0,w,h,fill=1,stroke=0)
            c.setFillColor(t.parchment); c.roundRect(20,20,w-40,h-40,5,fill=1,stroke=0)
            c.setStrokeColor(colors.HexColor('#DDD8C8')); c.setLineWidth(0.15)
            for y in range(20,int(h)-20,7): c.line(20,y,w-20,y)
        c.setFillColor(t.accent if t.name=='nc' else colors.HexColor('#CC2200'))
        c.rect(20,h-90,w-40,70,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#0A1428') if t.name=='nc' else colors.HexColor('#2A2A2A'))
        c.rect(20,20,w-40,50,fill=1,stroke=0)
        c.setStrokeColor(t.accent); c.setLineWidth(2.0); c.roundRect(20,20,w-40,h-40,5,fill=0,stroke=1)
        c.setLineWidth(0.5); c.roundRect(24,24,w-48,h-48,3,fill=0,stroke=1)
        c.setLineWidth(0.8)
        for y in [h-90,h-20,70,20]: c.line(20,y,w-20,y)
        c.restoreState()
    return fn

def make_page_bg(t):
    def fn(c,doc):
        c.saveState(); w,h=A4
        c.setFillColor(t.page_bg); c.rect(0,0,w,h,fill=1,stroke=0)
        if t.name=='nc':
            c.setStrokeColor(colors.HexColor('#D0D8E8')); c.setLineWidth(0.15)
            for y in range(0,int(h),10): c.line(0,y,w,y)
        else:
            c.setStrokeColor(colors.HexColor('#DDD8C8')); c.setLineWidth(0.15)
            for y in range(0,int(h),8): c.line(0,y,w,y)
        c.setStrokeColor(t.rule); c.setLineWidth(1.5); c.rect(8,8,w-16,h-16,fill=0,stroke=1)
        c.setStrokeColor(t.accent); c.setLineWidth(0.4); c.rect(11,11,w-22,h-22,fill=0,stroke=1)
        c.setFont('Helvetica',7.5); c.setFillColor(t.footer)
        c.drawCentredString(w/2,14,t.footer_text)
        c.restoreState()
    return fn

# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# ZOMBIE COMBAT DATA
# ═══════════════════════════════════════════════════════════════════════════════

# (roll, zone_key, result_name, narrative, mechanics)
ZOMBIE_TABLE = [
    (1,  'close', "Near Miss",          "No HP. Lose 1 SAN."),
    (2,  'close', "Clothing Grab",      "No HP. Lose 1 SAN. Clothing may be torn."),
    (3,  'close', "Stumble",            "1 HP. Next action costs one full movement."),
    (4,  'close', "Nail Rake",          "1 HP. Skin intact — no infection risk."),
    (5,  'close', "Balance Lost",       "1 HP. Spend next action standing, or take another attack."),
    (6,  'close', "Shoulder Slam",      "1D3 HP. Knocked back 1m. -10% to next combat roll."),
    (7,  'infect',"Surface Scratch",    "1D3 HP.  INFECTION ROLL: CON×5 or symptomatic within hours."),
    (8,  'infect',"Teeth Graze",        "1D3 HP.  INFECTION ROLL: CON×5."),
    (9,  'infect',"Deep Scratch",       "1D4 HP.  INFECTION ROLL: CON×4."),
    (10, 'infect',"Hair Grab",          "1D4 HP.  INFECTION ROLL: CON×4."),
    (11, 'infect',"Bite — Clothed",     "1D4 HP.  INFECTION: automatic. CON×5 or symptomatic."),
    (12, 'infect',"Bite — Exposed",     "1D6 HP.  INFECTION: auto.  Bleeding: 1 HP/round until treated."),
    (13, 'infect',"Locked Grip",        "1D4 HP.  Full action to escape (Brawl/STR). Auto-attack next round if not free."),
    (14, 'danger',"Moderate Bite",      "1D6 HP.  INFECTION: auto.  Bleeding 1D3 HP/rd. First Aid 50%+ to stop."),
    (15, 'danger',"Knocked Down",       "1D6 HP.  Brawl -20% to escape. While pinned: re-roll each round, min result 11."),
    (16, 'danger',"Deep Bite",          "1D8 HP.  INFECTION: auto.  CON roll or unconscious 1D3 rounds."),
    (17, 'danger',"Multiple Contact",   "1D8 HP.  INFECTION: auto.  Roll D20 for 2nd zombie (min result 11)."),
    (18, 'fatal', "Severe Bite — Limb", "1D10 HP. INFECTION: auto.  Fail STR: limb loses function, -20% physical skills."),
    (19, 'fatal', "Critical Wound",     "2D6 HP.  INFECTION: auto.  CON-4 or death in 1D3 rounds. First Aid 70%+ now."),
    (20, 'fatal', "Overwhelmed",        "3D6 HP.  INFECTION: irreversible — turning within 1hr. CON-6 or instant death."),
]

ZOMBIE_ZONES = {
    'close':  ('#2A6040', colors.HexColor('#2A6040'), colors.HexColor('#E4F2E4'), colors.HexColor('#CDE8CD'), 'ZONE 1 — CLOSE CALL  (1–6)'),
    'infect': ('#7A5200', colors.HexColor('#7A5200'), colors.HexColor('#F8EDD4'), colors.HexColor('#F0DDA0'), 'ZONE 2 — INFECTION TERRITORY  (7–13)'),
    'danger': ('#8B3000', colors.HexColor('#8B3000'), colors.HexColor('#F4E0D8'), colors.HexColor('#E8C4B8'), 'ZONE 3 — SERIOUS DANGER  (14–17)'),
    'fatal':  ('#5A0000', colors.HexColor('#5A0000'), colors.HexColor('#ECC8C4'), colors.HexColor('#E0A8A0'), 'ZONE 4 — CATASTROPHIC  (18–20)'),
}

ZOMBIE_APPROACHES = [
    # (Approach, Skill, On success)
    ('Blunt weapon',         'Melee or Brawl skill',       'Skull crushed. Zombie neutralized.'),
    ('Bladed weapon',        'Melee (weapon skill)',        'Brain or neck severed. Zombie neutralized.'),
    ('Brawl / stomp',        'Brawl skill',                'Zombie down. Neutralized.'),
    ('Push past / evade',    'Dodge or Athletics',         'Zombie avoided. Pass through.'),
    ('Distract / divert',    'Fast Talk or Insight',       'Diverted 1D3 rounds. Not neutralized.'),
    ('Firearm — body shot',  'Firearms skill',             'Zombie slowed. -20% next attack. NOT neutralized.'),
    ('Firearm — head shot',  'Firearms skill at -20%',     'Zombie neutralized. Head shot.'),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CHARACTER DATA  (Day One: combat skills boosted)
# ═══════════════════════════════════════════════════════════════════════════════

NC_CHARS = [
  {'name':'Sable Kress','arch':'The Fixer','meta':'Neo-Ashford Operative','allg':'Veltris Contract — Active',
   'physical':'Late thirties. Corporate-smooth face, contractor-worn hands. Moves through rooms as if she has been in every one before. A corporate jaw augment visible as a faint ridge. Expensive coat. Never holds eye contact a moment longer than necessary.',
   'stats':[('STR','11'),('CON','12'),('SIZ','11'),('INT','15'),('POW','13'),('DEX','12'),('APP','14')],
   'derived':[('HP','12'),('PP','13'),('DB','—'),('SR','23'),('Move','10')],
   'skills':[('Persuade','65%'),('Fast Talk','60%'),('Insight','55%'),('Status','50%'),('Bargain','55%'),('Streetwise','50%'),('Dodge','40%'),('Stealth','30%'),('Spot Hidden','40%'),('Drive','45%'),('Law','35%'),('Research','45%'),('Firearms (Pistol)','40%'),('Psychology','50%'),('Disguise','30%'),('Perception','45%'),('Computer Use','35%'),('Intimidate','35%')],
   'equipment':['Corporate encrypted comm — one-time wipe if seized','Two burner comms — dead accounts','Licensed sidearm (2D6) — holstered, rarely drawn','Three contact IDs she would rather not explain','Veltris NDA — partially read, half understood','4,000 credits upfront — cold account'],
   'weapons':[{'name':'Licensed Pistol','skill':'Firearms (Pistol)','atk':'40%','par':'—','damage':'2D6','notes':'Rng 30m · 15 rds · Mal 00'},{'name':'Tactical Knife','skill':'Knife (base)','atk':'25%','par':'20%','damage':'1D4+2','notes':'Boot knife · base chance only'}],
   'sp_name':'"Subdermal Comms Mesh"','sp_type':'Corporate neural comm implant — jaw subdermal, Veltris issue','sp_stats':'Encrypted 500m range  ·  Signal sense 10m  ·  Emergency wipe (1-use)',
   'sp_abilities':[('Encrypted channel','Two-way comms 500m. Unjammable on standard bands. Veltris security can intercept — she does not know this.'),('Signal sense','Detects active comm transmissions within 10m as faint pressure.'),('Emergency wipe (1-use)','Destroys all comm history on voice command. Two-day headache follows.'),('Cost','Veltris telemetry ping still active. She believes it was deactivated. It was not.')],
   'sp_note':'Sable Morn smiled at the briefing already knowing exactly where this team was standing.',
   'background':'Eleven years on corporate-adjacent contracts. Three Veltris contracts before tonight. She knows Sable Morn smiles at the debrief. She has been paid not to ask questions. Tonight she will have to.',
   'hook':'Has worked three Veltris contracts. She knows Sable Morn. She knows the smile. Tonight she asks the questions she was paid not to.',
   'quote':'"I know what this job is. I also know what it costs to say no. Let\'s move."'},
  {'name':'Juno Rhee','arch':'The Ghost','meta':'Sub-District 7 background','allg':'Veltris Contract — Active',
   'physical':'Late twenties, looks younger. Small and fast. ECM rig lines visible at the collarbone in direct light. Black-weave clothing, no reflective surfaces. The stillness of someone who learned it from training, not temperament.',
   'stats':[('STR','11'),('CON','13'),('SIZ','10'),('INT','14'),('POW','12'),('DEX','16'),('APP','11')],
   'derived':[('HP','12'),('PP','12'),('DB','—'),('SR','26'),('Move','12')],
   'skills':[('Stealth','70%'),('Spot Hidden','60%'),('Perception','55%'),('Electronics','50%'),('Pick Lock','55%'),('Dodge','55%'),('Security Systems','55%'),('Climb','55%'),('Athletics','50%'),('Jump','50%'),('Sleight of Hand','40%'),('Disguise','45%'),('Firearms (Pistol)','40%'),('Melee','45%'),('Surveillance','50%'),('Drive','45%'),('Streetwise','50%'),('Computer Use','40%')],
   'equipment':['Surveillance-countermeasure suite — jams drone ID reads 5m radius','Black-weave bodysuit — 1pt armour, no thermal signature','Monoblade (ceramic) — worn at hip','Micro-fibre grapple rig — 30m, silent deployment','Two burner comms — cash-loaded, no chip trace','Six spare ECM power cells'],
   'weapons':[{'name':'Compact Holdout','skill':'Firearms (Pistol)','atk':'40%','par':'—','damage':'1D8','notes':'Rng 20m · 8 rds · Mal 00'},{'name':'Monoblade','skill':'Melee','atk':'45%','par':'45%','damage':'1D8+2','notes':'Ceramic · no scanner · can impale'}],
   'sp_name':'"ECM Shroud Suite"','sp_type':'Active countermeasure implant — collarbone/shoulder subdermal, black-market military-clone','sp_stats':'Drone ID blackout 5m  ·  +20% Stealth active  ·  Signal intercept passive',
   'sp_abilities':[('Drone ID blackout','Active: drone biometric recognition within 5m returns null. 1 power cell per 30 min.'),('+ 20% Stealth (active)','Electronic motion sensors treat her as background noise while running.'),('Signal intercept','Passively hears unencrypted comm traffic at Electronics 40%.'),('Cost','Runs hot. 2+ hrs: -10% fine motor. 4+ hrs: headaches. Warranty expired 6 months ago.')],
   'sp_note':'Military-pattern clone from Sub-District 8. Three of six original functions work. The tremor is newer than she has admitted.',
   'background':'Grew up in Sub-District 7. Left at seventeen. The Terminus Bar is known to her. Jed Osler — a debt from a decade ago. Coming back tonight will feel like something she cannot name.',
   'hook':'The Terminus Bar is her territory. She knows Jed Osler. She owes Jed one from a decade ago. She has not been back since going corporate-side.',
   'quote':'"Don\'t worry about the suit. Worry about what\'s in the tunnels."'},
  {'name':'Viktor Drav','arch':'The Muscle','meta':'Ex-Meridian Security Group','allg':'Veltris Contract — Active',
   'physical':'Late thirties. Large, economical, weight in the torso. Ex-military bearing he hasn\'t stopped performing. Subdermal armour faintly visible as ridges at the shoulders. A face that stopped being expressive in professional settings years ago.',
   'stats':[('STR','16'),('CON','15'),('SIZ','15'),('INT','11'),('POW','11'),('DEX','13'),('APP','10')],
   'derived':[('HP','16'),('PP','11'),('DB','+1D4'),('SR','28'),('Move','10')],
   'skills':[('Firearms (Pistol)','65%'),('Firearms (Rifle)','60%'),('Brawl','60%'),('Athletics','55%'),('Dodge','50%'),('Intimidate','50%'),('Drive','50%'),('Spot Hidden','45%'),('Melee','55%'),('Throw','45%'),('Climb','40%'),('Security Systems','35%'),('First Aid','35%'),('Track','30%'),('Perception','40%'),('Stealth','20%'),('Streetwise','35%'),('Firearms (Auto)','50%')],
   'equipment':['Military sidearm (2D6+2)','Telescopic combat baton — belt clip','Tactical rig — mag pouches, medkit slot, comms','Night-vision monocle — 4hr battery','Trauma pads ×3 — stop bleeding, +1D6 natural heal','Six-day field rations'],
   'weapons':[{'name':'Military Sidearm','skill':'Firearms (Pistol)','atk':'65%','par':'—','damage':'2D6+2','notes':'Rng 40m · 15 rds · Mal 00'},{'name':'Combat Baton','skill':'Melee','atk':'55%','par':'55%','damage':'1D8+DB','notes':'Telescopic · DB: +1D4 · can parry'},{'name':'Brawl/Grapple','skill':'Brawl','atk':'60%','par':'60%','damage':'1D3+DB','notes':'Unarmed · DB: +1D4 · grab/throw option'}],
   'sp_name':'"Subdermal Combat Plates + Reflex Tap"','sp_type':'Meridian Security Group standard issue — shoulder/torso armour + spinal reflex tap','sp_stats':'+2 armour (torso/shoulders)  ·  +1 DEX on combat SR  ·  Involuntary counter-attack',
   'sp_abilities':[('+2 armour (passive)','Subdermal plates at shoulders and upper torso. Cannot be removed, soaked, or directly targeted.'),('Reflex tap (+1 DEX SR)','Neural tap adds 1 DEX for Strike Rank in combat only.'),('Adrenaline dump (1/combat)','On being hit for 3+ HP: free attack at +10% before end of round. Involuntary.'),('Cost','Muscle spasm — sharp shoulder/neck contraction 1-2 sec. Was 1/session. Now daily.')],
   'sp_note':'Meridian issue. He kept them. Meridian records show them decommissioned. This is not the same thing.',
   'background':'Ex-Meridian Security Group. Sub-Districts 1-4, four years. Quit eighteen months ago — same time the Sub-District 7 disappearances started. He has been piecing this together. Has not said it to anyone.',
   'hook':'Quit Meridian eighteen months ago, same time the disappearances started. He has been connecting those two facts quietly for a year and a half.',
   'quote':'"I\'ve been corporate security. I\'ve been what hides things. This is different."'},
  {'name':'Tal Morgan','arch':'The Tech','meta':'Neo-Ashford Freelance','allg':'Veltris Contract — Active',
   'physical':'Mid-twenties. Something slightly caffeinated about the eyes. Too many pockets, all occupied. A clean neural interface scar behind the right ear. Fingers that move independently when thinking.',
   'stats':[('STR','11'),('CON','12'),('SIZ','11'),('INT','16'),('POW','12'),('DEX','14'),('APP','12')],
   'derived':[('HP','12'),('PP','12'),('DB','—'),('SR','25'),('Move','10')],
   'skills':[('Electronics','70%'),('Repair (Elec)','65%'),('Computer Use','60%'),('Drone Ops','60%'),('Spot Hidden','50%'),('Security Systems','55%'),('Science (Comp)','50%'),('Research','50%'),('Comms (Elec)','55%'),('Stealth','35%'),('Dodge','35%'),('Drive','40%'),('First Aid','30%'),('Perception','45%'),('Firearms (Pistol)','30%'),('Bargain','35%'),('Pick Lock','40%'),('Surveillance','45%')],
   'equipment':['Drone — palm-sized, near-silent, 20-min battery, live feed to wrist display','Hacking suite (wrist) — 1D6 min per encryption layer','EMP pulse device (1-use, 10m) — disables ALL electronics including augments','Tool roll — 14 pieces','Wrist display — drone feed, maps, comms, bio-scanner readout','Six spare power cells'],
   'weapons':[{'name':'Compact Sidearm','skill':'Firearms (Pistol)','atk':'30%','par':'—','damage':'1D8','notes':'Rng 20m · 8 rds · Mal 00'},{'name':'Multi-Tool Blade','skill':'Knife (base)','atk':'25%','par':'20%','damage':'1D4+1','notes':'From tool roll · base chance'},{'name':'EMP Pulse Device','skill':'Electronics','atk':'—','par':'—','damage':'Special','notes':'1-use · 10m radius · all electronics fail incl. augments'}],
   'sp_name':'"Neural I/O Bridge"','sp_type':'Direct machine interface — behind-ear subdermal, self-built prototype, 11 months','sp_stats':'Direct interface +15% Electronics  ·  Drone sync (visual cortex)  ·  Passive net sense 20m',
   'sp_abilities':[('Direct interface','Touch-range interface with any electronic system. Electronics +15% when using direct contact.'),('Drone sync','Drone feeds directly to visual cortex. -10% Spot Hidden in vicinity while synced.'),('Passive network sense','Within 20m: detects active wireless transmissions and direction. No roll.'),('Cost','Self-installed. 73% stable. Once per session: 2-3 sec feedback spike, no action possible. Has never told anyone.')],
   'sp_note':'The child on The Slab pressed a note into Tal\'s hand specifically. The paper smells faintly chemical.',
   'background':'Freelance tech contractor. The drone is a custom salvage build. The EMP is one of two built last month. The other is in a drawer at home.',
   'hook':'[PRIVATE] The child on The Slab approaches Tal and presses a note: Don\'t go to the plant. My dad went. He didn\'t come back the same. The paper has a faint chemical smell.',
   'quote':'"I have eyes everywhere. The problem is what the eyes are seeing."'},
  {'name':'Reina Vasquez','arch':'The Medic','meta':'Neo-Ashford Contract Medic','allg':'Veltris Contract — Active',
   'physical':'Early thirties. The calm of someone who learned it because the alternative made the job harder. Medical kit worn on the hip naturally. Watches breathing before she watches eyes.',
   'stats':[('STR','11'),('CON','13'),('SIZ','12'),('INT','15'),('POW','14'),('DEX','13'),('APP','13')],
   'derived':[('HP','13'),('PP','14'),('DB','—'),('SR','25'),('Move','10')],
   'skills':[('Medicine','65%'),('First Aid','70%'),('Sci (Biology)','50%'),('Perception','50%'),('Persuade','45%'),('Psychology','55%'),('Spot Hidden','45%'),('Dodge','40%'),('Drive','40%'),('Research','45%'),('Sci (Chemistry)','40%'),('Stealth','30%'),('Computer Use','35%'),('Bargain','40%'),('Brawl','30%'),('Insight','50%'),('Pharmacology','45%'),('Firearms (Pistol)','30%')],
   'equipment':['Full trauma kit — clamp, wound seal, bone stabiliser, pain management','Stimulants ×3 — +10% physical 1D4hrs then -15% crash','Bio-scanner (wrist strap) — organic life signs 5m','Sedative injectors ×2 — CON resist or unconscious 1D4hrs','Antibiotics and infection protocols','Encrypted data-pad — three years of field observations'],
   'weapons':[{'name':'Compact Pistol','skill':'Firearms (Pistol)','atk':'30%','par':'—','damage':'1D10','notes':'Rng 25m · 10 rds · Mal 00'},{'name':'Brawl','skill':'Brawl','atk':'30%','par':'30%','damage':'1D3','notes':'Unarmed · no DB'},{'name':'Sedative Injector','skill':'Medicine','atk':'30%','par':'—','damage':'Special','notes':'Med roll to hit · CON resist or unconscious 1D4hr · 2 doses'}],
   'sp_name':'"Biometric Diagnostics Array"','sp_type':'Medical diagnostic augment — palm/fingertip subdermal sensors, Meridian Medical licensed','sp_stats':'Tactile diagnosis  ·  Toxin detection  ·  Bio-scanner sync to 8m',
   'sp_abilities':[('Tactile diagnosis','Touch skin: temp, pulse, BP readout. Medicine +20% when treating someone she has touched.'),('Toxin detection','Identifies presence and class of toxin/pathogen at contact range.'),('Bio-scanner sync','Wrist-strap range extends to 8m. Near the entity: behaves strangely.'),('Cost','The array reads everything. Reina has learned to stop looking when she doesn\'t want to know.')],
   'sp_note':'Clause 14(f): Meridian Medical retains anonymised diagnostic data from all licensed arrays. Reina did not read clause 14(f).',
   'background':'Contract medic, three years. A colleague at a Meridian-contracted morgue once said: the tissue appeared to be growing inward. We did not determine the entry point. The colleague has since been reassigned.',
   'hook':'A colleague described unusual organic tissue: growing inward, entry point unknown. Colleague reassigned. Tonight Reina finds the entry point.',
   'quote':'"I can keep everyone alive four more hours. After that I need to know what we\'re dealing with."'},
  {'name':'Petra Amis','arch':'The Analyst','meta':'Independent Research Contractor','allg':'Veltris Contract — Active',
   'physical':'Mid-thirties. Defensive tidiness. Physical notepad in a jacket pocket — unusual, deliberate. Does not carry corporate-grade equipment because it has logs. Watches exits before people.',
   'stats':[('STR','10'),('CON','11'),('SIZ','11'),('INT','17'),('POW','13'),('DEX','11'),('APP','12')],
   'derived':[('HP','11'),('PP','13'),('DB','—'),('SR','22'),('Move','10')],
   'skills':[('Research','70%'),('Library Use','65%'),('Data Analysis','60%'),('Insight','60%'),('Spot Hidden','50%'),('Computer Use','50%'),('Persuade','45%'),('Psychology','50%'),('Drive','35%'),('Electronics','40%'),('Science (Var)','55%'),('Write','55%'),('Law','40%'),('Dodge','30%'),('Stealth','30%'),('Perception','55%'),('Bargain','35%'),('Cryptography','45%')],
   'equipment':['Encrypted terminal — Veltris public filings, all local data air-gapped','Signal scanner — active transmission detection, logs frequency/source','Physical notepad and pen — habit, or paranoia. Both.','Four data sticks — different encryption standards','800 credits cash, physical, untraceable','The anonymous message — printed, folded, left inside pocket'],
   'weapons':[{'name':'Micro Pistol','skill':'Handgun (base)','atk':'20%','par':'—','damage':'1D6','notes':'Rng 15m · 6 rds · Mal 00 · untrained'},{'name':'Signal Scanner','skill':'Improvised (base)','atk':'20%','par':'—','damage':'1D4','notes':'Used as club · base chance · one use before damaged'}],
   'sp_name':'"Encrypted Cortex Store"','sp_type':'Memory and data augment — temple subdermal, unknown manufacturer, received as payment 2yrs ago','sp_stats':'Eidetic recall  ·  Encrypted memory partition  ·  Passive cross-indexing',
   'sp_abilities':[('Eidetic recall','Any text or data directly observed recalled exactly. Research +20% from recalled material.'),('Encrypted partition','Locked cortex section. 12-char passphrase only Petra knows.'),('Passive indexing','Unconsciously cross-references all new information. Once per session: GM may tell Petra one thing the table missed.'),('Cost','Manufacturer unknown. Locked partition: something put there 18 months ago, never opened since.')],
   'sp_note':'The passphrase is the name of the client who paid her with this augment. She has never said that name aloud.',
   'background':'Independent research contractor. Two days before this job: anonymous encrypted message, 40 minutes to break. Inside: coordinates in Sub-District 9 and three words. Don\'t go back.',
   'hook':'[PRIVATE] Anonymous message, 40 minutes to break. Coordinates in Sub-District 9: Don\'t go back. She has never been there. Tonight she finds out what the third word means.',
   'quote':'"Two days ago someone sent me three words. I\'m here to understand what the third one means."'},
]

# ── DAY ONE  (combat skills boosted throughout) ──────────────────────────────
D1_CHARS = [
  {'name':'Kira Osei-Mensah','arch':'NHS Junior Doctor (off duty)','meta':'South Bank, Sunday 17 May','allg':'Reach: Abena (mother, 74, Peckham)',
   'physical':'Late twenties. 22 hours awake — the brightness of adrenaline over exhaustion. Hospital lanyard still clipped to her jacket. Moves between people the way someone trained to assess urgency fast.',
   'stats':[('STR','9'),('CON','12'),('SIZ','10'),('INT','16'),('POW','14'),('DEX','13'),('APP','14')],
   'derived':[('HP','11'),('MP','14'),('DB','—'),('SR','23'),('Move','10')],
   'skills':[('First Aid','75%'),('Medicine','55%'),('Sci (Biology)','50%'),('Persuade','55%'),('Insight','55%'),('Psychology','60%'),('Spot Hidden','50%'),('Dodge','40%'),('Research','50%'),('Drive','35%'),('Computer Use','35%'),('Bargain','30%'),('Brawl','40%'),('Climb','30%'),('Language (Twi)','50%'),('Status','40%'),('Perception','50%'),('Track','20%')],
   'equipment':['Phone — 73% battery. NHS group chats already flooding.','Crossbody bag: travel card, £60 cash, Oyster','Earbuds — call to her mum attempted, ringing out','Hospital ID badge — opens NHS facility doors','BNF pocket edition — always in the bag','A nearly finished flat white — warm at the alert'],
   'weapons':[
     {'name':'Scalpel/Blade','skill':'Knife','atk':'40%','par':'—','damage':'1D4','notes':'From medical kit · can impale · instinctive use'},
     {'name':'Brawl','skill':'Brawl','atk':'40%','par':'40%','damage':'1D3','notes':'Unarmed · no DB · trauma training'},
   ],
   'sp_name':'What You Know That Others Don\'t','sp_type':'22 hours post-night-shift. Triage training. Hospital ID.','sp_stats':'First Aid 75%  ·  Medicine 55%  ·  Triage (no roll)  ·  NHS ID access',
   'sp_abilities':[('Triage (no roll)','Once per scene: assess all wounded in view, rank by survivability in one round.'),('Improvised medicine','First Aid 75% becomes 55% with improvised supplies.'),('Infection assessment','Medicine 50%: assess bite victim\'s likely timeline. The answer will not be comforting.'),('Running on fumes','22hrs awake: -10% all non-medical rolls after Act Two begins.')],
   'sp_note':'Her mother Abena, 74, alone in Peckham. Infection spread from Elephant & Castle. Peckham is between the group and the river. Kira knows this geometry. Has not said it yet.',
   'background':'Junior doctor, 6 months post-qualification, A&E. Running on post-shift adrenaline. The group\'s best medical resource. Also 22 hours without sleep, trying to reach a 74-year-old who is not picking up.',
   'hook':'Her mother is in Peckham. The infection started at Elephant & Castle and moves east through Peckham. Kira has made this calculation. She has not said it aloud.',
   'quote':'"Tell me what you\'re feeling. Specifically. Not fine — specifically."'},

  {'name':'Dev Krishnamurthy','arch':'Freelance software engineer','meta':'Borough Market café, Sunday','allg':'Reach: flatmate near Old Street',
   'physical':'Late twenties. Headphones half-on. Laptop bag, worn strap. The unfocused expression of someone who has been in their own head all morning and is now very much not.',
   'stats':[('STR','10'),('CON','11'),('SIZ','11'),('INT','17'),('POW','12'),('DEX','13'),('APP','12')],
   'derived':[('HP','11'),('MP','12'),('DB','—'),('SR','24'),('Move','10')],
   'skills':[('Computer Use','75%'),('Electronics','65%'),('Library Use','60%'),('Research','55%'),('Sci (Maths)','45%'),('Sci (Computing)','70%'),('Spot Hidden','45%'),('Insight','40%'),('Dodge','35%'),('Drive','40%'),('Bargain','30%'),('Persuade','35%'),('Brawl','35%'),('Climb','30%'),('Stealth','30%'),('Perception','45%'),('Track','20%'),('Psychology','30%')],
   'equipment':['MacBook Pro — 81% battery, tracking spread on four social media threads','Phone — 94% battery, scanner app notifications since 9:40 AM','Laptop bag: charger, USB hub, notebook (unused), protein bar','AirPods (full charge)','Wallet: £45 cash, three cards, Oyster (£8.40)','Voice note from flatmate about spare keys — unanswered, one hour old'],
   'weapons':[
     {'name':'Laptop (improvised)','skill':'Improvised','atk':'35%','par':'—','damage':'1D4','notes':'Heavy, slow · one use before damaged · survival instinct'},
     {'name':'Brawl','skill':'Brawl','atk':'35%','par':'35%','damage':'1D3','notes':'Unarmed · no DB · desperation baseline'},
   ],
   'sp_name':'What You Know That Others Don\'t','sp_type':'Emergency scanner app. Tracking spread since 9:40 AM — 67 minutes before the alert.','sp_stats':'Computer Use 75%  ·  Early spread data  ·  Network access  ·  Signal mapping',
   'sp_abilities':[('Early data','Knows Elephant & Castle origin, three smoke plume locations, spread rate.'),('Network access','While signal exists: open CCTV, transport data, social media.'),('Signal mapping','Map cell tower activity to find crowd concentrations. 20-min task.'),('Cost — what he hasn\'t said','Has been watching since 9:40 AM. Told no one. Filed it as monitoring.')],
   'sp_note':'Dev has known something was wrong for an hour before the alert. Tonight data becomes geography.',
   'background':'Freelance software engineer. Works from coffee shops. Knows London through data, not geography. Tonight one becomes the other.',
   'hook':'Has been tracking the spread since 9:40 AM — an hour before the alert. Has more information than anyone. Has told no one.',
   'quote':'"I\'ve been watching this develop for an hour. I should have said something. I know."'},

  {'name':'Maggie Donnelly','arch':'Retired Metropolitan Police (22 yrs)','meta':'Jubilee Walkway, Sunday','allg':'Reach: Cara (daughter, Deptford)',
   'physical':'Early sixties. Practical coat, good shoes, a pace that covers ground without appearing to hurry. The assessment in her eyes is continuous. She retired six years ago and has not stopped doing the job.',
   'stats':[('STR','12'),('CON','13'),('SIZ','12'),('INT','15'),('POW','14'),('DEX','11'),('APP','12')],
   'derived':[('HP','13'),('MP','14'),('DB','—'),('SR','23'),('Move','10')],
   'skills':[('Persuade','70%'),('Psychology','65%'),('Spot Hidden','65%'),('Insight','70%'),('Law','60%'),('Brawl','55%'),('First Aid','50%'),('Dodge','55%'),('Drive','60%'),('Intimidate','60%'),('Firearms (Pistol)','45%'),('Track','45%'),('Athletics','45%'),('Search','55%'),('Streetwise','50%'),('Stealth','35%'),('Perception','65%'),('Climb','40%')],
   'equipment':['Phone — 62% battery. Cara not answering.','Practical coat, water bottle, small first aid kit (always)','Expired warrant card (laminated) — she does not know if it will work','Wallet: £120 cash (always), Oyster, two cards','ASP baton — telescopic, legally held, habit from service','Pocket notepad and two pens — old habit'],
   'weapons':[
     {'name':'ASP Baton','skill':'Brawl','atk':'55%','par':'50%','damage':'1D6','notes':'Telescopic · legally held · ex-police issue'},
     {'name':'Brawl','skill':'Brawl','atk':'55%','par':'55%','damage':'1D3','notes':'Unarmed · no DB · trained response'},
     {'name':'Personal Firearm','skill':'Firearms (Pistol)','atk':'45%','par':'—','damage':'1D10','notes':'Rng 30m · 8 rds · if found/available · Mal 00'},
   ],
   'sp_name':'What You Know That Others Don\'t','sp_type':'First on scene, Tavistock Square 2005. 22 years crowd management.','sp_stats':'Persuade +20% evacuation  ·  Scene assessment (no roll)  ·  Warrant card (1-use, 60%)',
   'sp_abilities':[('Scene assessment (no roll)','Assess any crowd, group or space for threat level, routes, key individuals in one round.'),('Authority','Persuade +20% in crowd management or evacuation.'),('Tavistock memory','First on scene at mass casualty. -10% to SAN loss from human casualties.'),('Warrant card (1-use, 60%)','Expired 6 years. Show with total confidence: 60% they don\'t check the date.')],
   'sp_note':'Cara lives in Deptford. The infection moves east from Elephant & Castle. Maggie has made this calculation. The tension between duty to this group and reaching her daughter is the engine of her character.',
   'background':'Twenty-two years Met Police, retired DCI. First on scene Tavistock Square 2005. Has handled riots, the 2011 disorder, a gas explosion. None prepared her for a person standing waist-deep in the Thames, head tilted, in no distress.',
   'hook':'Cara is in Deptford. The infection moves east from Elephant & Castle. The tension between getting these people out and reaching her daughter is the engine of her character.',
   'quote':'"Move. I\'ll explain why while we\'re moving."'},

  {'name':'Olu Adeyemi','arch':'Security guard, The Shard','meta':'Shard lobby, Sunday overtime','allg':'Reach: No family in London — group becomes the motivation',
   'physical':'Early thirties. Large, unhurried, the calm of someone who handles other people\'s panic professionally. Security uniform. Radio on his belt not working properly. His coffee from home is on the desk.',
   'stats':[('STR','15'),('CON','14'),('SIZ','14'),('INT','13'),('POW','13'),('DEX','12'),('APP','13')],
   'derived':[('HP','15'),('MP','13'),('DB','+1D4'),('SR','26'),('Move','10')],
   'skills':[('Brawl','65%'),('Spot Hidden','60%'),('Security Systems','60%'),('Athletics','60%'),('Persuade','45%'),('Drive','55%'),('Intimidate','55%'),('Dodge','55%'),('First Aid','40%'),('Climb','55%'),('Electronics','40%'),('Perception','65%'),('Stealth','40%'),('Track','35%'),('Firearms (Pistol)','40%'),('Melee','50%'),('Search','50%'),('Streetwise','45%')],
   'equipment':['Security radio — intermittently functional, fragments only','Shard keycard — all staff areas, service levels, roof','Security baton (1D6+DB) — standard issue','Personal phone — 91% battery. His mum picked up this morning.','Shard master key ring — 17 keys','Coffee from home in insulated mug'],
   'weapons':[
     {'name':'Security Baton','skill':'Brawl','atk':'65%','par':'60%','damage':'1D6+DB','notes':'Standard issue · DB: +1D4 · can parry'},
     {'name':'Brawl','skill':'Brawl','atk':'65%','par':'65%','damage':'1D3+DB','notes':'Unarmed · DB: +1D4 · grapple/restrain option'},
     {'name':'Sidearm (found)','skill':'Firearms (Pistol)','atk':'40%','par':'—','damage':'1D10','notes':'Rng 30m · 8 rds · if found in building · Mal 00'},
   ],
   'sp_name':'What You Know That Others Don\'t','sp_type':'The Shard: CCTV, radio, roof sightlines, full building access.','sp_stats':'Full building access  ·  Radio fragments  ·  CCTV 200m  ·  Shard sightlines',
   'sp_abilities':[('Full building access','Keycard/key to all Shard areas. Upper floors: three smoke plumes visible, all south of expected.'),('Radio fragments','Fragmented police transmissions. Key: Elephant & Castle first reports 7:14 AM — 2hrs before alert.'),('CCTV 200m','Security terminal, Electronics/Computer 40%. What it shows is already worse than the street sounds.'),('Group becomes the motivation','No family in London. By Act Two, this group is why he is here. Player should feel this, not be told it.')],
   'sp_note':'The radio fragment about the cordon — north of the river — lands hardest on Olu. He is holding the radio when it comes through. Give him the moment.',
   'background':'Shard security, two years. From Birmingham. No family in London. His mum picked up this morning — that fact anchors him throughout the night.',
   'hook':'The cordon radio fragment is his to deliver. He has trusted the institution all day. Give him the moment when the institution\'s logic becomes clear.',
   'quote':'"I have keys to everything in this building and I can see three miles from the roof. Use that before we lose it."'},

  {'name':'Priya Mehta','arch':'Science journalist','meta':'Southbank Centre, Sunday','allg':'Reach: editor (has Meridian documents)',
   'physical':'Early thirties. Press lanyard still on. A notebook in hand before she consciously decided to take it out. The tension of someone whose instinct is to find the story and whose training says find it very carefully.',
   'stats':[('STR','9'),('CON','11'),('SIZ','10'),('INT','17'),('POW','13'),('DEX','12'),('APP','14')],
   'derived':[('HP','11'),('MP','13'),('DB','—'),('SR','22'),('Move','10')],
   'skills':[('Library Use','70%'),('Research','70%'),('Insight','65%'),('Write','65%'),('Persuade','60%'),('Psychology','55%'),('Sci (Biology)','55%'),('Spot Hidden','50%'),('Computer Use','50%'),('Sci (Chemistry)','50%'),('Drive','35%'),('Dodge','35%'),('Law','30%'),('Climb','30%'),('Stealth','30%'),('Perception','55%'),('Language (Hindi)','60%'),('Bargain','45%')],
   'equipment':['Phone — 88% battery. Editor\'s message: "Something came in. Can we talk Monday?"','Notebook (half-full) and three pens — she will fill the rest tonight','Press lanyard — Southbank Centre media pass (valid)','Laptop in shoulder bag — research and other things','Voice recorder (full battery)','Wallet: £35 cash, press card, two cards'],
   'weapons':[
     {'name':'Brawl','skill':'Brawl','atk':'35%','par':'35%','damage':'1D3','notes':'Unarmed · no DB · survival instinct'},
     {'name':'Improvised','skill':'Improvised','atk':'30%','par':'—','damage':'1D3','notes':'Pen, bag, chair — last resort · no DB'},
   ],
   'sp_name':'What You Know That Others Don\'t','sp_type':'Editor has Meridian Biosciences documents. They arrived 48hrs before the outbreak.','sp_stats':'Research 70%  ·  Meridian thread  ·  Source assessment  ·  Press access (1-use)',
   'sp_abilities':[('Meridian thread','Editor has Meridian Biosciences documents. Research 70%/Psychology 55%: begin piecing together the connection.'),('Source assessment','Evaluate credibility of any info source: Insight 65%.'),('Story vs group','Best positioned to understand the truth. Using it to help vs document is a genuine player choice.'),('Press access (1-use)','Valid lanyard. In the first two hours, officials sometimes still respond. Once per session.')],
   'sp_note':'Her editor has the Meridian documents. They arrived 48 hours before the outbreak. She has been choosing not to use her instincts. Tonight she will not have that option.',
   'background':'Science journalist, biology and public health. Her editor\'s message is about Meridian Biosciences. She has been choosing not to know. Tonight everything she chose not to know becomes necessary.',
   'hook':'Editor has Meridian Biosciences documents that arrived 48hrs before the outbreak. She filed the message for Monday. Tonight it cannot wait.',
   'quote':'"I need to understand what this is before I can help anyone survive it."'},

  {'name':'Tom Becker','arch':'Scaffolding worker','meta':'Waterloo Road side street, Sunday','allg':'Reach: his van (exit route) and his mum (no answer)',
   'physical':'Late twenties. Work clothes, high-vis jacket. Van keys in his right hand. Tool bag over one shoulder. The unaffected physicality of someone who climbs things for a living without considering it unusual.',
   'stats':[('STR','14'),('CON','14'),('SIZ','13'),('INT','12'),('POW','11'),('DEX','13'),('APP','11')],
   'derived':[('HP','14'),('MP','11'),('DB','+1D4'),('SR','26'),('Move','10')],
   'skills':[('Craft (Construction)','70%'),('Athletics','65%'),('Climb','70%'),('Mechanics','60%'),('Drive','65%'),('Brawl','55%'),('Spot Hidden','50%'),('Throw','55%'),('Melee','50%'),('Dodge','50%'),('Perception','55%'),('Search','50%'),('Streetwise','45%'),('Intimidate','40%'),('First Aid','35%'),('Track','40%'),('Electronics (Basic)','25%'),('Security Systems','25%')],
   'equipment':['Tool bag: hammer (1D6+DB), bolt cutters, crowbar (1D8+DB), screwdrivers, zip ties','High-vis jacket — visibility is a mixed blessing tonight','Phone — 44% battery. Voicemail left for mum. No callback.','Van keys (parked Lambeth North — across the river or the long way round)','Work gloves — thick leather, 1pt hand armour, -10% fine motor','Half a water bottle and an energy bar'],
   'weapons':[
     {'name':'Crowbar','skill':'Melee','atk':'50%','par':'45%','damage':'1D8+DB','notes':'From tool bag · DB: +1D4 · can parry · best option'},
     {'name':'Hammer','skill':'Melee','atk':'50%','par':'—','damage':'1D6+DB','notes':'From tool bag · DB: +1D4 · backup'},
     {'name':'Brawl','skill':'Brawl','atk':'55%','par':'55%','damage':'1D3+DB','notes':'Unarmed · DB: +1D4'},
   ],
   'sp_name':'What You Know That Others Don\'t','sp_type':'Can build, break into, or assess structural stability of anything. Has a van.','sp_stats':'Craft 70%  ·  Structural instinct (no roll)  ·  Van across the river  ·  Tool bag',
   'sp_abilities':[('Structural instinct (no roll)','Assess any building or barrier for load capacity, weak points, fortification potential.'),('Break and build','Craft 70% for barriers, forced entry, climbing points. Tool bag: +10%.'),('The van','Near Lambeth North — across the river or the long way round. Tools, rope, full diesel, radio.'),('His mum','She didn\'t answer this morning. He left a voicemail. She still hasn\'t called back. He is not saying anything about it.')],
   'sp_note':'Tom\'s van is the scenario\'s most practical resource. Whether to go for it — and whether his real motivation is the van or what it represents — is a player choice.',
   'background':'Scaffolding worker, eight years. South London born and raised. Called his mum this morning. She didn\'t pick up. Left a voicemail. She still hasn\'t called back.',
   'hook':'His mum didn\'t answer. Still hasn\'t called back. He will not say this unless asked. If asked, he will answer plainly and change the subject.',
   'quote':'"Tell me what needs breaking or what needs holding. I can do both."'},
]

# ═══════════════════════════════════════════════════════════════════════════════
# ZOMBIE COMBAT PAGE BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_zombie_pages(story, t, UW):
    """Append zombie combat reference page to story."""
    S = make_styles(t)

    # Colours for zone bands
    ZC = {
        'close':  (colors.HexColor('#1A4A30'), colors.HexColor('#E4F2E4'), colors.HexColor('#CDE8CD')),
        'infect': (colors.HexColor('#6A4400'), colors.HexColor('#F8EDD4'), colors.HexColor('#F0DDA0')),
        'danger': (colors.HexColor('#7A2800'), colors.HexColor('#F4E0D8'), colors.HexColor('#E8C4B8')),
        'fatal':  (colors.HexColor('#5A0000'), colors.HexColor('#ECC8C4'), colors.HexColor('#E0A8A0')),
    }
    zone_labels = {
        'close':  'ZONE 1 — CLOSE CALL  (1–6)',
        'infect': 'ZONE 2 — INFECTION TERRITORY  (7–13)',
        'danger': 'ZONE 3 — SERIOUS DANGER  (14–17)',
        'fatal':  'ZONE 4 — CATASTROPHIC  (18–20)',
    }

    title_s    = ParagraphStyle('zt',  fontName=t.font_head,          fontSize=18, textColor=t.accent,        alignment=TA_CENTER, leading=22, spaceAfter=2)
    sub_s      = ParagraphStyle('zs',  fontName='Times-Italic',       fontSize=9,  textColor=t.italic,        alignment=TA_CENTER, leading=12, spaceAfter=1)
    body_s     = ParagraphStyle('zb',  fontName='Times-Roman',        fontSize=8.5,textColor=t.body,          leading=12, alignment=TA_JUSTIFY)
    zn_hdr_s   = ParagraphStyle('znh', fontName='Helvetica-Bold',     fontSize=7.5,textColor=colors.white,    leading=10)
    roll_s     = ParagraphStyle('zr',  fontName='Helvetica-Bold',     fontSize=8.5,textColor=t.accent,        leading=11, alignment=TA_CENTER)
    name_s     = ParagraphStyle('zn',  fontName=t.font_body_bold,     fontSize=7,  textColor=t.body,          leading=9)
    eff_s      = ParagraphStyle('ze',  fontName=t.font_body,          fontSize=6.5,textColor=t.body,          leading=8.5)
    mech_bold  = ParagraphStyle('zm',  fontName='Helvetica-Bold',     fontSize=6.5,textColor=t.body,          leading=8.5)
    ap_hdr     = ParagraphStyle('ah',  fontName='Helvetica-Bold',     fontSize=7,  textColor=colors.white,    leading=9)
    ap_cell    = ParagraphStyle('ac',  fontName='Times-Roman',        fontSize=7,  textColor=t.body,          leading=9)
    note_s     = ParagraphStyle('znt', fontName='Times-Italic',       fontSize=7,  textColor=t.italic,        alignment=TA_CENTER, leading=10)

    # Title
    story.append(Spacer(1,2))
    story.append(Paragraph("ZOMBIE ATTACK RESOLUTION", title_s))
    story.append(Paragraph("Day One — London Falls  ·  Player & GM Reference", sub_s))
    story.append(Spacer(1,3))
    story.append(OrnRule(UW, t))
    story.append(Spacer(1,4))

    # Rule explanation — condensed to two lines
    story.append(SectionBanner("THE RULE — TWO STEPS", UW, t))
    story.append(Spacer(1,3))
    story.append(Paragraph(
        "Zombies do not use Hit Points. A decisive blow to the head neutralizes them. A missed blow gives them one attack. "
        "<b>DECLARE YOUR APPROACH</b> (see table), roll D100 ≤ your skill. "
        "<b>HIT:</b> zombie neutralized, no HP loss, lose 1 SAN.  "
        "<b>MISS:</b> roll D20 on the attack table below.  "
        "<b>HORDE:</b> 2–3 zombies: roll twice, take the worse. 4+ zombies: automatic result 15+.",
        body_s))
    story.append(Spacer(1,3))

    # Approach table
    ap_rows = [[
        Paragraph('APPROACH', ap_hdr),
        Paragraph('SKILL TO ROLL', ap_hdr),
        Paragraph('ON SUCCESS', ap_hdr),
    ]]
    for i,(approach, skill, result) in enumerate(ZOMBIE_APPROACHES):
        ap_rows.append([
            Paragraph(approach, ap_cell),
            Paragraph(skill,    ap_cell),
            Paragraph(result,   ap_cell),
        ])
    ap_t = Table(ap_rows, colWidths=[UW*0.28, UW*0.27, UW*0.45])
    ap_ts = [
        ('BACKGROUND', (0,0),(-1,0), t.banner_bg),
        ('LINEBELOW',  (0,0),(-1,-1), 0.3, t.rule),
        ('LEFTPADDING',(0,0),(-1,-1), 5),('RIGHTPADDING',(0,0),(-1,-1), 4),
        ('TOPPADDING', (0,0),(-1,-1), 1),('BOTTOMPADDING',(0,0),(-1,-1), 1),
    ]
    for i in range(1, len(ap_rows)):
        ap_ts.append(('BACKGROUND',(0,i),(-1,i), t.row1 if i%2==1 else t.row2))
    ap_t.setStyle(TableStyle(ap_ts))
    story.append(ap_t)
    story.append(Spacer(1,4))
    story.append(OrnRule(UW, t))
    story.append(Spacer(1,4))

    # D20 table header
    story.append(SectionBanner("D20 ZOMBIE ATTACK TABLE", UW, t))
    story.append(Spacer(1,3))

    # Build the D20 rows, grouped by zone
    current_zone = None
    all_rows = []

    for roll, zone, name, mech in ZOMBIE_TABLE:
        if zone != current_zone:
            current_zone = zone
            hdr_col, light_col, dark_col = ZC[zone]
            # Zone banner row (spans all columns)
            all_rows.append(('zone_hdr', zone, zone_labels[zone]))

        # Combine description and mechanics — mech highlighted if it contains key terms
        mech_display = mech
        all_rows.append(('data', zone, roll, name, mech))

    # Now render the table
    tbl_rows = []
    style_cmds = [
        ('LINEBELOW',    (0,0),(-1,-1), 0.3, t.rule),
        ('LEFTPADDING',  (0,0),(-1,-1), 5),('RIGHTPADDING',(0,0),(-1,-1), 4),
        ('TOPPADDING',   (0,0),(-1,-1), 2),('BOTTOMPADDING',(0,0),(-1,-1), 2),
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
    ]

    for i, row in enumerate(all_rows):
        if row[0] == 'zone_hdr':
            zone = row[1]; label = row[2]
            hdr_col, light_col, dark_col = ZC[zone]
            tbl_rows.append([
                Paragraph(label, zn_hdr_s),
                Paragraph('', zn_hdr_s),
                Paragraph('', zn_hdr_s),
            ])
            style_cmds.append(('BACKGROUND', (0,i),(-1,i), hdr_col))
            style_cmds.append(('SPAN',        (0,i),(-1,i)))
            style_cmds.append(('TOPPADDING',  (0,i),(-1,i), 2))
            style_cmds.append(('BOTTOMPADDING',(0,i),(-1,i), 2))
        else:
            _, zone, roll, name, mech = row
            hdr_col, light_col, dark_col = ZC[zone]
            # Alternate between light and dark within zone
            row_idx_in_zone = sum(1 for r in all_rows[:i] if r[0]=='data' and r[1]==zone)
            bg = light_col if row_idx_in_zone % 2 == 0 else dark_col

            # Mechanics only in right column (desc dropped for compactness)
            combined = f"<b>{mech}</b>"
            tbl_rows.append([
                Paragraph(str(roll), roll_s),
                Paragraph(name, name_s),
                Paragraph(combined, eff_s),
            ])
            style_cmds.append(('BACKGROUND', (0,i),(-1,i), bg))

    d20_t = Table(tbl_rows, colWidths=[UW*0.07, UW*0.22, UW*0.71])
    d20_t.setStyle(TableStyle(style_cmds))
    story.append(d20_t)
    story.append(Spacer(1,3))
    story.append(Paragraph(
        "INFECTION ROLLS: CON×5 = roll D100 ≤ (CON×5) to avoid symptoms. "
        "Automatic infection = no roll permitted. Kira (Medicine 55%) can assess a bitten character's timeline.",
        note_s))
    story.append(OrnRule(UW, t))


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def get_skill(char, fragment):
    for n,v in char.get('skills',[]): 
        if fragment.lower() in n.lower(): return v
    return '—'

def build_pdf(path, CHARS, t, cover_title, cover_sub, cover_byline, rules, portraits=None, append_zombie=False):
    S  = make_styles(t)
    LW = UW * 0.62; RW = UW * 0.36; SKH = (LW - 4*mm) / 2
    port_w = RW - 2; port_h = port_w * (640/427)

    doc = BaseDocTemplate(path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN+4*mm, bottomMargin=MARGIN+8*mm)
    cover_frame   = Frame(0,0,PAGE_W,PAGE_H,id='cover')
    content_frame = Frame(MARGIN,MARGIN+8*mm,UW,PAGE_H-2*MARGIN-12*mm,id='content')
    doc.addPageTemplates([
        PageTemplate(id='cover',  frames=[cover_frame],   onPage=make_cover_bg(t)),
        PageTemplate(id='normal', frames=[content_frame], onPage=make_page_bg(t)),
    ])
    story = []

    # ── COVER ──────────────────────────────────────────────────────────────
    story.append(Spacer(1,72))
    story.append(Paragraph(cover_title, S['cover_title']))
    story.append(Spacer(1,5))
    story.append(Paragraph(cover_sub,   S['cover_sub']))
    story.append(Spacer(1,4))
    story.append(Paragraph(cover_byline,S['cover_byline']))
    story.append(Spacer(1,14))
    story.append(OrnRule(UW,t))
    story.append(Spacer(1,10))
    roster=[[Paragraph(f"<b>{c['name']}</b>",S['cover_name']),Paragraph(c['arch'],S['cover_arch']),Paragraph(c.get('meta',''),S['cover_meta'])]for c in CHARS]
    rt=Table(roster,colWidths=[UW*0.38,UW*0.38,UW*0.24])
    rt.setStyle(TableStyle([('ROWBACKGROUNDS',(0,0),(-1,-1),[t.cover_row1,t.cover_row2]),('LINEBELOW',(0,0),(-1,-1),0.4,t.rule),('LINEABOVE',(0,0),(-1,0),1.0,t.accent),('LINEBELOW',(0,-1),(-1,-1),1.0,t.accent),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.append(rt)
    story.append(Spacer(1,12))
    story.append(OrnRule(UW,t))
    story.append(Spacer(1,8))
    story.append(Paragraph("QUICK REFERENCE",S['rules_head']))
    rlt=Table([[Paragraph(cell,S['cover_rule'])for cell in row]for row in rules],colWidths=[UW/3]*3)
    rlt.setStyle(TableStyle([('ROWBACKGROUNDS',(0,0),(-1,-1),[t.cover_row1,t.cover_row2]),('GRID',(0,0),(-1,-1),0.4,t.rule),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    story.append(rlt)
    story.append(Spacer(1,8))
    story.append(Paragraph("Hand sheets face-down. Players choose by archetype, not stats.",S['cover_note']))
    story.append(NextPageTemplate('normal'))
    story.append(PageBreak())

    # ── CHARACTER PAGES ────────────────────────────────────────────────────
    for char in CHARS:
        max_hp  = int(next(v for k,v in char['derived'] if k in ('HP',)))
        max_san = int(next((v for k,v in char['derived'] if k in ('MP','PP')),10))
        dodge   = get_skill(char,'dodge')
        db_val  = next((v for k,v in char['derived'] if k=='DB'),'—')

        # FRONT PAGE
        story.append(CharHeader(char['name'],char['arch'],char['meta'],char['allg'],UW,t))
        story.append(Spacer(1,4))

        sk=char['skills']
        if len(sk)%2: sk=sk+[('','')]
        mid=len(sk)//2
        sk_rows=[]
        for (la,lv),(ra,rv) in zip(sk[:mid],sk[mid:]):
            sk_rows.append([Paragraph(la,S['body_sm']),Paragraph(f"<b>{lv}</b>",S['body_sm']),Paragraph(ra,S['body_sm']),Paragraph(f"<b>{rv}</b>",S['body_sm'])])
        skt=Table(sk_rows,colWidths=[SKH*0.72,SKH*0.28,SKH*0.72,SKH*0.28])
        skt.setStyle(TableStyle([('ROWBACKGROUNDS',(0,0),(-1,-1),[t.row1,t.row2]),('LINEBELOW',(0,0),(-1,-1),0.3,t.rule),('LINEAFTER',(1,0),(1,-1),0.5,t.rule),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),('ALIGN',(1,0),(1,-1),'RIGHT'),('ALIGN',(3,0),(3,-1),'RIGHT')]))
        left_items=[[SectionBanner("Characteristics",LW-4,t)],[Spacer(1,2)],[StatBlock(char['stats'],char['derived'],LW-4,t)],[Spacer(1,4)],[SectionBanner("Skills",LW-4,t)],[Spacer(1,2)],[skt]]
        left_inner=Table(left_items,colWidths=[LW-4])
        left_inner.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))

        if portraits and char['name'] in portraits:
            from reportlab.platypus import Image as RLImage
            right_ph=RLImage(portraits[char['name']],width=port_w,height=port_h)
        else:
            right_ph=PortraitPlaceholder(char['name'],port_w,port_h,t)

        two_col=Table([[left_inner,right_ph]],colWidths=[LW,RW])
        two_col.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),('ALIGN',(1,0),(1,-1),'RIGHT'),('LINEBEFORE',(1,0),(1,-1),0.5,t.accent)]))
        story.append(two_col)
        story.append(Spacer(1,4))

        # EQUIPMENT
        story.append(SectionBanner("Equipment",UW,t))
        story.append(Spacer(1,2))
        eqt=Table([[Paragraph(f"\u2022 {item}",S['body_sm'])]for item in char['equipment']],colWidths=[UW])
        eqt.setStyle(TableStyle([('ROWBACKGROUNDS',(0,0),(-1,-1),[t.row1,t.row2]),('LINEBELOW',(0,0),(-1,-1),0.3,t.rule),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
        story.append(eqt)
        story.append(Spacer(1,4))

        # COMBAT
        story.append(SectionBanner("Combat",UW,t))
        story.append(Spacer(1,2))
        cw=[UW*0.26,UW*0.17,UW*0.09,UW*0.09,UW*0.13,UW*0.26]
        wep_rows=[[Paragraph('WEAPON',S['wt_hdr']),Paragraph('SKILL',S['wt_hdr']),Paragraph('ATK',S['wt_hdr']),Paragraph('PAR',S['wt_hdr']),Paragraph('DAMAGE',S['wt_hdr']),Paragraph('NOTES',S['wt_hdr'])]]
        for w in char.get('weapons',[]):
            wep_rows.append([Paragraph(w['name'],S['wt_body']),Paragraph(w['skill'],S['wt_body']),Paragraph(w['atk'],S['wt_body_c']),Paragraph(w['par'],S['wt_body_c']),Paragraph(w['damage'],S['wt_body_c']),Paragraph(w['notes'],S['wt_body'])])
        ts=[('BACKGROUND',(0,0),(-1,0),t.banner_bg),('TEXTCOLOR',(0,0),(-1,0),colors.white),('LINEBELOW',(0,0),(-1,-1),0.3,t.rule),('LINEAFTER',(0,0),(4,-1),0.3,t.rule),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),('ALIGN',(2,0),(4,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]
        for i in range(1,len(wep_rows)): ts.append(('BACKGROUND',(0,i),(-1,i),t.row1 if i%2==1 else t.row2))
        wt=Table(wep_rows,colWidths=cw); wt.setStyle(TableStyle(ts))
        story.append(wt)
        dodge_row=Table([[Paragraph(f"DODGE: <b>{dodge}</b>",S['wt_dodge']),Paragraph(f"DAMAGE BONUS: <b>{db_val}</b>",S['wt_dodge'])]],colWidths=[UW*0.45,UW*0.55])
        dodge_row.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),t.derived_bg),('BOX',(0,0),(-1,-1),0.8,t.accent),('LEFTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
        story.append(dodge_row)
        story.append(Spacer(1,5))

        # HP + SAN TRACKS
        story.append(HPTrack(max_hp,UW,t))
        story.append(Spacer(1,4))
        story.append(HPTrack(max_san,UW,t,label="SANITY POINTS",fill=t.san_box_fill,fill5=t.san_box_5th,border=t.san_box_border,num=t.san_num))
        story.append(PageBreak())

        # BACK PAGE
        story.append(BackHeader(char['name'],char['arch'],UW,t))
        story.append(Spacer(1,6))
        story.append(Paragraph(f"<i>{char['physical']}</i>",S['italic_sm']))
        story.append(Spacer(1,8))
        story.append(SectionBanner(t.special_label_str,UW,t,special=True))
        story.append(Spacer(1,3))
        dc=[Paragraph(char['sp_name'],S['sp_title']),Paragraph(char['sp_type'],S['sp_label']),Paragraph(char['sp_stats'],S['sp_body'])]
        for abn,abd in char['sp_abilities']: dc.append(Paragraph(f"<b>{abn}:</b>  {abd}",S['sp_body']))
        dc.append(Paragraph(f"<i>{char['sp_note']}</i>",S['sp_body']))
        di=Table([[el]for el in dc],colWidths=[UW-18]); di.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),t.special_bg),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
        do=Table([[di]],colWidths=[UW]); do.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),t.special_bg),('BOX',(0,0),(0,0),1.2,t.special_border),('LEFTPADDING',(0,0),(0,0),9),('RIGHTPADDING',(0,0),(0,0),9),('TOPPADDING',(0,0),(0,0),5),('BOTTOMPADDING',(0,0),(0,0),5)]))
        story.append(do)
        story.append(Spacer(1,6))
        story.append(SectionBanner("Background",UW,t))
        story.append(Spacer(1,4))
        story.append(Paragraph(char['background'],S['body']))
        story.append(Spacer(1,5))
        ht=Table([[Paragraph("PERSONAL HOOK:",S['hook_label']),Paragraph(char['hook'],S['hook_body'])]],colWidths=[28*mm,UW-28*mm])
        ht.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),t.hook_bg),('BOX',(0,0),(-1,-1),0.8,t.hook_border),('LINEBEFORE',(0,0),(0,-1),3,t.hook_bar),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('VALIGN',(0,0),(-1,-1),'TOP')]))
        story.append(ht)
        story.append(Spacer(1,6))
        story.append(OrnRule(UW,t))
        story.append(Paragraph(char['quote'],S['quote']))
        story.append(OrnRule(UW,t))
        story.append(Spacer(1,8))
        story.append(SectionBanner("Notes",UW,t))
        story.append(Spacer(1,5))
        story.append(NotesBlock(UW,t,lines=8))
        story.append(PageBreak())

    # ── ZOMBIE COMBAT REFERENCE PAGE ────────────────────────────────────────
    if append_zombie:
        build_zombie_pages(story, t, UW)

    doc.build(story)
    print(f"Done: {path}")


# ── RUN ─────────────────────────────────────────────────────────────────────
NC = night_crawler_theme()
D1 = day_one_theme()

ART = '/home/claude/ChaosiumCon26/scenarios/art/event-91/player-characters'
NC_PORTRAITS = {
    'Sable Kress':   f'{ART}/nc-pc01-sable-kress.jpeg',
    'Juno Rhee':     f'{ART}/nc-pc02-juno-rhee.jpeg',
    'Viktor Drav':   f'{ART}/nc-pc03-viktor-drav.jpeg',
    'Tal Morgan':    f'{ART}/nc-pc04-tal-morgan.jpeg',
    'Reina Vasquez': f'{ART}/nc-pc05-reina-vasquez.jpeg',
    'Petra Amis':    f'{ART}/nc-pc06-petra-amis.jpeg',
}

ART_D1 = '/home/claude/ChaosiumCon26/scenarios/art/event-159/player-characters'
D1_PORTRAITS = {
    'Kira Osei-Mensah':   f'{ART_D1}/d1-pc01-kira-osei-mensah.jpeg',
    'Dev Krishnamurthy':  f'{ART_D1}/d1-pc02-dev-krishnamurthy.jpeg',
    'Maggie Donnelly':    f'{ART_D1}/d1-pc03-maggie-donnelly.jpeg',
    'Olu Adeyemi':        f'{ART_D1}/d1-pc04-olu-adeyemi.jpeg',
    'Priya Mehta':        f'{ART_D1}/d1-pc05-priya-mehta.jpeg',
    'Tom Becker':         f'{ART_D1}/d1-pc06-tom-becker.jpeg',
}
NC_RULES=[
    ['HP = (CON+SIZ)/2  round up','PP = POW','DB: STR+SIZ 17-24 = None'],
    ['SR = DEX + INT','Attack: D100 ≤ skill%','DB 25-32: +1D4 | 33-40: +1D6'],
    ['Parry: D100 ≤ par skill%','Dodge: D100 ≤ dodge%','Unconscious at 0 HP'],
]
D1_RULES=[
    ['HP = (CON+SIZ)/2  round up','MP = POW','DB: STR+SIZ 17-24 = None'],
    ['SR = DEX + INT','Attack: D100 ≤ skill%','DB 25-32: +1D4 | 33-40: +1D6'],
    ['ZOMBIES: succeed = neutralized','Miss = roll D20 attack table','Head shot only for instant kill'],
]

build_pdf('/mnt/user-data/outputs/brp-night-crawler-v4.pdf', NC_CHARS, NC,
    "THE NIGHT CRAWLER","Player Character Reference — Neo-Ashford, 2087",
    "Basic Role-Playing  ·  Event 91  ·  ChaosiumCon 2026",
    NC_RULES, portraits=NC_PORTRAITS)

build_pdf('/mnt/user-data/outputs/brp-day-one-v4.pdf', D1_CHARS, D1,
    "DAY ONE — London Falls","Player Character Reference — South Bank, 17 May 2026",
    "Basic Role-Playing  ·  Event 159  ·  ChaosiumCon 2026",
    D1_RULES, portraits=D1_PORTRAITS, append_zombie=True)

# ── STANDALONE HANDOUT ───────────────────────────────────────────────────────
from reportlab.platypus import SimpleDocTemplate
def build_handout(path, t):
    UW_h = PAGE_W - 2*MARGIN
    doc = BaseDocTemplate(path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN+4*mm, bottomMargin=MARGIN+8*mm)
    content_frame = Frame(MARGIN,MARGIN+8*mm,UW_h,PAGE_H-2*MARGIN-12*mm,id='content')
    doc.addPageTemplates([PageTemplate(id='normal',frames=[content_frame],onPage=make_page_bg(t))])
    story = []
    build_zombie_pages(story, t, UW_h)
    doc.build(story)
    print(f"Done: {path}")

build_handout('/mnt/user-data/outputs/day-one-zombie-attack-handout.pdf', D1)
