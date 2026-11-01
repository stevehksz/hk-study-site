# -*- coding: utf-8 -*-
import os, json, csv
from collections import Counter

WA = r"C:/Users/Administrator/WorkBuddy/_datamine/word-atlas/data/word-atlas.json"
words = json.load(open(WA, encoding="utf-8"))
print("总词条:", len(words))

# CEFR 分布
c = Counter(w.get("cefr","?") for w in words)
print("CEFR 分布:", dict(sorted(c.items())))

# 目标档：B1+B2（英中叩门相关上限）。预览只取示例，全量等定级回填。
TARGET = ["B1","B2"]
relevant_topics = {"environment","science","thinking","society","health","nature","technology","people","culture"}
sel = [w for w in words if w.get("cefr") in TARGET]
print(f"\nB1+B2 全量: {len(sel)} 条")

# 预览：每个档取若干，优先 relevant_topics，凑够 ~40 条展示格式
preview = []
for band in TARGET:
    pool = [w for w in sel if w["cefr"]==band]
    rel = [w for w in pool if w.get("topic") in relevant_topics]
    preview += rel[:22] + [w for w in pool if w not in rel][:6]
preview = preview[:44]
print("预览条数:", len(preview))

# 输出 CSV（Anki 友好）
out_csv = r"C:/Users/Administrator/WorkBuddy/_datamine/word-atlas_B1B2_preview.csv"
with open(out_csv,"w",encoding="utf-8-sig",newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["word","phonetic_uk","phonetic_us","pos","zh","example_en","example_zh","topic","cefr"])
    for w in preview:
        s = w["senses"][0] if w.get("senses") else {}
        ex = w["ex"][0] if w.get("ex") else {}
        wr.writerow([w.get("w",""), w.get("uk",""), w.get("us",""),
                     s.get("pos",""), s.get("zh",""),
                     ex.get("en",""), ex.get("zh",""),
                     w.get("topic",""), w.get("cefr","")])
print("CSV 已写:", out_csv)

# 输出 Obsidian 预览笔记
note = []
note.append("---")
note.append("tags: [插班, 涵涵, 英文, 词表]")
note.append("created: 2026-10-31")
note.append("source: designfuchen/word-atlas (CC BY 4.0, 署名 Word Atlas contributors 词光)")
note.append("---")
note.append("")
note.append("# Word Atlas 目标词表预览（B1–B2）")
note.append("")
note.append("> ⚠️ **预览·非全量**：仅展示格式与难度区间。全量词表等涵涵定级（卷 A/B）回填实际 CEFR 档后，用 `_datamine/word_atlas_export.py` 按档导出。")
note.append("> 数据来源：word-atlas 仓库 `data/word-atlas.json`（7,298 词，CEFR A1–C2）。词库 CC BY 4.0，**须署名「Word Atlas contributors（词光）」**。")
note.append("> ⚠️ 词库文字/插画为 AI 生成、自动校验但**未逐条人工审校**，给涵涵背前先过一遍重点词。")
note.append("")
for i,w in enumerate(preview,1):
    s = w["senses"][0] if w.get("senses") else {}
    ex = w["ex"][0] if w.get("ex") else {}
    note.append(f"## {i}. {w.get('w','')}  `{w.get('cefr','')}` · {w.get('topic','')}")
    note.append(f"- 音标：🇬🇧 {w.get('uk','')}  🇺🇸 {w.get('us','')}")
    note.append(f"- 释义：{s.get('pos','')} {s.get('zh','')}")
    if w.get("tip"): note.append(f"- 提示：{w['tip']}")
    if ex: note.append(f"- 例句：{ex.get('en','')} ｜ {ex.get('zh','')}")
    note.append("")
note.append("---")
note.append("### 复用导出脚本")
note.append("按实际档（如定级为 B1，则 `TARGET=['B1']`）改 `_datamine/word_atlas_export.py` 的 TARGET，重跑即可出全量 CSV/笔记。")
open(r"C:/Users/Administrator/WorkBuddy/_datamine/word-atlas_B1B2_preview.md","w",encoding="utf-8").write("\n".join(note))
print("预览笔记已写: word-atlas_B1B2_preview.md")

# 保存可复用导出脚本（全量，按 TARGET 导出）
exp = '''# -*- coding: utf-8 -*-
import os, json, csv
WA = r"C:/Users/Administrator/WorkBuddy/_datamine/word-atlas/data/word-atlas.json"
TARGET = ["B1","B2"]   # ← 定级后改成涵涵实际档，如 ["B1"] 或 ["A2","B1"]
words = json.load(open(WA, encoding="utf-8"))
sel = [w for w in words if w.get("cefr") in TARGET]
out = r"C:/Users/Administrator/WorkBuddy/_datamine/word-atlas_export.csv"
with open(out,"w",encoding="utf-8-sig",newline="") as f:
    wr = csv.writer(f); wr.writerow(["word","uk","us","pos","zh","ex_en","ex_zh","topic","cefr"])
    for w in sel:
        s = w["senses"][0] if w.get("senses") else {}
        ex = w["ex"][0] if w.get("ex") else {}
        wr.writerow([w.get("w",""),w.get("uk",""),w.get("us",""),s.get("pos",""),s.get("zh",""),ex.get("en",""),ex.get("zh",""),w.get("topic",""),w.get("cefr","")])
print("导出", len(sel), "条 ->", out)
'''
open(r"C:/Users/Administrator/WorkBuddy/_datamine/word_atlas_export.py","w",encoding="utf-8").write(exp)
print("复用脚本已写: word_atlas_export.py")
