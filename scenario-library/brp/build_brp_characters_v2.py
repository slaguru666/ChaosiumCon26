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
    t.cover_rule_body = colors.HexColor('#C0D8F0')   # body of rules table
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
    t.cover_rule_body = colors.HexColor('#2A2A2A')
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
        'cover_rule':  ParagraphStyle('cr', fontName=fb,  fontSize=8,  textColor=t.cover_rule_body, alignment=TA_CENTER, leading=12),
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
    """Seven characteristic boxes + dark derived-stats strip below."""
    def __init__(self, stats, derived, width, t):
        super().__init__(); self._s=stats; self._d=derived; self.width=width; self._t=t
        self.height = 62  # 36 (boxes) + 14 (derived strip) + 12 (padding)
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; t=self._t; w=self.width; n=len(self._s); bw=(w-4)/n
        BOX_H = 36
        # Characteristic boxes
        for i,(label,val) in enumerate(self._s):
            x=i*bw+2
            # Dark header row inside box
            c.setFillColor(t.stat_hdr_bg); c.rect(x,BOX_H-12,bw-1,12,fill=1,stroke=0)
            # Light value cell
            c.setFillColor(t.stat_cell_bg); c.rect(x,14,bw-1,BOX_H-12,fill=1,stroke=0)
            # Border
            c.setStrokeColor(t.rule); c.setLineWidth(0.5); c.rect(x,14,bw-1,22,fill=0,stroke=1)
            # Label (in dark header)
            c.setFillColor(t.stat_hdr_text); c.setFont('Helvetica-Bold',7)
            c.drawCentredString(x+(bw-1)/2,BOX_H-9,label)
            # Value (in light cell)
            c.setFillColor(t.stat_cell_text); c.setFont(t.font_head,14)
            c.drawCentredString(x+(bw-1)/2,17,str(val))

        # Dark derived stats strip
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
# CHARACTER DATA  (unchanged from v1)
# ═══════════════════════════════════════════════════════════════════════════════

