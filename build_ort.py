# -*- coding: utf-8 -*-
"""提取牛津树书目（正课视频文件名 → 书名，按阶分组，全局去重）→ _ort_books.json
数据性质：书名与阶数为事实信息，来源=本地视频文件目录（童老师牛津绘本视频）。
每本书携带 fs=[视频相对路径]，供网站本地打开时 ▶ 直接播放。
"""
import io, json, os, re, sys

BASE = r'G:\00 咨询&公自媒体\22 香港插班\88 涵涵\01英語\01 牛津树\童老师牛津绘本视频'
# 文件夹名 → 网站显示阶名（处理顺序即去重优先级：专阶在前，1+2 阶兜底）
FOLDERS = [
    ('牛津树1阶', '1階'),
    ('牛津树1+至2阶', '1–2階'),
    ('牛津树3阶', '3階'),
    ('牛津树4阶', '4階'),
    ('牛津树5阶', '5階'),
    ('牛津树6阶', '6階'),
    ('牛津树7阶', '7階'),
    ('牛津树8阶', '8階'),
    ('牛津树9阶(更新)', '9階'),
]

def norm_title(t):
    t = t.strip()
    t = re.sub(r'\s*双语讲解\s*$', '', t)
    t = t.replace('’', "'").replace('（', '(').replace('）', ')')
    t = re.sub(r'\s+', ' ', t)
    return t

def norm_key(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())

books = []
bykey = {}   # norm_key -> 首个书条目（重复书名的视频文件挂到它名下）
matched = 0  # 正课 mp4 总数（含重复书名）
for folder, label in FOLDERS:
    path = os.path.join(BASE, folder)
    if not os.path.isdir(path):
        print('跳过（不存在）:', folder); continue
    cnt = 0; dup = 0
    for fn in sorted(os.listdir(path)):
        m = re.match(r'^\d+\s*【正课】\s*(.+?)(?:-双语讲解|双语讲解)?\.mp4$', fn, re.I)
        if not m:
            continue
        matched += 1
        rel = folder + '/' + fn
        title = norm_title(m.group(1).rstrip('- '))
        if not title:
            continue
        k = norm_key(title)
        if k in bykey:
            bykey[k]['fs'].append(rel); dup += 1
            continue
        e = {'lv': label, 't': title, 'n': 0, 'fs': [rel]}
        bykey[k] = e; books.append(e); cnt += 1
    print(f'{folder} → {label}: 新增 {cnt}，重复 {dup}')

order = ['1階', '1–2階', '3階', '4階', '5階', '6階', '7階', '8階', '9階']
books.sort(key=lambda b: order.index(b['lv']))
# 多集讲解合并为一本书：Key Trouble (1)/(2)... → Key Trouble（附集数）
merged = {}
for b in books:
    m = re.match(r'^(.*?)\s*\((\d+)\)$', b['t'])
    if m:
        base = m.group(1).strip()
        e = merged.setdefault((b['lv'], norm_key(base)), {'lv': b['lv'], 't': base, 'n': 0, 'fs': []})
        e['n'] += 1; e['fs'] += b['fs']
    else:
        merged.setdefault((b['lv'], norm_key(b['t'])), {'lv': b['lv'], 't': b['t'], 'n': 0, 'fs': b['fs']})
books = [v for _, v in sorted(merged.items(), key=lambda kv: order.index(kv[1]['lv']))]
for b in books:
    b['fs'].sort()  # 同书多講按文件名（编号）排
    b['n'] = len(b['fs'])  # 講数=文件数（含同文件夹上下两講被旧逻辑当重复的 48 本）
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_ort_books.json'), 'w', encoding='utf-8').write(
    json.dumps(books, ensure_ascii=False, separators=(',', ':')))

by = {}
for b in books: by[b['lv']] = by.get(b['lv'], 0) + 1
total_fs = sum(len(b['fs']) for b in books)
print('各阶数量:', by, '总计:', len(books), '视频文件:', total_fs)
if len(books) < 150:  # 合并多講後約 204 本（合併前 455 條）
    print('⚠️ 数量偏少，请人工核对'); sys.exit(1)
if total_fs != matched:
    print(f'⚠️ 视频文件数不守恒: {total_fs} != {matched}，请人工核对'); sys.exit(1)
print('OK _ort_books.json')
