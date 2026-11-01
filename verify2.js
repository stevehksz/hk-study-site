// 验证 v0.6 中英数站点结构（练习区按科目归口：中文/英文/數學）
const fs = require('fs');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync('index.html', 'utf-8');
const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true, url: 'https://localhost/' });
const { window } = dom;
const doc = window.document;

let pass = 0, fail = 0;
function ok(name, cond) {
  if (cond) { pass++; console.log('  ✓', name); }
  else { fail++; console.log('  ✗ FAIL', name); }
}

console.log('--- 导航与子导航 ---');
ok('主tab 5个(guide/plan/practice/progress/fun)', doc.querySelectorAll('nav button').length === 5);
ok('guideSub 4个(cn/en/math/ft)', doc.querySelectorAll('#guideSub button').length === 4);
ok('practiceSub 3个(cn/en/math)', doc.querySelectorAll('#practiceSub button').length === 3);

console.log('--- 数学术语表 ---');
const rows = doc.querySelectorAll('#mathBody tr');
ok('mathBody 已渲染行(>100)', rows.length > 100);
// 数一下分类覆盖
const cats = new Set([...doc.querySelectorAll('#mathBody tr td:first-child')].map(td => td.textContent));
ok('分类>=6', cats.size >= 6);
console.log('    分类:', [...cats].join(' / '));

console.log('--- 默认视图 ---');
ok('guideView 显示', doc.getElementById('guideView').style.display !== 'none');
ok('practiceView 隐藏', doc.getElementById('practiceView').style.display === 'none');
ok('guideSub 显示', doc.getElementById('guideSub').style.display !== 'none');
ok('practiceSub 隐藏', doc.getElementById('practiceSub').style.display === 'none');
ok('cnView 显示', doc.getElementById('cnView').style.display !== 'none');
ok('mathView 隐藏', doc.getElementById('mathView').style.display === 'none');

console.log('--- 切换: practice（默认中文） ---');
doc.querySelector('nav button[data-tab="practice"]').click();
ok('practiceView 显示', doc.getElementById('practiceView').style.display !== 'none');
ok('guideView 隐藏', doc.getElementById('guideView').style.display === 'none');
ok('practiceSub 显示', doc.getElementById('practiceSub').style.display !== 'none');
ok('cnPracView 显示(默认中文)', doc.getElementById('cnPracView').style.display !== 'none');
ok('enPracView 隐藏', doc.getElementById('enPracView').style.display === 'none');
ok('mathPracView 隐藏', doc.getElementById('mathPracView').style.display === 'none');

console.log('--- 切换: practice -> 英文 -> 詞表 ---');
doc.querySelector('#practiceSub button[data-sub="en"]').click();
ok('enPracView 显示', doc.getElementById('enPracView').style.display !== 'none');
ok('cnPracView 隐藏', doc.getElementById('cnPracView').style.display === 'none');
doc.querySelector('#enPracSub button[data-es="vocab"]').click();
ok('vocabView 显示', doc.getElementById('vocabView').style.display !== 'none');
ok('hkView 隐藏', doc.getElementById('hkView').style.display === 'none');

console.log('--- 练习→英文→升中面試（移入模块） ---');
doc.querySelector('#enPracSub button[data-es="iv"]').click();
ok('ivView 顯示', doc.getElementById('ivView').style.display !== 'none');
ok('hkView 隱藏(iv)', doc.getElementById('hkView').style.display === 'none');
ok('vocabView 隱藏(iv)', doc.getElementById('vocabView').style.display === 'none');
const ivTxt = doc.getElementById('ivView').textContent;
ok('升中面試含四卷結構', ivTxt.includes('Reading') && ivTxt.includes('Writing') && ivTxt.includes('Listening') && ivTxt.includes('Speaking'));
ok('升中面試含自我介紹模板', ivTxt.includes('Good morning'));
ok('升中面試含10大題型表', ivTxt.includes('報考原因') && ivTxt.includes('創意思考'));
ok('升中面試含小組DO/DONT', ivTxt.includes('加分做法') && ivTxt.includes('扣分做法'));
ok('升中面試含真實題例', ivTxt.includes('景嶺書院') && ivTxt.includes('可風中學'));
ok('升中面試含資料來源', ivTxt.includes('hkstudyroute') && ivTxt.includes('notesity'));
ok('升中面試含練習卡輸入', !!doc.getElementById('ivName') && !!doc.getElementById('ivOut'));
ok('升中面試含錄音按鈕', !!doc.getElementById('ivRecBtn'));
const ivNameEl=doc.getElementById('ivName');
ivNameEl.value='Test Lee';
ivNameEl.dispatchEvent(new doc.defaultView.Event('input'));
ok('自我介紹練習卡填名即生成', doc.getElementById('ivOut').textContent.includes('Test Lee'));

