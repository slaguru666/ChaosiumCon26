#!/usr/bin/env python3
"""
Call of Cthulhu 7e Character Sheets
Event 92 — Last Train to Coney Island (NYC, 1979)
ChaosiumCon 2026
"""

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

pdfmetrics.registerFont(TTFont('SerBold', '/tmp/source-serif-bold.ttf'))
pdfmetrics.registerFont(TTFont('SerReg',  '/tmp/source-serif-regular.ttf'))
pdfmetrics.registerFont(TTFont('SerIt',   '/tmp/source-serif-italic.ttf'))

PAGE_W, PAGE_H = A4
MARGIN = 17 * mm
UW = PAGE_W - 2 * MARGIN

# ═══════════════════════════════════════════════════════════════════════════════
# THEME — 1979 NYC Subway: newsprint concrete, transit charcoal, MTA orange
# ═══════════════════════════════════════════════════════════════════════════════

class T: pass

def last_train_theme():
    t = T()
    t.name = 'ltci'
    # ── Page ──
    t.page_bg         = colors.HexColor('#ECEADF')   # newsprint/concrete
    t.parchment       = colors.HexColor('#ECEADF')
    t.parchment_dark  = colors.HexColor('#E0DCCC')
    # ── Header (near-black charcoal) ──
    t.header_bg       = colors.HexColor('#0E0E0C')
    t.header_inner    = colors.HexColor('#1A1A14')
    t.header_border   = colors.HexColor('#E06000')   # transit orange
    t.header_name     = colors.HexColor('#F0ECD8')
    t.header_sub      = colors.HexColor('#E8883A')   # warm orange on dark
    t.header_right    = colors.HexColor('#C8A878')
    # ── Section banners ──
    t.banner_bg       = colors.HexColor('#1A1A14')
    t.banner_text     = colors.HexColor('#F0ECD8')
    t.banner_special  = colors.HexColor('#0A0C08')
    # ── Characteristics ──
    t.stat_hdr_bg     = colors.HexColor('#1A1A14')
    t.stat_hdr_text   = colors.HexColor('#E8883A')   # orange on dark
    t.stat_cell_bg    = colors.HexColor('#E0DCCC')
    t.stat_cell_text  = colors.HexColor('#0E0E08')
    # ── Derived stats strip ──
    t.derived_bg      = colors.HexColor('#1A1A14')
    t.derived_label   = colors.HexColor('#E8883A')
    t.derived_val     = colors.HexColor('#F0ECD8')
    # ── Skill / equipment rows ──
    t.row1            = colors.HexColor('#ECEADF')
    t.row2            = colors.HexColor('#E0DCCC')
    t.row_text        = colors.HexColor('#0E0E08')
    t.rule            = colors.HexColor('#5A4820')
    # ── Brief box (dark) ──
    t.special_bg      = colors.HexColor('#080808')
    t.special_border  = colors.HexColor('#E06000')
    t.special_title   = colors.HexColor('#E8883A')
    t.special_label   = colors.HexColor('#D07030')
    t.special_body    = colors.HexColor('#EAD8B8')
    # ── HP track (red-orange) ──
    t.hp_label        = colors.HexColor('#6A1000')
    t.hp_max          = colors.HexColor('#6A1000')
    t.hp_box_fill     = colors.HexColor('#FFF0E4')
    t.hp_box_5th      = colors.HexColor('#FFCCA0')
    t.hp_box_border   = colors.HexColor('#CC3800')
    t.hp_num          = colors.HexColor('#3A0800')
    # ── SAN track (subway tile green) ──
    t.san_label       = colors.HexColor('#0A2818')
    t.san_box_fill    = colors.HexColor('#E4F4EC')
    t.san_box_5th     = colors.HexColor('#A8DCC0')
    t.san_box_border  = colors.HexColor('#1A6040')
    t.san_num         = colors.HexColor('#082010')
    # ── Luck (blue) ──
    t.luck_label      = colors.HexColor('#0A1850')
    t.luck_box_fill   = colors.HexColor('#EAF0FF')
    t.luck_box_5th    = colors.HexColor('#BBCCF0')
    t.luck_box_border = colors.HexColor('#1A3088')
    t.luck_num        = colors.HexColor('#0A1040')
    # ── Portrait placeholder ──
    t.port_bg         = colors.HexColor('#0E0E0C')
    t.port_border     = colors.HexColor('#E06000')
    t.port_text       = colors.HexColor('#3A3820')
    t.port_label      = colors.HexColor('#E8883A')
    # ── Personal hook box ──
    t.hook_bg         = colors.HexColor('#FAF6E8')
    t.hook_border     = colors.HexColor('#E06000')
    t.hook_bar        = colors.HexColor('#E06000')
    t.hook_label      = colors.HexColor('#5A2000')
    t.hook_body       = colors.HexColor('#0E0E08')
    # ── Back header ──
    t.back_bg         = colors.HexColor('#0E0E0C')
    t.back_border     = colors.HexColor('#E06000')
    t.back_sub        = colors.HexColor('#E8883A')
    # ── Body ──
    t.body            = colors.HexColor('#0E0E08')
    t.italic          = colors.HexColor('#2A2410')
    t.quote           = colors.HexColor('#5A2800')
    # ── Cover ──
    t.cover_row1      = colors.HexColor('#0E0E0C')
    t.cover_row2      = colors.HexColor('#1A1A14')
    t.cover_name      = colors.HexColor('#F0ECD8')
    t.cover_arch      = colors.HexColor('#E8883A')
    t.cover_meta      = colors.HexColor('#C8A870')
    t.cover_note      = colors.HexColor('#C8A870')
    t.cover_title     = colors.HexColor('#E8883A')
    t.cover_sub       = colors.HexColor('#D07030')
    t.cover_byline    = colors.HexColor('#7A6430')
    t.cover_rule_body = colors.HexColor('#F0ECD8')
    t.accent          = colors.HexColor('#E06000')   # transit orange
    t.footer          = colors.HexColor('#5A4820')
    t.footer_text     = "Last Train to Coney Island  ·  Call of Cthulhu 7e  ·  Event 92  ·  ChaosiumCon 2026"
    t.special_label_str = "WARRIOR'S BRIEF"
    t.back_note       = "New York City, 1979  ·  Background & Notes"
    t.font_head       = 'SerBold'
    t.font_body       = 'SerReg'
    t.font_body_bold  = 'SerBold'
    return t

# STYLES
# ═══════════════════════════════════════════════════════════════════════════════

