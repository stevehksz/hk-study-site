# -*- coding: utf-8 -*-
import os, json, glob

CP = r"C:/Users/Administrator/WorkBuddy/_datamine/chinese-poetry"

# 小学级清单：唐绝句为主 + 少量宋词。title/author 用繁體以匹配仓库。
# paraphrase 为本人撰写的白话释义（非搬运）。firstline 用于消歧（同题多首时定位名篇）。
TARGETS = [
    # 唐诗（全唐诗按 title 匹配）
    {"title":"靜夜思","author":"李白","paraphrase":"床前月光，疑是地上霜；抬头望月，低头想家。"},
    {"title":"春曉","author":"孟浩然","paraphrase":"春睡不觉天亮，处处鸟鸣；夜来风雨，不知落花多少。"},
    {"title":"詠鵝","author":"駱賓王","paraphrase":"鹅鹅鹅，弯脖向天歌；白毛浮绿水，红掌拨清波。"},
    {"title":"登鸛雀樓","author":"王之渙","paraphrase":"夕阳依山尽，黄河入海流；想看千里景，再上一层楼。"},
    {"title":"","author":"李紳","firstline":"鋤禾日當午","display":"憫農（鋤禾日當午）","paraphrase":"中午锄禾汗滴土，谁知碗里饭，粒粒皆辛苦。"},
    {"title":"江雪","author":"柳宗元","paraphrase":"千山无鸟，万径无人；孤舟老翁，独钓寒江雪。"},
    {"title":"鹿柴","author":"王維","paraphrase":"空山不见人，只闻人语响；夕阳入深林，照在青苔上。"},
    {"title":"相思","author":"王維","paraphrase":"红豆生南国，春来发几枝；愿君多采撷，此物最相思。"},
    {"title":"九月九日憶山東兄弟","author":"王維","paraphrase":"独在异乡为异客，每逢佳节倍思亲；遥想兄弟登高，少我一人。"},
    {"title":"早發白帝城","author":"李白","paraphrase":"朝辞白帝彩云间，千里江陵一日还；两岸猿声，轻舟已过万重山。"},
    {"title":"望廬山瀑布","author":"李白","paraphrase":"日照香炉生紫烟，遥看瀑布挂前川；飞流直下三千尺，疑是银河落九天。"},
    {"title":"絕句","author":"杜甫","firstline":"兩個黃鸝","paraphrase":"两个黄鹂鸣翠柳，一行白鹭上青天；窗含西岭雪，门泊东吴船。"},
    {"title":"贈汪倫","author":"李白","paraphrase":"李白乘舟将欲行，忽闻岸上踏歌声；桃花潭水深千尺，不及汪伦送我情。"},
    {"title":"楓橋夜泊","author":"張繼","paraphrase":"月落乌鸦霜满天，江枫渔火对愁眠；姑苏城外寒山寺，夜半钟声到客船。"},
    {"title":"滁州西澗","author":"韋應物","paraphrase":"独怜幽草涧边生，上有黄鹂深树鸣；春潮带雨晚来急，野渡无人舟自横。"},
    {"title":"遊子吟","author":"孟郊","paraphrase":"慈母手中线，游子身上衣；临行密密缝，谁言寸草心，报得三春晖。"},
    {"title":"賦得古原草送別","author":"白居易","firstline":"離離原上草","paraphrase":"原上草岁岁枯荣；野火烧不尽，春风吹又生。"},
    {"title":"池上","author":"白居易","paraphrase":"小娃撑小艇，偷采白莲回；不解藏踪迹，浮萍一道开。"},
    {"title":"尋隱者不遇","author":"賈島","paraphrase":"松下问童子，言师采药去；只在此山中，云深不知处。"},
    {"title":"樂遊原","author":"李商隱","paraphrase":"向晚意不适，驱车登古原；夕阳无限好，只是近黄昏。"},
    {"title":"望天門山","author":"李白","paraphrase":"天门中断楚江开，碧水东流至此回；两岸青山相对出，孤帆一片日边来。"},
    {"title":"黃鶴樓送孟浩然之廣陵","author":"李白","paraphrase":"故人西辞黄鹤楼，烟花三月下扬州；孤帆远影碧空尽，唯见长江天际流。"},
    {"title":"涼州詞","author":"王之渙","firstline":"黃河遠上","paraphrase":"黄河远上白云间，一片孤城万仞山；羌笛何须怨杨柳，春风不度玉门关。"},
    {"title":"出塞","author":"王昌齡","paraphrase":"秦时明月汉时关，万里长征人未还；但使龙城飞将在，不教胡马度阴山。"},
    {"title":"芙蓉樓送辛漸","author":"王昌齡","paraphrase":"寒雨连江夜入吴，平明送客楚山孤；洛阳亲友如相问，一片冰心在玉壶。"},
    {"title":"風","author":"李嶠","paraphrase":"解落三秋叶，能开二月花；过江千尺浪，入竹万竿斜。"},
    {"title":"塞下曲","author":"盧綸","firstline":"月黑雁飛高","paraphrase":"月黑雁飞高，单于夜遁逃；欲将轻骑逐，大雪满弓刀。"},
    {"title":"獨坐敬亭山","author":"李白","paraphrase":"众鸟高飞尽，孤云独去闲；相看两不厌，只有敬亭山。"},
    # 宋词（宋词按 rhythmic 词牌 + author 匹配；仓库词牌/作者为简体）
    {"title":"如夢令","author":"李清照","rhythmic":"如梦令","paraphrase":"昨夜雨疏风骤，睡醒酒意未消；问卷帘人，却道海棠依旧。知否知否，应是绿肥红瘦。"},
    {"title":"水調歌頭","author":"苏轼","rhythmic":"水调歌头","paraphrase":"明月几时有，把酒问青天；人有悲欢离合，月有阴晴圆缺，此事古难全。但愿人长久，千里共婵娟。"},
]