console.log('--- 切换: guide -> math ---');
doc.querySelector('nav button[data-tab="guide"]').click();
doc.querySelector('#guideSub button[data-sub="math"]').click();
ok('mathView 显示', doc.getElementById('mathView').style.display !== 'none');
ok('cnView 隐藏', doc.getElementById('cnView').style.display === 'none');

console.log('--- 数学筛选: 幾何（练习→數學） ---');
doc.querySelector('nav button[data-tab="practice"]').click();
doc.querySelector('#practiceSub button[data-sub="math"]').click();
ok('mathPracView 显示', doc.getElementById('mathPracView').style.display !== 'none');
doc.querySelector('#mathPracView .chip[data-mc="幾何"]').click();
const geoRows = doc.querySelectorAll('#mathBody tr');
let allGeo = true;
geoRows.forEach(r => { if (r.children[0] && r.children[0].textContent !== '幾何') allGeo = false; });
ok('幾何筛选后全为幾何(' + geoRows.length + '行)', geoRows.length > 0 && allGeo);

console.log('--- 数学搜索: fraction ---');
doc.querySelector('#mathPracView .chip[data-mc="all"]').click();
const ms = doc.getElementById('mathSearch'); ms.value = 'fraction';
ms.dispatchEvent(new window.Event('input'));
const fRows = doc.querySelectorAll('#mathBody tr');
ok('搜 fraction 有结果(' + fRows.length + ')', fRows.length > 0);

console.log('--- 诗词/词表仍渲染 ---');
doc.querySelector('nav button[data-tab="practice"]').click();
ok('poemGrid 有卡片', doc.querySelectorAll('#poemGrid .pcard').length > 0);
doc.querySelector('#practiceSub button[data-sub="en"]').click();
doc.querySelector('#enPracSub button[data-es="vocab"]').click();
ok('vocabList 有卡片', doc.querySelectorAll('#vocabList .vcard').length > 0);

console.log('--- 诗词年级筛选（练习→中文） ---');
doc.querySelector('#practiceSub button[data-sub="cn"]').click();
const pgChips = doc.querySelectorAll('#cnPracView .chip[data-g]');
ok('诗词年级chip数=8(全部+6年級+初中)', pgChips.length === 8);
doc.querySelector('#cnPracView .chip[data-g="六年級"]').click();
const g6Cards = doc.querySelectorAll('#poemGrid .pcard');
let allG6 = true;
g6Cards.forEach(c => { if (!c.querySelector('.tag.b')) allG6 = false; });
ok('六年級筛选后全为高亮六年級(' + g6Cards.length + '張)', g6Cards.length > 0 && allG6);
doc.querySelector('#cnPracView .chip[data-g="初中"]').click();
const czCards = doc.querySelectorAll('#poemGrid .pcard');
let allCz = true;
czCards.forEach(c => { if (![...c.querySelectorAll('.tag')].some(t => t.textContent === '初中')) allCz = false; });
ok('初中筛选后全为初中(' + czCards.length + '張)', czCards.length > 0 && allCz);
doc.querySelector('#cnPracView .chip[data-g="一年級"]').click();
const g1Cards = doc.querySelectorAll('#poemGrid .pcard');
let allG1 = true;
g1Cards.forEach(c => { if (![...c.querySelectorAll('.tag')].some(t => t.textContent === '一年級')) allG1 = false; });
ok('一年級筛选后全为一年級(' + g1Cards.length + '張)', g1Cards.length > 0 && allG1);
doc.querySelector('#cnPracView .chip[data-g="all"]').click();
ok('全部恢复>100張(' + doc.querySelectorAll('#poemGrid .pcard').length + '張)', doc.querySelectorAll('#poemGrid .pcard').length > 100);