def make_styles(t):
    fh, fb, fbb = t.font_head, t.font_body, t.font_body_bold
    return {
        'cover_title': ParagraphStyle('ct', fontName=fh,  fontSize=28, textColor=t.cover_title,  alignment=TA_CENTER, leading=34, spaceAfter=4),
        'cover_sub':   ParagraphStyle('cs', fontName=fh,  fontSize=11, textColor=t.cover_sub,    alignment=TA_CENTER, leading=15, spaceAfter=2),
        'cover_byline':ParagraphStyle('cb', fontName=fb,  fontSize=8,  textColor=t.cover_byline, alignment=TA_CENTER, leading=12),
        'cover_name':  ParagraphStyle('cn', fontName=fh,  fontSize=11, textColor=t.cover_name,   leading=15),
        'cover_arch':  ParagraphStyle('ca', fontName=fb,  fontSize=9,  textColor=t.cover_arch,   leading=13),
        'cover_meta':  ParagraphStyle('cm', fontName=fb,  fontSize=8,  textColor=t.cover_meta,   leading=12),
        'cover_rule':  ParagraphStyle('cr', fontName='Helvetica-Bold', fontSize=8, textColor=t.cover_rule_body, alignment=TA_CENTER, leading=11),
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
        'italic_sm':   ParagraphStyle('is', fontName='Times-Italic', fontSize=8.5, textColor=t.italic, leading=12, alignment=TA_JUSTIFY),
        'notes_head':  ParagraphStyle('nh', fontName=fh,  fontSize=9,  textColor=t.banner_text,  leading=13),
        'wt_hdr':      ParagraphStyle('wth',fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white,  leading=10),
        'wt_body':     ParagraphStyle('wtb',fontName=fb,  fontSize=7.5, textColor=t.row_text,    leading=10),
        'wt_body_c':   ParagraphStyle('wtc',fontName=fbb, fontSize=7.5, textColor=t.row_text,    leading=10, alignment=TA_CENTER),
        'wt_dodge':    ParagraphStyle('wtd',fontName='Helvetica-Bold', fontSize=8.5, textColor=t.derived_label, leading=12),
        'ref_title':   ParagraphStyle('rft',fontName=fh,  fontSize=16, textColor=t.accent,       alignment=TA_CENTER, leading=20, spaceAfter=2),
        'ref_sub':     ParagraphStyle('rfs',fontName='Times-Italic',   fontSize=9, textColor=t.italic, alignment=TA_CENTER, leading=12),
        'ref_hdr':     ParagraphStyle('rfh',fontName='Helvetica-Bold', fontSize=7, textColor=colors.white, leading=9),
        'ref_body':    ParagraphStyle('rfb',fontName='Times-Roman',    fontSize=8, textColor=t.body, leading=10),
        'ref_bold':    ParagraphStyle('rfc',fontName='Helvetica-Bold', fontSize=8, textColor=t.body, leading=10),
        'ref_note':    ParagraphStyle('rfn',fontName='Times-Italic',   fontSize=7.5, textColor=t.italic, alignment=TA_CENTER, leading=10),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FLOWABLES
# ═══════════════════════════════════════════════════════════════════════════════

class OrnRule(Flowable):
    """Ornamental rule with diamond accents — Art Deco style."""
    def __init__(self, width, t): super().__init__(); self._t=t; self.width=width; self.height=10
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; t=self._t; mid=self.width/2
        c.setStrokeColor(t.accent); c.setFillColor(t.accent); c.setLineWidth(0.6)
        c.line(0,5,mid-14,5); c.line(mid+14,5,self.width,5)
        # Central triple-diamond motif
        for x,s in [(mid-10,3),(mid,4),(mid+10,3)]:
            c.saveState(); c.translate(x,5); c.rotate(45); c.rect(-s/2,-s/2,s,s,fill=1,stroke=0); c.restoreState()
        # End tick marks
        for ex in [0, self.width]:
            c.saveState(); c.translate(ex,5); c.rotate(45); c.rect(-2,-2,4,4,fill=1,stroke=0); c.restoreState()


class CharHeader(Flowable):
    """Character name banner with Art Deco styling."""
    def __init__(self, name, arch, meta, allg, width, t):
        super().__init__(); self._n=name; self._a=arch; self._m=meta; self._g=allg
        self.width=width; self.height=52; self._t=t
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; t=self._t; w,h=self.width,self.height
        # Background layers
        c.setFillColor(t.header_bg); c.roundRect(0,0,w,h,3,fill=1,stroke=0)
        c.setFillColor(t.header_inner); c.roundRect(2,2,w-4,h-4,2,fill=1,stroke=0)
        # Gold border
        c.setStrokeColor(t.header_border); c.setLineWidth(1.2); c.roundRect(1,1,w-2,h-2,3,fill=0,stroke=1)
        # Inner accent line (thinner secondary line)
        c.setStrokeColor(t.accent); c.setLineWidth(0.4); c.line(12,h-31,w-12,h-31)
        # Decorative side brackets (Art Deco corner elements)
        c.setStrokeColor(t.accent); c.setLineWidth(1.0)
        for x0,dx in [(6,1),(w-6,-1)]:
            c.line(x0,h-8,x0+dx*12,h-8); c.line(x0,h-8,x0,h-22)
        # Character name
        c.setFillColor(t.header_name); c.setFont(t.font_head,20)
        c.drawString(14,h-22,self._n)
        # Archetype · scenario
        c.setFillColor(t.header_sub); c.setFont('Helvetica',8.5)
        c.drawString(14,h-38,f"{self._a}  ·  {self._m}")
        # Connection (right-aligned)
        c.setFillColor(t.header_right); c.setFont('Helvetica',7.5)
        c.drawRightString(w-12,h-38,self._g)
        # Corner diamond accents
        c.setFillColor(t.accent)
        for cx,cy in [(6,h-6),(w-6,h-6),(6,6),(w-6,6)]:
            c.saveState(); c.translate(cx,cy); c.rotate(45); c.rect(-2,-2,4,4,fill=1,stroke=0); c.restoreState()


class StatBlock(Flowable):
    """Eight CoC characteristic boxes + dark derived-stats strip.
    Header band split: label (top) · thin rule · stat×5% (bottom).
    Light cell below has the main stat value."""
    def __init__(self, stats, derived, width, t):
        super().__init__(); self._s=stats; self._d=derived; self.width=width; self._t=t
        self.height = 70
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; t=self._t; w=self.width; n=len(self._s); bw=(w-4)/n
        BOX_H=44; HDR_H=16
        for i,(label,val) in enumerate(self._s):
            x=i*bw+2

            # Dark header cell (full height - no percentile band needed)
            c.setFillColor(t.stat_hdr_bg)
            c.rect(x, BOX_H-HDR_H, bw-1, HDR_H, fill=1, stroke=0)
            # Light value cell
            c.setFillColor(t.stat_cell_bg)
            c.rect(x, 14, bw-1, BOX_H-HDR_H-14, fill=1, stroke=0)
            # Full box border
            c.setStrokeColor(t.rule); c.setLineWidth(0.5)
            c.rect(x, 14, bw-1, BOX_H-14, fill=0, stroke=1)
            # Label — centred in header band
            c.setFillColor(t.stat_hdr_text); c.setFont('Helvetica-Bold', 8)
            c.drawCentredString(x+(bw-1)/2, BOX_H-9, label)
            # Main stat value in light cell
            c.setFillColor(t.stat_cell_text); c.setFont(t.font_head, 14)
            c.drawCentredString(x+(bw-1)/2, 16, str(val))
        # Dark derived stats strip
        c.setFillColor(t.derived_bg); c.rect(0,0,w,13,fill=1,stroke=0)
        c.setStrokeColor(t.rule); c.setLineWidth(0.3); c.rect(0,0,w,13,fill=0,stroke=1)
        x_pos=6
        for lbl,val in self._d:
            c.setFillColor(t.derived_label); c.setFont('Helvetica-Bold',7)
            c.drawString(x_pos,3,lbl+':')
            lw=c.stringWidth(lbl+':','Helvetica-Bold',7)
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
        bg = t.banner_special if self._sp else t.banner_bg
        c.setFillColor(bg); c.rect(0,0,self.width,16,fill=1,stroke=0)
        c.setStrokeColor(t.accent); c.setLineWidth(0.5); c.rect(0,0,self.width,16,fill=0,stroke=1)
        # Small diamond accent left
        c.setFillColor(t.accent)
        c.saveState(); c.translate(6,8); c.rotate(45); c.rect(-2.5,-2.5,5,5,fill=1,stroke=0); c.restoreState()
        c.setFillColor(t.banner_text); c.setFont('Helvetica-Bold',9)
        c.drawString(16,4.5,self._text.upper())


class HPTrack(Flowable):
    """Numbered HP/SAN/Luck track boxes."""
    BOX=15; GAP=3
    def __init__(self, max_val, width, t, label="HIT POINTS",
                 fill=None, fill5=None, border=None, num=None, lbl_col=None):
        super().__init__()
        self.max_val=max_val; self.width=width; self._t=t
        self._label=label
        self._fill   = fill   or t.hp_box_fill
        self._fill5  = fill5  or t.hp_box_5th
        self._border = border or t.hp_box_border
        self._num    = num    or t.hp_num
        self._lbl_col= lbl_col or t.hp_label
        B,G=self.BOX,self.GAP
        bpr=int(width/(B+G)); self.bpr=max(bpr,1)
        rows=(max_val+self.bpr-1)//self.bpr
        self.height=20+rows*(B+G)
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; B,G=self.BOX,self.GAP
        max_val=self.max_val; bpr=self.bpr; w=self.width; top=self.height
        # Label row
        c.setFillColor(self._lbl_col); c.setFont('Helvetica-Bold',9)
        c.drawString(0,top-13,self._label)
        c.drawRightString(w,top-13,f"MAX  {max_val}")
        c.setStrokeColor(self._border); c.setLineWidth(0.4)
        c.line(0,top-16,w,top-16)
        y_start=top-20
        for i in range(max_val):
            row=i//bpr; col=i%bpr
            items_this_row=min(bpr, max_val-row*bpr)
            row_w=items_this_row*(B+G)-G
            start_x=(w-row_w)/2
            x=start_x+col*(B+G)
            y=y_start-row*(B+G)
            val=max_val-i
            # Shadow
            c.setFillColor(colors.HexColor('#B8A878')); c.rect(x+1,y-1,B,B,fill=1,stroke=0)            # Box
            fill=self._fill5 if (val%5==0) else self._fill
            c.setFillColor(fill); c.setStrokeColor(self._border); c.setLineWidth(1.0)
            c.rect(x,y,B,B,fill=1,stroke=1)
            # Number
            c.setFillColor(self._num); c.setFont('Helvetica-Bold',9)
            c.drawCentredString(x+B/2, y+(B-7)/2, str(val))


class PortraitPlaceholder(Flowable):
    """Reserved portrait space for Midjourney art."""
    def __init__(self, char_name, width, height, t):
        super().__init__(); self._name=char_name; self.width=width; self.height=height; self._t=t
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; t=self._t; w,h=self.width,self.height
        c.setFillColor(t.port_bg); c.roundRect(0,0,w,h,4,fill=1,stroke=0)
        c.setStrokeColor(t.port_border); c.setLineWidth(1.0); c.roundRect(0,0,w,h,4,fill=0,stroke=1)
        # Crosshatch
        c.setStrokeColor(t.port_text); c.setLineWidth(0.25)
        for y in range(0,int(h)+1,14): c.line(0,y,w,y)
        for x in range(0,int(w)+1,14): c.line(x,0,x,h)
        # Text panel
        c.setFillColor(t.port_bg)
        mid_y=h/2; text_h=60
        c.rect(4,mid_y-text_h/2,w-8,text_h,fill=1,stroke=0)
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
        c.setFillColor(t.header_name); c.setFont(t.font_head,14); c.drawString(10,h-19,self._n)
        nw=c.stringWidth(self._n,t.font_head,14)
        c.setFillColor(t.back_sub); c.setFont('Helvetica',8)
        c.drawString(14+nw,h-18,f"·  {self._a}  ·  {t.back_note}")
        c.setFillColor(t.accent)
        for cx,cy in [(5,h-5),(w-5,h-5),(5,5),(w-5,5)]:
            c.saveState(); c.translate(cx,cy); c.rotate(45); c.rect(-1.5,-1.5,3,3,fill=1,stroke=0); c.restoreState()


class NotesBlock(Flowable):
    def __init__(self, width, t, lines=8):
        super().__init__(); self.width=width; self._t=t; self.lines=lines; self.height=lines*16+4
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; c.setStrokeColor(self._t.rule); c.setLineWidth(0.4)
        for i in range(self.lines): c.line(0,self.height-(i+1)*16+4,self.width,self.height-(i+1)*16+4)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE BACKGROUNDS
# ═══════════════════════════════════════════════════════════════════════════════

def make_cover_bg(t):
    def fn(c, doc):
        c.saveState(); w,h=A4
        # Near-black tunnel background
        c.setFillColor(colors.HexColor('#080808')); c.rect(0,0,w,h,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#101010')); c.roundRect(20,20,w-40,h-40,4,fill=1,stroke=0)
        # Subway grid texture (horizontal + vertical — transit map aesthetic)
        c.setStrokeColor(colors.HexColor('#1C1C18')); c.setLineWidth(0.2)
        for y in range(20,int(h)-20,18): c.line(20,y,w-20,y)
        for x in range(20,int(w)-20,18): c.line(x,20,x,h-20)
        # Transit orange header band
        c.setFillColor(t.accent); c.rect(20,h-88,w-40,68,fill=1,stroke=0)
        # Dark footer band
        c.setFillColor(colors.HexColor('#101010')); c.rect(20,20,w-40,48,fill=1,stroke=0)
        # Transit orange outer border
        c.setStrokeColor(t.accent); c.setLineWidth(2.0); c.roundRect(20,20,w-40,h-40,4,fill=0,stroke=1)
        c.setLineWidth(0.5); c.roundRect(25,25,w-50,h-50,2,fill=0,stroke=1)
        c.setLineWidth(0.8)
        for y in [h-88,h-20,68,20]: c.line(20,y,w-20,y)
        # Corner marks (squared — transit/brutalist aesthetic)
        c.setStrokeColor(t.accent); c.setLineWidth(1.5)
        for cx,cy,sx,sy in [(20,h-20,1,-1),(w-20,h-20,-1,-1),(20,20,1,1),(w-20,20,-1,1)]:
            c.line(cx,cy,cx+sx*18,cy); c.line(cx,cy,cx,cy+sy*18)
        c.restoreState()
    return fn


def make_page_bg(t):
    def fn(c, doc):
        c.saveState(); w,h=A4
        # Newsprint / concrete background
        c.setFillColor(t.page_bg); c.rect(0,0,w,h,fill=1,stroke=0)
        # Very subtle grid lines (transit aesthetic)
        c.setStrokeColor(colors.HexColor('#D8D4C0')); c.setLineWidth(0.15)
        for y in range(0,int(h),11): c.line(0,y,w,y)
        # Charcoal border with orange accent
        c.setStrokeColor(t.rule); c.setLineWidth(1.5); c.rect(8,8,w-16,h-16,fill=0,stroke=1)
        c.setStrokeColor(t.accent); c.setLineWidth(0.5); c.rect(11,11,w-22,h-22,fill=0,stroke=1)
        # Square corner marks (no diamonds — cleaner, more urban)
        c.setFillColor(t.accent)
        for cx,cy in [(8,8),(w-8,8),(8,h-8),(w-8,h-8)]:
            c.saveState(); c.translate(cx,cy); c.rect(-3,-3,6,6,fill=1,stroke=0); c.restoreState()
        # Footer
        c.setFont('Helvetica',7.5); c.setFillColor(t.footer)
        c.drawCentredString(w/2,14,t.footer_text)
        c.restoreState()
    return fn


# ═══════════════════════════════════════════════════════════════════════════════
# SANITY EVENTS REFERENCE TABLE
# ═══════════════════════════════════════════════════════════════════════════════

SAN_EVENTS = [
    ("Portraits with faces cut out",             "0/1"),
    ("Reading the Codex — failed roll",          "1/1D6"),
    ("Herald's appearance (wrong face)",          "0/1D3"),
    ("Herald speaks with Ashworth's voice",       "0/1D4"),
    ("Failed Occult roll during incantation",     "1/1D4"),
    ("First sight of the Skinless Watcher",       "1D3/1D10"),
    ("Holding the mirror (volunteer)",            "1D6/1D20"),
    ("Watcher Face Peel attack",                  "1D6 + 1D6 SAN"),
    ("Henderson's final words",                   "0/1D3"),
    ("Banishment succeeds",                       "+1D6 SAN"),
]

COMBAT_QUICK = [
    ("REGULAR success",    "Roll ≤ skill",            "Standard hit"),
    ("HARD success",       "Roll ≤ skill ÷ 2",        "Bonus effect"),
    ("EXTREME success",    "Roll ≤ skill ÷ 5",        "Critical effect"),
    ("Fumble",             "96–100 (or 99–00 if skill>50)", "Catastrophic failure"),
    ("DODGE",              "Roll ≤ Dodge skill",      "Avoid attack"),
    ("FIGHTING (Brawl)",   "1D3 + DB",                "Unarmed damage"),
    ("FIREARMS",           "By weapon",               "Range matters"),
    ("GRAPPLE",            "Opposed Fighting",        "1D3 per round held"),
    ("DAMAGE BONUS",       "STR+SIZ 2–64 → table",   "65–84: +1D4  85–124: +1D6"),
    ("BUILD",              "−1 = pushed easily",      "+1 = hard to push"),
]

WATCHER_STATS = [
    ("STR","90"), ("CON","—"), ("SIZ","80"), ("DEX","70"), ("INT","60"), ("POW","120"),
    ("HP","18"), ("MP","24"), ("Armour","2pt + fire immune"), ("SAN loss","1D3/1D10 on sight"),
    ("Face Peel","Fighting 65%  ·  1D6 dmg + 1D6 SAN per rd (opposed STR to break)"),
    ("Presence","Auto within 5ft  ·  1D3 SAN per rd"),
    ("Mirror aversion","Hard POW or paralysed 1D3 rds"),
    ("Midnight","Cannot fully manifest before midnight  ·  banishable until then"),
]


# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# SAN EVENTS & REFERENCE DATA
# ═══════════════════════════════════════════════════════════════════════════════

LTCI_SAN_EVENTS = [
    ("Silver-eyed corpse — no cause of death",            "0/1"),
    ("Platform reflection: full ghost train, no passengers","0/1"),
    ("Token vision — faceless conductor in transit uniform","1/1D4"),
    ("Broadcast uses investigators' real names",           "1/1D4"),
    ("Knocking on outside of tunnel car",                  "0/1"),
    ("Intact wards extending into darkness",               "1/1D4"),
    ("Ritual timetable read in full",                      "1/1D6"),
    ("Platform freeze / ghost train passes without stopping","1/1D6"),
    ("First full sight of the Black Conductor",            "1D6/1D20"),
    ("Black Conductor — full-night accumulated exposure",  "1D4/1D10"),
    ("Sealing the line — token placement",                 "1D8 PERMANENT"),
    ("Taking the Bargain",                                 "1D10"),
]

CONDUCTOR_STATS = [
    ("STR","—"), ("CON","—"), ("SIZ","Vast"), ("DEX","—"),
    ("INT","200"), ("POW","200"), ("HP","—"), ("Armour","Immune to physical"),
    ("SAN loss","1D6/1D20 (sight) · 1D4/1D10 (accumulated)"),
    ("Presence","Auto within platform range · 1D4 SAN per round in direct contact"),
    ("Voice","All speakers/PA/chest simultaneously · Hard POW to act"),
    ("Weakness","Brass token placed in breaker shrine at Stillwell by 06:00"),
    ("Seal the gate","POW roll · failure: second investigator assists (combined POW)"),
    ("After 07:00","No known procedure"),
]

LTCI_COMBAT = [
    ("REGULAR success",    "Roll ≤ skill",            "Standard hit"),
    ("HARD success",       "Roll ≤ skill ÷ 2",        "Bonus effect / knockdown"),
    ("EXTREME success",    "Roll ≤ skill ÷ 5",        "Max damage / disarm"),
    ("Fumble",             "96–100 (99–00 if skill>50)","Weapon lost / self-harm"),
    ("DODGE",              "Roll ≤ Dodge",            "Avoid one attack"),
    ("FIGHTING (Knife)",   "1D4+2 + DB",              "Can impale"),
    ("FIGHTING (Brawl)",   "1D3 + DB",                "Unarmed / improvised"),
    ("FIREARMS",           "By weapon",               "Range and ammo critical"),
    ("THROW",              "STR/DEX range + DB",      "Improvised missiles"),
    ("DAMAGE BONUS",       "STR+SIZ 65–84: +1D4",     "85–124: +1D6 · <65: None"),
]


# ═══════════════════════════════════════════════════════════════════════════════
# CHARACTER DATA — Event 92: Last Train to Coney Island, NYC 1979
# ═══════════════════════════════════════════════════════════════════════════════

LTCI_CHARS = [
  {
    'name': 'Leon "Swan" Mercer',
    'arch': 'War Chief',
    'meta': 'Coney Island Warriors',
    'allg': 'Hook: Cyrus made eye contact before the shot',
    'physical': 'Mid-20s. The kind of face people follow — not because it\'s exceptional but because it\'s decided. Warriors colours worn like a second skin. Moves through crowds the way water finds gaps, constantly reading the room. Carries the tension of someone who\'s responsible for five other people\'s lives and is doing the arithmetic quietly.',
    'stats': [('STR','60'),('CON','70'),('SIZ','60'),('DEX','60'),('INT','80'),('POW','50'),('APP','50'),('EDU','40')],
    'derived': [('HP','13'),('MP','10'),('SAN','50'),('Luck','50'),('DB','+1D4'),('Build','1'),('Move','8')],
    'skills': [
      ('Fighting (Brawl)','60%'),('Fast Talk','50%'),
      ('Psychology','60%'),('Dodge','50%'),
      ('Intimidate','45%'),('Persuade','45%'),
      ('Spot Hidden','45%'),('Stealth','40%'),
      ('Listen','40%'),('Navigate','30%'),
      ('Streetwise','55%'),('Jump','40%'),
      ('Climb','35%'),('Drive Auto','35%'),
      ('Firearms (Handgun)','40%'),('Track','35%'),
      ('First Aid','30%'),('Throw','40%'),
    ],
    'equipment': [
      'Warriors colours jacket — every set on the island knows it',
      'Street clothes, good running shoes',
      'The brass token (warm, stays warm) — pressed into his palm by Cyrus',
      '$23 cash and a subway MetroCard',
      'Pack of Marlboros, half empty',
      'A folding knife — not a weapon, a tool. He tells himself this.',
    ],
    'weapons': [
      {'name':'Fighting (Brawl)','skill':'Fighting (Brawl)','atk':'60%','par':'60%','damage':'1D3+DB','notes':'DB: +1D4 · grapple · leadership presence'},
      {'name':'Folding Knife',   'skill':'Fighting (Brawl)','atk':'60%','par':'—', 'damage':'1D4+DB','notes':'DB: +1D4 · "just a tool" · can impale'},
      {'name':'Improvised',      'skill':'Fighting (Brawl)','atk':'60%','par':'—', 'damage':'1D4+DB','notes':'Pipes, bats, whatever the city provides'},
    ],
    'sp_name': "Warrior's Brief — Leon \"Swan\" Mercer",
    'sp_type': 'War Chief, Coney Island Warriors · The one they follow when things go wrong',
    'sp_stats': 'Fighting (Brawl) 60%  ·  Psychology 60%  ·  Fast Talk 50%  ·  Streetwise 55%',
    'sp_abilities': [
      ('Personal Hook', 'Cyrus made direct eye contact with Swan the moment before the shot. Swan is certain Cyrus was already afraid of something before the bullet came. Not of the crowd. Of something in it.'),
      ('SAN Triggers', 'Losing a Warrior under his command (–1D4). Full extent of the cult\'s involvement (–1D6). First clear sight of the Black Conductor (–1D10).'),
      ('Special Ability', 'Leadership: once per scene, Swan can grant one Warrior a free re-roll on a skill that requires nerve or coordination. The group follows his read on a situation.'),
      ('Keeper Note', 'Swan carries the brass token from the Introduction. It is warm. It stays warm. He checks this every twenty minutes and stops checking himself doing it around Act 2.'),
    ],
    'sp_note': '"Cyrus told me once that I had the kind of face people follow." Tonight he finds out what that costs.',
    'background': 'War chief at 24. He didn\'t campaign for it — the previous chief walked into the East River in January and Swan was the one who kept the set together through February. He\'s been running the delegation for six months, which mostly means mediating disputes and keeping younger members from starting wars that can\'t be won. He took this summit seriously because Cyrus was serious, and Cyrus was never wrong about the city. Cyrus is now dead, his name is being broadcast to every set in five boroughs, and he is holding a warm brass token he can\'t explain.',
    'hook': 'Cyrus made eye contact with Swan the moment before the shot. Swan is certain Cyrus was already afraid of something before the bullet. Not the crowd. Something in it.',
    'quote': '"Cyrus told me once that I had the kind of face people follow. I never asked him if that was a compliment."',
  },

  {
    'name': 'Daryl "Spray" Soto',
    'arch': 'Tagger / Scout',
    'meta': 'Coney Island Warriors',
    'allg': 'Hook: three years of cult sigils in his sketchbook',
    'physical': 'Early 20s. Paint-stained fingers, always. Carries the sketchbook the way some people carry weapons — constantly accessible, constantly open to the next page. Light enough to move fast, observant enough that he notices the city\'s grammar where others just see walls. Eyes that track movement and pattern simultaneously.',
    'stats': [('STR','40'),('CON','50'),('SIZ','50'),('DEX','80'),('INT','70'),('POW','60'),('APP','50'),('EDU','40')],
    'derived': [('HP','10'),('MP','12'),('SAN','60'),('Luck','55'),('DB','0'),('Build','0'),('Move','9')],
    'skills': [
      ('Art/Craft (Graffiti)','65%'),('Spot Hidden','60%'),
      ('Stealth','60%'),('Dodge','60%'),
      ('Climb','55%'),('Listen','50%'),
      ('Jump','50%'),('Navigate','55%'),
      ('Fighting (Brawl)','40%'),('Occult','25%'),
      ('Art/Craft (Drawing)','50%'),('Fast Talk','35%'),
      ('Sleight of Hand','35%'),('Drive Auto','25%'),
      ('Language (Spanish)','40%'),('Track','30%'),
      ('Firearms (Handgun)','40%'),('First Aid','25%'),
    ],
    'equipment': [
      'Sketchbook (half-full) — tunnel maps, graf, three pages of cult sigils he thought were patterns',
      'Six spray cans in a shoulder bag — various colours, still his main tool',
      'Marker pens in inside jacket pocket',
      '$11 cash and tokens',
      'A penknife (art tool, legitimately)',
      'Warriors colours — smaller tags on the back than Swan\'s, deliberately',
    ],
    'weapons': [
      {'name':'Fighting (Brawl)','skill':'Fighting (Brawl)','atk':'40%','par':'40%','damage':'1D3+DB','notes':'DB: 0 · fast and evasive · runs first'},
      {'name':'Spray Can',       'skill':'Throw',          'atk':'40%','par':'—', 'damage':'Special','notes':'Eyes: Dodge or blinded 1D4 rds · improvised distraction'},
      {'name':'Penknife',        'skill':'Fighting (Brawl)','atk':'40%','par':'—', 'damage':'1D3',   'notes':'Small blade · last resort · can impale'},
    ],
    'sp_name': "Warrior's Brief — Daryl \"Spray\" Soto",
    'sp_type': 'Tagger and scout · Been mapping the tunnels for three years without knowing what he was mapping',
    'sp_stats': 'Art/Craft (Graffiti) 65%  ·  Spot Hidden 60%  ·  Stealth 60%  ·  Navigate 55%',
    'sp_abilities': [
      ('Personal Hook', 'His sketchbook contains three pages of Third Rail Choir sigils. He\'s been mapping cult ritual sites across the subway system for two years. He thought he was documenting interesting tag styles. He was not.'),
      ('SAN Triggers', 'Realising he\'s been mapping cult sites for years (–1D4). Chalk-work in tunnels that appears to respond to his presence (–1D6).'),
      ('Special Ability', 'The sketchbook is a map. Once per act, Spray can cross-reference a location with his tunnel documentation. Navigate 55% or Spot Hidden 60%: finds a route, access point, or pattern no one else would see.'),
      ('Keeper Note', 'On page 34 of the sketchbook is a near-perfect recreation of the Stillwell terminal\'s ward configuration. He has no memory of drawing it. He drew it in April.'),
    ],
    'sp_note': '"You want to know this city? Read the walls. The walls remember everything." So does the sketchbook.',
    'background': 'Has been tagging subway infrastructure since he was 14. Knows the maintenance tunnels, service corridors, and signal rooms of the BMT, IND, and IRT lines better than anyone employed by the MTA. Has been unconsciously documenting Third Rail Choir sigil-work across the system for two years — the patterns interested him because they were consistent. He now understands why they were consistent. He needs a moment.',
    'hook': 'His sketchbook maps three years of cult sigils. He thought they were interesting tag styles. The sketchbook is a ritual map of the entire subway network.',
    'quote': '"You want to know this city? Read the walls. The walls remember everything."',
  },

  {
    'name': 'Ruth "Rook" Alvarez',
    'arch': 'Fighter',
    'meta': 'Coney Island Warriors',
    'allg': 'Hook: Marco, 12, alone in the apartment',
    'physical': 'Early 20s. The precise economy of someone who trained to move in confined spaces. Didn\'t want to be at this summit — wants to be home. The blade she technically didn\'t bring is in her left boot. Her eyes do a room-assessment in the first three seconds of entering it: exits, threats, distance to both.',
    'stats': [('STR','70'),('CON','60'),('SIZ','50'),('DEX','70'),('INT','60'),('POW','50'),('APP','50'),('EDU','40')],
    'derived': [('HP','11'),('MP','10'),('SAN','50'),('Luck','50'),('DB','0'),('Build','0'),('Move','8')],
    'skills': [
      ('Fighting (Knife)','70%'),('Intimidate','60%'),
      ('Dodge','60%'),('Jump','55%'),
      ('Throw','55%'),('Fighting (Brawl)','40%'),
      ('Stealth','45%'),('First Aid','40%'),
      ('Climb','45%'),('Navigate','35%'),
      ('Listen','45%'),('Spot Hidden','40%'),
      ('Fast Talk','30%'),('Streetwise','50%'),
      ('Language (Spanish)','55%'),('Track','30%'),
      ('Firearms (Handgun)','40%'),('Psychology','30%'),
    ],
    'equipment': [
      'The blade she didn\'t bring — boot knife, 4-inch fixed, worn grip',
      'Warriors colours jacket — worn tighter than Swan\'s for movement',
      '$16 cash and transit tokens',
      'A photograph of Marco, folded once, breast pocket',
      'Street clothes built for running',
      'A length of bicycle chain (wrapped around wrist as a bracelet, technically)',
    ],
    'weapons': [
      {'name':'Boot Knife',        'skill':'Fighting (Knife)', 'atk':'70%','par':'40%','damage':'1D4+2',  'notes':'4-inch fixed · always present · can impale'},
      {'name':'Bicycle Chain',     'skill':'Fighting (Brawl)','atk':'40%','par':'40%','damage':'1D6',    'notes':'Wrapped at wrist · reach weapon · improvised'},
      {'name':'Fighting (Brawl)',   'skill':'Fighting (Brawl)','atk':'40%','par':'40%','damage':'1D3+DB','notes':'DB: 0 · grapple and throw option · Throw 55%'},
    ],
    'sp_name': "Warrior's Brief — Ruth \"Rook\" Alvarez",
    'sp_type': 'Fighter · Didn\'t want to come · Has to get home before Marco wakes up',
    'sp_stats': 'Fighting (Knife) 70%  ·  Intimidate 60%  ·  Dodge 60%  ·  Throw 55%',
    'sp_abilities': [
      ('Personal Hook', 'Kid brother Marco, 12, is alone in their Coney Island apartment. The Black Conductor learns about Marco when it learns her name. The broadcast in Act 2 says it aloud. She was three feet from the speaker.'),
      ('SAN Triggers', 'Harm to a civilian child (–1D6). Marco\'s name spoken in the broadcast (–1D8).'),
      ('Special Ability', 'The boot knife was "not brought." Rook fights in enclosed spaces at Fighting (Knife) 70% and knows how to use a doorframe. First Aid 40%: field-dresses wounds fast enough to keep someone moving.'),
      ('Keeper Note', 'Three teenagers in prom wear appear in the adjacent train car in Act 3. Rook sees them and thinks about Marco. Name this moment. Let her sit with it.'),
    ],
    'sp_note': '"I don\'t want a war. But I will absolutely finish one." She needs to be home before 7am.',
    'background': 'Joined the Warriors at 16 because the alternative in her block was worse. Has been the set\'s primary fighter for three years — methodical, not reckless. Brought Marco to a Warriors cookout once. He won\'t talk about anything else. She went to the summit because Swan asked and Swan doesn\'t ask unless it matters. She\'d been planning to be back before midnight. It is now past midnight and she is in the Bronx.',
    'hook': 'Marco, 12, is alone in their Coney Island apartment. The Black Conductor learns his name and speaks it aloud on the broadcast. She was standing next to the speaker.',
    'quote': '"I don\'t want a war. But I will absolutely finish one."',
  },

  {
    'name': 'Eddie "Wheels" Carbone',
    'arch': 'Transit Runner',
    'meta': 'Coney Island Warriors',
    'allg': 'Hook: his sealed platform has been accessed',
    'physical': 'Mid-20s. The slightly distracted manner of someone whose attention is always partially elsewhere — calculating routes, assessing infrastructure, noting which service door he hasn\'t tried yet. Carries a multi-tool and three keys that open things they technically shouldn\'t. Moving through a subway station, he looks like he works there. He has never worked there.',
    'stats': [('STR','50'),('CON','60'),('SIZ','60'),('DEX','60'),('INT','70'),('POW','50'),('APP','50'),('EDU','60')],
    'derived': [('HP','12'),('MP','10'),('SAN','50'),('Luck','45'),('DB','0'),('Build','0'),('Move','8')],
    'skills': [
      ('Navigate','70%'),('Mechanical Repair','60%'),
      ('Locksmith','55%'),('Dodge','50%'),
      ('Electrical Repair','50%'),('Spot Hidden','45%'),
      ('Listen','40%'),('Climb','50%'),
      ('Fighting (Brawl)','40%'),('Stealth','45%'),
      ('Drive Auto','45%'),('Jump','40%'),
      ('Fast Talk','35%'),('First Aid','30%'),
      ('Firearms (Handgun)','40%'),('Science (Engineering)','35%'),
      ('Occult','15%'),('Track','30%'),
    ],
    'equipment': [
      'Multi-tool — Leatherman, always on him',
      'Three skeleton keys (opens 80% of MTA service doors)',
      'A hand-drawn map of sealed IND platforms — marked in pencil',
      'Transit worker\'s vest (not his, fits well enough)',
      '$18 cash and tokens',
      'Small flashlight — good battery life',
    ],
    'weapons': [
      {'name':'Fighting (Brawl)','skill':'Fighting (Brawl)','atk':'40%','par':'40%','damage':'1D3+DB','notes':'DB: 0 · prefers not to'},
      {'name':'Multi-Tool',     'skill':'Fighting (Brawl)','atk':'40%','par':'—', 'damage':'1D4',   'notes':'Improvised · heavy end · can impale'},
      {'name':'Improvised',     'skill':'Fighting (Brawl)','atk':'40%','par':'—', 'damage':'1D6',   'notes':'Transit infrastructure has a lot of heavy things'},
    ],
    'sp_name': "Warrior's Brief — Eddie \"Wheels\" Carbone",
    'sp_type': 'Transit runner · Knows every service door in the city · His locked platform has been opened',
    'sp_stats': 'Navigate 70%  ·  Mechanical Repair 60%  ·  Locksmith 55%  ·  Electrical Repair 50%',
    'sp_abilities': [
      ('Personal Hook', 'A sealed IND platform he personally locked two years ago has been recently accessed. The lock he installed has been changed — by someone who knew exactly what they were doing and what they were hiding.'),
      ('SAN Triggers', 'The depth of the cult\'s MTA infiltration (–1D4). The interior of the sealed platform (–1D8).'),
      ('Special Ability', 'Navigate 70%: Wheels can route the group through any part of the transit system, including sealed or decommissioned infrastructure. His keys open most things. Mechanical Repair 60%: can disable or re-enable transit equipment.'),
      ('Keeper Note', 'The ward placements throughout the system required exactly the level of MTA access Wheels has. He has been unconsciously protecting the ward network by keeping the sealed platforms locked. He will work this out in Act 2.'),
    ],
    'sp_note': '"They built this system to move people. They left a lot of doors unlocked." Not the one he locked, though. Someone changed that.',
    'background': 'Has been running the Warriors\' logistics since he found a transit worker\'s vest at a yard sale at 15 and discovered it opened service doors. Has a working knowledge of every operational and decommissioned line in the five boroughs. The MTA once offered him a job after he reported a structural fault in a 14th Street platform — he declined and they never asked again. The sealed IND platform has been bothering him for three weeks, ever since he checked it on a routine walk-through and found the lock replaced.',
    'hook': 'An IND platform he personally sealed two years ago has been accessed. The lock he installed was replaced by someone who understood exactly what they were securing.',
    'quote': '"They built this system to move people. They left a lot of doors unlocked."',
  },

  {
    'name': 'Malik "Doc" Green',
    'arch': 'Street Medic',
    'meta': 'Coney Island Warriors',
    'allg': 'Hook: the photograph, the handwriting, the warning',
    'physical': 'Mid-20s. Calm in the way of someone who has had to be calm in situations that required it. Medical kit is a constant presence — hip-slung, worn in. Watches people\'s breathing before he watches their eyes. The photograph is folded in his breast pocket. He has not shown it to anyone. He has read the back of it approximately forty times.',
    'stats': [('STR','50'),('CON','50'),('SIZ','60'),('DEX','60'),('INT','70'),('POW','70'),('APP','50'),('EDU','60')],
    'derived': [('HP','11'),('MP','14'),('SAN','70'),('Luck','60'),('DB','0'),('Build','0'),('Move','8')],
    'skills': [
      ('First Aid','70%'),('Medicine','55%'),
      ('Persuade','60%'),('Psychology','55%'),
      ('Listen','55%'),('Spot Hidden','45%'),
      ('Dodge','40%'),('Fighting (Brawl)','40%'),
      ('Science (Biology)','40%'),('Fast Talk','40%'),
      ('Navigate','30%'),('Stealth','30%'),
      ('Climb','30%'),('Firearms (Handgun)','40%'),
      ('Library Use','35%'),('Occult','20%'),
      ('Drive Auto','35%'),('Language (French)','30%'),
    ],
    'equipment': [
      'Medical kit — field-grade, bandages, suture kit, antiseptic, morphine (2 doses)',
      'The photograph — Riff runner, three weeks ago, reverse side: "Union Square / transfer / voice in static / do not ride the last car"',
      'Notebooks (two) — patient notes in one, the runner\'s case notes in the other',
      '$20 cash and tokens',
      'A disposable lighter',
      'Warriors colours — worn carefully, like he was asked to wear them and is trying to do it right',
    ],
    'weapons': [
      {'name':'Fighting (Brawl)','skill':'Fighting (Brawl)','atk':'40%','par':'40%','damage':'1D3+DB','notes':'DB: 0 · grapple/restrain · prefers to stabilise'},
      {'name':'Scalpel/Blade',   'skill':'Fighting (Brawl)','atk':'40%','par':'—', 'damage':'1D4',   'notes':'From kit · fine edge · can impale · he hates this'},
    ],
    'sp_name': "Warrior's Brief — Malik \"Doc\" Green",
    'sp_type': 'Street medic · Carries a warning from a man who vanished from hospital without record',
    'sp_stats': 'First Aid 70%  ·  Medicine 55%  ·  Persuade 60%  ·  Psychology 55%',
    'sp_abilities': [
      ('Personal Hook', 'Carries a photograph of a Riff runner he treated three weeks ago. On the reverse, in the runner\'s own handwriting: "Union Square / transfer / voice in static / do not ride the last car." The runner was subsequently discharged from Kings County Hospital with no record of admission. Doc has told no one.'),
      ('SAN Triggers', 'A victim in the same dissociative state as the Riff runner (–1D4). Learning the runner vanished from the hospital without record (–1D6).'),
      ('Special Ability', 'First Aid 70%: keeps the Warriors moving. Medicine 55%: assesses and diagnoses — including effects of Mythos exposure on physiology. The photograph is Handout H2. He\'s the reason the group finds it.'),
      ('Keeper Note', 'Doc eventually learns, in the Epilogue under Outcome B, that the Riff runner was discharged from Kings County without record. He will think about that for the rest of his life.'),
    ],
    'sp_note': '"I\'ve stitched up enough of you to know that fear always bleeds the same colour." He has been carrying this photograph for three weeks.',
    'background': 'Self-taught medic, originally from a family that couldn\'t afford the ER. Has been patching up Warriors and civilians across Coney Island for two years, using a combination of stolen hospital supplies and things he taught himself from a manual he found in a closing library. Joined the summit delegation because Swan said "bring the kit." The Riff runner three weeks ago was the most disturbing patient he\'d had — not the injuries, which were minor. The vacancy behind the eyes. The silver tinge at the iris edge. And then no record. No record at all.',
    'hook': 'The photograph in his pocket. The runner\'s handwriting. "Do not ride the last car." He has told no one for three weeks.',
    'quote': '"I\'ve stitched up enough of you to know that fear always bleeds the same colour."',
  },

  {
    'name': 'Tina "Mercy" Velez',
    'arch': 'Runaway / Swing Investigator',
    'meta': 'Formerly Turnstiles — no set',
    'allg': 'Hook: saw Creed in a dead man\'s face',
    'physical': 'Early 20s. The specific composure of someone who has been underestimated continuously and learned to use it. APP 80 — the kind of face that makes people assume she\'s harmless. She is aware of this and has never corrected it. Moves lightly. Keeps exits in her peripheral vision. Has been watching the Third Rail Choir from a careful distance for two years.',
    'stats': [('STR','40'),('CON','50'),('SIZ','40'),('DEX','70'),('INT','60'),('POW','60'),('APP','80'),('EDU','40')],
    'derived': [('HP','9'),('MP','12'),('SAN','60'),('Luck','65'),('DB','-1D4'),('Build','-1'),('Move','9')],
    'skills': [
      ('Charm','70%'),('Stealth','60%'),
      ('Dodge','60%'),('Sleight of Hand','50%'),
      ('Fast Talk','55%'),('Listen','45%'),
      ('Psychology','45%'),('Fighting (Brawl)','40%'),
      ('Navigate','50%'),('Occult','35%'),
      ('Spot Hidden','45%'),('Climb','40%'),
      ('Jump','40%'),('First Aid','30%'),
      ('Persuade','45%'),('Language (Spanish)','50%'),
      ('Firearms (Handgun)','40%'),('Drive Auto','25%'),
    ],
    'equipment': [
      'No colours — deliberately neutral, reads as nobody in particular',
      'A small knife (not a weapon — an opener, she insists)',
      'Transit tokens — more than she should have',
      '$28 cash from sources she doesn\'t specify',
      'A handwritten list of three Choir safehouses along the route — all traps. She knows this.',
      'A cassette tape she hasn\'t explained to anyone (blank label)',
    ],
    'weapons': [
      {'name':'Fighting (Brawl)','skill':'Fighting (Brawl)','atk':'40%','par':'40%','damage':'1D3+DB','notes':'DB: -1D4 · fast and hard to hold · uses reach'},
      {'name':'Small Knife',    'skill':'Fighting (Brawl)','atk':'40%','par':'—', 'damage':'1D4+DB','notes':'DB: -1D4 · "not a weapon" · can impale'},
      {'name':'Sleight of Hand','skill':'Sleight of Hand', 'atk':'50%','par':'—', 'damage':'Special','notes':'Disarm · pocket · distract · she\'s very good at this'},
    ],
    'sp_name': "Warrior's Brief — Tina \"Mercy\" Velez",
    'sp_type': 'Swing investigator (groups of 4–5) · Former Turnstiles · Knows the Choir and what it does to people',
    'sp_stats': 'Charm 70%  ·  Stealth 60%  ·  Dodge 60%  ·  Occult 35%',
    'sp_abilities': [
      ('Personal Hook', 'Her former set, the Turnstiles, was absorbed into the Third Rail Choir two years ago. She left before it happened — she saw it coming. She has also witnessed Lester Creed wearing what she can only describe as a dead man\'s face. She has a list of three Choir safehouses along tonight\'s route. They are all traps.'),
      ('SAN Triggers', 'Proof the Choir deliberately dissolved her set (–1D4). Creed\'s physical transformation (–1D8).'),
      ('Special Ability', 'Mercy knows three Choir safehouses — all traps. Occult 35%: deepest Mythos knowledge in the group. Charm 70% / Persuade 45%: can negotiate with NPCs who\'d shoot anyone else. Swing character: replaces any incapacitated investigator.'),
      ('Keeper Note', 'The cassette tape in Mercy\'s pocket has a blank label. She found it in the Turnstiles\' old space before the Choir moved in. She doesn\'t know if it\'s the same tape as the Union Square cache. She hasn\'t played it. She\'s been afraid to.'),
    ],
    'sp_note': '"I don\'t have a set anymore. I have a destination." She knows where every trap is. She just hasn\'t decided what to do about it yet.',
    'background': 'Former founding member of the Turnstiles, a small Lower Manhattan set that was absorbed into the Third Rail Choir two years ago through a combination of offers and threats she still won\'t describe in detail. She left before the absorption completed — she saw the pattern in the chalk marks on the walls before anyone else did. Has been living adjacent to the city\'s gang infrastructure ever since, with no allegiance and a working knowledge of the Choir\'s geography. She is at the summit because she had a message for Cyrus that she never got to deliver.',
    'hook': 'She was going to warn Cyrus tonight. She has a list of Choir safehouses along the Warriors\' route home. Every one of them is a trap.',
    'quote': '"I don\'t have a set anymore. I have a destination."',
  },
]


# ═══════════════════════════════════════════════════════════════════════════════
# REFERENCE PAGE BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_ltci_reference_page(story, t, UW):
    S = make_styles(t)

    story.append(Spacer(1,2))
    story.append(Paragraph("KEEPER'S QUICK REFERENCE", S['ref_title']))
    story.append(Paragraph("Last Train to Coney Island  ·  Call of Cthulhu 7e  ·  New York City, 1979", S['ref_sub']))
    story.append(Spacer(1,4))
    story.append(OrnRule(UW, t))
    story.append(Spacer(1,5))

    # CoC 7e combat
    story.append(SectionBanner("CoC 7E — SKILL ROLLS & COMBAT", UW, t))
    story.append(Spacer(1,3))
    mech_rows = [[Paragraph('DIFFICULTY',S['ref_hdr']),Paragraph('HOW TO ROLL',S['ref_hdr']),Paragraph('RESULT',S['ref_hdr'])]]
    for label, how, result in LTCI_COMBAT:
        mech_rows.append([Paragraph(label,S['ref_bold']),Paragraph(how,S['ref_body']),Paragraph(result,S['ref_body'])])
    mech_t = Table(mech_rows, colWidths=[UW*0.28,UW*0.38,UW*0.34])
    mts = [('BACKGROUND',(0,0),(-1,0),t.banner_bg),('LINEBELOW',(0,0),(-1,-1),0.3,t.rule),
           ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),4),
           ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]
    for i in range(1,len(mech_rows)):
        mts.append(('BACKGROUND',(0,i),(-1,i),t.row1 if i%2==1 else t.row2))
    mech_t.setStyle(TableStyle(mts))
    story.append(mech_t)
    story.append(Spacer(1,5))

    # SAN events
    story.append(SectionBanner("SANITY EVENTS — THIS SCENARIO", UW, t))
    story.append(Spacer(1,3))
    SAN_COLORS = {
        'low':    (colors.HexColor('#1A4A28'),colors.HexColor('#E8F4EC'),colors.HexColor('#C8E8D4')),
        'mid':    (colors.HexColor('#5A3A00'),colors.HexColor('#F8EDD4'),colors.HexColor('#F0DDA0')),
        'high':   (colors.HexColor('#7A1800'),colors.HexColor('#F6E0D8'),colors.HexColor('#EECAB8')),
        'severe': (colors.HexColor('#1A0808'),colors.HexColor('#E8D0C8'),colors.HexColor('#DEB8B0')),
    }
    san_zones = [
        ('low',   "LOW — atmospheric dread",           LTCI_SAN_EVENTS[:3]),
        ('mid',   "MODERATE — genuine horror",         LTCI_SAN_EVENTS[3:7]),
        ('high',  "HIGH — confrontation / broadcast",  LTCI_SAN_EVENTS[7:9]),
        ('severe',"SEVERE — the Black Conductor",      LTCI_SAN_EVENTS[9:]),
    ]
    san_rows=[]; san_cmds=[('LINEBELOW',(0,0),(-1,-1),0.3,t.rule),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]
    zhs=ParagraphStyle('zhs',fontName='Helvetica-Bold',fontSize=7.5,textColor=colors.white,leading=10)
    ens=ParagraphStyle('ens',fontName='Times-Roman',fontSize=8,textColor=t.body,leading=10)
    sls=ParagraphStyle('sls',fontName='Helvetica-Bold',fontSize=8,textColor=t.body,leading=10,alignment=TA_CENTER)
    row_idx=0
    for zone_key,zone_label,events in san_zones:
        hdr_col,light,dark=SAN_COLORS[zone_key]
        san_rows.append([Paragraph(zone_label,zhs),Paragraph('',zhs)])
        san_cmds.extend([('BACKGROUND',(0,row_idx),(-1,row_idx),hdr_col),('SPAN',(0,row_idx),(-1,row_idx))])
        row_idx+=1
        for i,(ev,loss) in enumerate(events):
            san_rows.append([Paragraph(ev,ens),Paragraph(loss,sls)])
            san_cmds.append(('BACKGROUND',(0,row_idx),(-1,row_idx),light if i%2==0 else dark))
            row_idx+=1
    san_t=Table(san_rows,colWidths=[UW*0.78,UW*0.22])
    san_t.setStyle(TableStyle(san_cmds))
    story.append(san_t)
    story.append(Spacer(1,4))

    # Black Conductor stats
    story.append(SectionBanner("THE BLACK CONDUCTOR — STAT SUMMARY", UW, t, special=True))
    story.append(Spacer(1,3))
    stat_lbl_s=ParagraphStyle('wsl',fontName='Helvetica-Bold',fontSize=7.5,textColor=t.special_label,leading=10)
    stat_val_s=ParagraphStyle('wsv',fontName='Times-Roman',fontSize=8,textColor=t.special_body,leading=10)
    core=CONDUCTOR_STATS[:8]; detail=CONDUCTOR_STATS[8:]
    w_rows=[]
    for i,(lbl,val) in enumerate(core):
        if i<len(detail):
            rl,rv=detail[i]
            w_rows.append([Paragraph(f"{lbl}:",stat_lbl_s),Paragraph(str(val),stat_val_s),
                           Paragraph(f"{rl}:",stat_lbl_s),Paragraph(str(rv),stat_val_s)])
        else:
            w_rows.append([Paragraph(f"{lbl}:",stat_lbl_s),Paragraph(str(val),stat_val_s),
                           Paragraph('',stat_lbl_s),Paragraph('',stat_val_s)])
    for i in range(len(core),len(detail)):
        rl,rv=detail[i]
        w_rows.append([Paragraph('',stat_lbl_s),Paragraph('',stat_val_s),
                       Paragraph(f"{rl}:",stat_lbl_s),Paragraph(str(rv),stat_val_s)])
    col_q=UW/4
    wt=Table(w_rows,colWidths=[col_q*0.35,col_q*0.65,col_q*0.6,col_q*1.4])
    wt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),t.special_bg),
        ('LINEBELOW',(0,0),(-1,-1),0.3,colors.HexColor('#2A1808')),
        ('BOX',(0,0),(-1,-1),1.2,t.special_border),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBEFORE',(2,0),(2,-1),0.5,colors.HexColor('#2A1808'))]))
    story.append(wt)
    story.append(Spacer(1,4))
    story.append(Paragraph(
        "The Black Conductor cannot be harmed by conventional weapons. "
        "It is not here to destroy the city — it wants to run it. "
        "The brass token placed in the Stillwell breaker shrine is the only resolution. "
        "Firearms are pointless. Standing in the terminal is where courage actually lives.",
        S['ref_note']))
    story.append(OrnRule(UW,t))
    story.append(Paragraph(
        '"This is the last stop. All passengers must exit here."',
        S['quote']))
    story.append(OrnRule(UW,t))


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD FUNCTION — reused from NAT with LTCI reference page
# ═══════════════════════════════════════════════════════════════════════════════

