# -*- coding: utf-8 -*-
"""激活碼生成器（葉工本地工具）· 配合學習站 v1.21 授權碼月付
用法:
  python gen_license.py                    # 互動式輸入
  python gen_license.py 陈太太 3            # 3 個月（從今天起算）
  python gen_license.py 陈太太 2026-12-31   # 指定到期日
激活碼格式: HKSS-到期日(YYYYMMDD)-SHA256(密鑰|到期日)前8位
密鑰: 與 generate_html.py 共用 license_secret.txt（同目錄）。
注意: 校驗屬「防君子」級——密鑰隨頁面分發，讀源碼者可自製碼；
月付模式的真正護城河是持續更新的題庫與內容。換密鑰＝舊碼全部失效。
"""
import csv
import datetime
import hashlib
import os
import sys

WS = os.path.dirname(os.path.abspath(__file__))
SECRET_PATH = os.path.join(WS, 'license_secret.txt')
LEDGER = os.path.join(WS, 'licenses_issued.csv')
MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def make_code(exp_yyyymmdd):
    mac = hashlib.sha256((open(SECRET_PATH).read().strip() + '|' + exp_yyyymmdd).encode()).hexdigest()[:8].upper()
    return 'HKSS-%s-%s' % (exp_yyyymmdd, mac)


def exp_from_months(months):
    d = datetime.date.today()
    m = d.month - 1 + months
    y = d.year + m // 12
    m = m % 12 + 1
    leap = (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0))
    day = min(d.day, MONTH_DAYS[m - 1] + (1 if (m == 2 and leap) else 0))
    return '%04d%02d%02d' % (y, m, day)


def main():
    if not os.path.exists(SECRET_PATH):
        print('錯誤: 找不到 license_secret.txt（先跑一次 generate_html.py 會自動生成）')
        sys.exit(1)
    args = sys.argv[1:]
    if len(args) >= 2:
        name, spec = args[0], args[1]
    else:
        name = input('客戶姓名/備註: ').strip()
        spec = input('月數或到期日(YYYY-MM-DD): ').strip()
    if '-' in spec:
        exp = spec.replace('-', '')
        if len(exp) != 8 or not exp.isdigit():
            print('錯誤: 到期日格式應為 YYYY-MM-DD')
            sys.exit(1)
    else:
        exp = exp_from_months(int(spec))
    code = make_code(exp)
    new_file = not os.path.exists(LEDGER)
    with open(LEDGER, 'a', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(['發出日期', '客戶', '到期日', '激活碼'])
        w.writerow([datetime.date.today().isoformat(), name, exp, code])
    print('客戶: %s' % name)
    print('到期: %s-%s-%s' % (exp[:4], exp[4:6], exp[6:8]))
    print('激活碼: %s' % code)
    print('已記錄到 licenses_issued.csv')


if __name__ == '__main__':
    main()
