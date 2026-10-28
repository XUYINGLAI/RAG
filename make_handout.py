from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
from pathlib import Path

out = Path(r'C:\Users\23716\Desktop\test\test111\进程线程协程_模拟面试打印讲义.docx')
doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.65); sec.bottom_margin = Inches(0.65); sec.left_margin = Inches(0.75); sec.right_margin = Inches(0.75)
styles = doc.styles
styles['Normal'].font.name='Microsoft YaHei'; styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'),'Microsoft YaHei'); styles['Normal'].font.size=Pt(10.5)
for name,size in [('Title',22),('Heading 1',16),('Heading 2',13),('Heading 3',11)]:
    s=styles[name]; s.font.name='Microsoft YaHei'; s._element.rPr.rFonts.set(qn('w:eastAsia'),'Microsoft YaHei'); s.font.size=Pt(size); s.font.bold=True; s.font.color.rgb=RGBColor(0,0,0)
styles['Title'].paragraph_format.space_after=Pt(8)
for n in ['Heading 1','Heading 2','Heading 3']:
    styles[n].paragraph_format.space_before=Pt(10); styles[n].paragraph_format.space_after=Pt(4)

def shade(cell, fill):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),fill); tcPr.append(shd)
def borders(table):
    tblPr=table._tbl.tblPr; b=tblPr.first_child_found_in('w:tblBorders')
    if b is None: b=OxmlElement('w:tblBorders'); tblPr.append(b)
    for edge in ('top','left','bottom','right','insideH','insideV'):
        e=OxmlElement(f'w:{edge}'); e.set(qn('w:val'),'single'); e.set(qn('w:sz'),'4'); e.set(qn('w:color'),'D9D9D9'); b.append(e)