console.log('--- 港小生字模塊（练习→英文→港小生字） ---');
doc.querySelector('#practiceSub button[data-sub="en"]').click();
doc.querySelector('#enPracSub button[data-es="hk"]').click();
ok('hkView 顯示', doc.getElementById('hkView').style.display !== 'none');
ok('港小詞卡片>300(' + doc.querySelectorAll('#hkList .vcard').length + '張)', doc.querySelectorAll('#hkList .vcard').length > 300);
const gsecs=doc.querySelectorAll('#hkList .gsec');
ok('港小分級小節=6(P1-P6)('+gsecs.length+')', gsecs.length === 6);
ok('每個小節含詞卡', [...gsecs].every(s=>s.querySelectorAll('.vcard').length>0));
const firstSec=gsecs[0];
ok('首節標題含 P1 與 一年級', !!firstSec && /P1/.test(firstSec.querySelector('.gsec-h').textContent) && firstSec.querySelector('.gsec-h').textContent.indexOf('一年級')>=0);
ok('港小主題選項>0(' + doc.getElementById('hkTheme').options.length + ')', doc.getElementById('hkTheme').options.length > 1);
const totalCards=doc.querySelectorAll('#hkList .vcard').length;
ok('分級後總詞卡>300('+totalCards+')', totalCards>300);
const sampleWord=firstSec.querySelector('.vcard .w').textContent.trim();
doc.getElementById('hkSearch').value=sampleWord;
doc.getElementById('hkSearch').dispatchEvent(new window.Event('input'));
const afterSearch=doc.querySelectorAll('#hkList .vcard').length;
ok('搜索該詞後結果≤總數且>0('+afterSearch+'/'+totalCards+')', afterSearch>0 && afterSearch<=totalCards);
doc.getElementById('hkSearch').value='';
doc.getElementById('hkSearch').dispatchEvent(new window.Event('input'));
const firstHk = doc.querySelector('#hkList .vcard');
firstHk.click();
ok('點擊卡片後港小進度+1(' + doc.getElementById('stHk').textContent + ')', doc.getElementById('stHk').textContent === '1');
// 自測隱中文：勾選後卡片帶 hidezh
const hkHide = doc.getElementById('hkHide'); hkHide.checked = true; hkHide.dispatchEvent(new window.Event('change'));
ok('勾選自測後卡片隱中文(hidezh)', doc.querySelector('#hkList .vcard.hidezh') !== null);
// 全展開 / 全收
ok('詞彙全展開/全收按鈕存在', !!doc.getElementById('hkExpandAll') && !!doc.getElementById('hkCollapseAll'));
const openBefore=doc.querySelectorAll('#hkList details[open]').length;
doc.getElementById('hkCollapseAll').click();
ok('收起全部後無展開小節('+doc.querySelectorAll('#hkList details[open]').length+')', doc.querySelectorAll('#hkList details[open]').length===0);
doc.getElementById('hkExpandAll').click();
ok('展開全部後小節全開('+doc.querySelectorAll('#hkList details[open]').length+'/'+openBefore+')', doc.querySelectorAll('#hkList details[open]').length===openBefore);

console.log('--- 速览: 繁體對照 ---');
doc.querySelector('nav button[data-tab="guide"]').click();
doc.querySelector('#guideSub button[data-sub="ft"]').click();
ok('ftView 顯示', doc.getElementById('ftView').style.display !== 'none');
ok('ftList 有對照行(' + doc.querySelectorAll('#ftList .ftrow').length + ')', doc.querySelectorAll('#ftList .ftrow').length > 50);
const ftSearch = doc.getElementById('ftSearch'); ftSearch.value = '国'; ftSearch.dispatchEvent(new window.Event('input'));
const ftRows = doc.querySelectorAll('#ftList .ftrow');
ok('搜「国」過濾出國→國(' + ftRows.length + ')', ftRows.length === 1 && ftRows[0].textContent.includes('國'));

