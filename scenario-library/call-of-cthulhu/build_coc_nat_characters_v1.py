#!/usr/bin/env python3
"""
Call of Cthulhu 7e Character Sheets
Event 93 — Not Another Telegram (CoC 1920s, NYC 1924)
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

# ── FONTS ─────────────────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont('SerBold',  '/tmp/source-serif-bold.ttf'))
pdfmetrics.registerFont(TTFont('SerReg',   '/tmp/source-serif-regular.ttf'))
pdfmetrics.registerFont(TTFont('SerIt',    '/tmp/source-serif-italic.ttf'))

PAGE_W, PAGE_H = A4
MARGIN = 17 * mm
UW = PAGE_W - 2 * MARGIN          # ≈ 499 pt

# ═══════════════════════════════════════════════════════════════════════════════
# THEME — Art Deco 1920s:  warm parchment, mahogany, antique gold, sepia ink
# Every light-BG text is near-black; every dark-BG text is cream/gold.
# ═══════════════════════════════════════════════════════════════════════════════

class T: pass

def not_another_telegram_theme():
    t = T()
    t.name = 'nat'
    # ── Page background ──
    t.page_bg         = colors.HexColor('#F6EED9')   # warm parchment
    t.parchment       = colors.HexColor('#F6EED9')
    t.parchment_dark  = colors.HexColor('#EDE0C0')
    # ── Header banner (dark mahogany) ──
    t.header_bg       = colors.HexColor('#1C0E05')
    t.header_inner    = colors.HexColor('#2A1508')
    t.header_border   = colors.HexColor('#B8860B')   # antique gold border
    t.header_name     = colors.HexColor('#F5E8C0')   # warm cream on dark
    t.header_sub      = colors.HexColor('#D4AC50')   # gold on dark
    t.header_right    = colors.HexColor('#C8A870')
    # ── Section banners ──
    t.banner_bg       = colors.HexColor('#2A1508')
    t.banner_text     = colors.HexColor('#F5E8C0')
    t.banner_special  = colors.HexColor('#1A0A0A')   # very dark for hook box
    # ── Characteristics ──
    t.stat_hdr_bg     = colors.HexColor('#2A1508')   # dark mahogany header
    t.stat_hdr_text   = colors.HexColor('#D4AC50')   # gold on dark
    t.stat_cell_bg    = colors.HexColor('#EDE0C0')   # slightly darker parchment
    t.stat_cell_text  = colors.HexColor('#1A0A02')   # near-black on light
    # ── Derived stats strip ──
    t.derived_bg      = colors.HexColor('#2A1508')
    t.derived_label   = colors.HexColor('#D4AC50')   # gold on dark
    t.derived_val     = colors.HexColor('#F5E8C0')
    # ── Skill / equipment rows ──
    t.row1            = colors.HexColor('#F6EED9')
    t.row2            = colors.HexColor('#EDE0C0')
    t.row_text        = colors.HexColor('#1A0A02')
    t.rule            = colors.HexColor('#7A5210')
    # ── Investigator Brief box (dark) ──
    t.special_bg      = colors.HexColor('#100805')
    t.special_border  = colors.HexColor('#9B7C1A')
    t.special_title   = colors.HexColor('#D4AC50')   # gold on near-black
    t.special_label   = colors.HexColor('#C8A040')
    t.special_body    = colors.HexColor('#EAD8A0')   # warm cream on dark
    # ── HP track (deep red) ──
    t.hp_label        = colors.HexColor('#5A0A0A')   # dark red on parchment
    t.hp_max          = colors.HexColor('#5A0A0A')
    t.hp_box_fill     = colors.HexColor('#FFF0E8')
    t.hp_box_5th      = colors.HexColor('#FFCCB4')
    t.hp_box_border   = colors.HexColor('#9B2000')
    t.hp_num          = colors.HexColor('#3A0808')
    # ── SAN track (deep green) ──
    t.san_label       = colors.HexColor('#0A3020')
    t.san_box_fill    = colors.HexColor('#E8F4E8')
    t.san_box_5th     = colors.HexColor('#AADCAA')
    t.san_box_border  = colors.HexColor('#1A6030')
    t.san_num         = colors.HexColor('#0A2010')
    # ── Luck track (antique blue) ──
    t.luck_label      = colors.HexColor('#0A1A50')
    t.luck_box_fill   = colors.HexColor('#EAF0FF')
    t.luck_box_5th    = colors.HexColor('#BBCCF0')
    t.luck_box_border = colors.HexColor('#1A3088')
    t.luck_num        = colors.HexColor('#0A1040')
    # ── Portrait placeholder ──
    t.port_bg         = colors.HexColor('#1C0E05')
    t.port_border     = colors.HexColor('#B8860B')
    t.port_text       = colors.HexColor('#4A3010')
    t.port_label      = colors.HexColor('#D4AC50')
    # ── Personal hook box ──
    t.hook_bg         = colors.HexColor('#FDF5E0')
    t.hook_border     = colors.HexColor('#9B7C1A')
    t.hook_bar        = colors.HexColor('#B8860B')
    t.hook_label      = colors.HexColor('#5A3800')   # dark amber on cream
    t.hook_body       = colors.HexColor('#1A0A02')
    # ── Back header ──
    t.back_bg         = colors.HexColor('#1C0E05')
    t.back_border     = colors.HexColor('#B8860B')
    t.back_sub        = colors.HexColor('#D4AC50')
    # ── Body text ──
    t.body            = colors.HexColor('#1A0A02')
    t.italic          = colors.HexColor('#3A2010')
    t.quote           = colors.HexColor('#5A2800')   # dark sepia on cream
    # ── Cover (dark mahogany cover page) ──
    t.cover_row1      = colors.HexColor('#1C0E05')
    t.cover_row2      = colors.HexColor('#2A1508')
    t.cover_name      = colors.HexColor('#F5E8C0')
    t.cover_arch      = colors.HexColor('#D4AC50')
    t.cover_meta      = colors.HexColor('#C4A878')
    t.cover_note      = colors.HexColor('#C4A878')
    t.cover_title     = colors.HexColor('#D4AC50')
    t.cover_sub       = colors.HexColor('#C49A30')
    t.cover_byline    = colors.HexColor('#8A6020')
    t.cover_rule_body = colors.HexColor('#F5E8C0')
    t.accent          = colors.HexColor('#B8860B')   # antique gold
    t.footer          = colors.HexColor('#7A5210')
    t.footer_text     = "Not Another Telegram  ·  Call of Cthulhu 7e  ·  Event 93  ·  ChaosiumCon 2026"
    t.special_label_str = "INVESTIGATOR BRIEF"
    t.back_note       = "New York City, 1924  ·  Background & Notes"
    t.font_head       = 'SerBold'
    t.font_body       = 'SerReg'
    t.font_body_bold  = 'SerBold'
    return t

# ═══════════════════════════════════════════════════════════════════════════════
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
            try:    pct_str = f"{int(val)*5}%"
            except: pct_str = ''
            # Dark header cell
            c.setFillColor(t.stat_hdr_bg)
            c.rect(x, BOX_H-HDR_H, bw-1, HDR_H, fill=1, stroke=0)
            # Light value cell
            c.setFillColor(t.stat_cell_bg)
            c.rect(x, 14, bw-1, BOX_H-HDR_H-14, fill=1, stroke=0)
            # Full box border
            c.setStrokeColor(t.rule); c.setLineWidth(0.5)
            c.rect(x, 14, bw-1, BOX_H-14, fill=0, stroke=1)
            # Thin divider at mid-header
            c.setStrokeColor(t.accent); c.setLineWidth(0.3)
            c.line(x+3, BOX_H-8, x+bw-4, BOX_H-8)
            # Label — upper header band
            c.setFillColor(t.stat_hdr_text); c.setFont('Helvetica-Bold', 7)
            c.drawCentredString(x+(bw-1)/2, BOX_H-6, label)
            # ×5 percentile — lower header band
            if pct_str:
                c.setFillColor(t.stat_hdr_text); c.setFont('Helvetica-Bold', 6.5)
                c.drawCentredString(x+(bw-1)/2, BOX_H-14, pct_str)
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
    BOX=17; GAP=3
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
            c.setFillColor(colors.HexColor('#C8A878')); c.rect(x+1.5,y-1.5,B,B,fill=1,stroke=0)            # Box
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
        # Deep mahogany background
        c.setFillColor(colors.HexColor('#100804')); c.rect(0,0,w,h,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#1A0C06')); c.roundRect(20,20,w-40,h-40,5,fill=1,stroke=0)
        # Fine diagonal hatching (Art Deco texture)
        c.setStrokeColor(colors.HexColor('#241006')); c.setLineWidth(0.15)
        for i in range(-int(h), int(w)+int(h), 12):
            c.line(max(20,i), 20, min(w-20,w-20+i), h-20)
        # Top gold header band
        c.setFillColor(t.accent); c.rect(20,h-88,w-40,68,fill=1,stroke=0)
        # Bottom dark footer band
        c.setFillColor(colors.HexColor('#1A0C06')); c.rect(20,20,w-40,48,fill=1,stroke=0)
        # Outer gold border
        c.setStrokeColor(t.accent); c.setLineWidth(2.0); c.roundRect(20,20,w-40,h-40,5,fill=0,stroke=1)
        # Inner thinner border
        c.setLineWidth(0.6); c.roundRect(25,25,w-50,h-50,3,fill=0,stroke=1)
        # Horizontal rules at transitions
        c.setLineWidth(0.8)
        for y in [h-88, h-20, 68, 20]: c.line(20,y,w-20,y)
        # Art Deco corner ornaments
        c.setFillColor(t.accent); c.setLineWidth(1.5)
        for cx,cy,sx,sy in [(20,h-20,1,-1),(w-20,h-20,-1,-1),(20,20,1,1),(w-20,20,-1,1)]:
            c.setStrokeColor(t.accent)
            c.line(cx,cy,cx+sx*20,cy); c.line(cx,cy,cx,cy+sy*20)
            c.saveState(); c.translate(cx+sx*20,cy+sy*20); c.rotate(45)
            c.rect(-4,-4,8,8,fill=1,stroke=0); c.restoreState()
        c.restoreState()
    return fn


def make_page_bg(t):
    def fn(c, doc):
        c.saveState(); w,h=A4
        # Warm parchment
        c.setFillColor(t.page_bg); c.rect(0,0,w,h,fill=1,stroke=0)
        # Subtle horizontal lines (aged paper feel)
        c.setStrokeColor(colors.HexColor('#E8D8B0')); c.setLineWidth(0.2)
        for y in range(0,int(h),9): c.line(0,y,w,y)
        # Mahogany border
        c.setStrokeColor(t.rule); c.setLineWidth(1.5); c.rect(8,8,w-16,h-16,fill=0,stroke=1)
        c.setStrokeColor(t.accent); c.setLineWidth(0.5); c.rect(11,11,w-22,h-22,fill=0,stroke=1)
        # Corner diamond ornaments
        c.setFillColor(t.accent)
        for cx,cy in [(8,8),(w-8,8),(8,h-8),(w-8,h-8)]:
            c.saveState(); c.translate(cx,cy); c.rotate(45); c.rect(-3,-3,6,6,fill=1,stroke=0); c.restoreState()
        # Footer text
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
# CHARACTER DATA — Event 93: Not Another Telegram, NYC 1924
# ═══════════════════════════════════════════════════════════════════════════════

NAT_CHARS = [
  {
    'name': 'Helen Cross',
    'arch': 'The Reporter',
    'meta': 'New York Tribune',
    'allg': 'Connection: Whitmore was her source',
    'physical': 'Age 29. Sharp eyes, press credentials always visible. Moves through a crowd like someone who knows the story is always at the edges. A flask of bourbon in her bag and a pencil behind her ear. The composure of a woman who has learned to take notes while her hands shake.',
    'stats': [('STR','50'),('CON','60'),('SIZ','55'),('DEX','65'),('INT','80'),('POW','65'),('APP','70'),('EDU','75')],
    'derived': [('HP','12'),('MP','13'),('SAN','65'),('Luck','55'),('DB','0'),('Build','0'),('Move','8')],
    'skills': [
      ('Fast Talk','75%'),('Psychology','60%'),('Library Use','65%'),
      ('Spot Hidden','60%'),('Photography','55%'),('Persuade','55%'),
      ('Charm','50%'),('Navigate','45%'),('Dodge','40%'),
      ('Stealth','35%'),('First Aid','30%'),('History','45%'),
      ('Language (French)','40%'),('Drive Auto','40%'),
      ('Credit Rating','40%'),('Occult','25%'),
      ('Fighting (Brawl)','25%'),('Firearms (Handgun)','20%'),
    ],
    'equipment': [
      'Press credentials — New York Tribune (opens doors)',
      'Camera with 4 remaining exposures',
      'Reporter\'s notebook and three sharpened pencils',
      'A flask of bourbon (near-full)',
      'City map of Manhattan with pencilled notes',
      '$12 cash and a spare roll of film',
    ],
    'weapons': [
      {'name':'Fighting (Brawl)', 'skill':'Fighting (Brawl)', 'atk':'25%','par':'—','damage':'1D3+DB','notes':'Unarmed · DB: 0 · last resort'},
      {'name':'Camera (improvised)','skill':'Fighting (Brawl)','atk':'25%','par':'—','damage':'1D4','notes':'Heavy · one use before damaged'},
    ],
    'sp_name': 'Investigator Brief — Helen Cross',
    'sp_type': 'Reporter, age 29 · New York Tribune · Investigating occult societies',
    'sp_stats': 'Fast Talk 75%  ·  Psychology 60%  ·  Spot Hidden 60%  ·  Persuade 55%',
    'sp_abilities': [
      ('Personal Hook', 'Helen\'s editor doesn\'t know she\'s here tonight. If she files this story, it could make her career. If she doesn\'t come back, no one will know where to look.'),
      ('SAN Trigger', 'Witnessing supernatural events in daylight or public spaces — the violation of normalcy hits her hardest.'),
      ('Special Ability', 'Press credentials open doors. In the first act, officials and club staff respond to the Tribune badge before they\'d respond to anyone else.'),
      ('Private Note', 'Helen has been to Whitmore\'s office twice. She knows the layout of the 44 West 53rd building and has Miss Pruitt\'s direct telephone number.'),
    ],
    'sp_note': 'Helen will write this story whether she survives it or not. She started taking notes in the telegram office.',
    'background': 'Six years at the Tribune, three of them on the society beat. She has covered séances, occult salons, and two failed exorcisms — always with faint amusement, always filing the piece. Whitmore was the most genuinely interesting source she\'d found: too careful about what she said, which meant she was protecting something real. Tonight she finds out what.',
    'hook': 'Helen\'s editor doesn\'t know she\'s here. If she files this story, it could make her career. If she doesn\'t come back, no one will know where to look for her.',
    'quote': '"There\'s a story in everything. I just have to survive long enough to file it."',
  },

  {
    'name': 'Dr. Edmund Graves',
    'arch': 'The Doctor',
    'meta': 'Private Practice, Upper West Side',
    'allg': 'Connection: Whitmore\'s personal physician',
    'physical': 'Age 45. A man who has maintained professional composure for twenty years and intends to maintain it tonight. Medical bag on his arm like an extension of himself. The slight stiffness of someone who\'s been worried for three weeks and won\'t say so. Good coat, well-worn shoes. A face that is better at listening than speaking.',
    'stats': [('STR','60'),('CON','70'),('SIZ','65'),('DEX','55'),('INT','75'),('POW','60'),('APP','55'),('EDU','85')],
    'derived': [('HP','14'),('MP','12'),('SAN','60'),('Luck','50'),('DB','0'),('Build','0'),('Move','7')],
    'skills': [
      ('Medicine','80%'),('First Aid','75%'),('Science (Biology)','60%'),
      ('Psychology','55%'),('Library Use','60%'),('Spot Hidden','45%'),
      ('Persuade','50%'),('Credit Rating','60%'),('Navigate','40%'),
      ('History','45%'),('Natural World','40%'),('Occult','25%'),
      ('Language (Latin)','35%'),('Drive Auto','40%'),
      ('Dodge','35%'),('Fighting (Brawl)','35%'),
      ('Pharmacy','50%'),('Science (Chemistry)','40%'),
    ],
    'equipment': [
      'Medical bag: First Aid kit, stethoscope, morphine, suture kit',
      'Legal notepad and two pens',
      'Wallet: $35 cash, calling cards, membership card (Upper West Side Physicians\' Club)',
      'Reading glasses (bifocal)',
      'A folded note: "RE: the Ashworth examination" in his own handwriting — unposted',
      'Watch: seventeen minutes fast, always',
    ],
    'weapons': [
      {'name':'Fighting (Brawl)','skill':'Fighting (Brawl)','atk':'35%','par':'—','damage':'1D3+DB','notes':'Unarmed · DB: 0'},
      {'name':'Scalpel','skill':'Fighting (Brawl)','atk':'35%','par':'—','damage':'1D4','notes':'From medical bag · can impale'},
    ],
    'sp_name': 'Investigator Brief — Dr. Edmund Graves',
    'sp_type': 'Physician, age 45 · Upper West Side private practice · Whitmore\'s personal doctor',
    'sp_stats': 'Medicine 80%  ·  First Aid 75%  ·  Science (Biology) 60%  ·  Psychology 55%',
    'sp_abilities': [
      ('Personal Hook', 'Three weeks ago, Graves examined a body from one of Ashworth\'s early salons — listed as natural causes. Something about the skin of the corpse has been nagging at him. Not the marks. The texture.'),
      ('SAN Trigger', 'Things that violate the integrity of the human body. Particularly faces. The medical framework that lets him examine bodies calmly does not extend to this.'),
      ('Special Ability', 'Medicine 80%: can assess wounds, corpses, and biological anomalies. Will be the first to recognise what the Watcher does to its victims at a cellular level.'),
      ('Private Note', 'He wrote up the Ashworth examination. Listed cause of death as cardiac event. Signed it. Filed it. Has not slept well since.'),
    ],
    'sp_note': 'He is here partly for the money Whitmore owes him. Mostly because the Ashworth body has been wrong in his head for three weeks and tonight he will understand why.',
    'background': 'Private physician for twelve years, specialist in internal medicine. Whitmore has been his most unusual patient: meticulous about her health, brusque about everything else, and in the habit of paying her bills in books rather than cheques. He tolerated this because she was interesting. Tonight he is concerned that she is dead, that he is responsible, and that something he signed off as a cardiac event was neither cardiac nor an event.',
    'hook': 'Three weeks ago he examined a body from Ashworth\'s salon — officially "natural causes." Something about the skin has been nagging at him. Tonight he finds out what was wrong.',
    'quote': '"Medicine teaches you two things: the body is resilient, and the body is not."',
  },

  {
    'name': 'Mickey Doyle',
    'arch': 'The Private Eye',
    'meta': 'Doyle Investigations, Midtown',
    'allg': 'Connection: Hired to follow Ashworth',
    'physical': 'Age 38. The kind of face that blends into rooms — not unhandsome, just unremarkable by professional necessity. A good hat and a better coat. Shoulder holster visible if the coat moves wrong, which it rarely does. Moves like someone who\'s been tracking people long enough to know they\'re always being tracked back.',
    'stats': [('STR','70'),('CON','65'),('SIZ','70'),('DEX','70'),('INT','65'),('POW','60'),('APP','55'),('EDU','60')],
    'derived': [('HP','14'),('MP','12'),('SAN','60'),('Luck','65'),('DB','+1D4'),('Build','1'),('Move','8')],
    'skills': [
      ('Firearms (Handgun)','65%'),('Fighting (Brawl)','60%'),
      ('Spot Hidden','70%'),('Track','55%'),('Psychology','60%'),
      ('Stealth','55%'),('Locksmith','50%'),('Intimidate','55%'),
      ('Fast Talk','45%'),('Persuade','40%'),('Navigate','55%'),
      ('Drive Auto','55%'),('Listen','60%'),('Dodge','50%'),
      ('Credit Rating','35%'),('Library Use','30%'),
      ('Law','35%'),('Occult','20%'),
    ],
    'equipment': [
      '.38 revolver (3D6, 6 shots) in shoulder holster',
      'Brass knuckles (concealed, left pocket)',
      'Lock-picks (concealed in lapel)',
      'Camera — good one, professional quality',
      'Hip flask (rye, nearly empty)',
      'Three weeks of surveillance notes on Ashworth — in his breast pocket',
    ],
    'weapons': [
      {'name':'.38 Revolver','skill':'Firearms (Handgun)','atk':'65%','par':'—','damage':'1D10+2','notes':'Rng 15yds · 6 shots · Mal 00'},
      {'name':'Brass Knuckles','skill':'Fighting (Brawl)','atk':'60%','par':'60%','damage':'1D3+DB+1','notes':'DB: +1D4 · concealable'},
      {'name':'Fighting (Brawl)','skill':'Fighting (Brawl)','atk':'60%','par':'60%','damage':'1D3+DB','notes':'DB: +1D4 · grapple option'},
    ],
    'sp_name': 'Investigator Brief — Mickey Doyle',
    'sp_type': 'Private Investigator, age 38 · Doyle Investigations · Hired by Whitmore to follow Ashworth',
    'sp_stats': 'Spot Hidden 70%  ·  Firearms (Handgun) 65%  ·  Psychology 60%  ·  Track 55%',
    'sp_abilities': [
      ('Personal Hook', 'During his surveillance, Mickey photographed something in one of Ashworth\'s windows he couldn\'t explain. He burned the photograph. He\'s been waking at 3am ever since.'),
      ('SAN Trigger', 'Things that move wrong. Faces that settle. Limbs that don\'t follow expected physics. The thing in the photograph moved like it was adjusting its own face.'),
      ('Special Ability', 'Three weeks of surveillance notes on Ashworth — including guest lists, schedules, and the address of the Blue Orchid connection. Spot Hidden 70%: notices exits, tails, wrong details.'),
      ('Private Note', 'Whitmore\'s final message to him was: "Stop following him. I mean that as kindly as I can." He stopped. For two weeks. Then the telegram arrived.'),
    ],
    'sp_note': 'He burned the photograph. He still knows what was in it. Tonight he will see it in three dimensions.',
    'background': 'Eight years as a private investigator after four on the NYPD. Left the police under circumstances he describes as "philosophical differences." The real reason involves a case he closed too quickly because the alternative was looking at something he wasn\'t equipped to look at. The Ashworth job was supposed to be simple: follow a socialite, document his associates, file the report. It was simple until it wasn\'t.',
    'hook': 'He photographed something in Ashworth\'s window that he couldn\'t explain. He burned the photo. He\'s been waking at 3am ever since. Tonight he understands what he saw.',
    'quote': '"I\'ve seen worse. Usually on a Tuesday."',
  },

  {
    'name': 'Louis "Lucky" Beaumont',
    'arch': 'The Jazz Musician',
    'meta': 'Trumpet · Harlem',
    'allg': 'Connection: Whitmore saved him from Prohibition bust',
    'physical': 'Age 32. Tall and unhurried in the way of someone who has learned that timing is everything. Good shoes — crucial, he will tell you, for running as much as dancing. Trumpet case always present, always slightly dented on the left side from a previous occasion he never discusses. The smile arrives before the caution does, which has gotten him into trouble and out of it in roughly equal measure.',
    'stats': [('STR','55'),('CON','65'),('SIZ','60'),('DEX','75'),('INT','70'),('POW','75'),('APP','80'),('EDU','55')],
    'derived': [('HP','13'),('MP','15'),('SAN','75'),('Luck','70'),('DB','0'),('Build','0'),('Move','8')],
    'skills': [
      ('Art/Craft (Trumpet)','85%'),('Charm','75%'),
      ('Psychology','65%'),('Listen','70%'),
      ('Persuade','60%'),('Stealth','55%'),
      ('Spot Hidden','50%'),('Fast Talk','55%'),
      ('Navigate','50%'),('Fighting (Brawl)','40%'),
      ('Dodge','50%'),('Credit Rating','30%'),
      ('Occult','30%'),('History','35%'),
      ('Language (French)','30%'),('Natural World','25%'),
      ('Drive Auto','35%'),('Library Use','25%'),
    ],
    'equipment': [
      'Trumpet case (trumpet inside, slightly dented left side)',
      'Good leather shoes (important for running)',
      'Pocket flask (rum)',
      'Connections across Harlem — names, doors, favours owed',
      '$8 cash and some coins',
      'A pawn ticket (unrelated, but suspicious-looking)',
    ],
    'weapons': [
      {'name':'Fighting (Brawl)','skill':'Fighting (Brawl)','atk':'40%','par':'40%','damage':'1D3+DB','notes':'DB: 0 · quick and improvised'},
      {'name':'Trumpet Case (improv)','skill':'Fighting (Brawl)','atk':'40%','par':'—','damage':'1D6','notes':'Dented left side · he will be furious'},
    ],
    'sp_name': 'Investigator Brief — Louis "Lucky" Beaumont',
    'sp_type': 'Jazz musician (trumpet), age 32 · Harlem · Former Blue Orchid house band member',
    'sp_stats': 'Art/Craft (Trumpet) 85%  ·  Charm 75%  ·  Listen 70%  ·  Psychology 65%',
    'sp_abilities': [
      ('Personal Hook', 'Lucky has heard things in music that other musicians haven\'t noticed — wrong notes that form patterns. He thought he was imagining it. At the Blue Orchid tonight, the band will play one wrong note and he will know it was not a mistake.'),
      ('SAN Trigger', 'Music that behaves incorrectly. Sound from the wrong direction. The wrong note played with intention. The Watcher enters his world through sound before it enters through sight.'),
      ('Special Ability', 'Automatic success on gaining Delia Monroe\'s trust at the Blue Orchid. Music 85%: can identify deliberate wrong notes as signals, patterns, or communications.'),
      ('Private Note', 'Three years ago, Whitmore talked a desk sergeant out of a Prohibition charge on Lucky\'s behalf. He has never forgotten. Debts matter where he comes from.'),
    ],
    'sp_note': 'Lucky hears the world differently. Tonight that becomes both a warning system and a vulnerability.',
    'background': 'Twelve years playing trumpet across Harlem, from backroom joints to proper venues. Three years as part of the Blue Orchid house band before a disagreement about payment (amicable) ended the arrangement. Knows everyone who matters in Harlem and half of downtown. Owes Whitmore a favour he\'s been half-hoping she\'d never call in. She has, from a distance, through a telegram from someone else. He is already worried.',
    'hook': 'Lucky has heard wrong notes in music that formed patterns — he thought he was imagining it. Tonight, the band at the Blue Orchid will play one deliberate wrong note, and he will know it wasn\'t a mistake.',
    'quote': '"If the music stops, something\'s wrong. It always stops before the worst things."',
  },

  {
    'name': 'Vivienne St. Claire',
    'arch': 'The Heiress',
    'meta': 'St. Claire Foundation, Park Avenue',
    'allg': 'Connection: Funded Whitmore\'s research ($3,000)',
    'physical': 'Age 34. The posture of someone who was taught to enter rooms correctly and has since learned to leave them strategically. Evening bag, good jewellery chosen for elegance not ostentation, a pocket revolver she mentions to no one. The composure of a woman who has funded three academic expeditions and attended the debrief on two of them — she knows that the debrief is always worse than the expedition.',
    'stats': [('STR','45'),('CON','55'),('SIZ','50'),('DEX','65'),('INT','80'),('POW','70'),('APP','90'),('EDU','75')],
    'derived': [('HP','11'),('MP','14'),('SAN','70'),('Luck','60'),('DB','-1'),('Build','-1'),('Move','7')],
    'skills': [
      ('Persuade','70%'),('Charm','75%'),('Credit Rating','90%'),
      ('Library Use','65%'),('Occult','50%'),('Psychology','65%'),
      ('Art/Craft (Drawing)','55%'),('History','50%'),
      ('Fast Talk','55%'),('Spot Hidden','45%'),
      ('Dodge','40%'),('Navigate','35%'),
      ('Firearms (Handgun)','35%'),('Drive Auto','50%'),
      ('Language (French)','60%'),('Language (German)','40%'),
      ('Accounting','50%'),('Law','40%'),
    ],
    'equipment': [
      'Automobile — waiting outside (chauffeur: Marcus, discreet)',
      'Evening bag: compact, $200 cash, calling cards, two keys she hasn\'t explained',
      'Pocket revolver (.22, 1D6, 6 shots) — very concealable, very well maintained',
      'Notebook of Whitmore\'s research extracts (her copies)',
      'A sealed letter to her solicitor, written this morning',
      'Opera glasses (useful in many contexts)',
    ],
    'weapons': [
      {'name':'.22 Pocket Revolver','skill':'Firearms (Handgun)','atk':'35%','par':'—','damage':'1D6','notes':'Rng 10yds · 6 shots · concealable · Mal 96'},
      {'name':'Fighting (Brawl)','skill':'Fighting (Brawl)','atk':'15%','par':'—','damage':'1D3+DB','notes':'DB: -1 · last resort only'},
    ],
    'sp_name': 'Investigator Brief — Vivienne St. Claire',
    'sp_type': 'Heiress/patron, age 34 · St. Claire Foundation · Funded Whitmore\'s research for 18 months',
    'sp_stats': 'Charm 75%  ·  Credit Rating 90%  ·  Persuade 70%  ·  Psychology 65%',
    'sp_abilities': [
      ('Personal Hook', 'Vivienne has read Whitmore\'s research notes carefully. She understands more than she lets on. Since signing the funding cheque, she has had recurring dreams: always the same corridor, always a door at the end she is very glad to wake up before opening.'),
      ('SAN Trigger', 'Having her sense of social control taken away. Being unable to talk her way out of something. The Watcher will remove every tool she knows how to use.'),
      ('Special Ability', 'Credit Rating 90%: money opens doors even at midnight. Automobile with discreet driver available. She is the best candidate to hold the mirror in the ritual — social courage taken to its absolute limit.'),
      ('Private Note', 'The sealed letter to her solicitor was written this morning. She has not told anyone. She has done this before expeditions. She considers it prudent.'),
    ],
    'sp_note': 'Vivienne is the character best placed to volunteer for the mirror scene. Social courage taken to its absolute limit is still courage.',
    'background': 'Heir to a shipping fortune, trustee of the St. Claire Foundation since age 28. Has funded two archaeological expeditions, one meteorological survey, and Whitmore\'s research into pre-Columbian ceremonial practice. She funds things that interest her; Whitmore interested her enormously. The dreams started eleven days after signing the cheque. She has not told Whitmore this. She has not told anyone this. She has been looking forward to and dreading this conversation in equal measure.',
    'hook': 'Vivienne has been having strange dreams since signing Whitmore\'s funding cheque — always the same corridor, always a door at the end she\'s very glad to wake up before opening.',
    'quote': '"I fund things that interest me. This no longer interests me. I want my money back."',
  },

  {
    'name': 'Prof. Walter Finch',
    'arch': 'The Academic',
    'meta': 'Columbia University, Comparative Religion',
    'allg': 'Connection: Whitmore\'s former graduate student',
    'physical': 'Age 52. The deliberate dishevelment of someone who has decided that precision in dress is less important than precision in thought and has been wrong about this socially for thirty years. Pipe and tobacco always present. Briefcase with a broken clasp, held shut by a thick rubber band. Reference cards in his breast pocket, some of them fifteen years old. A face that is better suited to scepticism than to belief — tonight it is doing neither.',
    'stats': [('STR','50'),('CON','60'),('SIZ','55'),('DEX','50'),('INT','90'),('POW','65'),('APP','55'),('EDU','90')],
    'derived': [('HP','12'),('MP','13'),('SAN','65'),('Luck','45'),('DB','0'),('Build','0'),('Move','7')],
    'skills': [
      ('Occult','70%'),('Library Use','80%'),('Cthulhu Mythos','20%'),
      ('History','75%'),('Language (Latin)','65%'),('Psychology','55%'),
      ('Spot Hidden','55%'),('Language (Greek)','50%'),
      ('Science (Archaeology)','50%'),('Persuade','45%'),
      ('Credit Rating','55%'),('Natural World','45%'),
      ('Language (German)','45%'),('Art/Craft (Writing)','60%'),
      ('Fighting (Brawl)','25%'),('Dodge','35%'),
      ('Drive Auto','30%'),('Accounting','30%'),
    ],
    'equipment': [
      'Briefcase (broken clasp, rubber band): notebook, twelve reference cards, annotated bibliography',
      'Pipe, tobacco pouch, three boxes of matches',
      'Reading glasses (in breast pocket)',
      'A fountain pen that leaks slightly',
      'Whitmore\'s letters — six of them, all read, none replied to',
      '$22 cash and an overdue library book',
    ],
    'weapons': [
      {'name':'Fighting (Brawl)','skill':'Fighting (Brawl)','atk':'25%','par':'—','damage':'1D3+DB','notes':'DB: 0 · purely defensive'},
      {'name':'Walking Stick','skill':'Fighting (Brawl)','atk':'25%','par':'25%','damage':'1D4+DB','notes':'Always present · can parry'},
    ],
    'sp_name': 'Investigator Brief — Prof. Walter Finch',
    'sp_type': 'Academic, age 52 · Columbia University, Comparative Religion · Whitmore\'s former student',
    'sp_stats': 'Library Use 80%  ·  Occult 70%  ·  History 75%  ·  Cthulhu Mythos 20%',
    'sp_abilities': [
      ('Personal Hook', 'Six weeks ago, Whitmore\'s letters began containing rough transcriptions of symbols from Ashworth\'s home. Finch recognised two of them. He should not have recognised any of them. He has not replied to a single letter. The guilt is eating him alive.'),
      ('SAN Trigger', 'Things that his academic frameworks cannot contain. He is most vulnerable when the intellectual scaffolding gives way — when the thing in front of him has no category. Thirty years of scholarship becomes thirty years of wrong assumptions.'),
      ('Special Ability', 'Cthulhu Mythos 20%: already has partial knowledge of what they\'re dealing with. Library Use 80%: fastest reader and cross-referencer in the group. Best candidate to lead the incantation from the Codex.'),
      ('Private Note', 'He knows what the two symbols mean. He\'s known for six weeks. He told himself he wasn\'t sure. He was sure. Tonight he carries that weight into the basement.'),
    ],
    'sp_note': 'Finch is the most intellectually equipped investigator and the one carrying the most guilt. The recognition of the symbols is the key to his character.',
    'background': 'Thirty years in comparative religion and pre-Christian ritual practice. Whitmore was his supervisor\'s student, fifteen years his senior, who treated his early work with exacting fairness and occasional devastating accuracy. He has spent fifteen years trying to catch up with her. When her letters became increasingly desperate, he told himself she was catastrophising. He filed them. He did not reply. He is here because the telegram arrived and he knew immediately it was real, and he understood immediately what that meant about his silence for six weeks.',
    'hook': 'He recognised two symbols from Whitmore\'s letters that he should not have recognised. He\'s been ignoring her increasingly desperate letters for six weeks. The guilt is eating him.',
    'quote': '"I\'ve spent thirty years studying what people believe. I\'ve always assumed there was a subject and an observer. I\'m revising that assumption."',
  },
]


# ═══════════════════════════════════════════════════════════════════════════════
# SANITY REFERENCE PAGE BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_san_reference_page(story, t, UW):
    S = make_styles(t)

    story.append(Spacer(1,2))
    story.append(Paragraph("KEEPER'S QUICK REFERENCE", S['ref_title']))
    story.append(Paragraph("Not Another Telegram  ·  Call of Cthulhu 7e  ·  New York City, 1924", S['ref_sub']))
    story.append(Spacer(1,4))
    story.append(OrnRule(UW, t))
    story.append(Spacer(1,5))

    # ── COMBAT & MECHANICS ─────────────────────────────────────────────────
    story.append(SectionBanner("CoC 7E — SKILL ROLLS & COMBAT", UW, t))
    story.append(Spacer(1,3))

    mech_rows = [[
        Paragraph('DIFFICULTY', S['ref_hdr']),
        Paragraph('HOW TO ROLL', S['ref_hdr']),
        Paragraph('RESULT', S['ref_hdr']),
    ]]
    for label, how, result in COMBAT_QUICK:
        mech_rows.append([
            Paragraph(label, S['ref_bold']),
            Paragraph(how,   S['ref_body']),
            Paragraph(result,S['ref_body']),
        ])
    mech_t = Table(mech_rows, colWidths=[UW*0.28, UW*0.38, UW*0.34])
    mech_ts = [
        ('BACKGROUND', (0,0),(-1,0), t.banner_bg),
        ('LINEBELOW',  (0,0),(-1,-1), 0.3, t.rule),
        ('LEFTPADDING',(0,0),(-1,-1), 6),('RIGHTPADDING',(0,0),(-1,-1), 4),
        ('TOPPADDING', (0,0),(-1,-1), 2),('BOTTOMPADDING',(0,0),(-1,-1), 2),
    ]
    for i in range(1, len(mech_rows)):
        mech_ts.append(('BACKGROUND',(0,i),(-1,i), t.row1 if i%2==1 else t.row2))
    mech_t.setStyle(TableStyle(mech_ts))
    story.append(mech_t)
    story.append(Spacer(1,5))

    # ── SANITY EVENTS ─────────────────────────────────────────────────────
    story.append(SectionBanner("SANITY EVENTS — THIS SCENARIO", UW, t))
    story.append(Spacer(1,3))

    # Colour zones
    SAN_COLORS = {
        'minor':  (colors.HexColor('#2A5020'), colors.HexColor('#E8F4E0'), colors.HexColor('#D0EAC0')),
        'medium': (colors.HexColor('#6A4000'), colors.HexColor('#F8EED0'), colors.HexColor('#F0DCA0')),
        'major':  (colors.HexColor('#7A1000'), colors.HexColor('#F6E0D8'), colors.HexColor('#EECAB8')),
        'reward': (colors.HexColor('#0A3070'), colors.HexColor('#E0ECFF'), colors.HexColor('#C0D8F8')),
    }
    san_zones = [
        ('minor',  "MINOR — atmospheric dread"),
        ('medium', "MODERATE — genuine horror"),
        ('major',  "MAJOR — confrontation"),
        ('reward', "REWARD"),
    ]
    san_buckets = {
        'minor':  SAN_EVENTS[:2],
        'medium': SAN_EVENTS[2:6],
        'major':  SAN_EVENTS[6:9],
        'reward': [SAN_EVENTS[9]],
    }

    san_tbl_rows = []
    san_style_cmds = [
        ('LINEBELOW',   (0,0),(-1,-1), 0.3, t.rule),
        ('LEFTPADDING', (0,0),(-1,-1), 6),('RIGHTPADDING',(0,0),(-1,-1), 4),
        ('TOPPADDING',  (0,0),(-1,-1), 2),('BOTTOMPADDING',(0,0),(-1,-1), 2),
        ('VALIGN',      (0,0),(-1,-1), 'TOP'),
    ]
    zone_hdr_s  = ParagraphStyle('zhs',fontName='Helvetica-Bold',fontSize=7.5,textColor=colors.white,leading=10)
    event_name_s= ParagraphStyle('ens',fontName='Times-Roman',   fontSize=8,  textColor=t.body,leading=10)
    san_loss_s  = ParagraphStyle('sls',fontName='Helvetica-Bold',fontSize=8,  textColor=t.body,leading=10,alignment=TA_CENTER)

    row_idx = 0
    for zone_key, zone_label in san_zones:
        hdr_col, light, dark = SAN_COLORS[zone_key]
        san_tbl_rows.append([
            Paragraph(zone_label, zone_hdr_s),
            Paragraph('', zone_hdr_s),
        ])
        san_style_cmds.append(('BACKGROUND',(0,row_idx),(-1,row_idx), hdr_col))
        san_style_cmds.append(('SPAN',(0,row_idx),(-1,row_idx)))
        row_idx += 1
        for i,(event, loss) in enumerate(san_buckets[zone_key]):
            bg = light if i%2==0 else dark
            san_tbl_rows.append([
                Paragraph(event, event_name_s),
                Paragraph(loss,  san_loss_s),
            ])
            san_style_cmds.append(('BACKGROUND',(0,row_idx),(-1,row_idx), bg))
            row_idx += 1

    san_t = Table(san_tbl_rows, colWidths=[UW*0.78, UW*0.22])
    san_t.setStyle(TableStyle(san_style_cmds))
    story.append(san_t)
    story.append(Spacer(1,4))

    # ── SKINLESS WATCHER STATS ─────────────────────────────────────────────
    story.append(SectionBanner("THE SKINLESS WATCHER — STAT SUMMARY", UW, t, special=True))
    story.append(Spacer(1,3))

    # Two-column layout
    w_left  = [s for s in WATCHER_STATS[:6]]
    w_right = WATCHER_STATS[6:]
    stat_lbl_s = ParagraphStyle('wsl',fontName='Helvetica-Bold',fontSize=7.5,textColor=t.special_label,leading=10)
    stat_val_s = ParagraphStyle('wsv',fontName='Times-Roman',   fontSize=8,  textColor=t.special_body,leading=10)

    w_rows = []
    for i, (lbl, val) in enumerate(w_left):
        # Pair with right column if available
        if i < len(w_right):
            rl, rv = w_right[i]
            w_rows.append([
                Paragraph(f"{lbl}:", stat_lbl_s), Paragraph(str(val), stat_val_s),
                Paragraph(f"{rl}:", stat_lbl_s), Paragraph(str(rv),   stat_val_s),
            ])
        else:
            w_rows.append([
                Paragraph(f"{lbl}:", stat_lbl_s), Paragraph(str(val), stat_val_s),
                Paragraph('', stat_lbl_s), Paragraph('', stat_val_s),
            ])
    # Remaining right-column rows
    for i in range(len(w_left), len(w_right)):
        rl, rv = w_right[i]
        w_rows.append([
            Paragraph('', stat_lbl_s), Paragraph('', stat_val_s),
            Paragraph(f"{rl}:", stat_lbl_s), Paragraph(str(rv), stat_val_s),
        ])

    col_q = UW / 4
    wt = Table(w_rows, colWidths=[col_q*0.35, col_q*0.65, col_q*0.6, col_q*1.4])
    wt_style = [
        ('BACKGROUND', (0,0),(-1,-1), t.special_bg),
        ('LINEBELOW',  (0,0),(-1,-1), 0.3, colors.HexColor('#3A2010')),
        ('BOX', (0,0),(-1,-1), 1.2, t.special_border),
        ('LEFTPADDING', (0,0),(-1,-1), 6),('RIGHTPADDING',(0,0),(-1,-1), 4),
        ('TOPPADDING',  (0,0),(-1,-1), 2),('BOTTOMPADDING',(0,0),(-1,-1), 2),
        ('VALIGN',      (0,0),(-1,-1), 'TOP'),
        ('LINEBEFORE',  (2,0),(2,-1), 0.5, colors.HexColor('#3A2010')),
    ]
    wt.setStyle(TableStyle(wt_style))
    story.append(wt)
    story.append(Spacer(1,4))

    story.append(Paragraph(
        "The Watcher cannot be harmed by conventional weapons. "
        "It has 2 points of physical resistance and is immune to fire. "
        "The ritual circle is the only resolution. Firearms and brawling are deeply unsatisfying and somewhat expensive in Sanity.",
        S['ref_note']))
    story.append(OrnRule(UW, t))
    story.append(Paragraph(
        '"Whatever face it wears, it is not the face. Whatever door it opens, the door opens from both sides."',
        S['quote']))
    story.append(OrnRule(UW, t))


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD FUNCTION
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

    # ── COVER ──────────────────────────────────────────────────────────────
    story.append(Spacer(1,68))
    story.append(Paragraph(cover_title, S['cover_title']))
    story.append(Spacer(1,4))
    story.append(Paragraph(cover_sub,   S['cover_sub']))
    story.append(Spacer(1,4))
    story.append(Paragraph(cover_byline,S['cover_byline']))
    story.append(Spacer(1,14))
    story.append(OrnRule(UW,t))
    story.append(Spacer(1,10))

    # Roster table
    roster = [[
        Paragraph(f"<b>{c['name']}</b>", S['cover_name']),
        Paragraph(c['arch'],             S['cover_arch']),
        Paragraph(c.get('meta',''),      S['cover_meta']),
    ] for c in CHARS]
    rt = Table(roster, colWidths=[UW*0.38, UW*0.38, UW*0.24])
    rt.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0),(-1,-1), [t.cover_row1, t.cover_row2]),
        ('LINEBELOW',      (0,0),(-1,-1), 0.4, t.rule),
        ('LINEABOVE',      (0,0),(-1, 0), 1.0, t.accent),
        ('LINEBELOW',      (0,-1),(-1,-1),1.0, t.accent),
        ('LEFTPADDING',    (0,0),(-1,-1), 8),('RIGHTPADDING',(0,0),(-1,-1), 6),
        ('TOPPADDING',     (0,0),(-1,-1), 5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ]))
    story.append(rt)
    story.append(Spacer(1,12))
    story.append(OrnRule(UW,t))
    story.append(Spacer(1,8))
    story.append(Paragraph("QUICK REFERENCE", S['rules_head']))

    rlt = Table(
        [[Paragraph(cell, S['cover_rule']) for cell in row] for row in rules],
        colWidths=[UW/3]*3
    )
    rlt.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0),(-1,-1), [t.cover_row1, t.cover_row2]),
        ('GRID',           (0,0),(-1,-1), 0.4, t.rule),
        ('ALIGN',          (0,0),(-1,-1), 'CENTER'),
        ('TOPPADDING',     (0,0),(-1,-1), 4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(rlt)
    story.append(Spacer(1,8))
    story.append(Paragraph(
        "Hand sheets face-down. Players choose by archetype, not stats.  "
        "Scenario begins 8:00 PM. Midnight is four hours away.",
        S['cover_note']))
    story.append(NextPageTemplate('normal'))
    story.append(PageBreak())

    # ── CHARACTER PAGES ────────────────────────────────────────────────────
    for char in CHARS:
        max_hp  = int(next(v for k,v in char['derived'] if k=='HP'))
        max_san = int(next(v for k,v in char['derived'] if k=='SAN'))
        max_luck= int(next(v for k,v in char['derived'] if k=='Luck'))
        dodge   = get_skill(char, 'dodge')
        db_val  = next((v for k,v in char['derived'] if k=='DB'), '0')

        # ── FRONT PAGE ─────────────────────────────────────────────────────
        story.append(CharHeader(char['name'],char['arch'],char['meta'],char['allg'],UW,t))
        story.append(Spacer(1,4))

        sk = char['skills']
        if len(sk)%2: sk = sk+[('','')]
        mid = len(sk)//2
        sk_rows = []
        for (la,lv),(ra,rv) in zip(sk[:mid], sk[mid:]):
            sk_rows.append([
                Paragraph(la,S['body_sm']), Paragraph(f"<b>{lv}</b>",S['body_sm']),
                Paragraph(ra,S['body_sm']), Paragraph(f"<b>{rv}</b>",S['body_sm']),
            ])
        skt = Table(sk_rows, colWidths=[SKH*0.72,SKH*0.28,SKH*0.72,SKH*0.28])
        skt.setStyle(TableStyle([
            ('ROWBACKGROUNDS', (0,0),(-1,-1), [t.row1,t.row2]),
            ('LINEBELOW',      (0,0),(-1,-1), 0.3, t.rule),
            ('LINEAFTER',      (1,0),(1,-1),  0.5, t.rule),
            ('LEFTPADDING',    (0,0),(-1,-1), 4),('RIGHTPADDING',(0,0),(-1,-1),3),
            ('TOPPADDING',     (0,0),(-1,-1), 1),('BOTTOMPADDING',(0,0),(-1,-1),1),
            ('ALIGN',          (1,0),(1,-1),  'RIGHT'),('ALIGN',(3,0),(3,-1),'RIGHT'),
        ]))

        left_items = [
            [SectionBanner("Characteristics", LW-4, t)],
            [Spacer(1,2)],
            [StatBlock(char['stats'], char['derived'], LW-4, t)],
            [Spacer(1,4)],
            [SectionBanner("Skills", LW-4, t)],
            [Spacer(1,2)],
            [skt],
        ]
        left_inner = Table(left_items, colWidths=[LW-4])
        left_inner.setStyle(TableStyle([
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING', (0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
        ]))

        if portraits and char['name'] in portraits:
            import os
            if os.path.exists(portraits[char['name']]):
                from reportlab.platypus import Image as RLImage
                right_ph = RLImage(portraits[char['name']], width=port_w, height=port_h)
            else:
                right_ph = PortraitPlaceholder(char['name'], port_w, port_h, t)
        else:
            right_ph = PortraitPlaceholder(char['name'], port_w, port_h, t)

        two_col = Table([[left_inner, right_ph]], colWidths=[LW, RW])
        two_col.setStyle(TableStyle([
            ('VALIGN',       (0,0),(-1,-1), 'TOP'),
            ('LEFTPADDING',  (0,0),(-1,-1), 0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',   (0,0),(-1,-1), 0),('BOTTOMPADDING',(0,0),(-1,-1),0),
            ('ALIGN',        (1,0),(1,-1),  'RIGHT'),
            ('LINEBEFORE',   (1,0),(1,-1),  0.5, t.accent),
        ]))
        story.append(two_col)
        story.append(Spacer(1,4))

        # Equipment
        story.append(SectionBanner("Equipment", UW, t))
        story.append(Spacer(1,2))
        eqt = Table([[Paragraph(f"\u2022 {item}", S['body_sm'])] for item in char['equipment']],
                    colWidths=[UW])
        eqt.setStyle(TableStyle([
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[t.row1,t.row2]),
            ('LINEBELOW',    (0,0),(-1,-1), 0.3, t.rule),
            ('LEFTPADDING',  (0,0),(-1,-1), 7),('RIGHTPADDING',(0,0),(-1,-1),4),
            ('TOPPADDING',   (0,0),(-1,-1), 1),('BOTTOMPADDING',(0,0),(-1,-1),1),
        ]))
        story.append(eqt)
        story.append(Spacer(1,4))

        # Combat
        story.append(SectionBanner("Combat", UW, t))
        story.append(Spacer(1,2))
        cw = [UW*0.26, UW*0.17, UW*0.09, UW*0.09, UW*0.13, UW*0.26]
        wep_rows = [[
            Paragraph('WEAPON',  S['wt_hdr']),
            Paragraph('SKILL',   S['wt_hdr']),
            Paragraph('ATK',     S['wt_hdr']),
            Paragraph('PAR',     S['wt_hdr']),
            Paragraph('DAMAGE',  S['wt_hdr']),
            Paragraph('NOTES',   S['wt_hdr']),
        ]]
        for w in char.get('weapons', []):
            wep_rows.append([
                Paragraph(w['name'],   S['wt_body']),
                Paragraph(w['skill'],  S['wt_body']),
                Paragraph(w['atk'],    S['wt_body_c']),
                Paragraph(w['par'],    S['wt_body_c']),
                Paragraph(w['damage'], S['wt_body_c']),
                Paragraph(w['notes'],  S['wt_body']),
            ])
        ts = [
            ('BACKGROUND',   (0,0),(-1,0),  t.banner_bg),
            ('TEXTCOLOR',    (0,0),(-1,0),  colors.white),
            ('LINEBELOW',    (0,0),(-1,-1), 0.3, t.rule),
            ('LINEAFTER',    (0,0),(4,-1),  0.3, t.rule),
            ('LEFTPADDING',  (0,0),(-1,-1), 5),('RIGHTPADDING',(0,0),(-1,-1),4),
            ('TOPPADDING',   (0,0),(-1,-1), 2),('BOTTOMPADDING',(0,0),(-1,-1),2),
            ('ALIGN',        (2,0),(4,-1),  'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ]
        for i in range(1, len(wep_rows)):
            ts.append(('BACKGROUND',(0,i),(-1,i), t.row1 if i%2==1 else t.row2))
        wt = Table(wep_rows, colWidths=cw); wt.setStyle(TableStyle(ts))
        story.append(wt)
        dodge_row = Table([[
            Paragraph(f"DODGE: <b>{dodge}</b>",  S['wt_dodge']),
            Paragraph(f"DAMAGE BONUS: <b>{db_val}</b>", S['wt_dodge']),
        ]], colWidths=[UW*0.45, UW*0.55])
        dodge_row.setStyle(TableStyle([
            ('BACKGROUND',  (0,0),(-1,-1), t.derived_bg),
            ('BOX',         (0,0),(-1,-1), 0.8, t.accent),
            ('LEFTPADDING', (0,0),(-1,-1), 10),
            ('TOPPADDING',  (0,0),(-1,-1), 4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ]))
        story.append(dodge_row)
        story.append(Spacer(1,5))

        # HP and SAN tracks (Luck displayed as derived stat, tracked on paper)
        story.append(HPTrack(max_hp, UW, t, label="HIT POINTS"))
        story.append(Spacer(1,4))
        story.append(HPTrack(max_san, UW, t, label="SANITY",
                             fill=t.san_box_fill, fill5=t.san_box_5th,
                             border=t.san_box_border, num=t.san_num, lbl_col=t.san_label))
        story.append(Spacer(1,4))
        # Luck as a simple labelled box (tracked manually)
        luck_row = Table([[
            Paragraph(f"LUCK (starting): <b>{max_luck}</b>", S['wt_dodge']),
            Paragraph("Track Luck on the back page notes section", S['wt_body']),
        ]], colWidths=[UW*0.40, UW*0.60])
        luck_row.setStyle(TableStyle([
            ('BACKGROUND',   (0,0),(-1,-1), t.luck_box_fill),
            ('BOX',          (0,0),(-1,-1), 0.8, t.luck_box_border),
            ('LEFTPADDING',  (0,0),(-1,-1), 10),
            ('TOPPADDING',   (0,0),(-1,-1), 4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ]))
        story.append(luck_row)
        story.append(PageBreak())

        # ── BACK PAGE ──────────────────────────────────────────────────────
        story.append(BackHeader(char['name'], char['arch'], UW, t))
        story.append(Spacer(1,6))
        story.append(Paragraph(f"<i>{char['physical']}</i>", S['italic_sm']))
        story.append(Spacer(1,8))

        # Investigator Brief box (dark)
        story.append(SectionBanner(t.special_label_str, UW, t, special=True))
        story.append(Spacer(1,3))
        dc = [
            Paragraph(char['sp_name'],  S['sp_title']),
            Paragraph(char['sp_type'],  S['sp_label']),
            Paragraph(char['sp_stats'], S['sp_body']),
        ]
        for abn, abd in char['sp_abilities']:
            dc.append(Paragraph(f"<b>{abn}:</b>  {abd}", S['sp_body']))
        dc.append(Paragraph(f"<i>{char['sp_note']}</i>", S['sp_body']))
        di = Table([[el] for el in dc], colWidths=[UW-18])
        di.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,-1), t.special_bg),
            ('LEFTPADDING',   (0,0),(-1,-1), 0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',    (0,0),(-1,-1), 1),('BOTTOMPADDING',(0,0),(-1,-1),1),
        ]))
        do = Table([[di]], colWidths=[UW])
        do.setStyle(TableStyle([
            ('BACKGROUND',   (0,0),(0,0), t.special_bg),
            ('BOX',          (0,0),(0,0), 1.2, t.special_border),
            ('LEFTPADDING',  (0,0),(0,0), 9),('RIGHTPADDING',(0,0),(0,0),9),
            ('TOPPADDING',   (0,0),(0,0), 5),('BOTTOMPADDING',(0,0),(0,0),5),
        ]))
        story.append(do)
        story.append(Spacer(1,6))

        # Background
        story.append(SectionBanner("Background", UW, t))
        story.append(Spacer(1,4))
        story.append(Paragraph(char['background'], S['body']))
        story.append(Spacer(1,5))

        # Personal Hook
        ht = Table([[
            Paragraph("PERSONAL HOOK:", S['hook_label']),
            Paragraph(char['hook'], S['hook_body']),
        ]], colWidths=[28*mm, UW-28*mm])
        ht.setStyle(TableStyle([
            ('BACKGROUND',   (0,0),(-1,-1), t.hook_bg),
            ('BOX',          (0,0),(-1,-1), 0.8, t.hook_border),
            ('LINEBEFORE',   (0,0),(0,-1),  3, t.hook_bar),
            ('LEFTPADDING',  (0,0),(-1,-1), 6),('RIGHTPADDING',(0,0),(-1,-1),6),
            ('TOPPADDING',   (0,0),(-1,-1), 5),('BOTTOMPADDING',(0,0),(-1,-1),5),
            ('VALIGN',       (0,0),(-1,-1), 'TOP'),
        ]))
        story.append(ht)
        story.append(Spacer(1,6))
        story.append(OrnRule(UW, t))
        story.append(Paragraph(char['quote'], S['quote']))
        story.append(OrnRule(UW, t))
        story.append(Spacer(1,8))

        # Notes
        story.append(SectionBanner("Notes", UW, t))
        story.append(Spacer(1,5))
        story.append(NotesBlock(UW, t, lines=8))
        story.append(PageBreak())

    # ── KEEPER REFERENCE PAGE ───────────────────────────────────────────────
    if append_reference:
        build_san_reference_page(story, t, UW)

    doc.build(story)
    print(f"Done: {path}")


# ── RUN ─────────────────────────────────────────────────────────────────────
NAT = not_another_telegram_theme()

# Portrait paths (placeholder — will be replaced with Midjourney art)
ART_NAT = '/home/claude/ChaosiumCon26/scenarios/art/event-93/player-characters'
NAT_PORTRAITS = {
    'Helen Cross':            f'{ART_NAT}/nat-pc01-helen-cross.jpeg',
    'Dr. Edmund Graves':      f'{ART_NAT}/nat-pc02-dr-edmund-graves.jpeg',
    'Mickey Doyle':           f'{ART_NAT}/nat-pc03-mickey-doyle.jpeg',
    'Louis "Lucky" Beaumont': f'{ART_NAT}/nat-pc04-louis-lucky-beaumont.jpeg',
    'Vivienne St. Claire':    f'{ART_NAT}/nat-pc05-vivienne-st-claire.jpeg',
    'Prof. Walter Finch':     f'{ART_NAT}/nat-pc06-prof-walter-finch.jpeg',
}

NAT_RULES = [
    ['HP = (CON+SIZ)÷10  round up', 'MP = POW÷5  round down', 'SAN = POW'],
    ['LUCK = POW×5  (starting)', 'DB: STR+SIZ 2–64 = None', '65–84: +1D4  ·  85–124: +1D6'],
    ['Regular: roll ≤ skill', 'Hard: roll ≤ skill÷2', 'Extreme: roll ≤ skill÷5'],
]

build_pdf(
    '/mnt/user-data/outputs/coc-not-another-telegram-characters.pdf',
    NAT_CHARS, NAT,
    "NOT ANOTHER TELEGRAM",
    "Player Character Reference — New York City, 1924",
    "Call of Cthulhu 7th Edition  ·  Event 93  ·  ChaosiumCon 2026",
    NAT_RULES,
    portraits=NAT_PORTRAITS,
    append_reference=True,
)