def add_table(headers, rows, widths=None):
    t=doc.add_table(rows=1, cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.style='Table Grid'; borders(t)
    for i,h in enumerate(headers):
        c=t.rows[0].cells[i]; c.text=h; shade(c,'1F4E78'); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for p in c.paragraphs:
            for r in p.runs: r.font.bold=True; r.font.color.rgb=RGBColor(255,255,255); r.font.size=Pt(9.5)
    for ri,row in enumerate(rows):
        cells=t.add_row().cells
        for i,v in enumerate(row):
            cells[i].text=str(v); cells[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if ri%2==1: shade(cells[i],'F3F6F9')
            for p in cells[i].paragraphs:
                p.paragraph_format.space_after=Pt(1)
                for r in p.runs: r.font.size=Pt(9.2)
    return t

def p(text='', bold=False, italic=False):
    para=doc.add_paragraph(); para.paragraph_format.space_after=Pt(4); para.paragraph_format.line_spacing=1.12
    run=para.add_run(text); run.bold=bold; run.italic=italic; return para

def bullet(text, level=0):
    para=doc.add_paragraph(style='List Bullet' if level==0 else 'List Bullet 2'); para.paragraph_format.space_after=Pt(2); para.paragraph_format.line_spacing=1.08; para.add_run(text); return para

def code(text):
    para=doc.add_paragraph(); para.paragraph_format.left_indent=Inches(0.25); para.paragraph_format.space_after=Pt(4)
    r=para.add_run(text); r.font.name='Consolas'; r._element.rPr.rFonts.set(qn('w:eastAsia'),'Consolas'); r.font.size=Pt(9); return para

# title
t=doc.add_paragraph(style='Title'); t.alignment=WD_ALIGN_PARAGRAPH.CENTER; t.add_run('进程 线程 协程模拟面试打印讲义')
sub=doc.add_paragraph(); sub.alignment=WD_ALIGN_PARAGRAPH.CENTER; rr=sub.add_run('按老师笔记整理  面向明日提问与面试复习'); rr.font.size=Pt(11); rr.font.color.rgb=RGBColor(89,89,89)
p('使用方法：先背“30秒总答”，再理解对比表和代码执行链，最后用面试题自测。文中“老师口径”来自老师的两份总结笔记；“面试补充”用于避免追问时表述过于绝对。')

doc.add_heading('一 30秒总答',1)
p('程序是保存在硬盘上的静态代码；程序运行起来后成为进程，进程是资源分配的基本单位；线程依赖进程，是代码执行的最小单位，一个进程至少有一个主线程。线程共享进程的大部分资源，所以创建和切换成本通常小于进程，但多线程操作共享数据时要考虑线程安全。')
p('多进程、多线程和协程都可以用来提高等待场景下的整体效率。IO密集型任务优先考虑协程，不能使用异步库时考虑多线程；CPU密集型任务按老师的口径选择多进程，因为多进程可以利用多个 CPU 核心实现真正并行。协程运行在线程中，由程序通过事件循环和 await 主动调度，适合大量异步 IO。')


doc.add_heading('二 三个概念先分清',1)
add_table(['对象','老师的定义','关键特征','面试关键词'],[
('程序','代码的集合，通常是硬盘上的文件，静态。','还没有运行，不占用运行时资源。','静态代码、文件'),
('进程','程序的一次运行过程，运行后变成进程。','动态；占用 CPU、内存等资源；是线程的容器。','资源分配、隔离、并行'),
('线程','依赖进程的执行单位。每个进程至少一个主线程。','执行代码的最小单位；自己的资源少，大部分共享进程资源。','执行、共享、线程安全'),
('协程','用户态、非抢占式的上下文切换技术，也称微线程。','依赖线程；由程序主动在 await/IO 等待处切换；同一时刻一个协程执行。','协作式调度、事件循环、异步IO')])
p('关系记忆：程序像一份菜谱，进程像正在营业的一家厨房，线程像厨房里的厨师，协程像由厨师主动安排的多个小任务。一个进程可以有多个线程；多个协程通常运行在一个线程的事件循环中。')


doc.add_heading('三 并发与并行',1)
add_table(['概念','含义','典型实现'],[
('并发','一段时间内处理多个任务；任务可能交替推进，不代表同一时刻同时运行。','单线程协程、多线程'),
('并行','同一时刻在多个执行单元上真正同时运行。','多进程、多个 CPU 核心'),
('阻塞','当前执行单元在等待资源，后续代码暂时无法继续。','网络、磁盘、数据库、sleep 等 IO 等待')])
p('老师强调：多进程和多线程最基本的作用都是解决阻塞，但各自擅长的任务不同。判断方案时先问：任务是在等 IO，还是在做大量计算？')


doc.add_heading('四 多线程：共享资源与线程锁',1)
p('老师示例中，fn1 和 fn2 各自先打印、再 sleep 两秒、再打印。如果串行调用，总耗时约四秒；创建两个线程并 start 后，两个 sleep 可以重叠，总耗时通常接近两秒。t1.join() 和 t2.join() 的作用是让主线程等待子线程执行结束，避免主线程提前结束。')
code('t1 = threading.Thread(target=fn1, name="thread01", args=())\nt2 = threading.Thread(target=fn2, name="thread02", args=())\nt1.start(); t2.start()\nt1.join(); t2.join()')
p('线程共享进程内的全局变量。多个线程同时读写同一个变量时，可能出现“读到旧值、修改后互相覆盖”的竞态条件，因此老师总结为：多线程操作全局变量，要考虑加互斥锁。锁的基本流程是 acquire 上锁，临界区操作完成后 release 解锁；实际代码更推荐使用 with lock，确保异常时也能释放。')
code('lock = threading.Lock()\nwith lock:\n    count += 1')
p('面试补充：Python 中常说的 GIL 是 CPython 解释器的实现细节，它限制同一进程内线程同时执行 Python 字节码；IO等待时线程可以切换，因此多线程适合 IO 密集型任务。带锁不等于线程变成串行，锁只保护需要一致性的临界区。')


doc.add_heading('五 多进程：CPU 密集型与真正并行',1)
p('老师示例用 multiprocessing.Process 或自定义 Process 子类启动两个进程。每个进程拥有相对独立的内存空间和解释器状态，进程之间不能像线程一样直接共享普通全局变量；需要共享时要使用队列、管道、共享内存或其他进程间通信方式。')
code('p1 = multiprocessing.Process(target=fn1, name="pro01", args=())\np2 = multiprocessing.Process(target=fn2, name="pro02", args=())\np1.start(); p2.start()\np1.join(); p2.join()')
add_table(['任务类型','老师建议','原因','常见例子'],[
('IO密集型','协程；不能异步时多线程','大量时间在等待 IO；线程可在等待时切换，进程开销较大。','网络请求、数据库、文件读写'),
('CPU密集型','多进程','多线程受 GIL 影响，同一进程同一时刻难以并行执行 Python 字节码；多进程可利用多个核心。','大量计算、图像处理、复杂数据计算')])
p('老师的记忆句：IO密集用多进程“能跑但血亏”；计算密集用多线程“能跑但白瞎”。面试时把这句话展开成“进程创建和切换开销、GIL、CPU核心利用率”三个原因。')


doc.add_heading('六 协程与 asyncio 执行链',1)
p('协程是依赖线程的微线程。它不是操作系统直接抢占的线程，而是程序在 await 或主动挂起的位置让出执行权。所有协程通常在同一个线程中运行，同一时刻只有一个协程执行；当一个协程等待 IO 时，事件循环把执行机会交给其他就绪协程。')
add_table(['步骤','老师代码中的对象','发生什么'],[
('1 定义','async def get_url(url)','定义协程函数；函数体不会在定义时执行。'),
('2 调用','get_url(url)','返回协程对象，不会立即执行函数体。'),
('3 包装任务','create_task(c)','把协程对象包装成事件循环可调度的 Task。'),
('4 启动循环','asyncio.run(main(...))','创建并启动事件循环，运行主协程。'),
('5 主动等待','await asyncio.sleep(2)','当前协程挂起，事件循环调度其他任务。'),
('6 汇总结果','await gather(*list2)','并发执行并收集结果；结果顺序与传入任务顺序一致。')])
code('async def get_url(url):\n    print("开始请求")\n    await asyncio.sleep(2)\n    return f"获取到{url}请求的状态"\n\nasync def main(urls):\n    coroutines = [get_url(url) for url in urls]\n    tasks = [asyncio.create_task(c) for c in coroutines]\n    return await asyncio.gather(*tasks)\n\nresult = asyncio.run(main(["http://www.baidu.com", "https://www.taobao.com"]))')
p('事件循环可以理解为持续管理任务状态的调度器：就绪的执行，等待 IO 的挂起，IO 完成后再唤醒。async 只表示协程函数；真正运行还需要放入事件循环。await 是等待异步操作完成，同时也是协作式切换的关键位置。')


doc.add_heading('七 三者对比速记表',1)
add_table(['维度','多进程','多线程','协程'],[
('调度者','操作系统','操作系统','程序/事件循环'),
('内存关系','进程间相对隔离','共享进程内存','通常共享线程内存'),
('切换成本','高','中','低'),
('并行能力','可真正并行','CPython中受GIL限制','单线程内不做真正并行'),
('适合任务','CPU密集','IO密集、异步库不足时','大量IO密集'),
('主要风险','进程通信和资源开销','竞态、死锁、锁竞争','阻塞事件循环、忘记await'),
('老师最终选择','CPU密集型','IO密集型备选','IO密集型优先')])


doc.add_heading('八 高频模拟面试题与标准回答',1)
qs=[
('1 进程和线程有什么区别？','进程是程序运行后的动态实体，也是资源分配和隔离的基本单位；线程依赖进程，是执行代码的最小单位。线程共享进程的大部分资源，所以创建和切换更轻，但共享数据带来线程安全问题。'),
('2 为什么 IO 密集型用多线程或协程？','IO 密集型大部分时间在等待网络、磁盘或数据库。等待时可以让出执行权，让其他任务推进。协程切换成本更低；如果库不支持异步，就用多线程。'),
('3 为什么 CPU 密集型用多进程？','CPU 密集型主要耗费计算时间。CPython 的 GIL 使同一进程内多个线程难以同时执行 Python 字节码；多进程有独立解释器并可占用多个核心，实现真正并行。'),
('4 协程是不是线程？','不是。协程是运行在线程中的用户态调度单位，依靠 async/await 和事件循环协作切换；线程由操作系统调度。'),
('5 async 函数调用后会立即执行吗？','不会。调用 async 函数先得到协程对象；把它交给 asyncio.run、create_task 等事件循环机制后，函数体才开始执行。'),
('6 await 的作用是什么？','等待一个可等待对象完成；等待期间当前协程挂起，事件循环可以运行其他就绪任务。它必须出现在 async 函数中。'),
('7 create_task 和 gather 有什么区别？','create_task 把协程包装成可调度的任务；gather 并发等待多个任务并收集结果。常见写法是 create_task 创建任务，await gather 汇总。'),
('8 join 的作用是什么？','让当前线程或进程等待目标子线程或子进程结束，再继续执行。它解决的是收尾和同步，不是创建并发。'),
('9 多线程为什么要加锁？','多个线程共享数据时，读改写可能交错，造成竞态和结果丢失。锁把临界区变成互斥访问；锁的范围要尽量小，避免锁竞争。'),
('10 协程有什么坑？','协程本身不会自动让同步阻塞代码变快；如果在事件循环里调用长时间同步计算或阻塞 IO，会卡住所有协程。要使用异步库，CPU计算应移到进程池或其他执行器。')]
for q,a in qs:
    p(q,bold=True); p('答：'+a)


doc.add_heading('九 一分钟综合回答模板',1)
p('如果让我选择并发模型，我会先判断任务类型。对于大量网络、数据库或文件等待，优先使用协程和 asyncio，让事件循环在 await 处切换；如果第三方库只有同步接口，则使用多线程。对于大量 CPU 计算，在 CPython 中使用多进程，利用多个核心并绕开单进程内 GIL 的限制。多线程共享内存，必须保护共享可变数据；多进程隔离性更强，但进程创建、通信和内存开销更大。无论使用哪种模型，都要通过 join、await 或任务收集机制完成同步和结果回收。')


doc.add_heading('十 明天上场前自测清单',1)
for x in ['能用30秒说清程序、进程、线程、协程的关系。','能解释并发和并行，不把“并发”直接说成“同时执行”。','能回答 IO 密集型为什么协程/多线程，CPU 密集型为什么多进程。','能按顺序说出 async def、调用、create_task、asyncio.run、await、gather 的执行链。','能解释 join 是等待，锁是保护共享数据。','能主动补充：协程不是线程；同步阻塞代码会卡住事件循环；GIL是CPython实现细节。','遇到追问时先给结论，再给原因和一个老师笔记中的代码例子。']:
    bullet('□ '+x)

p('资料依据：老师仓库 kb_0716/test/10、多进程和多线程总结.py；kb_0716/test/11、协程的总结.py。')

# footer page number
for section in doc.sections:
    footer=section.footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run('进程 线程 协程模拟面试打印讲义')

doc.save(out)
print(out)