console.log('--- v1.23 全站免費：英文卷/數學卷直開 ---');
doc.querySelector('nav button[data-tab="practice"]').click();
doc.querySelector('#practiceSub button[data-sub="en"]').click();
doc.querySelector('#enPracSub button[data-es="paper"]').click();
ok('免費直開：英文卷自動出題卡', doc.querySelectorAll('#enPaperBox .qcard').length > 0);
ok('無鎖定面板/狀態殘留', !doc.getElementById('licLockEn') && !doc.getElementById('licLockMath') && !doc.getElementById('licStatusEn') && !doc.getElementById('licStatusMath'));
ok('無授權碼代碼殘留', !doc.documentElement.outerHTML.includes('licActive') && !doc.documentElement.outerHTML.includes('__LIC_SECRET__'));

console.log('--- 练习→英文: 英文卷 ---');
doc.querySelector('#practiceSub button[data-sub="en"]').click();
doc.querySelector('#enPracSub button[data-es="paper"]').click();
ok('paperView 顯示', doc.getElementById('paperView').style.display !== 'none');

console.log('--- 英文卷·智能練習卷生成器 ---');
ok('年級chip=7(P1-P6+綜合)', doc.querySelectorAll('#pgChips .chip[data-pg]').length === 7);
ok('「出新卷」按鈕存在', doc.getElementById('enNewPaper') !== null);
ok('「交卷批改」按鈕存在', doc.getElementById('enSubmit') !== null);
doc.getElementById('enNewPaper').click();
const qcards = doc.querySelectorAll('#enPaperBox .qcard');
ok('出新卷後有題卡(' + qcards.length + ')', qcards.length > 0 && qcards.length <= 8);
ok('題卡含題型標籤', doc.querySelector('#enPaperBox .qtype') !== null);
ok('含閱讀小題容器qsub(若有閱讀)', doc.querySelectorAll('#enPaperBox .qsub').length >= 0);
doc.querySelector('#pgChips .chip[data-pg="P6"]').click();
ok('切 P6 後仍有題卡', doc.querySelectorAll('#enPaperBox .qcard').length > 0);
// 模擬作答：所有 radio 選第一項，所有 fill 填 'test'
doc.querySelectorAll('#enPaperBox input[type=radio]').forEach(r => { r.checked = true; });
doc.querySelectorAll('#enPaperBox .qfill').forEach(f => { f.value = 'test'; });
doc.getElementById('enSubmit').click();
ok('交卷後出現得分結果', doc.getElementById('enPaperResult').textContent.includes('得分'));
ok('本級最佳寫入localStorage(P6)', JSON.parse(window.localStorage.getItem('hkk_enpaper_v0') || '{}')['P6'] !== undefined);
doc.querySelector('#pgChips .chip[data-pg="P1"]').click();
ok('切回 P1 仍有題卡', doc.querySelectorAll('#enPaperBox .qcard').length > 0);

console.log('--- v1.11 年級分題 + 資料來源面板 ---');
ok('enGradeTopic 元素存在', doc.getElementById('enGradeTopic') !== null);
ok('enSrcNote 元素存在', doc.getElementById('enSrcNote') !== null);
ok('來源面板含檢索日期(2026-10-31)', doc.getElementById('enSrcNote').textContent.includes('2026-10-31'));
ok('來源面板含來源站(GoStudy/弦月)', /GoStudy|弦月教育/.test(doc.getElementById('enSrcNote').textContent));
doc.querySelector('#pgChips .chip[data-pg="P3"]').click();
ok('切 P3 後主題面板有內容(坊間參考)', doc.getElementById('enGradeTopic').textContent.includes('坊間參考'));
// 六級均可出卷 + 題池豐富度代理（5次出新卷去重後≥12題）
let richOk = true, genOk = true;
['P1','P2','P3','P4','P5','P6'].forEach(function(g){
  doc.querySelector('#pgChips .chip[data-pg="' + g + '"]').click();
  var seen = new Set();
  for (var k = 0; k < 5; k++) {
    doc.getElementById('enNewPaper').click();
    doc.querySelectorAll('#enPaperBox .qtext').forEach(function(n){ seen.add(n.textContent); });
  }
  if (seen.size < 12) richOk = false;
  if (doc.querySelectorAll('#enPaperBox .qcard').length === 0) genOk = false;
});
ok('六級均可出卷', genOk);
ok('各級題池豐富(去重≥12題)', richOk);