NC_CHARS = [
  {'name':'Sable Kress','arch':'The Fixer','meta':'Neo-Ashford Operative','allg':'Veltris Contract — Active',
   'physical':'Late thirties. Corporate-smooth face, contractor-worn hands. Moves through rooms as if she has been in every one before. A corporate jaw augment visible as a faint ridge. Expensive coat. Never holds eye contact a moment longer than necessary.',
   'stats':[('STR','11'),('CON','12'),('SIZ','11'),('INT','15'),('POW','13'),('DEX','12'),('APP','14')],
   'derived':[('HP','12'),('PP','13'),('DB','—'),('SR','23'),('Move','10')],
   'skills':[('Persuade','65%'),('Fast Talk','60%'),('Insight','55%'),('Status','50%'),('Bargain','55%'),('Streetwise','50%'),('Dodge','40%'),('Stealth','30%'),('Spot Hidden','40%'),('Drive','45%'),('Law','35%'),('Research','45%'),('Firearms (Pistol)','40%'),('Psychology','50%'),('Disguise','30%'),('Perception','45%'),('Computer Use','35%'),('Intimidate','35%')],
   'equipment':['Corporate encrypted comm — one-time wipe if seized','Two burner comms — dead accounts','Licensed sidearm (2D6) — rarely used','Three contact IDs she would rather not explain','Veltris NDA — partially read, half understood','4,000 credits upfront — cold account'],
   'sp_name':'"Subdermal Comms Mesh"','sp_type':'Corporate neural comm implant — jaw subdermal, Veltris issue',
   'sp_stats':'Encrypted 500m range  ·  Signal sense 10m  ·  Emergency wipe (1-use)',
   'sp_abilities':[('Encrypted channel','Two-way comms with any team member within 500m. Unjammable on standard bands. Veltris corporate security can intercept it. She does not know this.'),('Signal sense','Detects active comm transmissions within 10m. Shows as a faint pressure.'),('Emergency wipe (1-use)','Destroys all comm history on voice command. Two-day headache follows.'),('Cost','Veltris issued this. It has a passive telemetry ping. She believes it was deactivated when she went freelance. It was not.')],
   'sp_note':'Sable Morn smiled at the briefing and already knew exactly where this team was standing.',
   'background':'Eleven years on corporate-adjacent contracts. Never full-time — contractor status keeps distance useful. Three Veltris contracts before tonight. She knows Sable Morn smiles at the debrief. She knows what the absence of a fourth contract means. She has been paid not to ask questions. Tonight she will have to ask them.',
   'hook':'Has worked three Veltris contracts. She knows Sable Morn. She knows the smile. Tonight she asks the questions she was paid not to.',
   'quote':'"I know what this job is. I also know what it costs to say no. Let\'s move."'},

  {'name':'Juno Rhee','arch':'The Ghost','meta':'Sub-District 7 background','allg':'Veltris Contract — Active',
   'physical':'Late twenties, looks younger. Small and fast. ECM rig lines visible at the collarbone in direct light. Black-weave clothing, no reflective surfaces. The stillness of someone who learned it from training, not temperament.',
   'stats':[('STR','11'),('CON','13'),('SIZ','10'),('INT','14'),('POW','12'),('DEX','16'),('APP','11')],
   'derived':[('HP','12'),('PP','12'),('DB','—'),('SR','26'),('Move','12')],
   'skills':[('Stealth','70%'),('Spot Hidden','60%'),('Perception','55%'),('Electronics','50%'),('Pick Lock','55%'),('Dodge','55%'),('Security Systems','55%'),('Climb','55%'),('Athletics','50%'),('Jump','50%'),('Sleight of Hand','40%'),('Disguise','45%'),('Firearms (Pistol)','40%'),('Melee','45%'),('Surveillance','50%'),('Drive','45%'),('Streetwise','50%'),('Computer Use','40%')],
   'equipment':['Surveillance-countermeasure suite — jams drone ID reads 5m radius (drains power)','Black-weave bodysuit — 1pt armour, no thermal signature','Monoblade (1D6+1) — ceramic, no metal detector signature','Micro-fibre grapple rig — 30m, silent deployment','Two burner comms — cash-loaded, no chip trace','Six spare ECM power cells'],
   'sp_name':'"ECM Shroud Suite"','sp_type':'Active countermeasure implant — collarbone/shoulder subdermal, black-market military-clone',
   'sp_stats':'Drone ID blackout 5m  ·  +20% Stealth active  ·  Signal intercept passive',
   'sp_abilities':[('Drone ID blackout','Active: all drone facial/biometric recognition within 5m returns null. Costs 1 power cell per 30 min.'),('+ 20% Stealth (active)','Electronic motion sensors treat her as background noise while running.'),('Signal intercept','Passively hears unencrypted comm traffic. Electronics 40% to identify speech.'),('Cost','Runs hot. After 2 hrs: -10% fine motor skills. After 4 hrs: headaches start. Warranty expired 6 months ago.')],
   'sp_note':'Military-pattern clone from Sub-District 8. Two of the original six functions don\'t work. The three that do have kept her alive. The tremor is newer than she has admitted.',
   'background':'Grew up in Sub-District 7. Left at seventeen. The Terminus Bar is known to her. So is Jed Osler — a debt from a decade ago that doesn\'t require repayment but never fully dissolves. Coming back tonight will feel like something she can\'t name. She has decided not to examine that until afterward.',
   'hook':'The Terminus Bar is her territory. She knows Jed Osler. She owes Jed one from a decade ago. She has not been back since going corporate-side.',
   'quote':'"Don\'t worry about the suit. Worry about what\'s in the tunnels."'},

  {'name':'Viktor Drav','arch':'The Muscle','meta':'Ex-Meridian Security Group','allg':'Veltris Contract — Active',
   'physical':'Late thirties. Large, economical, weight in the torso. Ex-military bearing he hasn\'t stopped performing. Subdermal armour faintly visible as ridges at the shoulders. A face that stopped being expressive in professional settings years ago.',
   'stats':[('STR','16'),('CON','15'),('SIZ','15'),('INT','11'),('POW','11'),('DEX','13'),('APP','10')],
   'derived':[('HP','16'),('PP','11'),('DB','+1D4'),('SR','28'),('Move','10')],
   'skills':[('Firearms (Pistol)','65%'),('Firearms (Rifle)','60%'),('Brawl','60%'),('Athletics','55%'),('Dodge','50%'),('Intimidate','50%'),('Drive','50%'),('Spot Hidden','45%'),('Melee','55%'),('Throw','45%'),('Climb','40%'),('Security Systems','35%'),('First Aid','35%'),('Track','30%'),('Perception','40%'),('Stealth','20%'),('Streetwise','35%'),('Firearms (Auto)','50%')],
   'equipment':['Military sidearm (2D6+2)','Collapsible combat baton (1D8+DB)','Tactical rig — mag pouches, medkit slot, comms','Night-vision monocle — 4hr battery','Trauma pads x3 (stop bleeding, +1D6 natural heal)','Six-day field rations'],
   'sp_name':'"Subdermal Combat Plates + Reflex Tap"','sp_type':'Meridian Security Group standard issue — shoulder/torso armour + spinal reflex tap',
   'sp_stats':'+2 armour (torso/shoulders)  ·  +1 DEX on combat SR  ·  Involuntary counter-attack',
   'sp_abilities':[('+2 armour (passive)','Subdermal plates at shoulders and upper torso. Cannot be removed, soaked, or directly targeted.'),('Reflex tap (+1 DEX SR)','Neural tap at spine adds 1 DEX for Strike Rank in combat only.'),('Adrenaline dump (1/combat)','On being hit for 3+ HP: free attack at +10% before end of round. Involuntary.'),('Cost','Occasional muscle spasm — sharp shoulder/neck contraction, 1-2 sec. Was 1/session. Since the tunnels job three months ago: daily.')],
   'sp_note':'Meridian issue. He kept them when he quit. Meridian\'s records show them decommissioned. This is not the same thing.',
   'background':'Ex-Meridian Security Group. Sub-Districts 1-4, four years. Quit eighteen months ago — around the time the Sub-District 7 disappearances started. Nobody connected those two facts. He has been connecting them quietly for a year and a half.',
   'hook':'Quit Meridian eighteen months ago, same time the disappearances started. He has been piecing this together. He has not said it to anyone.',
   'quote':'"I\'ve been corporate security. I\'ve been what hides things. This is different."'},

  {'name':'Tal Morgan','arch':'The Tech','meta':'Neo-Ashford Freelance','allg':'Veltris Contract — Active',
   'physical':'Mid-twenties. Something slightly caffeinated about the eyes. Too many pockets, all occupied. A clean neural interface scar behind the right ear. Fingers that move independently when thinking.',
   'stats':[('STR','11'),('CON','12'),('SIZ','11'),('INT','16'),('POW','12'),('DEX','14'),('APP','12')],
   'derived':[('HP','12'),('PP','12'),('DB','—'),('SR','25'),('Move','10')],
   'skills':[('Electronics','70%'),('Repair (Elec)','65%'),('Computer Use','60%'),('Drone Ops','60%'),('Spot Hidden','50%'),('Security Systems','55%'),('Science (Comp)','50%'),('Research','50%'),('Comms (Elec)','55%'),('Stealth','35%'),('Dodge','35%'),('Drive','40%'),('First Aid','30%'),('Perception','45%'),('Firearms (Pistol)','30%'),('Bargain','35%'),('Pick Lock','40%'),('Surveillance','45%')],
   'equipment':['Drone — palm-sized, near-silent, 20-min battery, live feed to wrist display','Hacking suite (wrist) — 1D6 min per encryption layer, physical interface needed','EMP pulse (1-use, 10m) — disables ALL electronics including augments','Tool roll — 14 pieces','Wrist display — drone feed, maps, comms, bio-scanner','Six spare power cells'],
   'sp_name':'"Neural I/O Bridge"','sp_type':'Direct machine interface — behind-ear subdermal, self-built prototype, 11 months',
   'sp_stats':'Direct interface +15% Electronics  ·  Drone sync (visual cortex)  ·  Passive net sense 20m',
   'sp_abilities':[('Direct interface','Touch-range interface with any electronic system. Electronics +15% when using direct contact.'),('Drone sync','Drone feeds directly to visual cortex. No need to look at display. -10% Spot Hidden in vicinity while synced.'),('Passive network sense','Within 20m: detects active wireless transmissions and their direction. No roll. No decryption.'),('Cost','Self-installed. Neural integration 73% stable by own assessment. Once per session: 2-3 sec feedback spike, white noise, no action possible. Has never told anyone it was self-installed.')],
   'sp_note':'Built over 18 months. Installed over a weekend. The installation is technically competent. The integration is not fully stable. The child on The Slab pressed a note into Tal\'s hand specifically.',
   'background':'Freelance tech contractor. The drone is a custom salvage build. The hacking suite is third-gen black market. The EMP is one of two built last month. The other is in a drawer at home. Tonight Tal is the one who got the note from the child.',
   'hook':'[PRIVATE] The child on The Slab approaches Tal and presses a note into their hand: Don\'t go to the plant. My dad went. He didn\'t come back the same. The paper has a faint chemical smell.',
   'quote':'"I have eyes everywhere. The problem is what the eyes are seeing."'},

  {'name':'Reina Vasquez','arch':'The Medic','meta':'Neo-Ashford Contract Medic','allg':'Veltris Contract — Active',
   'physical':'Early thirties. The calm of someone who learned calm because the alternative was worse. Medical kit worn on the hip like it is always there. Watches people\'s breathing before she watches their eyes.',
   'stats':[('STR','11'),('CON','13'),('SIZ','12'),('INT','15'),('POW','14'),('DEX','13'),('APP','13')],
   'derived':[('HP','13'),('PP','14'),('DB','—'),('SR','25'),('Move','10')],
   'skills':[('Medicine','65%'),('First Aid','70%'),('Sci (Biology)','50%'),('Perception','50%'),('Persuade','45%'),('Psychology','55%'),('Spot Hidden','45%'),('Dodge','40%'),('Drive','40%'),('Research','45%'),('Sci (Chemistry)','40%'),('Stealth','30%'),('Computer Use','35%'),('Bargain','40%'),('Brawl','30%'),('Insight','50%'),('Pharmacology','45%'),('Firearms (Pistol)','30%')],
   'equipment':['Full trauma kit — arterial clamp, wound seal, bone stabiliser, pain management','Stimulants x3 — +10% physical 1D4hrs, then -15% crash equal duration','Bio-scanner (wrist strap) — organic material and life signs within 5m','Sedative injectors x2 — CON resist or unconscious 1D4hrs','Antibiotics and infection protocols','Encrypted data-pad — three years of field observations'],
   'sp_name':'"Biometric Diagnostics Array"','sp_type':'Medical diagnostic augment — palm/fingertip subdermal sensors, Meridian Medical licensed',
   'sp_stats':'Tactile diagnosis  ·  Toxin detection  ·  Bio-scanner sync to 8m',
   'sp_abilities':[('Tactile diagnosis','Touch skin: receives temp, pulse, BP, metabolic readout. Medicine +20% when treating someone she has touched.'),('Toxin detection','Identifies presence and class of any toxin or pathogen at contact range. Specific compound needs Research or Science roll.'),('Bio-scanner sync','Wrist-strap range extends to 8m. Includes structural anomaly detection. Near the entity: reads strangely. GM tells Reina first.'),('Cost','The array reads everything. A person lying shows different biometrics than one telling the truth. Reina has learned to stop looking when she doesn\'t want to know.')],
   'sp_note':'Clause 14(f) of the user agreement: Meridian Medical retains access to anonymised diagnostic data. Reina did not read clause 14(f). Tonight she will find out what entry point means.',
   'background':'Contract medic for mid-level corporate teams. Three years of jobs that paid above standard and required discretion. A colleague at a Meridian-contracted morgue once said: the tissue appeared to be growing inward. We did not determine the entry point. The colleague has since been reassigned. Reina never forgot it.',
   'hook':'A colleague described unusual organic tissue in thoracic cavities: growing inward, entry point unknown. The colleague was reassigned. Tonight Reina will determine the entry point.',
   'quote':'"I can keep everyone alive for four more hours. After that I need to know what we\'re dealing with."'},

  {'name':'Petra Amis','arch':'The Analyst','meta':'Independent Research Contractor','allg':'Veltris Contract — Active',
   'physical':'Mid-thirties. Tidiness that is defensive rather than aesthetic. Physical notepad in a jacket pocket — unusual, deliberate. Does not carry corporate-grade equipment because corporate-grade equipment has logs. Watches exits before she watches people.',
   'stats':[('STR','10'),('CON','11'),('SIZ','11'),('INT','17'),('POW','13'),('DEX','11'),('APP','12')],
   'derived':[('HP','11'),('PP','13'),('DB','—'),('SR','22'),('Move','10')],
   'skills':[('Research','70%'),('Library Use','65%'),('Data Analysis','60%'),('Insight','60%'),('Spot Hidden','50%'),('Computer Use','50%'),('Persuade','45%'),('Psychology','50%'),('Drive','35%'),('Electronics','40%'),('Science (Var)','55%'),('Write','55%'),('Law','40%'),('Dodge','30%'),('Stealth','30%'),('Perception','55%'),('Bargain','35%'),('Cryptography','45%')],
   'equipment':['Encrypted terminal — Veltris public filings, all local data air-gapped','Signal scanner — active transmission detection, logs frequency and source','Physical notepad and pen — old habit, or paranoia. Both.','Four data sticks — different encryption standards','800 credits cash, physical, untraceable','The anonymous message — printed, folded, left inside pocket'],
   'sp_name':'"Encrypted Cortex Store"','sp_type':'Memory and data augment — temple subdermal, unknown manufacturer, received as payment 2yrs ago',
   'sp_stats':'Eidetic recall  ·  Encrypted memory partition  ·  Passive cross-indexing',
   'sp_abilities':[('Eidetic recall','Any text, image or data directly observed can be recalled exactly. Research +20% from recalled material.'),('Encrypted partition','Locked section of cortex store. 12-char passphrase only Petra knows. Holds ~40hrs high-fidelity data.'),('Passive indexing','Unconsciously cross-references new information against everything observed. Once per session: GM may tell Petra one thing the table missed.'),('Cost','Manufacturer unknown. Provided as payment in kind. It works correctly. She has spent 18 months trying to find out who made it. The locked partition contains something she put there 18 months ago and has not opened since.')],
   'sp_note':'The passphrase is the name of the client who paid her with this augment. She has never said that name aloud.',
   'background':'Independent research contractor — pattern analysis, data archaeology. Two days before this job: an anonymous encrypted message, 40 minutes to break. Inside: coordinates in Sub-District 9 and three words. Don\'t go back. She has never been to Sub-District 9. She does not know what "back" means.',
   'hook':'[PRIVATE] An anonymous message took 40 minutes to break. Coordinates in Sub-District 9: Don\'t go back. She has never been there. Tonight she finds out what the third word means.',
   'quote':'"Two days ago someone sent me three words. I\'m here to understand what the third one means."'},
]

