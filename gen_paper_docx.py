# -*- coding: utf-8 -*-
"""把定级卷 md 转成打印用 docx（解析本项目 md 子集）"""
import re, os, sys
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

VAULT = r"G:\00 咨询&公自媒体\22 香港插班\88 涵涵\01英語"
JOBS = [
    ("20261030-定级卷A_小五至小六水平.md", "20261030-定级卷A_小五至小六水平.docx"),
    ("20261030-定级卷B_中一叩门难度.md", "20261030-定级卷B_中一叩门难度.docx"),
]

def add_runs(par, text):
    # 处理 **bold** 行内格式
    for i, seg in enumerate(re.split(r"\*\*", text)):
        if not seg:
            continue
        run = par.add_run(seg)
        run.bold = (i % 2 == 1)

def convert(md_path, docx_path):
    doc = Document()
    # 页面与基础字体
    for s in doc.sections:
        s.top_margin = Cm(2); s.bottom_margin = Cm(2)
        s.left_margin = Cm(2.2); s.right_margin = Cm(2.2)
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    from docx.oxml.ns import qn
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "微软雅黑")

    lines = open(md_path, encoding="utf-8").read().splitlines()
    i, table_buf = 0, []

    def flush_table():
        nonlocal table_buf
        if not table_buf:
            return
        rows = []
        for ln in table_buf:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):  # 分隔行
                continue
            rows.append(cells)
        table_buf = []
        if not rows:
            return
        t = doc.add_table(rows=len(rows), cols=len(rows[0]))
        t.style = "Table Grid"
        for r, cells in enumerate(rows):
            for c, txt in enumerate(cells):
                if c < len(t.rows[r].cells):
                    cell = t.rows[r].cells[c]
                    cell.text = ""
                    p = cell.paragraphs[0]
                    add_runs(p, txt)
                    for run in p.runs:
                        run.font.size = Pt(10)
                        if r == 0:
                            run.bold = True

    while i < len(lines):
        ln = lines[i]
        stripped = ln.strip()
        # 表格收集
        if stripped.startswith("|") and stripped.endswith("|"):
            table_buf.append(stripped)
            i += 1
            continue
        flush_table()
        if not stripped or stripped == "---":
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            level = min(len(m.group(1)), 4)
            doc.add_heading(m.group(2), level=level)
        elif stripped.startswith("> "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.8)
            add_runs(p, stripped[2:])
            for run in p.runs:
                run.font.size = Pt(10)
                run.font.color.rgb = None
            p.runs and setattr(p.runs[0].font, "italic", False)
        elif stripped.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            add_runs(p, stripped[2:])
        elif re.match(r"^\d+\.\s", stripped):
            # 保留原题号（不用自动编号，避免 Word 重排序号）
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.8)
            add_runs(p, stripped)
        elif re.match(r"^[A-D]\.\s|^　?[A-D]\.", stripped):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.8)
            add_runs(p, stripped)
        else:
            p = doc.add_paragraph()
            add_runs(p, stripped)
        i += 1
    flush_table()
    doc.save(docx_path)
    print("OK", docx_path, os.path.getsize(docx_path), "bytes")

for md_name, dx_name in JOBS:
    convert(os.path.join(VAULT, md_name), os.path.join(VAULT, dx_name))
