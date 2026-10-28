from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph as RParagraph, Spacer, Table as RTable, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xml.sax.saxutils import escape
from pathlib import Path

src=Path(r'C:\Users\23716\Desktop\test\test111\面试复习讲义_生成器装饰器迭代器.docx'); out=Path(r'C:\Users\23716\Desktop\test\test111\面试复习讲义_生成器装饰器迭代器.pdf')
pdfmetrics.registerFont(TTFont('YaHei',r'C:\Windows\Fonts\msyh.ttc', subfontIndex=0))
ss=getSampleStyleSheet()
ss.add(ParagraphStyle(name='B',parent=ss['BodyText'],fontName='YaHei',fontSize=8.8,leading=11,spaceAfter=3))
ss.add(ParagraphStyle(name='T',parent=ss['Title'],fontName='YaHei',fontSize=17,leading=21,alignment=TA_CENTER,textColor=colors.black,spaceAfter=5))
ss.add(ParagraphStyle(name='H1',parent=ss['Heading1'],fontName='YaHei',fontSize=12,leading=15,spaceBefore=7,spaceAfter=3,textColor=colors.black,keepWithNext=True))
ss.add(ParagraphStyle(name='H2',parent=ss['Heading2'],fontName='YaHei',fontSize=9.8,leading=12,spaceBefore=5,spaceAfter=2,textColor=colors.black,keepWithNext=True))
ss.add(ParagraphStyle(name='C',parent=ss['Code'],fontName='Courier',fontSize=7.3,leading=8.7,leftIndent=8,spaceAfter=1))

def esc(s): return escape(s).replace('\\n','<br/>')
def rp(text,style='B'): return RParagraph(esc(text),ss[style])
def iter_blocks(parent):
    for child in parent.element.body.iterchildren():
        if child.tag.endswith('}p'): yield Paragraph(child,parent)
        elif child.tag.endswith('}tbl'): yield Table(child,parent)

docx=Document(str(src)); story=[]
for block in iter_blocks(docx):
    if isinstance(block,Paragraph):
        txt=block.text
        if not txt: continue
        sty=block.style.name
        if sty=='Title': story.append(rp(txt,'T'))
        elif sty=='Heading 1': story.append(rp(txt,'H1'))
        elif sty=='Heading 2': story.append(rp(txt,'H2'))
        elif sty=='Code': story.append(rp(txt,'C'))
        elif sty=='List Bullet': story.append(rp('• '+txt,'B'))
        else: story.append(rp(txt,'B'))
    else:
        rows=[]
        for row in block.rows:
            rows.append([RParagraph(esc(c.text),ss['B']) for c in row.cells])
        n=len(rows[0]); widths=[35*mm]*n
        if n==3: widths=[28*mm,83*mm,51*mm]
        if n==4: widths=[38*mm,28*mm,31*mm,55*mm]
        tab=RTable(rows,colWidths=widths,repeatRows=1,hAlign='CENTER')
        ts=[('GRID',(0,0),(-1,-1),0.35,colors.HexColor('#D9D9D9')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1F4E78')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]
        for i in range(1,len(rows)):
            if i%2==0: ts.append(('BACKGROUND',(0,i),(-1,i),colors.HexColor('#F3F6F9')))
        tab.setStyle(TableStyle(ts)); story += [Spacer(1,2),tab,Spacer(1,4)]

def footer(canvas,doc):
    canvas.saveState(); canvas.setFont('YaHei',7); canvas.setFillColor(colors.HexColor('#777777')); canvas.drawCentredString(A4[0]/2,10*mm,'生成器 装饰器 迭代器面试复习讲义    第 %d 页'%doc.page); canvas.restoreState()

d=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=14*mm,leftMargin=14*mm,topMargin=12*mm,bottomMargin=15*mm); d.build(story,onFirstPage=footer,onLaterPages=footer); print(out)