# ---- 载入全唐诗 ----
tang = []
for fp in glob.glob(os.path.join(CP, "全唐诗", "poet.tang.*.json")):
    try:
        tang.extend(json.load(open(fp, encoding="utf-8")))
    except Exception as e:
        print("载入失败", fp, e)

# ---- 载入宋词 ----
ci = []
for fp in glob.glob(os.path.join(CP, "宋词", "ci.song.*.json")):
    try:
        ci.extend(json.load(open(fp, encoding="utf-8")))
    except Exception as e:
        print("载入失败", fp, e)

print(f"全唐诗载入 {len(tang)} 首；宋词载入 {len(ci)} 首")

def find_tang(t):
    cands = tang
    if t.get("title"):
        cands = [p for p in cands if t["title"] in p.get("title","")]
        if not cands:  # 标题未命中，退而按首句
            cands = [p for p in tang if any(t.get("firstline","") in para for para in p.get("paragraphs",[]))]
    if t.get("firstline"):
        f = [p for p in cands if any(t["firstline"] in para for para in p.get("paragraphs",[]))]
        if f: cands = f
    if t.get("author"):
        a = [p for p in cands if p.get("author")==t["author"]]
        if a: cands = a
    return cands[0] if cands else None

def find_ci(t):
    cands = [p for p in ci if p.get("rhythmic")==t.get("rhythmic") and p.get("author")==t.get("author")]
    return cands[0] if cands else None

results = []
miss = []
for t in TARGETS:
    if t.get("rhythmic"):
        p = find_ci(t)
        kind = "宋词"
    else:
        p = find_tang(t)
        kind = "唐"
    if p is None:
        miss.append(t["title"]); continue
    results.append({
        "display": t.get("display") or t["title"], "author": p.get("author"), "kind": kind,
        "paragraphs": p.get("paragraphs", []),
        "rhythmic": p.get("rhythmic",""),
        "paraphrase": t["paraphrase"],
        "repo_title": p.get("title",""),
    })

print(f"\n匹配成功 {len(results)} / {len(TARGETS)}")
print("未匹配：", miss if miss else "无")

# ---- 生成 Obsidian 背诵卡笔记 ----
VAULT = r"G:/00 咨询&公自媒体/22 香港插班/88 涵涵/02 中文(粵語）/唐詩宋詞繁體背诵卡.md"
note = []
note.append("---")
note.append("tags: [插班, 涵涵, 中文, 繁體, 背诵]")
note.append("created: 2026-10-31")
note.append("source: chinese-poetry/chinese-poetry (GitHub, 数据来源于互联网)")
note.append("---")
note.append("")
note.append("# 唐诗宋词·繁体背诵卡（小学级 30 首）")
note.append("")
note.append("> 用途：练**繁体字认读** + 香港中文课古诗背诵。原文从 `chinese-poetry` 仓库抽取（繁体）。")
note.append("> ⚠️ 仓库数据「来源于互联网」，无严格校勘；**白话释义为本人撰写**，供理解用，背诵以原文字为准。")
note.append("> ⚠️ **拼音/粤拼未附**：古典诗多音字机器注音易错，建议用 Pleco / 粤语 App 校对后再填。下方留了空格。")
note.append("> 静夜思：仓库「全唐诗」版为「牀前看月光 / 舉頭望山月」（宋本），与常见课本「床前明月光 / 舉頭望明月」不同，两版都认即可。")
note.append("")
cnt = 0
for r in results:
    cnt += 1
    label = f"{r['display']}（{r['author']}·{r['kind']}）"
    note.append(f"## {cnt}. {label}")
    note.append("")
    note.append("**原文（繁体）**")
    note.append("")
    note.append("<br>".join(r["paragraphs"]))
    note.append("")
    note.append(f"> 白话：{r['paraphrase']}")
    note.append("")
    note.append("| 拼音（普） | 粤拼 | 背诵打卡 |")
    note.append("|---|---|---|")
    note.append(f"| （待注） | （待注） | ☐ ____ |")
    note.append("")
note.append("---")
note.append(f"共 {cnt} 首。原文抽取自 chinese-poetry 仓库（全唐诗 57,607 首 / 宋词 21,053 首子集），繁体文本。")
open(VAULT, "w", encoding="utf-8").write("\n".join(note))
print(f"\n背诵卡笔记已写: {VAULT}  ({cnt} 首)")

json.dump(results, open(r"C:/Users/Administrator/WorkBuddy/2026-10-29-22-18-23/_poems_extracted.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("已写出 _poems_extracted.json")