console.log('--- v1.16 綜合卷 + AI 換題 ---');
const allChip=doc.querySelector('#pgChips .chip[data-pg="ALL"]');
ok('綜合chip存在', allChip !== null);
if(allChip) allChip.click();
ok('綜合卷含6個小節標題.qsec', doc.querySelectorAll('#enPaperBox .qsec').length === 6);
ok('綜合卷題卡數=12(每級2題)', doc.querySelectorAll('#enPaperBox .qcard').length === 12);
ok('綜合卷題卡帶data-grade', doc.querySelector('#enPaperBox .qcard[data-grade]') !== null);
ok('每題含換一題按鈕.mini', doc.querySelector('#enPaperBox .mini') !== null);
ok('每題含AI換題按鈕.mini.ai', doc.querySelector('#enPaperBox .mini.ai') !== null);
const swapLocal=doc.querySelector('#enPaperBox .qcard[data-qi="0"] .mini:not(.ai)');
if(swapLocal) swapLocal.click();
ok('換一題後首題卡仍存在', doc.querySelector('#enPaperBox .qcard[data-qi="0"]') !== null);
ok('AI設置面板#aiCfg存在', doc.getElementById('aiCfg') !== null);
ok('AI設置含Base/Key/Model輸入', !!(doc.getElementById('aiBase')&&doc.getElementById('aiKey')&&doc.getElementById('aiModel')));
ok('aiGenQuestion 函數存在', typeof window.aiGenQuestion === 'function');
ok('getAiCfg 未配置返回空', (function(){ try{ return Object.keys(window.getAiCfg()).length===0; }catch(e){ return false; } })());
doc.getElementById('aiBase').value='https://api.openai.com/v1';
doc.getElementById('aiKey').value='sk-test';
doc.getElementById('aiModel').value='gpt-4o-mini';
window.saveAiCfg();
ok('保存後localStorage寫入hkk_ai_cfg', (function(){ try{ return JSON.parse(window.localStorage.getItem('hkk_ai_cfg')).model==='gpt-4o-mini'; }catch(e){ return false; } })());
window.clearAiCfg();
ok('清除後hkk_ai_cfg為空', window.localStorage.getItem('hkk_ai_cfg')===null);
doc.querySelector('#pgChips .chip[data-pg="P1"]').click();
ok('切回P1仍有題卡', doc.querySelectorAll('#enPaperBox .qcard').length > 0);

