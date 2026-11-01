# -*- coding: utf-8 -*-
"""单文件 HTML 学习站生成器：把 build_data.json 注入模板，输出 index_vX.Y.html（并保留 index.html 兼容副本）。
v1.1 结构：2 级导航，練習區按科目歸口
  速覽指南（中文 / 英文 / 數學 / 繁體對照 / 英文卷） ＋ 練習（中文 / 英文 / 數學） ＋ 學習進度
  練習＝中文(古詩詞) / 英文(港小生字＋詞表) / 數學(中↔英術語表·點擊打卡)
數學術語表從速覽→數學挪至練習→數學，速覽只留差異卡。
新增：詩詞默寫填空+打印、數術語打卡、進度匯出/匯入、Web Speech 朗讀、移動端響應式。
v1.21：新增授權碼月付（付費模組＝英文卷＋數學卷，其餘免費）——激活碼 HKSS-YYYYMMDD-XXXXXXXX（SHA256(密鑰|到期日)前8位），未激活時出卷區顯示鎖定面板（輸入碼解鎖，過期碼／無效碼分別提示），出卷／打印全鏈路守衛，操作列顯示「已激活至」；新增 gen_license.py 發碼工具（記錄 licenses_issued.csv）與 license_secret.txt 密鑰（首次構建自動生成）。防君子級：密鑰隨頁面分發，月付護城河＝持續更新內容。verify2.js 加授權碼斷言（鎖定面板／無效拒／過期拒／解鎖出卷／localStorage）。v1.20：修復數學卷年級 chip 切換失效——術語分類 chip 的綁定選擇器原為 #mathPracView .chip，誤把數學卷年級 chip(#mpgChips P1–P6) 也綁成術語處理器，導致點 P2–P6 仍抽 P1 題、localStorage 年級寫錯；收斂為 #mTermsView .chip 僅綁術語分類，年級 chip 不再被覆寫。verify2.js 數學卷斷言全過。v1.19：練習→數學新增「數學卷」（雙語對照·分 P1–P6）——仿編原創題庫（mc/fill/word 三型），英文題幹＋中文對照，按年級 chip 出卷＋交卷批改（應用題不計分給參考答案）＋打印含答案版；mathPracView 加 subnav 分「中↔英術語表／數學卷」。verify2.js 加數學卷斷言。v1.18：排版優化——詞彙頁（港小生字）加「展開全部／收起全部」按鈕（複用 hkCollapsed 狀態），長標題補 line-height:1.5 改善小屏折行。v1.17：港小生字（英文詞）按 P1–P6 分級分塊展示——移除年級 chip 過濾，改為六個可折疊小節（P1·一年級…P6·六年級），每節列出該年級英文詞＋中文義，帶搜索/主題/自測過濾，折疊狀態跨重渲染保留（hkCollapsed）；沿用簡繁對照式簡潔列表。verify2.js 改寫 hk 斷言（.gsec=6／每節含詞卡／首節標題含 P1 與一年級／總詞卡>300／搜索過濾）。v1.16：英文卷新增「綜合 P1–P6」分年級小節卷（每級 2 題）＋每題「🔄 換一題（本地）」與「🤖 AI 換題（接 OpenAI 兼容大模型，自填接口／密鑰，存 localStorage）」；AI 設置面板。v1.15：英文卷閱讀題庫接入教育局「中國寓言系列」——10 篇 EDB 公開英文寓言（鑿壁偷光/亡羊補牢/一飯千金/賣油翁/守株待兔/塞翁失馬/愚公移山/三人成虎/大禹治水/花木蘭）依官方英文文本改編為 read 題型（每篇 4 題含 1 道文法選擇填空），分散 P4(4)/P5(3)/P6(3)，標 src:'EDB' 來源；genEnPaper 拼接 EN_EDB 常量（不動原 EN_QBANK）；renderEnPaper/打印雙端顯示「來源：EDB」；enSrcNote 補 EDB 版權聲明。verify2.js 加 4 項斷言（EN_EDB 存在／各級含 EDB read／src 字段）。
v1.14：練習→英文新增第 5 入口「詞彙路線圖」(goalView)——①站內現有詞量統計(港小335＋B1 1465＝1800，诗词185首另計，標注入門奠基包非全量)；②一年級→中六累計詞量目標表(P1 500–800…P6 2500–3000…S6 6000–8000／衝L5 10000+，坊間基準＋來源＋EDB不公布官方詞單聲明)；③本家庭落點(2027/28 插班中一，P6→S1 銜接路線)；④背詞方法(語境閱讀／主動被動詞彙／間隔重複／聽讀／遊戲化打卡／詞根聯想，標來源性質)。enPracSub 增第5按鈕與顯隱；verify2.js 加 3 項斷言(goalView 按鈕/點擊顯示/含「1,800」與「中六」與「2,500–3,000」)。
v1.13：英文卷打印升級「一次性打印一套卷子」——①空卷時按「打印一套卷子」自動先出一套再印，無須先按「出新卷」；②卷頭增「共 N 題／總分」；③勾「含答案版」時答案獨立成頁（題卷＋答案卷＝完整一套，答案卷 page-break-before 獨立分頁）；按鈕改名「🖨 打印一套卷子」。verify2.js 加 3 項斷言（空卷自動出卷／題卷含總分／含答案版答案卷獨立成頁）。
v1.12：升中面試模塊重做——依 2026 香港升中面試公開資料大幅擴充（4 大面試形式＋10 大題型佔比表＋英文自我介紹黃金4步＋互動練習卡＋小組討論 DO/DON'T＋分類題庫＋P5→P6 時間線＋2026 名校題例＋弱項自評＋資料來源）；新增自我介紹填空練習與錄音自測按鈕；verify2.js 加 6 項斷言。
v1.11：英文卷題庫按 P1–P6 重構擴充——依香港小學英文課程進度重排年級主題（初小文法參考 GoStudy.HK、各級文法專頁參考弦月教育、題型參考香港教育圖書樣本卷/Band1試卷網/The Exam Coach SSPA P6），每級題量 10→約20，減少中英互譯、增英文語境文法/閱讀/寫作；paperView 新增「本年級常見主題」與「資料來源」面板（標坊間參考＋2026-10-31 檢索日期）。
v1.10：背單詞激勵三件套——①連續打卡火焰（localStorage 記 lastday/streak，每日自動+1，斷更歸1，hkView 頂部 motiBar 顯示🔥天數+今日目標）；②成就徽章（renderBadges 按港小詞掌握數/連續天數/主題跨度給 7 枚徽章，progressView 新增 badgeBox）；③閃卡抽查（hkView 新增 flashPanel，隨機抽詞→翻開中文→認識/不認識，認識自動標已掌握並計本輪）。
v1.9：將「英文卷·智能練習卷」从「速覽→英文卷」(guideSub) 整體遷移至「練習→英文」第四個子標籤(data-es="paper")，速覽入口移除；enPracSub 增 paper 按鈕與顯隱/自動出卷邏輯，guideSub 移除 paper 入口與數組；verify2.js 重定向相關斷言。
v1.8：英文卷打印新增「含答案版」開關（勾選後打印帶標準答案的卷：mc/填空/閱讀標註正確選項與答案，open/write 附參考範文；抬頭自動標「答案版」；空白卷/答案卷共用同一隔離打印樣式）。
v1.7：英文卷新增「🖨 打印本卷」功能（生成 A4 空白練習卷：含年級/姓名/日期抬頭＋題目與作答空位，按 P1–P6 當前年級出卷；用 body.printing-paper 類隔離打印，不影響現有默寫打印）。
v1.6：介面高級化升級（覆蓋式 CSS：靛藍+金 premium 配色、玻璃擬態導覽、卡片陰影與懸停浮起、標題裝飾條、漸層按鈕、自定滾動條、入場動畫、移動端與打印適配）；不改結構與 JS，verify 斷言不受影響。
v1.5：新增「悠閒」頂層 tab 及「單詞貪吃蛇」遊戲（funView + canvas 經典貪吃蛇，食物＝隨機港小生字，吃到看中文義，死亡後可一鍵把本局詞標為「已掌握」，連動 hProg 打卡與進度統計）；回應「用平台吸引背單詞」。
v1.4：將「英文科·卷別結構與面試（坊間整理）」模塊從「速覽→英文卷」改掛到「練習→英文」第三個子標籤「升中面試」（enPracView 內新增 ivView），撤銷 v1.3 刪除；enPracSub 增 data-es="iv" 按鈕，切換 JS 同步顯隱三視圖；verify2.js 恢復並重定向該模塊斷言至 ivView。
v1.3：刪除「英文卷」頁面下「英文科·卷別結構與面試（坊間整理）」模塊（四卷結構/自我介紹模板/常見面試題三卡片），該頁僅保留「智能練習卷」出題器；同步移除 verify2.js 綁死該模塊的斷言。
v1.2：新增「升學規劃」頂層 tab 及 5 子頁（時間線/擇校分檔/材料清單/學習路線/身份政策），內容取自 hk-placement 知識庫，逐條帶來源/性質/時效标注。
v1.1：英文卷加「智能練習卷」本地出題引擎（分 P1–P6，mc/fill/read/open/write 題型，隨機組卷＋自動批改＋本級最佳記錄，非外部 AI）；
       公開版去除真實人名（「涵涵練習」→「練習」），啟用 v1.x 遞增版本號規範。
"""
import json, os, re

WS = os.path.dirname(os.path.abspath(__file__))
DATA = open(os.path.join(WS, 'build_data.json'), encoding='utf-8').read()
# 防止 </script> 注入破坏（极端安全）
DATA = DATA.replace('</', '<\\/')
# 授權碼密鑰（v1.21）：與 gen_license.py 共用；無文件則首次自動生成
LIC_SECRET_PATH = os.path.join(WS, 'license_secret.txt')
if not os.path.exists(LIC_SECRET_PATH):
    import secrets as _secrets
    open(LIC_SECRET_PATH, 'w').write(_secrets.token_hex(16))
    print('已生成新的授權碼密鑰 license_secret.txt（舊激活碼將全部失效，請注意）')
LIC_SECRET = open(LIC_SECRET_PATH).read().strip()

TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>香港教學速覽 · 中英數 ＋ 練習</title>
<style>
  :root{--bg:#eef1f7;--card:#fff;--ink:#1b2435;--mut:#6b7280;--acc:#4f46e5;--jy:#d6452f;--line:#e7eaf2;--math:#0d9488;--acc2:#c79a3a;--grad:linear-gradient(135deg,#4f46e5 0%,#6d28d9 55%,#4338ca 100%);--gold:linear-gradient(135deg,#e7c074,#c79a3a);--shadow-sm:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.10);--shadow-md:0 6px 16px -4px rgba(16,24,40,.12),0 12px 28px -10px rgba(16,24,40,.14);--radius:16px}
  *{box-sizing:border-box}
  body{margin:0;font-family:"PingFang HK","Microsoft JhengHei","Noto Sans CJK SC",system-ui,sans-serif;background:var(--bg);color:var(--ink);line-height:1.5}
  header{background:linear-gradient(135deg,#2c7be5,#1a5fc4);color:#fff;padding:18px 20px}
  header h1{margin:0;font-size:20px}
  header p{margin:4px 0 0;font-size:12px;opacity:.9}
  nav{display:flex;gap:8px;padding:12px 16px;background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:6}
  nav button{flex:1;padding:9px;border:1px solid var(--line);background:#fff;border-radius:8px;font-size:14px;cursor:pointer;color:var(--ink)}
  nav button.on{background:var(--acc);color:#fff;border-color:var(--acc)}
  .subnav{display:flex;gap:6px;padding:8px 16px;background:#f0f4fb;border-bottom:1px solid var(--line);position:sticky;top:53px;z-index:5;flex-wrap:wrap}
  .subnav button{padding:6px 14px;border:1px solid var(--line);background:#fff;border-radius:18px;font-size:13px;cursor:pointer;color:var(--ink)}
  .subnav button.on{background:var(--math);color:#fff;border-color:var(--math)}
  .wrap{max-width:900px;margin:0 auto;padding:16px}
  .tools{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px;align-items:center}
  .chip{padding:6px 12px;border:1px solid var(--line);border-radius:20px;background:#fff;cursor:pointer;font-size:13px}
  .chip.on{background:var(--acc);color:#fff;border-color:var(--acc)}
  input[type=search],select{padding:7px 10px;border:1px solid var(--line);border-radius:8px;font-size:14px}
  .btn{padding:7px 14px;border:1px solid var(--line);background:#fff;border-radius:8px;font-size:13px;cursor:pointer}
  .btn.on{background:var(--math);color:#fff;border-color:var(--math)}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
  .pcard{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;cursor:pointer;transition:.1s}
  .pcard:hover{box-shadow:0 2px 8px rgba(0,0,0,.08);transform:translateY(-1px)}
  .pcard .t{font-size:16px;font-weight:700}
  .pcard .m{font-size:12px;color:var(--mut);margin-top:3px}
  .tag{display:inline-block;font-size:10px;padding:1px 6px;border-radius:6px;background:#eef4ff;color:var(--acc);margin-left:4px}
  .tag.b{background:#fdecea;color:var(--jy)}
  /* 详情弹层 */
  .mask{position:fixed;inset:0;background:rgba(0,0,0,.4);display:none;align-items:flex-start;justify-content:center;overflow:auto;z-index:20;padding:24px 12px}
  .mask.show{display:flex}
  .modal{background:#fff;border-radius:14px;max-width:640px;width:100%;padding:22px;position:relative}
  .modal .x{position:absolute;top:10px;right:14px;font-size:22px;cursor:pointer;color:var(--mut)}
  .modal h2{margin:0 0 2px;font-size:22px}
  .modal .sub{color:var(--mut);font-size:13px;margin-bottom:14px}
  .line{display:flex;flex-wrap:wrap;justify-content:center;gap:2px 1px;margin:10px 0}
  .ch{display:flex;flex-direction:column;align-items:center;min-width:1.4em}
  .ch .py{font-size:10px;color:#777;height:13px;line-height:13px}
  .ch .han{font-size:24px;font-weight:600}
  .ch .jy{font-size:9px;color:var(--jy);height:12px;line-height:12px}
  .hidepy .ch .py,.hidejy .ch .jy{visibility:hidden}
  .para{background:#f4f7ff;border-left:3px solid var(--acc);padding:10px 12px;border-radius:6px;font-size:14px;color:#444;margin:12px 0}
  .acts{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px;align-items:center}
  .acts button{padding:8px 14px;border-radius:8px;border:1px solid var(--line);background:#fff;cursor:pointer;font-size:14px}
  .acts .done{background:#e8f7ee;color:#1a8a4a;border-color:#bfe8cd}
  .acts .wdone{background:#fff4e5;color:#c4761a;border-color:#f0d9b0}
  .toggles{display:flex;gap:14px;font-size:13px;color:var(--mut);margin-bottom:6px}
  /* 词表 */
  .vcard{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin-bottom:10px}
  .vcard .w{font-size:18px;font-weight:700}
  .vcard .ph{color:var(--mut);font-size:13px;margin-left:8px}
  .vcard .zh{font-size:14px;margin-top:4px}
  .vcard .tp{font-size:11px;color:var(--acc);margin-top:4px}
  .vcard.hidezh .zh{filter:blur(5px);user-select:none}
  /* 速览 */
  .gtitle{font-size:18px;margin:6px 0 4px}
  .folk{font-size:11px;color:#c4761a;background:#fff4e5;padding:2px 9px;border-radius:10px;display:inline-block;margin:0 0 12px}
  .gcard{background:#fff;border:1px solid var(--line);border-left:4px solid var(--math);border-radius:10px;padding:14px 16px;margin-bottom:12px}
  .gcard h3{margin:0 0 6px;font-size:16px}
  .gcard p{margin:6px 0;font-size:14px;color:#444;line-height:1.65}
  .gcard .tip{background:#fff7e6;border-radius:6px;padding:8px 10px;font-size:13px;color:#8a5a00;margin-top:8px}
  /* 数术语表 */
  .mtable{width:100%;border-collapse:collapse;background:#fff;font-size:14px;margin-top:6px}
  .mtable th,.mtable td{border:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}
  .mtable th{background:#eafaf4;font-weight:700;color:#0f7a63}
  .mtable tr:nth-child(even) td{background:#fafdfc}
  .mtable td.en{font-weight:600;color:#0f7a63}
  /* 进度 */
  .stat{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:16px}
  .stat .b{flex:1;min-width:140px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px;text-align:center}
  .stat .n{font-size:28px;font-weight:800;color:var(--acc)}
  .stat .l{font-size:12px;color:var(--mut)}
  .sec-title{font-size:15px;font-weight:700;margin:18px 0 8px}
  .clr{background:#fdecea;color:#c0392b;border:1px solid #f0c9c4;padding:8px 14px;border-radius:8px;cursor:pointer;font-size:13px}
  footer{text-align:center;color:var(--mut);font-size:11px;padding:20px;line-height:1.7}
  @media print{
    nav,.subnav,header .tools,.toggles,.acts,.x{display:none!important}
    body{background:#fff}
    .wrap{max-width:none}
    .pcard,.vcard{page-break-inside:avoid;border:none;border-bottom:1px solid #ccc;border-radius:0;padding:8px 0}
    .modal{box-shadow:none;max-width:none}
    .mtable{font-size:11px}
    .mtable th,.mtable td{padding:3px 5px}
    #guideView,#practiceView,#progressView{display:block!important}
    .snake-wrap{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
    #snakeCanvas{background:#0f2a22;border-radius:12px;max-width:100%;touch-action:none}
    .snake-side{flex:1;min-width:220px}
    .snake-stat{font-size:14px;margin-bottom:8px}
    .snake-word{font-size:18px;font-weight:700;color:#0f7a63;min-height:54px;padding:8px 10px;background:#eafaf4;border-radius:8px;margin-bottom:10px;line-height:1.4}
    .snake-word b{color:#b8541b}
    .snake-pad{margin-top:12px;display:flex;flex-direction:column;align-items:center;gap:6px}
    .snake-pad>div{display:flex;gap:6px}
    .spad{width:52px;height:46px;font-size:18px;border:1px solid #cfe3da;background:#fff;border-radius:10px;cursor:pointer}
    .spad:active{background:#eafaf4}
    .snake-tip{font-size:12px;color:#888;margin-top:10px}
    .gsec{display:block!important;page-break-inside:avoid}
  }
  /* 默写填空 */
  .han.blank{color:transparent;border-bottom:2px solid #888;padding:0 1px}
  .han.blank.reveal{color:var(--ink);border-bottom:none}
  /* 数术语掌握 */
  .mtable tr.mrow{cursor:pointer}
  .mtable tr.done td{background:#e8f7ee!important}
  .mtable tr.done td.en{color:#1a8a4a}
  .mini{font-size:11px;padding:1px 6px;border:1px solid var(--line);border-radius:6px;background:#f4f7ff;cursor:pointer;color:var(--acc)}
  /* 繁体对照 */
  .ftrow{display:flex;gap:10px;align-items:center;font-size:15px;padding:7px 2px;border-bottom:1px solid var(--line)}
  .ftrow .s{color:#888;min-width:2em;text-align:center}
  .ftrow .ar{color:#bbb}
  .ftrow .f{font-weight:700;font-size:22px;color:var(--jy)}
  /* 英文卷 */
  .paper{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-bottom:12px}
  .paper h3{margin:0 0 6px;font-size:16px}
  .paper ol{margin:6px 0;padding-left:20px;font-size:14px;color:#444;line-height:1.7}
  .paper .tmpl{background:#f4f7ff;border-left:3px solid var(--acc);padding:10px 12px;border-radius:6px;font-size:13px;white-space:pre-wrap;line-height:1.6}
  /* 英文卷·智能出题 */
  .pg-chips{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0 4px}
  .pg-chips .chip.on{background:var(--acc);color:#fff;border-color:var(--acc)}
  .enpaper-actions{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0 14px}
  .enpaper-actions .btn{padding:8px 16px;font-size:14px}
  .print-ans-toggle{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:#475069;cursor:pointer;user-select:none;padding:6px 10px;border:1px solid var(--line);border-radius:10px;background:#fff;box-shadow:var(--shadow-sm)}
  .print-ans-toggle input{width:16px;height:16px;accent-color:var(--acc);cursor:pointer}
  .enpaper-stat{font-size:13px;color:var(--mut);margin-left:auto}
  .qcard{background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:10px}
  .qcard .qhead{font-size:14px}
  .qcard .qn{font-weight:700;color:var(--acc)}
  .qcard .qtype{font-size:11px;color:var(--mut);margin-left:6px}
  .qcard .qtext{font-size:15px;margin:6px 0}
  .qpass{background:#fafbff;border:1px dashed var(--line);border-radius:8px;padding:10px 12px;font-size:14px;line-height:1.7;margin:6px 0;color:#333}
  .qopts{display:flex;flex-direction:column;gap:6px;margin:8px 0}
  .qopt{display:flex;align-items:center;gap:8px;padding:7px 10px;border:1px solid var(--line);border-radius:8px;cursor:pointer;font-size:14px}
  .qopt:hover{background:#f4f7ff}
  .qopt input{margin:0}
  .qopt.correct{background:#e8f7ee;border-color:#bfe8cd}
  .qopt.wrong{background:#fdecea;border-color:#f0c9c4}
  .qfill{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:8px;font-size:15px;box-sizing:border-box}
  .qfill.correct{border-color:#1a8a4a;background:#e8f7ee}
  .qfill.wrong{border-color:var(--jy);background:#fdecea}
  .qans{font-size:13px;margin-top:6px}
  .qans .ok{color:#1a8a4a;font-weight:700}
  .qans .no{color:var(--jy);font-weight:700}
  .qtip{font-size:12px;color:var(--mut);margin-top:4px}
  .qwrite{background:#f4f7ff;border-left:3px solid var(--acc);padding:10px 12px;border-radius:6px;font-size:13px;white-space:pre-wrap;line-height:1.6;margin-top:6px}
  .qwrite textarea{width:100%;min-height:80px;margin-top:6px;padding:8px;border:1px solid var(--line);border-radius:8px;font-size:14px;font-family:inherit;box-sizing:border-box}
  .qtot{font-size:16px;font-weight:700;margin:12px 0 6px}
  .qbar{height:10px;background:#eef4ff;border-radius:6px;overflow:hidden;margin:6px 0 2px}
  .qbar > i{display:block;height:100%;background:var(--acc)}
  .listen-btn{cursor:pointer;border:none;background:none;font-size:15px;padding:0 4px}
  .scroll-x{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:10px 0}
  .scroll-x .mtable{min-width:780px}
  .src{font-size:11px;color:#8a8f99;margin:6px 2px 16px;line-height:1.5;border-top:1px dashed #e2e6ee;padding-top:6px}
  .gcard.warn{border-left:3px solid #e0a200;background:#fff8e8}
  .gcard.warn h3{color:#9a6b00}
  .tier1{color:#c0392b;font-weight:600}.tier2{color:#2c7a3f;font-weight:600}.tier3{color:#2b6cb0;font-weight:600}
  /* 响应式（手机） */
  @media screen and (max-width:640px){
    header h1{font-size:17px}
    header p{font-size:11px}
    nav{flex-wrap:wrap}
    nav button{flex:1 1 30%}
    .subnav{position:static}
    .wrap{padding:12px}
    .grid{grid-template-columns:repeat(auto-fill,minmax(116px,1fr))}
    .tools{flex-direction:column;align-items:stretch}
    .tools .chip,.tools input[type=search],.tools select{flex:1;width:100%}
    .stat .b{min-width:100%}
    .mtable{font-size:12px}
    .ch .han{font-size:20px}
    .modal{padding:16px}
    .stat{flex-direction:column}
  }
/* ========== v1.6 高級化介面升級（覆蓋層：不改結構與 JS） ========== */
body{background:radial-gradient(1100px 560px at 85% -8%,rgba(79,70,229,.10),transparent 60%),radial-gradient(900px 480px at -8% 8%,rgba(13,148,136,.08),transparent 55%),#eef1f7;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;color:var(--ink)}
header{position:relative;overflow:hidden;text-align:center;background:linear-gradient(135deg,#312e81 0%,#4f46e5 50%,#4338ca 100%);color:#fff;padding:40px 24px 34px}
header::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.5;background-image:radial-gradient(circle at 18% 28%,rgba(255,255,255,.14) 0 2px,transparent 3px),radial-gradient(circle at 78% 62%,rgba(255,255,255,.09) 0 2px,transparent 3px);background-size:48px 48px,62px 62px}
header::after{content:"";position:absolute;left:0;right:0;bottom:0;height:3px;background:var(--gold)}
header h1{margin:0;font-size:30px;font-weight:800;letter-spacing:.5px;position:relative;text-shadow:0 2px 14px rgba(0,0,0,.28)}
header p{margin:12px auto 0;font-size:13.5px;max-width:660px;opacity:.92;position:relative;line-height:1.7}
nav{display:flex;gap:6px;justify-content:center;padding:9px;margin:0 14px;background:rgba(255,255,255,.72);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.55);border-radius:18px;box-shadow:var(--shadow-md);position:sticky;top:0;z-index:6}
nav button{flex:1;padding:11px 8px;border:1px solid transparent;background:transparent;border-radius:12px;font-size:14px;font-weight:600;cursor:pointer;color:#475069;transition:.2s}
nav button:hover{background:rgba(79,70,229,.08);color:var(--acc)}
nav button.on{background:var(--grad);color:#fff;box-shadow:0 8px 18px -6px rgba(79,70,229,.55)}
.subnav{display:flex;gap:6px;padding:8px 14px;justify-content:center;flex-wrap:wrap;background:rgba(255,255,255,.66);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--line);position:sticky;top:60px;z-index:5}
.subnav button{padding:7px 16px;border:1px solid var(--line);background:#fff;border-radius:20px;font-size:13px;font-weight:600;cursor:pointer;color:#475069;transition:.18s}
.subnav button:hover{border-color:var(--math);color:var(--math)}
.subnav button.on{background:var(--math);color:#fff;border-color:var(--math);box-shadow:0 6px 14px -4px rgba(13,148,136,.5)}
.wrap{max-width:960px;margin:0 auto;padding:26px 18px 44px;animation:fadeUp .45s ease both}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.tools{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:18px;align-items:center}
.chip{padding:8px 14px;border:1px solid var(--line);border-radius:22px;background:#fff;cursor:pointer;font-size:13px;font-weight:600;color:#475069;transition:.18s;box-shadow:var(--shadow-sm)}
.chip:hover{border-color:var(--acc);color:var(--acc);transform:translateY(-1px)}
.chip.on{background:var(--grad);color:#fff;border-color:transparent;box-shadow:0 8px 18px -8px rgba(79,70,229,.6)}
input[type=search],select{padding:9px 12px;border:1px solid var(--line);border-radius:10px;font-size:14px;background:#fff;box-shadow:var(--shadow-sm);color:var(--ink)}
.btn{padding:9px 16px;border:1px solid var(--line);background:#fff;border-radius:10px;font-size:13px;font-weight:600;cursor:pointer;color:#475069;box-shadow:var(--shadow-sm);transition:.18s}
.btn:hover{transform:translateY(-1px);border-color:var(--acc);color:var(--acc)}
.btn.on{background:var(--math);color:#fff;border-color:transparent;box-shadow:0 8px 18px -8px rgba(13,148,136,.55)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(162px,1fr));gap:14px;margin-top:6px}
.pcard{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:16px;cursor:pointer;transition:.2s;box-shadow:var(--shadow-sm);position:relative;overflow:hidden}
.pcard::before{content:"";position:absolute;left:0;top:0;height:3px;width:100%;background:var(--grad);opacity:0;transition:.2s}
.pcard:hover{box-shadow:var(--shadow-md);transform:translateY(-3px);border-color:transparent}
.pcard:hover::before{opacity:1}
.pcard .t{font-size:17px;font-weight:800;letter-spacing:.3px}
.pcard .m{font-size:12px;color:var(--mut);margin-top:4px;line-height:1.5}
.tag{display:inline-block;font-size:10px;padding:2px 7px;border-radius:7px;background:#eef0fe;color:var(--acc);margin-left:4px;font-weight:600}
.tag.b{background:#fdecec;color:var(--jy)}
.gtitle{font-size:20px;font-weight:800;margin:4px 0 8px;padding-left:15px;position:relative;color:var(--ink);letter-spacing:.3px}
.gtitle::before{content:"";position:absolute;left:0;top:4px;bottom:4px;width:5px;border-radius:3px;background:var(--grad)}
.folk{font-size:11px;color:#8a6d1f;background:linear-gradient(135deg,#fdf3d8,#f7e6b8);padding:3px 11px;border-radius:12px;display:inline-block;margin:0 0 14px;font-weight:600;border:1px solid #ecd9a0}
.gcard{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:18px 20px;margin-bottom:14px;box-shadow:var(--shadow-sm);transition:.2s;border-left:4px solid var(--math)}
.gcard:hover{box-shadow:var(--shadow-md);transform:translateY(-2px)}
.gcard h3{margin:0 0 8px;font-size:16.5px;font-weight:800}
.gcard p{margin:6px 0;font-size:14px;color:#475569;line-height:1.78}
.gcard .tip{background:linear-gradient(135deg,#fff7e6,#fff1d6);border-radius:10px;padding:10px 13px;font-size:13px;color:#8a5a00;margin-top:10px;border:1px solid #f3e2bb}
.gcard.warn{border-left:4px solid #e0a200;background:#fffdf6}
.gcard.warn h3{color:#9a6b00}
.vcard{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px;margin-bottom:12px;box-shadow:var(--shadow-sm);transition:.2s}
.vcard:hover{box-shadow:var(--shadow-md);transform:translateY(-2px)}
.vcard .w{font-size:18px;font-weight:800}
.vcard .zh{font-size:14px;margin-top:5px;color:#475569}
.vcard .tp{font-size:11px;color:var(--acc);margin-top:5px;font-weight:600}
.paper{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:18px 20px;margin-bottom:14px;box-shadow:var(--shadow-sm);transition:.2s}
.paper:hover{box-shadow:var(--shadow-md)}
.paper h3{margin:0 0 8px;font-size:16.5px;font-weight:800}
.paper .tmpl{background:linear-gradient(135deg,#f4f6ff,#eef0fe);border-left:3px solid var(--acc);padding:12px 14px;border-radius:8px;font-size:13px;white-space:pre-wrap;line-height:1.7}
.qcard{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px;margin-bottom:12px;box-shadow:var(--shadow-sm);transition:.2s}
.qcard:hover{box-shadow:var(--shadow-md)}
.qopt{border:1px solid var(--line);border-radius:10px;padding:9px 12px;font-size:14px;transition:.15s}
.qopt:hover{background:#f4f6ff;border-color:var(--acc)}
.qfill,.qwrite textarea{border:1px solid var(--line);border-radius:10px;padding:9px 12px;font-size:15px;transition:.15s}
.qfill:focus,.qwrite textarea:focus{outline:none;border-color:var(--acc);box-shadow:0 0 0 3px rgba(79,70,229,.15)}
.mtable th{background:linear-gradient(135deg,#e6fbf5,#d8f6ec);font-weight:700;color:#0b7a68}
.mtable tr:hover td{background:#f1fbf8}
.stat .b{flex:1;min-width:150px;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:18px 16px;text-align:center;box-shadow:var(--shadow-sm);position:relative;overflow:hidden}
.stat .b::after{content:"";position:absolute;right:-22px;top:-22px;width:74px;height:74px;border-radius:50%;background:var(--grad);opacity:.08}
.stat .n{font-size:30px;font-weight:800;color:var(--acc)}
.stat .l{font-size:12px;color:var(--mut);margin-top:4px}
.sec-title{font-size:16px;font-weight:800;margin:18px 0 10px;color:var(--ink);line-height:1.5}
.modal{background:#fff;border-radius:18px;max-width:640px;width:100%;padding:26px;position:relative;box-shadow:0 24px 60px -12px rgba(16,24,40,.35)}
.modal .x{position:absolute;top:12px;right:14px;font-size:22px;cursor:pointer;color:var(--mut);width:30px;height:30px;line-height:30px;text-align:center;border-radius:50%;transition:.15s}
.modal .x:hover{background:#f1f3f9;color:var(--ink)}
.acts button{padding:9px 15px;border-radius:10px;border:1px solid var(--line);background:#fff;cursor:pointer;font-size:14px;font-weight:600;color:#475069;transition:.18s;box-shadow:var(--shadow-sm)}
.acts button:hover{transform:translateY(-1px);border-color:var(--acc);color:var(--acc)}
.acts .done{background:#e8f7ee;color:#1a8a4a;border-color:#bfe8cd}
.acts .wdone{background:#fff4e5;color:#c4761a;border-color:#f0d9b0}
.ftrow{display:flex;gap:10px;align-items:center;font-size:15px;padding:9px 4px;border-bottom:1px solid var(--line)}
.ftrow .f{font-weight:800;font-size:22px;color:var(--jy)}
.src{font-size:11px;color:#8a8f99;margin:6px 2px 16px;line-height:1.6;border-top:1px dashed #e2e6ee;padding-top:8px}
footer{text-align:center;color:var(--mut);font-size:11px;padding:24px;line-height:1.8;background:rgba(255,255,255,.5);border-top:1px solid var(--line)}
::-webkit-scrollbar{width:11px;height:11px}
::-webkit-scrollbar-thumb{background:#c7cdda;border-radius:8px;border:3px solid #eef1f7;background-clip:padding-box}
::-webkit-scrollbar-thumb:hover{background:#aab2c4}
.en-print{display:none}
.en-print .eps-head{margin-bottom:16px;text-align:center}
.en-print .eps-title{font-size:22px;font-weight:800;letter-spacing:.5px}
.en-print .eps-meta{font-size:14px;margin-top:8px;color:#333}
.en-print .eps-q{margin-bottom:16px;page-break-inside:avoid}
.en-print .eps-qh{font-weight:700;font-size:15px;margin-bottom:4px}
.en-print .eps-text{font-size:14px;margin:4px 0;line-height:1.6}
.en-print .eps-pass{font-size:13px;background:#f4f7ff;padding:8px 10px;border-radius:6px;margin:4px 0;line-height:1.7}
.en-print .eps-opts{font-size:14px;margin:4px 0;line-height:1.8}
.en-print .eps-ans{font-size:14px;margin-top:6px;color:#444}
.en-print .eps-tip{font-size:12px;color:#888;margin:4px 0}
.en-print .eps-aksheet{margin-top:8px;page-break-before:always;padding-top:6px;border-top:2px solid #1b2435}
.en-print .eps-ak-title{font-size:18px;font-weight:800;text-align:center;margin:10px 0 16px;letter-spacing:.5px}
.en-print .eps-ak-row{font-size:14px;line-height:1.9;margin:6px 0;padding-bottom:4px;border-bottom:1px dotted #ccc}
@media screen and (max-width:640px){
  header{padding:30px 16px 26px}
  header h1{font-size:23px}
  nav{margin:0;padding:8px;gap:4px}
  nav button{flex:1 1 30%;padding:9px 4px;font-size:13px}
  .subnav{top:54px;padding:8px 8px}
  .gtitle{font-size:18px}
  .grid{grid-template-columns:repeat(auto-fill,minmax(118px,1fr))}
  .wrap{padding:18px 12px 36px}
}
@media print{
  header{background:#fff!important;color:#1b2435!important;padding:14px}
  header h1,header p{color:#1b2435!important;text-shadow:none!important}
  header::before,header::after{display:none!important}
  nav,.subnav{display:none!important}
  body.printing-paper nav,body.printing-paper .subnav,body.printing-paper header,body.printing-paper #guideView,body.printing-paper #practiceView,body.printing-paper #progressView,body.printing-paper #funView,body.printing-paper #mask,body.printing-paper footer,body.printing-paper .folk{display:none!important}
  body.printing-paper #enPrintSheet,body.printing-paper #mathPrintSheet{display:block!important;position:static;width:100%}
  @page{margin:14mm}
}
/* v1.10 背單詞激勵樣式 */
.moti{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:linear-gradient(135deg,#fff7ed,#fff1f0);border:1px solid #ffd9c2;border-radius:14px;padding:12px 16px;margin-bottom:14px;box-shadow:var(--shadow-sm)}
.moti .flame{font-size:26px;transition:.3s}
.moti .moti-num{font-size:24px;font-weight:800;color:#e8590c}
.moti .moti-label{font-size:14px;color:#7a4a2b;font-weight:600}
.moti .moti-goal{font-size:12.5px;color:#9a6b4a;margin-left:auto;background:#fff;border:1px solid #ffe0cc;padding:5px 10px;border-radius:10px}
.flash{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:22px 18px;margin-top:14px;box-shadow:var(--shadow-sm);text-align:center}
.flash-card{font-size:34px;font-weight:800;letter-spacing:1px;color:var(--acc);min-height:44px}
.flash-zh{font-size:20px;font-weight:700;color:#b8541b;margin-top:8px;min-height:26px}
.flash-acts{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:14px}
.flash-stat{font-size:13px;color:var(--mut);margin-top:12px}
.badges{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:12px;margin-bottom:18px}
.badge{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 8px;text-align:center;box-shadow:var(--shadow-sm);transition:.2s}
.badge:hover{transform:translateY(-2px);box-shadow:var(--shadow-md)}
.badge.off{filter:grayscale(1);opacity:.45}
.badge .bi{font-size:30px}
.badge .bn{font-size:13px;font-weight:800;margin-top:4px}
.badge .bd{font-size:11px;color:var(--mut);margin-top:3px;line-height:1.4}
  .en-grade-topic{font-size:12.5px;color:#3f5a4a;margin:4px 0 12px;line-height:1.95}
  .en-grade-topic .gtag{display:inline-block;background:#eef4ff;border:1px solid #cdddff;color:#2a4d8f;padding:2px 10px;border-radius:11px;margin:0 6px 5px 0;font-weight:600}
  .en-src-note{font-size:11.5px;color:#6b6b6b;background:#f6f6f6;border:1px dashed #cfcfcf;border-radius:10px;padding:10px 12px;margin-top:16px;line-height:1.7}
  .en-src-note a{color:#2a8a5a;font-weight:600;text-decoration:none}
  .en-src-note a:hover{text-decoration:underline}
.qsrc{font-size:12px;color:#9a7b3f;margin:4px 0 0;font-style:italic}
.eps-src{font-size:11px;color:#9a7b3f;margin:2px 0 6px;font-style:italic}

  .hint{font-size:12px;color:var(--mut);margin:8px 0 0;line-height:1.6}
  .iv-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:6px}
  .iv-grid .cell{background:#f6f9ff;border:1px solid var(--line);border-radius:9px;padding:10px 12px}
  .iv-grid .cell h4{margin:0 0 5px;font-size:14px;color:var(--acc)}
  .iv-grid .cell p{margin:0;font-size:12.5px;color:#444;line-height:1.6}
  .iv-tbl{width:100%;border-collapse:collapse;font-size:12.5px;margin-top:6px}
  .iv-tbl th,.iv-tbl td{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}
  .iv-tbl th{background:#eef2ff;font-weight:700;color:#2a3a6a}
  .iv-build{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:8px}
  .iv-build-in{display:flex;flex-direction:column;gap:7px}
  .iv-build-in label{font-size:12.5px;color:#444;display:flex;flex-direction:column;gap:3px}
  .iv-build-in input{padding:6px 9px;border:1px solid var(--line);border-radius:7px;font-size:13px}
  .iv-build-out{display:flex;flex-direction:column;gap:8px}
  .iv-dodont{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:6px}
  .iv-do,.iv-dont{border-radius:10px;padding:11px 13px}
  .iv-do{background:#f1faf3;border:1px solid #bfe6c8}
  .iv-do h4{color:#1a8a4a;margin:0 0 6px;font-size:14px}
  .iv-dont{background:#fdf2f2;border:1px solid #f0c0c0}
  .iv-dont h4{color:#c0392b;margin:0 0 6px;font-size:14px}
  .iv-do ul,.iv-dont ul{margin:0;padding-left:18px;font-size:12.5px;line-height:1.7}
  @media(max-width:560px){.iv-grid,.iv-build,.iv-dodont{grid-template-columns:1fr}}
  .qcard .qhead{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
  .qsec{margin:16px 0 8px;font-weight:700;font-size:15px;color:#2b2b6b;border-left:4px solid var(--accent,#4f46e5);background:rgba(79,70,229,.07);border-radius:0 6px 6px 0;padding:7px 12px}
  .qswap{margin-left:auto;display:flex;gap:6px}
  .mini{font-size:12px;line-height:1;padding:4px 9px;border:1px solid var(--accent,#4f46e5);background:#fff;color:var(--accent,#4f46e5);border-radius:14px;cursor:pointer}
  .mini.ai{background:var(--accent,#4f46e5);color:#fff;border-color:var(--accent,#4f46e5)}
  .mini:disabled{opacity:.5;cursor:default}
  .ai-cfg{margin:12px 0;border:1px solid #e3e3ef;border-radius:10px;background:#fafaff;padding:10px 14px}
  .ai-cfg summary{cursor:pointer;font-weight:600;color:#2b2b6b}
  .ai-cfg-body label{display:block;font-size:13px;margin-top:8px;color:#444}
  .ai-cfg-body input{width:100%;max-width:440px;padding:7px 9px;border:1px solid #ccc;border-radius:6px;margin-top:3px;font-size:13px}
  .ai-cfg-actions{margin-top:10px;display:flex;gap:8px;align-items:center}
  .ai-cfg-actions .btn{font-size:13px;padding:5px 12px}
  .eps-sec{font-weight:700;margin:12px 0 5px;color:#2b2b6b;page-break-after:avoid}
  .gsec{border:1px solid var(--line);border-radius:10px;margin:12px 0;overflow:hidden;background:var(--card)}
  .gsec-h{list-style:none;cursor:pointer;display:flex;align-items:center;gap:10px;padding:11px 14px;background:rgba(79,70,229,.08);font-weight:700;color:#2b2b6b;border-left:4px solid var(--accent,#4f46e5)}
  .gsec-h::-webkit-details-marker{display:none}
  .gsec-h::after{content:'▾';margin-left:auto;font-size:12px;color:#8a8aa0}
  .gsec[open]>.gsec-h::after{content:'▴'}
  .gcode{display:inline-block;min-width:34px;text-align:center;background:var(--accent,#4f46e5);color:#fff;border-radius:6px;padding:2px 6px;font-size:13px}
  .glabel{font-size:15px}
  .gcount{margin-left:8px;font-size:12px;color:#8a8aa0;font-weight:600}
  .gsec-body{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;padding:12px}
  .gsec-body .vcard{margin-bottom:0}
  .ok{color:#1a8a4a;font-weight:700}
  .hk-actions{display:flex;gap:6px;align-self:center}
  .qzh{font-size:12px;color:#6b7280;margin:2px 0 6px;line-height:1.5}
  .qopt .qzh{display:inline}
  .en-print .qzh{font-size:12px;color:#555;margin:2px 0 6px}
  .hk-actions button{font-size:12px;line-height:1;padding:5px 11px;border:1px solid var(--accent,#4f46e5);background:#fff;color:var(--accent,#4f46e5);border-radius:14px;cursor:pointer;transition:.15s}
  .hk-actions button:hover{background:var(--accent,#4f46e5);color:#fff}
/* ---- v1.21 授權碼鎖定面板 ---- */
.lic-lock{display:none;padding:4px 2px}
#paperView.locked>*:not(.lic-lock),#mathPaperView.locked>*:not(.lic-lock){display:none!important}
#paperView.locked .lic-lock,#mathPaperView.locked .lic-lock{display:block}
.lic-row{display:flex;gap:8px;margin:10px 0 6px;flex-wrap:wrap}
.lic-input{flex:1;min-width:220px;padding:9px 12px;border:1.5px solid var(--acc,#4f46e5);border-radius:10px;font-size:14px}
.lic-msg{color:#c0392b;font-size:13px;min-height:18px}
.lic-tip{font-size:12px;color:var(--mut,#8a8aa0)}
</style>
</head>
<body>
<header>
  <h1>香港教學速覽 · 中英數</h1>
  <p>內地家庭快速了解並跟上香港教學（中文·英文·數學）＋ 練習打卡 · 數據本地保存，不上傳 · 公開版 v1.21</p>
</header>
<nav>
  <button data-tab="guide" class="on">速覽指南</button>
  <button data-tab="plan">升學規劃</button>
  <button data-tab="practice">練習</button>
  <button data-tab="progress">學習進度</button>
  <button data-tab="fun">悠閒</button>
</nav>
<div class="subnav" id="guideSub">
  <button data-sub="cn" class="on">中文</button>
  <button data-sub="en">英文</button>
  <button data-sub="math">數學</button>
  <button data-sub="ft">繁體對照</button>
</div>
<div class="subnav" id="practiceSub" style="display:none">
  <button data-sub="cn" class="on">中文</button>
  <button data-sub="en">英文</button>
  <button data-sub="math">數學</button>
</div>

<!-- ============ 速覽指南 ============ -->
<div id="guideView">
  <!-- 中文 -->
  <div class="wrap gsec" id="cnView">
    <div class="gtitle">中文科 · 內地 vs 香港 速覽</div>
    <span class="folk">坊間整理，以香港教育局／課本為準</span>
    <div class="gcard">
      <h3>① 文字：繁體字是頭半年最大門檻</h3>
      <p>香港學校用<strong>繁體字（正體字）</strong>教學與作答；內地用簡體字。插班頭半年最痛的是「認繁、寫繁」。</p>
      <div class="tip">建議：每天 15–20 分鐘繁體字書寫＋閱讀，先過常用字，再過課本生詞。古詩詞練習見「練習 → 中文」。</div>
    </div>
    <div class="gcard">
      <h3>② 標點符號與引號</h3>
      <p>香港用全角「、，。」及書名號《》；引號用「「」『』」。內地用「，。」及「""」。作文易因標點格式扣分。</p>
      <div class="tip">重點糾：香港句號是「。」不是「.」；引號方向與內地相反。</div>
    </div>
    <div class="gcard">
      <h3>③ 文言文與古詩詞</h3>
      <p>香港 DSE 中文科必考文言文與古詩詞，小學已接觸；內地小學古詩文量大，但系統文言教學多在初中。</p>
      <div class="tip">必背古詩詞見「練習 → 中文」標籤（繁體＋拼音＋粵拼）。</div>
    </div>
    <div class="gcard">
      <h3>④ 聆聽與說話（口語）</h3>
      <p>香港中文科設<strong>獨立聆聽卷</strong>與<strong>說話卷</strong>（口語溝通／朗讀）；內地中考有聽力但說話考查較少。</p>
    </div>
    <div class="gcard">
      <h3>⑤ 寫作：實用文為主</h3>
      <p>香港寫作重<strong>實用文</strong>（書信、建議書、演講辭、報告）；內地重記敘／議論文。格式錯就掉分。</p>
    </div>
  </div>
  <!-- 英文 -->
  <div class="wrap gsec" id="enView" style="display:none">
    <div class="gtitle">英文科 · 內地 vs 香港 速覽</div>
    <span class="folk">坊間整理，以香港教育局／課本為準</span>
    <div class="gcard">
      <h3>① 教學語言：英文是「教學語言」</h3>
      <p>香港小學起大量英文授課（尤其英中／直資）；英文是學科載體而非純外語。內地英文是外語科目。</p>
      <div class="tip">差距不在「會不會」，在「用英文學其他科」的閱讀與聽課量。</div>
    </div>
    <div class="gcard">
      <h3>② 考評結構：四卷制</h3>
      <p>香港英文科分 <strong>Reading / Writing / Listening / Speaking</strong> 四卷（小學 TSA、中學 DSE）；內地中考英語含聽力＋筆試，口語比重較低。</p>
    </div>
    <div class="gcard">
      <h3>③ 詞彙量差距</h3>
      <p>Band 1 英中對詞彙與閱讀量要求明顯高於內地同齡。→ 見「練習 → 詞表」。</p>
    </div>
    <div class="gcard">
      <h3>④ 拼讀：Phonics vs 音標</h3>
      <p>香港小學重 <strong>Phonics 自然拼讀</strong>；內地多教國際音標（IPA）。</p>
    </div>
    <div class="gcard">
      <h3>⑤ 寫作：重格式</h3>
      <p>香港重格式寫作（letter / email / report / story）；內地重命題作文。→ 學術英文路線見專文。</p>
    </div>
  </div>
  <!-- 數學 -->
  <div class="wrap gsec" id="mathView" style="display:none">
    <div class="gtitle">數學科 · 內地 vs 香港 速覽</div>
    <span class="folk">坊間整理，術語以香港課本／考評局用語為準</span>
    <div class="gcard">
      <h3>最大痛點：數學用英文教</h3>
      <p>香港英中數學多以<strong>英文出題與作答</strong>。術語聽不懂＝題目看不懂。→ 背熟術語表（見「練習 → 數學」）是跟上第一步。</p>
    </div>
    <div class="gcard">
      <h3>進度差異（坊間觀察）</h3>
      <p>香港小學較早接觸<strong>統計／數據處理／概率</strong>；內地<strong>代數與幾何</strong>的深度與提早程度更高。插班時兩邊「已學／未學」章節常錯位，需按學校進度補。</p>
    </div>
    <div class="gcard">
      <h3>題目描述方式</h3>
      <p>符號（× ÷ ( )）與內地基本一致，但英文題目用句式描述運算，e.g. <em>"the product of a and b"</em>（a 與 b 的積）、<em>"increased by"</em>（增加）。</p>
      <div class="tip">術語表見「練習 → 數學」，可按分類篩選、搜尋、打印 A4 背诵。</div>
    </div>
  </div>
  <!-- 繁體對照 -->
  <div class="wrap gsec" id="ftView" style="display:none">
    <div class="gtitle">繁體字 · 簡→繁 高頻對照</div>
    <span class="folk">常用字對照，以香港課本用字為準；一簡對多繁者（如 发→發/髮、里→裡/裏）須按詞義選</span>
    <div class="tools">
      <input type="search" id="ftSearch" placeholder="搜簡體字，如 国 / 学">
    </div>
    <div id="ftList"></div>
  </div>
  <!-- 英文卷 -->
</div>

<!-- ============ 練習區（按科目歸口） ============ -->
<div id="practiceView" style="display:none">
  <!-- 中文 -->
  <div class="wrap" id="cnPracView">
    <div class="sec-title">古詩詞 · 小學 1–6 年級必背 ＋ 初中（繁體＋拼音＋粵拼）</div>
    <div class="tools">
      <span class="chip on" data-g="all">全部</span>
      <span class="chip" data-g="一年級">一年級</span>
      <span class="chip" data-g="二年級">二年級</span>
      <span class="chip" data-g="三年級">三年級</span>
      <span class="chip" data-g="四年級">四年級</span>
      <span class="chip" data-g="五年級">五年級</span>
      <span class="chip" data-g="六年級">六年級</span>
      <span class="chip" data-g="初中">初中</span>
      <input type="search" id="poemSearch" placeholder="搜詩題 / 作者">
    </div>
    <div class="grid" id="poemGrid"></div>
  </div>
  <!-- 英文 -->
  <div class="wrap" id="enPracView" style="display:none">
    <div class="subnav" id="enPracSub" style="position:static;top:auto;margin:0 -16px 12px">
      <button data-es="hk" class="on">港小生字</button>
      <button data-es="vocab">詞表</button>
      <button data-es="iv">升中面試</button>
      <button data-es="paper">英文卷</button>
      <button data-es="goal">詞彙路線圖</button>
    </div>
    <div id="hkView">
      <div class="tools">
        <span style="font-size:12px;color:#8a8aa0;align-self:center">按 P1–P6 分級 · 點標題折疊 · 年級為坊間估算，非 EDB 官方詞單</span>
        <select id="hkTheme"><option value="">全部主題</option></select>
        <input type="search" id="hkSearch" placeholder="搜單詞 / 中文義">
        <label style="font-size:12px;display:flex;align-items:center;gap:4px"><input type="checkbox" id="hkHide"> 自測(隱中文)</label>
        <span class="hk-actions"><button id="hkCollapseAll" type="button">收起全部</button><button id="hkExpandAll" type="button">展開全部</button></span>
      </div>
      <div id="hkList"></div>
      <div class="moti" id="motiBar">
        <span class="flame" id="flame">🔥</span>
        <span class="moti-num" id="streakNum">0</span>
        <span class="moti-label">天連續打卡</span>
        <span class="moti-goal" id="dailyGoal"></span>
      </div>
      <button class="btn" id="flashBtn">🎴 閃卡抽查</button>
      <div class="flash" id="flashPanel" style="display:none">
        <div class="flash-card" id="flashCard"></div>
        <div class="flash-zh" id="flashZh" style="display:none"></div>
        <div class="flash-acts">
          <button class="btn" id="flashReveal">👁 翻開中文</button>
          <button class="btn" id="flashKnow" style="display:none">✅ 認識</button>
          <button class="btn" id="flashUnk" style="display:none">❌ 不認識</button>
          <button class="btn" id="flashSound">🔊 發音</button>
        </div>
        <div class="flash-stat" id="flashStat">本輪：已認識 0 / 共 0</div>
      </div>
    </div>
    <div id="vocabView" style="display:none">
      <div class="tools">
        <input type="search" id="vocabSearch" placeholder="搜單詞 / 中文義">
        <select id="vocabTopic"><option value="">全部主題</option></select>
      </div>
      <div id="vocabList"></div>
    </div>
    <div id="ivView" style="display:none">
      <div class="gtitle">升中面試攻略（坊間整理 · 2026 更新）</div>
      <span class="folk">綜合香港升中面試 2026 公開資料整理，非學校官方題庫；各校正確題型以該校當年公佈為準</span>

      <div class="paper">
        <h3>升中英文考核架構（參考 DSE/TSA 四卷）</h3>
        <ol>
          <li><strong>Reading</strong>：閱讀理解，文章多為生活／科普／故事，附選擇＋短答。</li>
          <li><strong>Writing</strong>：格式寫作（letter / email / report / story），看重結構與連詞。</li>
          <li><strong>Listening</strong>：聽錄音答題，語速接近母語。</li>
          <li><strong>Speaking</strong>：個人短講＋小組討論（Group Interaction），Band 1 英中面試常見。</li>
        </ol>
        <p class="hint">EMI（英文中學）通常另設英文能力測試：朗讀、閱讀理解、看圖說話或即時問答，表現往往具決定性。</p>
      </div>

      <div class="paper">
        <h3>面試 4 大形式（2026 坊間歸納）</h3>
        <div class="iv-grid">
          <div class="cell"><h4>個人面試</h4><p>1–2 位老師、約 10–20 分鐘，問背景／興趣／選校原因。例：聖保羅男女、皇仁書院。</p></div>
          <div class="cell"><h4>小組討論</h4><p>4–6 人圍話題討論，觀察溝通、邏輯、合作。例：拔萃男書院、瑪利曼。</p></div>
          <div class="cell"><h4>英文測試（EMI 必考）</h4><p>英文朗讀、閱讀理解、看圖說話、即時問答；表現常決定性。</p></div>
          <div class="cell"><h4>家長面談</h4><p>了解家庭教育理念，通常不計分但影響整體印象。例：培英中學。</p></div>
          <div class="cell"><h4>個人＋小組混合</h4><p>全面評估、難度最高。例：華仁書院（九龍）、喇沙書院。</p></div>
          <div class="cell"><h4>即場做卷</h4><p>部分學校加考中／英／數／科筆試（如景嶺書院），佔評分一環。</p></div>
        </div>
      </div>

      <div class="paper">
        <h3>10 大面試題型佔比（2026 坊間統計）</h3>
        <table class="iv-tbl">
          <tr><th>題型</th><th>出現佔比</th><th>示例</th></tr>
          <tr><td>自我介紹</td><td>100%</td><td>用 1 分鐘介紹自己</td></tr>
          <tr><td>報考原因</td><td>90%</td><td>點解想入我哋學校？</td></tr>
          <tr><td>個人專長</td><td>80%</td><td>你最大的成就是咩？</td></tr>
          <tr><td>中英雙語切換</td><td>70%</td><td>廣東話問完轉英文問</td></tr>
          <tr><td>時事評論</td><td>60%</td><td>AI 對教育有咩影響？</td></tr>
          <tr><td>情境題</td><td>55%</td><td>同學抄你功課你點做？</td></tr>
          <tr><td>閱讀理解</td><td>50%</td><td>即場讀文章後回答</td></tr>
          <tr><td>小組討論</td><td>45%</td><td>6 人一組討論話題</td></tr>
          <tr><td>創意思考</td><td>40%</td><td>如果你係校長會改咩？</td></tr>
          <tr><td>家長面見</td><td>30%</td><td>家長單獨或同學生見</td></tr>
        </table>
        <p class="hint">用法：按目標學校模式，從上表圈出最相關 5–6 類優先練習（如小組型重點練時事／創意／討論）。</p>
      </div>

      <div class="paper">
        <h3>英文自我介紹 · 黃金 4 步 ＋ 練習卡</h3>
        <p>結構：<b>Who am I?</b> → <b>What do I like?</b> → <b>What am I good at?</b> → <b>What is my goal?</b>。準備「骨架」現場發揮，<u>切勿背稿</u>——Band 1 面試官一眼看穿。</p>
        <div class="iv-build">
          <div class="iv-build-in">
            <label>姓名 <input id="ivName" placeholder="e.g. Chan Tai Man"></label>
            <label>年齡 <input id="ivAge" placeholder="12"></label>
            <label>學校 <input id="ivSch" placeholder="ABC Primary School"></label>
            <label>地區 <input id="ivDist" placeholder="Kowloon"></label>
            <label>最愛科目 <input id="ivSubj" placeholder="English"></label>
            <label>喜愛原因 <input id="ivWhy" placeholder="I can read stories"></label>
            <label>興趣 1 <input id="ivH1" placeholder="reading"></label>
            <label>興趣 2 <input id="ivH2" placeholder="swimming"></label>
            <label>性格 <input id="ivChar" placeholder="helpful"></label>
            <label>目標校 <input id="ivTgt" placeholder="XYZ College"></label>
          </div>
          <div class="iv-build-out">
            <div class="tmpl" id="ivOut">Good morning. My name is ______. I am ______ years old and I study at ______ School in ______.
My favourite subject is ______ because ______.
In my free time, I enjoy ______ and ______.
I am a ______ person and I work well with others.
I want to join ______ because ______.
Thank you for your time.</div>
            <button class="btn" id="ivRecBtn">🎙 錄音自測（1 分鐘）</button>
            <span id="ivRecStat" class="hint"></span>
          </div>
        </div>
      </div>

      <div class="paper">
        <h3>小組討論 · DO / DON'T</h3>
        <div class="iv-dodont">
          <div class="iv-do"><h4>✅ 加分做法</h4>
            <ul>
              <li>主動發言但不霸道</li>
              <li>回應其他同學的觀點（"I agree with…"）</li>
              <li>提出具體例子</li>
              <li>邀請較安靜的同學表達</li>
              <li>協助小組整理方向</li>
              <li>接受不同意見</li>
            </ul>
          </div>
          <div class="iv-dont"><h4>⛔ 扣分做法</h4>
            <ul>
              <li>急於搶答、打斷別人</li>
              <li>只顧表現自己</li>
              <li>全程沉默</li>
              <li>與人爭拗、否定他人</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="paper">
        <h3>常見面試題 · 分類（中英對照）</h3>
        <div class="iv-grid">
          <div class="cell"><h4>個人背景</h4><p>Tell me about your family / school. · 用三個詞形容自己。</p></div>
          <div class="cell"><h4>選校動機</h4><p>Why do you want to study here? · 同時被兩校取錄點揀？</p></div>
          <div class="cell"><h4>個人專長</h4><p>What is your greatest achievement?</p></div>
          <div class="cell"><h4>時事評論</h4><p>AI 對教育影響？環保／健康生活看法？</p></div>
          <div class="cell"><h4>情境題</h4><p>同學抄功課點做？朋友唔開心點安慰？</p></div>
          <div class="cell"><h4>創意思維</h4><p>If you were the principal, what would you change?</p></div>
          <div class="cell"><h4>英文朗讀＋延伸</h4><p>讀文章、加詞、答「睇過咩書？作者係邊個？」</p></div>
          <div class="cell"><h4>適應中學</h4><p>點管理時間／面對壓力／處理衝突？</p></div>
        </div>
      </div>

      <div class="paper">
        <h3>準備時間線（P5 → P6）</h3>
        <ol>
          <li><b>P5 下學期</b>：準備自我介紹草稿與基本面試句型。</li>
          <li><b>P6 上（9–12 月）</b>：練答題技巧與主題式表達、實戰模擬。</li>
          <li><b>P6 下（1–3 月）</b>：提升自信、錄影練習並回放檢討。</li>
        </ol>
      </div>

      <div class="paper">
        <h3>真實名校題例（2026 坊間整理）</h3>
        <p><b>景嶺書院（2026-02-08 面試）</b>：粵／英／普介紹自己；英文朗讀＋增詞＋延伸問（喜好／看過咩書／作者）；情境題「課室還可加咩」；數學題；做卷（中／英／科）；小組討論（粵英普 3 語，先自我介紹，約 4 條英文＋2 條普問）。</p>
        <p><b>可風中學（荃灣 Band 1 英中）</b>：中一面試創意問題須英文作答。</p>
        <p class="hint">⚠️ 題例每年不同，僅供熟悉題型與語言切換，不可當真卷背誦。</p>
      </div>

      <div class="paper">
        <h3>弱項自評 3 問 ＋ 家長面試貼士</h3>
        <ol>
          <li>能否用廣東話連續講 2 分鐘不斷？</li>
          <li>用英文回答問題會否結巴？</li>
          <li>在陌生人面前敢不敢舉手發言？</li>
        </ol>
        <p><b>家長面試</b>：具體講子女性格、優點、需改善之處；表現了解子女、願配合學校、能支援適應中學生活。不必把子女說得完美。</p>
      </div>

      <div class="paper">
        <h3>資料來源（坊間參考 · 檢索 2026-10-31）</h3>
        <ul class="src">
          <li>hkstudyroute.com —《Band 1 中學面試攻略 2026》《沙田 Band 1 中學面試攻略》</li>
          <li>notesity.hk —《升中面試攻略 2026：常見題目、自我介紹範本、英文面試及家長問題》</li>
          <li>couchpotatoeducation.com —《升中英文面試最全面攻略（自我介紹範本）》</li>
          <li>topschool.hket.com —《升中面試2026 校長親授錦囊／景嶺書院、可風中學題例》</li>
        </ul>
        <p class="hint">以上均為補習／教育機構或傳媒整理，非學校或考評局官方發布；正式題型與評分以目標學校當年公佈為準。</p>
      </div>
    </div>

    <div id="goalView" style="display:none">
      <div class="gtitle">詞彙路線圖（一年級 → 中六 · 該背多少 · 怎麼背）</div>
      <span class="folk">目標詞量為坊間基準（香港教育／DSE 備考機構整理），非教育局官方分級詞表——EDB 不公布官方必背詞單</span>

      <div class="gcard">
        <h3>① 本學習站目前收錄多少單詞？</h3>
        <p>英文詞彙共 <b>1,800 個</b>：港小基礎詞 <b>335</b>（一年級 73／二年級 68／三年級 56／四年級 50／五年級 47／六年級 41，已分級）＋ 通用詞表 B1 檔 <b>1,465</b>（CEFR B1，未分年級）。另收古詩詞 <b>185 首</b>（不計入單詞量）。</p>
        <p class="tip">⚠️ 這 1,800 詞是<b>入門奠基包</b>，遠未覆蓋真實目標（見下表）。港小基礎詞只佔小六真實要求的約 1/8；通用 B1 詞是成人通用英語、不等於香港課本詞序。真要銜接，仍須大量閱讀補詞。</p>
      </div>

      <div class="gcard">
        <h3>② 一年級到中六 · 累計詞量目標（坊間基準）</h3>
        <table class="iv-tbl">
          <tr><th>階段</th><th>年級</th><th>累計應掌握詞量（約）</th><th>說明</th></tr>
          <tr><td rowspan="6">小學</td><td>一年級 P1</td><td>500–800</td><td>起步：課堂用語＋高頻名詞動詞</td></tr>
          <tr><td>二年級 P2</td><td>1,000–1,200</td><td>加入簡單句型詞</td></tr>
          <tr><td>三年級 P3</td><td>1,500–1,800</td><td>閱讀起步量</td></tr>
          <tr><td>四年級 P4</td><td>2,000–2,200</td><td></td></tr>
          <tr><td>五年級 P5</td><td>2,300–2,500</td><td></td></tr>
          <tr><td>六年級 P6</td><td><b>2,500–3,000</b></td><td>小六呈分試實際水平（Band 1 學校）</td></tr>
          <tr><td rowspan="6">中學（DSE）</td><td>中一 S1</td><td>3,500–4,000</td><td>插班關鍵門檻：科目全英授課</td></tr>
          <tr><td>中二 S2</td><td>4,500</td><td></td></tr>
          <tr><td>中三 S3</td><td>5,000–5,500</td><td></td></tr>
          <tr><td>中四 S4</td><td>6,000</td><td></td></tr>
          <tr><td>中五 S5</td><td>7,000</td><td></td></tr>
          <tr><td>中六 S6（DSE）</td><td>6,000–8,000 保底／衝 L5 約 10,000+</td><td>閱讀被動詞 EHLA 門檻 L3 6,500／L5 11,000</td></tr>
        </table>
        <p class="hint">來源（均坊間參考 · 檢索 2026-10-31）：小六 2,500–3,000 — 智瞳教育《中國香港學校英文難度深度解析》、51Talk 香港升學中心、公眾號「葫蘆媽的朋友们」；中六 6,000–8,000 — 智瞳教育；DSE 分級門檻（閱讀被動 L3≈6,500／L5≈11,000，寫作主動 L3≈3,000／L5≈5,500）— EHLA dse-english.org（基於 past paper 難度與 HKEAA 報告整理）；4,000 常用詞保底 — 博纳 DSE 備考文。教育局（EDB）不公布官方必背詞單，以上為機構估算，年級歸屬為常見教學進度估算。</p>
      </div>

      <div class="gcard warn">
        <h3>③ 本家庭落點（目標 2027/28 插班中一）</h3>
        <p>目標校為北區 Band 1 英中。按六年級必背古詩詞素材推算，當前約小六（P6）水平，距中一門檻 3,500–4,000 詞有缺口（P6 真實 2,500–3,000）。路線：先把港小基礎詞 335 全吃透（閃卡＋貪吃蛇＋打卡），同步大量閱讀補到 <b>P6 上限 3,000</b>，再衝 <b>S1 3,500–4,000</b> 銜接入學；學術詞（數學／科學術語）單獨過一遍（見練習→數學術語表）。</p>
      </div>

      <div class="gcard">
        <h3>④ 怎麼背 · 記憶方法（80% 建能力＋20% 熟悉賽道）</h3>
        <div class="iv-grid">
          <div class="cell"><h4>1. 語境閱讀法（最有效）</h4><p>不背單詞書，在適合程度的英文讀物裡遇詞記詞；有上下文、記得牢、順帶學用法。學術詞單獨背。來源：智瞳教育備考文（坊間）。</p></div>
          <div class="cell"><h4>2. 主動 vs 被動詞彙</h4><p>會認（閱讀）≠ 會用（寫作口語）。DSE 寫作主動詞 L3≈3,000／L5≈5,500（EHLA）。先衝被動量，再煉主動輸出。</p></div>
          <div class="cell"><h4>3. 間隔重複（Spaced Repetition）</h4><p>按遺忘曲線複習，比死背一遍牢。本站「🎴閃卡抽查」即此邏輯；可用 Anki 加強。</p></div>
          <div class="cell"><h4>4. 聽讀法（Auditory）</h4><p>每詞點 🔊 跟讀（en-US），聽覺＋口型記憶，避開「啞巴英語」。本站港小詞／詞表均帶朗讀。</p></div>
          <div class="cell"><h4>5. 遊戲化＋打卡</h4><p>貪吃蛇吃詞、🔥連續打卡火焰、🏅徽章、🎴閃卡——把背詞藏進日常，降低抗拒。見本站「悠閒」「練習→英文」。</p></div>
          <div class="cell"><h4>6. 詞根詞綴＋聯想</h4><p>-tion 名詞、-ful 形容、un- 否定；用影像／故事聯想。適合中高年級擴詞。</p></div>
        </div>
        <p class="hint">方法學為通用學習科學與機構備考經驗整理（坊間參考），非官方教學指引；80/20 框架源自本規劃顧問方法論（見升學規劃→學習路線），機構軟文僅借框架、已重排時間與教材。</p>
      </div>
    </div>
    <div class="wrap gsec" id="paperView" style="display:none">
      <div class="lic-lock" id="licLockEn"></div>
      <div class="gtitle">英文卷 · 智能練習卷（本地隨機出題 · 分 P1–P6 · 可 AI 換題）</div>
      <span class="folk">基礎題庫為本地規則生成（非外部 AI）；可於下方「⚙ AI 設置」接入大模型現場換題（需自填接口與密鑰，僅存本瀏覽器）。題目為小學英文常見題型，年級歸屬為常見教學進度估算，以學校課本為準</span>
      <div class="pg-chips" id="pgChips">
        <span class="chip on" data-pg="P1">P1</span>
        <span class="chip" data-pg="P2">P2</span>
        <span class="chip" data-pg="P3">P3</span>
        <span class="chip" data-pg="P4">P4</span>
        <span class="chip" data-pg="P5">P5</span>
        <span class="chip" data-pg="P6">P6</span>
        <span class="chip" data-pg="ALL">綜合 P1–P6</span>
      </div>
      <div id="enGradeTopic" class="en-grade-topic"></div>
      <div class="enpaper-actions">
        <button class="btn" id="enNewPaper" onclick="genEnPaper()">🎲 出新卷</button>
        <button class="btn" id="enSubmit" onclick="gradeEnPaper()">✅ 交卷批改</button>
        <button class="btn" id="enPrint" onclick="printEnPaper()">🖨 打印一套卷子</button>
        <label class="print-ans-toggle"><input type="checkbox" id="enPrintAns"> 含答案版</label>
        <span class="enpaper-stat" id="enStat">本級最佳：—</span>
        <span class="enpaper-stat" id="licStatusEn"></span>
      </div>
      <div id="enPaperBox"></div>
      <div id="enPaperResult"></div>
      <div id="enSrcNote" class="en-src-note">
        <b>資料來源與說明（坊間參考 · 2026-10-31 檢索）：</b>
        年級主題參考 <a href="https://www.gostudy.hk" target="_blank" rel="noopener">GoStudy.HK</a>「小一至小三英文科練習」、<a href="https://crescenteduhk.com" target="_blank" rel="noopener">弦月教育</a> English Section P1–P6 文法專頁；
        題型參考 <a href="https://www.hkep.com" target="_blank" rel="noopener">香港教育圖書</a> 樣本卷、<a href="https://www.band1.org" target="_blank" rel="noopener">Band1 試卷網</a>、<a href="https://www.theexamcoach.tv/hk/sspa" target="_blank" rel="noopener">The Exam Coach</a> SSPA P6 文法練習。
        <br>⚠️ 本卷為本地規則隨機仿題，非評估局／學校真卷；年級難度為常見教學進度估算，以學校課本為準。
        <br>        📚 閱讀理解題取材自 <a href="https://www.edb.gov.hk/en/curriculum-development/kla/eng-edu/references-resources/Lit_Classics_Pri_CFT_r.html" target="_blank" rel="noopener">教育局「中國寓言系列」</a>（EDB 公開學與教資源，版權歸教育局，僅教學用途，檢索 2026-10-31）；題目為本站依官方英文文本改編，非逐字複製。
      </div>
      <details class="ai-cfg" id="aiCfg">
        <summary>⚙ AI 設置（接大模型現場換題 · 自填接口與密鑰）</summary>
        <div class="ai-cfg-body">
          <p class="hint">密鑰僅存於本瀏覽器 localStorage，不會上傳到本站以外的任何地方；僅發往你填寫的接口地址。若瀏覽器報 CORS 錯誤，說明該接口不允許瀏覽器直連，可改用 OpenRouter / Groq / 本地 LM Studio，或自建反向代理。</p>
          <label>Base URL（如 https://api.openai.com/v1）</label>
          <input id="aiBase" placeholder="https://api.openai.com/v1">
          <label>API Key</label>
          <input id="aiKey" type="password" placeholder="sk-...">
          <label>模型（如 gpt-4o-mini / deepseek-chat）</label>
          <input id="aiModel" placeholder="gpt-4o-mini">
          <div class="ai-cfg-actions">
            <button class="btn" onclick="saveAiCfg()">保存</button>
            <button class="btn" onclick="clearAiCfg()">清除</button>
            <span id="aiCfgMsg"></span>
          </div>
        </div>
      </details>
    </div>
  </div>
  <!-- 數學 -->
  <div class="wrap" id="mathPracView" style="display:none">
    <div class="subnav" id="mathPracSub" style="position:static;top:auto;margin:0 -16px 12px">
      <button data-es="mterms" class="on">中↔英術語表</button>
      <button data-es="mpaper">數學卷</button>
    </div>
    <div id="mTermsView">
      <div class="sec-title">數學中↔英術語表（點擊行＝標記「已掌握」；🔊 朗讀英文）</div>
      <div class="tools">
        <span class="chip on" data-mc="all">全部</span>
        <span class="chip" data-mc="數與運算">數與運算</span>
        <span class="chip" data-mc="分數小數百分數">分數·小數·百分數</span>
        <span class="chip" data-mc="代數">代數</span>
        <span class="chip" data-mc="幾何">幾何</span>
        <span class="chip" data-mc="度量">度量</span>
        <span class="chip" data-mc="統計與概率">統計與概率</span>
        <input type="search" id="mathSearch" placeholder="搜中文 / 英文術語">
        <button class="btn" id="mathPrint" onclick="window.print()">打印術語表</button>
      </div>
      <table class="mtable">
        <thead><tr><th style="width:120px">分類</th><th style="width:130px">中文術語</th><th style="width:200px">英文術語</th><th>備註</th></tr></thead>
        <tbody id="mathBody"></tbody>
      </table>
    </div>
    <div class="wrap gsec" id="mathPaperView" style="display:none">
      <div class="lic-lock" id="licLockMath"></div>
      <div class="gtitle">數學卷 · 智能練習卷（雙語對照 · 分 P1–P6）</div>
      <span class="folk">基礎題庫為本地仿編原創題（非評估局／學校真卷）；題目採「英文題幹＋中文對照」，對應香港英中數學以英文出題的實況；年級難度為常見教學進度估算，以學校課本為準。</span>
      <div class="pg-chips" id="mpgChips">
        <span class="chip on" data-pg="P1">P1</span>
        <span class="chip" data-pg="P2">P2</span>
        <span class="chip" data-pg="P3">P3</span>
        <span class="chip" data-pg="P4">P4</span>
        <span class="chip" data-pg="P5">P5</span>
        <span class="chip" data-pg="P6">P6</span>
      </div>
      <div class="enpaper-actions">
        <button class="btn" id="mathNewPaper" onclick="genMathPaper()">🎲 出新卷</button>
        <button class="btn" id="mathSubmit" onclick="gradeMathPaper()">✅ 交卷批改</button>
        <button class="btn" id="mathPrintBtn" onclick="printMathPaper()">🖨 打印一套卷子</button>
        <label class="print-ans-toggle"><input type="checkbox" id="mathPrintAns"> 含答案版</label>
        <span class="enpaper-stat" id="mathStat">本級最佳：—</span>
        <span class="enpaper-stat" id="licStatusMath"></span>
      </div>
      <div id="mathPaperBox"></div>
      <div id="mathPaperResult"></div>
      <div class="en-src-note" id="mathSrcNote">
        <b>資料來源與說明（坊間參考 · 2026-10-31 檢索）：</b>
        題庫為本地仿編原創練習題，參考香港小學數學課程常見進度（數與運算／分數·小數·百分數／代數／幾何／度量／統計與概率）整理；非評估局（HKEAA）或學校真卷，年級難度為估算。正式以學校課本與教育局課程指引為準。
      </div>
    </div>
  </div>
</div>

<!-- ============ 升學規劃（插班思路） ============ -->
<div id="planView" style="display:none">
  <div class="subnav" id="planSub">
    <button data-sub="timeline" class="on">時間線</button>
    <button data-sub="schools">擇校分檔</button>
    <button data-sub="docs">材料清單</button>
    <button data-sub="study">學習路線</button>
    <button data-sub="policy">身份政策</button>
  </div>

  <!-- 時間線 -->
  <div class="wrap" id="timelineView">
    <div class="gsec">
      <h2>申請時間線（以 2027.9 入中一為例）</h2>
      <p class="tip">適用以 9 月入學為主批、1 月春季為備選。具體日期以教育局及各校官網當年公告為準。</p>
      <table class="mtable">
        <thead><tr><th style="width:90px">階段</th><th style="width:140px">時間</th><th>動作</th></tr></thead>
        <tbody>
          <tr><td>備戰期</td><td>2026.10–12</td><td>確認簽證/身份進度；收集成績單（蓋章）＋繁體/英文翻譯；定 6–8 所衝穩保選校單；語言起步（英文/繁體/粵語聽力）</td></tr>
          <tr><td>自行分配<br>（官立/資助/參加派位直資）</td><td><b>2027.1.4–1.18</b></td><td>向教育局學位分配組遞交；⚠️ 遞交時須已持身份/居留權——本家庭身份 2027.6 到，<b>此窗口錯過</b></td></tr>
          <tr><td>申請高峰/備戰</td><td>2027.3–5</td><td>中英數筆試＋中英面試備戰；教育局途徑三（新來港）可於 <b>5 月起</b>向區域教育服務處登記</td></tr>
          <tr><td>關鍵節點</td><td>2027.6</td><td>辦香港身份證；教育局區域教育服務處登記學位需求（途徑三，5–8 月）；⚠️ 官津中一<b>放榜＝2027.7.6</b>（非 6 月初），放榜後開始叩門</td></tr>
          <tr><td>叩門衝刺</td><td>2027.7–8</td><td>跟進棄位空缺（7 月中下旬最多）；帶全套材料到校務處即場筆面試；收 Offer 後 <b>3–7 天內繳留位費</b></td></tr>
          <tr><td>入學</td><td>2027.9</td><td>辦內地學籍轉出；校服書單；參加新來港學童適應/啟動課程</td></tr>
        </tbody>
      </table>
      <div class="gcard warn">
        <h3>春季插班備選（1 月入學）</h3>
        <p>前一年 <b>10–12 月</b>申請，<b>12 月上旬</b>基本截止，學位約為秋季 30%。</p>
      </div>
      <div class="src">來源：教育局 2025/2027 中一學位分配辦法（官方）｜適用 2027/28 學年｜具體以各校官網當年公告為準</div>
    </div>
  </div>

  <!-- 擇校分檔 -->
  <div class="wrap" id="schoolsView" style="display:none">
    <div class="gsec">
      <h2>擇校分檔：北區 23 所中學（跨境插班視角）</h2>
      <div class="gcard">
        <h3>北區跨境要點</h3>
        <p>北區（上水/粉嶺）是羅湖、福田（落馬洲支線）、文錦渡口岸入港第一站，東鐵線 1 站到上水、2 站到粉嶺，單程通關＋車程約 30–40 分鐘，跨境生比例全港最高。教育局有跨境學童派位安排，北區 <b>30 所學校</b>參與（2025 年度數據，中一跨境學額約 <b>171 個</b>，來源：教育局公開資料，坊間引用）。跨境校巴/保姆車體系成熟，校巴申請一般每年 5–6 月。</p>
      </div>
      <div class="gcard warn">
        <h3>本家庭叩門總邏輯（身份 2027.6 到手的家庭先看這個）</h3>
        <p>孩子身份預計 <b>2027 年 6 月到手</b>，意味著：① 2027.1.4–1.18 自行分配窗口＝錯過（須遞交時已持身份）；② 5 月前所有主申請＝錯過；③ 唯一現實路徑＝兩條並行——<b>A. 2027.7.6 放榜後叩門</b>（黃金期 7.6–7.9，官津每班約 1 個留班位）＋ <b>B. 教育局途徑三</b>（新來港兒童資助中一，2027.5–8 月登記，分批 7.6/7 月底/8 月中出結果，兜底不會沒書讀）；④ 兩所直資（風采、心誠）同樣參加派位走 1 月窗口，不存在「身份到手即報第一批占位」紅利。</p>
      </div>
      <div class="scroll-x">
        <table class="mtable">
          <thead><tr><th>梯隊</th><th>學校</th><th>類型</th><th>教學語言</th><th>Band參考<br><span style="font-weight:400;color:#a33">非官方</span></th><th>學費</th><th>申請路徑（本家庭）</th></tr></thead>
          <tbody>
            <tr><td class="tier1">衝刺</td><td>鄧顯紀念中學</td><td>資助</td><td>英中</td><td>1A</td><td>免（僅堂費/書雜費）</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier1">衝刺</td><td>東華三院甲寅年總理中學</td><td>資助</td><td>英中</td><td>1A–1B</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier1">衝刺</td><td>田家炳中學</td><td>資助</td><td>英中</td><td>1B–1C</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier1">衝刺</td><td>聖公會陳融中學</td><td>資助</td><td>英中</td><td>1B–1C</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier1">衝刺</td><td>東華三院李嘉誠中學</td><td>資助</td><td>英中</td><td>1C</td><td>免</td><td>官津 7 月叩門＋8 月補錄</td></tr>
            <tr><td class="tier1">衝刺</td><td>風采中學（教育評議會主辦）</td><td>直資</td><td>中英並重</td><td>1B</td><td>約 $1.5–2 萬/年（坊間，以官網為準）</td><td>直資 7 月年中插班/叩門</td></tr>
            <tr><td class="tier1">衝刺</td><td>粉嶺官立中學</td><td>官立</td><td>英中</td><td>1C–2A</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>鳳溪第一中學</td><td>資助</td><td>英中為主</td><td>1C–2A</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>香海正覺蓮社佛教馬錦燦紀念英文中學</td><td>資助</td><td>英中</td><td>2A</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>宣道會陳朱素華紀念中學</td><td>資助</td><td>英中</td><td>2A–2B</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>粉嶺禮賢會中學</td><td>資助</td><td>英中</td><td>2A–2B</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>基督教香港信義會心誠中學</td><td>直資</td><td>英中</td><td>2</td><td>中一至中三 $7,100/年；中四至中六 $8,400/年（2025-26 官網）</td><td>直資 7 月年中插班/叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>鳳溪廖萬石堂中學</td><td>資助</td><td>英中為主</td><td>2</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>保良局馬錦明中學</td><td>資助</td><td>英中</td><td>2</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>粉嶺救恩書院</td><td>資助</td><td>英中</td><td>2B–2C</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>中華基督教會基新中學</td><td>資助</td><td>中文</td><td>2</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>上水官立中學</td><td>官立</td><td>中文</td><td>2B–3</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier3">保底</td><td>明愛粉嶺陳震夏中學</td><td>資助</td><td>中文</td><td>3</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier3">保底</td><td>聖芳濟各書院</td><td>資助</td><td>中文</td><td>3</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier3">保底</td><td>新界喇沙中學</td><td>資助</td><td>中文</td><td>3</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier3">保底</td><td>佛教茂峰法師紀念中學</td><td>資助</td><td>中文</td><td>3</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier3">保底</td><td>神召會康樂中學</td><td>資助</td><td>中文</td><td>3</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier3">保底</td><td>香港教師會李興貴中學</td><td>資助</td><td>中文</td><td>3</td><td>免</td><td>官津 7 月叩門</td></tr>
          </tbody>
        </table>
      </div>
      <div class="gcard">
        <h3>叩門衝刺組合建議（按英文水平分）</h3>
        <p><b>英文達標（PET 量級）</b>：衝刺 鄧顯/甲寅年/田家炳/陳融 ＋ 求穩 風采/心誠/粉嶺官立 ＋ 保底 基新/上水官立/粉嶺救恩。</p>
        <p><b>英文偏弱</b>：衝刺 甲寅年/李嘉誠 ＋ 求穩 鳳溪一中/救恩/基新 ＋ 保底 基新/上水官立/李興貴（先中文過渡一年，再圖轉校）。</p>
        <p>無論哪組，<b>7.6 一早從衝刺檔開始衝</b>，保底檔留 7.8–7.9 兜底，並同步走 EDB 途徑三。</p>
      </div>
      <div class="src">來源：北區 23 所中學清單（hk-placement 知識庫 v0.2，2026-10-27 核對）｜Band 組別＝坊間非官方參考（教育局不公布官方 Banding）｜學費/截止日以學校官網當年公告為準｜⚠️ 身份硬門檻：身份 2027.6 才到手者一律走放榜後叩門＋途徑三</div>
    </div>
  </div>

  <!-- 材料清單 -->
  <div class="wrap" id="docsView" style="display:none">
    <div class="gsec">
      <h2>材料清單（按身份類型準備）</h2>
      <p class="tip">⚠️ 簡體成績單<b>無蓋章、無翻譯</b> → 初審直接刷；簽證未到手就遞官津申請 → 不受理。下方清單為通用人型，受養人簽證/單程證/永居家庭共性相同，細節以學校與入境處要求為準。</p>
      <h3>一、必備（缺一不可）</h3>
      <table class="mtable">
        <thead><tr><th style="width:90px">類別</th><th>材料</th></tr></thead>
        <tbody>
          <tr><td>身份類</td><td>孩子港澳通行證＋受養人簽證/香港身份證、出生證明（內地出生需公證/翻譯）、父母證件、親子關係證明</td></tr>
          <tr><td>學業類</td><td>近兩年成績單（<b>學校蓋章</b>＋繁體/英文翻譯件）、在讀證明、學籍/轉學證明、班主任或校長推薦信 1–2 封</td></tr>
          <tr><td>健康類</td><td>疫苗接種記錄（提前核對是否補針，備翻譯本）</td></tr>
          <tr><td>住址類</td><td>香港租約/水電單（官津派位與校網、叩門優先序都看住址）</td></tr>
        </tbody>
      </table>
      <h3>二、加分材料</h3>
      <p>獎狀證書 5–8 項、作品集、孩子中英文自我介紹文書、叩門信（一頁紙，寫具體優勢與擇校理由）、英語證書（KET/PET 等）。</p>
      <div class="gcard warn">
        <h3>叩門當天材料 8 樣（缺一不可）</h3>
        <p>① 派位證/獲派通知正本＋複印件（入場券）；② 小五小六成績表（蓋章）＋繁體/英文翻譯；③ 叩門信（每校單獨寫）；④ 個人簡歷＋獲獎證書（學術類優先）；⑤ 身份證明（出生證、香港身份證/通行證、家長簽證）；⑥ 證件照（1 寸/2 寸白底各 5 張）；⑦ 文具（筆/橡皮/尺）；⑧ 補給（水、小零食、充電寶）。</p>
      </div>
      <div class="src">來源：插班全流程時間線與材料清單（hk-placement 知識庫 v1.1，2026-10-29）｜具體以教育局及各校官網當年公告為準</div>
    </div>
  </div>

  <!-- 學習路線 -->
  <div class="wrap" id="studyView" style="display:none">
    <div class="gsec">
      <h2>學習提升路線（80% 建能力 ＋ 20% 熟悉賽道）</h2>
      <div class="gcard warn">
        <h3>原則與來源</h3>
        <p>「80% 建能力＋20% 熟悉賽道」框架來自 2025-12-01 公眾號「雙母語娃養成記」文章《13歲，雅思8分，沒刷一套題》——<b>該文為機構軟文（文末導流試聽課）</b>，框架本身成立但<b>案例不可照搬</b>。香港插班不能照搬其「三年打底」：多數家庭是插班前 6–12 個月才啟動，且還要考繁體中文卷、英文題幹數學卷、粵語面試，純英文路線會漏項。</p>
      </div>
      <div class="gcard">
        <h3>排課前三條硬規則</h3>
        <p>① <b>先定級，再排課</b>——不給級別就給不出排期；② <b>按可用小時數配教材</b>——先算總賬（剩餘週數 × 每週小時＝總預算），超預算一律砍；③ <b>能力線在應試線之前，但應試線絕不省</b>——裸考去叩門是最常見的浪費機會方式。</p>
      </div>
      <h3>定級三連測（約 40 分鐘，一次搞定）</h3>
      <table class="mtable">
        <thead><tr><th style="width:90px">步驟</th><th>做法</th></tr></thead>
        <tbody>
          <tr><td>閱讀定級<br>15 分鐘</td><td>從 Reading Explorer 目標級抽 1 篇正文讀 8 分鐘，用中文口述：講什麼、作者想說什麼、哪句最關鍵。<b>能說出結構與主旨→該級合適；只能複述細節→降一級。</b></td></tr>
          <tr><td>寫作定級<br>20 分鐘</td><td>中性題目（例：*Should students have mobile phones at school?*）限時 20 分鐘、不查詞典。看：句子對不對（主謂一致/時態）→不對從 Foundations 起；有無主題句和支撐→沒有從 Level 1 起；段落銜接→有可直接進 Level 2。</td></tr>
          <tr><td>口語抽樣<br>5 分鐘</td><td>問三題（介紹自己/週末做什麼/為何想來港讀書）錄音，看能否連續講 60 秒不長時間卡頓。</td></tr>
        </tbody>
      </table>
      <h3>學習優先級（P0/P1/P2）</h3>
      <table class="mtable">
        <thead><tr><th style="width:60px">優先</th><th style="width:90px">項目</th><th>目標與動作</th></tr></thead>
        <tbody>
          <tr><td>P0</td><td>英文</td><td>決定走英中還是中文中學過渡。先定級；每日 30–45 分鐘分級閱讀；每週 2 篇寫作；學科詞彙表；量化錨點用 KET/PET（PET 通過約對應 Band 1 英中底線，<b>坊間說法，非官方標準</b>）。</td></tr>
          <tr><td>P1</td><td>繁體字</td><td>認讀覆蓋 80% 常用字。每天 15–20 分鐘，先常用 500 字認讀再書寫。</td></tr>
          <tr><td>P1</td><td>粵語</td><td>聽懂課堂指令即可。每天 15–30 分鐘磨耳朵（港台兒童節目/新聞）。</td></tr>
          <tr><td>P2</td><td>數學</td><td>短板在語言不在難度。英文題幹拆解＋香港術語/單位（術語表見練習→數學）。</td></tr>
          <tr><td>P2</td><td>面試</td><td>提前 3–6 個月啟動。1 分鐘中英自我介紹、常見問題庫（為何來港/為何選本校/如何適應）、每月 1 次模擬面試。</td></tr>
        </tbody>
      </table>
      <div class="gcard">
        <h3>8 個月壓縮排期（示例：2026.11 → 2027.7.6 叩門）</h3>
        <p>變量：每週 5–8 小時、目標穩妥英中檔。總預算約 36 週 × 6.5 小時 ≈ <b>230 小時</b>（估算）。能力線（80%）＝閱讀精讀＋寫作＋泛讀；應試線（20%）＝題型＋面試＋數學英文術語。每月驗收指標：11 月出定級表、12 月能寫 8–10 句連貫段落、1 月 100–120 詞有主題句、3 月 150 詞結構化短文、6 月材料 8 樣齊＋3 校信封好、7.6–7.9 叩門實戰。</p>
      </div>
      <div class="gcard">
        <h3>每週 6.5 小時模板（可排進日曆）</h3>
        <p>週一 45min 精讀＋拆長難句；週二 45min 寫作練習；週三 45min 精讀續（詞彙＋技巧）；週四 45min 數學英文題幹 20min＋口語錄音 25min；週五 45min 泛讀；週六 120min 限時寫作＋批改＋重寫；週日 45min 泛讀＋錯題回顧。<b>每天額外 15–20min：繁體字認讀＋粵語聽力（不佔英文預算）。</b></p>
      </div>
      <div class="gcard warn">
        <h3>常見坑（按踩坑頻率）</h3>
        <p>① 買齊六本教材從 Foundations 一路排到 Level 5（讀不完）；② 只刷題不建能力（面試一開口就露）；③ 只建能力不做應試（沒見過題型、沒模擬面試）；④ 忽略繁體與粵語（中文卷讀不完、面試聽不懂）；⑤ 按年齡選級別（12 歲≠Level 2，按定級）；⑥ 把機構推文當官方結論。</p>
      </div>
      <div class="src">來源：學術英語能力路線（hk-placement 知識庫 v1.0，2026-10-29）＋ 插班時間線 v1.1｜80/20 框架性質＝機構軟文（非學術）｜教材 CEFR/藍思為坊間教輔整理，選級以定級測試為準｜各校英文卷寫作題型未取到（待向目標校索取）</div>
    </div>
  </div>

  <!-- 身份政策 -->
  <div class="wrap" id="policyView" style="display:none">
    <div class="gsec">
      <h2>身份與政策合規</h2>
      <div class="gcard warn">
        <h3>⚠️ 受養人簽證是硬門檻</h3>
        <p>所有官立/資助/參加派位直資學校，在 1 月自行分配窗口遞交時須已持香港身份/居留權。身份到手時間直接決定能走哪條申請路徑——遲到者只能走放榜後叩門＋教育局途徑三（見「擇校分檔」叩門總邏輯）。</p>
      </div>
      <div class="gcard warn">
        <h3>⚠️ 居港 2 年新政（2028/29 學年起）</h3>
        <p>人才計劃子女申請政府資助大專學額須<b>居港滿 2 年</b>（已有司法案例）。若目標 DSE 後讀本地資助大學，需提前規劃搬港定居時間線——最遲 2027 年內安排搬港，從中學就要倒推。</p>
      </div>
      <div class="gcard">
        <h3>深圳學籍</h3>
        <p>拿到港校 Offer 前<b>不要註銷</b>內地學籍。兩邊銜接以「先拿到 Offer 再轉出」為原則。</p>
      </div>
      <div class="gcard">
        <h3>Band 分組說明</h3>
        <p>教育局<b>不公布官方 Banding</b>，坊間 Band（1A–3）僅作分檔錨點與擇校參考，非官方標準。擇校分檔表中的 Band 參考均標註「非官方」。</p>
      </div>
      <div class="src">來源：hk-placement 知識庫（north-district-schools v0.2 / timeline v1.1，2026-10-27 至 2026-10-29 核對）｜政策類以入境事務處、教育局及學校官方公告為準</div>
    </div>
  </div>
</div>

<!-- ============ 進度 ============ -->
<div class="wrap" id="progressView" style="display:none">
  <div class="stat">
    <div class="b"><div class="n" id="stRecite">0</div><div class="l">詩·已背熟</div></div>
    <div class="b"><div class="n" id="stWrite">0</div><div class="l">詩·已默寫</div></div>
    <div class="b"><div class="n" id="stVocab">0</div><div class="l">詞·已掌握</div></div>
    <div class="b"><div class="n" id="stHk">0</div><div class="l">港小詞·已掌握</div></div>
    <div class="b"><div class="n" id="stMath">0</div><div class="l">數術語·已掌握</div></div>
  </div>
  <div class="tools" style="margin-bottom:14px">
    <button class="btn" id="exportBtn">導出進度(JSON)</button>
    <button class="btn" id="importBtn">匯入進度</button>
    <input type="file" id="importFile" accept="application/json" style="display:none">
    <span style="font-size:12px;color:#888">進度只存本機瀏覽器，換設備／清緩存前請先導出備份</span>
  </div>
  <div class="sec-title">成就徽章</div>
  <div id="badgeBox" class="badges"></div>
  <div class="sec-title">已背熟詩列表</div>
  <div id="progList"></div>
  <button class="clr" id="clearBtn">清空全部進度</button>
</div>

<div class="wrap" id="funView" style="display:none">
  <div class="gtitle">單詞貪吃蛇（悠閒 · 邊玩邊記）</div>
  <span class="folk">食物＝隨機港小生字；吃到看中文義，死亡後可一鍵標「已掌握」。純本地，不計分排名。</span>
  <div class="snake-wrap">
    <canvas id="snakeCanvas" width="320" height="320"></canvas>
    <div class="snake-side">
      <div class="snake-stat">本局吃到：<b id="snakeScore">0</b> 詞 ｜ 最高：<b id="snakeBest">0</b></div>
      <div class="snake-word" id="snakeWord">按「開始」出題</div>
      <button class="btn" id="snakeStart">開始 / 重來</button>
      <button class="btn" id="snakeMaster" disabled>把本局詞標為已掌握（<span id="snakeMasterN">0</span>）</button>
      <div class="snake-pad">
        <button class="spad" data-dir="up">▲</button>
        <div><button class="spad" data-dir="left">◀</button><button class="spad" data-dir="down">▼</button><button class="spad" data-dir="right">▶</button></div>
      </div>
      <p class="snake-tip">電腦用方向鍵，手機用上面按鈕。撞牆或咬到自己就結束。</p>
    </div>
  </div>
</div>

<div class="mask" id="mask">
  <div class="modal" id="modal">
    <span class="x" onclick="closeModal()">×</span>
    <h2 id="mTitle"></h2>
    <div class="sub" id="mSub"></div>
    <div class="toggles">
      <label><input type="checkbox" id="tgPy" checked onchange="renderModal()"> 顯示拼音</label>
      <label><input type="checkbox" id="tgJy" checked onchange="renderModal()"> 顯示粵拼</label>
    </div>
    <div id="mBody"></div>
    <div class="acts" id="mActs"></div>
  </div>
</div>

<div id="enPrintSheet" class="en-print"></div>
<div id="mathPrintSheet" class="en-print"></div>

<footer>
數據來源：chinese-poetry（詩文）· word-atlas B1 檔（詞表，CC BY 4.0 須署名 Word Atlas contributors 詞光）· 港小基礎詞（坊間整理，非 EDB 官方分級詞表，年級為估算）· 拼音 pypinyin · 粵拼 jyutping<br>
數學術語表為手編中↔英對照，以香港課本／考評局用語為準。<br>
速覽差異與繁體對照、英文卷結構為坊間整理，正式以香港教育局課程指引、考評局與學校公布為準。本頁為本地原型，未上傳任何數據。<br>
🔊 朗讀功能依賴瀏覽器語音引擎：英文／普通話普遍支援；粵語朗讀需系統已安裝粵語嗓（如無則回退），以實際設備為準。
</footer>

<script>
const DATA = __DATA__;
const POEMS = DATA.poems, VOCAB = DATA.vocab, HK = DATA.hk_words;

// ---- 英文卷·智能練習卷（本地規則生成，分 P1–P6，非外部 AI） ----
// 題型：mc 選擇 / fill 填空 / read 閱讀 / open 短答(不計分) / write 寫作(不計分)
const EN_QBANK = {
  P1:[
    {t:"mc",q:"「apple」的中文是？",opts:["蘋果","香蕉","橙","葡萄"],a:0},
    {t:"mc",q:"「貓」的英文是？",opts:["cat","dog","bird","fish"],a:0},
    {t:"fill",q:"I have ___ (a / an) apple.",a:"an"},
    {t:"mc",q:"one book, two ___ (book).",opts:["books","book","bookes","bookies"],a:0},
    {t:"mc",q:"I ___ a boy.",opts:["am","is","are"],a:0},
    {t:"mc",q:"She ___ a student.",opts:["am","is","are"],a:1},
    {t:"mc",q:"They ___ my friends.",opts:["am","is","are"],a:2},
    {t:"mc",q:"「red」的中文是？",opts:["紅色","藍色","綠色","黃色"],a:0},
    {t:"mc",q:"「三」的英文是？",opts:["three","two","four","one"],a:0},
    {t:"fill",q:"This ___ (be) a dog.",a:"is"},
    {t:"mc",q:"「眼睛」的英文是？",opts:["eye","ear","nose","mouth"],a:0},
    {t:"mc",q:"The cat is ___ the table. (on / in / under)",opts:["on","in","under"],a:0},
    {t:"mc",q:"The ball is ___ the box. (in / on / under)",opts:["in","on","under"],a:0},
    {t:"mc",q:"The dog is ___ the chair. (under / on / in)",opts:["under","on","in"],a:0},
    {t:"mc",q:"「大」的相反詞是？",opts:["small","big","tall","long"],a:0},
    {t:"mc",q:"Which one is a fruit?",opts:["apple","dog","book","chair"],a:0},
    {t:"fill",q:"He is ___ (a / an) boy.",a:"a"},
    {t:"mc",q:"「學校」的英文是？",opts:["school","home","park","shop"],a:0},
    {t:"mc",q:"「星期一」的英文是？",opts:["Monday","Sunday","Tuesday","Friday"],a:0},
    {t:"mc",q:"「水」的英文是？",opts:["water","fire","air","earth"],a:0},
    {t:"read",pass:"Tom is a boy. He has a red ball. The ball is on the table.",qs:[
      {q:"Is Tom a boy?",opts:["Yes","No"],a:0},
      {q:"What colour is the ball?",opts:["red","blue","green"],a:0},
      {q:"Where is the ball?",opts:["on the table","under the table","in the box"],a:0}]}
  ],
  P2:[
    {t:"mc",q:"「學校」的英文是？",opts:["school","home","park","shop"],a:0},
    {t:"fill",q:"one box, two ___ (box).",a:"boxes"},
    {t:"mc",q:"Yesterday I ___ (go) to the park.",opts:["went","go","goes"],a:0},
    {t:"mc",q:"「快樂」的英文是？",opts:["happy","sad","angry","tired"],a:0},
    {t:"fill",q:"He ___ (like) apples.",a:"likes"},
    {t:"mc",q:"「牛奶」的英文是？",opts:["milk","water","juice","tea"],a:0},
    {t:"mc",q:"This is Mary's ___ (book / books).",opts:["book","books"],a:0},
    {t:"fill",q:"I have ___ (some / any) apples.",a:"some"},
    {t:"mc",q:"There ___ (be) some milk in the cup.",opts:["is","are"],a:0},
    {t:"mc",q:"The book is ___ the desk and the chair. (between / under / on)",opts:["between","under","on"],a:0},
    {t:"fill",q:"Many ___ (cat) like fish.",a:"cats"},
    {t:"mc",q:"「能」的英文是？",opts:["can","must","should","will"],a:0},
    {t:"mc",q:"Tom ___ swim. (他會游泳)",opts:["can","can't"],a:0},
    {t:"fill",q:"This is the ___ (teacher) desk. (所有格 's)",a:"teacher's"},
    {t:"mc",q:"「老師」的英文是？",opts:["teacher","student","doctor","driver"],a:0},
    {t:"mc",q:"「許多」的英文是？",opts:["many","some","any","few"],a:0},
    {t:"mc",q:"「醫生」的英文是？",opts:["doctor","teacher","farmer","driver"],a:0},
    {t:"fill",q:"We ___ (go) to school every day.",a:"go"},
    {t:"read",pass:"Mary is a girl. She has a big dog. The dog is under the chair. Mary likes the dog.",qs:[
      {q:"What has Mary?",opts:["a big dog","a small cat","a red ball"],a:0},
      {q:"Where is the dog?",opts:["under the chair","on the table","in the box"],a:0}]}
  ],
  P3:[
    {t:"read",pass:"Tom is a boy. He lives in Hong Kong. He likes reading books. Every Sunday he goes to the library.",qs:[
      {q:"Where does Tom live?",opts:["Hong Kong","London","Tokyo"],a:0},
      {q:"What does Tom like?",opts:["reading","swimming","singing"],a:0},
      {q:"When does he go to the library?",opts:["Sunday","Monday","Saturday"],a:0}]},
    {t:"mc",q:"We ___ (eat) pizza yesterday.",opts:["ate","eat","eats"],a:0},
    {t:"mc",q:"Tom ___ (go) to school yesterday.",opts:["went","go","goes"],a:0},
    {t:"mc",q:"She ___ (see) a bird in the tree.",opts:["saw","see","seen"],a:0},
    {t:"mc",q:"The book is ___ the desk. (on / in / under)",opts:["on","in","under"],a:0},
    {t:"fill",q:"She ___ (go) to school every day.",a:"goes"},
    {t:"mc",q:"「圖書館」的英文是？",opts:["library","garden","kitchen","bathroom"],a:0},
    {t:"mc",q:"「因為」的英文是？",opts:["because","but","and","or"],a:0},
    {t:"fill",q:"There ___ (be) two cats.",a:"are"},
    {t:"mc",q:"「醫生」的英文是？",opts:["doctor","teacher","farmer","driver"],a:0},
    {t:"mc",q:"Which is the correct order? ( words: I / like / apples )",opts:["I like apples","apples I like","like I apples"],a:0},
    {t:"mc",q:"My birthday is ___ Monday. (on / in / at)",opts:["on","in","at"],a:0},
    {t:"fill",q:"The party is ___ 3 o'clock. (at / on / in)",a:"at"},
    {t:"mc",q:"「昨天」的英文是？",opts:["yesterday","tomorrow","today","tonight"],a:0},
    {t:"fill",q:"___ there a book on the desk? (Is / Are)",a:"Is"},
    {t:"mc",q:"「博物館」的英文是？",opts:["museum","cinema","theatre","supermarket"],a:0},
    {t:"read",pass:"Mary has a red ball. She plays with it after school. Her brother Tom has a blue car. They are happy.",qs:[
      {q:"What colour is Mary's ball?",opts:["red","blue","green"],a:0},
      {q:"Who has a blue car?",opts:["Tom","Mary","Tom's friend"],a:0},
      {q:"How do they feel?",opts:["happy","sad","angry"],a:0}]},
    {t:"mc",q:"「邀請」的英文是？",opts:["invite","visit","invent","imagine"],a:0},
    {t:"fill",q:"I ___ (be) at home now.",a:"am"},
    {t:"mc",q:"「城市」的英文是？",opts:["city","town","village","country"],a:0}
  ],
  P4:[
    {t:"read",pass:"Last summer, Andy went to the beach with his family. They built a sandcastle and swam in the sea. Andy ate an ice cream. He was very happy.",qs:[
      {q:"Where did Andy go?",opts:["beach","mountain","zoo"],a:0},
      {q:"What did they build?",opts:["sandcastle","house","bridge"],a:0},
      {q:"How did Andy feel?",opts:["happy","sad","angry"],a:0}]},
    {t:"mc",q:"Tom is ___ (tall) than John.",opts:["taller","tall","tallest"],a:0},
    {t:"mc",q:"The blue whale is the ___ (big) animal.",opts:["biggest","bigger","big"],a:0},
    {t:"fill",q:"He ___ (walk) to school yesterday.",a:"walked"},
    {t:"mc",q:"「博物館」的英文是？",opts:["museum","cinema","theatre","supermarket"],a:0},
    {t:"mc",q:"「邀請」的英文是？",opts:["invite","visit","invent","imagine"],a:0},
    {t:"read",pass:"I ___ (1) to the park yesterday. I ___ (2) a dog there.",qs:[
      {q:"(1)",opts:["went","go","goes"],a:0},
      {q:"(2)",opts:["saw","see","seen"],a:0}]},
    {t:"write",q:"Write 3 sentences about your favourite food.",guide:["name the food","say why you like it","say when you eat it"],model:"My favourite food is dumplings. I like them because they are tasty. I eat them during Chinese New Year."},
    {t:"mc",q:"「勇敢」的英文是？",opts:["brave","bright","busy","broken"],a:0},
    {t:"fill",q:"If it rains, we ___ (stay) at home.",a:"stay"},
    {t:"mc",q:"She sings ___ (beautiful).",opts:["beautifully","beautiful","beauty"],a:0},
    {t:"fill",q:"They ___ (play) football every weekend.",a:"play"},
    {t:"mc",q:"「因為」的英文是？",opts:["because","but","and","or"],a:0},
    {t:"fill",q:"The children ___ (be) in the classroom now.",a:"are"},
    {t:"mc",q:"Which is correct? \"There ___ two apples.\"",opts:["are","is","am"],a:0},
    {t:"read",pass:"Sally is a careful girl. She does her homework slowly but neatly. Her teacher is proud of her.",qs:[
      {q:"How does Sally do her homework?",opts:["slowly and neatly","quickly and badly","loudly"],a:0},
      {q:"Who is proud of Sally?",opts:["her teacher","her mother","her friend"],a:0}]},
    {t:"fill",q:"They ___ (watch) TV now.",a:"are watching"},
    {t:"mc",q:"「方便的」的英文是？",opts:["convenient","correct","common","careful"],a:0}
  ],
  P5:[
    {t:"read",pass:"Pollution is a big problem in cities. Many people use cars every day. We should take the bus or train to protect the environment. Planting trees also helps.",qs:[
      {q:"What is a big problem in cities?",opts:["pollution","rain","noise"],a:0},
      {q:"How can we help the environment?",opts:["take bus or train","drive more cars","cut more trees"],a:0},
      {q:"Give ONE way to protect the environment.",opts:["plant trees","use more plastic","burn rubbish"],a:0}]},
    {t:"mc",q:"「環境」的英文是？",opts:["environment","equipment","experience","evidence"],a:0},
    {t:"mc",q:"Mary ___ (write) the letter yesterday.",opts:["wrote","write","written"],a:0},
    {t:"fill",q:"I have ___ (live) here for 5 years.",a:"lived"},
    {t:"mc",q:"「建議」的英文是？",opts:["suggest","protect","prevent","predict"],a:0},
    {t:"read",pass:"He ___ (1) up early and ___ (2) breakfast.",qs:[
      {q:"(1)",opts:["woke","wake","wakes"],a:0},
      {q:"(2)",opts:["ate","eat","eats"],a:0}]},
    {t:"write",q:"Write a paragraph (about 60 words) about your last summer holiday.",guide:["where you went","what you did","how you felt"],model:"Last summer, I went to Sanya with my family. We swam in the sea and built sandcastles. The weather was sunny and warm. I felt very happy and relaxed. It was a wonderful holiday."},
    {t:"mc",q:"「減少」的英文是？",opts:["reduce","reuse","recycle","refuse"],a:0},
    {t:"fill",q:"She is good ___ maths.",a:"at"},
    {t:"mc",q:"「方便的」的英文是？",opts:["convenient","correct","common","careful"],a:0},
    {t:"mc",q:"He ran ___ (quick).",opts:["quickly","quick","quicker"],a:0},
    {t:"fill",q:"She has ___ (finish) her homework already.",a:"finished"},
    {t:"mc",q:"「雖然」的英文是？",opts:["although","because","if","so"],a:0},
    {t:"read",pass:"Lisa studied hard, so she got good marks. She was happy because her parents praised her.",qs:[
      {q:"Why did Lisa get good marks?",opts:["she studied hard","she was lucky","she guessed"],a:0},
      {q:"How did she feel?",opts:["happy","sad","angry"],a:0}]},
    {t:"fill",q:"We should ___ (reuse) plastic bags.",a:"reuse"},
    {t:"mc",q:"「代表」的英文是？",opts:["represent","respect","repeat","report"],a:0},
    {t:"write",q:"Write 2 sentences about how to save energy.",guide:["one action","one reason"],model:"We can turn off lights when we leave a room. This saves electricity and protects the Earth."},
    {t:"mc",q:"「污染」的英文是？",opts:["pollution","solution","education","population"],a:0},
    {t:"fill",q:"We ___ (go) to the park yesterday.",a:"went"},
    {t:"mc",q:"「保護」的英文是？",opts:["protect","prevent","provide","prepare"],a:0}
  ],
  P6:[
    {t:"read",pass:"Climate change is affecting the world. Many animals are in danger. We must save energy and use renewable power. Everyone can make a difference by small actions.",qs:[
      {q:"What is affecting the world?",opts:["climate change","population","war"],a:0},
      {q:"What should we use more?",opts:["renewable power","coal","oil"],a:0},
      {q:"What can YOU do?",opts:["small daily actions","nothing","move away"],a:0}]},
    {t:"mc",q:"「代表」的英文是？",opts:["represent","respect","repeat","report"],a:0},
    {t:"mc",q:"___ it was raining, we went out.",opts:["Although","Because","If"],a:0},
    {t:"fill",q:"Please ___ (turn) off the light.",a:"turn"},
    {t:"mc",q:"「氣候變化」的英文是？",opts:["climate change","climate control","weather report","season change"],a:0},
    {t:"write",q:"Write a formal email to your principal asking for leave.",guide:["greeting","reason for leave","polite closing"],model:"Dear Principal, I am writing to ask for leave on Friday because I have a medical appointment. I will return to school on Monday. Thank you for your understanding. Yours sincerely, Chan Tai Man"},
    {t:"mc",q:"「責任」的英文是？",opts:["responsibility","ability","possibility","activity"],a:0},
    {t:"fill",q:"He has lived here ___ 2010.",a:"since"},
    {t:"mc",q:"「雖然」的英文是？",opts:["although","however","therefore","moreover"],a:0},
    {t:"write",q:"Describe a person you admire (about 80 words).",guide:["who the person is","why you admire him or her","give one example"],model:"I admire my mother. She is a nurse and works very hard to help sick people. Once, she stayed at the hospital all night to care for patients. She is kind and responsible. I want to be like her when I grow up."},
    {t:"mc",q:"The boy ___ is wearing a red shirt is my brother.",opts:["who","which","where","when"],a:0},
    {t:"fill",q:"This is the book ___ I bought yesterday. (which / who)",a:"which"},
    {t:"mc",q:"「減少」的英文是？",opts:["reduce","reuse","recycle","refuse"],a:0},
    {t:"read",pass:"John, who is my best friend, moved to another city. We still talk on the phone, which makes me happy.",qs:[
      {q:"Who moved to another city?",opts:["John","the teacher","my brother"],a:0},
      {q:"How do they keep in touch?",opts:["on the phone","by email","by letter"],a:0}]},
    {t:"fill",q:"If it ___ (rain) tomorrow, we will stay home.",a:"rains"},
    {t:"mc",q:"「方便的」的英文是？",opts:["convenient","correct","common","careful"],a:0},
    {t:"write",q:"Write a short paragraph (about 60 words) on 'My Dream Job'.",guide:["what job","why you like it","what you will do"],model:"My dream job is to be a doctor. I want to help sick people get better. I will study hard and learn a lot about medicine. I believe this job is meaningful and I will be proud of it."},
    {t:"mc",q:"「保護」的英文是？",opts:["protect","prevent","provide","prepare"],a:0},
    {t:"fill",q:"We should ___ (save) energy.",a:"save"},
    {t:"mc",q:"「可再生」的英文是？",opts:["renewable","recycle","reduce","reuse"],a:0}
  ]
};
const EN_GRADE_TOPICS = {
  P1:["現在簡單式 am/is/are","現在進行式","方位介詞 in/on/under","顏色與物件詞彙","a / an"],
  P2:["動詞表（現簡/現進）","所有格 's","方位介詞 in/on/at/between","可數/不可數 some/any","複數名詞","can / can't"],
  P3:["過去式（規則/不規則 went/ate/saw）","時間介詞 on/in/at","wh- 問句","there is / are","短文閱讀"],
  P4:["比較級 / 最高級","過去式敘事","現在完成式初階","副詞（manner）","較長閱讀","開放短答"],
  P5:["現在完成式 for / since","副詞（manner）","連接詞 because/so/but","閱讀理解","約 60 字寫作"],
  P6:["since / for","連接詞 although/because/if","關係代詞 who/which","時事閱讀（氣候/SSPA）","正式電郵","約 80 字寫作"]
};


const EN_EDB = {
  P4:[
    {t:'read',src:'EDB 中國寓言系列',pass:`Han Xin was a poor young man who often went hungry. When he had no food, he went to the river to catch fish, but he was usually empty-handed. One day, an old woman at the river felt sorry for him and said, "Poor young man, you look so thin! Please have a bowl of rice." From then on, she gave him rice whenever she saw him, and said, "I don't expect you to repay me. You should find a way to support yourself and remember to help others." Han Xin was grateful and promised to work hard in return. Later, he joined the army and gave strategic advice to Liu Bang, who became the first emperor of the Han Dynasty. Han Xin was given land and made a king. He went back to find the old woman and offered her gold, but she smiled and said, "You have already paid me back by becoming a strong and kind king."`,qs:[
      {q:"What problem did Han Xin face when he was young?",opts:["He did not have enough food to eat.","He did not have enough clothes.","He could not go fishing.","He had no toys."],a:0},
      {q:"What did young Han Xin do to solve his problem?",opts:["He begged people for food.","He washed clothes for money.","He went to the river to catch fish.","He cooked rice for the old woman."],a:2},
      {q:"Why was Han Xin grateful to the old woman?",opts:["She gave him rice every time.","She did not expect repayment.","She encouraged him to be kind.","All of the above."],a:3},
      {q:"Fill in: The _____ of his early life taught him to become a kind person.",opts:["humbleness","toughness","politeness","willingness"],a:1}
    ]},
    {t:'read',src:'EDB 中國寓言系列',pass:`Chen Yaozi was one of the best archers in his village in the Northern Song Dynasty. All the villagers cheered and praised him, and he was very proud of himself. One day, an old pitchman watched him hit the target eight or nine times out of ten arrows, but only nodded slightly. The pitchman then showed Chen how he could pour oil through a small coin hole without spilling a drop. "This is nothing," said the old pitchman. "I have just been pouring oil for a long time. Practice makes perfect." Chen Yaozi was embarrassed and apologised, realising he should practise with modesty.`,qs:[
      {q:"Chen Yaozi was _____.",opts:["an archer","a pitchman","a viewer","a teacher"],a:0},
      {q:"How did people think about Chen's archery?",opts:["It was poor.","It was average.","It was slightly above average.","It was excellent."],a:3},
      {q:"How could the old pitchman pour oil without spilling a drop?",opts:["He had secrets behind.","He played tricks.","He had practised very hard.","He did not pour at all."],a:2},
      {q:"Fill in: Chen was _____ about the old pitchman's comment because he expected praise.",opts:["embarrassed","frustrated","inspired","disappointed"],a:0}
    ]},
    {t:'read',src:'EDB 中國寓言系列',pass:`In ancient China, a young farmer's family had farmed for generations. Farmers sowed in spring and harvested in autumn, working from sunrise to sunset. One day, a big fat hare ran past him in panic and bumped into a tree stump; its neck broke and it died. The farmer grabbed it, cooked a delicious meal, and thought, "My luck comes at last! I need not work hard. All I have to do is wait by the stump for another hare." He abandoned his fields, put away his tools, and stayed by the stump. But no more hares came, and his fields grew thick with weeds.`,qs:[
      {q:"What is TRUE about farmers' life?",opts:["They collected crops in spring.","They put seeds in autumn.","They worked from sunrise.","They returned home when hot."],a:2},
      {q:"What happened to the scared hare?",opts:["It got lost in the woods.","It hit the farmer hard.","It hit the stump hard.","It was caught by hunters."],a:2},
      {q:"What happened to the farmer's abandoned fields?",opts:["Wild plants grew in them.","Crops were grown.","More hares died there.","There was a great harvest."],a:0},
      {q:"Which best describes the farmer after getting a hare?",opts:["He became selfish.","He became proactive.","He became idle and gave up farming.","He became a brave hunter."],a:2}
    ]},
    {t:'read',src:'EDB 中國寓言系列',pass:`Kuang Heng was a poor peasant child who could not afford school, but he was eager to learn. He sneaked into a neighbour's school to listen, and a kind teacher let him borrow books every day and ask questions. Kuang Heng farmed during the day and read at night, but his family was too poor for lamp oil. One night, he noticed light coming through a crack in the wall from his neighbour. Overjoyed, he dug the crack bigger to read by that light. Thanks to it, he read many books, passed the imperial exams, and became an imperial officer.`,qs:[
      {q:'What does "grass-roots families" mean?',opts:["Poor families.","Rich families.","Families that grow crops.","Families that raise horses."],a:0},
      {q:"Why did Kuang Heng sneak into the school?",opts:["He was afraid of disturbing others.","He could not pay the fees.","He was late for school.","He had not finished homework."],a:1},
      {q:"Which adjective best describes the teacher?",opts:["Worried","Honest","Selfish","Supportive"],a:3},
      {q:"Fill in: _____ Kuang Heng was sitting on the bed, he found light through the wall.",opts:["So","Although","If","While"],a:3}
    ]}
  ],
  P5:[
    {t:'read',src:'EDB 中國寓言系列',pass:`An old man called Sai Weng raised horses for a living. When he lost his most valuable horse, neighbours came to comfort him, but he was not sad and said, "Although my horse is lost, it might be a good thing." Later, the horse returned with a fine new horse, and neighbours congratulated him. Then his son rode the new horse, fell, and broke his leg badly. Sai Weng again said it might be good. Soon, the emperor's army recruited able-bodied young men, but his son did not join because of his injury. "They may be a blessing in disguise," said Sai Weng.`,qs:[
      {q:"What did Sai Weng do for a living?",opts:["He took care of horses.","He raced horses.","He rode horses.","He trained horses."],a:0},
      {q:'What does "misfortune" mean?',opts:["A pleasant event.","An unlucky event.","An annoying event.","A funny event."],a:1},
      {q:"How did Sai Weng feel when losing his horse?",opts:["Upset","Brave","Worried","Calm"],a:3},
      {q:'Fill in: "_____! What a beautiful horse!" exclaimed the neighbours.',opts:["Oh","Phew","Wow","Ouch"],a:2}
    ]},
    {t:'read',src:'EDB 中國寓言系列',pass:`Long ago, a ninety-year-old man called Yu Gong lived north of two high mountains. They blocked his way, so he decided to move them with his family. They dug rocks and threw earth to the Sea of Bohai. A neighbouring widow's eight-year-old son gladly helped. A wise man called Zhi Sou teased Yu Gong, saying he was too old. But Yu Gong replied that his descendants would continue forever, and the mountains would not grow taller. The Emperor of Heaven was moved and helped them. They proved that perseverance can move mountains.`,qs:[
      {q:"Where did Yu Gong live?",opts:["East of the mountains.","South of the mountains.","West of the mountains.","North of the mountains."],a:3},
      {q:"Why did he want to move the mountains?",opts:["Hard to get around them.","They were too rounded.","Easy to pass through.","They were too short."],a:0},
      {q:"Where did they put the earth and rocks?",opts:["Near the mountains.","Sea of Taihang.","Sea of Wangwu.","Sea of Bohai."],a:3},
      {q:"Fill in: Yu Gong decided to move mountains for generations; he was _____.",opts:["stouthearted","hardheaded","warm-hearted","tongue-tied"],a:0}
    ]},
    {t:'read',src:'EDB 中國寓言系列',pass:`The King of Chu and his officials lived a luxurious life while ignoring the state. A loyal official Zhuang Xin warned him, but the King did not listen. Within six months, the King of Qin invaded and occupied the territory. The King escaped to a small city and regretted not taking Zhuang Xin's advice. He invited Zhuang Xin back. Zhuang Xin told a story: a shepherd found a hole in his pen, lost a sheep, but his wife blocked the hole with her body, and he mended it. Zhuang Xin said, "If we reform now and strengthen our army, we can win the territory back." The King took his advice and succeeded.`,qs:[
      {q:"Why did Zhuang Xin leave the King?",opts:["The King guarded his territory.","The King enjoyed life all the time.","The King built a wall.","The King escaped."],a:1},
      {q:"What happened to the King's territory?",opts:["It became stronger.","It became part of Yang.","Enemies invaded it.","Zhuang ruled it."],a:2},
      {q:"What did the King do after remembering Zhuang's words?",opts:["He comforted himself.","He found Zhuang in Yang.","He invited Zhuang back.","He cried."],a:2},
      {q:"Fill in: Zhuang Xin thought the King was very _____responsible.",opts:["ir-","un-","dis-","in-"],a:1}
    ]}
  ],
  P6:[
    {t:'read',src:'EDB 中國寓言系列',pass:`During the Warring States Period, states formed alliances to avoid war. The Prince of Wei was sent to Zhao as a hostage. Pang Cong, who accompanied him, knew there were rumours slandering him in the palace, and feared the King would believe them. He asked the King: "If one person says there is a tiger on the street, would you believe it? What if three people say so?" The King admitted he would be doubtful. After Pang Cong left, many spoke ill of him; though the King doubted at first, his heart was shaken, and he alienated Pang Cong. The lesson: do not believe hearsay; seek truth from reliable sources.`,qs:[
      {q:"Why did states form alliances?",opts:["To cease wars.","To initiate wars.","To attack each other.","To weaken power."],a:0},
      {q:"Who was sent to Zhao as a hostage?",opts:["The king himself.","The king's son.","The king's daughter.","The king's father."],a:1},
      {q:"What did Pang Cong worry about?",opts:["A tiger would appear.","The King would believe rumours.","He could not return.","People would slander him."],a:1},
      {q:'"misery" is a synonym of _____.',opts:["uncertain","unions","dependable","unhappiness"],a:3}
    ]},
    {t:'read',src:'EDB 中國寓言系列',pass:`Long ago, great floods left many people homeless, forced to flee to mountaintops. Emperor Yao appointed his distant relative Gun to control the floods, but Gun spent nine years building embankments and failed. Emperor Shun then appointed Gun's son Yu as commander-in-chief. Yu led people over mountains, measured rivers, and dredged and widened them to divert floods to the sea. He was frugal, spent savings on water control, and left his new wife after four days. He passed his home three times but did not go in, for fear of delaying his task. People called him Yu the Great and he founded the Xia Dynasty.`,qs:[
      {q:"Why did people escape to mountaintops?",opts:["There was a great flood.","There were hills and valleys.","There was heavy rain.","They were homeless."],a:0},
      {q:"Who was Yu?",opts:["The current emperor.","Gun's father.","Gun's son.","The emperor's friend."],a:2},
      {q:"What did Yu do to tame the flood?",opts:["He built embankments.","He let the flood breach the dike.","He went under the sea.","He dredged and widened rivers to the sea."],a:3},
      {q:"Fill in: Yu was the _____ of flood control.",opts:["floodwater","newborn","commander-in-chief","mountaintops"],a:2}
    ]},
    {t:'read',src:'EDB 中國寓言系列',pass:`Mulan's father was a retired general, sick and frail, but he insisted on teaching her to ride and use a sword, believing everyone should know how to fight. When the military listed her father's name, Mulan disguised herself as a man and reported for duty secretly. In the army, her bravery reached the emperor, who gave her awards and let her return home. Her family greeted her with joy. When soldiers escorted her back, they were shocked to see her in women's clothes. Mulan's story shows courage, care and responsibility.`,qs:[
      {q:"Mulan knew how to fight because _____.",opts:["she learnt it in the army","her father taught her","she learnt by herself","a leader trained her"],a:1},
      {q:"What did Mulan do after seeing her father's name on the list?",opts:["She encouraged her brother.","She disguised as a man and joined.","She told her father to report.","She told officials her father was sick."],a:1},
      {q:"Why did Mulan receive awards from the emperor?",opts:["She worked at home.","She studied in the army.","She tried to protect the country.","She served the emperor."],a:2},
      {q:"Fill in: Mulan's father was a retired general _____ had come home sick.",opts:["which","who","when","where"],a:1}
    ]}
  ]
};

/* ===== 數學卷題庫（雙語對照·本地仿編原創·按 P1–P6 常見教學進度分級） ===== */
/* 版權與性質：非評估局（HKEAA）或學校真卷；題目為仿編原創練習題，年級難度為常見教學進度估算。 */
const MATH_QBANK = {
  P1:[
    {t:'mc',q:"There are 23 red balloons and 15 blue balloons. How many balloons are there altogether?",qzh:"有 23 個紅氣球和 15 個藍氣球，一共有多少個氣球？",opts:["38","35","40","33"],optszh:["38","35","40","33"],a:0},
    {t:'fill',q:"7 + ____ = 12",qzh:"7 + ____ = 12",a:"5",azh:"5"},
    {t:'mc',q:"Which shape has 4 equal sides and 4 corners?",qzh:"哪一個圖形有 4 條等長的邊和 4 個角？",opts:["Square","Triangle","Circle","Rectangle"],optszh:["正方形","三角形","圓形","長方形"],a:0},
    {t:'fill',q:"What is 10 less than 46?",qzh:"46 減少 10 是多少？",a:"36",azh:"36"},
    {t:'mc',q:"Amy has one $1 coin and two $2 coins. How much money does she have?",qzh:"Amy 有 1 個 $1 硬幣和 2 個 $2 硬幣，她共有多少錢？",opts:["$5","$6","$4","$7"],optszh:["$5","$6","$4","$7"],a:1},
    {t:'word',q:"Sam has 18 sweets. He gives 5 sweets to his sister. How many sweets does Sam have left? Show your working.",qzh:"Sam 有 18 粒糖，他給了妹妹 5 粒。Sam 還剩下多少粒糖？請寫出計算過程。",model:"18 - 5 = 13. Sam has 13 sweets left.",modelzh:"18 − 5 = 13，Sam 剩下 13 粒糖。"},
    {t:'mc',q:"The clock shows 3 o'clock. What time is it?",qzh:"時鐘顯示 3 點正，現在是幾點？",opts:["3:00","3:30","2:00","4:00"],optszh:["3:00","3:30","2:00","4:00"],a:0},
    {t:'fill',q:"Write the number 'seventy-two' in figures.",qzh:"把「七十二」寫成數字。",a:"72",azh:"72"},
    {t:'mc',q:"Which is the smallest number?",qzh:"下列哪一項數字最小？",opts:["25","52","35","45"],optszh:["25","52","35","45"],a:0},
    {t:'word',q:"There are 4 rows of chairs. Each row has 5 chairs. How many chairs are there in total?",qzh:"有 4 排椅子，每排 5 張。一共有多少張椅子？",model:"4 × 5 = 20 chairs.",modelzh:"4 × 5 = 20，共 20 張椅子。"}
  ],
  P2:[
    {t:'mc',q:"What is 6 × 7?",qzh:"6 × 7 等於多少？",opts:["42","36","48","40"],optszh:["42","36","48","40"],a:0},
    {t:'fill',q:"24 ÷ 4 = ____",qzh:"24 ÷ 4 = ____",a:"6",azh:"6"},
    {t:'mc',q:"If 1 out of 4 equal parts is shaded, what fraction is shaded?",qzh:"若一個圖形 4 等分中 1 份塗上顏色，塗色部分是幾分之幾？",opts:["1/4","1/2","3/4","1/3"],optszh:["四分之一","二分之一","四分之三","三分之一"],a:0},
    {t:'fill',q:"1 metre = ____ centimetres.",qzh:"1 米 = ____ 厘米。",a:"100",azh:"100"},
    {t:'mc',q:"A bag of rice weighs 2 kg. How many grams is that?",qzh:"一袋米重 2 公斤，即是多少克？",opts:["2000","200","20","20000"],optszh:["2000","200","20","20000"],a:0},
    {t:'word',q:"A book costs $28. Tom pays with a $50 note. How much change does he get?",qzh:"一本書售價 $28，Tom 用 $50 紙幣付款，他應找回多少零錢？",model:"$50 - $28 = $22. He gets $22 change.",modelzh:"50 − 28 = 22，找回 $22。"},
    {t:'mc',q:"The time is 20 minutes past 4. What is it in digital form?",qzh:"時間是 4 點 20 分，用數字表示是？",opts:["4:20","4:40","3:20","4:05"],optszh:["4:20","4:40","3:20","4:05"],a:0},
    {t:'fill',q:"What is 1/2 of 18?",qzh:"18 的一半是多少？",a:"9",azh:"9"},
    {t:'mc',q:"Which solid has a circular base?",qzh:"下列哪一個立體有圓形的底面？",opts:["Cylinder","Cube","Cuboid","Pyramid"],optszh:["圓柱","立方體","長方體","角錐"],a:0},
    {t:'word',q:"There are 3 packets of biscuits. Each packet has 8 biscuits. How many biscuits are there altogether?",qzh:"有 3 包餅乾，每包 8 块。一共有多少塊餅乾？",model:"3 × 8 = 24 biscuits.",modelzh:"3 × 8 = 24，共 24 塊餅乾。"}
  ],
  P3:[
    {t:'mc',q:"What is 456 + 378?",qzh:"456 + 378 等於多少？",opts:["834","824","844","814"],optszh:["834","824","844","814"],a:0},
    {t:'fill',q:"0.6 + 0.4 = ____",qzh:"0.6 + 0.4 = ____",a:"1",azh:"1",alt:["1.0"]},
    {t:'mc',q:"Which is larger: 3/5 or 2/5?",qzh:"3/5 和 2/5 哪一個較大？",opts:["3/5","2/5","They are the same.","Cannot tell."],optszh:["3/5","2/5","兩者相同","無法判斷"],a:0},
    {t:'fill',q:"Find the perimeter of a rectangle 6 cm by 4 cm. (Answer in cm)",qzh:"一個長方形長 6 厘米、寬 4 厘米，求周長（以厘米作答）。",a:"20",azh:"20",alt:["20 cm","20cm"]},
    {t:'mc',q:"What is 9 × 8?",qzh:"9 × 8 等於多少？",opts:["72","64","81","63"],optszh:["72","64","81","63"],a:0},
    {t:'word',q:"A box contains 120 sweets. They are shared equally among 6 children. How many sweets does each child get?",qzh:"一盒有 120 粒糖，平均分給 6 個小朋友，每人得多少粒？",model:"120 ÷ 6 = 20. Each child gets 20 sweets.",modelzh:"120 ÷ 6 = 20，每人 20 粒。"},
    {t:'mc',q:"What time is 14:30 in the afternoon?",qzh:"24 小時制 14:30 是下午幾點？",opts:["2:30 p.m.","1:30 p.m.","3:30 p.m.","12:30 p.m."],optszh:["下午 2:30","下午 1:30","下午 3:30","下午 12:30"],a:0},
    {t:'fill',q:"1 kg = ____ g",qzh:"1 公斤 = ____ 克",a:"1000",azh:"1000"},
    {t:'mc',q:"Which unit is used to measure area?",qzh:"量度面積應使用下列哪一個單位？",opts:["cm²","cm","mL","g"],optszh:["平方厘米","厘米","毫升","克"],a:0},
    {t:'word',q:"Mei saves $15 each week. How much does she save in 8 weeks?",qzh:"Mei 每週儲蓄 $15，8 週共儲了多少？",model:"8 × $15 = $120.",modelzh:"8 × 15 = 120，共儲 $120。"}
  ],
  P4:[
    {t:'mc',q:"What is 2.5 × 4?",qzh:"2.5 × 4 等於多少？",opts:["10","9","8","11"],optszh:["10","9","8","11"],a:0},
    {t:'fill',q:"Round 7.86 to the nearest tenth.",qzh:"把 7.86 捨入至最接近的十分位。",a:"7.9",azh:"7.9",alt:["7.90"]},
    {t:'mc',q:"3/8 + 2/8 = ?",qzh:"3/8 + 2/8 = ？",opts:["5/8","5/16","1/2","6/8"],optszh:["5/8","5/16","1/2","6/8"],a:0},
    {t:'fill',q:"How many right angles does a rectangle have?",qzh:"一個長方形有幾個直角？",a:"4",azh:"4"},
    {t:'mc',q:"Which number is a multiple of 6?",qzh:"下列哪一個數是 6 的倍數？",opts:["24","25","22","23"],optszh:["24","25","22","23"],a:0},
    {t:'word',q:"A rectangular field is 50 m long and 30 m wide. Find its area.",qzh:"一塊長方形農地長 50 米、寬 30 米，求它的面積。",model:"50 × 30 = 1500 m².",modelzh:"50 × 30 = 1500 平方米。"},
    {t:'mc',q:"Two angles on a straight line are 110° and ____. Find the missing angle.",qzh:"在一條直線上，兩個角分別是 110° 和 ____，求未知角。",opts:["70°","60°","80°","90°"],optszh:["70°","60°","80°","90°"],a:0},
    {t:'fill',q:"Give one factor of 12.",qzh:"寫出 12 的一個因數。",a:"3",azh:"3",alt:["1","2","4","6","12"]},
    {t:'mc',q:"How many lines of symmetry does an equilateral triangle have?",qzh:"一個等邊三角形有多少條對稱軸？",opts:["3","1","2","0"],optszh:["3","1","2","0"],a:0},
    {t:'word',q:"A bottle holds 1.5 L of water. How many millilitres is that?",qzh:"一個瓶子裝有 1.5 升水，即是多少毫升？",model:"1.5 L = 1500 mL.",modelzh:"1.5 升 = 1500 毫升。"}
  ],
  P5:[
    {t:'mc',q:"What is 1/2 + 1/3?",qzh:"1/2 + 1/3 等於多少？",opts:["5/6","2/5","1/6","3/5"],optszh:["5/6","2/5","1/6","3/5"],a:0},
    {t:'fill',q:"Find 20% of 80.",qzh:"求 80 的 20%。",a:"16",azh:"16"},
    {t:'mc',q:"What is the average of 12, 18 and 20?",qzh:"12、18 和 20 的平均數是多少？",opts:["16.67","16","17","15"],optszh:["16.67","16","17","15"],a:0},
    {t:'fill',q:"The ratio of boys to girls is 3:2. If there are 15 boys, how many girls are there?",qzh:"男生與女生的比例是 3:2。若有 15 名男生，女生有多少人？",a:"10",azh:"10"},
    {t:'mc',q:"Which has the largest volume?",qzh:"下列哪一項容積最大？",opts:["2 L","1500 mL","1.8 L","1200 mL"],optszh:["2 升","1500 毫升","1.8 升","1200 毫升"],a:0},
    {t:'word',q:"A shirt costs $120. It is sold at a 25% discount. What is the selling price?",qzh:"一件襯衫售價 $120，打 25% 折扣出售，售價是多少？",model:"Discount = 25% × $120 = $30; Selling price = $120 - $30 = $90.",modelzh:"折扣 = 25% × 120 = 30 元；售價 = 120 − 30 = 90 元。"},
    {t:'mc',q:"How many sides does a hexagon have?",qzh:"一個六邊形有多少條邊？",opts:["6","5","7","8"],optszh:["6","5","7","8"],a:0},
    {t:'fill',q:"Solve: x + 7 = 15. x = ____",qzh:"解方程：x + 7 = 15，x = ____",a:"8",azh:"8"},
    {t:'mc',q:"What is 0.4 × 0.5?",qzh:"0.4 × 0.5 等於多少？",opts:["0.20","0.9","2.0","0.02"],optszh:["0.20","0.9","2.0","0.02"],a:0},
    {t:'word',q:"The total of 5 numbers is 100. What is their average?",qzh:"5 個數的總和是 100，它們的平均數是多少？",model:"100 ÷ 5 = 20.",modelzh:"100 ÷ 5 = 20。"}
  ],
  P6:[
    {t:'mc',q:"A circle has radius 7 cm. What is its circumference? (Take π = 3.14)",qzh:"一個圓半徑為 7 厘米，它的周長是多少？（取 π = 3.14）",opts:["43.96","21.98","49","14"],optszh:["43.96","21.98","49","14"],a:0},
    {t:'fill',q:"A car travels 240 km in 3 hours. Its speed is ____ km/h.",qzh:"一輛車 3 小時行駛 240 公里，它的時速是 ____ 公里/小時。",a:"80",azh:"80"},
    {t:'mc',q:"What is 30% of 250?",qzh:"250 的 30% 是多少？",opts:["75","70","80","65"],optszh:["75","70","80","65"],a:0},
    {t:'fill',q:"Solve: 3x = 21. x = ____",qzh:"解方程：3x = 21，x = ____",a:"7",azh:"7"},
    {t:'mc',q:"A bag has 3 red and 2 blue balls. What is the probability of picking a red ball?",qzh:"袋中共有 3 個紅球和 2 個藍球，抽到紅球的概率是多少？",opts:["3/5","2/5","1/2","1/5"],optszh:["3/5","2/5","1/2","1/5"],a:0},
    {t:'word',q:"A shop buys a toy for $40 and sells it for $52. Find the profit and the profit percentage.",qzh:"一間店以 $40 買入一件玩具，以 $52 賣出。求利潤及利潤率。",model:"Profit = $52 - $40 = $12. Profit% = 12 / 40 × 100% = 30%.",modelzh:"利潤 = 52 − 40 = 12 元；利潤率 = 12 / 40 × 100% = 30%。"},
    {t:'mc',q:"What is -5 + 8?",qzh:"-5 + 8 等於多少？",opts:["3","-3","13","-13"],optszh:["3","-3","13","-13"],a:0},
    {t:'fill',q:"Find the area of a circle with radius 7 cm. (Take π = 3.14)",qzh:"求半徑 7 厘米的圓的面積。（取 π = 3.14）",a:"153.86",azh:"153.86",alt:["153.86 cm²","153.86cm²"]},
    {t:'mc',q:"A cuboid measures 4 cm by 3 cm by 2 cm. What is its volume?",qzh:"一個長方體長 4 厘米、闊 3 厘米、高 2 厘米，它的體積是多少？",opts:["24 cm³","18 cm³","26 cm³","12 cm³"],optszh:["24 立方厘米","18 立方厘米","26 立方厘米","12 立方厘米"],a:0},
    {t:'word',q:"The ratio of flour to sugar is 2:1. If 300 g of flour is used, how much sugar is needed?",qzh:"麵粉與糖的比例是 2:1。若用了 300 克麵粉，需要多少克糖？",model:"300 ÷ 2 = 150 g of sugar.",modelzh:"300 ÷ 2 = 150 克糖。"}
  ]
};

let curMathGrade='P1', curMathPaper=[], _mathPrintBound=false;
function prepMcMath(q){const idx=q.opts.map((_,i)=>i);const sh=shuffle(idx);const opts=sh.map(i=>q.opts[i]);const optszh=sh.map(i=>q.optszh[i]);return Object.assign({},q,{opts:opts,optszh:optszh,a:sh.indexOf(q.a)});}
function genMathPaper(){
  if(!licActive()){showLicLock('licLockMath','math');return;}
  const pool=(MATH_QBANK[curMathGrade]||[]);
  if(!pool.length){alert('該年級題庫暫空。');return;}
  const picked=shuffle(pool).slice(0,Math.min(8,pool.length));
  curMathPaper=picked.map(function(q){ if(q.t==='mc')return prepMcMath(q); return Object.assign({},q); });
  document.getElementById('mathPaperResult').innerHTML='';
  renderMathPaper();
  showMathStat();
}
const LAB_M=['A','B','C','D','E','F'];
function mathCardHtml(q,i){
  const TL={mc:"選擇題",fill:"填空題",word:"應用題"};
  let h='<div class="qcard" data-qi="'+i+'"><div class="qhead"><span class="qn">Q'+(i+1)+'.</span><span class="qtype">'+(TL[q.t]||"")+'</span></div>';
  if(q.t==='mc'){
    h+='<div class="qtext">'+q.q+'</div><div class="qzh">'+q.qzh+'</div><div class="qopts">';
    q.opts.forEach(function(o,k){ h+='<label class="qopt"><input type="radio" name="mq'+i+'" value="'+k+'"> '+LAB_M[k]+'. '+o+' <span class="qzh">('+q.optszh[k]+')</span></label>'; });
    h+='</div>';
  }else if(q.t==='fill'){
    h+='<div class="qtext">'+q.q+'</div><div class="qzh">'+q.qzh+'</div><input class="qfill" id="mqf'+i+'" placeholder="填答案">';
  }else if(q.t==='word'){
    h+='<div class="qtext">'+q.q+'</div><div class="qzh">'+q.qzh+'</div><div class="qwrite"><textarea id="mqf'+i+'" placeholder="寫下你的算式與答案…"></textarea></div>';
  }
  h+='</div>';
  return h;
}
function renderMathPaper(){
  const box=document.getElementById('mathPaperBox');
  if(!curMathPaper.length){box.innerHTML='<div class="qtip">選年級後按「🎲 出新卷」生成練習卷。</div>';return;}
  box.innerHTML=curMathPaper.map(mathCardHtml).join('');
}
function gradeMathPaper(){
  if(!curMathPaper.length){alert('請先按「🎲 出新卷」生成練習卷。');return;}
  let correct=0, scored=0;
  curMathPaper.forEach(function(q,i){
    const card=document.querySelector('.qcard[data-qi="'+i+'"]');
    if(q.t==='mc'){
      const sel=card.querySelector('input[name="mq'+i+'"]:checked');
      scored++; const ok=sel&&+sel.value===q.a; if(ok)correct++;
      card.querySelectorAll('.qopt').forEach(function(op,k){ if(k===q.a)op.classList.add('correct'); else if(sel&&+sel.value===k)op.classList.add('wrong'); });
      card.insertAdjacentHTML('beforeend', ok?'<div class="qans"><span class="ok">✓ 正確</span></div>':'<div class="qans"><span class="no">✗ 正確答案：'+q.opts[q.a]+'（'+q.optszh[q.a]+'）</span></div>');
    }else if(q.t==='fill'){
      const inp=document.getElementById('mqf'+i); const v=norm(inp.value);
      scored++; const ok=v===norm(q.a)||(q.alt&&q.alt.some(function(x){return norm(x)===v;})); if(ok)correct++;
      inp.classList.add(ok?'correct':'wrong');
      card.insertAdjacentHTML('beforeend', ok?'<div class="qans"><span class="ok">✓ 正確</span></div>':'<div class="qans"><span class="no">✗ 正確答案：'+(q.a||'')+(q.azh?('（'+q.azh+'）'):'')+'</span></div>');
    }else if(q.t==='word'){
      card.insertAdjacentHTML('beforeend','<div class="qans"><span class="no">✎ 應用題（不計分，對照參考答案自評）</span><br>參考：'+(q.model||'')+'<br><span class="qzh">'+(q.modelzh||'')+'</span></div>');
    }
  });
  const pct=scored?Math.round(correct/scored*100):0;
  document.getElementById('mathPaperResult').innerHTML='<div class="qtot">得分：'+correct+' / '+scored+' 題正確（'+pct+'%）</div><div class="qbar"><i style="width:'+pct+'%"></i></div>';
  const BK='hkk_mathpaper_v0'; let best=JSON.parse(localStorage.getItem(BK)||'{}');
  if(!(curMathGrade in best)||pct>best[curMathGrade]){best[curMathGrade]=pct;localStorage.setItem(BK,JSON.stringify(best));}
  showMathStat();
}
function showMathStat(){
  const best=JSON.parse(localStorage.getItem('hkk_mathpaper_v0')||'{}');
  const v=best[curMathGrade];
  document.getElementById('mathStat').textContent='本級最佳：'+(v!==undefined?v+'%':'—');
}
function printMathPaper(){
  if(!licActive()){showLicLock('licLockMath','math');return;}
  if(!curMathPaper.length) genMathPaper();
  if(!curMathPaper.length){ alert('題庫暫時無法出卷。'); return; }
  const withAns=document.getElementById('mathPrintAns').checked;
  const TL={mc:"選擇題",fill:"填空題",word:"應用題"};
  const LAB=['A','B','C','D','E','F'];
  function optsLine(opts,optszh){ return opts.map(function(o,k){return LAB[k]+'. '+o+' ('+optszh[k]+')';}).join('　　'); }
  const totalQ=curMathPaper.length, totalMarks=curMathPaper.length;
  let h='<div class="eps-head"><div class="eps-title">香港小學數學練習卷'+(withAns?'（答案版）':'')+'</div>'
       +'<div class="eps-meta">年級：<b>'+curMathGrade+'</b>　　姓名：________________　　日期：______________　　共 '+totalQ+' 題／'+totalMarks+' 分</div></div>';
  curMathPaper.forEach(function(q,i){
    h+='<div class="eps-q"><div class="eps-qh">Q'+(i+1)+'. （'+(TL[q.t]||'')+'）</div>';
    if(q.t==='mc'){
      h+='<div class="eps-text">'+q.q+'</div><div class="qzh">'+q.qzh+'</div><div class="eps-opts">'+optsLine(q.opts,q.optszh)+'</div><div class="eps-ans">答：____</div>';
    }else if(q.t==='fill'){
      h+='<div class="eps-text">'+q.q+'</div><div class="qzh">'+q.qzh+'</div><div class="eps-ans">答：________________________</div>';
    }else if(q.t==='word'){
      h+='<div class="eps-text">'+q.q+'</div><div class="qzh">'+q.qzh+'</div><div class="eps-ans"><br>______________________________<br>______________________________<br>______________________________</div>';
    }
    h+='</div>';
  });
  if(withAns){
    h+='<div class="eps-aksheet"><div class="eps-ak-title">答案卷 · '+curMathGrade+'（共 '+totalQ+' 題）</div>';
    curMathPaper.forEach(function(q,i){
      h+='<div class="eps-ak-row"><b>Q'+(i+1)+'.</b> ';
      if(q.t==='mc') h+=q.opts[q.a]+' ('+q.optszh[q.a]+')';
      else if(q.t==='fill') h+=(q.a||'')+(q.azh?(' ('+q.azh+')'):'');
      else if(q.t==='word') h+='參考：'+(q.model||'')+(q.modelzh?(' ｜ '+q.modelzh):'');
      h+='</div>';
    });
    h+='</div>';
  }
  document.getElementById('mathPrintSheet').innerHTML=h;
  if(!_mathPrintBound){_mathPrintBound=true;window.addEventListener('afterprint',function(){document.body.classList.remove('printing-paper');});}
  document.body.classList.add('printing-paper');
  if(typeof window.print==='function')window.print();else setTimeout(function(){document.body.classList.remove('printing-paper');},300);
}

let curEnGrade='P1', curEnPaper=[];
function shuffle(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));const t=a[i];a[i]=a[j];a[j]=t;}return a;}
function prepMc(q){const idx=q.opts.map((_,i)=>i);const sh=shuffle(idx);const opts=sh.map(i=>q.opts[i]);return Object.assign({},q,{opts:opts,a:sh.indexOf(q.a)});}
function prepRead(q){return Object.assign({},q,{qs:q.qs.map(prepMc)});}
function genEnPaper(){
  if(!licActive()){showLicLock('licLockEn','en');return;}
  let picked;
  if(curEnGrade==='ALL'){
    picked=[];
    ['P1','P2','P3','P4','P5','P6'].forEach(function(g){
      const pool=(EN_QBANK[g]||[]).concat(EN_EDB[g]||[]);
      shuffle(pool).slice(0,2).forEach(function(q){ picked.push(Object.assign({},q,{grade:g})); });
    });
  }else{
    const pool=(EN_QBANK[curEnGrade]||[]).concat(EN_EDB[curEnGrade]||[]);
    picked=shuffle(pool).slice(0,Math.min(8,pool.length));
  }
  curEnPaper=picked.map(function(q){const g=q.grade||curEnGrade;const o=Object.assign({},q,{grade:g});if(o.t==='mc')return prepMc(o);if(o.t==='read')return prepRead(o);return o;});
  document.getElementById('enPaperResult').innerHTML='';
  renderEnPaper();
  showEnStat();
  renderEnGradeTopic();
}
function enCardHtml(q,i){
  const TL={mc:"選擇",fill:"填空",read:"閱讀",open:"短答",write:"寫作"};
  let h='<div class="qcard" data-qi="'+i+'" data-grade="'+(q.grade||'')+'"><div class="qhead"><span class="qn">Q'+(i+1)+'.</span><span class="qtype">'+(TL[q.t]||"")+'</span><span class="qswap"><button class="mini" onclick="localSwap('+i+')">🔄 換一題</button><button class="mini ai" onclick="aiSwap('+i+')">🤖 AI 換題</button></span></div>';
  if(q.t==='read'){
    h+='<div class="qpass">'+q.pass+' <button class="listen-btn" onclick=\'speak('+JSON.stringify(q.pass)+',"en-US")\'>🔊</button></div>'+ (q.src?'<div class="qsrc">來源：'+q.src+'（教育局版權·僅教學用途）</div>':'')
    q.qs.forEach((sub,j)=>{
      h+='<div class="qsub" data-sj="'+j+'"><div class="qtext">'+(i+1)+'.'+(j+1)+' '+sub.q+'</div><div class="qopts">';
      sub.opts.forEach((o,k)=>{h+='<label class="qopt"><input type="radio" name="q'+i+'_'+j+'" value="'+k+'"> '+o+'</label>';});
      h+='</div></div>';
    });
  }else if(q.t==='mc'){
    h+='<div class="qtext">'+q.q+'</div><div class="qopts">';
    q.opts.forEach((o,k)=>{h+='<label class="qopt"><input type="radio" name="q'+i+'" value="'+k+'"> '+o+'</label>';});
    h+='</div>';
  }else if(q.t==='fill'){
    h+='<div class="qtext">'+q.q+'</div><input class="qfill" id="qf'+i+'" placeholder="填英文">';
  }else if(q.t==='open'){
    h+='<div class="qtext">'+q.q+'</div><input class="qfill" id="qf'+i+'" placeholder="用英文簡答">';
  }else if(q.t==='write'){
    h+='<div class="qtext">'+q.q+'</div>';
    if(q.guide&&q.guide.length)h+='<div class="qtip">引導：'+q.guide.join(' · ')+'</div>';
    h+='<div class="qwrite"><textarea id="qf'+i+'" placeholder="在此寫作…"></textarea></div>';
  }
  h+='</div>';
  return h;
}
function renderEnPaper(){
  const box=document.getElementById('enPaperBox');
  if(!curEnPaper.length){box.innerHTML='<div class="qtip">選年級後按「🎲 出新卷」生成練習卷。</div>';return;}
  let html='', prevGrade=null;
  curEnPaper.forEach((q,i)=>{
    if(curEnGrade==='ALL' && q.grade!==prevGrade){ html+='<div class="qsec">'+q.grade+' 年級</div>'; prevGrade=q.grade; }
    html+=enCardHtml(q,i);
  });
  box.innerHTML=html;
}
function norm(s){return (s||'').toString().trim().toLowerCase().replace(/\.+$/,'').replace(/\s+/g,' ');}
function gradeEnPaper(){
  if(!curEnPaper.length){alert('請先按「🎲 出新卷」生成練習卷。');return;}
  let correct=0, scored=0;
  curEnPaper.forEach((q,i)=>{
    const card=document.querySelector('.qcard[data-qi="'+i+'"]');
    if(q.t==='mc'){
      const sel=card.querySelector('input[name="q'+i+'"]:checked');
      scored++;const ok=sel&&+sel.value===q.a; if(ok)correct++;
      card.querySelectorAll('.qopt').forEach((op,k)=>{if(k===q.a)op.classList.add('correct');else if(sel&&+sel.value===k)op.classList.add('wrong');});
      card.insertAdjacentHTML('beforeend', ok?'<div class="qans"><span class="ok">✓ 正確</span></div>':'<div class="qans"><span class="no">✗ 正確答案：'+q.opts[q.a]+'</span></div>');
    }else if(q.t==='read'){
      q.qs.forEach((sub,j)=>{
        const subEl=card.querySelector('.qsub[data-sj="'+j+'"]');
        const sel=subEl.querySelector('input:checked');
        scored++;const ok=sel&&+sel.value===sub.a; if(ok)correct++;
        subEl.querySelectorAll('.qopt').forEach((op,k)=>{if(k===sub.a)op.classList.add('correct');else if(sel&&+sel.value===k)op.classList.add('wrong');});
      });
    }else if(q.t==='fill'){
      const inp=document.getElementById('qf'+i);const v=norm(inp.value);
      scored++;const ok=v===norm(q.a)||(q.alt&&q.alt.some(x=>norm(x)===v)); if(ok)correct++;
      inp.classList.add(ok?'correct':'wrong');
      card.insertAdjacentHTML('beforeend', ok?'<div class="qans"><span class="ok">✓ 正確</span></div>':'<div class="qans"><span class="no">✗ 正確答案：'+q.a+'</span></div>');
    }else if(q.t==='open'){
      card.insertAdjacentHTML('beforeend','<div class="qans"><span class="no">✎ 開放題（不計分）</span> 參考：'+(q.model||'')+'</div>');
    }else if(q.t==='write'){
      card.insertAdjacentHTML('beforeend','<div class="qans"><span class="no">✎ 寫作（不計分，對照範文自評）</span></div><div class="qwrite">範文：\n'+(q.model||'')+'</div>');
    }
  });
  const pct=scored?Math.round(correct/scored*100):0;
  document.getElementById('enPaperResult').innerHTML='<div class="qtot">得分：'+correct+' / '+scored+' 題正確（'+pct+'%）</div><div class="qbar"><i style="width:'+pct+'%"></i></div>';
  const BK='hkk_enpaper_v0';let best=JSON.parse(localStorage.getItem(BK)||'{}');
  if(!(curEnGrade in best)||pct>best[curEnGrade]){best[curEnGrade]=pct;localStorage.setItem(BK,JSON.stringify(best));}
  showEnStat();
}
function showEnStat(){
  const best=JSON.parse(localStorage.getItem('hkk_enpaper_v0')||'{}');
  const v=best[curEnGrade];
  document.getElementById('enStat').textContent='本級最佳：'+(v!==undefined?v+'%':'—');
}
function renderEnGradeTopic(){
  const el=document.getElementById('enGradeTopic'); if(!el)return;
  if(curEnGrade==='ALL'){ el.innerHTML='綜合卷：涵蓋 P1–P6 各年級常見主題（坊間參考）'; return; }
  const t=(typeof EN_GRADE_TOPICS!=='undefined'&&EN_GRADE_TOPICS[curEnGrade])||[];
  el.innerHTML='本年級常見主題（坊間參考）：'+t.map(function(x){return '<span class="gtag">'+x+'</span>';}).join('');
}

let _enPrintBound=false;
function printEnPaper(){
  if(!licActive()){showLicLock('licLockEn','en');return;}
  // 一次性打印一套：若尚未出卷，先自動出一套再印，無須先按「出新卷」
  if(!curEnPaper.length){ genEnPaper(); }
  if(!curEnPaper.length){ alert('題庫暫時無法出卷，請稍後再試。'); return; }
  const withAns=document.getElementById('enPrintAns').checked;
  const TL={mc:"選擇題",fill:"填空題",read:"閱讀理解",open:"短答題",write:"寫作題"};
  const LAB=['A','B','C','D','E','F'];
  function optsLine(opts){return opts.map((o,k)=>LAB[k]+'. '+o).join('　　');}
  // 題數與總分（閱讀每小題 1 分，其餘每題 1 分）
  let totalQ=curEnPaper.length, totalMarks=0;
  curEnPaper.forEach(q=>{ totalMarks += (q.t==='read' ? q.qs.length : 1); });
  // —— 題卷 ——
  const gLabel=(curEnGrade==='ALL'?'綜合 P1–P6':curEnGrade);
  let h='<div class="eps-head"><div class="eps-title">香港小學英文練習卷'+(withAns?'（答案版）':'')+'</div>'
       +'<div class="eps-meta">年級：<b>'+gLabel+'</b>　　姓名：________________　　日期：______________　　共 '+totalQ+' 題／'+totalMarks+' 分</div></div>';
  let prevG=null;
  curEnPaper.forEach((q,i)=>{
    if(curEnGrade==='ALL' && q.grade!==prevG){ h+='<div class="eps-sec">'+q.grade+' 年級</div>'; prevG=q.grade; }
    h+='<div class="eps-q"><div class="eps-qh">Q'+(i+1)+'. （'+(TL[q.t]||'')+'）</div>';
    if(q.t==='read'){
      h+='<div class="eps-pass">'+q.pass+'</div>'+ (q.src?'<div class="eps-src">來源：'+q.src+'（教育局版權·僅教學用途·檢索 2026-10-31）</div>':'')
      q.qs.forEach((sub,j)=>{ h+='<div class="eps-text">'+(i+1)+'.'+(j+1)+' '+sub.q+'</div><div class="eps-opts">'+optsLine(sub.opts)+'</div><div class="eps-ans">答：____</div>'; });
    }else if(q.t==='mc'){
      h+='<div class="eps-text">'+q.q+'</div><div class="eps-opts">'+optsLine(q.opts)+'</div><div class="eps-ans">答：____</div>';
    }else if(q.t==='fill'){
      h+='<div class="eps-text">'+q.q+'</div><div class="eps-ans">答：________________________</div>';
    }else if(q.t==='open'){
      h+='<div class="eps-text">'+q.q+'</div><div class="eps-ans">答：<br>______________________________<br>______________________________</div>';
    }else if(q.t==='write'){
      h+='<div class="eps-text">'+q.q+'</div>';
      if(q.guide&&q.guide.length)h+='<div class="eps-tip">引導：'+q.guide.join(' · ')+'</div>';
      h+='<div class="eps-ans"><br>______________________________<br>______________________________<br>______________________________<br>______________________________</div>';
    }
    h+='</div>';
  });
  // —— 答案卷（含答案版時獨立成頁）——
  if(withAns){
    h+='<div class="eps-aksheet"><div class="eps-ak-title">答案卷 · '+gLabel+'（共 '+totalQ+' 題／'+totalMarks+' 分）</div>';
    curEnPaper.forEach((q,i)=>{
      h+='<div class="eps-ak-row"><b>Q'+(i+1)+'.</b> ';
      if(q.t==='read'){ h+=q.qs.map((sub,k)=>((i+1)+'.'+(k+1)+' '+LAB[sub.a])).join('　　'); }
      else if(q.t==='mc'){ h+=LAB[q.a]+'. '+q.opts[q.a]; }
      else if(q.t==='fill'){ h+=q.a; }
      else if(q.t==='open'){ h+=(q.model||'（開放題，無標準答案）'); }
      else if(q.t==='write'){ h+=(q.model?('範文：'+q.model):'（寫作題，無標準答案）'); }
      h+='</div>';
    });
    h+='</div>';
  }
  document.getElementById('enPrintSheet').innerHTML=h;
  if(!_enPrintBound){_enPrintBound=true;window.addEventListener('afterprint',function(){document.body.classList.remove('printing-paper');});}
  document.body.classList.add('printing-paper');
  if(typeof window.print==='function')window.print();else setTimeout(function(){document.body.classList.remove('printing-paper');},300);
}

// ---- 英文卷：換一題（本地）＋ AI 換題（OpenAI 兼容） ----
function getAiCfg(){ try{return JSON.parse(localStorage.getItem('hkk_ai_cfg')||'{}');}catch(e){return {};} }
function saveAiCfg(){ const cfg={base:(document.getElementById('aiBase').value||'').trim(),key:(document.getElementById('aiKey').value||'').trim(),model:(document.getElementById('aiModel').value||'').trim()}; localStorage.setItem('hkk_ai_cfg',JSON.stringify(cfg)); const m=document.getElementById('aiCfgMsg'); if(m)m.textContent='已保存（本瀏覽器）'; }
function clearAiCfg(){ localStorage.removeItem('hkk_ai_cfg'); ['aiBase','aiKey','aiModel'].forEach(function(id){const e=document.getElementById(id); if(e)e.value='';}); const m=document.getElementById('aiCfgMsg'); if(m)m.textContent='已清除'; }
function swapCard(i,q){ curEnPaper[i]=q; const box=document.getElementById('enPaperBox'); const old=box.querySelector('.qcard[data-qi="'+i+'"]'); if(old) old.outerHTML=enCardHtml(q,i); }
function localSwap(i){
  const cur=curEnPaper[i]; if(!cur)return; const g=cur.grade||curEnGrade; const t=cur.t;
  const pool=(EN_QBANK[g]||[]).concat(EN_EDB[g]||[]).filter(function(x){return x.t===t;});
  if(!pool.length){ alert('該年級該題型暫無其他題，可試 🤖 AI 換題。'); return; }
  let cand=null, sig=cur.t==='read'?cur.pass:(cur.q||'');
  for(let k=0;k<10;k++){ const p=pool[Math.floor(Math.random()*pool.length)]; const ps=p.t==='read'?p.pass:(p.q||''); if(ps!==sig){cand=p;break;} }
  if(!cand){ alert('該年級該題型暫無其他題，可試 🤖 AI 換題。'); return; }
  let o=Object.assign({},cand,{grade:g});
  if(o.t==='mc')o=prepMc(o); else if(o.t==='read')o=prepRead(o);
  swapCard(i,o);
}
function aiPrompt(g,t){
  const sys='You are an expert author of English exercises for Hong Kong primary school students. Return ONLY a JSON object (no markdown, no explanation) matching the requested schema. Keep vocabulary appropriate to the grade level (P1 easiest to P6 hardest).';
  let usr='';
  if(t==='mc') usr='Create one multiple-choice question for grade '+g+' (Hong Kong primary). Schema: {"t":"mc","q":"question text","opts":["A","B","C","D"],"a":correctIndex0to3}. Use exactly 4 options.';
  else if(t==='fill') usr='Create one fill-in-the-blank question for grade '+g+'. Schema: {"t":"fill","q":"sentence with ____ for the blank","a":"correct answer word or phrase"}.';
  else if(t==='read') usr='Create one reading comprehension item for grade '+g+'. Schema: {"t":"read","pass":"short passage 60-90 words age-appropriate","qs":[{"q":"sub question","opts":["A","B","C","D"],"a":correctIndex0to3}]} with 2-3 sub-questions, each exactly 4 options.';
  else if(t==='open') usr='Create one short-answer question for grade '+g+'. Schema: {"t":"open","q":"question","model":"sample answer 1-2 sentences"}.';
  else usr='Create one writing task for grade '+g+'. Schema: {"t":"write","q":"writing prompt","guide":["tip1","tip2"],"model":"model paragraph 40-80 words"}.';
  return [{role:'system',content:sys},{role:'user',content:usr}];
}
async function aiGenQuestion(g,t){
  const cfg=getAiCfg();
  if(!cfg.base||!cfg.key||!cfg.model) return null;
  const body={model:cfg.model, messages:aiPrompt(g,t), temperature:0.8};
  try{ body.response_format={type:'json_object'}; }catch(e){}
  let resp;
  try{ resp=await fetch(cfg.base.replace(/\/$/,'')+'/chat/completions',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+cfg.key},body:JSON.stringify(body)}); }
  catch(e){ return null; }
  if(!resp||!resp.ok) return null;
  let data; try{ data=await resp.json(); }catch(e){ return null; }
  let content=data&&data.choices&&data.choices[0]&&data.choices[0].message&&data.choices[0].message.content;
  if(!content) return null;
  content=content.trim().replace(/^```(?:json)?/i,'').replace(/```$/i,'').trim();
  let obj; try{ obj=JSON.parse(content); }catch(e){ return null; }
  if(!obj||obj.t!==t) return null;
  if(t==='mc' && (!Array.isArray(obj.opts)||typeof obj.a!=='number')) return null;
  if(t==='read' && (!obj.pass||!Array.isArray(obj.qs))) return null;
  return obj;
}
async function aiSwap(i){
  const cur=curEnPaper[i]; if(!cur)return; const g=cur.grade||curEnGrade; const t=cur.t;
  const btn=document.querySelector('.qcard[data-qi="'+i+'"] .qswap .ai');
  const oldTxt=btn?btn.textContent:'';
  if(btn){ btn.disabled=true; btn.textContent='生成中…'; }
  try{
    const q=await aiGenQuestion(g,t);
    if(btn){ btn.disabled=false; btn.textContent=oldTxt; }
    if(!q){ if(!getAiCfg().key){ alert('尚未配置 AI 接口。請點開下方「⚙ AI 設置」填寫 Base URL／密鑰／模型（僅存本瀏覽器）。'); } else { alert('AI 生成失敗，可改用 🔄 換一題（本地）。'); } return; }
    let o=Object.assign({},q,{grade:g});
    if(o.t==='mc')o=prepMc(o); else if(o.t==='read')o=prepRead(o);
    swapCard(i,o);
  }catch(e){ if(btn){ btn.disabled=false; btn.textContent=oldTxt; } alert('AI 換題出錯：'+(e&&e.message?e.message:e)+'（常見原因：CORS 或密鑰問題）'); }
}

// ---- 繁體字 簡→繁 高頻對照（常用字，以香港課本用字為準） ----
const FT_MAP=[
 ['国','國'],['学','學'],['体','體'],['来','來'],['们','們'],['东','東'],['车','車'],['说','說'],
 ['时','時'],['会','會'],['这','這'],['里','裡'],['发','發'],['长','長'],['风','風'],['爱','愛'],
 ['开','開'],['关','關'],['电','電'],['见','見'],['亲','親'],['贝','貝'],['页','頁'],['马','馬'],
 ['鸟','鳥'],['鱼','魚'],['书','書'],['门','門'],['问','問'],['间','間'],['闻','聞'],['岁','歲'],
 ['历','歷'],['乐','樂'],['个','個'],['对','對'],['总','總'],['应','應'],['报','報'],['纸','紙'],
 ['图','圖'],['团','團'],['园','園'],['实','實'],['买','買'],['卖','賣'],['读','讀'],['写','寫'],
 ['话','話'],['语','語'],['讲','講'],['谢','謝'],['观','觀'],['认','認'],['识','識'],['远','遠'],
 ['进','進'],['过','過'],['还','還'],['边','邊'],['动','動'],['劳','勞'],['轻','輕'],['军','軍'],
 ['农','農'],['双','雙'],['难','難'],['颗','顆'],['怀','懷'],['礼','禮'],['视','視'],['课','課'],
 ['脸','臉'],['脑','腦'],['华','華'],['龙','龍'],['龟','龜'],['兰','蘭'],['检','檢'],['验','驗'],
 ['获','獲'],['梦','夢'],['乡','鄉'],['县','縣'],['类','類'],['红','紅'],['绿','綠'],['级','級'],
 ['结','結'],['续','續'],['绍','紹'],['译','譯'],['词','詞'],['诗','詩'],['觉','覺'],['声','聲'],
 ['养','養'],['义','義'],['兴','興'],['举','舉'],['汇','匯'],['惊','驚'],['护','護'],['术','術'],
 ['湿','濕'],['环','環'],['师','師'],['币','幣'],['胜','勝'],['复','復'],['杂','雜'],['备','備'],
 ['处','處'],['务','務'],['医','醫'],['药','藥'],['铁','鐵'],['银','銀'],['钢','鋼'],['针','針'],
 ['钟','鐘'],['镜','鏡'],['动','動'],['丽','麗'],['两岸','兩岸'],['后','後'],['只','隻'],['几','幾']
];

/* ===== 數學中↔英術語表（手編） ===== */
const MATH_TERMS = [
  // 數與運算
  {cat:'數與運算',zh:'整數',en:'integer',note:'正整數/負整數/零'},
  {cat:'數與運算',zh:'自然數',en:'natural number',note:''},
  {cat:'數與運算',zh:'質數（素數）',en:'prime number',note:''},
  {cat:'數與運算',zh:'合數',en:'composite number',note:''},
  {cat:'數與運算',zh:'因數',en:'factor',note:''},
  {cat:'數與運算',zh:'倍數',en:'multiple',note:''},
  {cat:'數與運算',zh:'公因數',en:'common factor',note:''},
  {cat:'數與運算',zh:'公倍數',en:'common multiple',note:''},
  {cat:'數與運算',zh:'最大公因數',en:'HCF / greatest common factor',note:'Highest Common Factor'},
  {cat:'數與運算',zh:'最小公倍數',en:'LCM / least common multiple',note:'Lowest Common Multiple'},
  {cat:'數與運算',zh:'奇數',en:'odd number',note:''},
  {cat:'數與運算',zh:'偶數',en:'even number',note:''},
  {cat:'數與運算',zh:'加法',en:'addition',note:''},
  {cat:'數與運算',zh:'減法',en:'subtraction',note:''},
  {cat:'數與運算',zh:'乘法',en:'multiplication',note:''},
  {cat:'數與運算',zh:'除法',en:'division',note:''},
  {cat:'數與運算',zh:'和',en:'sum',note:''},
  {cat:'數與運算',zh:'差',en:'difference',note:''},
  {cat:'數與運算',zh:'積',en:'product',note:''},
  {cat:'數與運算',zh:'商',en:'quotient',note:''},
  {cat:'數與運算',zh:'餘數',en:'remainder',note:''},
  {cat:'數與運算',zh:'平方',en:'square',note:''},
  {cat:'數與運算',zh:'立方',en:'cube',note:''},
  {cat:'數與運算',zh:'平方根',en:'square root',note:''},
  {cat:'數與運算',zh:'絕對值',en:'absolute value',note:''},
  {cat:'數與運算',zh:'倒數',en:'reciprocal',note:''},
  {cat:'數與運算',zh:'正數',en:'positive number',note:''},
  {cat:'數與運算',zh:'負數',en:'negative number',note:''},
  {cat:'數與運算',zh:'有理數',en:'rational number',note:''},
  {cat:'數與運算',zh:'無理數',en:'irrational number',note:''},
  {cat:'數與運算',zh:'實數',en:'real number',note:''},
  // 分數小數百分數
  {cat:'分數小數百分數',zh:'分數',en:'fraction',note:''},
  {cat:'分數小數百分數',zh:'分子',en:'numerator',note:''},
  {cat:'分數小數百分數',zh:'分母',en:'denominator',note:''},
  {cat:'分數小數百分數',zh:'真分數',en:'proper fraction',note:''},
  {cat:'分數小數百分數',zh:'假分數',en:'improper fraction',note:''},
  {cat:'分數小數百分數',zh:'帶分數',en:'mixed number',note:''},
  {cat:'分數小數百分數',zh:'小數',en:'decimal',note:''},
  {cat:'分數小數百分數',zh:'小數點',en:'decimal point',note:''},
  {cat:'分數小數百分數',zh:'四捨五入',en:'round / rounding',note:''},
  {cat:'分數小數百分數',zh:'百分數（百分比）',en:'percentage / percent',note:''},
  {cat:'分數小數百分數',zh:'百分點',en:'percentage point',note:''},
  {cat:'分數小數百分數',zh:'比率',en:'ratio',note:''},
  {cat:'分數小數百分數',zh:'比例',en:'proportion',note:''},
  {cat:'分數小數百分數',zh:'速率',en:'rate',note:''},
  // 代數
  {cat:'代數',zh:'代數',en:'algebra',note:''},
  {cat:'代數',zh:'變數（未知數）',en:'variable',note:''},
  {cat:'代數',zh:'常數',en:'constant',note:''},
  {cat:'代數',zh:'係數',en:'coefficient',note:''},
  {cat:'代數',zh:'項',en:'term',note:''},
  {cat:'代數',zh:'代數式（表達式）',en:'expression',note:''},
  {cat:'代數',zh:'方程（式）',en:'equation',note:''},
  {cat:'代數',zh:'不等式',en:'inequality',note:''},
  {cat:'代數',zh:'解方程',en:'solve the equation',note:''},
  {cat:'代數',zh:'線性方程',en:'linear equation',note:''},
  {cat:'代數',zh:'一次函數',en:'linear function',note:''},
  {cat:'代數',zh:'坐標',en:'coordinate',note:''},
  {cat:'代數',zh:'x 軸',en:'x-axis',note:''},
  {cat:'代數',zh:'y 軸',en:'y-axis',note:''},
  {cat:'代數',zh:'原點',en:'origin',note:''},
  {cat:'代數',zh:'直角坐標系',en:'rectangular coordinate system',note:''},
  {cat:'代數',zh:'斜率',en:'gradient / slope',note:''},
  {cat:'代數',zh:'截距',en:'intercept',note:''},
  {cat:'代數',zh:'多項式',en:'polynomial',note:''},
  {cat:'代數',zh:'因式分解',en:'factorisation',note:''},
  {cat:'代數',zh:'配方法',en:'completing the square',note:''},
  {cat:'代數',zh:'二次方程',en:'quadratic equation',note:''},
  {cat:'代數',zh:'公式',en:'formula',note:''},
  {cat:'代數',zh:'代入法',en:'substitution',note:''},
  // 幾何
  {cat:'幾何',zh:'點',en:'point',note:''},
  {cat:'幾何',zh:'線',en:'line',note:''},
  {cat:'幾何',zh:'線段',en:'line segment',note:''},
  {cat:'幾何',zh:'射線',en:'ray',note:''},
  {cat:'幾何',zh:'角',en:'angle',note:''},
  {cat:'幾何',zh:'直角',en:'right angle',note:''},
  {cat:'幾何',zh:'銳角',en:'acute angle',note:''},
  {cat:'幾何',zh:'鈍角',en:'obtuse angle',note:''},
  {cat:'幾何',zh:'平角',en:'straight angle',note:''},
  {cat:'幾何',zh:'三角形',en:'triangle',note:''},
  {cat:'幾何',zh:'直角三角形',en:'right-angled triangle',note:''},
  {cat:'幾何',zh:'等腰三角形',en:'isosceles triangle',note:''},
  {cat:'幾何',zh:'等邊三角形',en:'equilateral triangle',note:''},
  {cat:'幾何',zh:'四邊形',en:'quadrilateral',note:''},
  {cat:'幾何',zh:'正方形',en:'square',note:''},
  {cat:'幾何',zh:'長方形',en:'rectangle',note:''},
  {cat:'幾何',zh:'平行四邊形',en:'parallelogram',note:''},
  {cat:'幾何',zh:'梯形',en:'trapezoid / trapezium',note:''},
  {cat:'幾何',zh:'菱形',en:'rhombus',note:''},
  {cat:'幾何',zh:'圓',en:'circle',note:''},
  {cat:'幾何',zh:'圓心',en:'centre',note:''},
  {cat:'幾何',zh:'半徑',en:'radius',note:''},
  {cat:'幾何',zh:'直徑',en:'diameter',note:''},
  {cat:'幾何',zh:'圓周',en:'circumference',note:''},
  {cat:'幾何',zh:'圓周率',en:'pi (π)',note:''},
  {cat:'幾何',zh:'面積',en:'area',note:''},
  {cat:'幾何',zh:'周界（周長）',en:'perimeter',note:''},
  {cat:'幾何',zh:'體積',en:'volume',note:''},
  {cat:'幾何',zh:'表面積',en:'surface area',note:''},
  {cat:'幾何',zh:'平行',en:'parallel',note:''},
  {cat:'幾何',zh:'垂直',en:'perpendicular',note:''},
  {cat:'幾何',zh:'對稱',en:'symmetry',note:''},
  {cat:'幾何',zh:'軸對稱',en:'reflectional symmetry',note:''},
  {cat:'幾何',zh:'旋轉對稱',en:'rotational symmetry',note:''},
  {cat:'幾何',zh:'相似',en:'similar',note:''},
  {cat:'幾何',zh:'全等',en:'congruent',note:''},
  {cat:'幾何',zh:'畢氏定理',en:"Pythagoras' theorem",note:''},
  {cat:'幾何',zh:'正弦',en:'sine',note:''},
  {cat:'幾何',zh:'餘弦',en:'cosine',note:''},
  {cat:'幾何',zh:'正切',en:'tangent',note:''},
  {cat:'幾何',zh:'多邊形',en:'polygon',note:''},
  {cat:'幾何',zh:'頂點',en:'vertex',note:''},
  // 度量
  {cat:'度量',zh:'長度',en:'length',note:''},
  {cat:'度量',zh:'質量（重量）',en:'mass / weight',note:''},
  {cat:'度量',zh:'容量',en:'capacity',note:''},
  {cat:'度量',zh:'時間',en:'time',note:''},
  {cat:'度量',zh:'溫度',en:'temperature',note:''},
  {cat:'度量',zh:'公尺（米）',en:'metre',note:''},
  {cat:'度量',zh:'厘米',en:'centimetre',note:''},
  {cat:'度量',zh:'公里',en:'kilometre',note:''},
  {cat:'度量',zh:'毫米',en:'millimetre',note:''},
  {cat:'度量',zh:'公斤',en:'kilogram',note:''},
  {cat:'度量',zh:'克',en:'gram',note:''},
  {cat:'度量',zh:'升',en:'litre',note:''},
  {cat:'度量',zh:'毫升',en:'millilitre',note:''},
  {cat:'度量',zh:'速度',en:'speed',note:''},
  {cat:'度量',zh:'單位換算',en:'unit conversion',note:''},
  // 統計與概率
  {cat:'統計與概率',zh:'數據',en:'data',note:''},
  {cat:'統計與概率',zh:'統計',en:'statistics',note:''},
  {cat:'統計與概率',zh:'平均數',en:'mean / average',note:''},
  {cat:'統計與概率',zh:'中位數',en:'median',note:''},
  {cat:'統計與概率',zh:'眾數',en:'mode',note:''},
  {cat:'統計與概率',zh:'全距（極差）',en:'range',note:''},
  {cat:'統計與概率',zh:'頻數',en:'frequency',note:''},
  {cat:'統計與概率',zh:'頻數表',en:'frequency table',note:''},
  {cat:'統計與概率',zh:'棒形圖',en:'bar chart',note:''},
  {cat:'統計與概率',zh:'複合棒形圖',en:'compound bar chart',note:''},
  {cat:'統計與概率',zh:'折線圖',en:'line graph',note:''},
  {cat:'統計與概率',zh:'扇形圖（圓形圖）',en:'pie chart',note:''},
  {cat:'統計與概率',zh:'直方圖',en:'histogram',note:''},
  {cat:'統計與概率',zh:'箱形圖',en:'box-and-whisker plot',note:''},
  {cat:'統計與概率',zh:'概率（機會率）',en:'probability',note:''},
  {cat:'統計與概率',zh:'必然事件',en:'certain event',note:''},
  {cat:'統計與概率',zh:'不可能事件',en:'impossible event',note:''},
  {cat:'統計與概率',zh:'隨機',en:'random',note:''},
];
// 高頻術語英文例句（坊間整理，輔助記憶；以課本例句為準）
const MATH_EX={
  'integer':'e.g. −3, 0, 5 are integers', 'natural number':'e.g. 1, 2, 3, …',
  'prime number':'e.g. 2, 3, 5, 7', 'factor':'e.g. 2 is a factor of 6',
  'multiple':'e.g. 6 is a multiple of 3', 'square':'e.g. 3² = 9',
  'addition':'e.g. 2 + 3 = 5', 'subtraction':'e.g. 5 − 2 = 3',
  'multiplication':'e.g. 2 × 3 = 6', 'division':'e.g. 12 ÷ 3 = 4',
  'sum':'e.g. sum of 2 and 3 is 5', 'difference':'e.g. difference of 5 and 2 is 3',
  'product':'e.g. product of 2 and 3 is 6', 'quotient':'e.g. 12 ÷ 3 = 4',
  'fraction':'e.g. 1/2, 3/4', 'numerator':'top number of a fraction',
  'denominator':'bottom number of a fraction', 'decimal':'e.g. 0.5',
  'percentage / percent':'e.g. 50% means 50/100', 'ratio':'e.g. 2:3',
  'algebra':'using letters for numbers', 'variable':'e.g. x in 2x + 1',
  'coefficient':'e.g. 3 in 3x', 'equation':'e.g. 2x + 3 = 7',
  'linear equation':'e.g. y = 2x + 1', 'coordinate':'e.g. point (3, 4)',
  'triangle':'a 3-sided polygon', 'right angle':'e.g. a 90° corner',
  'circle':'a round shape', 'radius':'centre to edge', 'diameter':'twice the radius',
  'area':'e.g. area of rectangle = length × width', 'perimeter':'sum of all sides',
  'volume':'space inside a 3D shape', 'parallel':'lines that never meet',
  'perpendicular':'lines at 90°', 'mean / average':'e.g. mean of 2,4,6 = 4',
  'median':'middle value when ordered', 'mode':'most frequent value',
  'probability':'e.g. P(head) = 1/2', 'data':'a collection of facts'
};

const PKEY='hkk_poem_v0', VKEY='hkk_vocab_v0', HKEY='hkk_hkword_v0', MKEY='hkk_math_v0';
let pProg = JSON.parse(localStorage.getItem(PKEY)||'{}');
let vProg = JSON.parse(localStorage.getItem(VKEY)||'{}');
let hProg = JSON.parse(localStorage.getItem(HKEY)||'{}');
let mProg = JSON.parse(localStorage.getItem(MKEY)||'{}'); // 數術語掌握：key=索引
let curFilter='all', curPoem=null;
let clozeOn=false, clozeReveal=false;
const FOCUS_GRADE='六年級'; // 小六為升中銜接重點年級，卡片標籤高亮

function saveP(){localStorage.setItem(PKEY,JSON.stringify(pProg));}
function saveV(){localStorage.setItem(VKEY,JSON.stringify(vProg));}
function saveH(){localStorage.setItem(HKEY,JSON.stringify(hProg));}
function saveM(){localStorage.setItem(MKEY,JSON.stringify(mProg));}

// ---- 朗讀（Web Speech API） ----
function speak(text,lang){
  if(!('speechSynthesis' in window)){alert('此瀏覽器不支援語音朗讀');return;}
  try{
    window.speechSynthesis.cancel();
    const u=new SpeechSynthesisUtterance(text); u.lang=lang||'en-US';
    const vs=window.speechSynthesis.getVoices()||[];
    if(lang==='zh-HK'){const v=vs.find(x=>x.lang==='zh-HK'||x.lang==='zh-Hant-HK');if(v)u.voice=v;}
    window.speechSynthesis.speak(u);
  }catch(e){}
}
function speakPoem(){
  if(!curPoem)return;
  speak(curPoem.lines.map(l=>l.text).join('。'), 'zh-HK');
}

// ---- 主導航 + 子導航 ----
let curTab='guide', curGuide='cn', curPractice='cn', curPlan='timeline';
function showMain(m){
  curTab=m;
  document.querySelectorAll('nav button').forEach(x=>x.classList.toggle('on',x.dataset.tab===m));
  document.getElementById('guideView').style.display = m==='guide'?'block':'none';
  document.getElementById('planView').style.display = m==='plan'?'block':'none';
  document.getElementById('practiceView').style.display = m==='practice'?'block':'none';
  document.getElementById('progressView').style.display = m==='progress'?'block':'none';
  document.getElementById('funView').style.display = m==='fun'?'block':'none';
  document.getElementById('guideSub').style.display = m==='guide'?'flex':'none';
  document.getElementById('planSub').style.display = m==='plan'?'flex':'none';
  document.getElementById('practiceSub').style.display = m==='practice'?'flex':'none';
  if(m==='progress')renderProgress();
}

// ---- 單詞貪吃蛇（悠閒 · 邊玩邊記） ----
(function(){
  const cv=document.getElementById('snakeCanvas'), ctx=cv.getContext('2d');
  const hasCtx=!!ctx;
  const G=16, C=cv.width/G;
  let snake, dir, food, timer, running=false, score=0, roundWords=[];
  const bestKey='hkk_snake_best';
  let best=+localStorage.getItem(bestKey)||0;
  document.getElementById('snakeBest').textContent=best;
  function rndWord(){ return HK[Math.floor(Math.random()*HK.length)]; }
  function placeFood(){
    const w=rndWord(); let x,y,tries=0;
    do{ x=Math.floor(Math.random()*G); y=Math.floor(Math.random()*G); tries++; }
    while(snake && snake.some(s=>s.x===x&&s.y===y) && tries<50);
    food={w:w.w, zh:w.zh, id:w.id, x, y};
    document.getElementById('snakeWord').innerHTML='去吃：<b>'+food.w+'</b> ＝ '+food.zh;
  }
  function reset(){
    snake=[{x:8,y:8},{x:7,y:8},{x:6,y:8}]; dir={x:1,y:0}; score=0; roundWords=[];
    document.getElementById('snakeScore').textContent=0;
    document.getElementById('snakeMaster').disabled=true;
    document.getElementById('snakeMasterN').textContent=0;
    placeFood(); draw();
  }
  function draw(){
    if(!hasCtx)return;
    ctx.fillStyle='#0f2a22'; ctx.fillRect(0,0,cv.width,cv.height);
    if(food){ ctx.fillStyle='#f2c14e'; ctx.fillRect(food.x*C, food.y*C, C-2, C-2); }
    snake.forEach((s,i)=>{ ctx.fillStyle=i===0?'#5ad6a0':'#2f9e74'; ctx.fillRect(s.x*C, s.y*C, C-2, C-2); });
  }
  function die(){
    running=false; clearInterval(timer);
    if(score>best){best=score; localStorage.setItem(bestKey,best); document.getElementById('snakeBest').textContent=best;}
    document.getElementById('snakeWord').innerHTML='結束！本局吃到 <b>'+score+'</b> 詞。';
  }
  function step(){
    const head={x:snake[0].x+dir.x, y:snake[0].y+dir.y};
    if(head.x<0||head.y<0||head.x>=G||head.y>=G) return die();
    if(snake.some(s=>s.x===head.x&&s.y===head.y)) return die();
    snake.unshift(head);
    if(food && head.x===food.x && head.y===food.y){
      score++; document.getElementById('snakeScore').textContent=score;
      roundWords.push(food.id);
      document.getElementById('snakeMaster').disabled=false;
      document.getElementById('snakeMasterN').textContent=roundWords.length;
      placeFood();
    } else { snake.pop(); }
    draw();
  }
  function setDir(d){ const map={up:{x:0,y:-1},down:{x:0,y:1},left:{x:-1,y:0},right:{x:1,y:0}}; const nd=map[d]; if(nd && !(nd.x===-dir.x&&nd.y===-dir.y)) dir=nd; }
  document.getElementById('snakeStart').onclick=()=>{ if(running)clearInterval(timer); running=true; reset(); timer=setInterval(step,130); };
  document.querySelectorAll('.spad').forEach(b=>b.onclick=()=>setDir(b.dataset.dir));
  document.addEventListener('keydown',e=>{ const k={ArrowUp:'up',ArrowDown:'down',ArrowLeft:'left',ArrowRight:'right'}; if(k[e.key]){e.preventDefault(); setDir(k[e.key]);} });
  document.getElementById('snakeMaster').onclick=()=>{
    roundWords.forEach(id=>hProg[id]=true); saveH();
    document.getElementById('stHk').textContent=Object.keys(hProg).filter(k=>hProg[k]).length;
    document.getElementById('snakeWord').innerHTML='已把本局 <b>'+roundWords.length+'</b> 詞標為「已掌握」✅';
    document.getElementById('snakeMaster').disabled=true;
  };
  reset();
})();
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>showMain(b.dataset.tab));
document.querySelectorAll('#guideSub button').forEach(b=>b.onclick=()=>{
  curGuide=b.dataset.sub;
  document.querySelectorAll('#guideSub button').forEach(x=>x.classList.toggle('on',x===b));
  ['cn','en','math','ft'].forEach(s=>document.getElementById(s+'View').style.display = s===curGuide?'block':'none');
});
document.querySelectorAll('#pgChips .chip').forEach(c=>c.onclick=()=>{
  curEnGrade=c.dataset.pg;
  document.querySelectorAll('#pgChips .chip').forEach(x=>x.classList.toggle('on',x===c));
  genEnPaper();
});
document.querySelectorAll('#practiceSub button').forEach(b=>b.onclick=()=>{
  curPractice=b.dataset.sub;
  document.querySelectorAll('#practiceSub button').forEach(x=>x.classList.toggle('on',x===b));
  document.getElementById('cnPracView').style.display = curPractice==='cn'?'block':'none';
  document.getElementById('enPracView').style.display = curPractice==='en'?'block':'none';
  document.getElementById('mathPracView').style.display = curPractice==='math'?'block':'none';
  if(curPractice==='en'){renderHk();renderVocab();}
});
document.querySelectorAll('#planSub button').forEach(b=>b.onclick=()=>{
  curPlan=b.dataset.sub;
  document.querySelectorAll('#planSub button').forEach(x=>x.classList.toggle('on',x===b));
  ['timeline','schools','docs','study','policy'].forEach(s=>document.getElementById(s+'View').style.display = s===curPlan?'block':'none');
});
// 英文練習內部分類切換（港小生字 / 詞表）
// ---- 授權碼（v1.21）：英文卷／數學卷為付費模組，激活碼格式 HKSS-YYYYMMDD-XXXXXXXX ----
// 防君子級校驗：碼 = HKSS-到期日-SHA256(密鑰|到期日)前8位；密鑰隨頁面分發，讀源碼者可自製碼，月付模式的真正護城河是持續更新
const LIC_SECRET='__LIC_SECRET__';
function sha256(ascii){
  function rightRotate(v,a){return (v>>>a)|(v<<(32-a));}
  var maxWord=Math.pow(2,32),result='',words=[],asciiBitLength=ascii.length*8,i,j;
  var hash=sha256.h=sha256.h||[],k=sha256.k=sha256.k||[],primeCounter=k.length,isComposite={};
  for(var candidate=2;primeCounter<64;candidate++){
    if(!isComposite[candidate]){
      for(i=0;i<313;i+=candidate)isComposite[i]=candidate;
      hash[primeCounter]=(Math.pow(candidate,.5)*maxWord)|0;
      k[primeCounter++]=(Math.pow(candidate,1/3)*maxWord)|0;
    }
  }
  ascii+='\x80';
  while(ascii.length%64-56)ascii+='\x00';
  for(i=0;i<ascii.length;i++){
    j=ascii.charCodeAt(i);
    if(j>>8)return;
    words[i>>2]|=j<<((3-i)%4)*8;
  }
  words[words.length]=(asciiBitLength/maxWord)|0;
  words[words.length]=asciiBitLength;
  for(j=0;j<words.length;){
    var w=words.slice(j,j+=16),oldHash=hash;
    hash=hash.slice(0,8);
    for(i=0;i<64;i++){
      var w15=w[i-15],w2=w[i-2],a=hash[0],e=hash[4];
      var temp1=hash[7]+(rightRotate(e,6)^rightRotate(e,11)^rightRotate(e,25))+((e&hash[5])^((~e)&hash[6]))+k[i]
        +(w[i]=(i<16)?w[i]:(w[i-16]+(rightRotate(w15,7)^rightRotate(w15,18)^(w15>>>3))+w[i-7]+(rightRotate(w2,17)^rightRotate(w2,19)^(w2>>>10)))|0);
      var temp2=(rightRotate(a,2)^rightRotate(a,13)^rightRotate(a,22))+((a&hash[1])^(a&hash[2])^(hash[1]&hash[2]));
      hash=[(temp1+temp2)|0].concat(hash);
      hash[4]=(hash[4]+temp1)|0;
    }
    for(i=0;i<8;i++)hash[i]=(hash[i]+oldHash[i])|0;
  }
  for(i=0;i<8;i++)for(j=3;j+1;j--){var b=(hash[i]>>(j*8))&255;result+=((b<16)?0:'')+b.toString(16);}
  return result;
}
function licMac(exp){return sha256(LIC_SECRET+'|'+exp).slice(0,8).toUpperCase();}
function licToday(){const t=new Date();return ''+t.getFullYear()+String(t.getMonth()+1).padStart(2,'0')+String(t.getDate()).padStart(2,'0');}
function licJudge(code){
  const m=/^HKSS-(\d{8})-([0-9A-Fa-f]{8})$/.exec((code||'').trim());
  if(!m)return 'invalid';
  if(m[1]<licToday())return 'expired';
  return licMac(m[1])===m[2].toUpperCase()?'ok':'invalid';
}
function licActive(){
  return licJudge(localStorage.getItem('hkk_lic')||'')==='ok';
}
function licLockHtml(kind){
  return '<div class="gtitle">🔒 付費內容 · 智能練習卷</div>'
    +'<p>英文卷／數學卷為<strong>按月訂閱</strong>模組，輸入激活碼解鎖；其餘模組（術語表／港小生字／詞表／古詩詞／進度）免費開放。</p>'
    +'<div class="lic-row"><input class="lic-input" placeholder="輸入激活碼，如 HKSS-20261231-1A2B3C4D"><button class="btn lic-btn" data-kind="'+kind+'">激活</button></div>'
    +'<div class="lic-msg"></div>'
    +'<p class="lic-tip">訂閱或獲取激活碼請聯絡葉工：hkeec2023@gmail.com（激活碼按月發放，到期後輸入新碼續期）</p>';
}
function showLicLock(id,kind){
  const p=document.getElementById(id);if(!p)return;
  p.innerHTML=licLockHtml(kind);
  document.getElementById(kind==='en'?'paperView':'mathPaperView').classList.add('locked');
}
function hideLicLock(kind){
  document.getElementById(kind==='en'?'paperView':'mathPaperView').classList.remove('locked');
}
function licTry(kind){
  const panel=document.getElementById(kind==='en'?'licLockEn':'licLockMath');
  const input=panel.querySelector('.lic-input'),msg=panel.querySelector('.lic-msg');
  const code=(input.value||'').trim();
  const judge=licJudge(code);
  if(judge==='ok'){
    localStorage.setItem('hkk_lic',code.toUpperCase());
    hideLicLock(kind);updateLicStatus();
    if(kind==='en'){if(!curEnPaper.length)genEnPaper();}else{if(!curMathPaper.length)genMathPaper();}
  }else{
    msg.textContent=judge==='expired'?'此激活碼已過期，請續購後輸入新碼。':'激活碼無效，請核對後重試（格式 HKSS-YYYYMMDD-XXXXXXXX）。';
  }
}
function updateLicStatus(){
  const m=/^HKSS-(\d{8})-/.exec((localStorage.getItem('hkk_lic')||'').trim());
  const txt=(licActive()&&m)?('已激活至 '+m[1].slice(0,4)+'-'+m[1].slice(4,6)+'-'+m[1].slice(6,8)):'未激活';
  ['licStatusEn','licStatusMath'].forEach(function(id){const el=document.getElementById(id);if(el)el.textContent=txt;});
}
updateLicStatus();
// 事件委託：激活按鈕與輸入框回車（面板 HTML 動態生成，委託到 document 免重綁）
document.addEventListener('click',function(e){
  const b=e.target&&e.target.closest?e.target.closest('.lic-btn'):null;
  if(b)licTry(b.dataset.kind);
});
document.addEventListener('keydown',function(e){
  if(e.key==='Enter'&&e.target&&e.target.classList&&e.target.classList.contains('lic-input')){
    const btn=e.target.parentElement.querySelector('.lic-btn');if(btn)btn.click();
  }
});
document.querySelectorAll('#enPracSub button').forEach(b=>b.onclick=()=>{
  const es=b.dataset.es;
  document.querySelectorAll('#enPracSub button').forEach(x=>x.classList.toggle('on',x===b));
  document.getElementById('hkView').style.display = es==='hk'?'block':'none';
  document.getElementById('vocabView').style.display = es==='vocab'?'block':'none';
  document.getElementById('ivView').style.display = es==='iv'?'block':'none';
  document.getElementById('paperView').style.display = es==='paper'?'block':'none';
  document.getElementById('goalView').style.display = es==='goal'?'block':'none';
  if(es==='hk')renderHk(); else if(es==='vocab')renderVocab(); else if(es==='paper'){ if(licActive()){ if(!curEnPaper.length) genEnPaper(); } else showLicLock('licLockEn','en'); }
});
document.querySelectorAll('#mathPracSub button').forEach(b=>b.onclick=()=>{
  const es=b.dataset.es;
  document.querySelectorAll('#mathPracSub button').forEach(x=>x.classList.toggle('on',x===b));
  document.getElementById('mTermsView').style.display = es==='mterms'?'block':'none';
  document.getElementById('mathPaperView').style.display = es==='mpaper'?'block':'none';
  if(es==='mpaper'){ if(licActive()){ if(!curMathPaper.length) genMathPaper(); } else showLicLock('licLockMath','math'); }
});
document.querySelectorAll('#mpgChips .chip').forEach(c=>c.onclick=()=>{
  curMathGrade=c.dataset.pg;
  document.querySelectorAll('#mpgChips .chip').forEach(x=>x.classList.toggle('on',x===c));
  genMathPaper();
});
function buildIntro(){
  var g=function(id){return (document.getElementById(id).value||'').trim();};
  var f=function(v){return v? v : '______';};
  document.getElementById('ivOut').textContent=
    'Good morning. My name is '+f(g('ivName'))+'. I am '+f(g('ivAge'))+' years old and I study at '+f(g('ivSch'))+' School in '+f(g('ivDist'))+'.\n'+
    'My favourite subject is '+f(g('ivSubj'))+' because '+f(g('ivWhy'))+'.\n'+
    'In my free time, I enjoy '+f(g('ivH1'))+' and '+f(g('ivH2'))+'.\n'+
    'I am a '+f(g('ivChar'))+' person and I work well with others.\n'+
    'I want to join '+f(g('ivTgt'))+' because ______.\n'+
    'Thank you for your time.';
}
['ivName','ivAge','ivSch','ivDist','ivSubj','ivWhy','ivH1','ivH2','ivChar','ivTgt'].forEach(function(id){
  var el=document.getElementById(id); if(el) el.oninput=buildIntro;
});
(function(){
  var btn=document.getElementById('ivRecBtn'); if(!btn) return;
  var rec=null,chunks=[];
  btn.onclick=function(){
    var stat=document.getElementById('ivRecStat');
    if(!navigator.mediaDevices||!window.MediaRecorder){stat.textContent='此瀏覽器不支援錄音，請用手機錄影自測。';return;}
    try{
      if(rec&&rec.state==='recording'){rec.stop();return;}
      navigator.mediaDevices.getUserMedia({audio:true}).then(function(stream){
        rec=new MediaRecorder(stream);chunks=[];
        rec.ondataavailable=function(e){if(e.data&&e.data.size)chunks.push(e.data);};
        rec.onstop=function(){
          var blob=new Blob(chunks,{type:'audio/webm'});var a=document.createElement('a');
          a.href=URL.createObjectURL(blob);a.download='self-intro.webm';a.click();
          stat.textContent='已停止並下載錄音，回放檢討。';stream.getTracks().forEach(function(t){t.stop();});
        };
        rec.start();stat.textContent='錄音中…（再按一次停止並下載）';
      }).catch(function(e){stat.textContent='無法取得麥克風：'+e.message;});
    }catch(e){stat.textContent='錄音失敗：'+e.message;}
  };
})();
showMain('guide');

// ---- 數學術語表 ----
let mathFilter='all';
function mathMatches(t){
  if(mathFilter!=='all' && t.cat!==mathFilter) return false;
  const q=document.getElementById('mathSearch').value.trim().toLowerCase();
  if(q && !(t.zh.toLowerCase().includes(q)||t.en.toLowerCase().includes(q))) return false;
  return true;
}
function renderMath(){
  const tb=document.getElementById('mathBody'); tb.innerHTML='';
  MATH_TERMS.forEach((t,i)=>{
    if(!mathMatches(t))return;
    const ex=MATH_EX[t.en];
    const tr=document.createElement('tr');
    tr.className=(mProg[i]?'done ':'')+'mrow';
    tr.innerHTML=`<td>${t.cat}</td><td>${t.zh}</td><td class="en">${t.en} <span class="mini" data-sp="${i}">🔊</span></td><td>${t.note||''}${ex?'<br><span style="color:#0f7a63">例：'+ex+'</span>':''}</td>`;
    tr.onclick=()=>{mProg[i]=!mProg[i];saveM();renderMath();const el=document.getElementById('stMath');if(el)el.textContent=Object.keys(mProg).filter(k=>mProg[k]).length;if(curTab==='progress')renderProgress();};
    tb.appendChild(tr);
  });
  if(!tb.children.length)tb.innerHTML='<tr><td colspan="4" style="color:#888;text-align:center;padding:14px">無相符術語</td></tr>';
  tb.querySelectorAll('.mini[data-sp]').forEach(s=>s.onclick=e=>{e.stopPropagation();speak(MATH_TERMS[+s.dataset.sp].en,'en-US');});
}
document.querySelectorAll('#mTermsView .chip').forEach(c=>c.onclick=()=>{
  document.querySelectorAll('#mTermsView .chip').forEach(x=>x.classList.remove('on'));
  c.classList.add('on');mathFilter=c.dataset.mc;renderMath();
});
document.getElementById('mathSearch').oninput=renderMath;

// ---- 诗词列表 ----
function poemMatches(p){
  if(curFilter!=='all' && !p.grades.includes(curFilter)) return false;
  const q=document.getElementById('poemSearch').value.trim();
  if(q && !(p.title.includes(q)||p.author.includes(q))) return false;
  return true;
}
function renderPoemGrid(){
  const g=document.getElementById('poemGrid'); g.innerHTML='';
  POEMS.filter(poemMatches).forEach(p=>{
    const d=document.createElement('div'); d.className='pcard';
    const st=pProg[p.id]||{};
    const tick=(st.recite?'✓背 ':'')+(st.write?'✓默':'');
    d.innerHTML=`<div class="t">${p.title}</div><div class="m">〔${p.dynasty}〕${p.author} ${p.grades.map(x=>'<span class="tag'+(x===FOCUS_GRADE?' b':'')+'">'+x+'</span>').join('')} ${tick?'<span style="color:#1a8a4a">'+tick+'</span>':''}</div>`;
    d.onclick=()=>openPoem(p.id);
    g.appendChild(d);
  });
}
function openPoem(id){
  curPoem=POEMS.find(x=>x.id===id);
  document.getElementById('mask').classList.add('show');
  renderModal();
}
function closeModal(){document.getElementById('mask').classList.remove('show');}
document.getElementById('mask').onclick=e=>{if(e.target.id==='mask')closeModal();};
function renderModal(){
  const p=curPoem; if(!p)return;
  document.getElementById('mTitle').textContent=p.title;
  document.getElementById('mSub').textContent=`〔${p.dynasty}〕${p.author}　${p.grades.join(' / ')}`;
  const showPy=document.getElementById('tgPy').checked, showJy=document.getElementById('tgJy').checked;
  let html=''; let ni=0;
  p.lines.forEach(ln=>{
    html+='<div class="line">';
    for(let i=0;i<ln.text.length;i++){
      const c=ln.text[i];
      if(' ，。、？！；：'.includes(c)){html+=`<span class="ch"><span class="py">&nbsp;</span><span class="han">${c}</span><span class="jy">&nbsp;</span></span>`;continue;}
      const blank = clozeOn && (ni%2===1); ni++;
      const hanCls='han'+(blank?' blank':'')+(blank&&clozeReveal?' reveal':'');
      html+=`<span class="ch"><span class="py">${showPy&&!blank?(ln.py[i]||''):'&nbsp;'}</span><span class="${hanCls}">${c}</span><span class="jy">${showJy&&!blank?(ln.jy[i]||''):'&nbsp;'}</span></span>`;
    }
    html+='</div>';
  });
  if(p.paraphrase && !clozeOn) html+=`<div class="para">白話釋義：${p.paraphrase}</div>`;
  document.getElementById('mBody').innerHTML=html;
  if(!showPy)document.getElementById('mBody').classList.add('hidepy');else document.getElementById('mBody').classList.remove('hidepy');
  if(!showJy)document.getElementById('mBody').classList.add('hidejy');else document.getElementById('mBody').classList.remove('hidejy');
  const st=pProg[p.id]||{};
  document.getElementById('mActs').innerHTML=
    `<button class="${st.recite?'done':''}" onclick="toggleRecite()">${st.recite?'✓ 已背熟':'標記背熟'}</button>`+
    `<button class="${st.write?'wdone':''}" onclick="toggleWrite()">${st.write?'✓ 已默寫':'標記默寫'}</button>`+
    `<button class="${clozeOn?'on':''}" onclick="toggleCloze()">${clozeOn?'退出默寫':'默寫練習'}</button>`+
    (clozeOn?`<button onclick="toggleClozeReveal()">${clozeReveal?'隱藏答案':'顯示答案'}</button>`:'')+
    `<button onclick="speakPoem()">🔊 朗讀</button>`+
    `<button onclick="window.print()">打印${clozeOn?'默寫紙':'此首'}</button>`;
}
function toggleCloze(){clozeOn=!clozeOn;clozeReveal=false;renderModal();}
function toggleClozeReveal(){clozeReveal=!clozeReveal;renderModal();}
function toggleRecite(){const id=curPoem.id;pProg[id]=pProg[id]||{};pProg[id].recite=!pProg[id].recite;pProg[id].date=new Date().toISOString().slice(0,10);saveP();renderModal();renderPoemGrid();if(curTab==='progress')renderProgress();}
function toggleWrite(){const id=curPoem.id;pProg[id]=pProg[id]||{};pProg[id].write=!pProg[id].write;pProg[id].date=new Date().toISOString().slice(0,10);saveP();renderModal();renderPoemGrid();if(curTab==='progress')renderProgress();}
function printOne(){window.print();}

// ---- 词表 ----
function renderVocab(){
  const q=document.getElementById('vocabSearch').value.trim().toLowerCase();
  const tp=document.getElementById('vocabTopic').value;
  const list=document.getElementById('vocabList'); list.innerHTML='';
  VOCAB.filter(v=>{
    if(tp && v.topic!==tp)return false;
    if(q && !(v.w.toLowerCase().includes(q)||v.zh.includes(q)))return false;
    return true;
  }).forEach(v=>{
    const known=!!vProg[v.w];
    const d=document.createElement('div'); d.className='vcard';
    d.innerHTML=`<div><span class="w">${v.w}</span><span class="ph">${v.ph}</span>${known?' <span style="color:#1a8a4a">✓</span>':''}</div><div class="zh">${v.zh}</div><div class="tp">主題：${v.topic}</div>`;
    d.onclick=()=>{d.classList.toggle('hidezh');};
    d.ondblclick=()=>{vProg[v.w]=!vProg[v.w];saveV();renderVocab();if(curTab==='progress')renderProgress();};
    list.appendChild(d);
  });
}
(function(){const sel=document.getElementById('vocabTopic');const ts=[...new Set(VOCAB.map(v=>v.topic))].filter(Boolean).sort();ts.forEach(t=>{const o=document.createElement('option');o.value=t;o.textContent=t;sel.appendChild(o);});})();

// ---- 香港小學基礎詞（坊間整理，非 EDB 官方分級詞表；年級為估算） ----
// 按 P1–P6（一年級…六年級）分級分塊展示，可折疊；搜索/主題/自測過濾；折疊狀態跨重渲染保留
const HK_GRADE_CODE={'一年級':'P1','二年級':'P2','三年級':'P3','四年級':'P4','五年級':'P5','六年級':'P6'};
const HK_GRADE_RANK={'一年級':1,'二年級':2,'三年級':3,'四年級':4,'五年級':5,'六年級':6};
let hkCollapsed=new Set();
function renderHk(){
  const q=document.getElementById('hkSearch').value.trim().toLowerCase();
  const tp=document.getElementById('hkTheme').value;
  const hide=document.getElementById('hkHide').checked;
  const list=document.getElementById('hkList'); list.innerHTML='';
  const grades=[...new Set(HK.map(w=>w.grade))].filter(Boolean)
    .sort((a,b)=>((HK_GRADE_RANK[a]||99)-(HK_GRADE_RANK[b]||99))||a.localeCompare(b,'zh-Hant'));
  let any=false;
  grades.forEach(g=>{
    const words=HK.filter(w=>w.grade===g && (!tp||w.theme===tp) && (!q||w.w.toLowerCase().includes(q)||w.zh.includes(q)));
    if(!words.length)return;
    any=true;
    const code=HK_GRADE_CODE[g]||g;
    const sec=document.createElement('details'); sec.className='gsec'; sec.open=!hkCollapsed.has(g);
    const sum=document.createElement('summary'); sum.className='gsec-h';
    sum.innerHTML='<span class="gcode">'+code+'</span><span class="glabel">'+g+'</span><span class="gcount">'+words.length+' 詞</span>';
    sec.appendChild(sum);
    const body=document.createElement('div'); body.className='gsec-body';
    words.forEach(w=>{
      const known=!!hProg[w.id];
      const d=document.createElement('div'); d.className='vcard'+(hide?' hidezh':'');
      d.innerHTML=`<div><span class="w">${w.w}</span> <span class="mini" data-sp="${w.w}">🔊</span>${known?' <span class="ok">✓</span>':''}<span class="tp"> · ${w.grade} · ${w.theme}</span></div><div class="zh">${w.zh}</div>`;
      d.onclick=()=>{hProg[w.id]=!hProg[w.id];saveH();renderHk();document.getElementById('stHk').textContent=Object.keys(hProg).filter(k=>hProg[k]).length;renderBadges();};
      d.querySelector('.mini[data-sp]').onclick=e=>{e.stopPropagation();speak(w.w,'en-US');};
      body.appendChild(d);
    });
    sec.appendChild(body);
    sec.addEventListener('toggle',()=>{ if(sec.open)hkCollapsed.delete(g); else hkCollapsed.add(g); });
    list.appendChild(sec);
  });
  if(!any)list.innerHTML='<div style="color:#888;font-size:13px">無相符詞彙</div>';
}
function hkExpandAll(){hkCollapsed.clear();renderHk();}
function hkCollapseAll(){[...new Set(HK.map(w=>w.grade))].forEach(g=>hkCollapsed.add(g));renderHk();}
document.getElementById('hkExpandAll').onclick=hkExpandAll;
document.getElementById('hkCollapseAll').onclick=hkCollapseAll;
(function(){const sel=document.getElementById('hkTheme');const ts=[...new Set(HK.map(w=>w.theme))].filter(Boolean).sort();ts.forEach(t=>{const o=document.createElement('option');o.value=t;o.textContent=t;sel.appendChild(o);});})();

// ---- 繁體對照 ----
function renderFt(){
  const q=document.getElementById('ftSearch').value.trim();
  const list=document.getElementById('ftList'); list.innerHTML='';
  FT_MAP.filter(([s,f])=>!q||s.includes(q)||f.includes(q)).forEach(([s,f])=>{
    const d=document.createElement('div'); d.className='ftrow';
    d.innerHTML=`<span class="s">${s}</span><span class="ar">→</span><span class="f">${f}</span>`;
    list.appendChild(d);
  });
  if(!list.children.length)list.innerHTML='<div style="color:#888;font-size:13px">無相符字</div>';
}

// ---- 进度 ----
function renderProgress(){
  const recite=Object.values(pProg).filter(x=>x.recite).length;
  const write=Object.values(pProg).filter(x=>x.write).length;
  document.getElementById('stRecite').textContent=recite;
  document.getElementById('stWrite').textContent=write;
  document.getElementById('stVocab').textContent=Object.keys(vProg).filter(k=>vProg[k]).length;
  document.getElementById('stHk').textContent=Object.keys(hProg).filter(k=>hProg[k]).length;
  document.getElementById('stMath').textContent=Object.keys(mProg).filter(k=>mProg[k]).length;
  const list=document.getElementById('progList'); list.innerHTML='';
  POEMS.filter(p=>(pProg[p.id]||{}).recite).forEach(p=>{
    const st=pProg[p.id];
    const d=document.createElement('div'); d.className='vcard';
    d.innerHTML=`<div class="w">${p.title}</div><div class="ph">〔${p.dynasty}〕${p.author} · 背熟${st.recite?'✓':'✗'} 默寫${(st.write?'✓':'✗')} · ${st.date||''}</div>`;
    list.appendChild(d);
  });
  if(!list.children.length)list.innerHTML='<div style="color:#888;font-size:13px">尚未標記任何詩詞</div>';
  renderBadges();
}
document.getElementById('clearBtn').onclick=()=>{
  if(confirm('確定清空所有進度（詩詞／詞表／港小詞／數術語）？此操作不可恢復。')){
    pProg={};vProg={};hProg={};mProg={};saveP();saveV();saveH();saveM();renderPoemGrid();renderVocab();renderHk();renderMath();renderProgress();
  }
};
// ---- 進度匯出 / 匯入 ----
document.getElementById('exportBtn').onclick=()=>{
  const data={pProg,vProg,hProg,mProg,ver:'hkk_v1.21',exported:new Date().toISOString().slice(0,10)};
  const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='hkk_progress.json';a.click();URL.revokeObjectURL(a.href);
};
document.getElementById('importBtn').onclick=()=>document.getElementById('importFile').click();
document.getElementById('importFile').onchange=e=>{
  const f=e.target.files[0]; if(!f)return;
  const r=new FileReader();
  r.onload=()=>{try{
    const d=JSON.parse(r.result);
    if(d.pProg)pProg=d.pProg; if(d.vProg)vProg=d.vProg; if(d.hProg)hProg=d.hProg; if(d.mProg)mProg=d.mProg;
    saveP();saveV();saveH();saveM();renderPoemGrid();renderVocab();renderHk();renderMath();renderProgress();
    alert('已匯入進度（'+Object.keys(pProg).length+' 詩 / '+Object.keys(hProg).length+' 港小詞 / '+Object.keys(mProg).length+' 數術語）');
  }catch(err){alert('檔案格式錯誤，請選擇由本站匯出的 JSON');}};
  r.readAsText(f); e.target.value='';
};

// ---- 事件 ----
document.querySelectorAll('.chip[data-g]').forEach(c=>c.onclick=()=>{
  document.querySelectorAll('.chip[data-g]').forEach(x=>x.classList.remove('on'));
  c.classList.add('on');curFilter=c.dataset.g;renderPoemGrid();
});
document.getElementById('poemSearch').oninput=renderPoemGrid;
document.getElementById('vocabSearch').oninput=renderVocab;
document.getElementById('vocabTopic').onchange=renderVocab;
document.getElementById('hkSearch').oninput=renderHk;
document.getElementById('hkTheme').onchange=renderHk;
document.getElementById('hkHide').onchange=renderHk;
document.getElementById('ftSearch').oninput=renderFt;

// ---- 背單詞激勵：連續打卡火焰 / 成就徽章 / 閃卡抽查 (v1.10) ----
function todayStr(){var d=new Date();var z=function(n){return String(n).padStart(2,'0');};return d.getFullYear()+'-'+z(d.getMonth()+1)+'-'+z(d.getDate());}
function yestStr(){var d=new Date();d.setDate(d.getDate()-1);var z=function(n){return String(n).padStart(2,'0');};return d.getFullYear()+'-'+z(d.getMonth()+1)+'-'+z(d.getDate());}
function bumpStreak(){var s=+localStorage.getItem('hkk_streak')||0;var last=localStorage.getItem('hkk_lastday')||'';var t=todayStr();if(last===t){}else if(last===yestStr()){s+=1;}else{s=1;}localStorage.setItem('hkk_streak',s);localStorage.setItem('hkk_lastday',t);return s;}
function renderMoti(){var s=+localStorage.getItem('hkk_streak')||0;var e=document.getElementById('streakNum');if(e)e.textContent=s;var fl=document.getElementById('flame');if(fl)fl.style.opacity=s>0?'1':'.25';var g=document.getElementById('dailyGoal');if(g){if(s===0)g.textContent='今天開始第一次打卡吧！';else if(s<7)g.textContent='再堅持 '+(7-s)+' 天點亮 🔥 七天火焰徽章';else g.textContent='火焰不滅，已連續 '+s+' 天！';}}
function renderBadges(){var known=Object.keys(hProg).filter(function(k){return hProg[k];}).length;var s=+localStorage.getItem('hkk_streak')||0;var themes={};HK.forEach(function(w){if(hProg[w.id])themes[w.theme]=1;});var ts=Object.keys(themes).length;var B=[{ic:'🌱',n:'初露鋒芒',need:'掌握 10 詞',ok:known>=10},{ic:'🌿',n:'漸入佳境',need:'掌握 30 詞',ok:known>=30},{ic:'🌳',n:'詞彙小達人',need:'掌握 60 詞',ok:known>=60},{ic:'🏆',n:'百詞斬',need:'掌握 100 詞',ok:known>=100},{ic:'🔥',n:'七天火焰',need:'連續 7 天',ok:s>=7},{ic:'♨️',n:'半月火焰',need:'連續 15 天',ok:s>=15},{ic:'⭐',n:'主題探索',need:'橫跨 5 主題',ok:ts>=5}];var box=document.getElementById('badgeBox');if(!box)return;box.innerHTML=B.map(function(b){return '<div class="badge'+(b.ok?'':' off')+'"><div class="bi">'+b.ic+'</div><div class="bn">'+b.n+'</div><div class="bd">'+(b.ok?'已獲得 🎉':b.need)+'</div></div>';}).join('');}
var flashQueue=[],flashIdx=0,flashKnown=0,flashTotal=0,flashCur=null;
function startFlash(){flashQueue=HK.slice();for(var i=flashQueue.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=flashQueue[i];flashQueue[i]=flashQueue[j];flashQueue[j]=t;}flashIdx=0;flashKnown=0;flashTotal=0;document.getElementById('flashPanel').style.display='block';nextFlash();}
function nextFlash(){if(flashIdx>=flashQueue.length){document.getElementById('flashCard').textContent='🎉 本輪完成！';document.getElementById('flashZh').style.display='none';document.getElementById('flashReveal').style.display='none';document.getElementById('flashKnow').style.display='none';document.getElementById('flashUnk').style.display='none';return;}flashCur=flashQueue[flashIdx];document.getElementById('flashCard').textContent=flashCur.w;var z=document.getElementById('flashZh');z.style.display='none';z.textContent=flashCur.zh;document.getElementById('flashReveal').style.display='inline-block';document.getElementById('flashKnow').style.display='none';document.getElementById('flashUnk').style.display='none';document.getElementById('flashStat').textContent='本輪：已認識 '+flashKnown+' / 共 '+flashTotal;}
function flashReveal(){document.getElementById('flashZh').style.display='block';document.getElementById('flashReveal').style.display='none';document.getElementById('flashKnow').style.display='inline-block';document.getElementById('flashUnk').style.display='inline-block';}
function flashKnow(){if(flashCur){hProg[flashCur.id]=true;saveH();}flashKnown++;flashTotal++;flashIdx++;document.getElementById('stHk').textContent=Object.keys(hProg).filter(function(k){return hProg[k];}).length;renderBadges();nextFlash();}
function flashUnk(){if(flashCur){flashQueue.push(flashCur);}flashTotal++;flashIdx++;nextFlash();}
document.getElementById('flashBtn').onclick=function(){startFlash();};
document.getElementById('flashReveal').onclick=flashReveal;
document.getElementById('flashKnow').onclick=flashKnow;
document.getElementById('flashUnk').onclick=flashUnk;
document.getElementById('flashSound').onclick=function(){if(flashCur)speak(flashCur.w,'en-US');};
renderPoemGrid();renderVocab();renderHk();renderMath();renderFt();showEnStat();
bumpStreak();renderMoti();renderBadges();
(function(){const c=getAiCfg();if(!c||!c.base)return;const b=document.getElementById('aiBase');if(b&&c.base)b.value=c.base;const k=document.getElementById('aiKey');if(k&&c.key)k.value=c.key;const m=document.getElementById('aiModel');if(m&&c.model)m.value=c.model;})();
</script>
</body>
</html>'''
html = TEMPLATE.replace('__DATA__', DATA).replace('__LIC_SECRET__', LIC_SECRET)
# 版本號從副標題單一真相源提取（公開版 vX.Y），輸出帶版本號文件名
_m = re.search(r'公開版\s+(v\d+\.\d+)', TEMPLATE)
VER = _m.group(1) if _m else 'v1.15'
out = os.path.join(WS, 'index_%s.html' % VER)
open(out, 'w', encoding='utf-8').write(html)
# 兼容副本：verify2.js 與預覽／部署預設入口均依賴 index.html
open(os.path.join(WS, 'index.html'), 'w', encoding='utf-8').write(html)
print('生成', out, os.path.getsize(out), 'bytes')
