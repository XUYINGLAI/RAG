from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
from pathlib import Path

out = Path(r'C:\Users\23716\Desktop\test\test111\面试复习讲义_生成器装饰器迭代器.docx')
doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.55); sec.bottom_margin = Inches(0.55)
sec.left_margin = Inches(0.62); sec.right_margin = Inches(0.62)
sec.header_distance = Inches(0.25); sec.footer_distance = Inches(0.25)

styles = doc.styles
styles['Normal'].font.name = 'Microsoft YaHei'; styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'),'Microsoft YaHei'); styles['Normal'].font.size=Pt(9.5)
styles['Normal'].paragraph_format.space_after=Pt(3); styles['Normal'].paragraph_format.line_spacing=1.05
for name,size in [('Title',19),('Heading 1',13),('Heading 2',10.5),('Heading 3',9.5)]:
    st=styles[name]; st.font.name='Microsoft YaHei'; st._element.rPr.rFonts.set(qn('w:eastAsia'),'Microsoft YaHei'); st.font.size=Pt(size); st.font.bold=True; st.font.color.rgb=RGBColor(0,0,0)
    st.paragraph_format.space_before=Pt(7 if name!='Title' else 0); st.paragraph_format.space_after=Pt(3)
# custom code style
if 'Code' not in styles:
    cs=styles.add_style('Code', WD_STYLE_TYPE.PARAGRAPH)
else: cs=styles['Code']
cs.font.name='Consolas'; cs._element.rPr.rFonts.set(qn('w:eastAsia'),'Consolas'); cs.font.size=Pt(8.3); cs.font.color.rgb=RGBColor(35,35,35)
cs.paragraph_format.left_indent=Inches(0.18); cs.paragraph_format.space_after=Pt(2); cs.paragraph_format.line_spacing=1.0

def shade(cell, fill):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),fill); tcPr.append(shd)
def borders(table, color='D9D9D9'):
    tblPr=table._tbl.tblPr; b=tblPr.first_child_found_in('w:tblBorders')
    if b is None: b=OxmlElement('w:tblBorders'); tblPr.append(b)
    for edge in ('top','left','bottom','right','insideH','insideV'):
        e=b.find(qn('w:'+edge))
        if e is None: e=OxmlElement('w:'+edge); b.append(e)
        e.set(qn('w:val'),'single'); e.set(qn('w:sz'),'4'); e.set(qn('w:space'),'0'); e.set(qn('w:color'),color)
def table(rows, widths=None, header=True):
    t=doc.add_table(rows=0, cols=len(rows[0])); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.autofit=False; borders(t)
    for ri,row in enumerate(rows):
        cells=t.add_row().cells
        for ci,val in enumerate(row):
            cells[ci].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if widths: cells[ci].width=Inches(widths[ci])
            p=cells[ci].paragraphs[0]; p.paragraph_format.space_after=Pt(0); p.paragraph_format.line_spacing=1.0
            run=p.add_run(str(val)); run.font.name='Microsoft YaHei'; run._element.rPr.rFonts.set(qn('w:eastAsia'),'Microsoft YaHei'); run.font.size=Pt(8.3)
            if ri==0 and header:
                shade(cells[ci],'1F4E78'); run.font.bold=True; run.font.color.rgb=RGBColor(255,255,255)
            elif ri%2==0: shade(cells[ci],'F3F6F9')
    return t
def para(text='', style=None, bold_prefix=None):
    p=doc.add_paragraph(style=style)
    if bold_prefix and text.startswith(bold_prefix):
        r=p.add_run(bold_prefix); r.bold=True; p.add_run(text[len(bold_prefix):])
    else: p.add_run(text)
    return p
def code(text):
    for line in text.strip('\n').split('\n'): doc.add_paragraph(line, style='Code')
def bullet(text):
    p=doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after=Pt(1); p.paragraph_format.line_spacing=1.0; p.add_run(text)