D1_CHARS = [
  {'name':'Kira Osei-Mensah','arch':'NHS Junior Doctor (off duty)','meta':'South Bank, Sunday 17 May','allg':'Reach: Abena (mother, 74, Peckham)',
   'physical':'Late twenties. 22 hours awake — the brightness of adrenaline overriding exhaustion. Hospital lanyard still clipped to her jacket. Moves between people the way someone does who has been trained to assess urgency fast.',
   'stats':[('STR','9'),('CON','12'),('SIZ','10'),('INT','16'),('POW','14'),('DEX','13'),('APP','14')],
   'derived':[('HP','11'),('MP','14'),('DB','—'),('SR','23'),('Move','10')],
   'skills':[('First Aid','75%'),('Medicine','55%'),('Sci (Biology)','50%'),('Persuade','55%'),('Insight','55%'),('Psychology','60%'),('Spot Hidden','50%'),('Dodge','40%'),('Research','50%'),('Drive','35%'),('Computer Use','35%'),('Bargain','30%'),('Brawl','25%'),('Climb','30%'),('Language (Twi)','50%'),('Status','40%'),('Perception','50%'),('Track','20%')],
   'equipment':['Phone — 73% battery. NHS group chats already flooding.','Crossbody bag: travel card, £60 cash, Oyster','Earbuds — call to her mum attempted, ringing out','A nearly finished flat white — still warm at alert','Hospital ID badge — opens certain NHS facility doors','BNF pocket edition — always in the bag'],
   'sp_name':'What You Know That Others Don\'t','sp_type':'22 hours post-night-shift. Triage training. Hospital ID.',
   'sp_stats':'First Aid 75%  ·  Medicine 55%  ·  Triage (no roll)  ·  NHS ID access',
   'sp_abilities':[('Triage (no roll)','Once per scene: assess all wounded in view, rank by survivability in one round. Tells group who to help first.'),('Improvised medicine','Can use non-medical materials at -20% penalty: First Aid 75% becomes 55% with improvised supplies.'),('Infection assessment','Medicine 50%: assess bite victim\'s likely timeline. The answer will not be comforting.'),('Running on fumes','22hrs awake: -10% all non-medical rolls after Act Two. Medical skills unaffected — training is deeper than exhaustion.')],
   'sp_note':'Her mother Abena, 74, lives alone in Peckham. The infection spread from Elephant & Castle. Peckham is between the group and the river. Kira knows this geography. She knows what it means. She has not said it yet.',
   'background':'Junior doctor, 6 months post-qualification, A&E rotation. Running on post-shift adrenaline and the clarity that comes from exhaustion looping back around. The group\'s best medical resource. Also 22 hours without sleep, trying to reach a 74-year-old who is not picking up her phone.',
   'hook':'Her mother Abena, 74, alone in Peckham. The infection started at Elephant & Castle and is moving east through Peckham. Kira has made this calculation. She has not said it aloud.',
   'quote':'"Tell me what you\'re feeling. Specifically. Not fine — specifically."'},

  {'name':'Dev Krishnamurthy','arch':'Freelance software engineer','meta':'Borough Market café, Sunday','allg':'Reach: flatmate near Old Street',
   'physical':'Late twenties. Headphones half-on the way people wear them when they want to be left alone but also available. Laptop bag, worn strap. The slightly unfocused expression of someone who has been in their own head all morning.',
   'stats':[('STR','10'),('CON','11'),('SIZ','11'),('INT','17'),('POW','12'),('DEX','13'),('APP','12')],
   'derived':[('HP','11'),('MP','12'),('DB','—'),('SR','24'),('Move','10')],
   'skills':[('Computer Use','75%'),('Electronics','65%'),('Library Use','60%'),('Research','55%'),('Sci (Maths)','45%'),('Sci (Computing)','70%'),('Spot Hidden','45%'),('Insight','40%'),('Dodge','35%'),('Drive','40%'),('Bargain','30%'),('Persuade','35%'),('Brawl','25%'),('Climb','30%'),('Stealth','30%'),('Perception','45%'),('Track','20%'),('Psychology','30%')],
   'equipment':['MacBook Pro — 81% battery, tracking spread on four social media threads','Phone — 94% battery, scanner app notifications since 9:40 AM','Laptop bag: charger, USB hub, notebook (unused), protein bar','AirPods (full charge)','Wallet: £45 cash, three cards, Oyster (£8.40)','Voice note from flatmate about spare keys — unanswered, one hour old'],
   'sp_name':'What You Know That Others Don\'t','sp_type':'Emergency services scanner app. Has been watching since 9:40 AM — 67 minutes before the alert.',
   'sp_stats':'Computer Use 75%  ·  Early data (pre-alert)  ·  Network access  ·  Signal mapping',
   'sp_abilities':[('Early data','Tracked spread since 9:40 AM: knows Elephant & Castle origin, three smoke plume locations, approximate spread rate. The group should ask him what he knows.'),('Network access','While signal exists: aggregate public info, open CCTV feeds, transport data, social media.'),('Signal mapping','Map cell tower activity to identify where people are gathering — and where they are not. 20-min task with laptop.'),('Cost — what he hasn\'t said','He has been sitting on this data for over an hour. He did not call anyone. Did not post. He was watching.')],
   'sp_note':'Dev has known something was wrong since 9:40 AM. He watched it in real time. He told no one. Tonight, data becomes geography.',
   'background':'Freelance software engineer, security and infrastructure clients. Works from coffee shops. In London four years. Knows the city through data rather than geography. Tonight one becomes the other.',
   'hook':'Has been tracking the spread since 9:40 AM — an hour before the alert. He has more information than anyone at this table. He has told no one.',
   'quote':'"I\'ve been watching this develop for an hour. I should have said something. I know."'},

  {'name':'Maggie Donnelly','arch':'Retired Metropolitan Police (22 yrs)','meta':'Jubilee Walkway, Sunday','allg':'Reach: Cara (daughter, Deptford)',
   'physical':'Early sixties. Sunday walking gear — practical coat, good shoes, a pace that covers ground without appearing to hurry. The assessment in her eyes is continuous and automatic. She retired six years ago and has not stopped doing the job.',
   'stats':[('STR','12'),('CON','13'),('SIZ','12'),('INT','15'),('POW','14'),('DEX','11'),('APP','12')],
   'derived':[('HP','13'),('MP','14'),('DB','—'),('SR','23'),('Move','10')],
   'skills':[('Persuade','70%'),('Psychology','65%'),('Spot Hidden','65%'),('Insight','70%'),('Law','60%'),('Brawl','55%'),('First Aid','50%'),('Dodge','55%'),('Drive','60%'),('Intimidate','60%'),('Firearms (Pistol)','45%'),('Track','45%'),('Athletics','45%'),('Search','55%'),('Streetwise','50%'),('Stealth','35%'),('Perception','65%'),('Climb','40%')],
   'equipment':['Phone — 62% battery. Cara not answering. Voicemail.','Practical coat with pockets, water bottle, small first aid kit (always)','Expired police warrant card (laminated) — she does not know if it will work','Wallet: £120 cash (always), Oyster, two cards','Pocket notepad and two pens — old habit','A flapjack, half-eaten, right pocket'],
   'sp_name':'What You Know That Others Don\'t','sp_type':'First on scene, Tavistock Square 2005. 22 years crowd management. Pattern recognition.',
   'sp_stats':'Persuade 70% in evacuation  ·  Scene assessment (no roll)  ·  Warrant card (1-use, 60%)',
   'sp_abilities':[('Scene assessment (no roll)','Assess any crowd, group or space for threat level, routes, and key individuals in one round.'),('Authority','Persuade +20% in any crowd management or evacuation scenario.'),('Tavistock memory','Has been first on scene at mass casualty. -10% to SAN loss from human casualties. Experience, not callousness.'),('Warrant card (1-use, 60%)','Expired 6 years. Laminated. Show with complete confidence: 60% chance they don\'t check the date.')],
   'sp_note':'Cara lives in Deptford. Deptford is south-east. The infection is moving east from Elephant & Castle. Maggie has made this calculation. The tension between her duty to this group and her need to reach her daughter is the engine of her character.',
   'background':'Twenty-two years Met Police, retired at DCI level. Knows the South Bank better than her own flat. First on scene Tavistock Square 2005. Handled riots, the 2011 disorder, a gas explosion in 2019. None prepared her for a person standing waist-deep in the Thames, head tilted, in no apparent distress.',
   'hook':'Cara is in Deptford. The infection started at Elephant & Castle and is moving east. Maggie has made this calculation. The tension between getting these people out and reaching her daughter is the engine of her character.',
   'quote':'"Move. I\'ll explain why while we\'re moving."'},

  {'name':'Olu Adeyemi','arch':'Security guard, The Shard','meta':'Shard lobby, Sunday overtime','allg':'Reach: No family in London — the group becomes the motivation',
   'physical':'Early thirties. Large, unhurried, the calm of someone who handles other people\'s panic professionally. Security uniform. A radio on his belt that was already not working properly when his supervisor handed it to him. His coffee from home is on the security desk.',
   'stats':[('STR','15'),('CON','14'),('SIZ','14'),('INT','13'),('POW','13'),('DEX','12'),('APP','13')],
   'derived':[('HP','15'),('MP','13'),('DB','+1D4'),('SR','26'),('Move','10')],
   'skills':[('Brawl','65%'),('Spot Hidden','60%'),('Security Systems','60%'),('Athletics','60%'),('Persuade','45%'),('Drive','55%'),('Intimidate','55%'),('Dodge','55%'),('First Aid','40%'),('Climb','55%'),('Electronics','40%'),('Perception','65%'),('Stealth','40%'),('Track','35%'),('Firearms (Pistol)','40%'),('Melee','50%'),('Search','50%'),('Streetwise','45%')],
   'equipment':['Security radio — intermittently functional. Fragments only.','Shard keycard — all staff areas, service levels, roof','Security baton (1D6)','Personal phone — 91% battery. His mum picked up this morning.','Shard master key ring — 17 keys','Coffee from home in insulated mug. Probably cold.'],
   'sp_name':'What You Know That Others Don\'t','sp_type':'The Shard: CCTV, radio, roof access, defensible position, keys to everything.',
   'sp_stats':'Building access (full)  ·  Radio fragments  ·  CCTV 200m radius  ·  Shard sightlines',
   'sp_abilities':[('Full building access','Keycard and key access to all Shard staff/service areas. From upper floors: sees south and east — three smoke plumes, all south of where expected.'),('Radio fragments','Picks up fragmented police transmissions. Key fragment: Elephant & Castle first reports at 7:14 AM — 2 hrs before the alert. Needs the group to interpret it.'),('CCTV 200m','Security terminal, Computer/Electronics 40%. What it already shows is worse than the street sounds suggest.'),('The group becomes the motivation','No immediate family in London. By Act Two, this group is why he is still here. The player should feel this happen, not be told it.')],
   'sp_note':'The radio fragment about the cordon — "north of the river" — lands hardest on Olu. He is holding the radio when it comes through. Give him the moment where he doesn\'t say anything.',
   'background':'Shard security, two years. Moved to London from Birmingham three years ago. No family here. His mum picked up this morning; that fact will anchor him. Has handled everything the Shard security role requires. Has never handled something where the emergency services are the ones giving fragments instead of answers.',
   'hook':'The cordon radio fragment — "north of the river" — is his to deliver. He has been trying to do his job. He has trusted the institution. Give him the moment when the institution\'s logic becomes clear.',
   'quote':'"I have keys to everything in this building and I can see three miles from the roof. Use that before we lose it."'},

  {'name':'Priya Mehta','arch':'Science journalist','meta':'Southbank Centre, Sunday','allg':'Reach: editor (has Meridian documents)',
   'physical':'Early thirties. Press lanyard still on — force of habit. A notebook in hand before she consciously decided to take it out. The tension of someone whose instinct is to find the story and whose training says find it very carefully.',
   'stats':[('STR','9'),('CON','11'),('SIZ','10'),('INT','17'),('POW','13'),('DEX','12'),('APP','14')],
   'derived':[('HP','11'),('MP','13'),('DB','—'),('SR','22'),('Move','10')],
   'skills':[('Library Use','70%'),('Research','70%'),('Insight','65%'),('Write','65%'),('Persuade','60%'),('Psychology','55%'),('Sci (Biology)','55%'),('Spot Hidden','50%'),('Computer Use','50%'),('Sci (Chemistry)','50%'),('Drive','35%'),('Dodge','30%'),('Law','30%'),('Climb','30%'),('Stealth','30%'),('Perception','55%'),('Language (Hindi)','60%'),('Bargain','45%')],
   'equipment':['Phone — 88% battery. Editor\'s message: "Something came in. Can we talk Monday?"','Notebook (half-full) and three pens — she will fill the rest tonight','Press lanyard — Southbank Centre media pass (valid)','Laptop in shoulder bag — research plus other things','Voice recorder (full battery)','Wallet: £35 cash, press card, two cards'],
   'sp_name':'What You Know That Others Don\'t','sp_type':'Editor has Meridian Biosciences documents. They arrived 48 hours before the outbreak.',
   'sp_stats':'Research 70%  ·  Source assessment  ·  Meridian thread  ·  Press access (1-use)',
   'sp_abilities':[('Meridian thread','Editor has Meridian Biosciences documents. Research 70% or Psychology 55%: begin piecing together the Meridian-to-outbreak connection from the editor\'s message and public records.'),('Source assessment','Evaluate credibility of any information source or account: Insight 65%. Critical in a world where everyone speculates.'),('Story vs group','Best positioned to understand the truth. Whether she uses it to help the group or document the story is a genuine player choice. Neither is wrong.'),('Press access (1-use)','The lanyard is valid. In the first two hours of an emergency, officials sometimes still respond to press credentials.')],
   'sp_note':'Her editor has the Meridian documents. They arrived 48 hours before the outbreak. Priya has a very good instinct about what they mean. She has been choosing not to use it. Tonight she will not have that option.',
   'background':'Science journalist, primarily biology and public health. Her editor\'s message is about Meridian Biosciences. She has been choosing not to use her instincts. Tonight, everything she has been choosing not to know becomes necessary.',
   'hook':'Her editor has Meridian Biosciences documents that arrived 48 hours before the outbreak. She filed the message for Monday. Tonight everything she chose not to know becomes necessary.',
   'quote':'"I need to understand what this is before I can help anyone survive it."'},

  {'name':'Tom Becker','arch':'Scaffolding worker','meta':'Waterloo Road side street, Sunday','allg':'Reach: his van (exit route) and his mum (no answer)',
   'physical':'Late twenties. Work clothes, high-vis jacket still on. Van keys in his right hand. A bag of tools. The unaffected physicality of someone who climbs things and lifts things for a living without considering this unusual.',
   'stats':[('STR','14'),('CON','14'),('SIZ','13'),('INT','12'),('POW','11'),('DEX','13'),('APP','11')],
   'derived':[('HP','14'),('MP','11'),('DB','+1D4'),('SR','26'),('Move','10')],
   'skills':[('Craft (Construction)','70%'),('Athletics','65%'),('Climb','70%'),('Mechanics','60%'),('Drive','65%'),('Brawl','55%'),('Spot Hidden','50%'),('Throw','55%'),('Melee','50%'),('Dodge','50%'),('Perception','55%'),('Search','50%'),('Streetwise','45%'),('Intimidate','40%'),('First Aid','35%'),('Track','40%'),('Electronics (Basic)','25%'),('Security Systems','25%')],
   'equipment':['Tool bag: hammer (1D6+DB), bolt cutters, crowbar (1D8+DB), screwdrivers, zip ties','High-vis jacket — visibility is a mixed blessing tonight','Phone — 44% battery. Voicemail left for mum. No callback.','Van keys (parked near Lambeth North — across the river or the long way round)','Work gloves — thick leather, 1pt hand armour, -10% fine motor','Half a water bottle and an energy bar'],
   'sp_name':'What You Know That Others Don\'t','sp_type':'Can build, break into, or assess structural stability of anything. Has a van.',
   'sp_stats':'Craft 70%  ·  Structural instinct (no roll)  ·  Van across the river  ·  Tool bag',
   'sp_abilities':[('Structural instinct (no roll)','Assess any building, barrier or structure for load capacity, weak points, and improvised fortification potential.'),('Break and build','Craft (Construction) 70% for barriers, improvised tools, locked space access, or climbing points. Tool bag: +10%.'),('The van','Near Lambeth North — across the river, or the long way round. Has tools, rope, full diesel tank, radio. Whether reaching it is worth the detour is a genuine strategic decision.'),('His mum','She didn\'t answer this morning. He left a voicemail. She still hasn\'t called back. He is carrying this. He is not saying anything about it.')],
   'sp_note':'Tom\'s van is the scenario\'s most practical resource. It is also across the river. Whether to go for it — and whether Tom\'s real motivation is the van or what it represents — is a player choice.',
   'background':'Scaffolding worker, eight years. South London born and raised. Knows physical geography — what you can climb, what breaks, what holds. Called his mum this morning. She didn\'t pick up. Left a voicemail that was mostly road noise. She still hasn\'t called back.',
   'hook':'His mum didn\'t answer this morning. Still hasn\'t called back. He will not say this unless asked. If asked, he will answer plainly and change the subject.',
   'quote':'"Tell me what needs breaking or what needs holding. I can do both."'},
]

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def build_pdf(path, CHARS, t, cover_title, cover_sub, cover_byline, rules):
    S  = make_styles(t)
    LW = UW * 0.62           # left col — stats/skills
    RW = UW * 0.36           # right col — portrait placeholder (2% gap)
    SKH= (LW - 4*mm) / 2    # half-col for skill table

    # Portrait placeholder height = same ratio as Stormbringer (640/427)
    port_w = RW - 2
    port_h = port_w * (640/427)

    doc = BaseDocTemplate(path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN+4*mm, bottomMargin=MARGIN+8*mm)
    cover_frame   = Frame(0,0,PAGE_W,PAGE_H,id='cover')
    content_frame = Frame(MARGIN, MARGIN+8*mm, UW, PAGE_H-2*MARGIN-12*mm, id='content')
    doc.addPageTemplates([
        PageTemplate(id='cover',  frames=[cover_frame],   onPage=make_cover_bg(t)),
        PageTemplate(id='normal', frames=[content_frame], onPage=make_page_bg(t)),
    ])
    story = []

    # ── COVER ──────────────────────────────────────────────────────────────
    story.append(Spacer(1,72))
    story.append(Paragraph(cover_title,  S['cover_title']))
    story.append(Spacer(1,5))
    story.append(Paragraph(cover_sub,    S['cover_sub']))
    story.append(Spacer(1,4))
    story.append(Paragraph(cover_byline, S['cover_byline']))
    story.append(Spacer(1,14))
    story.append(OrnRule(UW,t))
    story.append(Spacer(1,10))

    roster=[[Paragraph(f"<b>{c['name']}</b>",S['cover_name']),
             Paragraph(c['arch'],             S['cover_arch']),
             Paragraph(c.get('meta',''),       S['cover_meta'])]for c in CHARS]
    rt=Table(roster,colWidths=[UW*0.38,UW*0.38,UW*0.24])
    rt.setStyle(TableStyle([
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[t.cover_row1,t.cover_row2]),
        ('LINEBELOW',(0,0),(-1,-1),0.4,t.rule),
        ('LINEABOVE',(0,0),(-1,0),1.0,t.accent),('LINEBELOW',(0,-1),(-1,-1),1.0,t.accent),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ]))
    story.append(rt)
    story.append(Spacer(1,12))
    story.append(OrnRule(UW,t))
    story.append(Spacer(1,8))
    story.append(Paragraph("QUICK REFERENCE",S['rules_head']))
    rlt=Table([[Paragraph(cell,S['cover_rule'])for cell in row]for row in rules],colWidths=[UW/3]*3)
    rlt.setStyle(TableStyle([
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[t.cover_row1,t.cover_row2]),
        ('GRID',(0,0),(-1,-1),0.4,t.rule),('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(rlt)
    story.append(Spacer(1,8))
    story.append(Paragraph("Hand sheets face-down. Players choose by archetype, not stats.",S['cover_note']))

    story.append(NextPageTemplate('normal'))
    story.append(PageBreak())

    # ── CHARACTER PAGES ──────────────────────────────────────────────────────
    for char in CHARS:
        max_hp  = int(next(v for k,v in char['derived'] if k in ('HP',)))
        max_san = int(next((v for k,v in char['derived'] if k in ('MP','PP')), 10))

        # ── FRONT PAGE ──────────────────────────────────────────────────────
        story.append(CharHeader(char['name'],char['arch'],char['meta'],char['allg'],UW,t))
        story.append(Spacer(1,4))

        # Left col: characteristics + skills
        sk=char['skills']
        if len(sk)%2: sk=sk+[('','')]
        mid=len(sk)//2
        sk_rows=[]
        for (la,lv),(ra,rv) in zip(sk[:mid],sk[mid:]):
            sk_rows.append([
                Paragraph(la,  S['body_sm']),
                Paragraph(f"<b>{lv}</b>",S['body_sm']),
                Paragraph(ra,  S['body_sm']),
                Paragraph(f"<b>{rv}</b>",S['body_sm']),
            ])
        skt=Table(sk_rows,colWidths=[SKH*0.72,SKH*0.28,SKH*0.72,SKH*0.28])
        skt.setStyle(TableStyle([
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[t.row1,t.row2]),
            ('LINEBELOW',(0,0),(-1,-1),0.3,t.rule),
            ('LINEAFTER',(1,0),(1,-1),0.5,t.rule),
            ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),3),
            ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),
            ('ALIGN',(1,0),(1,-1),'RIGHT'),('ALIGN',(3,0),(3,-1),'RIGHT'),
        ]))

        left_items=[
            [SectionBanner("Characteristics",LW-4,t)],
            [Spacer(1,2)],
            [StatBlock(char['stats'],char['derived'],LW-4,t)],
            [Spacer(1,4)],
            [SectionBanner("Skills",LW-4,t)],
            [Spacer(1,2)],
            [skt],
        ]
        left_inner=Table(left_items,colWidths=[LW-4])
        left_inner.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))

        right_ph=PortraitPlaceholder(char['name'],port_w,port_h,t)

        two_col=Table([[left_inner,right_ph]],colWidths=[LW,RW])
        two_col.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
            ('ALIGN',(1,0),(1,-1),'RIGHT'),
            ('LINEBEFORE',(1,0),(1,-1),0.5,t.accent),
        ]))
        story.append(two_col)
        story.append(Spacer(1,4))

        # Equipment
        story.append(SectionBanner("Equipment",UW,t))
        story.append(Spacer(1,2))
        eqt=Table([[Paragraph(f"\u2022 {item}",S['body_sm'])]for item in char['equipment']],colWidths=[UW])
        eqt.setStyle(TableStyle([
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[t.row1,t.row2]),
            ('LINEBELOW',(0,0),(-1,-1),0.3,t.rule),
            ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),4),
            ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),
        ]))
        story.append(eqt)
        story.append(Spacer(1,5))

        # HP Track (full width)
        story.append(HPTrack(max_hp,UW,t))
        story.append(Spacer(1,5))

        # SAN Track (full width, green boxes)
        story.append(HPTrack(max_san,UW,t,
            label="SANITY POINTS",
            fill=t.san_box_fill, fill5=t.san_box_5th,
            border=t.san_box_border, num=t.san_num))

        story.append(PageBreak())

        # ── BACK PAGE ────────────────────────────────────────────────────────
        story.append(BackHeader(char['name'],char['arch'],UW,t))
        story.append(Spacer(1,6))
        story.append(Paragraph(f"<i>{char['physical']}</i>",S['italic_sm']))
        story.append(Spacer(1,8))

        # Special section (augment / what you know)
        story.append(SectionBanner(t.special_label_str,UW,t,special=True))
        story.append(Spacer(1,3))
        dc=[Paragraph(char['sp_name'],S['sp_title']),
            Paragraph(char['sp_type'],S['sp_label']),
            Paragraph(char['sp_stats'],S['sp_body'])]
        for abn,abd in char['sp_abilities']:
            dc.append(Paragraph(f"<b>{abn}:</b>  {abd}",S['sp_body']))
        dc.append(Paragraph(f"<i>{char['sp_note']}</i>",S['sp_body']))
        di=Table([[el]for el in dc],colWidths=[UW-18])
        di.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),t.special_bg),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
        do=Table([[di]],colWidths=[UW])
        do.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),t.special_bg),
            ('BOX',(0,0),(0,0),1.2,t.special_border),
            ('LEFTPADDING',(0,0),(0,0),9),('RIGHTPADDING',(0,0),(0,0),9),
            ('TOPPADDING',(0,0),(0,0),5),('BOTTOMPADDING',(0,0),(0,0),5)]))
        story.append(do)
        story.append(Spacer(1,6))

        # Background
        story.append(SectionBanner("Background",UW,t))
        story.append(Spacer(1,4))
        story.append(Paragraph(char['background'],S['body']))
        story.append(Spacer(1,5))

        # Hook
        ht=Table([[Paragraph("PERSONAL HOOK:",S['hook_label']),
                   Paragraph(char['hook'],     S['hook_body'])]],
                 colWidths=[28*mm,UW-28*mm])
        ht.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),t.hook_bg),
            ('BOX',(0,0),(-1,-1),0.8,t.hook_border),
            ('LINEBEFORE',(0,0),(0,-1),3,t.hook_bar),
            ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
            ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        story.append(ht)
        story.append(Spacer(1,6))

        # Quote
        story.append(OrnRule(UW,t))
        story.append(Paragraph(char['quote'],S['quote']))
        story.append(OrnRule(UW,t))
        story.append(Spacer(1,8))

        # Notes
        story.append(SectionBanner("Notes",UW,t))
        story.append(Spacer(1,5))
        story.append(NotesBlock(UW,t,lines=8))
        story.append(PageBreak())

    doc.build(story)
    print(f"Done: {path}")

