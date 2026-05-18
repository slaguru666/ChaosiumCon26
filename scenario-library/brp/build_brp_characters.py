#!/usr/bin/env python3
"""
BRP Character Sheet PDF Generator
Event 91 — The Night Crawler (neo-noir cyberpunk)
Event 159 — Day One (urban survival horror)
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

PAGE_W, PAGE_H = A4
MARGIN = 17 * mm
UW = PAGE_W - 2 * MARGIN

# ═══════════════════════════════════════════════════════════════════════════════
# THEME DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

class Theme:
    pass

def night_crawler_theme():
    t = Theme()
    t.name = 'night_crawler'
    # Colours
    t.page_bg         = colors.HexColor('#0B0F1A')
    t.page_bg2        = colors.HexColor('#111827')
    t.header_bg       = colors.HexColor('#060910')
    t.header_border   = colors.HexColor('#00BFFF')
    t.header_inner    = colors.HexColor('#0D1525')
    t.accent          = colors.HexColor('#00BFFF')      # electric cyan
    t.accent2         = colors.HexColor('#7B4FFF')      # purple
    t.gold            = colors.HexColor('#00BFFF')
    t.rule            = colors.HexColor('#1E3A5F')
    t.banner_bg       = colors.HexColor('#0D1A30')
    t.banner_special  = colors.HexColor('#0D0520')      # augment banner
    t.special_bg      = colors.HexColor('#040810')
    t.special_border  = colors.HexColor('#0066CC')
    t.stat_header_bg  = colors.HexColor('#0D1A30')
    t.stat_row1       = colors.HexColor('#F0EDE5')
    t.stat_row2       = colors.HexColor('#E5E1D5')
    t.stat_val_col    = colors.HexColor('#1A3050')
    t.parchment       = colors.HexColor('#E8E4DA')
    t.parchment_dark  = colors.HexColor('#DDD8C8')
    t.page_text_rule  = colors.HexColor('#1A3050')
    t.cover_band      = colors.HexColor('#00BFFF')
    t.cover_band2     = colors.HexColor('#0A1428')
    t.hp_box_fill     = colors.HexColor('#E8F4FF')
    t.hp_box_border   = colors.HexColor('#00BFFF')
    t.hp_shadow       = colors.HexColor('#7BCFFF')
    t.hp_num_col      = colors.HexColor('#0D1A30')
    t.hp_label_col    = colors.HexColor('#00BFFF')
    t.back_bg         = colors.HexColor('#050810')
    t.back_border     = colors.HexColor('#00BFFF')
    t.hook_bg         = colors.HexColor('#0A1525')
    t.hook_border     = colors.HexColor('#00BFFF')
    t.hook_bar        = colors.HexColor('#00BFFF')
    # Text colours
    t.header_name     = colors.white
    t.header_sub      = colors.HexColor('#7BE0FF')
    t.header_right    = colors.HexColor('#A0C8FF')
    t.banner_text     = colors.white
    t.special_title   = colors.HexColor('#7BE0FF')
    t.special_label   = colors.HexColor('#00BFFF')
    t.special_body    = colors.HexColor('#C0D8F0')
    t.body_col        = colors.HexColor('#1A1008')
    t.italic_col      = colors.HexColor('#4A5A6A')
    t.quote_col       = colors.HexColor('#00BFFF')
    t.hook_label_col  = colors.HexColor('#00BFFF')
    t.hook_body_col   = colors.HexColor('#D0E8FF')
    t.footer_col      = colors.HexColor('#1A3050')
    t.footer_text     = "The Night Crawler  ·  BRP  ·  Event 91  ·  ChaosiumCon 2026"
    t.cover_title_col = colors.HexColor('#00BFFF')
    t.cover_sub_col   = colors.HexColor('#7BE0FF')
    t.cover_body_col  = colors.HexColor('#C0D8F0')
    # Labels
    t.special_section = "Augment"
    t.back_note       = "Neo-Ashford, 2087  ·  Background & Notes"
    return t

def day_one_theme():
    t = Theme()
    t.name = 'day_one'
    # Colours
    t.page_bg         = colors.HexColor('#F5F0E8')
    t.page_bg2        = colors.HexColor('#EDE8DE')
    t.header_bg       = colors.HexColor('#141414')
    t.header_border   = colors.HexColor('#CC2200')
    t.header_inner    = colors.HexColor('#1E1E1E')
    t.accent          = colors.HexColor('#CC2200')      # emergency red
    t.accent2         = colors.HexColor('#8B4500')
    t.gold            = colors.HexColor('#CC2200')
    t.rule            = colors.HexColor('#8B3300')
    t.banner_bg       = colors.HexColor('#2A2A2A')
    t.banner_special  = colors.HexColor('#4A0800')
    t.special_bg      = colors.HexColor('#1A0800')
    t.special_border  = colors.HexColor('#CC2200')
    t.stat_header_bg  = colors.HexColor('#2A2A2A')
    t.stat_row1       = colors.HexColor('#F7F5F0')
    t.stat_row2       = colors.HexColor('#EEEBE3')
    t.stat_val_col    = colors.HexColor('#2A2A2A')
    t.parchment       = colors.HexColor('#F5F0E8')
    t.parchment_dark  = colors.HexColor('#EDE8DE')
    t.page_text_rule  = colors.HexColor('#8B3300')
    t.cover_band      = colors.HexColor('#CC2200')
    t.cover_band2     = colors.HexColor('#2A2A2A')
    t.hp_box_fill     = colors.HexColor('#FFF0EE')
    t.hp_box_border   = colors.HexColor('#CC2200')
    t.hp_shadow       = colors.HexColor('#FFB0A0')
    t.hp_num_col      = colors.HexColor('#2A2A2A')
    t.hp_label_col    = colors.HexColor('#CC2200')
    t.back_bg         = colors.HexColor('#141414')
    t.back_border     = colors.HexColor('#CC2200')
    t.hook_bg         = colors.HexColor('#F5E8E5')
    t.hook_border     = colors.HexColor('#CC2200')
    t.hook_bar        = colors.HexColor('#CC2200')
    # Text colours
    t.header_name     = colors.white
    t.header_sub      = colors.HexColor('#FFB0A0')
    t.header_right    = colors.HexColor('#FFCCBB')
    t.banner_text     = colors.white
    t.special_title   = colors.HexColor('#FFB0A0')
    t.special_label   = colors.HexColor('#FF8060')
    t.special_body    = colors.HexColor('#FFD0C0')
    t.body_col        = colors.HexColor('#1A1008')
    t.italic_col      = colors.HexColor('#4A3020')
    t.quote_col       = colors.HexColor('#CC2200')
    t.hook_label_col  = colors.HexColor('#CC2200')
    t.hook_body_col   = colors.HexColor('#3A1008')
    t.footer_col      = colors.HexColor('#8B3300')
    t.footer_text     = "Day One  ·  BRP  ·  Event 159  ·  ChaosiumCon 2026"
    t.cover_title_col = colors.HexColor('#CC2200')
    t.cover_sub_col   = colors.HexColor('#8B3300')
    t.cover_body_col  = colors.HexColor('#2A2A2A')
    # Labels
    t.special_section = "What You're Carrying"
    t.back_note       = "London, 17 May 2026  ·  Background & Notes"
    return t

# ═══════════════════════════════════════════════════════════════════════════════
# STYLES
# ═══════════════════════════════════════════════════════════════════════════════

def make_styles(T):
    WHITE = colors.white
    return {
        'doc_title':    ParagraphStyle('dt',  fontName='Times-BoldItalic', fontSize=28, textColor=T.cover_title_col, alignment=TA_CENTER, leading=34, spaceAfter=4),
        'doc_sub':      ParagraphStyle('ds',  fontName='Times-Italic',     fontSize=13, textColor=T.cover_sub_col,   alignment=TA_CENTER, leading=18, spaceAfter=2),
        'doc_byline':   ParagraphStyle('dbl', fontName='Helvetica',        fontSize=9,  textColor=T.cover_body_col,  alignment=TA_CENTER, leading=13),
        'cover_name':   ParagraphStyle('cn',  fontName='Times-Bold',       fontSize=11, textColor=T.cover_body_col,  leading=16),
        'toc_sub':      ParagraphStyle('ts',  fontName='Helvetica',        fontSize=9,  textColor=T.accent,          leading=13),
        'rules_head':   ParagraphStyle('rh',  fontName='Times-Bold',       fontSize=10, textColor=T.accent,          alignment=TA_CENTER, leading=14, spaceBefore=4, spaceAfter=3),
        'cover_note':   ParagraphStyle('cno', fontName='Times-Italic',     fontSize=9,  textColor=T.cover_body_col,  alignment=TA_CENTER, leading=13),
        'body':         ParagraphStyle('b',   fontName='Times-Roman',      fontSize=9,  textColor=T.body_col,        leading=13, spaceAfter=3, alignment=TA_JUSTIFY),
        'body_sm':      ParagraphStyle('bs',  fontName='Times-Roman',      fontSize=8,  textColor=T.body_col,        leading=11, spaceAfter=2, alignment=TA_JUSTIFY),
        'sp_title':     ParagraphStyle('spt', fontName='Times-BoldItalic', fontSize=11, textColor=T.special_title,   leading=14, spaceBefore=1),
        'sp_label':     ParagraphStyle('spl', fontName='Helvetica-Bold',   fontSize=7.5,textColor=T.special_label,   leading=11, spaceAfter=1),
        'sp_body':      ParagraphStyle('spb', fontName='Times-Roman',      fontSize=8.5,textColor=T.special_body,    leading=12, spaceAfter=2, alignment=TA_JUSTIFY),
        'hook_label':   ParagraphStyle('hl',  fontName='Helvetica-Bold',   fontSize=8,  textColor=T.hook_label_col,  leading=11),
        'hook_body':    ParagraphStyle('hb',  fontName='Times-Italic',     fontSize=8.5,textColor=T.hook_body_col,   leading=12, spaceAfter=2, alignment=TA_JUSTIFY),
        'quote':        ParagraphStyle('q',   fontName='Times-Italic',     fontSize=9,  textColor=T.quote_col,       alignment=TA_CENTER, leading=13, spaceBefore=3),
        'italic_sm':    ParagraphStyle('is',  fontName='Times-Italic',     fontSize=8,  textColor=T.italic_col,      leading=11, alignment=TA_JUSTIFY),
    }

# ═══════════════════════════════════════════════════════════════════════════════
# FLOWABLES
# ═══════════════════════════════════════════════════════════════════════════════

class OrnRule(Flowable):
    def __init__(self, width, T):
        super().__init__()
        self._T=T; self.width=width; self.height=8
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; c.setFillColor(self._T.accent); c.setStrokeColor(self._T.accent); c.setLineWidth(0.5)
        mid=self.width/2
        c.line(0,4,mid-8,4); c.line(mid+8,4,self.width,4)
        for x in [0,mid,self.width]:
            c.saveState(); c.translate(x,4); c.rotate(45)
            c.rect(-2.5,-2.5,5,5,fill=1,stroke=0); c.restoreState()

class CharHeader(Flowable):
    def __init__(self, name, archetype, meta, allegiance, width, T):
        super().__init__()
        self._n=name; self._arc=archetype; self._meta=meta; self._all=allegiance
        self.width=width; self.height=52; self._T=T
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; T=self._T; w,h=self.width,self.height
        c.setFillColor(T.header_bg); c.roundRect(0,0,w,h,3,fill=1,stroke=0)
        c.setFillColor(T.header_inner); c.roundRect(2,2,w-4,h-4,2,fill=1,stroke=0)
        c.setStrokeColor(T.header_border); c.setLineWidth(1.0); c.roundRect(1,1,w-2,h-2,3,fill=0,stroke=1)
        c.setStrokeColor(T.accent); c.setLineWidth(0.4); c.line(12,h-30,w-12,h-30)
        c.setFillColor(T.header_name); c.setFont('Times-BoldItalic',20); c.drawString(12,h-22,self._n)
        c.setFillColor(T.header_sub); c.setFont('Helvetica',8.5)
        c.drawString(12,h-38,f"{self._arc}  \u00b7  {self._meta}")
        c.setFillColor(T.header_right); c.setFont('Helvetica',7.5)
        c.drawRightString(w-10,h-38,self._all)
        c.setFillColor(T.accent)
        for cx,cy in [(6,h-6),(w-6,h-6),(6,6),(w-6,6)]:
            c.saveState(); c.translate(cx,cy); c.rotate(45)
            c.rect(-2,-2,4,4,fill=1,stroke=0); c.restoreState()

class StatBlock(Flowable):
    def __init__(self, stats, derived, width, T):
        super().__init__()
        self._s=stats; self._d=derived; self.width=width; self.height=56; self._T=T
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; T=self._T; w=self.width; n=len(self._s); bw=(w-4)/n
        for i,(label,val) in enumerate(self._s):
            x=i*bw+2
            c.setFillColor(T.stat_header_bg); c.rect(x,22,bw-1,12,fill=1,stroke=0)
            c.setFillColor(T.stat_row1); c.rect(x,8,bw-1,14,fill=1,stroke=0)
            c.setStrokeColor(T.rule); c.setLineWidth(0.5); c.rect(x,8,bw-1,26,fill=0,stroke=1)
            c.setFillColor(T.accent); c.setFont('Helvetica-Bold',7)
            c.drawCentredString(x+(bw-1)/2,28,label)
            c.setFillColor(T.stat_val_col); c.setFont('Times-Bold',13)
            c.drawCentredString(x+(bw-1)/2,11,str(val))
        x_pos=2
        for lbl,val in self._d:
            c.setFillColor(T.accent); c.setFont('Helvetica-Bold',7.5)
            c.drawString(x_pos,1,lbl+": ")
            tw=c.stringWidth(lbl+": ",'Helvetica-Bold',7.5)
            c.setFillColor(T.stat_val_col); c.setFont('Times-Bold',7.5)
            c.drawString(x_pos+tw,1,str(val))
            x_pos+=tw+c.stringWidth(str(val),'Times-Bold',7.5)+12

class SectionBanner(Flowable):
    def __init__(self, text, width, T, special=False):
        super().__init__()
        self._t=text; self._sp=special; self.width=width; self.height=16; self._T=T
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; T=self._T
        bg=T.banner_special if self._sp else T.banner_bg
        c.setFillColor(bg); c.rect(0,0,self.width,16,fill=1,stroke=0)
        c.setStrokeColor(T.accent); c.setLineWidth(0.5); c.rect(0,0,self.width,16,fill=0,stroke=1)
        c.setFillColor(T.banner_text); c.setFont('Times-Bold',9.5); c.drawString(8,4.5,self._t.upper())

class HPTrack(Flowable):
    BOX=15; GAP=3
    def __init__(self, max_hp, width, T):
        super().__init__()
        self.max_hp=max_hp; self.width=width; self._T=T
        bpr=int(width/(self.BOX+self.GAP))
        self.bpr=bpr; self.rows=(max_hp+bpr-1)//bpr
        self.height=18+self.rows*(self.BOX+10+self.GAP)
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; T=self._T; B,G=self.BOX,self.GAP
        max_hp=self.max_hp; bpr=self.bpr; w=self.width; top=self.height-2
        c.setFillColor(T.hp_label_col); c.setFont('Times-Bold',9)
        c.drawString(0,top-12,"HIT POINTS")
        c.setFillColor(T.accent); c.setFont('Helvetica-Bold',8)
        c.drawRightString(w,top-12,f"MAX  {max_hp}")
        c.setStrokeColor(T.rule); c.setLineWidth(0.4); c.line(0,top-15,w,top-15)
        y_start=top-18
        for i in range(max_hp):
            row=i//bpr; col=i%bpr
            iir=min(bpr,max_hp-row*bpr)
            rtw=iir*(B+G)-G; sx=(w-rtw)/2
            x=sx+col*(B+G); y=y_start-row*(B+10+G); hp=max_hp-i
            c.setFillColor(T.hp_shadow); c.rect(x+1,y-1,B,B,fill=1,stroke=0)
            c.setFillColor(T.hp_box_fill); c.setStrokeColor(T.hp_box_border)
            c.setLineWidth(0.9); c.rect(x,y,B,B,fill=1,stroke=1)
            c.setStrokeColor(colors.HexColor('#C0B8A8')); c.setLineWidth(0.3); t=3
            c.line(x,y+B-t,x+t,y+B-t); c.line(x,y,x+t,y)
            c.line(x+B-t,y+B,x+B,y+B); c.line(x+B-t,y,x+B,y)
            c.setFillColor(T.hp_num_col); c.setFont('Helvetica-Bold',7)
            c.drawCentredString(x+B/2,y+(B-6)/2,str(hp))
        for i in range(max_hp):
            hp=max_hp-i
            if hp%5==0:
                row=i//bpr; col=i%bpr
                iir=min(bpr,max_hp-row*bpr)
                rtw=iir*(B+G)-G; sx=(w-rtw)/2
                x=sx+col*(B+G); y=y_start-row*(B+10+G)
                c.setFillColor(T.accent); c.setFont('Helvetica',5.5)
                c.drawCentredString(x+B/2,y-7,str(hp))

class SanTrack(Flowable):
    """Sanity point track — identical logic to HP but with different label."""
    BOX=12; GAP=2
    def __init__(self, max_san, width, T):
        super().__init__()
        self.max_san=max_san; self.width=width; self._T=T
        bpr=int(width/(self.BOX+self.GAP))
        self.bpr=bpr; self.rows=(max_san+bpr-1)//bpr
        self.height=18+self.rows*(self.BOX+8+self.GAP)
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; T=self._T; B,G=self.BOX,self.GAP
        max_san=self.max_san; bpr=self.bpr; w=self.width; top=self.height-2
        c.setFillColor(T.accent2); c.setFont('Times-Bold',9)
        c.drawString(0,top-12,"SANITY POINTS")
        c.setFillColor(T.accent2); c.setFont('Helvetica-Bold',8)
        c.drawRightString(w,top-12,f"MAX  {max_san}")
        c.setStrokeColor(T.rule); c.setLineWidth(0.4); c.line(0,top-15,w,top-15)
        y_start=top-18
        san_fill=colors.HexColor('#F0F8F0') if T.name=='night_crawler' else colors.HexColor('#F0F8F0')
        san_bord=colors.HexColor('#2A8040') if T.name=='night_crawler' else colors.HexColor('#2A8040')
        for i in range(max_san):
            row=i//bpr; col=i%bpr
            iir=min(bpr,max_san-row*bpr)
            rtw=iir*(B+G)-G; sx=(w-rtw)/2
            x=sx+col*(B+G); y=y_start-row*(B+8+G); sv=max_san-i
            c.setFillColor(san_fill); c.setStrokeColor(san_bord)
            c.setLineWidth(0.7); c.rect(x,y,B,B,fill=1,stroke=1)
            c.setFillColor(colors.HexColor('#1A3020')); c.setFont('Helvetica-Bold',6)
            c.drawCentredString(x+B/2,y+(B-5)/2,str(sv))
        for i in range(max_san):
            sv=max_san-i
            if sv%5==0:
                row=i//bpr; col=i%bpr
                iir=min(bpr,max_san-row*bpr)
                rtw=iir*(B+G)-G; sx=(w-rtw)/2
                x=sx+col*(B+G); y=y_start-row*(B+8+G)
                c.setFillColor(colors.HexColor('#2A8040')); c.setFont('Helvetica',5.5)
                c.drawCentredString(x+B/2,y-6,str(sv))

class BackHeader(Flowable):
    def __init__(self, name, archetype, width, T):
        super().__init__()
        self._n=name; self._arc=archetype; self.width=width; self.height=28; self._T=T
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; T=self._T; w,h=self.width,self.height
        c.setFillColor(T.back_bg); c.roundRect(0,0,w,h,3,fill=1,stroke=0)
        c.setStrokeColor(T.back_border); c.setLineWidth(0.8); c.roundRect(1,1,w-2,h-2,2,fill=0,stroke=1)
        c.setFillColor(colors.white); c.setFont('Times-BoldItalic',14); c.drawString(10,h-19,self._n)
        nw=c.stringWidth(self._n,'Times-BoldItalic',14)
        c.setFillColor(T.header_sub); c.setFont('Helvetica',8)
        c.drawString(14+nw,h-18,f"\u00b7  {self._arc}  \u00b7  {T.back_note}")
        c.setFillColor(T.accent)
        for cx,cy in [(5,h-5),(w-5,h-5),(5,5),(w-5,5)]:
            c.saveState(); c.translate(cx,cy); c.rotate(45)
            c.rect(-1.5,-1.5,3,3,fill=1,stroke=0); c.restoreState()

class NotesBlock(Flowable):
    def __init__(self, width, T, lines=6):
        super().__init__()
        self.width=width; self._T=T; self.lines=lines; self.height=lines*16+4
    def wrap(self,a,b): return (self.width,self.height)
    def draw(self):
        c=self.canv; c.setStrokeColor(self._T.rule); c.setLineWidth(0.4)
        for i in range(self.lines):
            y=self.height-(i+1)*16+4; c.line(0,y,self.width,y)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE BACKGROUNDS
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_bg(T):
    def draw_bg(c, doc):
        c.saveState(); w,h=A4
        c.setFillColor(T.parchment); c.rect(0,0,w,h,fill=1,stroke=0)
        # Subtle texture
        c.setStrokeColor(colors.HexColor('#DDD8C8') if T.name=='day_one' else colors.HexColor('#E8E4DA'))
        c.setLineWidth(0.15)
        for y in range(0,int(h),8): c.line(0,y,w,y)
        # Border
        c.setStrokeColor(T.rule); c.setLineWidth(1.5); c.rect(8,8,w-16,h-16,fill=0,stroke=1)
        c.setStrokeColor(T.accent); c.setLineWidth(0.4); c.rect(11,11,w-22,h-22,fill=0,stroke=1)
        c.setFont('Times-Italic',8); c.setFillColor(T.footer_col)
        c.drawCentredString(w/2,14,T.footer_text)
        c.restoreState()
    return draw_bg

def make_cover_bg(T):
    def draw_bg(c, doc):
        c.saveState(); w,h=A4
        if T.name == 'night_crawler':
            c.setFillColor(colors.HexColor('#060A12')); c.rect(0,0,w,h,fill=1,stroke=0)
            c.setFillColor(colors.HexColor('#0B1528')); c.roundRect(20,20,w-40,h-40,5,fill=1,stroke=0)
            # Subtle grid lines (cyberpunk grid)
            c.setStrokeColor(colors.HexColor('#0F2040')); c.setLineWidth(0.2)
            for y in range(20,int(h)-20,12): c.line(20,y,w-20,y)
            for x in range(20,int(w)-20,20): c.line(x,20,x,h-20)
        else:
            c.setFillColor(colors.HexColor('#1A1A1A')); c.rect(0,0,w,h,fill=1,stroke=0)
            c.setFillColor(T.parchment); c.roundRect(20,20,w-40,h-40,5,fill=1,stroke=0)
            c.setStrokeColor(colors.HexColor('#DDD8C8')); c.setLineWidth(0.15)
            for y in range(20,int(h)-20,7): c.line(20,y,w-20,y)
        # Bands
        c.setFillColor(T.cover_band); c.rect(20,h-90,w-40,70,fill=1,stroke=0)
        c.setFillColor(T.cover_band2 if T.name!='night_crawler' else T.cover_band)
        c.rect(20,20,w-40,50,fill=1,stroke=0)
        # Border
        c.setStrokeColor(T.accent); c.setLineWidth(2.0); c.roundRect(20,20,w-40,h-40,5,fill=0,stroke=1)
        c.setLineWidth(0.6); c.roundRect(25,25,w-50,h-50,3,fill=0,stroke=1)
        c.setLineWidth(1.0)
        for y in [h-90,h-20,70,20]: c.line(20,y,w-20,y)
        c.restoreState()
    return draw_bg

# ═══════════════════════════════════════════════════════════════════════════════
# CHARACTER DATA
# ═══════════════════════════════════════════════════════════════════════════════

NC_CHARS = [
  { 'name':'Sable Kress', 'archetype':'The Fixer', 'meta':'Ilmioran',
    'allegiance':'Neo-Ashford Operative',
    'physical':'Late thirties. Corporate-smooth face and contractor-worn hands. Moves between rooms as if she has been in every one before. Corporate-grade jaw augment visible as a faint ridge. Expensive coat. Never holds eye contact for more than necessary.',
    'stats':[('STR','11'),('CON','12'),('SIZ','11'),('INT','15'),('POW','13'),('DEX','12'),('APP','14')],
    'derived':[('HP','12'),('PP','13'),('DB','None'),('SR','23'),('Move','10')],
    'skills':[
      ('Persuade','65%'),('Fast Talk','60%'),('Insight','55%'),('Status','50%'),
      ('Bargain','55%'),('Streetwise','50%'),('Dodge','40%'),('Stealth','30%'),
      ('Spot Hidden','40%'),('Drive','45%'),('Law','35%'),('Research','45%'),
      ('Firearms (Pistol)','40%'),('Psychology','50%'),('Disguise','30%'),('Perception','45%'),
      ('Computer Use','35%'),('Intimidate','35%'),
    ],
    'equipment':[
      'Corporate-grade encrypted comm — one-time wipe if seized',
      'Two burner comms — already registered to dead accounts',
      'Licensed sidearm (2D6, rarely fired) — licensed in her real name',
      'Three contact IDs she would rather not explain',
      'Hardcopy NDA from Sable Morn — partially read, half understood',
      '4,000 credits upfront payment — loaded to a cold account',
    ],
    'sp_name':'"Subdermal Comms Mesh"',
    'sp_type':'Corporate-grade neural comm implant — jaw-line subdermal installation',
    'sp_stats':'Manufacturer: Veltris Internal / Grade: Corporate / Age: 3 years',
    'sp_abilities':[
      ('Encrypted channel','Passive two-way comms with any team member within 500m. Unjammable on standard frequencies. Veltris corporate security can intercept it. She does not know this.'),
      ('Signal sense','Can detect active comm transmissions within 10m (+20% Electronics passive). Shows as a faint pressure sensation.'),
      ('Emergency wipe','One-use: destroys all comm history and current channel on voice command. Leaves a two-day headache.'),
      ('Cost','Veltris issued this augment. It has a passive telemetry ping. Sable believes it was deactivated when she went freelance. It was not.'),
    ],
    'sp_note':'Sable has had this for three years and treats it as entirely hers. She does not know Veltris has a read on her location at all times. When Sable Morn smiled at the briefing, she already knew exactly where the team was standing.',
    'background':'Eleven years working corporate-adjacent contracts across the eight dominant corporations. Never full-time for any of them — contractor classification keeps the benefits low and the distance useful. Three Veltris contracts before tonight. Knows Sable Morn professionally, which means she knows that Sable Morn smiles at the debrief and that nobody who talks gets a fourth contract. Has been paid not to ask questions. Tonight is going to cost her that.',
    'hook':'Has worked Veltris contracts three times. She knows Sable Morn. She knows the smile. She knows what a fourth contract means and what the absence of one means. Tonight she is going to have to ask the questions she was paid not to ask.',
    'quote':'"I know what this job is. I also know what it costs to say no. Let\'s move."',
  },
  { 'name':'Juno Rhee', 'archetype':'The Ghost', 'meta':'Sub-District 7, Neo-Ashford',
    'allegiance':'Neo-Ashford Operative',
    'physical':'Late twenties, looks younger. Small and fast. Subdermal rig visible only as faint lines at the collarbone if the light catches right. Black-weave clothing, no reflective surfaces. The kind of stillness that comes from training, not calm.',
    'stats':[('STR','11'),('CON','13'),('SIZ','10'),('INT','14'),('POW','12'),('DEX','16'),('APP','11')],
    'derived':[('HP','12'),('PP','12'),('DB','None'),('SR','26'),('Move','12')],
    'skills':[
      ('Stealth','70%'),('Spot Hidden','60%'),('Perception','55%'),('Electronics','50%'),
      ('Pick Lock','55%'),('Dodge','55%'),('Security Systems','55%'),('Climb','55%'),
      ('Athletics','50%'),('Jump','50%'),('Sleight of Hand','40%'),('Disguise','45%'),
      ('Firearms (Pistol)','40%'),('Melee','45%'),('Surveillance','50%'),('Drive','45%'),
      ('Streetwise','50%'),('Computer Use','40%'),
    ],
    'equipment':[
      'Surveillance-countermeasure suite — jams drone ID reads within 5m (active, drains power)',
      'Black-weave bodysuit — 1-point armour, no thermal signature',
      'Monoblade (1D6+1) — ceramic, does not trigger metal detectors',
      'Micro-fibre grapple rig — 30m, silent deployment',
      'Two burner comms — physical cash-loaded, no chip trace',
      'Four-day emergency ration pack and water purification tabs',
    ],
    'sp_name':'"ECM Shroud Suite"',
    'sp_type':'Active electronic countermeasure implant — collarbone and shoulder subdermal installation',
    'sp_stats':'Manufacturer: Black market chop-shop / Grade: Military-pattern clone / Age: 18 months',
    'sp_abilities':[
      ('Drone ID blackout','Active: within 5m, all drone facial and biometric recognition returns null. Costs 1 power cell per 30 minutes. She carries six.'),
      ('+20% Stealth (active)','While the ECM suite is running, electronic motion sensors and surveillance systems treat her as background noise.'),
      ('Signal intercept','Passive: can hear unencrypted comm traffic on standard frequencies. Comes through as a faint hiss with identifiable speech at Electronics 40%.'),
      ('Cost','The suit runs hot. After 2 hours continuous use: -10% to all fine motor skills (tremor in the hands). After 4 hours: the headaches start. The chop-shop warranty expired six months ago.'),
    ],
    'sp_note':'Juno acquired this eighteen months ago from a contact in Sub-District 8. It was described as a "military-pattern clone with full function." Two of the six originally listed functions do not work. The three that do work have kept her alive. The tremor issue is newer than she has admitted to anyone.',
    'background':'Grew up in Sub-District 7. Left at seventeen for corporate-side work. Has been back only twice — both times fast, both times professionally. The Terminus Bar is known to her. So is Jed Osler — there is a debt between them from a decade ago, the kind that doesn\'t require repayment but also never fully dissolves. Coming back tonight will feel like something she can\'t name. She has decided not to examine that until afterward.',
    'hook':'The Terminus Bar is Sub-District 7 territory — her territory. She knows Jed Osler. She owes Jed Osler one, from a decade ago. She has not been back since going corporate-side. Coming back tonight will feel like something she cannot name.',
    'quote':'"Don\'t worry about the suit. Worry about what\'s in the tunnels."',
  },
  { 'name':'Viktor Drav', 'archetype':'The Muscle', 'meta':'Ex-Meridian Security Group',
    'allegiance':'Neo-Ashford Operative',
    'physical':'Late thirties. Large, economical, carries weight in the torso rather than the arms. Ex-military bearing he has not quite stopped performing. Subdermal armour patches faintly visible as ridges at the shoulders. A face that has stopped being expressive in professional situations.',
    'stats':[('STR','16'),('CON','15'),('SIZ','15'),('INT','11'),('POW','11'),('DEX','13'),('APP','10')],
    'derived':[('HP','16'),('PP','11'),('DB','+1D4'),('SR','28'),('Move','10')],
    'skills':[
      ('Firearms (Pistol)','65%'),('Firearms (Rifle)','60%'),('Brawl','60%'),('Athletics','55%'),
      ('Dodge','50%'),('Intimidate','50%'),('Drive','50%'),('Spot Hidden','45%'),
      ('Melee','55%'),('Throw','45%'),('Climb','40%'),('Security Systems','35%'),
      ('First Aid','35%'),('Track','30%'),('Perception','40%'),('Stealth','20%'),
      ('Streetwise','35%'),('Firearms (Auto)','50%'),
    ],
    'equipment':[
      'Military-grade sidearm (2D6+2) — standard corporate security pattern',
      'Collapsible combat baton (1D8+DB) — telescopic, clips to belt',
      'Tactical rig — four magazine pouches, medkit slot, comms bracket',
      'Night-vision monocle — four-hour battery, right eye mount',
      'Trauma pad set (3 uses, stops bleeding, +1D6 to natural healing)',
      'Six-day field ration pack in chest pocket',
    ],
    'sp_name':'"Subdermal Combat Plates"',
    'sp_type':'Combat augmentation — shoulder and upper torso subdermal armour installation + reflex tap',
    'sp_stats':'Manufacturer: Meridian Security Group (standard issue) / Grade: Military / Age: 4 years',
    'sp_abilities':[
      ('+2 armour (passive)','Subdermal plates cover shoulders and upper torso. 2 points of armour that cannot be removed, soaked through, or targeted directly.'),
      ('Reflex tap (+1 DEX on combat SR)','Neural reflex tap at the spine — adds 1 to DEX for Strike Rank in combat only. Does not apply to non-combat DEX rolls.'),
      ('Adrenaline dump (1/combat)','On being hit for 3+ HP: may immediately make one free attack at +10% before the end of the round. Involuntary.'),
      ('Cost','The plates occasionally cause muscle spasm — a random sharp contraction in the shoulders or neck, lasting 1-2 seconds. At 1/session it is manageable. Since the tunnels job three months ago it has been daily. Viktor has not sought medical advice.'),
    ],
    'sp_note':'Standard Meridian Security Group issue from his four years in Sub-Districts 1-4. He kept them when he quit. Meridian\'s contract stipulates decommissioning on departure. He did not return them. Meridian\'s records show them as decommissioned. This is not the same thing.',
    'background':'Ex-Meridian Security Group. Sub-Districts 1-4 patrol, four years. Quit eighteen months ago — around the same time the Sub-District 7 disappearances started. Nobody made that connection. He has been quietly making it for eighteen months. He left because the things they were told not to investigate were starting to pile up and the list was starting to look like a pattern. He was right about that.',
    'hook':'Quit Meridian Security Group eighteen months ago. The Sub-District 7 disappearances started around the same time. He has been piecing this together for a year and a half. He has not said this to anyone. He is going to have to say it tonight.',
    'quote':'"I\'ve seen what corporate security does when it doesn\'t want something found. I\'ve been that. This is different."',
  },
  { 'name':'Tal Morgan', 'archetype':'The Tech', 'meta':'Neo-Ashford Freelance',
    'allegiance':'Neo-Ashford Operative',
    'physical':'Mid-twenties. Something slightly caffeinated about the eyes. Wears too many pockets and all of them have something in. A thin neural interface scar behind the right ear — clean, professional. Fingers that move independently when thinking.',
    'stats':[('STR','11'),('CON','12'),('SIZ','11'),('INT','16'),('POW','12'),('DEX','14'),('APP','12')],
    'derived':[('HP','12'),('PP','12'),('DB','None'),('SR','25'),('Move','10')],
    'skills':[
      ('Electronics','70%'),('Repair (Electronics)','65%'),('Computer Use','60%'),('Drone Operation','60%'),
      ('Spot Hidden','50%'),('Security Systems','55%'),('Science (Computing)','50%'),('Research','50%'),
      ('Electronics (Comms)','55%'),('Stealth','35%'),('Dodge','35%'),('Drive','40%'),
      ('First Aid','30%'),('Perception','45%'),('Firearms (Pistol)','30%'),('Bargain','35%'),
      ('Lockpick','40%'),('Surveillance','45%'),
    ],
    'equipment':[
      'Portable drone — palm-sized, near-silent, 20-min battery, live video feed to wrist display',
      'Hacking suite (wrist-mounted) — 1D6 minutes per encryption layer, physical interface required',
      'EMP pulse device — one use, 10m radius, disables all electronic devices including augments',
      'Tool roll — fourteen pieces, corporate and black-market standard',
      'Wrist display — drone feed, maps, comms, bio-scanner readout',
      'Six spare power cells — drone and ECM compatible',
    ],
    'sp_name':'"Neural I/O Bridge"',
    'sp_type':'Direct machine interface augment — behind-ear subdermal installation',
    'sp_stats':'Manufacturer: Custom build (self-installed over 18 months) / Grade: Prototype / Age: 11 months',
    'sp_abilities':[
      ('Direct interface','Can interface directly with any electronic system at physical touch range, bypassing input hardware. Electronics rolls at +15% when using direct interface.'),
      ('Drone sync','The drone feeds directly to visual cortex when the bridge is active. Tal can see through the drone without looking at the wrist display. Disorienting — -10% to Spot Hidden in immediate vicinity while drone-synced.'),
      ('Passive network sense','Within 20m: passively detects active wireless transmissions and their approximate direction. No roll required. Does not decrypt.'),
      ('Cost','Self-installed. The installation is clean. The neural integration is not fully stable — once per session (GM calls when), Tal gets a 2-3 second feedback spike: sharp sensory white noise. Cannot take any action during. Has never told anyone it was self-installed.'),
    ],
    'sp_note':'Tal built this over eighteen months and installed it over a weekend with a medical kit, a bathroom mirror, and three tutorials from a forum that has since been taken down. The installation is technically competent. The integration is 73% stable by Tal\'s own assessment. The remaining 27% is a problem for later.',
    'background':'Freelance tech contractor, specialising in corporate infrastructure and security system bypass. Never full-time employment — too many questions asked about methods. The drone is a custom build from salvage. The hacking suite is third-generation corporate black market. The EMP is one of two built from surplus components last month. The other one is in a drawer at home. Tal is the one who got the note from the child on The Slab. The paper has a faint chemical smell that will mean something later.',
    'hook':'[PRIVATE] The child on The Slab approaches Tal specifically and presses a folded note into their hand. Don\'t go to the plant. My dad went. He didn\'t come back the same. The handwriting is a child\'s. The paper smells faintly of something chemical. That smell will return.',
    'quote':'"I have eyes everywhere. The problem is what the eyes are seeing."',
  },
  { 'name':'Reina Vasquez', 'archetype':'The Medic', 'meta':'Neo-Ashford Contract Medic',
    'allegiance':'Neo-Ashford Operative',
    'physical':'Early thirties. The calm of someone who learned to stay calm because the alternative was worse. Medical kit worn on the hip like it is always there. A small scar at the left wrist — blood draw needle, years of practice. Watches people\'s breathing before she watches their eyes.',
    'stats':[('STR','11'),('CON','13'),('SIZ','12'),('INT','15'),('POW','14'),('DEX','13'),('APP','13')],
    'derived':[('HP','13'),('PP','14'),('DB','None'),('SR','25'),('Move','10')],
    'skills':[
      ('Medicine','65%'),('First Aid','70%'),('Science (Biology)','50%'),('Perception','50%'),
      ('Persuade','45%'),('Psychology','55%'),('Spot Hidden','45%'),('Dodge','40%'),
      ('Drive','40%'),('Research','45%'),('Science (Chemistry)','40%'),('Stealth','30%'),
      ('Computer Use','35%'),('Bargain','40%'),('Brawl','30%'),('Insight','50%'),
      ('Science (Pharmacology)','45%'),('Firearms (Pistol)','30%'),
    ],
    'equipment':[
      'Full trauma kit — arterial clamp, wound seal, bone stabiliser, pain management',
      'Stimulants (3 doses) — +10% physical skills for 1D4 hours, then -15% crash for equal time',
      'Bio-scanner (wrist strap) — detects organic material and life signs within 5m',
      'Sedative injectors (2 doses) — CON resistance or unconscious 1D4 hours',
      'Antibiotics and infection protocols — relevant to tonight in ways not yet clear',
      'Personal encrypted data-pad — medical notes, contacts, three years of observations',
    ],
    'sp_name':'"Biometric Diagnostics Array"',
    'sp_type':'Medical diagnostic augment — palm and fingertip subdermal sensor installation',
    'sp_stats':'Manufacturer: Meridian Medical Division (licensed) / Grade: Commercial / Age: 2 years',
    'sp_abilities':[
      ('Tactile diagnosis','Touch a person\'s skin: receives temperature, pulse, blood pressure, and basic metabolic readout as a display in peripheral vision. Medicine rolls at +20% when treating someone she has touched.'),
      ('Toxin detection','Can identify the presence and approximate class of any toxin or pathogen in contact range. Does not identify the specific compound without a separate Research or Science roll.'),
      ('Bio-scanner sync','The wrist-strap bio-scanner syncs to the array — range extends to 8m and includes structural anomaly detection. Near the entity: the readout will behave strangely. The GM should tell Reina first.'),
      ('Cost','The array reads everything. A person who is lying shows different biometrics than a person who is telling the truth. Reina has learned to stop looking when she doesn\'t want to know. She does not always succeed.'),
    ],
    'sp_note':'The array was licensed through a Meridian Medical subsidiary two years ago. It was marketed as a diagnostic aid. What the fine print includes — Meridian Medical retaining access to anonymised diagnostic data from all licensed arrays — is technically disclosed in clause 14(f) of the user agreement. Reina did not read clause 14(f).',
    'background':'Contract medic for mid-level corporate field teams. Three years of jobs that paid above standard and required discretion. A colleague at a Meridian-contracted morgue once described unusual organic tissue found in the thoracic cavities of recovered bodies. The colleague has since been reassigned. Reina never forgot the phrase: the tissue appeared to be growing inward. We did not determine the entry point. Tonight she is going to determine the entry point.',
    'hook':'A colleague at a Meridian-contracted morgue once described unusual organic tissue found in thoracic cavities. The tissue appeared to be growing inward. We did not determine the entry point. The colleague has since been reassigned. Reina never forgot those words. Tonight she will find out what they mean.',
    'quote':'"I can keep everyone alive for the next four hours. After that I need to know what we\'re dealing with."',
  },
  { 'name':'Petra Amis', 'archetype':'The Analyst', 'meta':'Independent Research Contractor',
    'allegiance':'Neo-Ashford Operative',
    'physical':'Mid-thirties. The kind of tidiness that is defensive rather than aesthetic. Physical notepad in a jacket pocket — unusual, conspicuous, deliberate. Doesn\'t carry corporate-grade equipment because corporate-grade equipment has logs. Watches exits before she watches people.',
    'stats':[('STR','10'),('CON','11'),('SIZ','11'),('INT','17'),('POW','13'),('DEX','11'),('APP','12')],
    'derived':[('HP','11'),('PP','13'),('DB','None'),('SR','22'),('Move','10')],
    'skills':[
      ('Research','70%'),('Library Use','65%'),('Science (Data Analysis)','60%'),('Insight','60%'),
      ('Spot Hidden','50%'),('Computer Use','50%'),('Persuade','45%'),('Psychology','50%'),
      ('Drive','35%'),('Electronics','40%'),('Science (Various)','55%'),('Write','55%'),
      ('Law','40%'),('Dodge','30%'),('Stealth','30%'),('Perception','55%'),
      ('Bargain','35%'),('Cryptography','45%'),
    ],
    'equipment':[
      'Encrypted personal terminal — Veltris public filings accessible, all local data air-gapped',
      'Signal scanner — detects active transmissions, logs frequency and source patterns',
      'Physical notepad and pen — old habit, or paranoia about digital records (both)',
      'Four USB-equivalent data sticks — different encryption standards, one already loaded',
      'Cash: 800 credits in physical cards, untraceable',
      'The anonymous message — printed, folded, in the left inside pocket',
    ],
    'sp_name':'"Encrypted Cortex Store"',
    'sp_type':'Memory and data augment — temple subdermal installation',
    'sp_stats':'Manufacturer: Unknown (received as part of a contract payment, 2 years ago) / Grade: Unknown',
    'sp_abilities':[
      ('Eidetic recall','Any text, image, or data Petra has directly observed can be recalled with complete accuracy. Research rolls at +20% when working from recalled material.'),
      ('Encrypted memory partition','A section of the cortex store is locked with a 12-character passphrase only Petra knows. Can hold approximately 40 hours of high-fidelity sensory data. Whatever is in there was put there deliberately.'),
      ('Passive indexing','Petra unconsciously cross-references new information against everything she has ever observed. Once per session: the GM may tell Petra one thing the rest of the table has missed.'),
      ('Cost','The manufacturer is unknown. The augment was provided as "payment in kind" for a contract two years ago. It functions correctly. Petra has spent eighteen months trying to determine who made it. She has not found out. The encrypted partition contains something she put there eighteen months ago and has not accessed since.'),
    ],
    'sp_note':'Petra does not know who manufactured this augment. She has tried to find out and failed. The encrypted partition contains data she cannot currently bring herself to open. The passphrase is the name of the client who paid her with this augment instead of credits. She has never told anyone that client\'s name.',
    'background':'Independent research contractor — corporate intelligence, pattern analysis, data archaeology. Two days before this job, received an anonymous encrypted message. Breaking it took 40 minutes. Inside: coordinates in Sub-District 9 and three words. Don\'t go back. She has never been to Sub-District 9. She does not know what "back" means. She has been trying to find out for two days. Tonight she will.',
    'hook':'[PRIVATE] Two days ago, received an anonymous encrypted message. Breaking it took 40 minutes. Coordinates in Sub-District 9 and three words: Don\'t go back. She has never been to Sub-District 9. She does not know what "back" means. Tonight she will find out.',
    'quote':'"Two days ago someone sent me coordinates and three words. I\'m here to understand what the third word means."',
  },
]

D1_CHARS = [
  { 'name':'Kira Osei-Mensah', 'archetype':'NHS Junior Doctor (off duty)', 'meta':'South Bank, 10:47 AM',
    'allegiance':'Who to reach: Abena (mother, 74, Peckham)',
    'physical':'Late twenties. Awake for 22 hours — the particular brightness of adrenaline overriding exhaustion. Hospital lanyard removed but ID badge still clipped to her jacket. Moves between people the way someone does who has been trained to assess urgency fast.',
    'stats':[('STR','9'),('CON','12'),('SIZ','10'),('INT','16'),('POW','14'),('DEX','13'),('APP','14')],
    'derived':[('HP','11'),('MP','14'),('DB','None'),('SR','23'),('Move','10')],
    'skills':[
      ('First Aid','75%'),('Medicine','55%'),('Science (Biology)','50%'),('Persuade','55%'),
      ('Insight','55%'),('Psychology','60%'),('Spot Hidden','50%'),('Dodge','40%'),
      ('Research','50%'),('Drive','35%'),('Computer Use','35%'),('Bargain','30%'),
      ('Brawl','25%'),('Climb','30%'),('Language (Twi)','50%'),('Status','40%'),
      ('Perception','50%'),('Track','20%'),
    ],
    'equipment':[
      'Phone — 73% battery at alert. NHS group chats already flooding',
      'A small crossbody bag: travel card, purse (£60 cash + bank card), lip balm',
      'Earbuds (one in, one loose) — call to her mum already attempted. Ringing out.',
      'A nearly finished flat white — still warm when the alert fires',
      'Hospital ID badge (still clipped to jacket) — will open certain NHS facility doors',
      'A BNF pocket edition (British National Formulary) in the bag — always there',
    ],
    'sp_name':'What You Know That Others Don\'t',
    'sp_type':'22 hours post-night-shift. Three NHS group messages unopened before the alert.',
    'sp_stats':'Medical training  ·  Current status: Off duty  ·  First responder: yes',
    'sp_abilities':[
      ('Triage priority','Once per scene: can assess all wounded in view and rank by survivability in one round, no roll required. Tells the group who to help first.'),
      ('Improvised medical','Can use non-medical materials for medical purposes at -20% penalty. First Aid 75% becomes 55% with household supplies, bar stock, etc.'),
      ('Infection assessment','Can assess a bitten person\'s likely timeline with Medicine 50% roll. The answer will not be comforting.'),
      ('Running on fumes','Awake 22 hours: -10% to all non-medical rolls after Act Two begins. Kira\'s medical skills are unaffected — training is deeper than fatigue.'),
    ],
    'sp_note':'Kira\'s mother is 74, lives alone in Peckham, and is not picking up. Peckham is south and east of the current position. The infection spread from Elephant & Castle. Peckham is between the group and the river. Kira knows this geography. She knows what it means. She has not said it yet.',
    'background':'Junior doctor, six months post-qualification. A&E rotation. She has seen mass casualty events in training but never in practice. She is running on post-night-shift adrenaline and the particular clarity that comes from exhaustion so deep it loops back around. She is the group\'s best medical resource. She is also 22 hours without sleep and trying to reach a 74-year-old woman who is not picking up her phone.',
    'hook':'Her mother Abena, 74, lives alone in Peckham. Peckham is south and east. The outbreak started at Elephant & Castle. Kira knows what that geography means. She has not said it aloud yet.',
    'quote':'"Tell me what you\'re feeling. Specifically. Not fine — specifically."',
  },
  { 'name':'Dev Krishnamurthy', 'archetype':'Freelance software engineer', 'meta':'Borough Market café, 10:47 AM',
    'allegiance':'Who to reach: flatmate near Old Street',
    'physical':'Late twenties. Headphones half-on the way people wear them when they want to be left alone but also available. Laptop bag, good quality, worn strap. The slightly unfocused expression of someone who has been in their own head all morning and is now very much not.',
    'stats':[('STR','10'),('CON','11'),('SIZ','11'),('INT','17'),('POW','12'),('DEX','13'),('APP','12')],
    'derived':[('HP','11'),('MP','12'),('DB','None'),('SR','24'),('Move','10')],
    'skills':[
      ('Computer Use','75%'),('Electronics','65%'),('Library Use','60%'),('Research','55%'),
      ('Science (Mathematics)','45%'),('Science (Computing)','70%'),('Spot Hidden','45%'),
      ('Insight','40%'),('Dodge','35%'),('Drive','40%'),('Bargain','30%'),
      ('Persuade','35%'),('Brawl','25%'),('Climb','30%'),('Stealth','30%'),
      ('Perception','45%'),('Track','20%'),('Psychology','30%'),
    ],
    'equipment':[
      'MacBook Pro — 81% battery, already tracking spread on four social media threads',
      'Phone — 94% battery, emergency services scanner app notifications since 9:40 AM',
      'Laptop bag: charger (useful), USB hub, notebook (unused), protein bar',
      'AirPods and case — full charge',
      'Wallet: £45 cash, three cards, Oyster with £8.40',
      'A voice note from his flatmate about spare keys — unanswered, one hour old',
    ],
    'sp_name':'What You Know That Others Don\'t',
    'sp_type':'Has been tracking the spread since before the alert. Scanner app flagged first reports at 9:40 AM.',
    'sp_stats':'Software engineer  ·  Current status: Remote working  ·  Info advantage: significant',
    'sp_abilities':[
      ('Early data','Has been tracking social media spread since 9:40 AM — 67 minutes before the alert. Knows the Elephant & Castle origin point. Knows three smoke plume locations. Has approximate spread rate. The group should ask him what he knows.'),
      ('Network access','As long as any signal exists: can access and aggregate public information, CCTV feeds (those that are publicly accessible), transport data, and social media. Computer Use 75%.'),
      ('Signal mapping','Can map cell tower activity to identify where people are gathering (and where they are not). 20-minute task with a laptop and signal.'),
      ('Cost — what he hasn\'t said','He has been sitting on the scanner app data for over an hour. He did not call anyone. Did not post. He\'s been watching. The group may wonder why.'),
    ],
    'sp_note':'Dev has known something was wrong since 9:40 AM. He watched it develop in real time. He did not call anyone. He filed it as "monitoring." He is a very good analyst and a very isolated person. Tonight is going to test both.',
    'background':'Freelance software engineer, primarily security and infrastructure clients. Works from coffee shops because home is a flat share with a flatmate he gets on fine with and that is the limit of his social infrastructure in London. Has been in the city four years. Knows it through data rather than geography. Tonight data is going to have to become geography.',
    'hook':'He has been tracking the spread on his scanner app since 9:40 AM — an hour before the alert. He has more information than anyone. He has not told anyone. The group will need to ask him directly.',
    'quote':'"I\'ve been watching this develop for an hour. I should have said something earlier. I know."',
  },
  { 'name':'Maggie Donnelly', 'archetype':'Retired Metropolitan Police (22 years)', 'meta':'Jubilee Walkway, 10:47 AM',
    'allegiance':'Who to reach: Cara (daughter, Deptford)',
    'physical':'Early sixties. Sunday morning walking gear — practical coat, good shoes, a pace that covers ground without appearing to hurry. The assessment in her eyes is continuous and automatic. She retired six years ago and has not yet stopped doing the job.',
    'stats':[('STR','12'),('CON','13'),('SIZ','12'),('INT','15'),('POW','14'),('DEX','11'),('APP','12')],
    'derived':[('HP','13'),('MP','14'),('DB','None'),('SR','23'),('Move','10')],
    'skills':[
      ('Persuade','70%'),('Psychology','65%'),('Spot Hidden','65%'),('Insight','70%'),
      ('Law','60%'),('Brawl','55%'),('First Aid','50%'),('Dodge','55%'),
      ('Drive','60%'),('Intimidate','60%'),('Firearms (Pistol)','45%'),('Track','45%'),
      ('Athletics','45%'),('Search','55%'),('Streetwise','50%'),('Stealth','35%'),
      ('Perception','65%'),('Climb','40%'),
    ],
    'equipment':[
      'Phone — 62% battery. Already trying to reach Cara. Voicemail.',
      'Walking gear: practical coat with good pockets, water bottle, small first aid kit (always)',
      'Police warrant card (expired 6 years, but laminated) — she does not know if it will still work',
      'Wallet: £120 cash (always carries cash), Oyster, two cards',
      'A pocket notepad and two pens — old habit',
      'A flapjack, half-eaten, in her right pocket',
    ],
    'sp_name':'What You Know That Others Don\'t',
    'sp_type':'First on scene at Tavistock Square, 2005. Twenty-two years Metropolitan Police. Pattern recognition.',
    'sp_stats':'Retired DCI  ·  Current status: Civilian  ·  Crowd management: expert',
    'sp_abilities':[
      ('Scene assessment','Can assess any crowd, group, or space for immediate threat level, routes, and key individuals in one round without a roll. Tells the group who is dangerous, who is useful, where the exits are.'),
      ('Authority','When Maggie speaks with police authority (even retired), civilians respond. Persuade at +20% in any crowd management or evacuation scenario.'),
      ('Tavistock memory','Has been first on scene at a mass casualty event. Knows what that does to people, including herself. -10% to SAN losses from human casualties (not zombies). This is experience, not callousness.'),
      ('The warrant card','It expired six years ago. She keeps it laminated. Once per session: show it to a civilian or official with complete confidence. 60% chance they don\'t check the date.'),
    ],
    'sp_note':'Maggie\'s daughter Cara lives in Deptford. Deptford is south-east. The infection is moving east from Elephant & Castle. Maggie has not said this calculation aloud. She has made it. She will keep making it. Her ability to do her job and her need to get to her daughter are going to come apart from each other before Act Three.',
    'background':'Twenty-two years in the Metropolitan Police, retired at DCI level. Knows the South Bank better than she knows her own flat. Was first on scene at Tavistock Square in 2005. Has handled riots, the 2011 disorder, a gas explosion in 2019. None of those prepared her for a person standing waist-deep in the Thames, head tilted, facing the wrong direction, in no apparent distress. That specific wrongness is new.',
    'hook':'Her daughter Cara is in Deptford. The infection started at Elephant & Castle and is moving east. Maggie has made this calculation. She will not stop until she has also got these people out. The tension between those two things is the engine of her character.',
    'quote':'"Move. I\'ll explain why while we\'re moving."',
  },
  { 'name':'Olu Adeyemi', 'archetype':'Security guard, The Shard', 'meta':'The Shard lobby, 10:47 AM',
    'allegiance':'Who to reach: No immediate family in London — the group becomes his motivation',
    'physical':'Early thirties. Large, unhurried, the particular calm of someone who handles other people\'s panic for a living. Security uniform. A radio on his belt that was already not working properly when his supervisor handed it to him. His coffee — from home, better than the building\'s — is on the security desk.',
    'stats':[('STR','15'),('CON','14'),('SIZ','14'),('INT','13'),('POW','13'),('DEX','12'),('APP','13')],
    'derived':[('HP','15'),('MP','13'),('DB','+1D4'),('SR','26'),('Move','10')],
    'skills':[
      ('Brawl','65%'),('Spot Hidden','60%'),('Security Systems','60%'),('Athletics','60%'),
      ('Persuade','45%'),('Drive','55%'),('Intimidate','55%'),('Dodge','55%'),
      ('First Aid','40%'),('Climb','55%'),('Electronics','40%'),('Perception','65%'),
      ('Stealth','40%'),('Track','35%'),('Firearms (Pistol)','40%'),('Melee','50%'),
      ('Search','50%'),('Streetwise','45%'),
    ],
    'equipment':[
      'Security radio — intermittently functional. Fragments only. Keeps cutting out.',
      'Shard security keycard — access to all staff areas, service levels, roof',
      'Security baton (1D6) — standard issue',
      'Personal phone — 91% battery. He called his mum this morning. She picked up.',
      'Shard master key ring — seventeen keys, most useful, two unknown',
      'His coffee, from home, in an insulated mug. Probably cold by now.',
    ],
    'sp_name':'What You Know That Others Don\'t',
    'sp_type':'The Shard: radio, CCTV, roof access, staff corridors, defensible position.',
    'sp_stats':'Security grade: SIA licensed  ·  Building access: full  ·  Radio: intermittent',
    'sp_abilities':[
      ('Building access','Has keycard and key access to all Shard staff and service areas. From upper floors: can see south and east across London. What he can see includes three smoke plumes, all south of where they expected.'),
      ('Radio fragments','The security radio is broken but picks up fragmented police transmissions. Olu hears more than he understands. Key fragment: Elephant & Castle first reports at 7:14 AM — nearly two hours before the alert. He will need the group to help him interpret it.'),
      ('CCTV','The Shard\'s ground floor CCTV covers a 200m radius. Computer Use or Electronics 40%: can access the feed on the security desk terminal. What it shows is already worse than the street sounds suggest.'),
      ('The group becomes the motivation','Olu has no immediate family in London. His motivation shifts as the session progresses. By Act Two, the group is why he is doing this. The player should feel this happen, not be told it.'),
    ],
    'sp_note':'The radio fragment about the cordon — "north of the river" — is going to land hardest on Olu. He is the one holding the radio when it comes through. He has been trying to do his job all day. He has trusted the institution. Give him the moment when he doesn\'t say anything. Then let the players deal with what they\'ve seen on his face.',
    'background':'Security guard at The Shard, two years. Moved to London from Birmingham three years ago. No immediate family here — his family is in Birmingham and Lagos. His mum picked up this morning; that fact will anchor him throughout the night. Has handled everything the Shard security role requires: aggressive visitors, medical emergencies, one bomb scare in 2024 that was a forgotten bag. Has never handled something where the emergency services are the ones providing fragments instead of answers.',
    'hook':'He is the only character who starts with a functioning radio and a defensible high-ground position. What he does with that advantage in the first ten minutes shapes the rest of the session. The radio fragment about the cordon is his to deliver. Give him the moment.',
    'quote':'"I have keys to everything in this building and I can see for three miles from the roof. Let\'s use that before we lose it."',
  },
  { 'name':'Priya Mehta', 'archetype':'Science journalist', 'meta':'Southbank Centre, 10:47 AM',
    'allegiance':'Who to reach: editor (has documents re: Meridian Biosciences)',
    'physical':'Early thirties. Press lanyard visible — she hasn\'t taken it off yet, force of habit. A notebook in her hand before she consciously decided to take it out. The particular tension of someone whose instinct is to find the story and whose training is telling them to find it very carefully.',
    'stats':[('STR','9'),('CON','11'),('SIZ','10'),('INT','17'),('POW','13'),('DEX','12'),('APP','14')],
    'derived':[('HP','11'),('MP','13'),('DB','None'),('SR','22'),('Move','10')],
    'skills':[
      ('Library Use','70%'),('Research','70%'),('Insight','65%'),('Write','65%'),
      ('Persuade','60%'),('Psychology','55%'),('Science (Biology)','55%'),('Spot Hidden','50%'),
      ('Computer Use','50%'),('Science (Chemistry)','50%'),('Drive','35%'),('Dodge','30%'),
      ('Law','30%'),('Climb','30%'),('Stealth','30%'),('Perception','55%'),
      ('Language (Hindi)','60%'),('Bargain','45%'),
    ],
    'equipment':[
      'Phone — 88% battery. Editor\'s message: "Something came in. Might be relevant. Can we talk Monday?"',
      'Notebook (half-full already) and three pens — she will fill the rest of it tonight',
      'Press lanyard — Southbank Centre media pass',
      'Laptop in shoulder bag — research on the exhibition piece, and other things',
      'Voice recorder (battery full) — habit',
      'Wallet: £35 cash, press card, two other cards',
    ],
    'sp_name':'What You Know That Others Don\'t',
    'sp_type':'Editor has documents relating to Meridian Biosciences. She has been choosing not to use her instincts.',
    'sp_stats':'Science journalist  ·  Publications: Nature, New Scientist  ·  Meridian connection: unconfirmed',
    'sp_abilities':[
      ('Meridian thread','Her editor has documents about Meridian Biosciences. The message came last night. She chose to think about it later. Research 70% or Psychology 55%: can begin piecing together the Meridian-to-outbreak connection from public information, with the editor\'s message as a starting point.'),
      ('Source assessment','Can evaluate the credibility of any information source or account with Insight 65%. Critical in a world where everyone is speculating and nobody has the full picture.'),
      ('The story vs the group','Priya is the character best positioned to understand the truth. Whether she uses that ability to help the group or to document the story is a genuine player choice. Neither answer is wrong.'),
      ('Press access','The press lanyard is real and currently valid. In the first two hours of an emergency, officials sometimes still respond to press credentials. Once per session.'),
    ],
    'sp_note':'Priya\'s editor has the Meridian Biosciences documents. They arrived 48 hours before the outbreak. The editor didn\'t run the story — legal wouldn\'t clear it in time, or maybe someone made sure it wasn\'t run. Priya has the editor\'s number and the editor is north of the river. Whether she can reach him, and what he tells her, is the scenario\'s deepest thread.',
    'background':'Science journalist, primarily biology and public health. Has covered three NHS crises, a pharmaceutical fraud case, and last year\'s antibiotic resistance WHO report. Good instincts, disciplined verification practice, and the journalist\'s particular capacity to document things clearly while they are happening to her personally. Her editor\'s message is about Meridian Biosciences. She has a very good instinct about what it means. She has been choosing not to use it. Tonight she won\'t have that option.',
    'hook':'Her editor has documents about Meridian Biosciences that arrived 48 hours before the outbreak. The message came last night. She filed it for Monday. Tonight, everything she has been choosing not to know is going to become necessary.',
    'quote':'"I need to understand what this is before I can help anyone survive it."',
  },
  { 'name':'Tom Becker', 'archetype':'Scaffolding worker', 'meta':'Waterloo Road side street, 10:47 AM',
    'allegiance':'Who to reach: his van (practical exit) and his mum (no answer, voicemail)',
    'physical':'Late twenties. Work clothes, high-vis jacket still on. The van keys in his right hand. A bag of tools over one shoulder. The unaffected physicality of someone who climbs things and lifts things for a living and has never thought of this as unusual.',
    'stats':[('STR','14'),('CON','14'),('SIZ','13'),('INT','12'),('POW','11'),('DEX','13'),('APP','11')],
    'derived':[('HP','14'),('MP','11'),('DB','+1D4'),('SR','26'),('Move','10')],
    'skills':[
      ('Craft (Construction)','70%'),('Athletics','65%'),('Climb','70%'),('Mechanics','60%'),
      ('Drive','65%'),('Brawl','55%'),('Spot Hidden','50%'),('Throw','55%'),
      ('Melee','50%'),('Dodge','50%'),('Perception','55%'),('Search','50%'),
      ('Streetwise','45%'),('Intimidate','40%'),('First Aid','35%'),('Track','40%'),
      ('Electronics (Basic)','25%'),('Security Systems','25%'),
    ],
    'equipment':[
      'Tool bag: hammer (1D6+DB), bolt cutters, crowbar (1D8+DB), screwdrivers, zip ties',
      'High-vis jacket — visibility is a mixed blessing tonight',
      'Phone — 44% battery. One voicemail left for his mum. She didn\'t answer.',
      'Van keys (parked near Lambeth North — across the river, or the long way round)',
      'Work gloves — thick leather, -10% fine motor but effectively 1-point hand armour',
      'Half a bottle of water and an energy bar from this morning',
    ],
    'sp_name':'What You Know That Others Don\'t',
    'sp_type':'Can build, break into, reinforce, or assess structural stability of anything. Has a van.',
    'sp_stats':'Scaffolding: 8 years  ·  Structural assessment: expert  ·  Van location: across the river',
    'sp_abilities':[
      ('Structural instinct','Can assess any building, structure, or barricade for load-bearing capacity, weak points, and improvised fortification potential without a roll. Tells the group what will hold and what won\'t.'),
      ('Break and build','Craft (Construction) 70% for any task involving temporary barriers, improvised tools, access to locked spaces via force, or rigging climbing points. The tool bag gives a further +10%.'),
      ('The van','Tom\'s van is near Lambeth North, north bank or the long way round. It has tools, jump leads, rope, a full tank of diesel, and a radio. Whether reaching it is worth the detour is a genuine strategic question that the group will have to decide. Tom knows where it is at all times.'),
      ('His mum','Tom\'s mother is in Catford, south-east London. He left a voicemail this morning. She didn\'t answer. He has been half-listening for a callback since. She has not called back. Tom is not the kind of person who talks about this.'),
    ],
    'sp_note':'Tom\'s van is the most practical resource in the scenario. It is also across the river, or the long way round, and reaching it costs time and exposure. The decision about whether to go for it — and whether Tom\'s motivation to reach it is the van or the fact that it represents a way to reach his mother — is a genuine player-character choice.',
    'background':'Scaffolding worker, eight years. South London born and raised. Knows the physical geography — where you can climb, what you can break through, which buildings are structurally sound and which aren\'t. Called his mum this morning. She didn\'t pick up. Left a voicemail that was mostly road noise. She still hasn\'t called back. He is carrying this alongside everything else and not saying anything about it because that is how he is.',
    'hook':'His mum is in Catford. She didn\'t answer this morning. He left a voicemail. She still hasn\'t called back. He is not going to say this unless directly asked. If directly asked, he will say it plainly and then change the subject.',
    'quote':'"Tell me what needs breaking or what needs holding. I can do both."',
  },
]

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def build_pdf(path, CHARS, T, cover_title, cover_sub, cover_byline, rules):
    S = make_styles(T)
    UW  = PAGE_W - 2*MARGIN
    LW  = UW * 0.615
    SKH = (LW - 4*mm) / 2

    doc = BaseDocTemplate(path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN+4*mm, bottomMargin=MARGIN+8*mm)

    cover_frame   = Frame(0,0,PAGE_W,PAGE_H, id='cover')
    content_frame = Frame(MARGIN, MARGIN+8*mm, UW, PAGE_H-2*MARGIN-12*mm, id='content')
    doc.addPageTemplates([
        PageTemplate(id='cover',  frames=[cover_frame],   onPage=make_cover_bg(T)),
        PageTemplate(id='normal', frames=[content_frame], onPage=make_page_bg(T)),
    ])

    story = []

    # ── COVER ──────────────────────────────────────────────────────────────
    story.append(Spacer(1,72))
    story.append(Paragraph(cover_title, S['doc_title']))
    story.append(Spacer(1,6))
    story.append(Paragraph(cover_sub, S['doc_sub']))
    story.append(Spacer(1,4))
    story.append(Paragraph(cover_byline, S['doc_byline']))
    story.append(Spacer(1,14))
    story.append(OrnRule(UW,T))
    story.append(Spacer(1,10))

    # Roster table
    roster = [[
        Paragraph(f"<b>{c['name']}</b>",  S['cover_name']),
        Paragraph(c['archetype'],          S['toc_sub']),
        Paragraph(c.get('meta',''),        S['doc_byline']),
    ] for c in CHARS]
    rt = Table(roster, colWidths=[UW*0.38, UW*0.38, UW*0.24])
    rt.setStyle(TableStyle([
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[T.parchment, T.parchment_dark]),
        ('LINEBELOW',(0,0),(-1,-1),0.4,T.rule),
        ('LINEABOVE',(0,0),(-1,0),1.0,T.accent),
        ('LINEBELOW',(0,-1),(-1,-1),1.0,T.accent),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ]))
    story.append(rt)
    story.append(Spacer(1,14))
    story.append(OrnRule(UW,T))
    story.append(Spacer(1,10))

    story.append(Paragraph("QUICK REFERENCE", S['rules_head']))
    rlt = Table([[Paragraph(c,S['doc_byline']) for c in row] for row in rules],
                colWidths=[UW/3]*3)
    rlt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),T.parchment_dark),
        ('GRID',(0,0),(-1,-1),0.4,T.rule),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(rlt)
    story.append(Spacer(1,8))
    story.append(Paragraph("Hand sheets face-down. Let players choose by archetype description, not by stats.", S['cover_note']))

    story.append(NextPageTemplate('normal'))
    story.append(PageBreak())

    # ── CHARACTER PAGES ──────────────────────────────────────────────────────
    for char in CHARS:
        max_hp  = int(next(v for k,v in char['derived'] if k in ('HP',)))
        max_san = int(next((v for k,v in char['derived'] if k=='MP' or k=='PP'), 10))

        # ── FRONT PAGE ──────────────────────────────────────────────────────
        story.append(CharHeader(char['name'], char['archetype'],
                                char['meta'], char['allegiance'], UW, T))
        story.append(Spacer(1,3))

        # Skills table (full-width, no portrait column)
        sk = char['skills']
        if len(sk)%2: sk=sk+[('','')]
        mid=len(sk)//2
        sk_rows=[]
        for (la,lv),(ra,rv) in zip(sk[:mid],sk[mid:]):
            sk_rows.append([Paragraph(la,S['body_sm']),Paragraph(f"<b>{lv}</b>",S['body_sm']),
                            Paragraph(ra,S['body_sm']),Paragraph(f"<b>{rv}</b>",S['body_sm'])])
        skt=Table(sk_rows, colWidths=[SKH*0.72,SKH*0.28,SKH*0.72,SKH*0.28])
        skt.setStyle(TableStyle([
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[T.stat_row1,T.stat_row2]),
            ('LINEBELOW',(0,0),(-1,-1),0.3,T.rule),
            ('LINEAFTER',(1,0),(1,-1),0.6,T.rule),
            ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),3),
            ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),
            ('ALIGN',(1,0),(1,-1),'RIGHT'),('ALIGN',(3,0),(3,-1),'RIGHT'),
        ]))

        story.append(SectionBanner("Characteristics", UW, T))
        story.append(Spacer(1,2))
        story.append(StatBlock(char['stats'], char['derived'], UW, T))
        story.append(Spacer(1,4))
        story.append(SectionBanner("Skills", UW, T))
        story.append(Spacer(1,2))
        story.append(skt)
        story.append(Spacer(1,4))

        # Equipment
        story.append(SectionBanner("Equipment", UW, T))
        story.append(Spacer(1,2))
        eqt=Table([[Paragraph(f"\u2022 {item}",S['body_sm'])] for item in char['equipment']],
                  colWidths=[UW])
        eqt.setStyle(TableStyle([
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[T.stat_row1,T.stat_row2]),
            ('LINEBELOW',(0,0),(-1,-1),0.3,T.rule),
            ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),4),
            ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),
        ]))
        story.append(eqt)
        story.append(Spacer(1,4))

        # Special section (Augment / What You're Carrying)
        story.append(SectionBanner(T.special_section, UW, T, special=True))
        story.append(Spacer(1,2))
        dc=[Paragraph(char['sp_name'],S['sp_title']),
            Paragraph(char['sp_type'],S['sp_label']),
            Paragraph(char['sp_stats'],S['sp_body'])]
        for abn,abd in char['sp_abilities']:
            dc.append(Paragraph(f"<b>{abn}:</b>  {abd}",S['sp_body']))
        dc.append(Paragraph(f"<i>{char['sp_note']}</i>",S['sp_body']))
        di=Table([[el] for el in dc], colWidths=[UW-16])
        di.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),T.special_bg),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
        do=Table([[di]], colWidths=[UW])
        do.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),T.special_bg),
            ('BOX',(0,0),(0,0),1.2,T.special_border),
            ('LEFTPADDING',(0,0),(0,0),8),('RIGHTPADDING',(0,0),(0,0),8),
            ('TOPPADDING',(0,0),(0,0),4),('BOTTOMPADDING',(0,0),(0,0),4)]))
        story.append(do)
        story.append(Spacer(1,5))

        # HP + SAN tracks (side by side)
        hp_w = UW * 0.52
        san_w = UW * 0.46
        tracks=Table([[HPTrack(max_hp,hp_w,T), SanTrack(max_san,san_w,T)]],
                     colWidths=[hp_w, san_w])
        tracks.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
            ('LINEAFTER',(0,0),(0,-1),0.4,T.rule),
        ]))
        story.append(tracks)

        story.append(PageBreak())

        # ── BACK PAGE ────────────────────────────────────────────────────────
        story.append(BackHeader(char['name'], char['archetype'], UW, T))
        story.append(Spacer(1,6))
        story.append(Paragraph(f"<i>{char['physical']}</i>",S['italic_sm']))
        story.append(Spacer(1,8))

        story.append(SectionBanner("Background", UW, T))
        story.append(Spacer(1,5))
        story.append(Paragraph(char['background'], S['body']))
        story.append(Spacer(1,6))

        ht=Table([[Paragraph("PERSONAL HOOK:",S['hook_label']),
                   Paragraph(char['hook'],S['hook_body'])]],
                 colWidths=[26*mm, UW-26*mm])
        ht.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),T.hook_bg),
            ('BOX',(0,0),(-1,-1),0.8,T.hook_border),
            ('LINEBEFORE',(0,0),(0,-1),3,T.hook_bar),
            ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
            ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        story.append(ht)
        story.append(Spacer(1,8))

        story.append(OrnRule(UW,T))
        story.append(Paragraph(char['quote'],S['quote']))
        story.append(OrnRule(UW,T))
        story.append(Spacer(1,10))

        story.append(SectionBanner("Notes", UW, T))
        story.append(Spacer(1,6))
        story.append(NotesBlock(UW, T, lines=8))

        story.append(PageBreak())

    doc.build(story)
    print(f"Done: {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

NC = night_crawler_theme()
D1 = day_one_theme()

NC_RULES = [
    ['HP = (CON+SIZ)/2 round up', 'PP = POW', 'DB: STR+SIZ 17-24 = None'],
    ['SR = DEX + INT', 'Attack: D100 <= skill%', 'DB: 25-32 = +1D4 | 33-40 = +1D6'],
    ['SAN loss: roll success = less loss', 'Augments: see character sheet', 'Unconscious at 0 HP'],
]
D1_RULES = [
    ['HP = (CON+SIZ)/2 round up', 'MP = POW', 'DB: STR+SIZ 17-24 = None'],
    ['SR = DEX + INT', 'Attack: D100 <= skill%', 'DB: 25-32 = +1D4 | 33-40 = +1D6'],
    ['Infected bite: CON resist or symptomatic', 'SAN loss on zombie encounter', 'Unconscious at 0 HP'],
]

build_pdf(
    '/mnt/user-data/outputs/brp-night-crawler-characters.pdf',
    NC_CHARS, NC,
    "THE NIGHT CRAWLER",
    "Player Character Reference — Neo-Ashford, 2087",
    "Basic Role-Playing  \u00b7  Event 91  \u00b7  ChaosiumCon 2026",
    NC_RULES,
)

build_pdf(
    '/mnt/user-data/outputs/brp-day-one-characters.pdf',
    D1_CHARS, D1,
    "DAY ONE — London Falls",
    "Player Character Reference — South Bank, 17 May 2026",
    "Basic Role-Playing  \u00b7  Event 159  \u00b7  ChaosiumCon 2026",
    D1_RULES,
)