# title
p=doc.add_paragraph(style='Title'); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run('生成器 装饰器 迭代器面试复习讲义')
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; r=p.add_run('以老师笔记和项目源码为准 适合打印与面试前速记'); r.font.size=Pt(9); r.font.color.rgb=RGBColor(90,90,90)
para('使用方法：先背第 1 页“30 秒回答”，再按源码执行顺序复述；面试时优先回答“定义、执行过程、使用场景、易错点”。')

doc.add_heading('一 30 秒总回答', level=1)
para('生成器、装饰器、迭代器解决的是三类不同问题：生成器用 yield 把数据一个一个地产生，并且记住上次暂停的位置；迭代器遵守 __iter__ 和 __next__ 协议，可以通过 next() 逐个取值，for 循环内部就是不断调用 next()；装饰器接收一个函数并返回一个包装函数，用来增加日志、计时、权限校验等功能。老师的装饰器建立在闭包上，闭包让 wrapper 继续保存原函数 func。')
table([
['知识点','一句话定义','面试关键词'],
['迭代器','能记住当前位置并通过 next() 返回下一个值的对象','__iter__、__next__、StopIteration'],
['生成器','使用 yield 的函数，调用后返回生成器对象，按需产生数据','yield、暂停、恢复、节省内存'],
['装饰器','接收函数并返回新函数，在不改原函数主体的情况下增加功能','wrapper、*args、**kwargs、wraps'],
['闭包','内部函数引用外部函数变量，并由外部函数返回内部函数','延长生命周期、装饰器基础']
],[1.0,3.2,2.6])

doc.add_heading('二 老师笔记的学习主线', level=1)
para('老师的文件顺序是：05、闭包.py 先讲闭包和装饰器；07、生成器.py 讲 yield、next() 和暂停恢复；项目中的 query_service.py 用生成器实现 SSE 流式推送；node_md_img.py 使用 MinIO 返回的可迭代结果进行删除遍历。老师没有单独写“迭代器”章节，因此本讲义用生成器代码补齐迭代器协议。')

doc.add_heading('三 闭包：装饰器的基础', level=1)
code('''def fn():
    a = 100
    def fn2():
        nonlocal a
        a += 1
        print(a)
    return fn2

f = fn()
f()  # 101
f()  # 102''')
para('执行 fn() 后，外部函数虽然结束，但 fn2 仍引用变量 a，所以 a 没有立即销毁。老师总结闭包的三个条件：外函数和内函数嵌套；内函数引用外函数局部变量；外函数返回内函数。闭包的作用是延长局部变量生命周期、封装私有变量，也是装饰器的基础。')
para('面试回答：闭包不是“只要有内部函数就算”，关键是内部函数引用了外部函数的局部变量，并且外部函数把内部函数返回出去。每调用一次 fn()，都会产生一套互不影响的闭包数据。')

doc.add_heading('四 装饰器：定义阶段与调用阶段', level=1)
code('''from functools import wraps

def loggerdecorator(func):
    print("装饰器执行")
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"入参：{args}")
        result = func(*args, **kwargs)
        print(f"返回值：{result}")
        return result
    return wrapper

@loggerdecorator
def add(a, b):
    return a + b''')
para('装饰器语法等价于 add = loggerdecorator(add)。因此装饰器函数在 add 定义时执行一次；之后调用 add(10, 20) 时，真正先进入的是 wrapper，wrapper 再调用原来的 func。')
table([
['阶段','实际动作','结果'],
['定义阶段','add = loggerdecorator(add)','创建 wrapper，打印装饰器初始化信息'],
['调用阶段','add(10, 20)','进入 wrapper，记录入参，调用原函数'],
['返回阶段','return result','把原函数结果继续交给调用者']
],[1.2,3.2,2.4])
para('为什么使用 *args 和 **kwargs：装饰器不知道未来会装饰什么函数，因此用它们接收任意位置参数和关键字参数，再用 func(*args, **kwargs) 原样传回。为什么使用 @wraps(func)：不使用它时，add.__name__ 会变成 wrapper；使用后可以恢复原函数的名称、说明等元数据。')