# ── RUN ────────────────────────────────────────────────────────────────────────

NC = night_crawler_theme()
D1 = day_one_theme()

NC_RULES=[
    ['HP = (CON+SIZ)/2  round up', 'PP = POW', 'DB: STR+SIZ 17-24 = None'],
    ['SR = DEX + INT', 'Attack: D100 ≤ skill%', 'Augment effects: see back page'],
    ['SAN loss: success = less loss', 'DB 25-32: +1D4 | 33-40: +1D6','Unconscious at 0 HP'],
]
D1_RULES=[
    ['HP = (CON+SIZ)/2  round up', 'MP = POW', 'DB: STR+SIZ 17-24 = None'],
    ['SR = DEX + INT', 'Attack: D100 ≤ skill%', 'Zombie: head shot only for instant kill'],
    ['Bite: CON resist or symptomatic', 'DB 25-32: +1D4 | 33-40: +1D6','SAN loss on zombie encounter'],
]

build_pdf('/mnt/user-data/outputs/brp-night-crawler-v2.pdf', NC_CHARS, NC,
    "THE NIGHT CRAWLER",
    "Player Character Reference — Neo-Ashford, 2087",
    "Basic Role-Playing  ·  Event 91  ·  ChaosiumCon 2026",
    NC_RULES)

build_pdf('/mnt/user-data/outputs/brp-day-one-v2.pdf', D1_CHARS, D1,
    "DAY ONE — London Falls",
    "Player Character Reference — South Bank, 17 May 2026",
    "Basic Role-Playing  ·  Event 159  ·  ChaosiumCon 2026",
    D1_RULES)