def get_skill(char, fragment):
    for n,v in char.get('skills',[]):
        if fragment.lower() in n.lower(): return v
    return '—'


def build_pdf(path, CHARS, t, cover_title, cover_sub, cover_byline, rules,
              portraits=None, append_reference=False):
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

    # Cover
    story.append(Spacer(1,68))
    story.append(Paragraph(cover_title, S['cover_title']))
    story.append(Spacer(1,4))
    story.append(Paragraph(cover_sub,   S['cover_sub']))
    story.append(Spacer(1,4))
    story.append(Paragraph(cover_byline,S['cover_byline']))
    story.append(Spacer(1,14))
    story.append(OrnRule(UW,t))
    story.append(Spacer(1,10))
    roster=[[Paragraph(f"<b>{c['name']}</b>",S['cover_name']),
             Paragraph(c['arch'],S['cover_arch']),
             Paragraph(c.get('meta',''),S['cover_meta'])] for c in CHARS]
    rt=Table(roster,colWidths=[UW*0.40,UW*0.30,UW*0.30])
    rt.setStyle(TableStyle([('ROWBACKGROUNDS',(0,0),(-1,-1),[t.cover_row1,t.cover_row2]),
        ('LINEBELOW',(0,0),(-1,-1),0.4,t.rule),
        ('LINEABOVE',(0,0),(-1,0),1.0,t.accent),('LINEBELOW',(0,-1),(-1,-1),1.0,t.accent),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.append(rt)
    story.append(Spacer(1,12))
    story.append(OrnRule(UW,t))
    story.append(Spacer(1,8))
    story.append(Paragraph("QUICK REFERENCE",S['rules_head']))
    rlt=Table([[Paragraph(cell,S['cover_rule'])for cell in row]for row in rules],colWidths=[UW/3]*3)
    rlt.setStyle(TableStyle([('ROWBACKGROUNDS',(0,0),(-1,-1),[t.cover_row1,t.cover_row2]),
        ('GRID',(0,0),(-1,-1),0.4,t.rule),('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    story.append(rlt)
    story.append(Spacer(1,8))
    story.append(Paragraph(
        "Hand sheets face-down. Players choose by role, not stats.  "
        "Scenario begins midnight. Dawn is six hours away.",
        S['cover_note']))
    story.append(NextPageTemplate('normal'))
    story.append(PageBreak())

    # Character pages
    for char in CHARS:
        max_hp  = int(next(v for k,v in char['derived'] if k=='HP'))
        max_san = int(next(v for k,v in char['derived'] if k=='SAN'))
        max_luck= int(next(v for k,v in char['derived'] if k=='Luck'))
        dodge   = get_skill(char,'dodge')
        db_val  = next((v for k,v in char['derived'] if k=='DB'),'0')

        # Front page
        story.append(CharHeader(char['name'],char['arch'],char['meta'],char['allg'],UW,t))
        story.append(Spacer(1,4))
        sk=char['skills']
        if len(sk)%2: sk=sk+[('','')]
        mid=len(sk)//2
        sk_rows=[]
        for (la,lv),(ra,rv) in zip(sk[:mid],sk[mid:]):
            sk_rows.append([Paragraph(la,S['body_sm']),Paragraph(f"<b>{lv}</b>",S['body_sm']),
                            Paragraph(ra,S['body_sm']),Paragraph(f"<b>{rv}</b>",S['body_sm'])])
        skt=Table(sk_rows,colWidths=[SKH*0.72,SKH*0.28,SKH*0.72,SKH*0.28])
        skt.setStyle(TableStyle([('ROWBACKGROUNDS',(0,0),(-1,-1),[t.row1,t.row2]),
            ('LINEBELOW',(0,0),(-1,-1),0.3,t.rule),('LINEAFTER',(1,0),(1,-1),0.5,t.rule),
            ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),3),
            ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),
            ('ALIGN',(1,0),(1,-1),'RIGHT'),('ALIGN',(3,0),(3,-1),'RIGHT')]))
        left_items=[[SectionBanner("Characteristics",LW-4,t)],[Spacer(1,2)],
                    [StatBlock(char['stats'],char['derived'],LW-4,t)],[Spacer(1,4)],
                    [SectionBanner("Skills",LW-4,t)],[Spacer(1,2)],[skt]]
        left_inner=Table(left_items,colWidths=[LW-4])
        left_inner.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
        import os
        if portraits and char['name'] in portraits and os.path.exists(portraits[char['name']]):
            from reportlab.platypus import Image as RLImage
            right_ph=RLImage(portraits[char['name']],width=port_w,height=port_h)
        else:
            right_ph=PortraitPlaceholder(char['name'],port_w,port_h,t)
        two_col=Table([[left_inner,right_ph]],colWidths=[LW,RW])
        two_col.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
            ('ALIGN',(1,0),(1,-1),'RIGHT'),('LINEBEFORE',(1,0),(1,-1),0.5,t.accent)]))
        story.append(two_col)
        story.append(Spacer(1,4))
        # Equipment
        story.append(SectionBanner("Equipment",UW,t))
        story.append(Spacer(1,2))
        eqt=Table([[Paragraph(f"\u2022 {item}",S['body_sm'])]for item in char['equipment']],colWidths=[UW])
        eqt.setStyle(TableStyle([('ROWBACKGROUNDS',(0,0),(-1,-1),[t.row1,t.row2]),
            ('LINEBELOW',(0,0),(-1,-1),0.3,t.rule),('LEFTPADDING',(0,0),(-1,-1),7),
            ('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
        story.append(eqt)
        story.append(Spacer(1,4))
        # Combat
        story.append(SectionBanner("Combat",UW,t))
        story.append(Spacer(1,2))
        cw=[UW*0.26,UW*0.17,UW*0.09,UW*0.09,UW*0.13,UW*0.26]
        wep_rows=[[Paragraph('WEAPON',S['wt_hdr']),Paragraph('SKILL',S['wt_hdr']),
                   Paragraph('ATK',S['wt_hdr']),Paragraph('PAR',S['wt_hdr']),
                   Paragraph('DAMAGE',S['wt_hdr']),Paragraph('NOTES',S['wt_hdr'])]]
        for w in char.get('weapons',[]):
            wep_rows.append([Paragraph(w['name'],S['wt_body']),Paragraph(w['skill'],S['wt_body']),
                             Paragraph(w['atk'],S['wt_body_c']),Paragraph(w['par'],S['wt_body_c']),
                             Paragraph(w['damage'],S['wt_body_c']),Paragraph(w['notes'],S['wt_body'])])
        ts=[('BACKGROUND',(0,0),(-1,0),t.banner_bg),('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('LINEBELOW',(0,0),(-1,-1),0.3,t.rule),('LINEAFTER',(0,0),(4,-1),0.3,t.rule),
            ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),4),
            ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
            ('ALIGN',(2,0),(4,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]
        for i in range(1,len(wep_rows)): ts.append(('BACKGROUND',(0,i),(-1,i),t.row1 if i%2==1 else t.row2))
        wt=Table(wep_rows,colWidths=cw); wt.setStyle(TableStyle(ts))
        story.append(wt)
        dodge_row=Table([[Paragraph(f"DODGE: <b>{dodge}</b>",S['wt_dodge']),
                          Paragraph(f"DAMAGE BONUS: <b>{db_val}</b>",S['wt_dodge'])]],
                        colWidths=[UW*0.45,UW*0.55])
        dodge_row.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),t.derived_bg),
            ('BOX',(0,0),(-1,-1),0.8,t.accent),('LEFTPADDING',(0,0),(-1,-1),10),
            ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
        story.append(dodge_row)
        story.append(Spacer(1,5))
        # Tracks
        story.append(HPTrack(max_hp,UW,t,label="HIT POINTS"))
        story.append(Spacer(1,4))
        story.append(HPTrack(max_san,UW,t,label="SANITY",
            fill=t.san_box_fill,fill5=t.san_box_5th,border=t.san_box_border,
            num=t.san_num,lbl_col=t.san_label))
        story.append(Spacer(1,4))
        luck_row=Table([[Paragraph(f"LUCK (starting): <b>{max_luck}</b>",S['wt_dodge']),
                         Paragraph("Track Luck in the notes section below",S['wt_body'])]],
                       colWidths=[UW*0.42,UW*0.58])
        luck_row.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),t.luck_box_fill),
            ('BOX',(0,0),(-1,-1),0.8,t.luck_box_border),('LEFTPADDING',(0,0),(-1,-1),10),
            ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
        story.append(luck_row)
        story.append(PageBreak())

        # Back page
        story.append(BackHeader(char['name'],char['arch'],UW,t))
        story.append(Spacer(1,6))
        story.append(Paragraph(f"<i>{char['physical']}</i>",S['italic_sm']))
        story.append(Spacer(1,8))
        story.append(SectionBanner(t.special_label_str,UW,t,special=True))
        story.append(Spacer(1,3))
        dc=[Paragraph(char['sp_name'],S['sp_title']),Paragraph(char['sp_type'],S['sp_label']),
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
        story.append(SectionBanner("Background",UW,t))
        story.append(Spacer(1,4))
        story.append(Paragraph(char['background'],S['body']))
        story.append(Spacer(1,5))
        ht=Table([[Paragraph("PERSONAL HOOK:",S['hook_label']),Paragraph(char['hook'],S['hook_body'])]],
                 colWidths=[28*mm,UW-28*mm])
        ht.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),t.hook_bg),
            ('BOX',(0,0),(-1,-1),0.8,t.hook_border),('LINEBEFORE',(0,0),(0,-1),3,t.hook_bar),
            ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
            ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
            ('VALIGN',(0,0),(-1,-1),'TOP')]))
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

    if append_reference:
        build_ltci_reference_page(story,t,UW)

    doc.build(story)
    print(f"Done: {path}")