doc.add_heading('五 多个装饰器的顺序', level=1)
code('''@loggerdecorator
'timerdecorator'
def add(a, b):
    return a + b

# 等价于
add = loggerdecorator(timerdecorator(add))''')
para('定义时从下往上，离函数最近的装饰器先执行；调用时从外往内，最外层 wrapper 先进入。面试可直接说：装饰器套装饰器，语法展开后最清楚。')

doc.add_heading('六 生成器：yield 如何暂停和恢复', level=1)
code('''def func():
    print("aaaa")
    yield 1
    print("bbbb")
    yield 2
    print("cccc")
    yield 3
    print("dddd")
    yield 4
    print("eeee")
    yield 5
    print("ffff")
    return 100
    yield 6

result = func()       # 只创建生成器，函数体还没执行
print(next(result))   # aaaa，然后返回 1''')
para('调用生成器函数时，返回的是生成器对象，函数体尚未执行。每次 next(result) 都从上一次 yield 暂停的位置继续，执行到下一个 yield 后再次暂停。第五次 next() 返回 5；第六次 next() 会先打印 ffff，然后因为 return 100 结束并抛出 StopIteration。yield 6 永远不会执行，因为它位于 return 之后。')
table([
['调用','执行过程','返回或结果'],
['第 1 次 next','打印 aaaa，遇到 yield 1 暂停','1'],
['第 2 次 next','打印 bbbb，遇到 yield 2 暂停','2'],
['第 3 次 next','打印 cccc，遇到 yield 3 暂停','3'],
['第 4 次 next','打印 dddd，遇到 yield 4 暂停','4'],
['第 5 次 next','打印 eeee，遇到 yield 5 暂停','5'],
['第 6 次 next','打印 ffff，执行 return 100','StopIteration']
],[1.1,4.0,1.7])
para('生成器的优势是按需产生数据，不必一次把全部结果放进内存，适合大文件、数据库结果、网络流式响应和大量文档处理。')

doc.add_heading('七 迭代器协议与 for 循环', level=1)
code('''class Count:
    def __init__(self):
        self.number = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.number += 1
        if self.number > 3:
            raise StopIteration
        return self.number''')
para('迭代器必须能够被 iter() 获取，并且能够通过 next() 返回下一个值；没有更多数据时必须抛出 StopIteration。for 循环会自动完成 iter、next 和 StopIteration 处理。')
code('''iterator = iter([1, 2, 3])
while True:
    try:
        item = next(iterator)
    except StopIteration:
        break''')
table([
['对象','for 循环','直接 next()','是否保存当前位置'],
['列表、字符串等可迭代对象','可以','通常不可以','对象本身不负责当前位置'],
['迭代器','可以','可以','可以'],
['生成器','可以','可以','可以；生成器是特殊迭代器']
],[2.2,1.3,1.4,2.1])

doc.add_heading('八 项目中的真实应用', level=1)
doc.add_heading('1 SSE 流式推送', level=2)
code('''def generate_data(task_id):
    while True:
        data = get_data(task_id)
        yield f"event: {data.get('event')}\\n"
        yield f"data: {json.dumps(data.get('data'))}\\n\\n"

return StreamingResponse(
    generate_data(task_id),
    media_type="text/event-stream"
)''')
para('query_service.py 中，后台任务把进度写入队列，generate_data() 不断取出数据并 yield 给 StreamingResponse。这样前端可以一条一条收到进度，而不是等待整个检索流程结束后一次性返回。')
doc.add_heading('2 MinIO 对象遍历', level=2)
code('''old_image_generator = minio_client.list_objects(...)
delete_object_list = [
    DeleteObject(obj.object_name)
    for obj in old_image_generator
]

errors = minio_client.remove_objects(...)
for error in errors:
    logger.warning(error)''')
