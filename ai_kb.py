# -*- coding: utf-8 -*-
"""v1.74 AI 客服白名單知識庫構建器。

唯一真相源是站內模板本身：FAQ 10 問、申請時間線、身份政策摘要直接從 TEMPLATE 的
HTML 段落抽取，70 校名單與類別從 build_data.json 抽取。不手寫副本，站內改了 KB 跟著改。

刻意不納入的欄位：Band／組別（站內標「非官方」，餵了等於鼓勵模型編）、
學費金額、學額、任何搜尋摘要或機構軟文。
"""
import json
import os
import re

WS = os.path.dirname(os.path.abspath(__file__))


def _seg(html, start, end):
    i = html.find(start)
    if i < 0:
        return ''
    j = html.find(end, i + len(start)) if end else -1
    return html[i:j if j > 0 else len(html)]


def _clean(s):
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    return re.sub(r'\s+', ' ', s).strip()


def build_ai_kb(template_html):
    items = []

    def add(tag, title, body):
        t, b = _clean(title), _clean(body)
        if t and b:
            items.append({'k': tag, 't': t, 's': b})

    # ① FAQ 15 問（v1.88 起按「家長顧慮」分 5 組；分組頭是 <h3 class="faq-grp">，不在 gcard 內，天然不入庫）
    # ⚠️ 每張卡尾部多了一段 <p class="nx">下一步…</p>（站內跳轉引導，非知識）。
    #    正則只取第一段 <p> 當答案，nx 段用可選組跳過——否則下一步文案會混進 AI 答案。
    faq = _seg(template_html, 'id="faqView"', 'id="progressView"')
    for h3, p in re.findall(r'<div class="gcard"><h3>(.*?)</h3>\s*<p>(.*?)</p>(?:<p class="nx">.*?</p>)?\s*</div>', faq, re.S):
        add('常見問題', h3, p)

    # ② 申請時間線（三列表格行；日期一律保留站內「以當年公告為準」口徑）
    tl = _seg(template_html, 'id="timelineView"', 'id="schoolsView"')
    for c1, c2, c3 in re.findall(r'<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>', tl, re.S):
        add('申請時間線', c1 + '｜' + c2, c3)

    # ③ 身份與政策摘要
    pol = _seg(template_html, 'id="policyView"', 'id="faqView"')
    for h3, p in re.findall(r'<div class="gcard(?: warn)?">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</div>', pol, re.S):
        add('身份政策', h3, p)

    # ④ 70 校名單（只餵站內已核實的「校名／類別／性別／學段」，不餵 Band／坐標／電話）
    data = json.load(open(os.path.join(WS, 'build_data.json'), encoding='utf-8'))
    sec, pri = data.get('sch_profiles', {}), data.get('sch_pri_profiles', {})
    for name in data.get('school_geo', {}):
        p = pri.get(name) or sec.get(name) or {}
        stage = '小學' if name in pri else '中學'
        bits = ['學段：' + stage]
        if p.get('type'):
            bits.append('類別：' + str(p['type']))
        if p.get('gender'):
            bits.append('性別：' + str(p['gender']))
        add('學校名冊', name, '；'.join(bits) + '。本站未收錄該校官方 Banding，如需分檔請查學校官網及教育局。')

    return items


def kb_json(template_html):
    """注入 <script> 前的序列化：防 </script> 提前閉合。"""
    return json.dumps(build_ai_kb(template_html), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


if __name__ == '__main__':
    src = open(os.path.join(WS, 'generate_html.py'), encoding='utf-8').read()
    tpl = src.split("TEMPLATE = r'''", 1)[1].rsplit("'''", 1)[0]
    kb = build_ai_kb(tpl)
    from collections import Counter
    print('KB 條數:', len(kb), dict(Counter(x['k'] for x in kb)))
    print('字數:', sum(len(x['t']) + len(x['s']) for x in kb))
    print('含 Band 條目:', sum(1 for x in kb if re.search(r'Band\s*[123]', x['s'])))
    for x in kb[:3]:
        print(' -', x['k'], x['t'][:38], '|', x['s'][:60])