# ── RUN ──────────────────────────────────────────────────────────────────────
LTCI = last_train_theme()

ART_LTCI = '/home/claude/ChaosiumCon26/scenarios/art/event-92/player-characters'
LTCI_PORTRAITS = {
    'Leon "Swan" Mercer':    f'{ART_LTCI}/ltci-pc01-swan-mercer.jpeg',
    'Daryl "Spray" Soto':    f'{ART_LTCI}/ltci-pc02-spray-soto.jpeg',
    'Ruth "Rook" Alvarez':   f'{ART_LTCI}/ltci-pc03-rook-alvarez.jpeg',
    'Eddie "Wheels" Carbone':f'{ART_LTCI}/ltci-pc04-wheels-carbone.jpeg',
    'Malik "Doc" Green':     f'{ART_LTCI}/ltci-pc05-doc-green.jpeg',
    'Tina "Mercy" Velez':    f'{ART_LTCI}/ltci-pc06-mercy-velez.jpeg',
}

LTCI_RULES = [
    ['HP = (CON+SIZ)÷10  round up', 'SAN = POW', 'DB: STR+SIZ 65–84 = +1D4'],
    ['Regular: roll ≤ skill%', 'Hard: roll ≤ skill÷2', 'Extreme: roll ≤ skill÷5'],
    ['Dodge: roll ≤ Dodge%', 'STAY OFF THE LAST CAR', 'Brass token: Stillwell shrine · 06:00'],
]

build_pdf(
    '/mnt/user-data/outputs/coc-last-train-to-coney-island-characters.pdf',
    LTCI_CHARS, LTCI,
    "LAST TRAIN TO CONEY ISLAND",
    "Player Character Reference — New York City, Midnight 1979",
    "Call of Cthulhu 7th Edition  ·  Event 92  ·  ChaosiumCon 2026",
    LTCI_RULES,
    portraits=LTCI_PORTRAITS,
    append_reference=True,
)