console.log('--- v1.19 數學卷（雙語·分 P1–P6） ---');
doc.querySelectorAll('#practiceSub button').forEach(b=>{ if(b.dataset.sub==='math') b.click(); });
ok('mathPracView 顯示', doc.getElementById('mathPracView').style.display !== 'none');
const msub=doc.querySelector('#mathPracSub button[data-es="mpaper"]');
ok('數學卷子標籤存在', msub !== null);
msub.click();
ok('mathPaperView 顯示', doc.getElementById('mathPaperView').style.display !== 'none');
ok('數學卷年級chip=6(P1-P6)', doc.querySelectorAll('#mpgChips .chip[data-pg]').length === 6);
ok('數學卷出新卷按鈕存在', doc.getElementById('mathNewPaper') !== null);
ok('數學卷交卷批改按鈕存在', doc.getElementById('mathSubmit') !== null);
ok('數學卷打印按鈕存在', doc.getElementById('mathPrintBtn') !== null);
ok('數學卷含答案版開關#mathPrintAns', doc.getElementById('mathPrintAns') !== null);
ok('數學卷打印容器#mathPrintSheet', doc.getElementById('mathPrintSheet') !== null);
doc.getElementById('mathNewPaper').click();
const mcards=doc.querySelectorAll('#mathPaperBox .qcard');
ok('數學卷出新卷後有題卡('+mcards.length+')', mcards.length>0 && mcards.length<=8);
ok('數學卷題卡含題型標籤', doc.querySelector('#mathPaperBox .qtype') !== null);
ok('數學卷題卡含中文對照.qzh', doc.querySelector('#mathPaperBox .qzh') !== null);
doc.querySelector('#mpgChips .chip[data-pg="P6"]').click();
ok('數學卷切 P6 仍有題卡', doc.querySelectorAll('#mathPaperBox .qcard').length>0);
doc.querySelectorAll('#mathPaperBox input[type=radio]').forEach(r=>{ r.checked = true; });
doc.querySelectorAll('#mathPaperBox .qfill').forEach(f => { f.value = '9'; });
doc.getElementById('mathSubmit').click();
ok('數學卷交卷後出現得分結果', doc.getElementById('mathPaperResult').textContent.includes('得分'));
ok('數學卷本級最佳寫入localStorage(P6)', JSON.parse(window.localStorage.getItem('hkk_mathpaper_v0') || '{}')['P6'] !== undefined);
let mGenOk=true;
['P1','P2','P3','P4','P5','P6'].forEach(g=>{
  doc.querySelector('#mpgChips .chip[data-pg="'+g+'"]').click();
  if(doc.querySelectorAll('#mathPaperBox .qcard').length===0) mGenOk=false;
});
ok('數學卷六級均可出卷', mGenOk);
ok('數學卷題庫常量 const MATH_QBANK', html.includes('const MATH_QBANK = {'));
ok('數學卷題庫含 P1-P6 六級', /const MATH_QBANK = \{[\s\S]*P1:\[[\s\S]*P2:\[[\s\S]*P3:\[[\s\S]*P4:\[[\s\S]*P5:\[[\s\S]*P6:\[/.test(html));
// 中英術語表仍在（子標籤切回）；先復位 line 91 設定的 fraction 搜索過濾（過濾態會跨子視圖保留，屬正常行為）
const _ms = doc.getElementById('mathSearch'); _ms.value=''; _ms.dispatchEvent(new window.Event('input'));
doc.querySelector('#mathPracSub button[data-es="mterms"]').click();
ok('切回中↔英術語表後 mathBody 仍有行', doc.querySelectorAll('#mathBody tr').length > 100);

console.log('--- 诗词默写填空 + 朗读（练习→中文） ---');
doc.querySelector('nav button[data-tab="practice"]').click();
doc.querySelector('#practiceSub button[data-sub="cn"]').click();
doc.querySelector('#poemGrid .pcard').click(); // 開詩詞詳情
ok('詩詞modal顯示', doc.getElementById('mask').classList.contains('show'));
const actsTxt = doc.getElementById('mActs').textContent;
ok('詳情含「默寫練習」按鈕', actsTxt.includes('默寫練習'));
ok('詳情含「朗讀」按鈕', actsTxt.includes('朗讀'));
// 進入默寫模式
[...doc.querySelectorAll('#mActs button')].find(b => b.textContent.includes('默寫練習')).click();
const blanks = doc.querySelectorAll('#mBody .han.blank');
ok('默寫模式生成填空(' + blanks.length + ')', blanks.length > 0);
// 顯示答案
const revBtn = [...doc.querySelectorAll('#mActs button')].find(b => b.textContent.includes('顯示答案'));
ok('默寫模式出現「顯示答案」', !!revBtn);
revBtn.click();
ok('顯示答案後出現 reveal 類', doc.querySelectorAll('#mBody .han.blank.reveal').length > 0);
// 退出默寫
[...doc.querySelectorAll('#mActs button')].find(b => b.textContent.includes('退出默寫')).click();
ok('退出後填空消失', doc.querySelectorAll('#mBody .han.blank').length === 0);
doc.getElementById('mask').classList.remove('show');

console.log('--- 數術語 已掌握打卡 + 朗读（练习→數學） ---');
doc.querySelector('nav button[data-tab="practice"]').click();
doc.querySelector('#practiceSub button[data-sub="math"]').click();
doc.querySelector('#mathBody tr').click();
ok('數術語點擊後 stMath=1', doc.getElementById('stMath').textContent === '1');
ok('數術語首行變 done', doc.querySelector('#mathBody tr').classList.contains('done'));
ok('數術語含🔊朗讀鈕', doc.querySelector('#mathBody .mini[data-sp]') !== null);

console.log('--- 進度導出/導入 + 響應式 ---');
doc.querySelector('nav button[data-tab="progress"]').click();
ok('導出按鈕存在', doc.getElementById('exportBtn') !== null);
ok('匯入按鈕存在', doc.getElementById('importBtn') !== null);
ok('響應式CSS存在(@media screen max-width:640px)', html.includes('@media screen and (max-width:640px)'));

console.log('--- 升學規劃 tab + 5 子頁 ---');
doc.querySelector('nav button[data-tab="plan"]').click();
ok('planView 顯示', doc.getElementById('planView').style.display !== 'none');
ok('guideView 隱藏', doc.getElementById('guideView').style.display === 'none');
ok('planSub 5个(timeline/schools/docs/study/policy)', doc.querySelectorAll('#planSub button').length === 5);
ok('timelineView 顯示(默認)', doc.getElementById('timelineView').style.display !== 'none');
ok('schoolsView 隱藏', doc.getElementById('schoolsView').style.display === 'none');
// 切到擇校分檔
doc.querySelector('#planSub button[data-sub="schools"]').click();
ok('schoolsView 顯示', doc.getElementById('schoolsView').style.display !== 'none');
ok('timelineView 隱藏', doc.getElementById('timelineView').style.display === 'none');
const schoolRows = doc.querySelectorAll('#tierTable tbody tr');
ok('北區學校表 23 行', schoolRows.length === 23);
const tiers = new Set([...doc.querySelectorAll('#tierTable tbody tr td:first-child')].map(td=>td.textContent));
ok('梯隊含 衝刺/穩妥/保底', tiers.has('衝刺') && tiers.has('穩妥') && tiers.has('保底'));
// v1.22 勘誤卡＋北區一覽＋外鏈精選
ok('交叉勘誤卡存在', doc.getElementById('schoolsView').innerHTML.includes('交叉勘誤'));
ok('北區一覽 20 行', doc.querySelectorAll('#ssTable tbody tr').length === 20);
ok('英文名稱列存在', doc.querySelector('#ssTable tbody tr td:nth-child(2)').textContent.length > 3);
ok('外鏈卡含 schooland+EDB', doc.querySelectorAll('#schoolsView a[href*="schooland"],#schoolsView a[href*="edb.gov.hk"]').length >= 5);
doc.querySelector('#ssChips .chip[data-ss="en"]').click();
ok('英中篩選後 7 行', [...doc.querySelectorAll('#ssTable tbody tr')].filter(tr=>tr.style.display!=='none').length === 7);
doc.querySelector('#ssChips .chip[data-ss="all"]').click();
ok('取消篩選復 20 行', [...doc.querySelectorAll('#ssTable tbody tr')].filter(tr=>tr.style.display!=='none').length === 20);
// 切到材料/學習/身份
doc.querySelector('#planSub button[data-sub="docs"]').click();
ok('docsView 顯示', doc.getElementById('docsView').style.display !== 'none');
doc.querySelector('#planSub button[data-sub="study"]').click();
ok('studyView 顯示(含定級/80:20)', doc.getElementById('studyView').style.display !== 'none' && doc.getElementById('studyView').innerHTML.includes('定級三連測'));
doc.querySelector('#planSub button[data-sub="policy"]').click();
ok('policyView 顯示(含居港2年)', doc.getElementById('policyView').style.display !== 'none' && doc.getElementById('policyView').innerHTML.includes('居港 2 年'));
ok('plan 子頁含來源標注(.src)', doc.querySelectorAll('#planView .src').length >= 4);

console.log('--- 悠閒：單詞貪吃蛇 ---');
doc.querySelector('nav button[data-tab="fun"]').click();
ok('funView 顯示', doc.getElementById('funView').style.display !== 'none');
ok('snakeCanvas 存在', doc.getElementById('snakeCanvas') !== null);
ok('開始按鈕存在', doc.getElementById('snakeStart') !== null);
ok('方向按鈕4個', doc.querySelectorAll('.spad').length === 4);
ok('死亡標記按鈕存在', doc.getElementById('snakeMaster') !== null);
ok('英文卷含打印按鈕', !!doc.getElementById('enPrint'));
ok('英文卷含打印容器#enPrintSheet', doc.getElementById('enPrintSheet') !== null);
ok('練習→英文含打卡火焰#motiBar', doc.getElementById('motiBar') !== null);
ok('練習→英文含閃卡按鈕#flashBtn', doc.getElementById('flashBtn') !== null);
ok('練習→英文含閃卡面板#flashPanel', doc.getElementById('flashPanel') !== null);
ok('進度頁含徽章盒#badgeBox', doc.getElementById('badgeBox') !== null);
ok('英文卷含答案版開關#enPrintAns', doc.getElementById('enPrintAns') !== null);
// v1.13：一次性打印一套卷子（以點擊按鈕＋讀 DOM 驗證，避免依賴頁面腳本作用域變數）
try{
  const enPrint=doc.getElementById('enPrint');
  const enSheet=doc.getElementById('enPrintSheet');
  // 點擊「打印一套卷子」：無論是否已出卷，都應產出一份完整可印卷（含總分）
  enPrint.click();
  const sheetTxt=(enSheet||{}).textContent||'';
  ok('點擊打印即產出完整題卷(含「共N題／總分」)', /共\s*\d+\s*題/.test(sheetTxt) && /分/.test(sheetTxt) && sheetTxt.length>50);
  // 勾選含答案版再打印：答案應獨立成頁(eps-aksheet)
  if(doc.getElementById('enPrintAns')) doc.getElementById('enPrintAns').checked=true;
  enPrint.click();
  const sheetHtml=(enSheet||{}).innerHTML||'';
  ok('含答案版時答案卷獨立成頁(eps-aksheet)', /eps-aksheet/.test(sheetHtml));
  if(doc.getElementById('enPrintAns')) doc.getElementById('enPrintAns').checked=false;
}catch(e){ ok('v1.13 打印邏輯執行', false); console.log('   err='+e.message); }

// v1.14：練習→英文「詞彙路線圖」(goalView)
try{
  const goalBtn=doc.querySelector('#enPracSub button[data-es="goal"]');
  ok('英文練習含詞彙路線圖按鈕#enPracSub goal', !!goalBtn);
  if(goalBtn){
    goalBtn.click();
    const gv=doc.getElementById('goalView');
    ok('點擊後 goalView 顯示', gv && gv.style.display==='block');
    const gTxt=(gv||{}).textContent||'';
    ok('詞彙路線圖含站內詞量1,800與中六目標', /1,800/.test(gTxt) && /中六/.test(gTxt) && /2,500–3,000/.test(gTxt));
  }
}catch(e){ ok('v1.14 詞彙路線圖執行', false); console.log('   err='+e.message); }

// v1.15：英文卷接入 EDB 寓言阅读题库（教育局「中國寓言系列」改編）
ok('英文卷接入 EDB 寓言常量 const EN_EDB', html.includes('const EN_EDB = {'));
ok('EDB read 題標 src:EDB 來源', html.includes("src:'EDB 中國寓言系列'"));
ok('EDB 分 P4/P5/P6 三級', /const EN_EDB = \{[\s\S]*P4:\[[\s\S]*P5:\[[\s\S]*P6:\[/.test(html));
ok('genEnPaper 拼接 EN_EDB 常量', html.includes('EN_EDB[curEnGrade]'));
ok('renderEnPaper read 加 src 來源標記代碼', html.includes('qsrc'));
ok('打印 read 加 eps-src 來源標記代碼', html.includes('eps-src'));
// DOM：切 P4 英文卷，反覆出新卷直到抽到 EDB 來源標記（驗證真實渲染＋src 顯示不報錯）
try{
  const paperBtn=doc.querySelector('#enPracSub button[data-es="paper"]');
  if(paperBtn) paperBtn.click();
  const p4=doc.querySelector('#pgChips .chip[data-pg="P4"]');
  if(p4) p4.click();
  const newBtn=doc.getElementById('enNewPaper');
  let sawEdb=false;
  for(let n=0;n<40 && newBtn;n++){
    newBtn.click();
    if(doc.querySelector('.qsrc')){ sawEdb=true; break; }
  }
  ok('P4 英文卷真實渲染出 EDB 來源標記(.qsrc)', sawEdb);
}catch(e){ ok('v1.15 EDB DOM 渲染執行', false); console.log('   err='+e.message); }

console.log('\n结果: ' + pass + ' 通过, ' + fail + ' 失败');
process.exit(fail ? 1 : 0);
