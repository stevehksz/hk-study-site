# -*- coding: utf-8 -*-
"""生成「教育局官方字表 3,171 字」的繁→簡對照表（只列有差異者）。

來源口徑（必須隨資料一起保留）：
- 字表：_lex3171.txt（教育局《香港小學學習字詞表》2007 小學用字一覽表文本轉錄，3,171 字筆畫序）
- 對照：OpenCC 開源轉換表 t2s 機械轉換，套件 opencc-python-reimplemented==0.1.7
- ⚠️ 非教育局官方對照。部分差異屬香港／內地規範字形差異或異體歸併（如 內→内、冊→册、並→并），
  並非一對一簡繁關係；一字多義（乾／幹、後／后、裏／里）須按詞義判斷，以課本為準。
- 輸出 _lex_simp.json 為 {繁:簡} 物件，構建期由 generate_html.py 直接注入靜態頁，
  瀏覽器零外部依賴；重跑本腳本即可刷新資料（構建本身不需要裝 opencc）。
"""
import io
import json
import os

from opencc import OpenCC

WS = os.path.dirname(os.path.abspath(__file__))
raw = io.open(os.path.join(WS, '_lex3171.txt'), encoding='utf-8').read()
chars = ''.join(c for c in raw if not c.isspace())
assert len(chars) == 3171 and len(set(chars)) == 3171, '字表須 3171 唯一字'

simp = OpenCC('t2s').convert(chars)
assert len(simp) == len(chars), 'OpenCC 輸出須與字表逐字對齊（單字對單字）'

diff = {a: b for a, b in zip(chars, simp) if a != b}
assert len(diff) > 1000, '差異對數量異常：%d' % len(diff)
assert all(len(k) == 1 and len(v) == 1 and k != v for k, v in diff.items()), '鍵值須為單字且不相同'

out = json.dumps(diff, ensure_ascii=False, separators=(',', ':'))
io.open(os.path.join(WS, '_lex_simp.json'), 'w', encoding='utf-8').write(out)
print('差異對 %d / %d 字，JSON %d bytes' % (len(diff), len(chars), len(out.encode('utf-8'))))
print('首 10 對：', ' '.join('%s>%s' % kv for kv in list(diff.items())[:10]))
