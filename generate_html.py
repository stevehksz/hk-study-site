# -*- coding: utf-8 -*-
"""单文件 HTML 学习站生成器：把 build_data.json 注入模板，输出 index_vX.Y.html（并保留 index.html 兼容副本）。
v1.1 结构：2 级导航，練習區按科目歸口
  速覽指南（中文 / 英文 / 數學 / 繁體對照 / 英文卷） ＋ 練習（中文 / 英文 / 數學） ＋ 學習進度
  練習＝中文(古詩詞) / 英文(港小生字＋詞表) / 數學(中↔英術語表·點擊打卡)
數學術語表從速覽→數學挪至練習→數學，速覽只留差異卡。
新增：詩詞默寫填空+打印、數術語打卡、進度匯出/匯入、Web Speech 朗讀、移動端響應式。
v1.26：主導航重排——「升學規劃」移至第一位（速覽指南之前），方便家長一進站先看插班時間線與擇校分檔；默認選中頁保持速覽指南不變。
v1.35：練習→英文新增「繪本閱讀」打卡模塊——牛津樹校園版 1–9 階共 204 本書單（build_ort.py 從家中課程視頻目錄提取正課書名，跨文件夾去重、多集合併標注講數，書名為事實信息不含教材內容）；每本點擊打卡（localStorage hkk_ort，隨賬號隔離），各階進度條＋總進度統計；模塊頂部「📁 家庭英語資源地圖」折疊卡列出牛津樹/朗文本地路徑與磨耳朵/精讀用法建議。同版新增「朗文詞庫」子標籤——LWTE GOLD 5A/5B Word Bank 19 類 140 條（build_lwte.py 以 .doc piece table 解析教材詞庫頁，兩欄串行人工清理；詞條為常見短語列表事實性內容，中文釋義自譯，版權屬 Pearson，站內標注僅家庭學習）；按冊/類別進度條＋點擊標記已掌握（hkk_lwte）。verify2.js 加 12 項斷言。v1.34：應葉工要求刪除頁腳「數據來源」可見標注行；授權信息改保留在 HTML 源碼注釋內（不顯示給訪客）。v1.33：登入註冊系統（仿 PLG iPlatform 風格）——線上鏈接強制登入方可使用（全屏登入頁：登入/註冊分 Tab、密碼👁切換、記住我、忘記密碼可重置賬號並清空進度），本地直開 file://·localhost 免登入以「本地」身份直接進站。本機賬號：暱稱+密碼存本瀏覽器 localStorage（密碼 salt+SHA-256 哈希，不上傳）；學習進度（打卡/最佳分/生字掌握等全部 hkk_* 鍵）按賬號隔離（hkk_u@暱稱@鍵 作用域搬移），多孩子各開賬號互不干擾，登入/退出時自動切換。⚠️ 純本地賬號：換設備需重新註冊，進度不跟隨；密碼遺失只能重置（清空該賬號進度）。原計劃接雲服務真賬號，開通確認被取消後改本地方案，日後可再開通升級。verify2.js 加 12 項賬號斷言（sha256 標準測向量/註冊登入/密碼錯拒/作用域往返/強制攔截）。v1.32：港小生字卡加英式 DJ 音標——335 詞全部配 IPA（/_add_ipa.py 人工標注生成 _hk_word_ipa.json，build_data.py 合併進 hk_words，全覆蓋校驗無缺無多）；生字卡詞後顯示音標（復用 .ph 樣式），閃卡「揭曉」同時顯示中文+音標。音標以 Oxford/Longman 詞典為準，個別詞有美式異讀。verify2.js 加音標斷言。v1.31：10 套卷答案可視——目錄卡每套加「📖 答案」按鈕，一按即載入該套卷並自動填入全部正確答案（A–J 十段、MC 打勾、開放題填範文），批改後全綠高亮 SCORE 100/100，答案即卷底可直接對照；答案模式不寫入「本級最佳」記錄（gradeExamPaper 加 noSave 參數）。打印含答案版照舊。verify2.js 加答案模式斷言（滿分+最佳分不被污染）。v1.30：呈分試卷題庫加厚，一次出 10 套不重樣——閱讀理解 (H) 與海報閱讀 (I) 每級由 2 套擴至 5 套（P5 新增街市/獅子山/節水 + 失物招領/閱讀週/游泳 gala，P6 新增猴子/港鐵/廚餘 + 運動會/探訪安老院/科學週），時態篇章 (C) 每級由 2 篇擴至 5 篇（P5 運動會/跨境上學/科學館，P6 賣物會/筆友/地質公園）；「一次出 10 套」新增硬規則：10 套卷的 H+I 組合互不重複（目錄上不會再有兩套同一篇閱讀+海報），全卷 JSON 簽名去重不變。修錯字 A umbrella→An umbrella。verify2.js 加題庫數量與 H+I 組合去重斷言。v1.29：呈分試卷「一次出 10 套」可視化——目錄卡每套新增「📄 打開」按鈕，點一下即把該套整卷載入屏幕作答區（可作答、可交卷批改、可單獨打印），卷頭標「第 N 套」；生成後自動滾動到目錄卡，唔使再靠「出新卷」碰運氣。目錄表加操作欄。按「🎲 出新卷」或切年級會清套號返回隨機卷。verify2.js 加「打開第 1 套」斷言。v1.28：呈分試卷「一次出 10 套」——「📋 一次出 10 套」按鈕一鍵隨機組卷 10 套並簽名去重（組合空間每級約 10,368 種，屏幕出目錄卡列出各套閱讀/海報篇章與時態開頭，不影響當前作答卷）；「🖨 打印這 10 套」把 10 套整冊打印（每套獨立分頁 page-break，卷頭標「第 N 套」，勾含答案版時答案頁跟在各自卷後）。打印函數重構：卷體構造抽出 examPrintHtml(p,ans,examNo) 供單套/十套共用。verify2.js 加 10 套生成與打印內容斷言。v1.27：呈分試卷按第二批樣張補內容＋AI 出新卷——①題型補齊：新增 (I) 海報閱讀（公告海報＋MC 4×1%＋開放回答 2%×2，P5 校遊/舊書義賣、P6 慈善遊園會/沙灘清潔，仿樣張 I 版式）與 (J) since/therefore 填空（10×1%，各級 2 套，仿樣張 M）；樣張 K 電影職業（scriptwriter/film director/costume designer/extra/stuntman/set designer）與 L 習語（black sheep/green light/see red/egg on face/once in a blue moon/a slip of the tongue）、J 明喻詞庫分別併入 (D)(B)(A) 題庫（各加第 3 套）。②分值重排仍滿 100：A12+B12+C10(10×1%)+D10+E12+F10+G6(6×1%)+H10(MC 2%×2)+I8+J10。③「🤖 AI 出新卷」：復用英文卷的 OpenAI 兼容設置(hkk_ai_cfg)，大模型按 10 段 schema 生成整卷，結構校驗（exValidate：段數/題數/J 答案僅 since|therefore）通過才替換當前卷，卷頭標「AI 生成（請家長把關）」，失敗提示回退本地「🎲 出新卷」。④打印含 I/J 段與答案頁，AI 卷打印同步標注；verify2.js 更新 radio/textarea/段數斷言＋P5/P6 閉環滿分(SCORE 100/100)斷言。v1.25：繁體字庫分級擴充——簡→繁對照改為 FT_GRADES 分 P1–P6（自編分級：按簡體常用度＋繁體書寫複雜度遞增，頁面標注非教育局官方分級），字庫由 146 對擴至約 250 對，一簡對多繁字加注記（里/發/歷/復/鬆/隻/幾/盡等）；繁體對照視圖加年級 chips（全部/P1–P6）＋字數統計，搜尋在選中年級內生效。同版修復：.gsec margin 覆蓋 .wrap 居中致寬屏內容貼左（margin 12px 0 → 12px auto）。v1.24：練習→英文新增「呈分試卷」（P5–P6·仿版式原創題）——版式仿坊間呈分試模擬卷：生詞表8詞＋Warm-up詞形填空(不計分)＋(A)明喻12%＋(B)習語12%＋(C)時態篇章20%＋(D)職業對話10%＋(E)情境造句12%＋(F)短語動詞10%＋(G)量詞連詞12%＋(H)閱讀理解12%＝100%；每級2套分段題庫隨機組卷（2⁸組合），交卷自動批改（填空歸一化比對、開放題按要點關鍵詞、MC自動判分），記錄本級最佳(localStorage hkk_exampaper_v0)，打印含答案版；題目全部原創仿編，非任何機構真卷。verify2.js 加呈分試卷斷言。v1.23：全站免費——移除 v1.21 授權碼月付（英文卷／數學卷直接開放，無需激活；刪除鎖定面板、校驗 JS 與頁面注入密鑰；gen_license.py 保留在倉庫但不再被構建引用，後續如需收費可再啟）。免費為主的定位：題庫持續更新靠自願支持。verify2.js 改寫授權碼斷言為「免費直開」斷言（無鎖定面板／直出題卡）。v1.22：擇校分檔接入 schooland×教育局交叉勘誤——風采＝資助（EDB收費證明書免學費堂費$340，非直資）、官津英中僅6所（心誠直資英中、馬錦燦雙語部分英文、其餘中中）、茂峰＝元朗天水圍非北區、康樂/李興貴＝大埔接收北區跨境生；新增北區中學一覽20所（可篩選英中/官立/直資，含英文名/宗教/性別/地址）、升中攻略外鏈精選（EDB/中學概覽/schooland，正文版權屬原站）。verify2.js 加勘誤/篩選/外鏈斷言。v1.21：新增授權碼月付（付費模組＝英文卷＋數學卷，其餘免費）——激活碼 HKSS-YYYYMMDD-XXXXXXXX（SHA256(密鑰|到期日)前8位），未激活時出卷區顯示鎖定面板（輸入碼解鎖，過期碼／無效碼分別提示），出卷／打印全鏈路守衛，操作列顯示「已激活至」；新增 gen_license.py 發碼工具（記錄 licenses_issued.csv）與 license_secret.txt 密鑰（首次構建自動生成）。防君子級：密鑰隨頁面分發，月付護城河＝持續更新內容。verify2.js 加授權碼斷言（鎖定面板／無效拒／過期拒／解鎖出卷／localStorage）。v1.20：修復數學卷年級 chip 切換失效——術語分類 chip 的綁定選擇器原為 #mathPracView .chip，誤把數學卷年級 chip(#mpgChips P1–P6) 也綁成術語處理器，導致點 P2–P6 仍抽 P1 題、localStorage 年級寫錯；收斂為 #mTermsView .chip 僅綁術語分類，年級 chip 不再被覆寫。verify2.js 數學卷斷言全過。v1.19：練習→數學新增「數學卷」（雙語對照·分 P1–P6）——仿編原創題庫（mc/fill/word 三型），英文題幹＋中文對照，按年級 chip 出卷＋交卷批改（應用題不計分給參考答案）＋打印含答案版；mathPracView 加 subnav 分「中↔英術語表／數學卷」。verify2.js 加數學卷斷言。v1.18：排版優化——詞彙頁（港小生字）加「展開全部／收起全部」按鈕（複用 hkCollapsed 狀態），長標題補 line-height:1.5 改善小屏折行。v1.17：港小生字（英文詞）按 P1–P6 分級分塊展示——移除年級 chip 過濾，改為六個可折疊小節（P1·一年級…P6·六年級），每節列出該年級英文詞＋中文義，帶搜索/主題/自測過濾，折疊狀態跨重渲染保留（hkCollapsed）；沿用簡繁對照式簡潔列表。verify2.js 改寫 hk 斷言（.gsec=6／每節含詞卡／首節標題含 P1 與一年級／總詞卡>300／搜索過濾）。v1.16：英文卷新增「綜合 P1–P6」分年級小節卷（每級 2 題）＋每題「🔄 換一題（本地）」與「🤖 AI 換題（接 OpenAI 兼容大模型，自填接口／密鑰，存 localStorage）」；AI 設置面板。v1.15：英文卷閱讀題庫接入教育局「中國寓言系列」——10 篇 EDB 公開英文寓言（鑿壁偷光/亡羊補牢/一飯千金/賣油翁/守株待兔/塞翁失馬/愚公移山/三人成虎/大禹治水/花木蘭）依官方英文文本改編為 read 題型（每篇 4 題含 1 道文法選擇填空），分散 P4(4)/P5(3)/P6(3)，標 src:'EDB' 來源；genEnPaper 拼接 EN_EDB 常量（不動原 EN_QBANK）；renderEnPaper/打印雙端顯示「來源：EDB」；enSrcNote 補 EDB 版權聲明。verify2.js 加 4 項斷言（EN_EDB 存在／各級含 EDB read／src 字段）。
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

TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>香港插班擇校 · 北區中小學名單＋申請時間線｜葉工</title>
<meta name="description" content="香港新界北區跨境學童插班指南：北區小學 30 所／中學 20 所名單（電話·校網·檔位篩選）、申請時間線、材料清單、中英數練習。葉工整理，全站免費。">
<meta property="og:title" content="香港插班擇校 · 北區中小學名單＋申請時間線｜葉工">
<meta property="og:description" content="北區小學 30 所／中學 20 所（電話·校網·檔位篩選）＋插班時間線＋材料清單＋中英數練習，跨境學童家長免費使用。">
<meta property="og:type" content="website">
<meta property="og:url" content="https://stevehksz.github.io/hk-study-site/">
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
  body.printing-paper #enPrintSheet,body.printing-paper #mathPrintSheet,body.printing-paper #examPrintSheet{display:block!important;position:static;width:100%}
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
  .gsec{border:1px solid var(--line);border-radius:10px;margin:12px auto;overflow:hidden;background:var(--card)}
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
/* ---- v1.24 呈分試卷 ---- */
.ex-head{display:flex;justify-content:space-between;flex-wrap:wrap;border:2px solid #333;border-radius:6px;padding:8px 12px;margin:6px 0 12px;font-weight:bold}
.ex-code{color:#1a3c8f}
.ex-nd{font-weight:normal;font-size:13px}
.ex-lead{margin:14px 0 6px;font-size:15px}
.ex-vocab,.ex-bank{width:100%;border-collapse:collapse;margin:6px 0 12px}
.ex-vocab td,.ex-bank td{border:1.5px solid #999;padding:6px 8px;font-size:13.5px;text-align:center}
.ex-zh{color:#666;font-size:12px}
.ex-sec{margin:18px 0;padding:12px 14px;border:1px solid #ddd;border-radius:10px;background:#fff}
.ex-q{margin:0 0 10px;font-size:14.5px}
.ex-it{margin:8px 0;line-height:2;font-size:14px}
.ex-ol{margin:6px 0 4px 22px}
.ex-ol li{margin:10px 0;line-height:2.1;font-size:14px}
.ex-pass{line-height:2.3;font-size:14px;background:#fafafa;border:1px dashed #ccc;border-radius:8px;padding:12px 14px}
.ex-inp{width:130px;border:none;border-bottom:1.5px solid #888;background:#f4f7ff;text-align:center;font-size:13.5px;padding:2px 4px;border-radius:4px 4px 0 0}
.ex-inp.ex-ok{background:#e6f6e6;border-bottom-color:#2e8b2e;color:#1e6b1e}
.ex-inp.ex-bad{background:#fdeaea;border-bottom-color:#c0392b;color:#c0392b}
.ex-open{width:100%;border:1.5px solid #bbb;border-radius:8px;padding:6px 10px;font-size:13.5px;font-family:inherit}
.ex-open.ex-ok{border-color:#2e8b2e;background:#e6f6e6}
.ex-open.ex-bad{border-color:#c0392b;background:#fdeaea}
.ex-mc{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;margin:4px 0 10px}
.ex-opt{font-size:13.5px;line-height:1.7}
.ex-warm{color:#b06a00;font-size:12px}
.ex-result{border:2px solid #1a3c8f;border-radius:10px;padding:12px 16px;margin:14px 0;background:#f4f7ff;font-size:15px}
.ex-wrongs{margin:8px 0 8px 20px;font-size:13.5px;line-height:1.9;color:#8a3a30}
.ex-tip{font-size:12px;color:#888}
.ex-anspage{margin-top:18px;border-top:2px dashed #999;padding-top:10px}
.ex-ans{font-size:12.5px;line-height:1.9;margin:4px 0}
.ex-lines{color:#bbb;letter-spacing:1px}
/* ---- 登录注册页（v1.33，仿 PLG iPlatform 风格） ---- */
#authGate{position:fixed;inset:0;background:#f6faf9;z-index:9999;display:none;overflow-y:auto;font-family:inherit}
#authGate.on{display:block}
body.authLock{overflow:hidden}
.authHero{background:linear-gradient(135deg,#17b3a6,#2ecf9e);padding:34px 16px 26px;text-align:center;color:#fff;border-radius:0 0 42% 42%/0 0 12% 12%}
.authHero .logo{font-size:38px;font-weight:800;letter-spacing:1px;text-shadow:0 2px 6px rgba(0,0,0,.15)}
.authHero .logo .hl{color:#ffe37a}
.authHero .sub{font-size:15px;margin-top:6px;opacity:.95}
.authCard{max-width:400px;margin:-14px auto 24px;background:#fff;border:1px solid #e3eeec;border-radius:14px;box-shadow:0 6px 24px rgba(23,120,110,.10);padding:22px 20px 18px}
.authTabs{display:flex;gap:6px;margin-bottom:16px}
.authTabs button{flex:1;padding:9px 0;border:1px solid #d7e6e3;background:#f4fbfa;border-radius:8px;font-size:15px;cursor:pointer;color:#3d6b65;font-family:inherit}
.authTabs button.on{background:#17b3a6;border-color:#17b3a6;color:#fff;font-weight:700}
.authRow{display:flex;align-items:center;border:1px solid #d9e5e2;border-radius:8px;margin-bottom:12px;background:#fff;overflow:hidden}
.authRow:focus-within{border-color:#17b3a6;box-shadow:0 0 0 2px rgba(23,179,166,.15)}
.authRow .ico{padding:0 10px;font-size:16px;color:#8aa8a3}
.authRow input{flex:1;border:0;outline:0;padding:11px 10px 11px 0;font-size:15px;min-width:0;font-family:inherit}
.authRow .eye{border:0;background:none;cursor:pointer;padding:0 12px;font-size:15px;color:#5f8a84;font-family:inherit}
.authOpts{display:flex;justify-content:space-between;align-items:center;margin:2px 0 14px;font-size:13px;color:#5f7f7a}
.authOpts label{cursor:pointer;display:flex;gap:5px;align-items:center}
.authOpts a{color:#17b3a6;cursor:pointer;text-decoration:underline}
.authBtn{display:block;width:100%;padding:12px 0;border:0;border-radius:24px;background:#17b3a6;color:#fff;font-size:17px;font-weight:700;cursor:pointer;font-family:inherit}
.authBtn:active{transform:translateY(1px)}
.authBtn.alt{margin-top:12px;background:#fff;color:#17b3a6;border:2px solid #17b3a6}
.authErr{min-height:18px;font-size:13px;color:#d64545;margin:4px 0 8px;text-align:center}
.authOk{color:#17a05c}
.authFoot{max-width:400px;margin:0 auto 30px;text-align:center;font-size:12.5px;color:#7d9a95;line-height:1.7}
.authFoot .terms{text-decoration:underline;color:#4a8f88;cursor:pointer}
.authReset{border-top:1px dashed #dbe9e6;margin-top:16px;padding-top:12px;font-size:13px;color:#5f7f7a}
.authReset summary{cursor:pointer;color:#4a8f88}
#userChip{position:absolute;top:14px;right:16px;display:none;align-items:center;gap:8px;font-size:13px;color:#0d5a53;background:rgba(255,255,255,.85);border:1px solid #cfe8e4;border-radius:20px;padding:4px 6px 4px 12px;z-index:50}
#userChip button{border:0;background:#17b3a6;color:#fff;border-radius:14px;padding:3px 10px;font-size:12px;cursor:pointer;font-family:inherit}
header{position:relative}
@media print{#authGate{display:none !important}#userChip{display:none !important}}
.ort-map{margin:10px 0;border:1px solid var(--line);border-radius:10px;background:#fff}
.ort-map summary{cursor:pointer;padding:9px 12px;font-size:13px;font-weight:600;color:#475069}
.ort-map-body{padding:4px 14px 12px;font-size:13px;color:#3b4252}
.ort-map-body code{background:#f0f4fb;border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-size:12px;word-break:break-all}
.ort-map-body ul{margin:4px 0 8px;padding-left:20px}
.ort-map-body li{margin:3px 0}
.ort-stat{font-size:13px;color:#475069;margin:8px 0}
.ort-lv{margin:14px 0}
.ort-lv-h{display:flex;align-items:center;gap:10px;font-size:14px;font-weight:700;color:var(--ink);margin-bottom:6px}
.ort-bar{flex:1;height:8px;background:#e8edf5;border-radius:4px;overflow:hidden;min-width:80px}
.ort-bar i{display:block;height:100%;background:var(--math);border-radius:4px;transition:width .3s}
.ort-books{display:flex;flex-wrap:wrap;gap:6px}
.ort-bk{padding:5px 11px;border:1px solid var(--line);border-radius:16px;background:#fff;font-size:13px;cursor:pointer;color:var(--ink);transition:.15s}
.ort-bkw{display:inline-flex;align-items:center;gap:4px;margin:2px 0}
.ort-play{font-size:11px;color:#0f766e;text-decoration:none;border:1px solid #99f6e4;border-radius:10px;padding:2px 6px;background:#f0fdfa}
.ort-play:hover{background:#0f766e;color:#fff}
.ort-bk:hover{border-color:var(--math);color:var(--math)}
.ort-bk.done{background:var(--math);border-color:var(--math);color:#fff;text-decoration:line-through;opacity:.85}
.ort-bk .ort-n{font-size:11px;opacity:.75;margin-left:3px}
  /* v1.48 悬浮咨询按钮 */
  #ctaFab{position:fixed;right:14px;bottom:18px;z-index:15}
  #ctaFabBtn{padding:11px 16px;border:none;border-radius:26px;background:linear-gradient(135deg,#2c7be5,#1a5fc4);color:#fff;font-size:14px;font-weight:700;cursor:pointer;box-shadow:0 6px 18px -4px rgba(28,90,180,.5)}
  #ctaFabBtn:active{transform:scale(.96)}
  #ctaModal .wechat{font-size:22px;font-weight:800;letter-spacing:.5px;color:#1a5fc4;background:#f0f6ff;border:1px dashed #9cc0ee;border-radius:8px;padding:10px 14px;text-align:center;margin:10px 0}
  @media print{#ctaFab{display:none!important}}
</style>
<!-- 51la 访问统计（v1.43，叶工 2026-11-02 注册开通；sdk 地址显式 https，file:// 本地打开不请求） -->
<script charset="UTF-8" id="LA_COLLECT" src="https://sdk.51.la/js-sdk-pro.min.js"></script>
<script>try{LA.init({id:"3RhjH055gOjxA8UA",ck:"3RhjH055gOjxA8UA"})}catch(e){}</script>
</head>
<body>
<!-- ============ 登录注册页（v1.33）：線上強制登入，本地直開免登入 ============ -->
<div id="authGate">
  <div class="authHero">
    <div class="logo">香港插班<span class="hl">學習站</span></div>
    <div class="sub">中英數練習 · 呈分試模擬卷 · 升學規劃（免費）</div>
  </div>
  <div class="authCard">
    <div class="authTabs">
      <button id="authTabLogin" class="on" onclick="authShowTab('login')">登 入</button>
      <button id="authTabReg" onclick="authShowTab('reg')">註 冊</button>
    </div>
    <div id="authLoginBox">
      <div class="authRow"><span class="ico">👤</span><input id="authLoginName" maxlength="16" placeholder="暱稱（註冊時填的名字）"></div>
      <div class="authRow"><span class="ico">🔒</span><input id="authLoginPwd" type="password" maxlength="64" placeholder="密碼（至少 8 位）"><button class="eye" type="button" onclick="authTogglePwd('authLoginPwd',this)">👁</button></div>
      <div class="authOpts"><label><input type="checkbox" id="authRemember" checked> 記住我</label><a onclick="authShowTab('reset')">忘記密碼？</a></div>
      <div class="authErr" id="authLoginErr"></div>
      <button class="authBtn" id="authLoginBtn" onclick="authLogin()">登 入</button>
      <button class="authBtn alt" onclick="authShowTab('reg')">創建新賬號</button>
    </div>
    <div id="authRegBox" style="display:none">
      <div class="authRow"><span class="ico">👧</span><input id="authRegName" maxlength="16" placeholder="暱稱（2–16 字，中文或英文）"></div>
      <div class="authRow"><span class="ico">🔒</span><input id="authRegPwd" type="password" maxlength="64" placeholder="密碼（至少 8 位）"><button class="eye" type="button" onclick="authTogglePwd('authRegPwd',this)">👁</button></div>
      <div class="authRow"><span class="ico">✅</span><input id="authRegPwd2" type="password" maxlength="64" placeholder="再輸入一次密碼"></div>
      <div class="authErr" id="authRegErr"></div>
      <button class="authBtn" id="authRegBtn" onclick="authRegister()">創建賬號並登入</button>
    </div>
    <details class="authReset" id="authResetBox" style="display:none">
      <summary>🔑 忘記密碼？重置賬號</summary>
      <p style="margin:8px 0">⚠️ 純本地賬號無法找回舊密碼。輸入暱稱和新密碼可<strong>重置該賬號並清空其全部學習進度</strong>（其他賬號不受影響）。</p>
      <div class="authRow"><span class="ico">👤</span><input id="authResetName" maxlength="16" placeholder="要重置的暱稱"></div>
      <div class="authRow"><span class="ico">🔒</span><input id="authResetPwd" type="password" maxlength="64" placeholder="新密碼（至少 8 位）"></div>
      <div class="authErr" id="authResetErr"></div>
      <button class="authBtn alt" onclick="authReset()">重置賬號</button>
    </details>
  </div>
  <div class="authFoot">
    <span class="terms" onclick="alert('本站為免費學習站。賬號僅保存在本瀏覽器（不上傳服務器），用於區分不同孩子的學習進度；請勿使用重要密碼。')">使用條款</span><br>
    數據保存在本設備瀏覽器，不上傳 · 換設備需重新註冊<br>
    © 叶工 SteveHKSZ · 公開版 v1.51（全站免費）
  </div>
</div>
<header>
  <div id="userChip"><span id="userChipName"></span><button onclick="authLogout()">退出</button></div>
  <h1>香港教學速覽 · 中英數</h1>
  <p>內地家庭快速了解並跟上香港教學（中文·英文·數學）＋ 練習打卡 · 賬號登入·數據保存在本設備 · 公開版 v1.51（全站免費）</p>
</header>
<nav>
  <button data-tab="plan" class="on">升學規劃</button>
  <button data-tab="guide">速覽指南</button>
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
<div id="guideView" style="display:none">
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
    <div class="gtitle">繁體字 · 簡→繁 高頻對照（分 P1–P6）</div>
    <span class="folk">常用字對照，以香港課本用字為準；分級＝自編（按簡體常用度＋繁體書寫複雜度遞增），非教育局官方分級；一簡對多繁者（如 发→發/髮、里→裡/裏）須按詞義選</span>
    <div class="pg-chips" id="ftChips">
      <span class="chip on" data-fg="all">全部</span>
      <span class="chip" data-fg="P1">P1</span>
      <span class="chip" data-fg="P2">P2</span>
      <span class="chip" data-fg="P3">P3</span>
      <span class="chip" data-fg="P4">P4</span>
      <span class="chip" data-fg="P5">P5</span>
      <span class="chip" data-fg="P6">P6</span>
    </div>
    <div class="tools">
      <input type="search" id="ftSearch" placeholder="搜簡體字，如 国 / 学">
      <span class="mini" id="ftCount"></span>
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
      <button data-es="exam">呈分試卷</button>
      <button data-es="ort">繪本閱讀</button>
      <button data-es="lwte">朗文詞庫</button>
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
    <div class="wrap gsec" id="examView" style="display:none">
      <div class="gtitle">呈分試卷 · 英文呈分試模擬卷（P5–P6 · 仿版式原創題）</div>
      <span class="folk">版式仿照坊間呈分試卷：生詞表＋詞形填空＋明喻(A)／習語(B)／時態篇章(C)／職業對話(D)／情境造句(E)／短語動詞(F)／量詞連詞(G)／閱讀理解(H)／海報閱讀(I)／since·therefore(J)，共 100%。⚠️ 題目全部本地原創仿編，非任何補習社／學校／評估局真卷；AI 生成卷請家長先過目。</span>
      <div class="pg-chips" id="examChips">
        <span class="chip" data-pg="P5">P5</span>
        <span class="chip on" data-pg="P6">P6</span>
      </div>
      <div class="enpaper-actions">
        <button class="btn" id="examNewPaper" onclick="genExamPaper()">🎲 出新卷</button>
        <button class="btn" id="examAiBtn" onclick="exAiPaper()">🤖 AI 出新卷</button>
        <button class="btn" id="examSubmit" onclick="gradeExamPaper()">✅ 交卷批改</button>
        <button class="btn" id="examTenBtn" onclick="genTenExamPapers()">📋 一次出 10 套</button>
        <button class="btn" id="examPrintBtn" onclick="printExamPaper()">🖨 打印一套卷子</button>
        <label class="print-ans-toggle"><input type="checkbox" id="examPrintAns"> 含答案版</label>
        <span class="enpaper-stat" id="examStat">本級最佳：—</span>
      </div>
      <div id="examPaperBox"></div>
      <div id="examPaperResult"></div>
      <div class="en-src-note"><b>說明：</b>題型版式取自家長提供的坊間呈分試模擬卷樣式（2026-10-31 兩批樣張，僅取版式與分值結構，不取內容）：第二批樣張的海報閱讀、since/therefore、電影職業、習語等題型已對應併入 (I)(J)(D)(B)；題目內容全部原創仿編。「🤖 AI 出新卷」需先在「練習→英文→智能練習卷」底部「⚙ AI 設置」填好接口（僅存本瀏覽器），AI 生成的整卷經結構校驗後才替換當前卷，卷頭標 AI 生成。年級難度以 P5–P6 呈分試常見水平估算，以學校課本為準。</div>
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
      </div>
      <div id="mathPaperBox"></div>
      <div id="mathPaperResult"></div>
      <div class="en-src-note" id="mathSrcNote">
        <b>資料來源與說明（坊間參考 · 2026-10-31 檢索）：</b>
        題庫為本地仿編原創練習題，參考香港小學數學課程常見進度（數與運算／分數·小數·百分數／代數／幾何／度量／統計與概率）整理；非評估局（HKEAA）或學校真卷，年級難度為估算。正式以學校課本與教育局課程指引為準。
      </div>
    </div>
    <div class="wrap gsec" id="ortView" style="display:none">
      <div class="gtitle">繪本閱讀打卡 · 牛津樹校園版 1–9 階</div>
      <span class="folk">書單提取自家中課程視頻目錄（書名與階數為事實信息）；本站僅做閱讀打卡記錄，不含任何教材內容。點書名即標記/取消「已讀」，進度按登入賬號分開保存。</span>
      <details class="ort-map">
        <summary>📁 家庭英語資源地圖（本地路徑 + 用法建議）</summary>
        <div class="ort-map-body">
          <p><b>牛津樹（Oxford Reading Tree）校園版</b> — <a href="file:///G:/00%20%E5%92%A8%E8%AF%A2%26%E5%85%AC%E8%87%AA%E5%AA%92%E4%BD%93/22%20%E9%A6%99%E6%B8%AF%E6%8F%92%E7%8F%AD/88%20%E6%B6%B5%E6%B6%B5/01%E8%8B%B1%E8%AA%9E/01%20%E7%89%9B%E6%B4%A5%E6%A0%91" target="_blank" rel="noopener"><code>G:\00 咨询&公自媒体\22 香港插班\88 涵涵\01英語\01 牛津树</code></a></p>
          <ul>
            <li><b>磨耳朵（每天 15–20 分鐘）</b>：<a href="file:///G:/00%20%E5%92%A8%E8%AF%A2%26%E5%85%AC%E8%87%AA%E5%AA%92%E4%BD%93/22%20%E9%A6%99%E6%B8%AF%E6%8F%92%E7%8F%AD/88%20%E6%B6%B5%E6%B6%B5/01%E8%8B%B1%E8%AA%9E/01%20%E7%89%9B%E6%B4%A5%E6%A0%91/%E6%A0%A1%E5%9B%AD%E7%89%88%E7%89%9B%E6%B4%A5%E6%A0%91%E9%9F%B3%E9%A2%91%E6%96%87%E4%BB%B6" target="_blank" rel="noopener">校園版牛津树音频文件</a>按階播 mp3，配合已讀過的書循環聽。</li>
            <li><b>精讀（每週 2 本）</b>：<a href="file:///G:/00%20%E5%92%A8%E8%AF%A2%26%E5%85%AC%E8%87%AA%E5%AA%92%E4%BD%93/22%20%E9%A6%99%E6%B8%AF%E6%8F%92%E7%8F%AD/88%20%E6%B6%B5%E6%B6%B5/01%E8%8B%B1%E8%AA%9E/01%20%E7%89%9B%E6%B4%A5%E6%A0%91/%E7%AB%A5%E8%80%81%E5%B8%88%E7%89%9B%E6%B4%A5%E7%BB%98%E6%9C%AC%E8%A7%86%E9%A2%91" target="_blank" rel="noopener">童老师牛津绘本视频</a>正課雙語講解（每本 1–2 講），先看講解再自讀，讀完來本頁打卡；書單裡每本書旁的 ▶ 按鈕本地打開時可直接播放。</li>
            <li><b>娛樂時間</b>：<a href="file:///G:/00%20%E5%92%A8%E8%AF%A2%26%E5%85%AC%E8%87%AA%E5%AA%92%E4%BD%93/22%20%E9%A6%99%E6%B8%AF%E6%8F%92%E7%8F%AD/88%20%E6%B6%B5%E6%B6%B5/01%E8%8B%B1%E8%AA%9E/01%20%E7%89%9B%E6%B4%A5%E6%A0%91/%E7%89%9B%E6%B4%A5%E6%A0%91%E7%9C%9F%E4%BA%BA%E5%89%A7" target="_blank" rel="noopener">牛津树真人剧</a>Biff &amp; Chip 30 集 + The Magic Key 動畫，只准英文原聲。</li>
          </ul>
          <p><b>香港朗文（Longman）教材</b> — <a href="file:///G:/00%20%E5%92%A8%E8%AF%A2%26%E5%85%AC%E8%87%AA%E5%AA%92%E4%BD%93/22%20%E9%A6%99%E6%B8%AF%E6%8F%92%E7%8F%AD/88%20%E6%B6%B5%E6%B6%B5/01%E8%8B%B1%E8%AA%9E/10%20%E9%A6%99%E6%B8%AF%E6%9C%97%E6%96%87" target="_blank" rel="noopener"><code>G:\00 咨询&公自媒体\22 香港插班\88 涵涵\01英語\10 香港朗文</code></a></p>
          <ul>
            <li><b>課內同步</b>：<a href="file:///G:/00%20%E5%92%A8%E8%AF%A2%26%E5%85%AC%E8%87%AA%E5%AA%92%E4%BD%93/22%20%E9%A6%99%E6%B8%AF%E6%8F%92%E7%8F%AD/88%20%E6%B6%B5%E6%B6%B5/01%E8%8B%B1%E8%AA%9E/10%20%E9%A6%99%E6%B8%AF%E6%9C%97%E6%96%87/LWTEGOLD%201A-6B%20%E5%85%A8%E5%A5%97%E8%B5%84%E6%BA%90" target="_blank" rel="noopener">LWTE GOLD 1A–6B 全套資源</a>教師用書/課件（跟學校進度預習複習）。</li>
            <li><b>聽力</b>：<a href="file:///G:/00%20%E5%92%A8%E8%AF%A2%26%E5%85%AC%E8%87%AA%E5%AA%92%E4%BD%93/22%20%E9%A6%99%E6%B8%AF%E6%8F%92%E7%8F%AD/88%20%E6%B6%B5%E6%B6%B5/01%E8%8B%B1%E8%AA%9E/10%20%E9%A6%99%E6%B8%AF%E6%9C%97%E6%96%87/B5135-Longman%20English%20World" target="_blank" rel="noopener">Longman English World</a>各冊 Listening &amp; Speaking mp3。</li>
            <li>⚠️ 教材音視頻版權屬出版社，僅限家庭使用，勿外傳。</li>
          </ul>
          <p class="folk">💡 上面的資料夾連結與書單 ▶ 按鈕，只有在**本機直接打開這份 HTML 文件**（地址欄是 file:/// 開頭）時才能點開；線上版不出現 ▶。</p>
        </div>
      </details>
      <div class="pg-chips" id="ortChips"></div>
      <div id="ortStat" class="ort-stat"></div>
      <div id="ortList"></div>
    </div>
    <div class="wrap gsec" id="lwteView" style="display:none">
      <div class="gtitle">朗文詞庫 · LWTE GOLD 5A/5B（19 類 140 條）</div>
      <span class="folk">詞條取自朗文 LWTE GOLD 教材詞庫頁（常見短語/單詞列表，事實性內容；中文釋義為自譯；版權屬 Pearson Education Asia，僅供家庭學習參考，請勿外傳）。點擊即標記/取消「已掌握」。</span>
      <div class="pg-chips" id="lwteChips"></div>
      <div id="lwteStat" class="ort-stat"></div>
      <div id="lwteList"></div>
    </div>
  </div>
</div>

<!-- ============ 升學規劃（插班思路） ============ -->
<div id="planView">
  <div class="subnav" id="planSub">
    <button data-sub="timeline" class="on">時間線</button>
    <button data-sub="schools">擇校分檔</button>
    <button data-sub="docs">材料清單</button>
    <button data-sub="study">學習路線</button>
    <button data-sub="policy">身份政策</button>
    <button data-sub="faq">常見問題</button>
  </div>

  <!-- 時間線 -->
  <div class="wrap" id="timelineView">
    <div class="gsec">
      <h2>申請時間線（以 2027.9 入中一為例）</h2>
      <p class="tip">適用以 9 月入學為主批、1 月春季為備選。具體日期以教育局及各校官網當年公告為準。</p>

      <h3>🎓 中學插班（以 2027.9 入中一為例）</h3>
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
        <p>前一年 <b>10–12 月</b>申請，<b>12 月上旬</b>基本截止，學位約為秋季 30%。⚠️ 本家庭身份 2027.6 到手，<b>2027 年春季批趕不上</b>（申請時無身份）；2028 年春季批可作中途轉校備選。</p>
      </div>
      <div class="src">來源：教育局 2025/2027 中一學位分配辦法（官方）＋區域教育服務處插班安排｜適用 2027/28 學年｜具體以各校官網當年公告為準</div>
    </div>
  </div>

  <!-- 擇校分檔 -->
  <div class="wrap" id="schoolsView" style="display:none">
    <div class="gsec">
      <h2>擇校分檔：北區中學 20 所＋東鐵沿線（大埔）20 所＋北區小學 30 所</h2>
      <div style="display:flex;gap:10px;margin:12px 0">
        <button class="btn" id="jmpPri" style="flex:1;padding:12px 8px;font-size:15px;font-weight:700">🏫 北區小學 30 所</button>
        <button class="btn" id="jmpSec" style="flex:1;padding:12px 8px;font-size:15px;font-weight:700">🎓 北區中學 20 所</button>
      </div>
      <p class="tip" style="margin:0 0 6px">按上面按鈕直達對應名單；上次看的表會被記住。</p>
      <div class="gcard">
        <h3>北區跨境要點</h3>
        <p>北區（上水/粉嶺）是羅湖、福田（落馬洲支線）、文錦渡口岸入港第一站，東鐵線 1 站到上水、2 站到粉嶺，單程通關＋車程約 30–40 分鐘，跨境生比例全港最高。教育局有跨境學童派位安排，北區 <b>30 所學校</b>參與（2025 年度數據，中一跨境學額約 <b>171 個</b>，來源：教育局公開資料，坊間引用）。跨境校巴/保姆車體系成熟，校巴申請一般每年 5–6 月。</p>
      </div>
      <div class="gcard">
        <h3>🚌 校車 / 保姆車怎麼回事（跨境交通現實）</h3>
        <p>① <b>校巴/保姆車不是學校配套</b>：由私營營辦商按線路經營，跨境校巴在北區體系成熟（坊間常見營辦商如葉太、禮姨、菁荭等——坊間整理，2026-10-27 核對，線路與營辦商每年變動）。<b>申請一般在每年 5–6 月</b>，錯過要等補位。</p>
        <p>② <b>中學階段的現實</b>：北區中學的跨境生絕大多數<b>自行搭東鐵通勤</b>（羅湖/落馬洲 → 上水/粉嶺，1–2 站）；中學保姆車線路遠少於小學，某校有沒有線路、上車點在哪、費用多少，要<b>逐校電話校務處問</b>（連同叩門一起問最省事）——下兩表已附各校電話，可直接點撥。</p>
        <p>③ <b>大埔（東鐵沿線）</b>：粉嶺再一站即太和，鐵路通勤可控；保姆車線路更少，以東鐵為主——所以下表每所都標了「近東鐵站」（依地址所在社區估算）。</p>
        <p class="src">來源：hk-placement 知識庫 v0.2（2026-10-27）＋ 校務處諮詢慣例整理；線路/費用/集合點以學校及營辦商當年公布為準。</p>
      </div>
      <div class="gcard warn">
        <h3>本家庭叩門總邏輯（身份 2027.6 到手的家庭先看這個）</h3>
        <p>孩子身份預計 <b>2027 年 6 月到手</b>，意味著：① 2027.1.4–1.18 自行分配窗口＝錯過（須遞交時已持身份）；② 5 月前所有主申請＝錯過；③ 唯一現實路徑＝兩條並行——<b>A. 2027.7.6 放榜後叩門</b>（黃金期 7.6–7.9，官津每班約 1 個留班位）＋ <b>B. 教育局途徑三</b>（新來港兒童資助中一，2027.5–8 月登記，分批 7.6/7 月底/8 月中出結果，兜底不會沒書讀）；④ 直資僅心誠一所（風采經 2026-10-31 教育局收費證明書勘誤為資助、免學費僅堂費 $340/年，走官津派位窗口），不存在「身份到手即報第一批占位」紅利。</p>
      </div>
        <div class="scroll-x">
        <table class="mtable" id="tierTable">
          <thead><tr><th>梯隊</th><th>學校</th><th>類型</th><th>教學語言</th><th>Band參考<br><span style="font-weight:400;color:#a33">非官方</span></th><th>學費</th><th>申請路徑（本家庭）</th></tr></thead>
          <tbody>
            <tr><td class="tier1">衝刺</td><td>鄧顯紀念中學</td><td>資助</td><td>英中</td><td>1A</td><td>免（僅堂費/書雜費）</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier1">衝刺</td><td>東華三院甲寅年總理中學</td><td>資助</td><td>英中</td><td>1A–1B</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier1">衝刺</td><td>田家炳中學</td><td>資助</td><td>英中</td><td>1B–1C</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier1">衝刺</td><td>聖公會陳融中學</td><td>資助</td><td>英中</td><td>1B–1C</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier1">衝刺</td><td>東華三院李嘉誠中學</td><td>資助</td><td>英中</td><td>1C</td><td>免</td><td>官津 7 月叩門＋8 月補錄</td></tr>
            <tr><td class="tier1">衝刺</td><td>風采中學（教育評議會主辦）</td><td>資助</td><td>英中</td><td>1B</td><td>免（僅堂費 $340/年，EDB 收費證明書）</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier1">衝刺</td><td>粉嶺官立中學</td><td>官立</td><td>中文</td><td>1C–2A</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>鳳溪第一中學</td><td>資助</td><td>中文</td><td>1C–2A</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>香海正覺蓮社佛教馬錦燦紀念英文中學</td><td>資助</td><td>雙語（部分英文）</td><td>2A</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>宣道會陳朱素華紀念中學</td><td>資助</td><td>中文</td><td>2A–2B</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>粉嶺禮賢會中學</td><td>資助</td><td>中文</td><td>2A–2B</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>基督教香港信義會心誠中學</td><td>直資</td><td>英中</td><td>2</td><td>中一至中三 $7,100/年；中四至中六 $8,400/年（2025-26 官網）</td><td>直資 7 月年中插班/叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>鳳溪廖萬石堂中學</td><td>資助</td><td>中文</td><td>2</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>保良局馬錦明中學</td><td>資助</td><td>中文</td><td>2</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>粉嶺救恩書院</td><td>資助</td><td>中文</td><td>2B–2C</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>中華基督教會基新中學</td><td>資助</td><td>中文</td><td>2</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier2">穩妥</td><td>上水官立中學</td><td>官立</td><td>中文</td><td>2B–3</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier3">保底</td><td>明愛粉嶺陳震夏中學</td><td>資助</td><td>中文</td><td>3</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier3">保底</td><td>聖芳濟各書院</td><td>資助</td><td>中文</td><td>3</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier3">保底</td><td>新界喇沙中學</td><td>資助</td><td>中文</td><td>3</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier3">保底</td><td>佛教茂峰法師紀念中學 ⚠️（元朗天水圍，非北區）</td><td>資助</td><td>中文</td><td>3</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier3">保底</td><td>神召會康樂中學（大埔·接收北區跨境生）</td><td>資助</td><td>中文</td><td>3</td><td>免</td><td>官津 7 月叩門</td></tr>
            <tr><td class="tier3">保底</td><td>香港教師會李興貴中學（大埔·接收北區跨境生）</td><td>資助</td><td>中文</td><td>3</td><td>免</td><td>官津 7 月叩門</td></tr>
          </tbody>
        </table>
      </div>
      <div class="gcard">
        <h3>叩門衝刺組合建議（按英文水平分）</h3>
        <p><b>英文達標（PET 量級）</b>：衝刺 鄧顯/甲寅年/田家炳/陳融 ＋ 求穩 風采/心誠 ＋ 保底 基新/上水官立/粉嶺救恩/粉嶺官立（粉嶺官立 2026-10-31 勘誤為中中，接受中文授課才納入）。</p>
        <p><b>英文偏弱</b>：衝刺 甲寅年/李嘉誠 ＋ 求穩 鳳溪一中/救恩/基新 ＋ 保底 基新/上水官立/李興貴（先中文過渡一年，再圖轉校）。</p>
        <p>無論哪組，<b>7.6 一早從衝刺檔開始衝</b>，保底檔留 7.8–7.9 兜底，並同步走 EDB 途徑三。</p>
      </div>
      <div class="gcard warn">
        <h3>⚠️ 交叉勘誤（2026-10-31 · schooland × 教育局 × 中學概覽）</h3>
        <p>本次以 <a href="https://www.schooland.hk/ss/north" target="_blank" rel="noopener">schooland 北區中學頁</a>（2026-10-31 取樣）與教育局公開資料交叉核對，修正本表：① <b>風采中學＝資助</b>（EDB 收費證明書：學費免、堂費 $340/年），非直資；② 官津<b>英中僅 6 所</b>（教育局名單）：鄧顯/甲寅/田家炳/陳融/李嘉誠/風采；心誠為直資英中；馬錦燦屬雙語（部分科目英文，中學概覽），其餘均中中；③ 茂峰位於<b>元朗天水圍</b>（非北區，建議從策略中移除）、康樂/李興貴位於<b>大埔</b>（他區：北區，接收北區跨境生）。Band 各源不一，僅作非官方參考。</p>
      </div>
      <div class="gcard">
        <h3>北區中學一覽（20 所 · 可篩選）</h3>
        <div class="pg-chips" id="ssChips">
          <span class="chip on" data-ss="all">全部 20</span>
          <span class="chip" data-ss="en">英中 7</span>
          <span class="chip" data-ss="gov">官立 2</span>
          <span class="chip" data-ss="dss">直資 1</span>
        </div>
        <div class="scroll-x">
        <table class="mtable" id="ssTable">
          <thead><tr><th>學校</th><th>英文名稱</th><th>種類</th><th>宗教</th><th>性別</th><th>教學語言</th><th>Band參考<br><span style="font-weight:400;color:#a33">非官方</span></th><th>地址</th><th>電話<br><span style="font-weight:400;color:#a33">核對 2026-11-02</span></th><th>官網<br><span style="font-weight:400;color:#a33">核對 2026-11-02</span></th></tr></thead>
          <tbody>
            <tr data-ss="en" data-lan="en"><td>鄧顯紀念中學</td><td>HKTA Tang Hin Memorial Secondary School</td><td>資助</td><td>道教</td><td>男女</td><td>英中</td><td>1A</td><td>上水彩園邨</td><td><a href="tel:26726820">26726820</a></td><td><a href="https://www.tanghin.edu.hk" target="_blank" rel="noopener" title="學校官網">www.tanghin.edu.hk</a></td></tr>
            <tr data-ss="en" data-lan="en"><td>東華三院甲寅年總理中學</td><td>TWGHs Kap Yan Directors' College</td><td>資助</td><td>無</td><td>男女</td><td>英中</td><td>1B</td><td>上水彩園邨</td><td><a href="tel:26727395">26727395</a></td><td><a href="http://www.twghkyds.edu.hk" target="_blank" rel="noopener" title="學校官網">www.twghkyds.edu.hk</a></td></tr>
            <tr data-ss="en" data-lan="en"><td>風采中學（教育評議會主辦）</td><td>Elegantia College</td><td>資助</td><td>無</td><td>男女</td><td>英中</td><td>1B</td><td>上水清城路8號</td><td><a href="tel:24683680">24683680</a></td><td><a href="http://www.elegantia.edu.hk" target="_blank" rel="noopener" title="學校官網">www.elegantia.edu.hk</a></td></tr>
            <tr data-ss="en" data-lan="en"><td>田家炳中學</td><td>Tin Ka Ping Secondary School</td><td>資助</td><td>無</td><td>男女</td><td>英中</td><td>1B</td><td>粉嶺維翰路1號</td><td><a href="tel:26731778">26731778</a></td><td><a href="http://web.tkpss.edu.hk" target="_blank" rel="noopener" title="學校官網">web.tkpss.edu.hk</a></td></tr>
            <tr data-ss="en" data-lan="en"><td>聖公會陳融中學</td><td>SKH Chan Young Secondary School</td><td>資助</td><td>基督教</td><td>男女</td><td>英中</td><td>1C–1B</td><td>上水智昌路6號</td><td><a href="tel:26718989">26718989</a></td><td><a href="https://www.skhcyss.edu.hk" target="_blank" rel="noopener" title="學校官網">www.skhcyss.edu.hk</a></td></tr>
            <tr data-ss="en" data-lan="en"><td>東華三院李嘉誠中學</td><td>TWGHs Li Ka Shing College</td><td>資助</td><td>無</td><td>男女</td><td>英中</td><td>1B</td><td>粉嶺祥華邨</td><td><a href="tel:26697455">26697455</a></td><td><a href="https://www.twghlkss.edu.hk" target="_blank" rel="noopener" title="學校官網">www.twghlkss.edu.hk</a></td></tr>
            <tr data-ss="dss" data-lan="en"><td>基督教香港信義會心誠中學</td><td>Fanling Lutheran Secondary School</td><td>直資</td><td>基督教</td><td>男女</td><td>英中</td><td>2C</td><td>粉嶺馬會道270號</td><td><a href="tel:26700541">26700541</a></td><td><a href="https://www.flss.edu.hk" target="_blank" rel="noopener" title="學校官網">www.flss.edu.hk</a></td></tr>
            <tr data-ss="aided"><td>香海正覺蓮社佛教馬錦燦紀念英文中學</td><td>HHCKLA Buddhist Ma Kam Chan Memorial English Secondary School</td><td>資助</td><td>佛教</td><td>男女</td><td>雙語（部分英文）</td><td>2C</td><td>粉嶺聯和墟聯益街9號</td><td><a href="tel:26699208">26699208</a></td><td><a href="https://www.bmkc.edu.hk" target="_blank" rel="noopener" title="學校官網">www.bmkc.edu.hk</a></td></tr>
            <tr data-ss="aided"><td>宣道會陳朱素華紀念中學</td><td>Christian Alliance S W Chan Memorial College</td><td>資助</td><td>基督教</td><td>男女</td><td>中文</td><td>2C–2B</td><td>粉嶺暉明路12號</td><td><a href="tel:26709229">26709229</a></td><td><a href="https://www.caswcmc.edu.hk" target="_blank" rel="noopener" title="學校官網">www.caswcmc.edu.hk</a></td></tr>
            <tr data-ss="aided"><td>粉嶺禮賢會中學</td><td>Fanling Rhenish Church Secondary School</td><td>資助</td><td>基督教</td><td>男女</td><td>中文</td><td>2C–2B</td><td>粉嶺聯和墟聯益街1號</td><td><a href="tel:29473698">29473698</a></td><td><a href="https://www.frcss.edu.hk" target="_blank" rel="noopener" title="學校官網">www.frcss.edu.hk</a></td></tr>
            <tr data-ss="aided"><td>保良局馬錦明中學</td><td>PLK Ma Kam Ming College</td><td>資助</td><td>無</td><td>男女</td><td>中文</td><td>2B–2A</td><td>粉嶺華明路38號</td><td><a href="tel:26794545">26794545</a></td><td><a href="http://www.plkmkmc.edu.hk" target="_blank" rel="noopener" title="學校官網">www.plkmkmc.edu.hk</a></td></tr>
            <tr data-ss="aided"><td>鳳溪廖萬石堂中學</td><td>Fung Kai Liu Man Shek Tong Secondary School</td><td>資助</td><td>無</td><td>男女</td><td>中文</td><td>2C–2B</td><td>上水鳳南路6號</td><td><a href="tel:26736106">26736106</a></td><td><a href="http://www.fklmstss.edu.hk" target="_blank" rel="noopener" title="學校官網">www.fklmstss.edu.hk</a></td></tr>
            <tr data-ss="aided"><td>粉嶺救恩書院</td><td>Fanling Kau Yan College</td><td>資助</td><td>基督教</td><td>男女</td><td>中文</td><td>2C–2B</td><td>粉嶺欣盛里3號</td><td><a href="tel:26608405">26608405</a></td><td><a href="https://www.fkyc.edu.hk" target="_blank" rel="noopener" title="學校官網">www.fkyc.edu.hk</a></td></tr>
            <tr data-ss="aided"><td>鳳溪第一中學</td><td>Fung Kai No.1 Secondary School</td><td>資助</td><td>無</td><td>男女</td><td>中文</td><td>2</td><td>上水馬會道17號</td><td><a href="tel:26700366">26700366</a></td><td><a href="https://www.fk1ss.edu.hk" target="_blank" rel="noopener" title="學校官網">www.fk1ss.edu.hk</a></td></tr>
            <tr data-ss="aided"><td>明愛粉嶺陳震夏中學</td><td>Caritas Fanling Chan Chun Ha Secondary School</td><td>資助</td><td>天主教</td><td>男女</td><td>中文</td><td>3A</td><td>粉嶺新運路28號</td><td><a href="tel:26699966">26699966</a></td><td><a href="https://www.cfs.edu.hk" target="_blank" rel="noopener" title="學校官網">www.cfs.edu.hk</a></td></tr>
            <tr data-ss="aided"><td>新界喇沙中學</td><td>De La Salle Secondary School, N.T.</td><td>資助</td><td>天主教</td><td>男女</td><td>中文</td><td>3B</td><td>上水金錢村</td><td><a href="tel:26700443">26700443</a></td><td><a href="http://www.delasalle.edu.hk" target="_blank" rel="noopener" title="學校官網">www.delasalle.edu.hk</a></td></tr>
            <tr data-ss="aided"><td>聖芳濟各書院</td><td>St. Francis Of Assisi's College</td><td>資助</td><td>天主教</td><td>男女</td><td>中文</td><td>3A–2C</td><td>粉嶺欣盛里1號</td><td><a href="tel:26779702">26779702</a></td><td><a href="https://www.sfac.edu.hk" target="_blank" rel="noopener" title="學校官網">www.sfac.edu.hk</a></td></tr>
            <tr data-ss="aided"><td>中華基督教會基新中學</td><td>CCC Kei San Secondary School</td><td>資助</td><td>基督教</td><td>男女</td><td>中文</td><td>3A</td><td>粉嶺蝴蝶山路8號</td><td><a href="tel:26693906">26693906</a></td><td><a href="http://www.ks.edu.hk" target="_blank" rel="noopener" title="學校官網">www.ks.edu.hk</a></td></tr>
            <tr data-ss="gov"><td>粉嶺官立中學</td><td>Fanling Government Secondary School</td><td>官立</td><td>無</td><td>男女</td><td>中文</td><td>3</td><td>粉嶺一鳴路27號</td><td><a href="tel:26776778">26776778</a></td><td><a href="http://www.fgss.edu.hk" target="_blank" rel="noopener" title="學校官網">www.fgss.edu.hk</a></td></tr>
            <tr data-ss="gov"><td>上水官立中學</td><td>Sheung Shui Government Secondary School</td><td>官立</td><td>無</td><td>男女</td><td>中文</td><td>3C</td><td>上水百和路21號</td><td><a href="tel:26680628">26680628</a></td><td><a href="https://www.ssgss.edu.hk" target="_blank" rel="noopener" title="學校官網">www.ssgss.edu.hk</a></td></tr>
          </tbody>
        </table>
        </div>
        <p class="src">事實欄（種類/宗教/性別/語言/地址）：schooland.hk 北區頁 2026-10-31 核對＋教育局中學概覽；英中判定以教育局名單為準；Band＝坊間非官方估計；電話：schooland.hk 各校資料頁 2026-11-02 核對。</p>
      </div>
      <div class="gcard">
        <h3>東鐵沿線備選：大埔區中學 20 所（太和 / 大埔墟站）</h3>
        <p>北區之後的東鐵備選梯隊：羅湖出發約 15–20 分鐘到太和（估算，4 站），通關＋車程單程約 45–60 分鐘。事實欄（類型/語言/地址）經升學天地/教育王國/家委會概覽多源交叉（2026-11-02 核對）；Band＝坊間非官方參考；<b>近站為依地址所在社區的估算</b>，步行時間以地圖為準；電話可點擊直撥（手機）——號碼來源 schooland.hk 各校資料頁 2026-11-02 逐一核對，變動以學校官網為準。⚠️ 原大埔官立中學已於 2014 年停辦，已從表移除。</p>
        <div class="pg-chips" id="tpChips">
          <span class="chip on" data-tp="all">全部 20</span>
          <span class="chip" data-tp="en">英中 7</span>
          <span class="chip" data-tp="dss">直資 2</span>
          <span class="chip" data-tp="gov">官立 1</span>
        </div>
        <div class="scroll-x">
        <table class="mtable" id="tpTable">
          <thead><tr><th>學校</th><th>類型</th><th>教學語言</th><th>Band參考<br><span style="font-weight:400;color:#a33">非官方</span></th><th>近東鐵站<br><span style="font-weight:400;color:#a33">估算</span></th><th>備註</th><th>電話<br><span style="font-weight:400;color:#a33">核對 2026-11-02</span></th></tr></thead>
          <tbody>
            <tr data-tp="en"><td>迦密柏雨中學</td><td>資助</td><td>英中</td><td>1A</td><td>太和（大元邨）</td><td>區內龍頭，數理強</td><td><a href="tel:26650078">26650078</a></td></tr>
            <tr data-tp="en"><td>聖公會莫壽增會督中學</td><td>資助</td><td>英中</td><td>1B</td><td>大埔墟（運頭角里）</td><td>聖公會，校風嚴謹</td><td><a href="tel:26567804">26567804</a></td></tr>
            <tr data-tp="en"><td>王肇枝中學</td><td>資助</td><td>英中</td><td>1B</td><td>大埔墟（站旁）</td><td>大埔首間英中，通勤最省</td><td><a href="tel:26561270">26561270</a></td></tr>
            <tr data-tp="en"><td>恩主教書院</td><td>資助</td><td>英中</td><td>1B–1C</td><td>大埔墟（培賢里）</td><td>天主教，全人教育</td><td><a href="tel:26560017">26560017</a></td></tr>
            <tr data-tp="en"><td>南亞路德會沐恩中學</td><td>資助</td><td>英中</td><td>1C</td><td>太和（大元邨）</td><td>與柏雨同邨</td><td><a href="tel:26673129">26673129</a></td></tr>
            <tr data-tp="en dss"><td>羅定邦中學</td><td>直資</td><td>英中</td><td>2A</td><td>大埔墟（馬聰路）</td><td>直資英中，商科/ICT 特色</td><td><a href="tel:26851210">26851210</a></td></tr>
            <tr data-tp="en dss"><td>大埔三育中學</td><td>直資</td><td>英中</td><td>2</td><td>太和（大埔頭徑）</td><td>直資英中，學費約 $15,500；統一派位乙部 150 位分北區，跨境生備選友好</td><td><a href="tel:26653459">26653459</a></td></tr>
            <tr data-tp="aided"><td>救恩書院（大埔富善邨）</td><td>資助</td><td>中文（部分科目英文分組）</td><td>2B</td><td>太和/大埔墟之間</td><td>與「粉嶺救恩書院」同名不同校</td><td><a href="tel:26608308">26608308</a></td></tr>
            <tr data-tp="aided"><td>孔教學院大成何郭佩珍中學</td><td>資助</td><td>中英並重</td><td>2B</td><td>太和/大埔墟之間（富善邨）</td><td>孔教</td><td><a href="tel:26665926">26665926</a></td></tr>
            <tr data-tp="aided"><td>港九街坊婦女會孫方中書院</td><td>資助</td><td>中文</td><td>2B</td><td>大埔滘（需巴士短駁）</td><td>離站較遠</td><td><a href="tel:26567123">26567123</a></td></tr>
            <tr data-tp="aided"><td>香港道教聯合會圓玄學院第二中學</td><td>資助</td><td>中文</td><td>2B</td><td>太和/大埔墟之間（富善邨）</td><td>道教</td><td><a href="tel:26616038">26616038</a></td></tr>
            <tr data-tp="aided"><td>神召會康樂中學</td><td>資助</td><td>中文</td><td>2C–3</td><td>太和（寶雅苑）</td><td>已列北區表（接收北區跨境生）；體育特色</td><td><a href="tel:26520698">26520698</a></td></tr>
            <tr data-tp="aided"><td>迦密聖道中學</td><td>資助</td><td>中文</td><td>2C</td><td>太和（太和路）</td><td>基督教</td><td><a href="tel:26539786">26539786</a></td></tr>
                        <tr data-tp="gov"><td>新界鄉議局大埔區中學</td><td>官立</td><td>中文</td><td>3B</td><td>太和（大元邨）</td><td>官立免費</td><td><a href="tel:26643032">26643032</a></td></tr>
            <tr data-tp="aided"><td>中華聖潔會靈風中學</td><td>資助</td><td>中文</td><td>3A</td><td>太和（棟樑里）</td><td>基督教</td><td><a href="tel:29589694">29589694</a></td></tr>
            <tr data-tp="aided"><td>靈糧堂劉梅軒中學</td><td>資助</td><td>中文</td><td>3A</td><td>大埔墟（雍宜里）</td><td>基督教</td><td><a href="tel:26531234">26531234</a></td></tr>
            <tr data-tp="aided"><td>佛教大光慈航中學</td><td>資助</td><td>中文</td><td>3A</td><td>大埔墟（翠怡街）</td><td>佛教</td><td><a href="tel:26640833">26640833</a></td></tr>
            <tr data-tp="aided"><td>中華基督教會馮梁結紀念中學</td><td>資助</td><td>中文</td><td>3B</td><td>大埔墟（寶湖道）</td><td>基督教</td><td><a href="tel:26516033">26516033</a></td></tr>
            <tr data-tp="aided"><td>香港教師會李興貴中學</td><td>資助</td><td>中文</td><td>3B</td><td>大埔墟（運頭塘邨）</td><td>已列北區表；⭐ 有跨境學童支援</td><td><a href="tel:26317556">26317556</a></td></tr>
            <tr data-tp="aided"><td>香港紅卍字會大埔卍慈中學</td><td>資助</td><td>中文</td><td>3C</td><td>富亨邨（需巴士短駁）</td><td>離站較遠</td><td><a href="tel:26666821">26666821</a></td></tr>
          </tbody>
        </table>
        </div>
        <p class="src">來源：教育王國大埔區中學列表＋hkecec 大埔區中學組別表＋schooland（救恩書院頁）＋hkstudyroute 大埔排名，多源交叉 2026-11-02 核對；英中判定以教育局微調教學語言安排及各校官網為準（王肇枝＝EMI 官網確認）；Band／近站／車程＝坊間非官方估算，以學校官網與港鐵路線圖為準。</p>
      </div>
      <div class="gcard">
        <h3>升中攻略 · 外鏈精選（正文版權屬原站）</h3>
        <p><b>官方</b>：<a href="https://www.edb.gov.hk/en/student-parents/sch-info/sch-search/schlist-by-district/school-list-n.html" target="_blank" rel="noopener">教育局·北區中學名單</a>｜<a href="https://applications.edb.gov.hk/schoolsearch/" target="_blank" rel="noopener">教育局·學校搜尋（含收費證明書）</a>｜<a href="https://www.chsc.hk/ssp2025/" target="_blank" rel="noopener">家委會·中學概覽</a></p>
        <p><b>深讀（schooland）</b>：<a href="https://www.schooland.hk/post/sspa00" target="_blank" rel="noopener">中學學位分配辦法</a>｜<a href="https://www.schooland.hk/post/sspa01" target="_blank" rel="noopener">自行分配重點分析</a>｜<a href="https://www.schooland.hk/post/sspa02" target="_blank" rel="noopener">統一派位重點分析</a>｜<a href="https://www.schooland.hk/post/sspa03" target="_blank" rel="noopener">升中部署日誌</a>｜<a href="https://www.schooland.hk/post/ss-banding" target="_blank" rel="noopener">Banding 怎樣分</a>｜<a href="https://www.schooland.hk/ss/direct-subsidy" target="_blank" rel="noopener">直資中學學費比較</a>｜<a href="https://www.schooland.hk/ss/traditional-elite" target="_blank" rel="noopener">傳統名校名單</a>｜<a href="https://www.schooland.hk/ss/north" target="_blank" rel="noopener">北區中學頁</a></p>
        <p class="src">攻略文章版權屬各原站，此處僅收錄外鏈供家長延伸閱讀。</p>
      </div>
      <div class="src">來源：北區 20 所中學（schooland.hk 2026-10-31 核對＋hk-placement 知識庫 v0.2）｜Band 組別＝坊間非官方參考（教育局不公布官方 Banding）｜學費/截止日以學校官網當年公告為準｜⚠️ 身份硬門檻：身份 2027.6 才到手者一律走放榜後叩門＋途徑三</div>
    </div>
  <!-- 北區小學（v1.42 建；v1.49 併入擇校分檔 tab，不再全 sub 常顯） -->
  <div class="gsec">
    <h2>北區小學 30 所（P1–P6 插班 · 小一校網 80/81/83）</h2>
      <h3>🏫 小學插班時間線（以 2027.9 插小二為例——本家庭適用）</h3>
      <table class="mtable">
        <thead><tr><th style="width:90px">階段</th><th style="width:140px">時間</th><th>動作</th></tr></thead>
        <tbody>
          <tr><td>備戰期</td><td>2026.10–2027.2</td><td>收集成績單（蓋章）＋繁體/英文翻譯；定 6–8 所北區小學選校單（校網 <b>80 = 上水跨境最優</b>）；低小插班看重<b>聽說與識字</b>，英文起步以牛津樹繪本＋日常聽說為主</td></tr>
          <tr><td>申請高峰<br>（直接向學校申請）</td><td><b>2027.3–5</b></td><td>⚠️ 小學插班<b>沒有中央派位</b>——官津小學由各校自收插班生，逐校向校務處交表（電話先問是否收插班、收哪級）；直資/私立時間更早，逐校看公告</td></tr>
          <tr><td>筆面試</td><td>2027.5–7</td><td>低小多為<b>中英面談＋遊戲觀察</b>，部分校有簡單筆試（坊間整理，以各校為準）；同步辦香港身份證；教育局途徑三（區域教育服務處登記學位需求）<b>5–8 月</b>可登記，兜底不會沒書讀</td></tr>
          <tr><td>確認學位</td><td>2027.7–8</td><td>跟進各校空缺答覆；收 Offer 後 <b>3–7 天內繳留位費</b>；⚠️ 校巴/保姆車正期申請 <b>5–6 月</b>，7–8 月只能問補位</td></tr>
          <tr><td>入學</td><td>2027.9</td><td>辦內地學籍轉出；校服書單；跨境生出席首日安排（校巴線路/集合點 8 月底與營辦商確認）</td></tr>
        </tbody>
      </table>
      <div class="gcard warn">
        <h3>小學插班與中學的兩個關鍵區別</h3>
        <p>① <b>沒有統一派位</b>：中學插班還能蹭中一派位放榜後的叩門潮，小學插班全靠<b>逐校直接申請</b>，3–5 月就要動手，不能等 7 月；② <b>呈分試暫不相關</b>：呈分試影響中一派位，P5–P6 才關鍵——低小（P1–P3）插班主要看面談表現＋學位空缺，難度低於中學插班，但熱門校網（80）學位也緊張。</p>
        <p class="src">來源：教育局區域教育服務處插班安排（官方途徑）＋各校插班慣例（坊間整理）｜以各校官網當年公告為準</p>
      </div>

    <div class="gcard">
      <h3>🎯 小學插班怎麼用這張表（P1–P2 年齡段）</h3>
      <p>① <b>通勤選校網</b>：校網 80＝上水（羅湖口岸 1 站，跨境最優先看這網）；校網 81＝粉嶺/聯和墟（再一站，皇后山新校區偏一點）；校網 83＝沙頭角（邊境禁區範圍，通勤遠，跨境生一般要保姆車，普通家庭不建議）。</p>
      <p>② <b>插班申請邏輯</b>：官津小學插班<b>直接向學校申請</b>（不像小一有統一派位），學位有空缺就收——<b>照表打電話問校務處</b>最直接；官津插班窗口通行為每年 3–5 月（秋季入學），越早問越主動。以學校當年公告為準。</p>
      <p>③ <b>語言現實</b>：北區小學基本全中文（粵語）授課，P1–P2 插班年齡小、語言適應快，是小學階段最大優勢。標「普教中」的學校用普通話教中文科，內地生過渡更順：鳳溪創新（全校普教中）、靳茂生/于良發/沙頭角中心（部分班）。曾憲備小學＝中英並重雙語教學。</p>
      <p>④ <b>材料</b>：受養人簽證、出生紙、深圳成績單（翻譯+蓋章）、免疫接種記錄、住址證明。P5 前無呈分試，低年級插班以成績表＋面試為主，筆試壓力小。</p>
      <p class="src">事實欄（種類/校網/宗教/地址/電話）：schooland.hk 北區小學頁＋各校檔案頁＋教育局學校搜尋（馬錦燦地址以教育局為準），2026-11-02 核對；普教中名單＝schooland 匯總；插班窗口為坊間通行整理。以學校官網當年公告為準。</p>
    </div>
    <div class="chips" id="psChips">
      <span class="chip on" data-m="all">全部 30</span>
      <span class="chip" data-m="t1">首選·上水市區 12</span>
      <span class="chip" data-m="t2">常規·粉嶺/皇后山 14</span>
      <span class="chip" data-m="t3">偏遠·鄉郊邊境 4</span>
      <span class="chip" data-m="80">校網80 14</span>
      <span class="chip" data-m="81">校網81 14</span>
      <span class="chip" data-m="83">校網83 2</span>
      <span class="chip" data-m="gov">官立 1</span>
      <span class="chip" data-m="pth">普教中 5</span>
      <span class="chip" data-m="bil">雙語 1</span>
    </div>
    <p class="tip" style="margin:4px 0 10px">檔位＝跨境通勤便利粗分（依已核實地址推算，非官方）：首選＝上水市區（羅湖 1 站，步行/短保姆車可及）｜常規＝粉嶺/聯和墟/皇后山（東鐵 2 站）｜偏遠＝鄉郊/邊境（須保姆車）。點 chips 可疊加單選篩選。</p>
    <div class="scroll-x">
      <table class="mtable" id="psTable">
        <thead><tr><th style="width:52px">檔位</th><th>學校</th><th>類型</th><th>語言</th><th>校網 · 位置</th><th>備註</th><th>電話<br><span style="font-weight:400;color:#a33">核對 2026-11-02</span></th></tr></thead>
        <tbody>
          <tr data-m="80 t1"><td class="tier1">首選</td><td>香海正覺蓮社佛教正慧小學</td><td>資助</td><td>中文（粵）</td><td>80網 · 上水清城路6號</td><td>宗教·佛教｜2003創校，近上水站</td><td><a href="tel:26689088">2668 9088</a></td></tr>
          <tr data-m="80 t1"><td class="tier1">首選</td><td>育賢學校</td><td>資助</td><td>中文（粵）</td><td>80網 · 上水馬會道</td><td>1939創校，每級僅1班</td><td><a href="tel:26729917">2672 9917</a></td></tr>
          <tr data-m="80 t1"><td class="tier1">首選</td><td>石湖墟公立學校</td><td>資助</td><td>中文（粵）</td><td>80網 · 上水天平邨</td><td></td><td><a href="tel:26721225">2672 1225</a></td></tr>
          <tr data-m="80 t1"><td class="tier1">首選</td><td>東華三院港九電器商聯會小學</td><td>資助</td><td>中文（粵）</td><td>80網 · 上水石湖墟智昌路</td><td></td><td><a href="tel:26723285">2672 3285</a></td></tr>
          <tr data-m="80 t1"><td class="tier1">首選</td><td>東華三院馬錦燦紀念小學</td><td>資助</td><td>中文（粵）</td><td>80網 · 上水彩園邨（清城路2號）</td><td>⚠️ schooland 表行誤標沙田火炭，教育局+校方申請表確認上水彩園邨</td><td><a href="tel:26711071">2671 1071</a></td></tr>
          <tr data-m="80 t1"><td class="tier1">首選</td><td>香海正覺蓮社佛教陳式宏學校</td><td>資助</td><td>中文（粵）</td><td>80網 · 上水彩園邨</td><td>宗教·佛教｜近彩園邨，鄰近上水站</td><td><a href="tel:26724813">2672 4813</a></td></tr>
          <tr data-m="80 t3"><td class="tier3">偏遠</td><td>金錢村何東學校</td><td>資助</td><td>中文（粵）</td><td>80網 · 上水金錢村</td><td>鄉郊小校，近邊境</td><td><a href="tel:26703849">2670 3849</a></td></tr>
          <tr data-m="80 t2"><td class="tier2">常規</td><td>聖公會榮真小學</td><td>資助</td><td>中文（粵）</td><td>80網 · 粉嶺吉祥街3號</td><td>宗教·基督教｜地址在粉嶺但屬校網80</td><td><a href="tel:26703338">2670 3338</a></td></tr>
          <tr data-m="80 t1"><td class="tier1">首選</td><td>曾梅千禧學校</td><td>資助</td><td>中文（粵）</td><td>80網 · 上水清城路1號</td><td>30班大校，每級5班</td><td><a href="tel:26703111">2670 3111</a></td></tr>
          <tr data-m="80 t1"><td class="tier1">首選</td><td>上水惠州公立學校</td><td>資助</td><td>中文（粵）</td><td>80網 · 上水天平路51號</td><td></td><td><a href="tel:26731183">2673 1183</a></td></tr>
          <tr data-m="80 t1"><td class="tier1">首選</td><td>鳳溪第一小學</td><td>資助</td><td>中文（粵）</td><td>80網 · 上水馬會道19號</td><td>鳳溪系，校園超大型</td><td><a href="tel:26709353">2670 9353</a></td></tr>
          <tr data-m="80 t1 pth"><td class="tier1">首選</td><td>鳳溪創新小學</td><td>資助</td><td><b>全校普教中</b></td><td>80網 · 上水馬會道19號A</td><td><b>全校普教中</b>，4位外籍英語教師</td><td><a href="tel:26392201">2639 2201</a></td></tr>
          <tr data-m="80 t1"><td class="tier1">首選</td><td>李志達紀念學校</td><td>資助</td><td>中文（粵）</td><td>80網 · 上水天平路30號</td><td></td><td><a href="tel:26738581">2673 8581</a></td></tr>
          <tr data-m="80 t1"><td class="tier1">首選</td><td>東莞學校</td><td>資助</td><td>中文（粵）</td><td>80網 · 上水馬會道</td><td>1959創校</td><td><a href="tel:26700334">2670 0334</a></td></tr>
          <tr data-m="81 t2 gov"><td class="tier2">常規</td><td>粉嶺官立小學</td><td>官立</td><td>中文（粵）</td><td>81網 · 粉嶺祥華村</td><td>聯繫中學：粉嶺官立/上水官立（升中統一派位保留學位）</td><td><a href="tel:26692024">2669 2024</a></td></tr>
          <tr data-m="81 t2 pth"><td class="tier2">常規</td><td>五旬節靳茂生小學</td><td>資助</td><td>普教中（部分）</td><td>81網 · 粉嶺璧峰路4號</td><td>宗教·基督教｜普教中（部分班）</td><td><a href="tel:26700103">2670 0103</a></td></tr>
          <tr data-m="81 t2"><td class="tier2">常規</td><td>聖公會嘉福榮真小學</td><td>資助</td><td>中文（粵）</td><td>81網 · 粉嶺嘉福邨</td><td>宗教·基督教</td><td><a href="tel:29476888">2947 6888</a></td></tr>
          <tr data-m="81 t2"><td class="tier2">常規</td><td>基督教粉嶺神召會小學</td><td>資助</td><td>中文（粵）</td><td>81網 · 粉嶺和鳴里2號</td><td>宗教·基督教</td><td><a href="tel:29479966">2947 9966</a></td></tr>
          <tr data-m="81 t2"><td class="tier2">常規</td><td>鳳溪廖潤琛紀念學校</td><td>資助</td><td>中文（粵）</td><td>81網 · 粉嶺華明邨</td><td></td><td><a href="tel:26772311">2677 2311</a></td></tr>
          <tr data-m="81 t2"><td class="tier2">常規</td><td>方樹福堂基金方樹泉小學</td><td>資助</td><td>中文（粵）</td><td>81網 · 粉嶺華明邨二期</td><td></td><td><a href="tel:27082211">2708 2211</a></td></tr>
          <tr data-m="81 t2 pth"><td class="tier2">常規</td><td>五旬節于良發小學</td><td>資助</td><td>普教中（部分）</td><td>81網 · 粉嶺暉明路16號</td><td>宗教·基督教｜普教中（部分班）</td><td><a href="tel:26795626">2679 5626</a></td></tr>
          <tr data-m="81 t2"><td class="tier2">常規</td><td>上水宣道小學</td><td>資助</td><td>中文（粵）</td><td>81網 · 粉嶺聯和墟和睦路2號</td><td>宗教·基督教｜聯和墟中心位置</td><td><a href="tel:26702257">2670 2257</a></td></tr>
          <tr data-m="81 t2"><td class="tier2">常規</td><td>粉嶺公立學校</td><td>資助</td><td>中文（粵）</td><td>81網 · 粉嶺粉嶺村651號</td><td>1936創校</td><td><a href="tel:26702297">2670 2297</a></td></tr>
          <tr data-m="81 t2"><td class="tier2">常規</td><td>香海正覺蓮社佛教正覺蓮社學校</td><td>資助</td><td>中文（粵）</td><td>81網 · 粉嶺一鳴路12號</td><td>宗教·佛教</td><td><a href="tel:26754411">2675 4411</a></td></tr>
          <tr data-m="81 t2"><td class="tier2">常規</td><td>寶血會培靈學校</td><td>資助</td><td>中文（粵）</td><td>81網 · 粉嶺安樂村安樂門街13號</td><td>宗教·天主教</td><td><a href="tel:26756617">2675 6617</a></td></tr>
          <tr data-m="81 t2 bil"><td class="tier2">常規</td><td>東華三院曾憲備小學</td><td>資助</td><td><b>雙語（中英並重）</b></td><td>81網 · 粉嶺龍馬路53號（皇后山）</td><td>2021創校，<b>中英並重雙語教學</b></td><td><a href="tel:23709811">2370 9811</a></td></tr>
          <tr data-m="81 t2"><td class="tier2">常規</td><td>救世軍中原慈善基金皇后山學校</td><td>資助</td><td>中文（粵）</td><td>81網 · 粉嶺龍峻路2號（皇后山）</td><td>宗教·基督教｜2021創校新校</td><td><a href="tel:31510323">3151 0323</a></td></tr>
          <tr data-m="81 t3 pth"><td class="tier3">偏遠</td><td>打鼓嶺嶺英公立學校</td><td>資助</td><td>普教中（部分）</td><td>81網 · 打鼓嶺週田村</td><td>邊境鄉郊小校，普教中（部分班）；跨境通勤須保姆車</td><td><a href="tel:26740538">2674 0538</a></td></tr>
          <tr data-m="83 t3"><td class="tier3">偏遠</td><td>福德學社小學</td><td>資助</td><td>中文（粵）</td><td>83網 · 沙頭角山咀村</td><td>沙頭角邊境，通勤遠</td><td><a href="tel:26742120">2674 2120</a></td></tr>
          <tr data-m="83 t3 pth"><td class="tier3">偏遠</td><td>沙頭角中心小學</td><td>資助</td><td>普教中（部分）</td><td>83網 · 沙頭角墟第四區</td><td>普教中（部分班）；沙頭角屬邊境禁區範圍</td><td><a href="tel:26749080">2674 9080</a></td></tr>
        </tbody>
      </table>
    </div>
  </div>
  </div><!-- /schoolsView -->

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

  <!-- 常見問題 FAQ（v1.40） -->
  <div class="wrap" id="faqView" style="display:none">
    <div class="gsec">
      <h2>家長最常問的 10 個問題</h2>
      <p class="tip">答案為坊間整理＋hk-placement 知識庫（2026-10 至 11 核對），一切以教育局、學校官網當年公告為準。</p>
      <div class="gcard"><h3>① 幾年級插班最合適？</h3><p>通行說法「最遲中三前」——中四起課程落差與 DSE 壓力大增；小學階段越早越從容（坊間整理）。P5–P6 有呈分試，插進去就直項考試，更要提前備。</p></div>
      <div class="gcard"><h3>② 需要什麼身份？</h3><p><b>受養人簽證是硬門檻</b>（須有在港工作/就讀的監護人），單程證/永居亦可。辦理以入境事務處官方為準。</p></div>
      <div class="gcard"><h3>③ 插班考什麼？怎麼準備？</h3><p>筆試（中英數，英文最關鍵）＋面試（可能粵語/英語作答）。直資校自主命題，各校題型不同；官津多看成績表＋隨機測。考前 8–10 週切題型與面試模擬，別裸考。</p></div>
      <div class="gcard"><h3>④ 英文要到什麼水平？</h3><p>英文決定你能進<b>英中還是中中</b>，是最重的一項。先做定級（閱讀/寫作/口語），再按「80% 建能力 + 20% 熟題型」排計劃（見「學習路線」子頁）。</p></div>
      <div class="gcard"><h3>⑤ 呈分試和 Banding 是什麼？</h3><p>呈分試＝小五下學期起的三次校內考，成績直接影響升中派位組別；Band 1–3 組別由派位結果反推，<b>教育局不公布官方 Banding</b>，坊間版本僅作參考。</p></div>
      <div class="gcard"><h3>⑥ 有校車嗎？</h3><p>校巴/保姆車由私營營辦商按線路經營（一般 5–6 月申請），中學線路遠少於小學；北區中學跨境生主流是<b>自行搭東鐵</b>（1–2 站）。有沒有線路逐校電話校務處問（擇校表內有電話）。</p></div>
      <div class="gcard"><h3>⑦ 官津和直資學費差多少？</h3><p>官立/資助中學免學費；直資校收學費，幾千到數萬一年不等（各校官網當年公布為準，站內擇校表已標注已知直資）。</p></div>
      <div class="gcard"><h3>⑧ 內地學籍要註銷嗎？</h3><p>拿到港校 Offer 前<b>不要註銷</b>。先拿 Offer 再轉出，保留退路。</p></div>
      <div class="gcard"><h3>⑨ 大學學額有什麼新政？</h3><p>⚠️ 2028/29 學年起，人才計劃子女申請政府資助大專學額須<b>居港滿 2 年</b>。目標 DSE 讀本地資助大學的話，要提前倒推搬港時間線（見「身份政策」子頁）。</p></div>
      <div class="gcard"><h3>⑩ 材料清單在哪看？</h3><p>本站「材料清單」子頁有完整版：身份類/學業類（蓋章+翻譯）/健康類/住址類/加分類。建議提前一個學期開始備，翻譯公證有周期。</p></div>
      <div class="src">來源：hk-placement 知識庫 v0.2＋通行插班實務（坊間整理，2026-11-02 歸納）；居港 2 年政策為官方公報內容，個案以官方為準</div>
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
<div id="examPrintSheet" class="en-print"></div>

<!-- v1.48 悬浮咨询 -->
<div id="ctaFab"><button id="ctaFabBtn">💬 諮詢葉工</button></div>
<div class="mask" id="ctaMask">
  <div class="modal" id="ctaModal">
    <span class="x" id="ctaClose">×</span>
    <h2>諮詢葉工</h2>
    <p class="sub">擇校分析｜插班時間線｜學習規劃——直接加微信，備註「插班」</p>
    <div class="wechat">SteveHKSZ</div>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <button class="btn" id="ctaCopy" style="padding:9px 16px">📋 複製微信號</button>
      <a class="btn" href="mailto:hkeec2023@gmail.com" style="padding:9px 16px;text-decoration:none">📧 郵件諮詢</a>
    </div>
    <p style="font-size:12px;color:#8a8aa0;margin-top:12px">公眾號：史蒂夫HKSZ｜免費回答，擇校數據以教育局及學校官網為準</p>
  </div>
</div>

<div class="wrap" id="aboutView">
  <div class="gcard about-card">
    <h2>關於葉工 · 諮詢與合作</h2>
    <p>葉工（公眾號「史蒂夫HKSZ」）：香港註冊專業工程師（RPE）、英國特許工程師（CEng）、香港科技大學碩士，深港雙城生活。本站最初為女兒的插班學習工具，現免費開放給同路的內地家庭。</p>
    <p>📧 <a href="mailto:hkeec2023@gmail.com">hkeec2023@gmail.com</a>（諮詢／合作／勘誤）　💬 微信號：<b>SteveHKSZ</b>（擇校諮詢直接加）　💬 公眾號搜「史蒂夫HKSZ」（插班乾貨更新）　🗓 或郵件留言（孩子年級／身份／目標），會回覆安排</p>
    <!-- TODO(v1.41+): 預約表單外鏈（騰訊問卷/金數據，待葉工開通帳號後填入）；數據埋點（51la/umami，同） -->
    <p class="folk">⚠️ 免責聲明：本站內容為公開資料整理與非官方參考（Band 組別等均非教育局公布），一切以學校官網、教育局、考評局當年公布為準；本站不構成任何升學承諾；牛津樹／朗文等教材內容僅限家庭學習，勿商用或外傳。</p>
  </div>
</div>

<footer>
<!-- Credits (not displayed): 詞表源自 word-atlas（CC BY 4.0, Word Atlas contributors）；詩文取自 chinese-poetry 收錄之公有領域古典詩文；拼音 pypinyin；粵拼 jyutping。 -->
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
// 繁體字庫 v2（v1.25）：按年級分級。分級＝自編（按簡體字常用度＋繁體書寫複雜度遞增），非教育局官方分級；
// 一簡對多繁者第三位元素給注記（如 里→裡/裏 依詞義選）。
const FT_GRADES={
 P1:[['说','說'],['来','來'],['时','時'],['会','會'],['国','國'],['学','學'],['后','後'],['开','開'],['关','關'],['里','裡','一簡對多繁：裡/裏 依詞義'],['动','動'],['问','問'],['过','過'],['还','還'],['给','給'],['见','見'],['间','間'],['话','話'],['长','長'],['东','東'],['车','車'],['马','馬'],['门','門'],['风','風'],['飞','飛'],['电','電'],['头','頭'],['体','體'],['发','發','毛髮義讀髮'],['经','經'],['红','紅'],['钱','錢'],['纸','紙'],['书','書'],['写','寫'],['读','讀'],['习','習'],['贝','貝'],['云','雲'],['乌','烏'],['页','頁'],['这','這'],['们','們'],['两','兩']],
 P2:[['买','買'],['卖','賣'],['让','讓'],['谢','謝'],['请','請'],['闻','聞'],['认','認'],['识','識'],['记','記'],['试','試'],['变','變'],['选','選'],['达','達'],['运','運'],['进','進'],['远','遠'],['递','遞'],['带','帶'],['帮','幫'],['与','與'],['义','義'],['为','為'],['专','專'],['办','辦'],['无','無'],['从','從'],['万','萬'],['亿','億'],['优','優'],['伤','傷'],['价','價'],['众','眾'],['传','傳'],['伟','偉'],['兴','興'],['举','舉'],['严','嚴'],['临','臨'],['丽','麗'],['乐','樂'],['乱','亂'],['亏','虧'],['爱','愛'],['亲','親'],['个','個'],['边','邊'],['师','師']],
 P3:[['鸟','鳥'],['鱼','魚'],['龙','龍'],['龟','龜'],['鸡','雞'],['鸭','鴨'],['猫','貓'],['猪','豬'],['脸','臉'],['脑','腦'],['齿','齒'],['树','樹'],['叶','葉'],['岛','島'],['湾','灣'],['陆','陸'],['桥','橋'],['兰','蘭'],['岁','歲'],['历','歷','日曆義讀曆'],['声','聲'],['响','響'],['鹅','鵝'],['猎','獵'],['兽','獸'],['献','獻'],['环','環'],['场','場'],['尘','塵'],['湿','濕'],['满','滿'],['圆','圓'],['团','團'],['图','圖'],['园','園'],['华','華'],['层','層'],['币','幣'],['针','針'],['钟','鐘'],['网','網']],
 P4:[['铁','鐵'],['银','銀'],['钢','鋼'],['贵','貴'],['双','雙'],['对','對'],['总','總'],['应','應'],['该','該'],['谁','誰'],['松','鬆','緊鬆義讀鬆，鬆樹同'],['紧','緊'],['净','淨'],['热','熱'],['广','廣'],['厂','廠'],['馆','館'],['县','縣'],['乡','鄉'],['区','區'],['农','農'],['军','軍'],['护','護'],['医','醫'],['药','藥'],['礼','禮'],['胜','勝'],['败','敗'],['输','輸'],['赢','贏'],['导','導'],['卫','衛'],['课','課'],['视','視'],['验','驗'],['检','檢'],['难','難'],['绿','綠'],['杂','雜'],['务','務'],['备','備'],['类','類']],
 P5:[['处','處'],['复','復','重複義讀複'],['怀','懷'],['惊','驚'],['坏','壞'],['旧','舊'],['势','勢'],['击','擊'],['压','壓'],['协','協'],['忆','憶'],['梦','夢'],['汇','匯'],['术','術'],['报','報'],['语','語'],['讲','講'],['观','觀'],['觉','覺'],['养','養'],['劳','勞'],['颗','顆'],['绍','紹'],['译','譯'],['词','詞'],['诗','詩'],['级','級'],['结','結'],['续','續'],['纪','紀'],['纯','純'],['约','約'],['织','織'],['组','組'],['细','細'],['终','終'],['获','獲'],['两岸','兩岸'],['只','隻','量詞讀隻；只是義仍作只'],['几','幾','詢問數量讀幾']],
 P6:[['链','鏈'],['锁','鎖'],['错','錯'],['键','鍵'],['简','簡'],['篮','籃'],['条','條'],['联','聯'],['统','統'],['继','繼'],['绝','絕'],['缓','緩'],['编','編'],['缘','緣'],['纲','綱'],['纳','納'],['纵','縱'],['纷','紛'],['练','練'],['尽','盡','儘管義讀儘'],['属','屬'],['妇','婦'],['归','歸'],['当','當'],['录','錄'],['弃','棄'],['丧','喪'],['实','實'],['态','態'],['忧','憂'],['懒','懶'],['择','擇'],['担','擔'],['连','連'],['迟','遲'],['适','適'],['灵','靈'],['烟','煙'],['灯','燈'],['炉','爐'],['烂','爛'],['轻','輕'],['镜','鏡']]
};
const FT_MAP=[].concat(...Object.values(FT_GRADES));

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
let curTab='plan', curGuide='cn', curPractice='cn', curPlan='timeline';
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

// ---- v1.48 悬浮咨询按钮 ----
(function(){
  const fab=document.getElementById('ctaFabBtn'),mask=document.getElementById('ctaMask'),x=document.getElementById('ctaClose');
  if(!fab||!mask)return;
  fab.onclick=()=>mask.classList.add('show');
  x.onclick=()=>mask.classList.remove('show');
  mask.onclick=e=>{if(e.target===mask)mask.classList.remove('show')};
  const cp=document.getElementById('ctaCopy');
  if(cp)cp.onclick=()=>{
    const t='SteveHKSZ', done=()=>{const o=cp.textContent;cp.textContent='✅ 已複製';setTimeout(()=>cp.textContent=o,1500);};
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done).catch(()=>fallback());}
    else fallback();
    function fallback(){const i=document.createElement('input');i.value=t;document.body.appendChild(i);i.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(i);done();}
  };
})();

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
function swPlan(s){
  curPlan=s;
  document.querySelectorAll('#planSub button').forEach(x=>x.classList.toggle('on',x.dataset.sub===s));
  ['timeline','schools','docs','study','policy','faq'].forEach(t=>{const el=document.getElementById(t+'View'); if(el) el.style.display = t===s?'block':'none';});
}
document.querySelectorAll('#planSub button').forEach(b=>b.onclick=()=>swPlan(b.dataset.sub));
// v1.48 擇校頁小學/中學置頂切換（滾動定位＋記住上次）
function jmpSch(k){
  const t=document.getElementById(k==='pri'?'psTable':'ssTable'); if(!t)return;
  const g=t.closest('.gsec')||t; if(g.scrollIntoView)g.scrollIntoView({behavior:'smooth',block:'start'});
  try{localStorage.setItem('hkk_lastSchool',k)}catch(e){}
}
(function(){
  const a=document.getElementById('jmpPri'),b=document.getElementById('jmpSec'); if(!a||!b)return;
  a.onclick=()=>jmpSch('pri'); b.onclick=()=>jmpSch('sec');
  let last=null; try{last=localStorage.getItem('hkk_lastSchool')}catch(e){}
  if(last){const el=last==='pri'?a:b; el.style.borderColor='#0d9488'; el.style.color='#0d9488';}
})();
// 英文練習內部分類切換（港小生字 / 詞表）
// ---- v1.24 呈分試卷（英文呈分試模擬卷 · P5–P6 · 仿編原創） ----
// 版式仿照坊間呈分試卷：生詞表＋詞形填空＋明喻/習語/時態篇章/職業對話/情境造句/短語動詞/量詞連詞/閱讀理解，全卷 100%。
// ⚠️ 題目全部本地原創仿編，非任何補習社／學校／評估局真卷。
let curExamGrade='P6', curExamPaper=null;
const EXAM_QBANK={
P5:{
 heads:[
  {words:[{w:'celebrate (v.)',zh:'慶祝'},{w:'tradition (n.)',zh:'傳統'},{w:'lantern (n.)',zh:'燈籠'},{w:'reunion (n.)',zh:'團聚'},{w:'decorate (v.)',zh:'佈置／裝飾'},{w:'delicious (adj.)',zh:'美味的'},{w:'gather (v.)',zh:'聚集'},{w:'ancestor (n.)',zh:'祖先'}],
   fills:[{s:'Chinese people {0} the Mid-Autumn Festival with mooncakes and lanterns.',a:['celebrate']},{s:'My grandparents {0} at our home for a big reunion dinner last night.',a:['gathered']},{s:'We {0} the Christmas tree with colourful balls and stars every year.',a:['decorate']},{s:'It is a {0} for children to receive red packets at Lunar New Year.',a:['tradition']},{s:'The mooncakes from that bakery are really {0} .',a:['delicious']}]},
  {words:[{w:'exercise (v./n.)',zh:'運動'},{w:'healthy (adj.)',zh:'健康的'},{w:'junk food (n.)',zh:'垃圾食物'},{w:'energy (n.)',zh:'精力／能量'},{w:'habit (n.)',zh:'習慣'},{w:'rest (v.)',zh:'休息'},{w:'stretch (v.)',zh:'伸展'},{w:'balance (n.)',zh:'平衡'}],
   fills:[{s:'Tom {0} for thirty minutes every morning before school.',a:['exercises']},{s:'Eating too much {0} like chips and sweets is bad for your body.',a:['junk food']},{s:'A good sleep helps our bodies {0} and grow.',a:['rest']},{s:'Remember to {0} your legs before you run.',a:['stretch']},{s:'A balanced diet gives us the {0} we need for the day.',a:['energy']}]}
 ],
 A:[
  {bank1:['big','sweet','slow','cool','red','hungry'],bank2:['an elephant','honey','a snail','a cucumber','a tomato','a wolf'],items:[
   {s:'The watermelon felt as {0} as {1} on a hot afternoon.',a:['cool','a cucumber']},
   {s:'Grandpa walks as {0} as {1} in the park every morning.',a:['slow','a snail']},
   {s:'Kitty was as {0} as {1} after the long hike up the hill.',a:['hungry','a wolf']},
   {s:'Uncle Chan’s new car is as {0} as {1} .',a:['big','an elephant']},
   {s:'Grandma’s homemade jam tastes as {0} as {1} .',a:['sweet','honey']},
   {s:'Peter’s face turned as {0} as {1} after he ran so fast.',a:['red','a tomato']}]},
  {bank1:['hard','busy','gentle','shiny','tall','fast'],bank2:['a rock','an ant','a lamb','a mirror','a giraffe','lightning'],items:[
   {s:'The ice on the ground was as {0} as {1} yesterday morning.',a:['hard','a rock']},
   {s:'May is as {0} as {1} during the exam week.',a:['busy','an ant']},
   {s:'The new puppy is as {0} as {1} — it never bites anyone.',a:['gentle','a lamb']},
   {s:'After polishing, the floor of the hall was as {0} as {1} .',a:['shiny','a mirror']},
   {s:'The new player runs as {0} as {1} on the football field.',a:['fast','lightning']},
   {s:'The tree in our school garden is as {0} as {1} .',a:['tall','a giraffe']}]},
  {bank1:['hot','tall','fast','pretty','white','cold'],bank2:['the sun','a mountain','the wind','a picture','snow','ice'],items:[
   {s:'The tea is still as {0} as {1} — do not drink it yet.',a:['hot','the sun']},
   {s:'The pine tree on the hill looks as {0} as {1} from far away.',a:['tall','a mountain']},
   {s:'The runner dashed as {0} as {1} to the finish line.',a:['fast','the wind']},
   {s:'The garden in full bloom looked as {0} as {1} .',a:['pretty','a picture']},
   {s:'After the heavy snowfall, the whole field was as {0} as {1} .',a:['white','snow']},
   {s:'After skating for an hour, my hands were as {0} as {1} .',a:['cold','ice']}]}
 ],
 B:[
  {bank:['rain cats and dogs','cry over spilt milk','in the same boat','busy as a bee','slept like a log','as easy as ABC'],items:[
   {s:'It started to {0} just as we left for the picnic.',a:['rain cats and dogs']},
   {s:'Do not {0} about the broken cup — it cannot be fixed anyway.',a:['cry over spilt milk']},
   {s:'We are all {0} because none of us knows the answer.',a:['in the same boat']},
   {s:'Mary was {0} all morning, cleaning every corner of the house.',a:['busy as a bee']},
   {s:'After the tiring trip, Dad {0} for ten whole hours.',a:['slept like a log']},
   {s:'Do not worry — the test is {0} if you have studied hard.',a:['as easy as ABC']}]},
  {bank:['once in a blue moon','give someone a hand','feel blue','keep a secret','in a nutshell','make up one’s mind'],items:[
   {s:'We only eat at that expensive restaurant {0} .',a:['once in a blue moon']},
   {s:'Can you {0} with these heavy bags, please?',a:['give me a hand','give us a hand']},
   {s:'Tim has felt {0} since his best friend moved away.',a:['blue']},
   {s:'A true friend knows how to {0} .',a:['keep a secret']},
   {s:'{0} , we won the game but lost the trophy.',a:['in a nutshell']},
   {s:'Kitty could not {0} about which dress to wear.',a:['make up her mind']}]},
  {bank:['a black sheep','give the green light','see red','have egg on one’s face','once in a blue moon','a slip of the tongue'],items:[
   {s:'Jenny accidentally called her teacher “Mum” — it was {0} , and the whole class laughed.',a:['a slip of the tongue','slip of the tongue']},
   {s:'If you tell a lie, you might {0} when the truth comes out.',a:['have egg on your face','have egg on one’s face']},
   {s:'We visit our grandparents’ farm {0} because it is quite far away.',a:['once in a blue moon']},
   {s:'Even though Tim loved football, he often felt like {0} in his family of basketball fans.',a:['a black sheep','black sheep']},
   {s:'The principal {0} for the school talent show to proceed as planned.',a:['gave the green light','gave the green light for']},
   {s:'When Jenny saw her classmate teasing her best friend, she began to {0} .',a:['see red']}]}
 ],
 C:[
  {s:'Last Friday, our class (e.g.) went (go) on a picnic in Tai Po Waterfront Park. The weather (1) {0} (be) sunny and cool. When we (2) {1} (arrive), some classmates (3) {2} (fly) kites on the grass. Miss Chan (4) {3} (teach) us how to make kites last month, so we all (5) {4} (bring) our own kites. At noon, we (6) {5} (share) the sandwiches that Mum (7) {6} (make) the night before. Suddenly, a strong wind (8) {7} (blow) and one kite (9) {8} (land) in a tall tree! A kind uncle (10) {9} (help) us get it back.',
   a:[['was'],['arrived'],['were flying'],['taught'],['brought'],['shared'],['made'],['blew'],['landed'],['helped']]},
  {s:'My cat Mochi (e.g.) is (be) three years old. She (1) {0} (have) big green eyes and soft grey fur. Every evening, she (2) {1} (sit) by the window and (3) {2} (watch) the birds outside. Last month, she (4) {3} (catch) her first cockroach, and we (5) {4} (be) all very proud. Mochi (6) {5} (not like) loud noises, so she always (7) {6} (hide) under the sofa during Chinese New Year. Now she (8) {7} (sleep) on my lap while I (9) {8} (write) this passage. I hope she (10) {9} (live) with us for many more years.',
   a:[['has'],['sits'],['watches'],['caught'],['were'],['does not like','don’t like','dont like'],['hides'],['is sleeping'],['am writing'],['will live']]},
  {s:'Last Friday, our school (e.g.) held (hold) its annual Sports Day at the Sha Tin Sports Ground. The weather (1) {0} (be) perfect for running. In the morning, the headmaster (2) {1} (give) a short speech and then the races (3) {2} (begin). My best friend Ken (4) {3} (come) first in the 100-metre race, and our class (5) {4} (cheer) loudly for him. At noon, we (6) {5} (eat) lunch under the trees and (7) {6} (rest) before the afternoon events. In the relay race, Class 4B (8) {7} (drop) the baton, but they still (9) {8} (finish) the race with smiles. On the bus home, everyone (10) {9} (feel) tired but happy.',
   a:[['was'],['gave'],['began'],['came'],['cheered'],['ate'],['rested'],['dropped'],['finished'],['felt']]},
  {s:'My name is Tim and I (e.g.) live (live) in Shenzhen. Every school day, I (1) {0} (wake) up at half past five. My mother (2) {1} (make) breakfast while I (3) {2} (pack) my school bag. We then (4) {3} (take) the early train to the border. I never (5) {4} (forget) my travel documents because Mum (6) {5} (check) my bag every night. On the train, I often (7) {6} (revise) my spelling words. My friend Ada and I (8) {7} (play) word games when the journey is long. Our teacher (9) {8} (say) that reading on the train (10) {9} (be) a good habit.',
   a:[['wake'],['makes'],['pack'],['take'],['forget'],['checks'],['revise'],['play'],['says'],['is']]},
  {s:'Next Thursday, our class (e.g.) will visit (visit) the Hong Kong Science Museum. The bus (1) {0} (leave) the school gate at half past eight. Miss Cheung (2) {1} (remind) us to bring a pencil for the worksheet. At the museum, we (3) {2} (watch) a robot show first. Then a scientist (4) {3} (teach) us how to make simple circuits. I hope we (5) {4} (see) the giant dinosaur model too. Kitty (6) {5} (bring) her camera because she (7) {6} (want) to take photos of the space gallery. In the afternoon, we (8) {7} (eat) lunch at the museum café before we (9) {8} (return) to school. I believe it (10) {9} (be) the best trip this year.',
   a:[['will leave','leaves'],['will remind','reminds'],['will watch','watch'],['will teach','teaches'],['will see','see'],['will bring','brings'],['wants'],['will eat','eat'],['return','will return'],['will be']]}
 ],
 D:[
  {bank:['teacher','nurse','police officer','farmer','singer'],lines:[
   {who:'Polly',s:'I like helping sick people and taking their temperature. I want to be a (1) {0} .',a:['nurse']},
   {who:'Kelly',s:'I enjoy singing and I practise every day after school. I want to be a (2) {0} .',a:['singer']},
   {who:'Amy',s:'I want to keep our city safe and help people find their lost things. I want to be a (3) {0} .',a:['police officer']},
   {who:'Samuel',s:'I love books and I want to help children learn in a classroom. I want to be a (4) {0} .',a:['teacher']},
   {who:'Nathan',s:'I want to grow vegetables and take care of pigs and chickens in the countryside. I want to be a (5) {0} .',a:['farmer']}]},
  {bank:['postman','baker','lifeguard','zookeeper','bus driver'],lines:[
   {who:'Polly',s:'I can swim very well and I want to save people at the beach. I want to be a (1) {0} .',a:['lifeguard']},
   {who:'Kelly',s:'I get up very early to deliver letters to every home. I want to be a (2) {0} .',a:['postman']},
   {who:'Amy',s:'I love animals and I feed the lions and monkeys every day. I want to be a (3) {0} .',a:['zookeeper']},
   {who:'Samuel',s:'I drive carefully and take people to different parts of the city. I want to be a (4) {0} .',a:['bus driver']},
   {who:'Nathan',s:'I get up at four o’clock to make bread and cakes for the neighbourhood. I want to be a (5) {0} .',a:['baker']}]},
  {bank:['extra','scriptwriter','film director','costume designer','stuntman'],lines:[
   {who:'Polly',s:'I act in films, but my parts are usually very small. I want to be an (1) {0} .',a:['extra']},
   {who:'Kelly',s:'I design beautiful clothes for the actors to wear on screen. I want to be a (2) {0} .',a:['costume designer']},
   {who:'Amy',s:'I write the stories and dialogues for the movies. I want to be a (3) {0} .',a:['scriptwriter']},
   {who:'Samuel',s:'I often shout “action” and “cut” on the film set. I want to be a (4) {0} .',a:['film director']},
   {who:'Nathan',s:'I do the dangerous parts in films so the main actors do not get hurt. I want to be a (5) {0} .',a:['stuntman']}]}
 ],
 E:[
  {bank:['children make snowmen','we should take an umbrella','it is a good day for a picnic','the leaves fall from the trees'],items:[
   {lead:'Since the sky is clear and sunny,',a:['it is a good day for a picnic']},
   {lead:'Since autumn comes and the wind gets stronger,',a:['the leaves fall from the trees']},
   {lead:'Since it is snowing heavily outside,',a:['children make snowmen']},
   {lead:'Since dark clouds are gathering in the sky,',a:['we should take an umbrella']}]},
  {bank:['people should stay indoors','plants may die','we must save electricity','the streets get busy'],items:[
   {lead:'Since it is a public holiday today,',a:['the streets get busy']},
   {lead:'Since global energy is becoming more and more precious,',a:['we must save electricity']},
   {lead:'Since there has been no rain for weeks,',a:['plants may die']},
   {lead:'Since the air pollution index is very high today,',a:['people should stay indoors']}]}
 ],
 F:[
  {bank:['get up','wake up','put on','turn off','look at','take out'],s:'Every morning, Mum (e.g.) wakes me up at seven. I (1) {0} at once and (2) {1} my school uniform. After breakfast, I remember to (3) {2} the lights before leaving home. On the school bus, I like to (4) {3} the scenery outside the window. When it rains, I (5) {4} my umbrella before I get off.',a:[['get up'],['put on'],['turn off'],['look at'],['take out']]},
  {bank:['sit down','write down','look for','pick up','give back','come back'],s:'Yesterday, Amy (e.g.) looked for books about dinosaurs in the school library. First she (1) {0} at a quiet table and (2) {1} the names of three books about space. Then she (3) {2} a big book about the solar system and started reading. Before leaving, she (4) {3} the storybook she borrowed last week and promised to (5) {4} next Saturday.',a:[['sat down'],['wrote down'],['picked up'],['gave back'],['come back']]}
 ],
 G:[
  {bank:['very few','very little','enough','either…or','neither…nor'],lines:[
   {who:'Mum',s:'Ruby, you can have (1) {0} fried noodles (2) {1} dumplings for dinner tonight.'},
   {who:'Ruby',s:'But there is (3) {2} fried noodles (4) {3} dumplings left in the fridge, Mum.'},
   {who:'Mum',s:'Hurry then! There are only (5) {4} eggs and (6) {5} rice, so I will make soup too.'}],
   a:[['either'],['or'],['neither'],['nor'],['very few'],['very little']]},
  {bank:['both…and','either…or','very few','very little','enough'],lines:[
   {who:'Librarian',s:'You can borrow (1) {0} this storybook (2) {1} that comic, but not both.'},
   {who:'Ben',s:'Great! Can I (3) {2} borrow books (3) {3} read magazines here?'},
   {who:'Librarian',s:'Sure. But there are only (4) {4} seats left at noon, and there is (5) {5} space in the reading corner.'}],
   a:[['either'],['or'],['both'],['and'],['very few'],['very little']]}
 ],
 H:[
  {title:'Sea Turtles in Hong Kong',
   s:'Every summer, a few sea turtles come to lay their eggs on the quiet beaches of Hong Kong. Green sea turtles can grow to more than one metre long and live for over sixty years. They swim thousands of kilometres across the ocean, but they always return to the beach where they were born to lay their eggs.<br>Sadly, sea turtles face many dangers. Plastic bags in the sea look like jellyfish, one of their favourite foods. If a turtle eats a plastic bag, it may die. Lights from beachside buildings also confuse baby turtles, which follow the light instead of crawling towards the sea.<br>In Hong Kong, it is illegal to disturb the beaches where sea turtles lay their eggs. Scientists hope that with everyone’s help, these gentle animals will keep visiting our shores.',
   mc:[{q:'How far do sea turtles swim to lay their eggs?',opts:['A few metres','Thousands of kilometres','Sixty kilometres','More than one metre'],a:1},
       {q:'Why are plastic bags dangerous to sea turtles?',opts:['They are too heavy to carry.','They stop turtles from swimming fast.','They look like jellyfish, one of their favourite foods.','They make the sea water dirty.'],a:2}],
   open:[{q:'Where do sea turtles lay their eggs?',keys:['beach','born'],model:'They return to the beach where they were born to lay their eggs.'},
         {q:'Why do lights confuse baby turtles?',keys:['follow','light'],model:'Because the baby turtles follow the light instead of crawling towards the sea.'}],
   fill:{q:'In Hong Kong, it is illegal to {0} the beaches where sea turtles lay their eggs.',a:[['disturb']]}},
  {title:'The Star Ferry',
   s:'The Star Ferry is one of the oldest forms of public transport in Hong Kong. The famous green-and-white boats have carried passengers across Victoria Harbour for over a hundred years. A ride from Tsim Sha Tsui to Central takes only about ten minutes and costs just a few dollars.<br>Many people think the ferry is only for tourists, but thousands of commuters still use it every day. It is also a friendlier choice for the environment because ferries use less fuel per passenger than cars.<br>In a recent survey, visitors from around the world named the short ride one of the best cheap experiences in the world.',
   mc:[{q:'How long does a ride from Tsim Sha Tsui to Central take?',opts:['About ten minutes','About a hundred years','A few dollars','One whole day'],a:0},
       {q:'Why is the ferry a friendlier choice for the environment?',opts:['It is green and white.','It carries many tourists.','It costs only a few dollars.','It uses less fuel per passenger than cars.'],a:3}],
   open:[{q:'Who still uses the ferry every day?',keys:['commuters'],model:'Thousands of commuters still use it every day.'},
         {q:'Where do the boats run?',keys:['tsim sha tsui','central'],model:'They run between Tsim Sha Tsui and Central or Wan Chai.'}],
   fill:{q:'A ferry ride across Victoria Harbour costs just a few {0} .',a:[['dollars']]}},
  {title:'Wet Markets in Hong Kong',
   s:'Early in the morning, wet markets all over Hong Kong become busy and noisy. Vendors shout to attract customers, and the smells of fresh fish, fruit and flowers fill the air. A wet market is a group of stalls selling fresh food, such as vegetables, meat, seafood and eggs.<br>Many people believe that food from wet markets is fresher than food from supermarkets, because most of it arrives from local farms and fishing boats early every morning. Customers can also ask the vendors to choose, weigh and even prepare the food for them.<br>However, fewer young people shop at wet markets now. Some markets have been moved into air-conditioned buildings so that shoppers can stay cool in summer and dry in the rain.',
   mc:[{q:'What is a wet market?',opts:['A supermarket in a building.','A group of stalls selling fresh food.','A fishing boat from a local farm.','A restaurant selling vegetables.'],a:1},
       {q:'Why is some wet market food very fresh?',opts:['Because it is frozen quickly.','Because it comes from other countries.','Because it arrives from local farms and boats early every morning.','Because vendors cook it every morning.'],a:2}],
   open:[{q:'What can customers ask the vendors to do with the food?',keys:['choose','weigh'],model:'They can ask the vendors to choose, weigh and even prepare the food for them.'},
         {q:'Why have some markets been moved into air-conditioned buildings?',keys:['cool'],model:'So that shoppers can stay cool in summer and dry in the rain.'}],
   fill:{q:'The smells of fresh fish, fruit and flowers {0} the air.',a:[['fill']]}},
  {title:'The Lion Rock',
   s:'Lion Rock is a hill between Kowloon and the New Territories. From far away, the hill looks like a lion sitting and watching over the city, so people gave it this name. It is 495 metres high, and thousands of hikers climb it every year.<br>From the top, you can see Kowloon on one side and Sha Tin on the other. At sunset, the city lights begin to shine, and the view is wonderful.<br>Lion Rock is also a symbol of Hong Kong. In the past, many people worked very hard here to build a better life. The never-give-up spirit of those people is often called the Lion Rock spirit.',
   mc:[{q:'Why is the hill called Lion Rock?',opts:['Because lions live there.','Because it looks like a sitting lion.','Because a lion statue stands on the top.','Because lions were born there long ago.'],a:1},
       {q:'How high is Lion Rock?',opts:['459 metres','495 metres','549 metres','594 metres'],a:1}],
   open:[{q:'What can you see from the top of Lion Rock?',keys:['kowloon'],model:'You can see Kowloon on one side and Sha Tin on the other.'},
         {q:'What is the never-give-up spirit of Hong Kong people often called?',keys:['lion rock'],model:'It is often called the Lion Rock spirit.'}],
   fill:{q:'From far away, the hill {0} like a lion sitting and watching over the city.',a:[['looks']]}},
  {title:'Saving Water in Hong Kong',
   s:'Hong Kong buys most of its water from the Dongjiang River in Guangdong, but the city also collects rainwater in its seventeen reservoirs. Together, these reservoirs cover about one quarter of Hong Kong’s land area.<br>Water is precious, and everyone should help to save it. Turn off the tap while brushing your teeth. Take shorter showers. Report dripping taps to your parents or teachers quickly, because one dripping tap can waste many litres of water in a single day.<br>The Water Supplies Department also visits schools to teach students how to use water wisely. If everybody does a little, Hong Kong will always have enough water for the future.',
   mc:[{q:'Where does most of Hong Kong’s water come from?',opts:['From the seventeen reservoirs.','From the Dongjiang River in Guangdong.','From the sea around the city.','From the rain in summer only.'],a:1},
       {q:'What can one dripping tap do in a single day?',opts:['Save many litres of water.','Waste many litres of water.','Fill a whole reservoir.','Water all the plants.'],a:1}],
   open:[{q:'Name TWO ways to save water at home.',keys:['tap'],model:'Turn off the tap while brushing your teeth, take shorter showers and report dripping taps quickly.'},
         {q:'How much land do the reservoirs cover?',keys:['quarter'],model:'They cover about one quarter of Hong Kong’s land area.'}],
   fill:{q:'Hong Kong collects rainwater in its seventeen {0} .',a:[['reservoirs']]}}
 ],
I:[
  {title:'School Picnic Day',
   s:'Our school picnic will be held on 20th March (Friday) at Tai Po Waterfront Park.<br><b>Time:</b> Meet at the school playground at 8:30 a.m. The bus leaves at 9:00 a.m.<br><b>Lunch:</b> Bring your own lunch box and a bottle of water.<br><b>Important reminders:</b> Wear your school uniform and sports shoes. Do not bring sharp objects or glass bottles. If it rains heavily, the picnic will be postponed to 27th March. Parents will receive a notice on the morning of the picnic day.',
   mc:[{q:'When is the school picnic?',opts:['20th March','27th March','8th March','9th March'],a:0},
       {q:'What time does the bus leave?',opts:['At 8:30 a.m.','At 9:00 a.m.','At 9:30 a.m.','At 8:00 a.m.'],a:1},
       {q:'What should students bring for lunch?',opts:['Money for fast food','Snacks from the tuck shop','Their own lunch box and water','Food from the school canteen'],a:2},
       {q:'What will happen if it rains heavily?',opts:['The picnic will be cancelled.','The picnic will move indoors.','The bus will leave later.','The picnic will be postponed to 27th March.'],a:3}],
   open:[{q:'Where should students meet in the morning?',keys:['playground'],model:'They should meet at the school playground at 8:30 a.m.'},
         {q:'What must students NOT bring to the picnic?',keys:['sharp','glass'],model:'They must not bring sharp objects or glass bottles.'}]},
  {title:'Second-hand Book Sale',
   s:'The Student Union is holding a second-hand book sale in the school hall on 12th May (Saturday), from 10 a.m. to 3 p.m.<br>All books cost five dollars each, and the money will buy new books for our library.<br><b>How to help:</b> Bring your old books to the Student Union room before 8th May. Volunteers are needed to sort books and set up the tables.<br><b>Important reminders:</b> Do not bring magazines or broken books. All sellers must hand in a permission slip signed by a parent before 5th May.',
   mc:[{q:'Where will the book sale be held?',opts:['In the school hall','In the library','In the Student Union room','On the playground'],a:0},
       {q:'How much does each book cost?',opts:['Three dollars','Five dollars','Eight dollars','Ten dollars'],a:1},
       {q:'Why does the Student Union hold the book sale?',opts:['To buy new books for the library.','To help students sell toys.','To raise money for a picnic.','To clean the school hall.'],a:0},
       {q:'What must sellers hand in before 5th May?',opts:['Old magazines','A signed permission slip','New books','Broken books'],a:1}],
   open:[{q:'When must students bring their old books?',keys:['8th may'],model:'They must bring their old books before 8th May.'},
         {q:'Who must sign the permission slip?',keys:['parent'],model:'A parent must sign the permission slip.'}]},
  {title:'Lost Property Notice',
   s:'A wristwatch was found on the school playground yesterday afternoon.<br><b>Item:</b> A blue digital wristwatch with a silver strap.<br><b>Where:</b> Near the basketball courts, beside the drinking fountain.<br>If this watch is yours, please come to the General Office at lunchtime (1:00 p.m. to 1:40 p.m.) and describe the time shown on it. Unclaimed items will be kept for one month and then given to charity.<br><b>Please remember:</b> Do not leave your belongings in the playground. Write your name and class on everything you bring to school.',
   mc:[{q:'Where was the watch found?',opts:['In the General Office.','Near the basketball courts.','In the school hall.','Beside the tuck shop.'],a:1},
       {q:'When can the owner go to the General Office?',opts:['From 1:00 p.m. to 1:40 p.m.','After school at 4:00 p.m.','Before the morning assembly.','Any time on Saturday.'],a:0},
       {q:'What will happen to unclaimed items after one month?',opts:['They will be sold at the tuck shop.','They will be thrown away.','They will be given to charity.','They will be kept for another year.'],a:2},
       {q:'What should students write on everything they bring to school?',opts:['Their teacher’s name.','Their name and class.','Their home address.','Their phone number.'],a:1}],
   open:[{q:'What must the owner do to prove the watch is theirs?',keys:['time'],model:'They must describe the time shown on the watch.'},
         {q:'Where should students not leave their belongings?',keys:['playground'],model:'They should not leave their belongings in the playground.'}]},
  {title:'School Reading Week',
   s:'Our school Reading Week starts on Monday, 23rd April!<br><b>Events:</b> Monday — Bookmark design competition (apply at the library). Wednesday — Storytelling by S6 students in the hall at 1:30 p.m. Friday — Dress-up Day: come as your favourite storybook character!<br><b>Prizes:</b> The class that reads the most books will win a pizza party.<br><b>Important reminders:</b> Bring your reading passport every day this week. Teachers will stamp it for every book you finish. The last day to return library books for stamping is Friday, 27th April.',
   mc:[{q:'When does the storytelling take place?',opts:['On Monday at 1:30 p.m.','On Wednesday at 1:30 p.m.','On Friday at 1:30 p.m.','On Wednesday at 3:30 p.m.'],a:1},
       {q:'What happens on Dress-up Day?',opts:['Students wear the school uniform.','Students dress as their favourite storybook character.','Students design bookmarks.','Students make pizza.'],a:1},
       {q:'What will the winning class get?',opts:['A pizza party.','A new set of storybooks.','A day off school.','A bookmark each.'],a:0},
       {q:'When is the last day for stamping?',opts:['23rd April','25th April','27th April','30th April'],a:2}],
   open:[{q:'Where can students apply for the bookmark design competition?',keys:['library'],model:'They can apply at the library.'},
         {q:'What must students bring every day during Reading Week?',keys:['passport'],model:'They must bring their reading passport every day.'}]},
  {title:'Annual Swimming Gala',
   s:'The Annual Swimming Gala will be held on 18th October (Wednesday) at Kowloon Park Swimming Pool.<br><b>Time:</b> Report to your class teacher at the pool entrance at 8:15 a.m. The first race starts at 9:00 a.m.<br><b>Events:</b> Freestyle, breaststroke and backstroke races for all grades, plus the exciting teachers’ relay at the end!<br><b>Important reminders:</b> Swimmers must bring goggles, a towel and a swim cap. Spectators should bring a water bottle and stay in the seating area. Students who feel unwell must tell the teacher on duty at once. The gala will be postponed to 20th October if the red rainstorm warning is in force.',
   mc:[{q:'When does the first race start?',opts:['At 8:15 a.m.','At 9:00 a.m.','At 9:15 a.m.','At 10:00 a.m.'],a:1},
       {q:'What must swimmers bring?',opts:['Goggles, a towel and a swim cap.','A lunch box and snacks.','A chair for the seating area.','An umbrella and a raincoat.'],a:0},
       {q:'When will the gala be postponed?',opts:['If it is too hot.','If the coach is late.','If the red rainstorm warning is in force.','If the pool is closed.'],a:2},
       {q:'What special event happens at the end?',opts:['A prize ceremony.','The teachers’ relay.','A picnic.','A swimming lesson.'],a:1}],
   open:[{q:'Where and when should students report?',keys:['entrance'],model:'They should report at the pool entrance at 8:15 a.m.'},
         {q:'What must a student do if they feel unwell?',keys:['teacher'],model:'They must tell the teacher on duty at once.'}]}
 ],
J:[
  {items:[
   {s:'{0} it was raining outside, we stayed indoors and played board games.',a:['since']},
   {s:'Ben was hungry, {0} he made a big sandwich.',a:['therefore']},
   {s:'{0} she practised every day, she won the piano competition.',a:['since']},
   {s:'The shop was closed, {0} we went home.',a:['therefore']},
   {s:'{0} Kitty forgot her umbrella, she got wet in the rain.',a:['since']},
   {s:'Tom studied hard for the test, {0} he got full marks.',a:['therefore']},
   {s:'{0} the bus was full, we waited for the next one.',a:['since']},
   {s:'Mary loves animals, {0} she visits the SPCA every month.',a:['therefore']},
   {s:'{0} it was a public holiday, there was no school.',a:['since']},
   {s:'John missed the school bus, {0} he was late for class.',a:['therefore']}]},
  {items:[
   {s:'{0} it was Mother’s Day, Kitty made a card for her mum.',a:['since']},
   {s:'The bus broke down, {0} we walked to school.',a:['therefore']},
   {s:'{0} Peter was ill, he stayed at home all day.',a:['since']},
   {s:'Amy watered the flowers every day, {0} they grew tall and strong.',a:['therefore']},
   {s:'{0} the shop was closing soon, they rushed to finish their shopping.',a:['since']},
   {s:'Tom wanted to save money, {0} he cooked dinner at home instead of eating out.',a:['therefore']},
   {s:'{0} the roads were busy, they arrived at the airport later than expected.',a:['since']},
   {s:'Jenny practised the dance every night, {0} she performed well at the show.',a:['therefore']},
   {s:'{0} there was no bread left, Mum made rice for breakfast.',a:['since']},
   {s:'The children tidied up the classroom quickly, {0} the teacher gave them stickers.',a:['therefore']}]}
 ]
},
P6:{
 heads:[
  {words:[{w:'extinct (adj.)',zh:'絕種的'},{w:'pollution (n.)',zh:'污染'},{w:'recycle (v.)',zh:'回收'},{w:'survive (v.)',zh:'生存'},{w:'habitat (n.)',zh:'棲息地'},{w:'release (v.)',zh:'排放／釋放'},{w:'wildlife (n.)',zh:'野生動物'},{w:'protect (v.)',zh:'保護'}],
   fills:[{s:'We should {0} plastic bottles instead of throwing them away.',a:['recycle']},{s:'Many animals cannot {0} when their forests are cut down.',a:['survive']},{s:'Factories must not {0} dirty water into the sea.',a:['release']},{s:'The panda’s natural {0} is disappearing because of farming.',a:['habitat']},{s:'Air {0} in big cities makes many children ill.',a:['pollution']}]},
  {words:[{w:'astronaut (n.)',zh:'太空人'},{w:'orbit (v.)',zh:'繞軌道運行'},{w:'launch (v.)',zh:'發射'},{w:'gravity (n.)',zh:'地心吸力'},{w:'explore (v.)',zh:'探索'},{w:'satellite (n.)',zh:'衛星'},{w:'float (v.)',zh:'漂浮'},{w:'universe (n.)',zh:'宇宙'}],
   fills:[{s:'China {0} its newest space station module last year.',a:['launched']},{s:'The moon {0} around the Earth about once a month.',a:['orbits']},{s:'Without gravity, astronauts {0} inside the spacecraft.',a:['float']},{s:'Scientists use giant telescopes to {0} deep space.',a:['explore']},{s:'A weather {0} takes photos of clouds from space.',a:['satellite']}]}
 ],
 A:[
  {bank1:['dry','brave','busy','free','smooth','bright'],bank2:['a desert','a lion','a bee','a bird','silk','the stars'],items:[
   {s:'After the long dry summer, the cracked ground looked as {0} as {1} .',a:['dry','a desert']},
   {s:'The knight drew his sword and faced the dragon, as {0} as {1} .',a:['brave','a lion']},
   {s:'Mum cleaned the whole house and cooked dinner; she was as {0} as {1} .',a:['busy','a bee']},
   {s:'With no homework for the whole weekend, Tom felt as {0} as {1} .',a:['free','a bird']},
   {s:'The cat’s fur was as {0} as {1} after Grandpa brushed it.',a:['smooth','silk']},
   {s:'On a clear night, the moon was as {0} as {1} .',a:['bright','the stars']}]},
  {bank1:['cold','quiet','light','sharp','playful','white'],bank2:['ice','a library','a feather','a knife','a kitten','snow'],items:[
   {s:'The water in the swimming pool felt as {0} as {1} in winter.',a:['cold','ice']},
   {s:'Please be as {0} as {1} — everyone is reading.',a:['quiet','a library']},
   {s:'Pick up the empty box; it is as {0} as {1} .',a:['light','a feather']},
   {s:'Be careful — the kitchen scissors are as {0} as {1} .',a:['sharp','a knife']},
   {s:'The new puppy was as {0} as {1} , chasing its tail all day long.',a:['playful','a kitten']},
   {s:'The whole field was as {0} as {1} after the heavy snowfall.',a:['white','snow']}]},
  {bank1:['brave','free','gentle','dark','smooth','sweet'],bank2:['a lion','a bird','a lamb','the night','silk','sugar'],items:[
   {s:'The hero faced the giant, as {0} as {1} .',a:['brave','a lion']},
   {s:'After the exams were over, Kitty felt as {0} as {1} .',a:['free','a bird']},
   {s:'The newborn kitten was as {0} as {1} , sleeping in Mum’s hands.',a:['gentle','a lamb']},
   {s:'The clouds covered the sky and the room became as {0} as {1} .',a:['dark','the night']},
   {s:'The lotion made her skin as {0} as {1} .',a:['smooth','silk']},
   {s:'The freshly baked cake tasted as {0} as {1} .',a:['sweet','sugar']}]}
 ],
 B:[
  {bank:['a piece of cake','under the weather','break the ice','hit the books','on cloud nine','a cold fish'],items:[
   {s:'The maths test was {0} for Kitty because she had practised every day.',a:['a piece of cake','piece of cake']},
   {s:'Peter felt {0} , so he stayed at home from school with a fever.',a:['under the weather']},
   {s:'To {0} at the new student’s welcome party, we played a name game first.',a:['break the ice']},
   {s:'With the final exam tomorrow, John must {0} tonight.',a:['hit the books']},
   {s:'After winning the inter-school championship, the whole team was {0} .',a:['on cloud nine']},
   {s:'Ben rarely talks and never smiles at parties, so everyone calls him {0} .',a:['a cold fish','cold fish']}]},
  {bank:['pull someone’s leg','in hot water','add fuel to the fire','the last straw','keep an eye on','make a mountain out of a molehill'],items:[
   {s:'Do not be angry about the joke — Tom was only {0} .',a:['pulling your leg','pulling my leg']},
   {s:'Sam was {0} after he broke his neighbour’s window with a football.',a:['in hot water']},
   {s:'Arguing about whose fault it was only {0} .',a:['added fuel to the fire']},
   {s:'Losing my homework on the bus was {0} — I had already been late that morning.',a:['the last straw']},
   {s:'Please {0} my plants while I am away for the holiday.',a:['keep an eye on']},
   {s:'It is only a small scratch — do not {0} !',a:['make a mountain out of a molehill']}]},
  {bank:['black sheep','give the green light','see red','have egg on one’s face','once in a blue moon','a slip of the tongue'],items:[
   {s:'In a family of doctors, Uncle Ben became an artist — he was always the {0} .',a:['black sheep']},
   {s:'The manager finally {0} for the staff outing after weeks of waiting.',a:['gave the green light','gave the green light for']},
   {s:'Dad begins to {0} whenever anyone touches his precious stamp collection.',a:['see red']},
   {s:'Peter predicted the wrong winner in front of the whole class, so he had {0} .',a:['egg on his face','egg on one’s face']},
   {s:'My uncle lives in Australia, so we see each other {0} .',a:['once in a blue moon']},
   {s:'Calling your aunt “Mummy” by mistake is a common {0} among children.',a:['slip of the tongue','a slip of the tongue']}]}
 ],
 C:[
  {s:'Hannah Wong (e.g.) is (be) a promising swimmer at her school. She (1) {0} (take) up swimming when she was only six years old. Last year, she (2) {1} (break) two school records and (3) {2} (be) named Best Athlete of the year. Since then, she (4) {3} (train) at the municipal pool every morning before school. Her coach says she (5) {4} (swim) faster than anyone he has ever seen. Next month, Hannah (6) {5} (compete) in the All-Hong Kong Youth Games. “I (7) {6} (never feel) so excited,” she said yesterday. “Winning is important, but I (8) {7} (enjoy) every race.” Unfortunately, she (9) {8} (hurt) her shoulder last week, but the doctor says she (10) {9} (be) fine by the weekend.',
   a:[['took'],['broke'],['was'],['has trained'],['swims'],['will compete'],['have never felt','’ve never felt','ve never felt'],['enjoy'],['hurt'],['will be']]},
  {s:'Uncle Lam (e.g.) runs (run) a small bakery in Sham Shui Po. Every morning he (1) {0} (get) up at four o’clock to prepare the dough. His pineapple buns (2) {1} (be) so popular that they (3) {2} (sell) out before noon every day. Ten years ago, he (4) {3} (borrow) money from his family to open the shop. Business (5) {4} (be) terrible in the first year, and he nearly (6) {5} (give) up. “My neighbours (7) {6} (support) me since day one,” he told our reporter. “Sometimes they (8) {7} (queue) for thirty minutes just for a fresh bun!” Last month, Uncle Lam (9) {8} (open) a second branch in Kowloon City. He says he (10) {9} (teach) young bakers for free in the future.',
   a:[['gets'],['are'],['sell'],['borrowed'],['was'],['gave'],['have supported'],['queue'],['opened'],['will teach']]},
  {s:'Last Saturday, our school (e.g.) held (hold) a fun fair to raise money for the SPCA. Parents and teachers (1) {0} (work) together to set up game stalls in the playground. Kitty (2) {1} (help) at the lucky draw stall, while Ben (3) {2} (sell) cookies that his mother (4) {3} (bake) the night before. By noon, hundreds of visitors (5) {4} (arrive) and the playground (6) {5} (be) full of people. In the afternoon, the school choir (7) {6} (sing) three songs on the stage. At the end of the day, the headmaster (8) {7} (announce) that we (9) {8} (raise) more than eight thousand dollars. Everyone (10) {9} (agree) that it was a wonderful day.',
   a:[['worked'],['helped'],['sold'],['had baked','baked'],['had arrived','arrived'],['was'],['sang'],['announced'],['had raised','raised'],['agreed']]},
  {s:'May (e.g.) has (have) a pen friend called Emma in Australia. The two girls (1) {0} (write) to each other every month. Emma (2) {1} (live) on a farm near Melbourne. Her family (3) {2} (keep) sheep and chickens, and her brothers (4) {3} (ride) their bikes to school every day. In her last letter, Emma (5) {4} (tell) May about the bushfires last summer. Luckily, no one on her farm (6) {5} (be) hurt. “Australian animals (7) {6} (need) our help after the fires,” Emma wrote. May (8) {7} (reply) at once and (9) {8} (send) her a drawing of a koala. The two girls (10) {9} (hope) to meet each other one day.',
   a:[['write'],['lives'],['keep'],['ride'],['told'],['was'],['need'],['replied'],['sent'],['hope']]},
  {s:'Next Friday, our class (e.g.) will go (go) on a field trip to the Sai Kung geopark. A guide (1) {0} (show) us the famous hexagonal rock columns, which (2) {1} (form) more than 100 million years ago. We (3) {2} (travel) there by bus and (4) {3} (walk) along the coastal trail. Everyone (5) {4} (bring) a hat and plenty of water because the trail (6) {5} (have) little shade. During the trip, we (7) {6} (complete) a worksheet about rocks and landforms. Miss Ho (8) {7} (remind) us that we (9) {8} (must not) pick up or take away any rocks. I think the trip (10) {9} (be) both fun and educational.',
   a:[['will show'],['formed'],['will travel','travel'],['will walk','walk'],['will bring','brings'],['has'],['will complete','complete'],['will remind','reminds'],['must not'],['will be']]}
 ],
 D:[
  {bank:['chef','pilot','dentist','journalist','firefighter'],lines:[
   {who:'Polly',s:'I love aeroplanes and I want to fly to cities all over the world. I want to be a (1) {0} .',a:['pilot']},
   {who:'Kelly',s:'I am good at writing and I enjoy finding out the truth for other people. I want to be a (2) {0} .',a:['journalist']},
   {who:'Amy',s:'Saving people from burning buildings looks dangerous but brave. I want to be a (3) {0} .',a:['firefighter']},
   {who:'Samuel',s:'I spend every weekend trying new recipes for my family. I want to be a (4) {0} .',a:['chef']},
   {who:'Nathan',s:'I do not like sweets, but I care a lot about healthy teeth. I want to be a (5) {0} .',a:['dentist']}]},
  {bank:['vet','architect','engineer','dancer','tour guide'],lines:[
   {who:'Polly',s:'I love animals and I want to take care of sick pets. I want to be a (1) {0} .',a:['vet']},
   {who:'Kelly',s:'I enjoy drawing buildings and designing dream houses. I want to be an (2) {0} .',a:['architect']},
   {who:'Amy',s:'I am interested in bridges and machines, and I am good at maths. I want to be an (3) {0} .',a:['engineer']},
   {who:'Samuel',s:'I have danced ballet since I was four years old. I want to be a (4) {0} .',a:['dancer']},
   {who:'Nathan',s:'I love history and I enjoy showing visitors around old temples. I want to be a (5) {0} .',a:['tour guide']}]},
  {bank:['scriptwriter','film director','costume designer','set designer','stuntman'],lines:[
   {who:'Polly',s:'I love telling stories and I am writing a movie script for our class. I want to be a (1) {0} .',a:['scriptwriter']},
   {who:'Kelly',s:'I enjoy telling the actors what to do in different scenes. I want to be a (2) {0} .',a:['film director']},
   {who:'Amy',s:'I make all the clothes that the actors and actresses wear in the film. I want to be a (3) {0} .',a:['costume designer']},
   {who:'Samuel',s:'I prepare the scenery and backgrounds for films. I want to be a (4) {0} .',a:['set designer']},
   {who:'Nathan',s:'I do the dangerous parts in films for the main actors. I want to be a (5) {0} .',a:['stuntman']}]}
 ],
 E:[
  {bank:['many birds fly to warmer places','we should drink more water','the match will be cancelled','the roads are very slippery'],items:[
   {lead:'Since the temperature drops quickly in autumn,',a:['many birds fly to warmer places']},
   {lead:'Since it is very hot in summer,',a:['we should drink more water']},
   {lead:'Since a black rainstorm warning is in force,',a:['the match will be cancelled']},
   {lead:'Since ice covers the streets after the storm,',a:['the roads are very slippery']}]},
  {bank:['people should stay indoors','crops cannot grow','the air is fresher','there may be bacteria'],items:[
   {lead:'Since there is a serious drought in the fields,',a:['crops cannot grow']},
   {lead:'Since the air pollution index is very high today,',a:['people should stay indoors']},
   {lead:'Since tall trees give out oxygen in the park nearby,',a:['the air is fresher']},
   {lead:'Since the water in the tank is dirty and full of germs,',a:['there may be bacteria']}]}
 ],
 F:[
  {bank:['set off','get on','put up','come across','look after','put out','give up'],s:'Ken and his classmates went camping last Friday. They (e.g.) set off at nine in the morning and (1) {0} the minibus at Sai Kung. At the campsite, they (2) {1} the tents and cooked lunch together. While exploring, Ken (3) {2} a wounded bird, so the teacher told them to (4) {3} it carefully until a vet arrived. When a small fire started at the next site, the wardens quickly (5) {4} it with sand and water.',a:[['got on'],['put up'],['came across'],['look after'],['put out']]},
  {bank:['put on','turn on','look for','run out of','pick up','take off'],s:'It was the night before the school concert. Amy laid out her costume on the bed, ready to (e.g.) put on in the morning. Suddenly the lights went out! She used her phone to (1) {0} the torch and (2) {1} her missing shoe under the bed. She began to (3) {2} time, so her brother helped her (4) {3} everything and pack the bag quickly. Only when she reached school in the rain did she (5) {4} her wet raincoat.',a:[['turn on'],['looked for','look for'],['run out of'],['pick up'],['take off']]}
 ],
 G:[
  {bank:['very few','very little','enough','either…or','neither…nor'],lines:[
   {who:'Mum',s:'Ruby, you can have (1) {0} fried noodles (2) {1} dumplings for dinner tonight.'},
   {who:'Ruby',s:'But there is (3) {2} fried noodles (4) {3} dumplings left in the fridge, Mum.'},
   {who:'Mum',s:'Hurry then! There are only (5) {4} eggs and (6) {5} rice, so I will make soup too.'}],
   a:[['either'],['or'],['neither'],['nor'],['very few'],['very little']]},
  {bank:['both…and','either…or','very few','very little','enough'],lines:[
   {who:'Librarian',s:'You can borrow (1) {0} this storybook (2) {1} that comic, but not both.'},
   {who:'Ben',s:'Great! Can I (3) {2} borrow books (4) {3} read magazines here?'},
   {who:'Librarian',s:'Sure. But there are only (5) {4} seats left at noon, and there is (6) {5} space in the reading corner.'}],
   a:[['either'],['or'],['both'],['and'],['very few'],['very little']]}
 ],
 H:[
  {title:'Bees at Risk',
   s:'Honeybees are small but very important insects. They carry pollen from flower to flower as they search for food. Without bees, many plants cannot produce fruit or seeds, so farmers would not be able to grow much of our food.<br>In recent years, beekeepers around the world have reported that large numbers of bees are disappearing. Scientists believe there are several reasons. Some pesticides used on farms are poisonous to bees. In addition, as cities grow bigger, the fields and wildflowers that bees need are disappearing.<br>You can help the bees in simple ways. Plant flowers on your balcony, put out a small dish of water with pebbles for tired bees to rest on, and never spray pesticides in your garden.',
   mc:[{q:'Why are honeybees so important?',opts:['They make sweet honey for people.','They carry pollen so plants can produce fruit and seeds.','They eat harmful insects on farms.','They produce pesticides for farmers.'],a:1},
       {q:'Which of the following is NOT a reason why bees are disappearing?',opts:['Poisonous pesticides on farms.','Cities are growing bigger.','There are fewer wildflowers.','Beekeepers are selling honey.'],a:3}],
   open:[{q:'Why should we put out a small dish of water with pebbles?',keys:['tired bees','rest'],model:'So that tired bees can rest on the pebbles.'},
         {q:'According to scientists, name TWO reasons why bees are disappearing.',keys:['pesticide','cities'],model:'Because some pesticides are poisonous to bees and cities are growing bigger.'}],
   fill:{q:'Honeybees carry {0} from flower to flower as they search for food.',a:[['pollen']]}},
  {title:'A Bridge Across the Sea',
   s:'The Hong Kong-Zhuhai-Macao Bridge is the longest sea crossing in the world. It stretches for about 55 kilometres and connects the three cities across the Pearl River Delta. The bridge opened to traffic in October 2018 after nine years of construction.<br>Before the bridge was built, travellers had to take a long detour around the delta or cross by ferry. Now a journey between Hong Kong and Zhuhai takes only about 45 minutes by bus.<br>The bridge was designed to last for 120 years. Engineers had to consider strong typhoons and even the impact of ships, so the crossing includes special tunnels and artificial islands.',
   mc:[{q:'How long is the Hong Kong-Zhuhai-Macao Bridge?',opts:['About 45 kilometres','About 55 kilometres','About 120 kilometres','About 9 kilometres'],a:1},
       {q:'How long did the construction of the bridge take?',opts:['About 45 years','About 55 years','About 9 years','About 120 years'],a:2}],
   open:[{q:'How did travellers cross the delta before the bridge was built?',keys:['detour','ferry'],model:'They had to take a long detour around the delta or cross by ferry.'},
         {q:'Why did engineers include tunnels and artificial islands?',keys:['typhoon','ships'],model:'Because engineers had to consider strong typhoons and the impact of ships.'}],
   fill:{q:'A journey between Hong Kong and Zhuhai now takes only about {0} minutes by bus.',a:[['45']]}},
  {title:'Wild Neighbours: The Monkeys of Kam Shan',
   s:'Kam Shan Country Park, also known as Monkey Hill, is home to more than a thousand wild monkeys. Most of them are rhesus macaques. They were introduced to Hong Kong about a hundred years ago to help control snakes around the old reservoirs.<br>The monkeys eat leaves, fruit and insects. However, many visitors feed them snacks, and this has changed their behaviour. The monkeys now gather near the car parks and sometimes snatch plastic bags from visitors because they think there is food inside.<br>Feeding wild monkeys is against the law, and offenders can be fined. If you meet a monkey, do not stare at it or show your teeth. Keep your food inside your bag and simply walk past calmly.',
   mc:[{q:'Why were the monkeys introduced to Hong Kong?',opts:['To attract tourists to the park.','To help control snakes around the reservoirs.','To eat the leaves in the forests.','To carry things for the workers.'],a:1},
       {q:'Why do the monkeys snatch plastic bags from visitors?',opts:['They like the colour of the bags.','They collect bags for their nests.','They think there is food inside.','They want to play with visitors.'],a:2}],
   open:[{q:'What do the wild monkeys eat?',keys:['leaves'],model:'They eat leaves, fruit and insects.'},
         {q:'What must you NOT do when you meet a monkey?',keys:['stare'],model:'Do not stare at it or show your teeth.'}],
   fill:{q:'Feeding wild monkeys is against the law, and offenders can be {0} .',a:[['fined']]}},
  {title:'The MTR: From One Line to a Network',
   s:'The MTR began operating in 1979 with just one short line in Kowloon. Today, it is one of the most reliable railways in the world, carrying about five million passengers every weekday.<br>The first line ran from Shek Kip Mei to Kwun Tong. Over the years, new lines crossed the harbour, reached the New Territories and even Tung Chung on Lantau Island. The Airport Express opened in 1998 to serve the new airport.<br>The MTR is famous for being clean, fast and punctual. Trains usually arrive every few minutes, and air-conditioning keeps passengers comfortable even in summer. Many people say the MTR is the easiest way for visitors to travel around Hong Kong.',
   mc:[{q:'When did the MTR begin operating?',opts:['In 1979','In 1998','In 1989','In 2007'],a:0},
       {q:'What is the MTR famous for?',opts:['Being slow but cheap.','Being clean, fast and punctual.','Being the oldest railway in Asia.','Having no air-conditioning.'],a:1}],
   open:[{q:'Where did the first MTR line run?',keys:['shek kip mei'],model:'It ran from Shek Kip Mei to Kwun Tong.'},
         {q:'Why do passengers feel comfortable even in summer?',keys:['air-condition'],model:'Because air-conditioning keeps passengers comfortable.'}],
   fill:{q:'The MTR carries about five million passengers every {0} .',a:[['weekday']]}},
  {title:'Food Waste in Hong Kong',
   s:'Every day, Hong Kong people throw away more than three thousand tonnes of food. That is like dumping 250 double-decker buses full of food into our landfills every single day. Most of this food is still edible when it is thrown away.<br>Food waste rotting in landfills produces methane, a greenhouse gas that is even more powerful than carbon dioxide. Our three landfills will be full in the coming years, so this problem cannot wait.<br>Everyone can help. Restaurants and hotels can join food donation programmes and send surplus food to food banks instead of the bin. At home, plan your meals, finish everything on your plate, and use leftover rice and vegetables to make fried rice the next day.',
   mc:[{q:'How much food do Hong Kong people throw away every day?',opts:['More than three thousand tonnes.','About three hundred tonnes.','About 250 tonnes.','More than ten thousand tonnes.'],a:0},
       {q:'What is methane?',opts:['A kind of food waste.','A new landfill in Hong Kong.','A greenhouse gas more powerful than carbon dioxide.','A programme that saves food.'],a:2}],
   open:[{q:'Where can restaurants send surplus food?',keys:['food bank'],model:'They can send it to food banks through food donation programmes.'},
         {q:'Name TWO things your family can do to reduce food waste at home.',keys:['plate'],model:'Plan meals, finish everything on the plate, and use leftovers to make fried rice.'}],
   fill:{q:'Food waste rotting in landfills produces {0} , a greenhouse gas.',a:[['methane']]}}
 ],
I:[
  {title:'School Charity Fair',
   s:'Many people in the mountain village are suffering because of a flood. The people need your help!<br><b>The situation:</b> Many houses are under water. The villagers have lost their homes and their farms. There is not enough clean water, and some children cannot go to school.<br><b>How to help:</b> A charity fair will be held on 12th November (Sunday) in the school playground. S1 and S2 students can make bookmarks to sell. S3 and S4 students can collect old books and toys. S5 and S6 students can run a food stall.<br><b>Important reminders:</b> Join us and collect a permission slip from Miss Chau. Return the completed slip with your parent’s signature to Miss Chau. We need to collect all the books, toys and crafts before 9th November (Thursday).',
   mc:[{q:'Why do the villagers need help?',opts:['There was a fire in the village.','A flood has destroyed their homes.','There has been no rain for 40 days.','An earthquake hit the village.'],a:1},
       {q:'When will the charity fair be held?',opts:['9th November','12th November','11th November','20th November'],a:1},
       {q:'What can S5 and S6 students do?',opts:['Make bookmarks.','Collect old books.','Run a food stall.','Collect permission slips.'],a:2},
       {q:'When must all the books, toys and crafts be collected?',opts:['Before 9th November.','Before 12th November.','Before 11th November.','Before 5th November.'],a:0}],
   open:[{q:'What do pupils need to give Miss Chau if they want to join the fair?',keys:['permission slip','signature'],model:'They need to give her the completed permission slip with their parent’s signature.'},
         {q:'Where will the charity fair be held?',keys:['playground'],model:'It will be held in the school playground.'}]},
  {title:'Beach Clean-up Day',
   s:'Our school is organising a beach clean-up on 3rd October (Saturday) at Clear Water Bay Beach.<br><b>The problem:</b> Last month, volunteers found more than two hundred plastic bags and bottles on the beach. The rubbish is dangerous to sea turtles and fish.<br><b>What to do:</b> We will meet at the school gate at 8:45 a.m. and travel by coach. Gloves, tongs and rubbish bags will be provided. The clean-up ends at noon, and there will be a picnic afterwards.<br><b>Important reminders:</b> Wear a cap and sports shoes. Bring your own water bottle. Return the permission slip with your parent’s signature to Mr Lee before 30th September. The event will be cancelled if a typhoon signal No. 3 or above is hoisted.',
   mc:[{q:'What did volunteers find on the beach last month?',opts:['Sea turtles and fish.','A typhoon signal.','More than 200 plastic bags and bottles.','New picnic tables.'],a:2},
       {q:'How will students travel to the beach?',opts:['By MTR','By minibus','By ferry','By coach'],a:3},
       {q:'What will students do after the clean-up?',opts:['Have a picnic.','Go swimming.','Watch a film.','Visit a museum.'],a:0},
       {q:'When will the event be cancelled?',opts:['If it is too hot.','If a typhoon signal No. 3 or above is hoisted.','If students forget their gloves.','If the coach is late.'],a:1}],
   open:[{q:'Where and when should students meet?',keys:['school gate','8:45'],model:'They should meet at the school gate at 8:45 a.m.'},
         {q:'Who must sign the permission slip?',keys:['parent'],model:'The student’s parent must sign the permission slip.'}]},
  {title:'Annual Sports Day',
   s:'The Annual Sports Day will be held on 24th November (Friday) at the Sha Tin Sports Ground.<br><b>Time:</b> Assemble at the sports ground at 8:00 a.m. Buses will leave the school gate at 7:40 a.m. for those who need transport.<br><b>Events:</b> 100 m, 200 m and 800 m races, high jump, long jump, and the 4×100 m inter-class relay.<br><b>Important reminders:</b> Bring your student card, water and sunblock. Spectators must stay in the stands. Only athletes may enter the track area. Lunch will NOT be provided, so bring your own lunch box. If tropical cyclone signal No. 1 or above is hoisted, Sports Day will be cancelled and a notice will be posted on the school website.',
   mc:[{q:'When do the buses leave the school gate?',opts:['At 7:40 a.m.','At 8:00 a.m.','At 7:00 a.m.','At 8:40 a.m.'],a:0},
       {q:'Who may enter the track area?',opts:['All students.','Spectators in the stands.','Only athletes.','Parents and teachers.'],a:2},
       {q:'What about lunch?',opts:['The school provides lunch boxes.','Lunch is sold at the sports ground.','Students must bring their own lunch box.','There is no lunch break.'],a:2},
       {q:'When will Sports Day be cancelled?',opts:['If it rains lightly.','If tropical cyclone signal No. 1 or above is hoisted.','If the buses are late.','If the track is wet.'],a:1}],
   open:[{q:'Where and when should students assemble?',keys:['sports ground'],model:'They should assemble at the Sha Tin Sports Ground at 8:00 a.m.'},
         {q:'Where will the cancellation notice be posted?',keys:['website'],model:'It will be posted on the school website.'}]},
  {title:'Visit to the Elderly Home',
   s:'The Community Youth Club is organising a visit to Wong Tai Sin Care Home for the Elderly on 6th December (Saturday).<br><b>Programme:</b> We will sing songs, perform a short play and play board games with the elderly. We will also give them handmade cards and fruit gift bags.<br><b>Meeting point:</b> School playground at 9:15 a.m. We will return to school at about 1:00 p.m.<br><b>How to prepare:</b> Volunteers must attend one rehearsal in the hall after school on 3rd December. Please bring one piece of fruit for the gift bags by 4th December.<br><b>Important reminders:</b> Speak loudly and slowly to the elderly, and be patient when they talk about their stories. Wear your school uniform with the CYC badge.',
   mc:[{q:'What will the volunteers give to the elderly?',opts:['Toys and storybooks.','Handmade cards and fruit gift bags.','Cakes and biscuits.','Board games to keep.'],a:1},
       {q:'When is the rehearsal?',opts:['On 6th December in the playground.','After school on 3rd December in the hall.','On 4th December at 9:15 a.m.','On the morning of the visit.'],a:1},
       {q:'What time will the group return to school?',opts:['At about 11:00 a.m.','At about 12:00 noon.','At about 1:00 p.m.','At about 3:00 p.m.'],a:2},
       {q:'By when must volunteers bring a piece of fruit?',opts:['3rd December','4th December','5th December','6th December'],a:1}],
   open:[{q:'What must volunteers bring by 4th December?',keys:['fruit'],model:'They must bring one piece of fruit for the gift bags.'},
         {q:'How should we speak to the elderly?',keys:['loudly'],model:'We should speak loudly and slowly, and be patient when they tell their stories.'}]},
  {title:'Science Week Exhibition',
   s:'The Science Society presents Science Week from 14th to 18th January in the school hall.<br><b>Exhibition highlights:</b> Student projects on renewable energy, a model of the International Space Station, and live experiments every lunchtime at 1:15 p.m.<br><b>Guest talk:</b> Dr Chan from HKUST will give a talk on robots in our daily life on 17th January (Wednesday) at 3:30 p.m. in the lecture theatre. S5 and S6 students may sign up at the Science Society notice board before 15th January.<br><b>Important reminders:</b> Please do not touch the exhibits unless a helper says it is allowed. Photography without flash is welcome. The hall will close at 5:00 p.m. every day during Science Week.',
   mc:[{q:'When are the live experiments held?',opts:['Every morning at 8:15 a.m.','Every lunchtime at 1:15 p.m.','Every day at 3:30 p.m.','On 17th January only.'],a:1},
       {q:'What is Dr Chan’s talk about?',opts:['Renewable energy.','The International Space Station.','Robots in our daily life.','Space travel.'],a:2},
       {q:'When is the deadline to sign up for the talk?',opts:['14th January','15th January','17th January','18th January'],a:1},
       {q:'What time does the hall close during Science Week?',opts:['At 3:30 p.m.','At 4:30 p.m.','At 5:00 p.m.','At 6:00 p.m.'],a:2}],
   open:[{q:'Where can S5 and S6 students sign up for the talk?',keys:['notice board'],model:'At the Science Society notice board.'},
         {q:'What kind of photography is welcome?',keys:['flash'],model:'Photography without flash is welcome.'}]}
 ],
J:[
  {items:[
   {s:'{0} it was Kitty’s birthday, her friends prepared a surprise party for her.',a:['since']},
   {s:'Peter forgot to bring his wallet, {0} he could not buy any lunch.',a:['therefore']},
   {s:'{0} the MTR was under maintenance, we took the bus instead.',a:['since']},
   {s:'Hannah trains very hard every day, {0} she is one of the best swimmers in her school.',a:['therefore']},
   {s:'{0} Uncle Lam gets up at four o’clock every morning, he is always sleepy after dinner.',a:['since']},
   {s:'The bakery sells out its pineapple buns before noon, {0} you should get there early.',a:['therefore']},
   {s:'{0} the weather forecast says it will rain, we had better bring umbrellas.',a:['since']},
   {s:'Sam did not revise for the test, {0} he failed it.',a:['therefore']},
   {s:'{0} Amy had waited for over an hour, she decided to go home.',a:['since']},
   {s:'The little boy was lost in the mall, {0} he asked a shopkeeper for help.',a:['therefore']}]},
  {items:[
   {s:'{0} too many people were queueing at the counter, we ordered online instead.',a:['since']},
   {s:'Kitty ate too much junk food, {0} she felt sick on the bus.',a:['therefore']},
   {s:'{0} the library was full, we studied in the classroom.',a:['since']},
   {s:'John has practised the violin for six years, {0} he can play very difficult pieces.',a:['therefore']},
   {s:'{0} the road was flooded, the coach could not cross the bridge.',a:['since']},
   {s:'Grandpa does morning exercise every day, {0} he is very healthy at seventy.',a:['therefore']},
   {s:'{0} it was a black rainstorm warning, the match was cancelled.',a:['since']},
   {s:'May left her homework at home, {0} she had to ask her brother to send her a photo of it.',a:['therefore']},
   {s:'{0} the bees are disappearing, we should plant more flowers in our garden.',a:['since']},
   {s:'The bridge opened nine years after construction started, {0} people call it a miracle of engineering.',a:['therefore']}]}
 ]
}};

// ---- v1.24 呈分試卷引擎（渲染 / 批改 / 打印） ----
function exPick(a){return a[Math.floor(Math.random()*a.length)];}
function exInp(id){return '<input class="ex-inp" id="'+id+'" autocomplete="off" spellcheck="false">';}
function exTxt(s,pre){return s.replace(/\{(\d+)\}/g,function(m,n){return exInp(pre+'_'+n);});}
function exNorm(s){return (s||'').toLowerCase().replace(/[’']/g,'’').replace(/[，、。！？,.!?:;；()（）"'’]/g,'').replace(/\s+/g,' ').trim();}
function exBankTable(rows){return '<table class="ex-bank">'+rows.map(r=>'<tr>'+r.map(c=>'<td>'+c+'</td>').join('')+'</tr>').join('')+'</table>';}
function genExamPaper(){
  const B=EXAM_QBANK[curExamGrade];
  curTenNo=0;
  curExamPaper={head:exPick(B.heads),A:exPick(B.A),B:exPick(B.B),C:exPick(B.C),D:exPick(B.D),E:exPick(B.E),F:exPick(B.F),G:exPick(B.G),H:exPick(B.H),I:exPick(B.I),J:exPick(B.J)};
  renderExamPaper(); showExamStat();
}
function exSecHtml(id,title,body){return '<div class="ex-sec" id="exSec'+id+'"><p class="ex-q"><b>'+title+'</b></p>'+body+'</div>';}
function renderExamPaper(){
  const p=curExamPaper;
  let h='<div class="ex-head"><span class="ex-code">'+curExamGrade+' ENGLISH · 呈分試模擬卷'+(curTenNo?' · 第 '+curTenNo+' 套':'')+(p.src==='ai'?' · 🤖 AI 生成（請家長把關）':'')+'</span><span class="ex-nd">NAME: ____________　DATE: ____________</span></div>';
  h+='<p class="ex-lead"><b>LEARN and MASTER new words.</b></p><table class="ex-vocab">';
  for(let r=0;r<2;r++){h+='<tr>';for(let c=0;c<4;c++){const w=p.head.words[r*4+c];h+='<td><b>'+w.w+'</b><br><span class="ex-zh">'+w.zh+'</span></td>';}h+='</tr>';}
  h+='</table>';
  h+='<div class="ex-sec" id="exSecWU"><p class="ex-q"><b>Fill in the blanks with the correct form of the words.</b> <span class="ex-warm">（Warm-up · 不計分）</span></p>';
  p.head.fills.forEach((f,i)=>{h+='<p class="ex-it">('+(i+1)+') '+exTxt(f.s,'ex_wu_'+i)+'</p>';});
  h+='</div>';
  let ba=exBankTable([p.A.bank1,p.A.bank2])+'<ol class="ex-ol">';
  p.A.items.forEach((it,i)=>{ba+='<li>'+exTxt(it.s,'ex_A_'+i)+'</li>';});ba+='</ol>';
  h+=exSecHtml('A','(A) Fill in the blanks with the correct similes. (12%@2%)',ba);
  let bb=exBankTable([p.B.bank])+'<ol class="ex-ol">';
  p.B.items.forEach((it,i)=>{bb+='<li>'+exTxt(it.s,'ex_B_'+i)+'</li>';});bb+='</ol>';
  h+=exSecHtml('B','(B) Fill in the blanks with the correct idioms. You may need to change the verb form. (12%@2%)',bb);
  h+=exSecHtml('C','(C) Complete the passage with the correct form of the verbs in brackets. (10%@1%)','<p class="ex-pass">'+exTxt(p.C.s,'ex_C')+'</p>');
  let bd=exBankTable([p.D.bank]);
  p.D.lines.forEach((l,i)=>{bd+='<p class="ex-it"><b>'+l.who+'</b>：'+exTxt(l.s,'ex_D_'+i)+'</p>';});
  h+=exSecHtml('D','(D) Finish the conversation with the correct names of the jobs. (10%@2%)',bd);
  let be=exBankTable([p.E.bank]);
  p.E.items.forEach((it,i)=>{be+='<p class="ex-it">'+it.lead+' '+exInp('ex_E_'+i)+' .</p>';});
  h+=exSecHtml('E','(E) Finish the sentences with the correct expressions from the table. (12%@3%)',be);
  h+=exSecHtml('F','(F) Complete the passage with the correct phrasal verbs. You may need to change the verb form. (10%@2%)',exBankTable([p.F.bank])+'<p class="ex-pass">'+exTxt(p.F.s,'ex_F')+'</p>');
  let bg=exBankTable([p.G.bank]);let gi=0;
  p.G.lines.forEach(l=>{bg+='<p class="ex-it"><b>'+l.who+'</b>：'+l.s.replace(/\{(\d+)\}/g,function(){return exInp('ex_G_'+(gi++));})+'</p>';});
  h+=exSecHtml('G','(G) Complete the conversation with the words given. You may use each word ONCE. (6%@1%)',bg);
  let bh='<div class="ex-pass"><b>'+p.H.title+'</b><br>'+p.H.s+'</div>';
  p.H.mc.forEach((m,i)=>{bh+='<p class="ex-it">('+(i+1)+') '+m.q+'</p><div class="ex-mc">';
    m.opts.forEach((o,j)=>{bh+='<label class="ex-opt"><input type="radio" name="ex_H_mc'+i+'" value="'+j+'"> '+o+'</label>';});
    bh+='</div>';});
  p.H.open.forEach((o,i)=>{bh+='<p class="ex-it">('+(i+3)+') '+o.q+'</p><textarea class="ex-open" id="ex_H_open'+i+'" rows="2"></textarea>';});
  bh+='<p class="ex-it">(5) '+exTxt(p.H.fill.q,'ex_H_fill')+'</p>';
  h+=exSecHtml('H','(H) Read the article and answer the questions. (10%：MC 2%×2，其餘 2%)',bh);
  let bi='<div class="ex-pass"><b>'+p.I.title+'</b><br>'+p.I.s+'</div>';
  p.I.mc.forEach((m,i)=>{bi+='<p class="ex-it">('+(i+1)+') '+m.q+'</p><div class="ex-mc">';
    m.opts.forEach((o,j)=>{bi+='<label class="ex-opt"><input type="radio" name="ex_I_mc'+i+'" value="'+j+'"> '+o+'</label>';});
    bi+='</div>';});
  p.I.open.forEach((o,i)=>{bi+='<p class="ex-it">('+(i+5)+') '+o.q+'</p><textarea class="ex-open" id="ex_I_open'+i+'" rows="2"></textarea>';});
  h+=exSecHtml('I','(I) Read the poster and answer the questions. (8%：MC 1%×4，回答 2%×2)',bi);
  let bj='<ol class="ex-ol">';
  p.J.items.forEach((it,i)=>{bj+='<li>'+exTxt(it.s,'ex_J_'+i)+'</li>';});bj+='</ol>';
  h+=exSecHtml('J',"(J) Fill in the blanks with the word 'since' or 'therefore'. You may use each word more than once. (10%@1%)",bj);
  document.getElementById('examPaperBox').innerHTML=h;
  document.getElementById('examPaperResult').innerHTML='';
}
function gradeExamPaper(noSave){
  if(!curExamPaper){genExamPaper();return;}
  let got=0,total=0,wrongs=[];
  function markFill(id,accs,w,label){
    total+=w;
    const el=document.getElementById(id);const v=el?el.value:'';
    const okv=accs.some(a=>exNorm(v)===exNorm(a));
    if(okv)got+=w;else wrongs.push({label:label,ans:accs[0]});
    if(el){el.classList.add(okv?'ex-ok':'ex-bad');el.disabled=true;}
  }
  for(let i=0;i<5;i++){const el=document.getElementById('ex_wu_'+i+'_0');if(el)el.disabled=true;}
  curExamPaper.A.items.forEach((it,i)=>{
    total+=2;
    const e0=document.getElementById('ex_A_'+i+'_0'),e1=document.getElementById('ex_A_'+i+'_1');
    const okv=exNorm(e0?e0.value:'')===exNorm(it.a[0])&&exNorm(e1?e1.value:'')===exNorm(it.a[1]);
    if(okv)got+=2;else wrongs.push({label:'A('+(i+1)+')',ans:it.a[0]+' / '+it.a[1]});
    [e0,e1].forEach(function(el){if(el){el.disabled=true;el.classList.add(okv?'ex-ok':'ex-bad');}});
  });
  curExamPaper.B.items.forEach((it,i)=>{markFill('ex_B_'+i+'_0',it.a,2,'B('+(i+1)+')');});
  curExamPaper.C.a.forEach((accs,i)=>{markFill('ex_C_'+i,accs,1,'C('+(i+1)+')');});
  curExamPaper.D.lines.forEach((l,i)=>{markFill('ex_D_'+i+'_0',l.a,2,'D('+(i+1)+')');});
  curExamPaper.E.items.forEach((it,i)=>{markFill('ex_E_'+i,Array.isArray(it.a)?it.a:[it.a],3,'E('+(i+1)+')');});
  curExamPaper.F.a.forEach((accs,i)=>{markFill('ex_F_'+i,accs,2,'F('+(i+1)+')');});
  curExamPaper.G.a.forEach((accs,i)=>{markFill('ex_G_'+i,accs,1,'G('+(i+1)+')');});
  curExamPaper.H.mc.forEach((m,i)=>{
    total+=2;
    const sel=document.querySelector('input[name="ex_H_mc'+i+'"]:checked');
    const okv=!!sel&&parseInt(sel.value,10)===m.a;
    if(okv)got+=2;else wrongs.push({label:'H 選擇('+(i+1)+')',ans:m.opts[m.a]});
  });
  curExamPaper.H.open.forEach((o,i)=>{
    total+=2;
    const el=document.getElementById('ex_H_open'+i);const v=el?el.value.toLowerCase():'';
    const okv=o.keys.every(k=>v.indexOf(k.toLowerCase())>-1);
    if(okv)got+=2;else wrongs.push({label:'H 回答('+(i+3)+')',ans:o.model,model:true});
    if(el){el.disabled=true;el.classList.add(okv?'ex-ok':'ex-bad');}
  });
  {const accs=curExamPaper.H.fill.a.flat();const el=document.getElementById('ex_H_fill_0');const v=el?el.value:'';
   const okv=accs.some(a=>exNorm(v)===exNorm(a));
   total+=2;if(okv)got+=2;else wrongs.push({label:'H (5)',ans:accs[0]});
   if(el){el.disabled=true;el.classList.add(okv?'ex-ok':'ex-bad');}}
  curExamPaper.I.mc.forEach((m,i)=>{
    total+=1;
    const sel=document.querySelector('input[name="ex_I_mc'+i+'"]:checked');
    const okv=!!sel&&parseInt(sel.value,10)===m.a;
    if(okv)got+=1;else wrongs.push({label:'I 選擇('+(i+1)+')',ans:m.opts[m.a]});
  });
  curExamPaper.I.open.forEach((o,i)=>{
    total+=2;
    const el=document.getElementById('ex_I_open'+i);const v=el?el.value.toLowerCase():'';
    const okv=o.keys.every(k=>v.indexOf(k.toLowerCase())>-1);
    if(okv)got+=2;else wrongs.push({label:'I 回答('+(i+5)+')',ans:o.model,model:true});
    if(el){el.disabled=true;el.classList.add(okv?'ex-ok':'ex-bad');}
  });
  curExamPaper.J.items.forEach((it,i)=>{markFill('ex_J_'+i+'_0',Array.isArray(it.a)?it.a:[it.a],1,'J('+(i+1)+')');});
  const key='hkk_exampaper_v0';let rec={};
  if(!noSave){
   try{rec=JSON.parse(localStorage.getItem(key)||'{}');}catch(e){}
   if(!rec[curExamGrade]||got>rec[curExamGrade]){rec[curExamGrade]=got;localStorage.setItem(key,JSON.stringify(rec));}
  }
  let rh='<div class="ex-result"><b>SCORE: '+got+' / '+total+'</b>';
  if(wrongs.length){rh+='<ol class="ex-wrongs">'+wrongs.map(w=>'<li>'+w.label+' → '+w.ans+'</li>').join('')+'</ol>';}
  else rh+='<p>全對！繼續保持！</p>';
  rh+='<p class="ex-tip">開放題按要點批改（意思對即可）；再練一套按「🎲 出新卷」。</p></div>';
  document.getElementById('examPaperResult').innerHTML=rh;
  showExamStat();
}
function showExamStat(){
  let rec={};try{rec=JSON.parse(localStorage.getItem('hkk_exampaper_v0')||'{}');}catch(e){}
  const b=rec[curExamGrade];
  const el=document.getElementById('examStat');if(el)el.textContent='本級最佳：'+(b!=null?(b+' / 100'):'—');
}
function examPrintHtml(p,ans,examNo){
  const blanks=function(s){return s.replace(/\{(\d+)\}/g,'__________');};
  let h='<div class="ex-head"><span class="ex-code">'+curExamGrade+' ENGLISH · 呈分試模擬卷'+(examNo?(' · 第 '+examNo+' 套'):'')+(p.src==='ai'?' · 🤖 AI 生成（請家長把關）':'')+'</span><span class="ex-nd">NAME: ____________　DATE: ____________</span></div>';
  h+='<p class="ex-lead"><b>LEARN and MASTER new words.</b></p><table class="ex-vocab">';
  for(let r=0;r<2;r++){h+='<tr>';for(let c=0;c<4;c++){const w=p.head.words[r*4+c];h+='<td><b>'+w.w+'</b><br><span class="ex-zh">'+w.zh+'</span></td>';}h+='</tr>';}
  h+='</table>';
  h+='<div class="ex-sec"><p class="ex-q"><b>Fill in the blanks with the correct form of the words.</b></p>';
  p.head.fills.forEach((f,i)=>{h+='<p class="ex-it">('+(i+1)+') '+blanks(f.s)+'</p>';});h+='</div>';
  h+='<div class="ex-sec"><p class="ex-q"><b>(A) Fill in the blanks with the correct similes. (12%@2%)</b></p>'+exBankTable([p.A.bank1,p.A.bank2])+'<ol class="ex-ol">';
  p.A.items.forEach(it=>{h+='<li>'+blanks(it.s)+'</li>';});h+='</ol></div>';
  h+='<div class="ex-sec"><p class="ex-q"><b>(B) Fill in the blanks with the correct idioms. You may need to change the verb form. (12%@2%)</b></p>'+exBankTable([p.B.bank])+'<ol class="ex-ol">';
  p.B.items.forEach(it=>{h+='<li>'+blanks(it.s)+'</li>';});h+='</ol></div>';
  h+='<div class="ex-sec"><p class="ex-q"><b>(C) Complete the passage with the correct form of the verbs in brackets. (10%@1%)</b></p><p class="ex-pass">'+blanks(p.C.s)+'</p></div>';
  h+='<div class="ex-sec"><p class="ex-q"><b>(D) Finish the conversation with the correct names of the jobs. (10%@2%)</b></p>'+exBankTable([p.D.bank]);
  p.D.lines.forEach(l=>{h+='<p class="ex-it"><b>'+l.who+'</b>：'+blanks(l.s)+'</p>';});h+='</div>';
  h+='<div class="ex-sec"><p class="ex-q"><b>(E) Finish the sentences with the correct expressions from the table. (12%@3%)</b></p>'+exBankTable([p.E.bank]);
  p.E.items.forEach(it=>{h+='<p class="ex-it">'+it.lead+' __________ .</p>';});h+='</div>';
  h+='<div class="ex-sec"><p class="ex-q"><b>(F) Complete the passage with the correct phrasal verbs. You may need to change the verb form. (10%@2%)</b></p>'+exBankTable([p.F.bank])+'<p class="ex-pass">'+blanks(p.F.s)+'</p></div>';
  h+='<div class="ex-sec"><p class="ex-q"><b>(G) Complete the conversation with the words given. You may use each word ONCE. (6%@1%)</b></p>'+exBankTable([p.G.bank]);
  p.G.lines.forEach(l=>{h+='<p class="ex-it"><b>'+l.who+'</b>：'+blanks(l.s)+'</p>';});h+='</div>';
  h+='<div class="ex-sec"><p class="ex-q"><b>(H) Read the article and answer the questions. (10%：MC 2%×2，其餘 2%)</b></p><div class="ex-pass"><b>'+p.H.title+'</b><br>'+p.H.s+'</div>';
  p.H.mc.forEach((m,i)=>{h+='<p class="ex-it">('+(i+1)+') '+m.q+'　'+m.opts.join('　')+'</p>';});
  p.H.open.forEach((o,i)=>{h+='<p class="ex-it">('+(i+3)+') '+o.q+'</p><p class="ex-lines">________________________________________________________________</p>';});
  h+='<p class="ex-it">(5) '+blanks(p.H.fill.q)+'</p></div>';
  h+='<div class="ex-sec"><p class="ex-q"><b>(I) Read the poster and answer the questions. (8%：MC 1%×4，回答 2%×2)</b></p><div class="ex-pass"><b>'+p.I.title+'</b><br>'+p.I.s+'</div>';
  p.I.mc.forEach((m,i)=>{h+='<p class="ex-it">('+(i+1)+') '+m.q+'　'+m.opts.join('　')+'</p>';});
  p.I.open.forEach((o,i)=>{h+='<p class="ex-it">('+(i+5)+') '+o.q+'</p><p class="ex-lines">________________________________________________________________</p>';});
  h+='</div>';
  h+='<div class="ex-sec"><p class="ex-q"><b>(J) Fill in the blanks with the word \'since\' or \'therefore\'. You may use each word more than once. (10%@1%)</b></p><ol class="ex-ol">';
  p.J.items.forEach(it=>{h+='<li>'+blanks(it.s)+'</li>';});h+='</ol></div>';
  if(ans){
    h+='<div class="ex-anspage"><p class="ex-lead"><b>答案版 Answers</b></p><p class="ex-ans"><b>Warm-up：</b>'+p.head.fills.map(f=>f.a[0]).join('；')+'</p>';
    h+='<p class="ex-ans"><b>(A)：</b>'+p.A.items.map((it,i)=>'('+(i+1)+') '+it.a[0]+' / '+it.a[1]).join('；')+'</p>';
    h+='<p class="ex-ans"><b>(B)：</b>'+p.B.items.map((it,i)=>'('+(i+1)+') '+it.a[0]).join('；')+'</p>';
    h+='<p class="ex-ans"><b>(C)：</b>'+p.C.a.map((a,i)=>'('+(i+1)+') '+a[0]).join('；')+'</p>';
    h+='<p class="ex-ans"><b>(D)：</b>'+p.D.lines.map((l,i)=>'('+(i+1)+') '+l.a[0]).join('；')+'</p>';
    h+='<p class="ex-ans"><b>(E)：</b>'+p.E.items.map((it,i)=>'('+(i+1)+') '+it.a).join('；')+'</p>';
    h+='<p class="ex-ans"><b>(F)：</b>'+p.F.a.map((a,i)=>'('+(i+1)+') '+a[0]).join('；')+'</p>';
    h+='<p class="ex-ans"><b>(G)：</b>'+p.G.a.map((a,i)=>'('+(i+1)+') '+a[0]).join('；')+'</p>';
    h+='<p class="ex-ans"><b>(H)：</b>(1) '+p.H.mc[0].opts[p.H.mc[0].a]+'；(2) '+p.H.mc[1].opts[p.H.mc[1].a]+'；(3) '+p.H.open[0].model+'；(4) '+p.H.open[1].model+'；(5) '+p.H.fill.a[0][0]+'</p>';
    h+='<p class="ex-ans"><b>(I)：</b>(1) '+p.I.mc[0].opts[p.I.mc[0].a]+'；(2) '+p.I.mc[1].opts[p.I.mc[1].a]+'；(3) '+p.I.mc[2].opts[p.I.mc[2].a]+'；(4) '+p.I.mc[3].opts[p.I.mc[3].a]+'；(5) '+p.I.open[0].model+'；(6) '+p.I.open[1].model+'</p>';
    h+='<p class="ex-ans"><b>(J)：</b>'+p.J.items.map((it,i)=>'('+(i+1)+') '+(Array.isArray(it.a)?it.a[0]:it.a)).join('；')+'</p></div>';
  }
  return h;
}
function printExamPaper(){
  if(!curExamPaper)genExamPaper();
  const ans=document.getElementById('examPrintAns').checked;
  document.getElementById('examPrintSheet').innerHTML=examPrintHtml(curExamPaper,ans);
  if(!window._examPrintBound){window._examPrintBound=true;window.addEventListener('afterprint',function(){document.body.classList.remove('printing-paper');});}
  document.body.classList.add('printing-paper');
  if(typeof window.print==='function')window.print();else setTimeout(function(){document.body.classList.remove('printing-paper');},300);
}
// ---- v1.28 一次出 10 套（去重組卷 + 目錄卡 + 整冊打印） ----
function genTenExamPapers(){
  const B=EXAM_QBANK[curExamGrade];
  const seen={},pairs={},list=[];
  for(let tries=0;tries<800&&list.length<10;tries++){
    const p={head:exPick(B.heads),A:exPick(B.A),B:exPick(B.B),C:exPick(B.C),D:exPick(B.D),E:exPick(B.E),F:exPick(B.F),G:exPick(B.G),H:exPick(B.H),I:exPick(B.I),J:exPick(B.J)};
    const sig=JSON.stringify(p);
    if(seen[sig])continue;
    const pair=p.H.title+' | '+p.I.title;
    if(pairs[pair])continue;
    seen[sig]=1;pairs[pair]=1;list.push(p);
  }
  window._tenPapers=list;
  let h='<div class="ex-sec" id="exTenBox"><p class="ex-q"><b>📋 已生成 '+list.length+' 套'+curExamGrade+' 呈分試模擬卷</b>（每套整卷內容互不相同，閱讀＋海報組合亦不重複；當前屏幕上的作答卷不受影響）</p><table class="ex-bank"><tr><th>套號</th><th>閱讀理解 (H)</th><th>海報閱讀 (I)</th><th>時態篇章 (C) 開頭</th><th>操作</th></tr>';
  list.forEach((p,i)=>{
    h+='<tr><td><b>第 '+(i+1)+' 套</b></td><td>'+p.H.title+'</td><td>'+p.I.title+'</td><td>'+p.C.s.slice(0,38)+'…</td><td><button class="btn" onclick="showTenPaper('+i+')">📄 打開</button> <button class="btn" onclick="showTenAnswer('+i+')">📖 答案</button></td></tr>';
  });
  h+='</table><p class="ex-it">勾選「含答案版」後按下方按鈕，10 套卷一次打印（每套獨立分頁，答案頁跟在各自卷後）。</p>';
  h+='<p class="ex-it"><button class="btn" id="examTenPrintBtn" onclick="printTenExamPapers()">🖨 打印這 '+list.length+' 套卷子</button>　<span class="folk">每套右側「📄 打開」整卷作答，「📖 答案」直接在屏幕上開卷底答案（自動填入正確答案並綠色高亮，不計入最佳分）。</span></p></div>';
  document.getElementById('examPaperBox').insertAdjacentHTML('beforeend',h);
  try{document.getElementById('exTenBox').scrollIntoView({behavior:'smooth',block:'start'});}catch(e){}
}
var curTenNo=0;
function showTenPaper(i){
  const p=(window._tenPapers||[])[i];
  if(!p){alert('請先按「📋 一次出 10 套」。');return;}
  curTenNo=i+1;
  curExamPaper=p;
  renderExamPaper();showExamStat();
  try{document.getElementById('examPaperBox').scrollIntoView({behavior:'smooth',block:'start'});}catch(e){}
}
function showTenAnswer(i){
  const p=(window._tenPapers||[])[i];
  if(!p){alert('請先按「📋 一次出 10 套」。');return;}
  showTenPaper(i);
  p.A.items.forEach(function(it,k){const e0=document.getElementById('ex_A_'+k+'_0'),e1=document.getElementById('ex_A_'+k+'_1');if(e0)e0.value=it.a[0];if(e1)e1.value=it.a[1];});
  p.B.items.forEach(function(it,k){const el=document.getElementById('ex_B_'+k+'_0');if(el)el.value=(Array.isArray(it.a)?it.a[0]:it.a);});
  p.C.a.forEach(function(accs,k){const el=document.getElementById('ex_C_'+k);if(el)el.value=accs[0];});
  p.D.lines.forEach(function(l,k){const el=document.getElementById('ex_D_'+k+'_0');if(el)el.value=l.a[0];});
  p.E.items.forEach(function(it,k){const a=(Array.isArray(it.a)?it.a:[it.a]);const el=document.getElementById('ex_E_'+k);if(el)el.value=a[0];});
  p.F.a.forEach(function(accs,k){const el=document.getElementById('ex_F_'+k);if(el)el.value=accs[0];});
  p.G.a.forEach(function(accs,k){const el=document.getElementById('ex_G_'+k);if(el)el.value=accs[0];});
  p.H.mc.forEach(function(m,k){const r=document.querySelector('input[name="ex_H_mc'+k+'"][value="'+m.a+'"]');if(r)r.checked=true;});
  p.H.open.forEach(function(o,k){const el=document.getElementById('ex_H_open'+k);if(el)el.value=o.model;});
  {const el=document.getElementById('ex_H_fill_0');if(el)el.value=p.H.fill.a.flat()[0];}
  p.I.mc.forEach(function(m,k){const r=document.querySelector('input[name="ex_I_mc'+k+'"][value="'+m.a+'"]');if(r)r.checked=true;});
  p.I.open.forEach(function(o,k){const el=document.getElementById('ex_I_open'+k);if(el)el.value=o.model;});
  p.J.items.forEach(function(it,k){const el=document.getElementById('ex_J_'+k+'_0');if(el)el.value=(Array.isArray(it.a)?it.a[0]:it.a);});
  gradeExamPaper(true);
  try{document.getElementById('examPaperBox').scrollIntoView({behavior:'smooth',block:'start'});}catch(e){}
}
function printTenExamPapers(){
  const list=window._tenPapers||[];
  if(!list.length){ alert('請先按「📋 一次出 10 套」。'); return; }
  const ans=document.getElementById('examPrintAns').checked;
  let h='';
  list.forEach((p,i)=>{ if(i)h+='<div style="page-break-before:always"></div>'; h+=examPrintHtml(p,ans,i+1); });
  document.getElementById('examPrintSheet').innerHTML=h;
  if(!window._examPrintBound){window._examPrintBound=true;window.addEventListener('afterprint',function(){document.body.classList.remove('printing-paper');});}
  document.body.classList.add('printing-paper');
  if(typeof window.print==='function')window.print();else setTimeout(function(){document.body.classList.remove('printing-paper');},300);
}
document.querySelectorAll('#examChips .chip').forEach(c=>c.onclick=()=>{
  curExamGrade=c.dataset.pg;
  document.querySelectorAll('#examChips .chip').forEach(x=>x.classList.toggle('on',x===c));
  genExamPaper();
});
// ---- v1.27 呈分試卷 AI 出新卷（OpenAI 兼容，復用 hkk_ai_cfg） ----
function exAiPrompt(g){
  const sys='You are an expert author of Hong Kong primary school English exam papers (呈分試). Return ONLY a valid JSON object — no markdown fences, no explanation. All content must be original and age-appropriate for grade '+g+'. Use Hong Kong context (school life, places, festivals).';
  const usr='Create ONE complete mock English exam paper. JSON schema:\n'
  +'{\n'
  +'"head":{"words":[exactly 8 items {"w":"word (part of speech)","zh":"中文解釋"}],"fills":[exactly 5 items {"s":"sentence containing {0} for the blank","a":["accepted answer"]}]},\n'
  +'"A":{"bank1":[6 adjectives],"bank2":[6 noun phrases],"items":[exactly 6 items {"s":"sentence with as {0} as {1} blanks","a":["adjective","phrase"]}]},\n'
  +'"B":{"bank":[6 idioms],"items":[exactly 6 items {"s":"sentence with {0} blank","a":["idiom with verb form changed if needed"]}]},\n'
  +'"C":{"s":"a passage with (e.g.) done for blank 0 and (1)..(10) marking blanks {0}..{9} with verb hints in brackets","a":[exactly 10 arrays of accepted answers]},\n'
  +'"D":{"bank":[6 job names],"lines":[exactly 5 items {"who":"Name","s":"first-person sentence with (n) {0}","a":["job"]}]},\n'
  +'"E":{"bank":[4 short expressions],"items":[exactly 4 items {"lead":"Since ...","a":["expression"]}]},\n'
  +'"F":{"bank":[6 phrasal verbs],"s":"a passage with (e.g.) and {0}..{4}","a":[exactly 5 arrays]},\n'
  +'"G":{"bank":[6 linking words],"lines":[3 items with {"who","s"} containing {0}..{5} across the lines],"a":[exactly 6 arrays]},\n'
  +'"H":{"title":"article title","s":"90-120 word article with <br> between paragraphs","mc":[exactly 2 items {"q":"question","opts":[4 options],"a":correctIndex0to3}],"open":[exactly 2 items {"q":"question","keys":["keywords that MUST appear in model"],"model":"model answer"}],"fill":{"q":"sentence with {0} from the article","a":[["answer"]]}},\n'
  +'"I":{"title":"poster title","s":"a school poster/notice with <b>sections</b> and <br>","mc":[exactly 4 items {"q","opts":[4 options],"a":index}],"open":[exactly 2 items {"q","keys","model"}]},\n'
  +'"J":{"items":[exactly 10 items {"s":"sentence with {0} blank","a":["since" or "therefore"]}]}\n'
  +'}\n'
  +'Rules: placeholders {n} must be used exactly as shown; every word in keys MUST appear in the model answer; distractor options in bank tables may exceed the blanks; keep everything at '+g+' level.';
  return [{role:'system',content:sys},{role:'user',content:usr}];
}
function exValidate(o){
  function arr(x,n){return Array.isArray(x)&&x.length===n;}
  if(!o||!o.head||!arr(o.head.words,8)||!arr(o.head.fills,5))return false;
  if(!o.A||!arr(o.A.items,6)||!o.B||!arr(o.B.items,6)||!o.C||!arr(o.C.a,10))return false;
  if(!o.D||!arr(o.D.lines,5)||!o.E||!arr(o.E.items,4)||!o.F||!arr(o.F.a,5))return false;
  if(!o.G||!arr(o.G.a,6)||!o.H||!arr(o.H.mc,2)||!arr(o.H.open,2)||!o.H.fill)return false;
  if(!o.I||!arr(o.I.mc,4)||!arr(o.I.open,2)||!o.J||!arr(o.J.items,10))return false;
  if(o.J.items.some(function(it){const a=Array.isArray(it.a)?it.a[0]:it.a;return a!=='since'&&a!=='therefore';}))return false;
  return true;
}
async function exAiPaper(){
  const cfg=getAiCfg();
  if(!cfg.base||!cfg.key||!cfg.model){ alert('尚未配置 AI 接口。請到「練習→英文→智能練習卷」底部的「⚙ AI 設置」填寫 Base URL／密鑰／模型（僅存本瀏覽器），再回來生成新卷。'); return; }
  const btn=document.getElementById('examAiBtn');const t0=btn?btn.textContent:'';
  if(btn){btn.disabled=true;btn.textContent='AI 生成中…（約 1–2 分鐘）';}
  try{
    const body={model:cfg.model,messages:exAiPrompt(curExamGrade),temperature:0.9};
    try{ body.response_format={type:'json_object'}; }catch(e){}
    const resp=await fetch(cfg.base.replace(/\/$/,'')+'/chat/completions',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+cfg.key},body:JSON.stringify(body)});
    if(!resp||!resp.ok)throw new Error('HTTP '+(resp?resp.status:'無回應'));
    let data; try{ data=await resp.json(); }catch(e){ throw new Error('回應不是 JSON'); }
    let content=data&&data.choices&&data.choices[0]&&data.choices[0].message&&data.choices[0].message.content;
    if(!content)throw new Error('回應為空');
    content=content.trim().replace(/^```(?:json)?/i,'').replace(/```$/i,'').trim();
    let obj; try{ obj=JSON.parse(content); }catch(e){ throw new Error('內容不是合法 JSON（模型未按要求返回）'); }
    if(!exValidate(obj))throw new Error('結構不合規（段落或題數不符要求）');
    obj.src='ai';
    curTenNo=0;
    curExamPaper=obj;
    renderExamPaper(); showExamStat();
  }catch(e){
    alert('AI 出卷失敗：'+(e&&e.message?e.message:e)+'。常見原因：CORS 限制／密鑰無效／模型未按 JSON 返回。可改用「🎲 出新卷」（本地題庫，隨機組合 2¹⁰ 種）。');
  }finally{ if(btn){btn.disabled=false;btn.textContent=t0;} }
}

// ============ 繪本閱讀打卡（v1.35，v1.37 加 ▶ 本地播放）：牛津樹 1–9 階書單 ============
var ORT_BOOKS = DATA.ort_books || [];
var ORT_ORDER = ['1階','1–2階','3階','4階','5階','6階','7階','8階','9階'];
var curOrtLv = '';
var ORT_LOCAL = (location.protocol === 'file:');  // ▶ 播放僅在本地打開本文件時可用
var ORT_DIR = 'G:/00 咨询&公自媒体/22 香港插班/88 涵涵/01英語/01 牛津树/童老师牛津绘本视频';
function ortHref(p){
  try{
    var segs=(ORT_DIR + '/' + p).split('/');
    var drive=segs.shift();  // 盤符 'G:' 不編碼（encodeURIComponent 會把冒號變 %3A）
    return 'file:///' + drive + '/' + segs.map(encodeURIComponent).join('/');
  }catch(e){ return ''; }
}
function ortRead(){
  try{ return JSON.parse(localStorage.getItem('hkk_ort')||'{}'); }catch(e){ return {}; }
}
function ortToggle(t){
  var r = ortRead();
  if(r[t]) delete r[t]; else r[t] = 1;
  localStorage.setItem('hkk_ort', JSON.stringify(r));
  renderOrt();
}
function renderOrt(){
  // 阶 chips（全部 + 各阶，带计数）
  var bylv = {}; ORT_BOOKS.forEach(function(b){ bylv[b.lv] = (bylv[b.lv]||0)+1; });
  var ch = '<span class="chip'+(curOrtLv===''?' on':'')+'" data-lv="">全部 ('+ORT_BOOKS.length+')</span>';
  ORT_ORDER.forEach(function(lv){
    if(bylv[lv]) ch += '<span class="chip'+(curOrtLv===lv?' on':'')+'" data-lv="'+lv+'">'+lv+' ('+bylv[lv]+')</span>';
  });
  document.getElementById('ortChips').innerHTML = ch;
  document.querySelectorAll('#ortChips .chip').forEach(function(c){
    c.onclick = function(){ curOrtLv = c.dataset.lv; renderOrt(); };
  });
  // 书单（按阶分块，打卡）
  var r = ortRead(), done = 0;
  var h = '';
  ORT_BOOKS.forEach(function(b){ if(r[b.lv+'|'+b.t]) done++; });
  var shown = 0;
  ORT_ORDER.forEach(function(lv){
    if(curOrtLv && lv !== curOrtLv) return;
    var bs = ORT_BOOKS.filter(function(b){ return b.lv === lv; });
    if(!bs.length) return;
    shown += bs.length;
    var d = bs.filter(function(b){ return r[b.lv+'|'+b.t]; }).length;
    var pct = Math.round(d/bs.length*100);
    h += '<div class="ort-lv"><div class="ort-lv-h"><span>'+lv+' · '+bs.length+' 本</span>'
      + '<span class="ort-bar"><i style="width:'+pct+'%"></i></span><span style="font-size:12px;color:#475069">'+d+'/'+bs.length+' 已讀</span></div>'
      + '<div class="ort-books">';
    bs.forEach(function(b){
      var k = b.lv+'|'+b.t;
      h += '<span class="ort-bkw"><button type="button" class="ort-bk'+(r[k]?' done':'')+'" data-k="'+k.replace(/&/g,'&amp;').replace(/"/g,'&quot;')+'" onclick="ortToggle(this.dataset.k)">'
        + (r[k]?'✓ ':'') + b.t + (b.n>1 ? '<span class="ort-n">('+b.n+'講)</span>' : '') + '</button>';
      if(ORT_LOCAL && b.fs && b.fs.length){
        b.fs.forEach(function(fp,i){
          h += '<a class="ort-play" href="'+ortHref(fp)+'" target="_blank" rel="noopener" title="播放講解視頻">▶'+(b.fs.length>1?(i+1):'')+'</a>';
        });
      }
      h += '</span>';
    });
    h += '</div></div>';
  });
  document.getElementById('ortStat').innerHTML = '總進度：<b>'+done+'</b> / '+ORT_BOOKS.length+' 本已讀'+(done>=ORT_BOOKS.length&&ORT_BOOKS.length?' 🎉 全部讀完！':'');
  document.getElementById('ortList').innerHTML = h || '<p class="folk">沒有這一階的書。</p>';
}
// ============ 朗文詞庫（v1.35）：LWTE GOLD 5A/5B ============
var LWTE_BANKS = DATA.lwte_banks || [];
var curLwteBk = '';
function lwteRead(){
  try{ return JSON.parse(localStorage.getItem('hkk_lwte')||'{}'); }catch(e){ return {}; }
}
function lwteToggle(t){
  var r = lwteRead();
  if(r[t]) delete r[t]; else r[t] = 1;
  localStorage.setItem('hkk_lwte', JSON.stringify(r));
  renderLwte();
}
function renderLwte(){
  var total = 0; LWTE_BANKS.forEach(function(e){ total += e.items.length; });
  var bybk = {}; LWTE_BANKS.forEach(function(e){ bybk[e.bk] = (bybk[e.bk]||0)+e.items.length; });
  var ch = '';
  Object.keys(bybk).forEach(function(bk){
    ch += '<span class="chip'+(curLwteBk===bk?' on':'')+'" data-bk="'+bk+'">'+bk+' ('+bybk[bk]+')</span>';
  });
  ch += '<span class="chip'+(curLwteBk===''?' on':'')+'" data-bk="">全部 ('+total+')</span>';
  document.getElementById('lwteChips').innerHTML = ch;
  document.querySelectorAll('#lwteChips .chip').forEach(function(c){
    c.onclick = function(){ curLwteBk = c.dataset.bk; renderLwte(); };
  });
  var r = lwteRead(), done = 0, h = '';
  LWTE_BANKS.forEach(function(e){ e.items.forEach(function(it){ if(r[e.bk+'|'+it.w]) done++; }); });
  LWTE_BANKS.forEach(function(e){
    if(curLwteBk && e.bk !== curLwteBk) return;
    var d = e.items.filter(function(it){ return r[e.bk+'|'+it.w]; }).length;
    var pct = Math.round(d/e.items.length*100);
    h += '<div class="ort-lv"><div class="ort-lv-h"><span>'+e.bk+' · '+e.cat+' · '+e.items.length+'</span>'
      + '<span class="ort-bar"><i style="width:'+pct+'%"></i></span><span style="font-size:12px;color:#475069">'+d+'/'+e.items.length+'</span></div>'
      + '<div class="ort-books">';
    e.items.forEach(function(it){
      var k = e.bk+'|'+it.w;
      var attr = k.replace(/&/g,'&amp;').replace(/"/g,'&quot;');
      h += '<button type="button" class="ort-bk'+(r[k]?' done':'')+'" data-k="'+attr+'" onclick="lwteToggle(this.dataset.k)">'+it.w+'<span style="opacity:.8"> '+it.zh+'</span></button>';
    });
    h += '</div></div>';
  });
  document.getElementById('lwteStat').innerHTML = '總進度：<b>'+done+'</b> / '+total+' 條已掌握'+(done>=total&&total?' 🎉 全部掌握！':'');
  document.getElementById('lwteList').innerHTML = h || '<p class="folk">沒有這一冊的詞庫。</p>';
}
document.querySelectorAll('#enPracSub button').forEach(b=>b.onclick=()=>{
  const es=b.dataset.es;
  const sw=(id,on)=>{const el=document.getElementById(id); if(el) el.style.display=on?'block':'none';};
  try{
    document.querySelectorAll('#enPracSub button').forEach(x=>x.classList.toggle('on',x===b));
    sw('hkView',es==='hk'); sw('vocabView',es==='vocab'); sw('ivView',es==='iv');
    sw('paperView',es==='paper'); sw('goalView',es==='goal'); sw('examView',es==='exam');
    sw('ortView',es==='ort'); sw('lwteView',es==='lwte');
    if(es==='hk')renderHk(); else if(es==='vocab')renderVocab(); else if(es==='paper' && !curEnPaper.length) genEnPaper(); else if(es==='exam' && !curExamPaper) genExamPaper(); else if(es==='ort')renderOrt(); else if(es==='lwte')renderLwte();
  }catch(e){ console.error('切換視圖失敗：',e); }
});
document.querySelectorAll('#mathPracSub button').forEach(b=>b.onclick=()=>{
  const es=b.dataset.es;
  const sw=(id,on)=>{const el=document.getElementById(id); if(el) el.style.display=on?'block':'none';};
  try{
    document.querySelectorAll('#mathPracSub button').forEach(x=>x.classList.toggle('on',x===b));
    sw('mTermsView',es==='mterms'); sw('mathPaperView',es==='mpaper');
    if(es==='mpaper' && !curMathPaper.length) genMathPaper();
  }catch(e){ console.error('切換視圖失敗：',e); }
});
document.querySelectorAll('#mpgChips .chip').forEach(c=>c.onclick=()=>{
  curMathGrade=c.dataset.pg;
  document.querySelectorAll('#mpgChips .chip').forEach(x=>x.classList.toggle('on',x===c));
  genMathPaper();
});
document.querySelectorAll('#ssChips .chip').forEach(c=>c.onclick=()=>{
  const k=c.dataset.ss;
  document.querySelectorAll('#ssChips .chip').forEach(x=>x.classList.toggle('on',x===c));
  document.querySelectorAll('#ssTable tbody tr').forEach(tr=>{
    tr.style.display=(k==='all'||tr.dataset.lan===k||tr.dataset.ss===k)?'':'none';
  });
});
document.querySelectorAll('#tpChips .chip').forEach(c=>c.onclick=()=>{
  const k=c.dataset.tp;
  document.querySelectorAll('#tpChips .chip').forEach(x=>x.classList.toggle('on',x===c));
  document.querySelectorAll('#tpTable tbody tr').forEach(tr=>{
    tr.style.display=(k==='all'||(' '+tr.dataset.tp+' ').includes(' '+k+' '))?'':'none';
  });
});
document.querySelectorAll('#psChips .chip').forEach(c=>c.onclick=()=>{
  const k=c.dataset.m;
  document.querySelectorAll('#psChips .chip').forEach(x=>x.classList.toggle('on',x===c));
  document.querySelectorAll('#psTable tbody tr').forEach(tr=>{
    tr.style.display=(k==='all'||(' '+tr.dataset.m+' ').includes(' '+k+' '))?'':'none';
  });
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
showMain(curTab); // v1.50 修：原硬編碼 'guide' 蓋掉默認 tab，致 v1.48 ②未生效

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
      d.innerHTML=`<div><span class="w">${w.w}</span> <span class="ph">${w.ipa||''}</span> <span class="mini" data-sp="${w.w}">🔊</span>${known?' <span class="ok">✓</span>':''}<span class="tp"> · ${w.grade} · ${w.theme}</span></div><div class="zh">${w.zh}</div>`;
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

// ---- 繁體對照（v1.25 分級） ----
let curFtGrade='all';
function renderFt(){
  const q=document.getElementById('ftSearch').value.trim();
  const list=document.getElementById('ftList'); list.innerHTML='';
  const src=curFtGrade==='all'?FT_MAP:FT_GRADES[curFtGrade];
  const rows=src.filter(([s,f])=>!q||s.includes(q)||f.includes(q));
  rows.forEach(([s,f,note])=>{
    const d=document.createElement('div'); d.className='ftrow';
    d.innerHTML='<span class="s">'+s+'</span><span class="ar">→</span><span class="f">'+f+'</span>'+(note?'<span class="mini" style="margin-left:8px">'+note+'</span>':'');
    list.appendChild(d);
  });
  document.getElementById('ftCount').textContent='共 '+rows.length+' 字';
  if(!list.children.length)list.innerHTML='<div style="color:#888;font-size:13px">無相符字</div>';
}
document.querySelectorAll('#ftChips .chip').forEach(c=>c.onclick=()=>{
  curFtGrade=c.dataset.fg;
  document.querySelectorAll('#ftChips .chip').forEach(x=>x.classList.toggle('on',x===c));
  renderFt();
});

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
  const data={pProg,vProg,hProg,mProg,ver:'hkk_v1.51',exported:new Date().toISOString().slice(0,10)};
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
function flashReveal(){document.getElementById('flashZh').style.display='block';document.getElementById('flashZh').innerHTML=flashCur.zh+(flashCur.ipa?' <span class="ph">'+flashCur.ipa+'</span>':'');document.getElementById('flashReveal').style.display='none';document.getElementById('flashKnow').style.display='inline-block';document.getElementById('flashUnk').style.display='inline-block';}
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

// ============ 賬號系統（v1.33）：本機賬號 + 進度按賬號隔離 ============
// 純前端方案（雲服務未開通）：賬號/進度僅存本瀏覽器 localStorage，密碼存 salt+SHA-256（Web Crypto 標準實現）。
// 線上（https 非本機域名）強制登入；本地直開 file:// / localhost 免登入，以「本地」身份使用。
async function hkSha256(s){
  const buf=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s));
  return Array.from(new Uint8Array(buf)).map(function(x){return ('0'+x.toString(16)).slice(-2);}).join('');
}
var AUTH_FORCE=(typeof location!=='undefined'&&location.protocol==='https:'&&location.hostname&&location.hostname.indexOf('localhost')!==0&&location.hostname.indexOf('127.')!==0&&location.hostname.indexOf('192.168.')!==0);
var AUTH_USERS='hkk_auth_users',AUTH_SESS='hkk_auth_sess',DEFAULT_USER='本地';
var curUser=DEFAULT_USER;
function authUsers(){try{return JSON.parse(localStorage.getItem(AUTH_USERS)||'{}');}catch(e){return {};}}
function authSaveUsers(u){localStorage.setItem(AUTH_USERS,JSON.stringify(u));}
function authReadSess(){try{return JSON.parse(localStorage.getItem(AUTH_SESS)||sessionStorage.getItem(AUTH_SESS)||'null');}catch(e){return null;}}
function authNameOk(n){return typeof n==='string'&&n.length>=2&&n.length<=16&&n!=='本地';}
// 進度作用域：全局 hkk_* 鍵屬於當前用戶；切換時搬到 hkk_u@<名>@<鍵>，登入時搬回
function authKeys(){var out=[];for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k&&k.indexOf('hkk_')===0&&k.indexOf('hkk_u@')!==0&&k!==AUTH_USERS&&k!==AUTH_SESS)out.push(k);}return out;}
function authSaveScope(name){if(!name)return;authKeys().forEach(function(k){localStorage.setItem('hkk_u@'+name+'@'+k.slice(4),localStorage.getItem(k));localStorage.removeItem(k);});}
function authLoadScope(name){if(!name||name===DEFAULT_USER)return;var pre='hkk_u@'+name+'@';for(var i=localStorage.length-1;i>=0;i--){var k=localStorage.key(i);if(k&&k.indexOf(pre)===0){localStorage.setItem('hkk_'+k.slice(pre.length),localStorage.getItem(k));localStorage.removeItem(k);}}}
function authShowTab(t){
  document.getElementById('authTabLogin').classList.toggle('on',t==='login');
  document.getElementById('authTabReg').classList.toggle('on',t==='reg');
  document.getElementById('authLoginBox').style.display=t==='login'?'block':'none';
  document.getElementById('authRegBox').style.display=t==='reg'?'block':'none';
  document.getElementById('authResetBox').style.display=t==='reset'?'block':'none';
  if(t==='login')document.getElementById('authResetBox').style.display='none';
  if(t==='reset')document.getElementById('authLoginBox').style.display='none';
}
function authTogglePwd(id,btn){var el=document.getElementById(id);if(!el)return;el.type=el.type==='password'?'text':'password';btn.textContent=el.type==='password'?'👁':'🙈';}
function authErr(id,msg,ok){var el=document.getElementById(id);if(el){el.textContent=msg||'';el.className='authErr'+(ok?' authOk':'');}}
function authShowGate(){var g=document.getElementById('authGate');g.classList.add('on');document.body.classList.add('authLock');document.getElementById('userChip').style.display='none';}
function authHideGate(){var g=document.getElementById('authGate');g.classList.remove('on');document.body.classList.remove('authLock');var chip=document.getElementById('userChip');chip.style.display='inline-flex';document.getElementById('userChipName').textContent='👤 '+curUser;}
function authRegister(){return authRegisterDo();}
async function authRegisterDo(){
  var n=document.getElementById('authRegName').value.trim(),p=document.getElementById('authRegPwd').value,p2=document.getElementById('authRegPwd2').value;
  if(!authNameOk(n)){authErr('authRegErr','暱稱需 2–16 字（中文或英文），不能用「本地」');return;}
  if(p.length<8){authErr('authRegErr','密碼至少 8 位');return;}
  if(p!==p2){authErr('authRegErr','兩次密碼不一致');return;}
  var u=authUsers();
  if(u[n]){authErr('authRegErr','這個暱稱已註冊，請直接登入');return;}
  var salt=(''+Math.random()).slice(2)+Date.now();
  u[n]={salt:salt,hash:await hkSha256(salt+'|'+p),created:new Date().toISOString().slice(0,10)};
  authSaveUsers(u);authErr('authRegErr','註冊成功，正在進入…',true);
  authEnter(n,true);
}
function authLogin(){return authLoginDo();}
async function authLoginDo(){
  var n=document.getElementById('authLoginName').value.trim(),p=document.getElementById('authLoginPwd').value;
  var u=authUsers();
  if(!u[n]){authErr('authLoginErr','沒有這個暱稱，請先註冊');return;}
  if(u[n].hash!==await hkSha256(u[n].salt+'|'+p)){authErr('authLoginErr','密碼不正確');return;}
  authErr('authLoginErr','登入成功，正在進入…',true);
  authEnter(n,document.getElementById('authRemember').checked);
}
function authReset(){return authResetDo();}
async function authResetDo(){
  var n=document.getElementById('authResetName').value.trim(),p=document.getElementById('authResetPwd').value;
  var u=authUsers();
  if(!u[n]){authErr('authResetErr','沒有這個暱稱');return;}
  if(p.length<8){authErr('authResetErr','新密碼至少 8 位');return;}
  if(!confirm('確定重置「'+n+'」？該賬號的全部學習進度將被清空，且無法恢復。'))return;
  var salt=(''+Math.random()).slice(2)+Date.now();
  u[n]={salt:salt,hash:await hkSha256(salt+'|'+p),created:new Date().toISOString().slice(0,10)};
  authSaveUsers(u);
  authKeys().forEach(function(k){localStorage.removeItem('hkk_u@'+n+'@'+k.slice(4));});
  authErr('authResetErr','已重置，用新密碼登入吧',true);
  authShowTab('login');document.getElementById('authLoginName').value=n;
}
function authEnter(name,remember){
  if(curUser!==name){authSaveScope(curUser);authLoadScope(name);}
  curUser=name;
  try{sessionStorage.removeItem(AUTH_SESS);}catch(e){}
  localStorage.removeItem(AUTH_SESS);
  if(remember)localStorage.setItem(AUTH_SESS,JSON.stringify({name:name}));
  else sessionStorage.setItem(AUTH_SESS,JSON.stringify({name:name}));
  authHideGate();
  try{location.reload();}catch(e){}
}
function authLogout(){
  authSaveScope(curUser);
  localStorage.removeItem(AUTH_SESS);try{sessionStorage.removeItem(AUTH_SESS);}catch(e){}
  if(AUTH_FORCE){curUser=DEFAULT_USER;authSaveScope(DEFAULT_USER);location.reload();}
  else{curUser=DEFAULT_USER;authLoadScope(DEFAULT_USER);authSaveScope(DEFAULT_USER);location.reload();}
}
function authBoot(){
  var sess=authReadSess();
  if(sess&&sess.name&&(sess.name===DEFAULT_USER||authUsers()[sess.name])){
    curUser=sess.name;authLoadScope(sess.name);authHideGate();renderUserStat();return;
  }
  if(AUTH_FORCE){authShowGate();return;}
  curUser=DEFAULT_USER;authHideGate();renderUserStat();
}
function renderUserStat(){
  if(curUser===DEFAULT_USER)return;
  var chip=document.getElementById('userChip');chip.style.display='inline-flex';
  document.getElementById('userChipName').textContent='👤 '+curUser;
}
document.getElementById('authLoginPwd').addEventListener('keydown',function(e){if(e.key==='Enter')authLogin();});
document.getElementById('authRegPwd2').addEventListener('keydown',function(e){if(e.key==='Enter')authRegister();});
authBoot();
</script>
</body>
</html>'''
html = TEMPLATE.replace('__DATA__', DATA)
# 版本號從副標題單一真相源提取（公開版 vX.Y），輸出帶版本號文件名
_m = re.search(r'公開版\s+(v\d+\.\d+)', TEMPLATE)
VER = _m.group(1) if _m else 'v1.15'
out = os.path.join(WS, 'index_%s.html' % VER)
open(out, 'w', encoding='utf-8').write(html)
# 兼容副本：verify2.js 與預覽／部署預設入口均依賴 index.html
open(os.path.join(WS, 'index.html'), 'w', encoding='utf-8').write(html)
print('生成', out, os.path.getsize(out), 'bytes')