para('node_md_img.py 中 list_objects() 和 remove_objects() 的结果需要遍历才会逐个取得对象或错误信息。这体现了迭代器的延迟产生特征：变量拿到的可能只是一个可遍历结果，不代表全部数据已经同时放入内存。')

doc.add_heading('九 高频面试题与标准回答', level=1)
qa=[
('1 生成器函数和普通函数有什么区别？','生成器函数含有 yield，调用时不立即执行，而是返回生成器对象；每次 next() 执行到下一个 yield 后暂停，下一次从暂停位置继续。'),
('2 yield 和 return 有什么区别？','return 结束函数；yield 产生一个值并暂停，后续还能继续执行。生成器中的 return 值会进入 StopIteration.value。'),
('3 生成器是不是迭代器？','是。生成器天然支持 iter() 和 next()，所以是特殊的迭代器。'),
('4 for 循环底层做了什么？','先调用 iter() 得到迭代器，再反复调用 next()；捕获 StopIteration 后结束循环。'),
('5 装饰器什么时候执行？','装饰器在被装饰函数定义时执行；包装函数在以后调用该函数时执行。'),
('6 @decorator 的本质是什么？','等价于 func = decorator(func)，即把原函数交给装饰器并接收装饰器返回的新函数。'),
('7 为什么 wrapper 要写 *args 和 **kwargs？','因为装饰器要兼容不同函数的参数形式，所以接收任意位置参数和关键字参数，再原样传给原函数。'),
('8 @wraps 有什么作用？','复制原函数的名称、文档等元数据，避免装饰后函数名变成 wrapper。'),
('9 多个装饰器怎么判断顺序？','定义时从下往上，调用时从外往内；先把语法展开成嵌套函数调用最可靠。'),
('10 项目为什么用生成器做 SSE？','队列中有一条数据就 yield 一条，StreamingResponse 将其持续发送给前端，实现流式进度推送，减少等待和内存压力。')]
for q,a in qa:
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(1); r=p.add_run(q); r.bold=True; r.font.size=Pt(9.2)
    p=doc.add_paragraph(a); p.paragraph_format.left_indent=Inches(0.18); p.paragraph_format.space_after=Pt(3); p.paragraph_format.line_spacing=1.0

doc.add_heading('十 易错点清单', level=1)
for x in ['把生成器函数和生成器对象混为一谈：func 是函数，func() 才得到生成器对象。','认为 yield 会结束函数：yield 只暂停，return 才结束。','认为装饰器每次调用都会执行：装饰器通常在定义阶段执行一次。','忘记 return result：wrapper 不返回结果时，原函数结果会丢失。','把可迭代对象和迭代器混为一谈：列表可迭代，但列表本身通常不能直接 next()。','看到生成器变量就认为数据已经全部产生：很多结果只有遍历时才真正获取。','老师示例最后一次 next() 抛 StopIteration 是正常结束，不是逻辑错误。']:
    bullet(x)

doc.add_heading('十一 面试最后背诵版', level=1)
para('我会先区分三个概念。迭代器通过 __iter__ 和 __next__ 逐个返回数据，并在没有数据时抛出 StopIteration；生成器是使用 yield 的特殊迭代器，调用时返回生成器对象，next() 才开始执行，执行到 yield 暂停，下一次从暂停位置继续；装饰器接收原函数并返回 wrapper，通过闭包保存原函数，常用于日志和计时。老师项目中，generate_data() 用生成器配合 StreamingResponse 实现 SSE 流式推送，MinIO 的 list_objects() 和 remove_objects() 结果也通过遍历逐个处理。')

# footer
for section in doc.sections:
    footer=section.footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
    run=footer.add_run('生成器 装饰器 迭代器面试复习讲义'); run.font.size=Pt(8); run.font.color.rgb=RGBColor(120,120,120)

doc.save(out)
print(out)
