# -*- coding: utf-8 -*-
import os, json, time
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

CP = r'C:/Users/Administrator/WorkBuddy/_datamine/chinese-poetry'
OUT_DIR = r'G:/00 咨询&公自媒体/22 香港插班/88 涵涵/02 中文(粵語）'
TODAY = '2026-10-31'

# 手工标准繁体文本（依内地统编六年级课本繁体化，以学校课本为准）
# (展示标题, 朝代, 作者, 正文逐句[带标点], 校验首句, 接受作者写法)
POEMS = [
 ('宿建德江','唐','孟浩然',['移舟泊煙渚，日暮客愁新。','野曠天低樹，江清月近人。'],'移舟泊煙渚',['孟浩然']),
 ('六月二十七日望湖樓醉書','宋','蘇軾',['黑雲翻墨未遮山，白雨跳珠亂入船。','卷地風來忽吹散，望湖樓下水如天。'],'黑雲翻墨未遮山',['蘇軾','苏轼']),
 ('西江月·夜行黃沙道中','宋','辛棄疾',['明月別枝驚鵲，清風半夜鳴蟬。','稻花香裡說豐年，聽取蛙聲一片。','七八个星天外，兩三點雨山前。','舊時茅店社林邊，路轉溪橋忽見。'],'明月別枝驚鵲',['辛棄疾','辛棄疾']),
 ('過故人莊','唐','孟浩然',['故人具雞黍，邀我至田家。','綠樹村邊合，青山郭外斜。','開軒面場圃，把酒話桑麻。','待到重陽日，還來就菊花。'],'故人具雞黍',['孟浩然']),
 ('春日','宋','朱熹',['勝日尋芳泗水濱，無邊光景一時新。','等閒識得東風面，萬紫千紅總是春。'],'勝日尋芳泗水濱',['朱熹']),
 ('回鄉偶書','唐','賀知章',['少小離家老大回，鄉音無改鬢毛衰。','兒童相見不相識，笑問客從何處來。'],'少小離家老大回',['賀知章','贺知章']),
 ('浪淘沙·其七','唐','劉禹錫',['九曲黃河萬里沙，浪淘風簸自天涯。','如今直上銀河去，同到牽牛織女家。'],'九曲黃河萬里沙',['劉禹錫','刘禹锡']),
 ('江南春','唐','杜牧',['千里鶯啼綠映紅，水村山郭酒旗風。','南朝四百八十寺，多少樓臺煙雨中。'],'千里鶯啼綠映紅',['杜牧']),
 ('書湖陰先生壁','宋','王安石',['茅簷長掃淨無苔，花木成畦手自栽。','一水護田將綠繞，兩山排闥送青來。'],'茅簷長掃淨無苔',['王安石']),
 ('寒食','唐','韓翃',['春城無處不飛花，寒食東風御柳斜。','日暮漢宮傳蠟燭，輕煙散入五侯家。'],'春城無處不飛花',['韓翃','韩翃']),
 ('迢迢牽牛星','漢','古詩十九首',['迢迢牽牛星，皎皎河漢女。','纖纖擢素手，札札弄機杼。','終日不成章，泣涕零如雨。','河漢清且淺，相去復幾許。','盈盈一水間，脈脈不得語。'],'迢迢牽牛星',['古詩十九首','佚名']),
 ('十五夜望月','唐','王建',['中庭地白樹棲鴉，冷露無聲濕桂花。','今夜月明人盡望，不知秋思落誰家。'],'中庭地白樹棲鴉',['王建']),
 ('長歌行','漢','漢樂府',['青青園中葵，朝露待日晞。','陽春布德澤，萬物生光輝。','常恐秋節至，焜黃華葉衰。','百川東到海，何時復西歸？','少壯不努力，老大徒傷悲。'],'青青園中葵',['漢樂府','樂府','佚名']),
 ('馬詩·其五','唐','李賀',['大漠沙如雪，燕山月似鉤。','何當金絡腦，快走踏清秋。'],'大漠沙如雪',['李賀','李贺']),
 ('石灰吟','明','于謙',['千錘萬鑿出深山，烈火焚燒若等閒。','粉骨碎身渾不怕，要留清白在人間。'],'千錘萬鑿出深山',['于謙','于谦']),
 ('竹石','清','鄭燮',['咬定青山不放鬆，立根原在破巖中。','千磨萬擊還堅勁，任爾東西南北風。'],'咬定青山不放鬆',['鄭燮','郑燮']),
 ('采薇','先秦','詩經·小雅',['昔我往矣，楊柳依依。','今我來思，雨雪霏霏。','行道遲遲，載渴載飢。','我心傷悲，莫知我哀。'],'昔我往矣',['詩經','佚名']),
 ('送元二使安西','唐','王維',['渭城朝雨浥輕塵，客舍青青柳色新。','勸君更盡一杯酒，西出陽關無故人。'],'渭城朝雨浥輕塵',['王維','王维']),
 ('春夜喜雨','唐','杜甫',['好雨知時節，當春乃發生。','隨風潛入夜，潤物細無聲。','野徑雲俱黑，江船火獨明。','曉看紅濕處，花重錦官城。'],'好雨知時節',['杜甫']),
 ('早春呈水部張十八員外','唐','韓愈',['天街小雨潤如酥，草色遙看近卻無。','最是一年春好處，絕勝煙柳滿皇都。'],'天街小雨潤如酥',['韓愈','韩愈']),
 ('江畔獨步尋花·其六','唐','杜甫',['黃師塔前江水東，春光懶困倚微風。','桃花一簇開無主，可愛深紅愛淺紅。'],'黃師塔前江水東',['杜甫']),
 ('遊子吟','唐','孟郊',['慈母手中線，遊子身上衣。','臨行密密縫，意恐遲遲歸。','誰言寸草心，報得三春暉。'],'慈母手中線',['孟郊']),
 ('泊船瓜洲','宋','王安石',['京口瓜洲一水間，鍾山只隔數重山。','春風又綠江南岸，明月何時照我還。'],'京口瓜洲一水間',['王安石']),
 ('卜算子·送鮑浩然之浙東','宋','王觀',['水是眼波橫，山是眉峰聚。','欲問行人去那邊？眉眼盈盈處。','才始送春歸，又送君歸去。','若到江南趕上春，千萬和春住。'],'水是眼波橫',['王觀','王观']),
 ('浣溪沙·游蘄水清泉寺','宋','蘇軾',['山下蘭芽短浸溪，松間沙路淨無泥，蕭蕭暮雨子規啼。','誰道人生無再少？門前流水尚能西！休將白髮唱黃雞。'],'山下蘭芽短浸溪',['蘇軾','苏轼']),
 ('清平樂·春歸何處','宋','黃庭堅',['春歸何處？寂寞無行路。','若有人知春去處，喚取歸來同住。','春無蹤跡誰知？除非問取黃鸝。','百囀無人能解，因風飛過薔薇。'],'春歸何處',['黃庭堅','黄庭坚']),
]

