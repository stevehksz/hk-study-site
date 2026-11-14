# -*- coding: utf-8 -*-
"""激活碼生成器（葉工本地工具）· 配合香港插班學習站 v2.37 免費額度＋授權碼解鎖

用法:
  python gen_license.py                          # 互動式輸入
  python gen_license.py 陈太太 1                 # 1 個月（從今天起算）
  python gen_license.py 陈太太 12                # 12 個月
  python gen_license.py 陈太太 2026-12-31        # 指定到期日
  python gen_license.py --verify HKSS-20261231-XXXXXXXX   # 只驗證不發碼
  python gen_license.py --list                   # 看已發出記錄

激活碼格式: HKSS-到期日(YYYYMMDD)-SHA256(PUB_SALT|到期日)前8位

⚠️ 鹽的來源：直接從 generate_html.py 抽 `var LIC_PUB_SALT='...'`（單一真相源）。
   抽不到就報錯退出，絕不靜默用舊值——用錯鹽＝發出去的碼全部無效。
⚠️ 與 license_secret.txt 的關係：v2.37 起前端校驗用的是本站**專用公開鹽** LIC_PUB_SALT，
   不再使用 license_secret.txt。原因：公開站源碼本來就可見，用專鹽可避免把其他用途的
   密鑰一併暴露。license_secret.txt 保留原樣，供其他用途。
⚠️ 安全級別（如實標註）：這是「防君子」級。鹽隨頁面分發，讀源碼者可自製碼。
   真正護城河是持續更新的題庫與內容；要真防需雲端側配額（站內路線 B，未做）。
"""
import csv
import datetime
import hashlib
import os
import re
import sys

WS = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(WS, 'generate_html.py')
LEDGER = os.path.join(WS, 'licenses_issued.csv')
MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def load_salt():
    """從 generate_html.py 抽 LIC_PUB_SALT，單一真相源。"""
    if not os.path.exists(GEN):
        sys.exit('錯誤: 找不到 generate_html.py（應與本工具同目錄）')
    src = open(GEN, encoding='utf-8', errors='replace').read()
    m = re.search(r"var\s+LIC_PUB_SALT\s*=\s*'([^']+)'", src)
    if not m:
        sys.exit('錯誤: generate_html.py 裡找不到 `var LIC_PUB_SALT=\'...\'`。\n'
                 '      v2.37 的授權碼校驗依賴這個常量，抽不到就不發碼（避免用錯鹽發出一批廢碼）。')
    return m.group(1)


SALT = load_salt()


def make_code(exp_yyyymmdd):
    mac = hashlib.sha256((SALT + '|' + exp_yyyymmdd).encode()).hexdigest()[:8].upper()
    return 'HKSS-%s-%s' % (exp_yyyymmdd, mac)


def verify_code(code):
    """回傳 (是否有效, 說明)。"""
    code = (code or '').strip().upper()
    m = re.match(r'^HKSS-(\d{4})(\d{2})(\d{2})-([0-9A-F]{8})$', code)
    if not m:
        return False, '格式不對，應為 HKSS-YYYYMMDD-XXXXXXXX'
    ymd = m.group(1) + m.group(2) + m.group(3)
    if m.group(4) != hashlib.sha256((SALT + '|' + ymd).encode()).hexdigest()[:8].upper():
        return False, '簽名校驗失敗（不是本站在用的鹽發出的碼，或碼抄錯）'
    try:
        exp = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return False, '到期日不是合法日期'
    today = datetime.date.today()
    if exp < today:
        return False, '已於 %s 到期（今天 %s）' % (exp, today)
    return True, '有效，至 %s（剩 %d 天）' % (exp, (exp - today).days)


def exp_from_months(months):
    d = datetime.date.today()
    m = d.month - 1 + months
    y = d.year + m // 12
    m = m % 12 + 1
    leap = (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0))
    day = min(d.day, MONTH_DAYS[m - 1] + (1 if (m == 2 and leap) else 0))
    return '%04d%02d%02d' % (y, m, day)


def show_list():
    if not os.path.exists(LEDGER):
        print('還沒有發碼記錄（%s 不存在）' % os.path.basename(LEDGER))
        return
    rows = list(csv.reader(open(LEDGER, encoding='utf-8-sig')))
    if len(rows) <= 1:
        print('記錄為空。')
        return
    print('%-12s %-14s %-12s %-8s %s' % ('發出日期', '客戶', '到期日', '狀態', '激活碼'))
    for r in rows[1:]:
        if len(r) < 4:
            continue
        ok, _ = verify_code(r[3])
        print('%-12s %-14s %-12s %-8s %s' % (r[0], r[1], r[2], '有效' if ok else '已過期', r[3]))


def main():
    args = sys.argv[1:]

    if args and args[0] == '--list':
        show_list()
        return
    if args and args[0] == '--verify':
        if len(args) < 2:
            sys.exit('用法: python gen_license.py --verify HKSS-20261231-XXXXXXXX')
        ok, why = verify_code(args[1])
        print(('✓ ' if ok else '✗ ') + why)
        sys.exit(0 if ok else 1)

    if len(args) >= 2:
        name, spec = args[0], args[1]
    else:
        name = input('客戶姓名/備註: ').strip()
        spec = input('月數或到期日(YYYY-MM-DD): ').strip()
    if not name:
        sys.exit('錯誤: 客戶不能為空')
    if '-' in spec:
        exp = spec.replace('-', '')
        if len(exp) != 8 or not exp.isdigit():
            sys.exit('錯誤: 到期日格式應為 YYYY-MM-DD')
    else:
        if not spec.isdigit():
            sys.exit('錯誤: 請給月數（如 3）或到期日（如 2026-12-31）')
        exp = exp_from_months(int(spec))
    code = make_code(exp)
    ok, why = verify_code(code)
    assert ok, '自檢失敗，發碼邏輯異常：%s' % why
    new_file = not os.path.exists(LEDGER)
    with open(LEDGER, 'a', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(['發出日期', '客戶', '到期日', '激活碼'])
        w.writerow([datetime.date.today().isoformat(), name, exp, code])
    print('客戶  : %s' % name)
    print('到期  : %s-%s-%s' % (exp[:4], exp[4:6], exp[6:8]))
    print('激活碼: %s' % code)
    print('自檢  : %s' % why)
    print('已記錄到 %s' % os.path.basename(LEDGER))
    print('提醒  : 家長在網站「🔑 輸入授權碼」貼上即可；換裝置或清瀏覽器資料需重新輸入。')


if __name__ == '__main__':
    main()