print('加载仓库索引(排除 rank 空版)...', flush=True)
t0=time.time()
idx=[]
for root,dirs,fs in os.walk(CP):
    if '.git' in root.split(os.sep): continue
    for f in fs:
        if f.endswith('.json') and 'rank' not in f:
            try: d=json.load(open(os.path.join(root,f),encoding='utf-8'))
            except: continue
            if isinstance(d,list):
                for e in d:
                    if isinstance(e,dict): idx.append((f,e))
def g(e): return e.get('author',''), ''.join(e.get('paragraphs',[]) or [])
print('条目',len(idx),'用时',round(time.time()-t0,1),'s', flush=True)

def verify(first, authors):
    cands=[(fp,au,par) for fp,e in idx for au,par in [g(e)] if par.startswith(first)]
    if not cands: return 'MISS(首句未匹配)'
    f=[c for c in cands if any(a in c[1] for a in authors)]
    if f: return 'OK '+f[0][0].split(os.sep)[-1]+' / '+f[0][1]
    return 'WARN(首句有,作者不符):'+cands[0][1]

diag=[]
for show_title,dynasty,author,body,first,authors in POEMS:
    v=verify(first,authors)
    diag.append(f'{v[:6]:6} {show_title} | 作者{author} | {v}')
print('\n'.join(diag))

# ===== A4 双栏紧凑打印 docx =====
from docx.oxml import OxmlElement

doc=Document()
sec=doc.sections[0]
sec.page_width=Mm(210); sec.page_height=Mm(297)
sec.top_margin=Mm(15); sec.bottom_margin=Mm(15)
sec.left_margin=Mm(15); sec.right_margin=Mm(15)

# 整文档双栏（省纸），栏间距约 0.5cm
sectPr=sec._sectPr
cols=sectPr.find(qn('w:cols'))
if cols is None:
    cols=OxmlElement('w:cols'); sectPr.append(cols)
cols.set(qn('w:num'),'2')
cols.set(qn('w:space'),'708')

def set_eastasia(p, font='新細明體'):
    for run in p.runs:
        run.font.name=font
        rPr=run._element.get_or_add_rPr(); rFonts=rPr.get_or_add_rFonts()
        rFonts.set(qn('w:eastAsia'), font)

def keep(p):
    # 本段与下一段尽量不分页/分栏（保证整首诗在同一栏，不翻页看）
    pPr=p._p.get_or_add_pPr()
    k=OxmlElement('w:keepWithNext'); pPr.append(k)

def span(p):
    # 标题跨栏占满整页宽度
    pPr=p._p.get_or_add_pPr()
    c=OxmlElement('w:cols'); c.set(qn('w:num'),'1'); c.set(qn('w:space'),'708')
    pPr.append(c)

# 顶部标题（跨栏）
h=doc.add_paragraph(); h.alignment=WD_ALIGN_PARAGRAPH.CENTER; span(h)
h.add_run('六年級必背古詩詞（繁體打印版）').bold=True; h.runs[0].font.size=Pt(15); set_eastasia(h)
sub=doc.add_paragraph(); sub.alignment=WD_ALIGN_PARAGRAPH.CENTER; span(sub)
rs=sub.add_run('適用：內地統編教材六年級課內必背 + 日積月累篇目'); rs.font.size=Pt(8.5); set_eastasia(sub)
note=doc.add_paragraph(); note.alignment=WD_ALIGN_PARAGRAPH.CENTER; span(note)
rn=note.add_run(f'文本依統編課本繁體化｜以學校課本為準｜生成 {TODAY}')
rn.font.size=Pt(7.5); set_eastasia(note)
sep_top=doc.add_paragraph(); span(sep_top); sep_top.paragraph_format.space_after=Pt(2)

for i,(show_title,dynasty,author,body,_,_) in enumerate(POEMS,1):
    p0=doc.add_paragraph(); p0.alignment=WD_ALIGN_PARAGRAPH.CENTER; keep(p0)
    r0=p0.add_run(f'{i:02d}　〔{dynasty}〕{author}'); r0.bold=True; r0.font.size=Pt(9); set_eastasia(p0)
    p0.paragraph_format.space_before=Pt(2); p0.paragraph_format.space_after=Pt(0)
    pt=doc.add_paragraph(); pt.alignment=WD_ALIGN_PARAGRAPH.CENTER; keep(pt)
    rt=pt.add_run(show_title); rt.bold=True; rt.font.size=Pt(12); set_eastasia(pt)
    pt.paragraph_format.space_after=Pt(1)
    for line in body:
        pb=doc.add_paragraph(); pb.alignment=WD_ALIGN_PARAGRAPH.CENTER; keep(pb)
        pb.add_run(line).font.size=Pt(10); set_eastasia(pb)
        pb.paragraph_format.space_after=Pt(1); pb.paragraph_format.line_spacing=1.05
    pc=doc.add_paragraph(); pc.alignment=WD_ALIGN_PARAGRAPH.CENTER; keep(pc)
    pc.add_run('☐ 已背熟　日期：____　☐ 已默寫　日期：____').font.size=Pt(8.5); set_eastasia(pc)
    pc.paragraph_format.space_after=Pt(4)
    # 分隔段：不设 keep，使两首诗断开，避免被绑定成一组
    sd=doc.add_paragraph(); sd.paragraph_format.space_after=Pt(2)

os.makedirs(OUT_DIR, exist_ok=True)
out=os.path.join(OUT_DIR,'六年級必背古詩詞_繁體A4打印版.docx')
doc.save(out)
print('\n已生成:', out, os.path.getsize(out), 'bytes')
