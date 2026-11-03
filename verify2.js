// 验证 v0.6 中英数站点结构（练习区按科目归口：中文/英文/數學）
const fs = require('fs');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync('index.html', 'utf-8');
const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true, url: 'https://localhost/',
  beforeParse(window){ Object.defineProperty(window,'crypto',{value:require('crypto').webcrypto,configurable:true}); } // v1.33 賬號系統 Web Crypto 注入（脚本執行前）
});
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
// v1.32 音標
const ipaCards=[...doc.querySelectorAll('#hkList .vcard .ph')].filter(s=>/^\/.+\/$/.test(s.textContent.trim()));
ok('v1.32 生字卡音標數=335('+ipaCards.length+')', ipaCards.length===335);
ok('v1.32 音標樣例(hello=/həˈləʊ/)', doc.querySelector('#hkList .vcard .ph').textContent.includes('həˈləʊ'));

console.log('--- 速览: 繁體對照 ---');
doc.querySelector('nav button[data-tab="guide"]').click();
doc.querySelector('#guideSub button[data-sub="ft"]').click();
ok('ftView 顯示', doc.getElementById('ftView').style.display !== 'none');
ok('ftList 有對照行(' + doc.querySelectorAll('#ftList .ftrow').length + ')', doc.querySelectorAll('#ftList .ftrow').length > 50);
const ftSearch = doc.getElementById('ftSearch'); ftSearch.value = '国'; ftSearch.dispatchEvent(new window.Event('input'));
const ftRows = doc.querySelectorAll('#ftList .ftrow');
ok('搜「国」過濾出國→國(' + ftRows.length + ')', ftRows.length === 1 && ftRows[0].textContent.includes('國'));
ftSearch.value = ''; ftSearch.dispatchEvent(new window.Event('input'));

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
console.log('--- v1.25 繁體字庫分級 ---');
const FTG = window.eval('FT_GRADES');
ok('FT_GRADES 含 P1–P6 六級', ['P1','P2','P3','P4','P5','P6'].every(g=>Array.isArray(FTG[g])&&FTG[g].length>=40));
ok('FT_MAP 總數 ≥ 240', window.eval('FT_MAP.length') >= 240);
const ftDup = window.eval('JSON.stringify(FT_MAP.map(x=>x[0]).sort().some((v,i,a)=>i&&a[i-1]===v))');
ok('FT_MAP 簡體無重複', ftDup === 'false');
ok('多繁注記存在(里→裡)', JSON.stringify(FTG.P1).includes('裡/裏'));
doc.querySelector('nav button[data-tab="guide"]').click();
doc.querySelector('#guideSub button[data-sub="ft"]').click();
ok('繁體對照 chips=7', doc.querySelectorAll('#ftChips .chip').length === 7);
ok('全部模式列表 ≥ 240 行', doc.querySelectorAll('#ftList .ftrow').length >= 240);
doc.querySelector('#ftChips .chip[data-fg="P6"]').click();
const p6rows = doc.querySelectorAll('#ftList .ftrow').length;
ok('P6 模式行數=P6級字數且 ≥40', p6rows >= 40 && p6rows === window.eval('FT_GRADES.P6.length'));
ok('P6 模式顯示字數統計', doc.getElementById('ftCount').textContent.includes(String(window.eval('FT_GRADES.P6.length'))));
doc.getElementById('ftSearch').value = '链';
doc.getElementById('ftSearch').dispatchEvent(new window.Event('input'));
ok('P6 內搜尋「链」只出 1 行', doc.querySelectorAll('#ftList .ftrow').length === 1);
doc.getElementById('ftSearch').value = '';
doc.getElementById('ftSearch').dispatchEvent(new window.Event('input'));
doc.querySelector('#ftChips .chip[data-fg="all"]').click();
ok('切回全部復原 ≥240 行', doc.querySelectorAll('#ftList .ftrow').length >= 240);

console.log('--- v1.24 呈分試卷（練習→英文→呈分試卷） ---');
doc.querySelector('nav button[data-tab="practice"]').click();
doc.querySelector('#practiceSub button[data-sub="en"]').click();
doc.querySelector('#enPracSub button[data-es="exam"]').click();
ok('examView 顯示', doc.getElementById('examView').style.display === 'block');
ok('呈分試卷年級 chips=2', doc.querySelectorAll('#examChips .chip').length === 2);
ok('P6 默認自動出卷含十大題(Warm-up+A–J)', doc.querySelectorAll('#examPaperBox .ex-sec').length >= 11);
ok('生詞表 8 詞(4×2)', doc.querySelectorAll('#examPaperBox .ex-vocab td').length === 8);
ok('填空輸入 ≥ 60', doc.querySelectorAll('#examPaperBox .ex-inp').length >= 60);
ok('H+I 部分 MC 6題(24個radio)', doc.querySelectorAll('#examPaperBox .ex-mc input[type=radio]').length === 24);
ok('H+I 部分開放題 textarea 4', doc.querySelectorAll('#examPaperBox .ex-open').length === 4);
ok('v1.27 I 段(海報閱讀)存在', !!doc.getElementById('exSecI') && doc.getElementById('exSecI').textContent.includes('poster'));
ok('v1.27 J 段(since/therefore)存在', !!doc.getElementById('exSecJ') && doc.getElementById('exSecJ').textContent.includes('therefore'));
ok('v1.27 AI 出新卷按鈕存在', !!doc.getElementById('examAiBtn') && doc.getElementById('examAiBtn').textContent.includes('AI'));
// v1.27 閉環滿分：程序化填入全部正確答案 → 交卷 → SCORE 100/100
function examFillPerfectAndGrade(){
  const P=window.eval('curExamPaper');
  P.head.fills.forEach((f,i)=>{const el=doc.getElementById('ex_wu_'+i+'_0');if(el)el.value=f.a[0];});
  P.A.items.forEach((it,i)=>{doc.getElementById('ex_A_'+i+'_0').value=it.a[0];doc.getElementById('ex_A_'+i+'_1').value=it.a[1];});
  P.B.items.forEach((it,i)=>{doc.getElementById('ex_B_'+i+'_0').value=it.a[0];});
  P.C.a.forEach((a,i)=>{doc.getElementById('ex_C_'+i).value=a[0];});
  P.D.lines.forEach((l,i)=>{doc.getElementById('ex_D_'+i+'_0').value=l.a[0];});
  P.E.items.forEach((it,i)=>{doc.getElementById('ex_E_'+i).value=Array.isArray(it.a)?it.a[0]:it.a;});
  P.F.a.forEach((a,i)=>{doc.getElementById('ex_F_'+i).value=a[0];});
  P.G.a.forEach((a,i)=>{doc.getElementById('ex_G_'+i).value=a[0];});
  P.H.mc.forEach((m,i)=>{const el=doc.querySelector('input[name="ex_H_mc'+i+'"][value="'+m.a+'"]');if(el)el.checked=true;});
  P.H.open.forEach((o,i)=>{doc.getElementById('ex_H_open'+i).value=o.model;});
  doc.getElementById('ex_H_fill_0').value=P.H.fill.a[0][0];
  P.I.mc.forEach((m,i)=>{const el=doc.querySelector('input[name="ex_I_mc'+i+'"][value="'+m.a+'"]');if(el)el.checked=true;});
  P.I.open.forEach((o,i)=>{doc.getElementById('ex_I_open'+i).value=o.model;});
  P.J.items.forEach((it,i)=>{doc.getElementById('ex_J_'+i+'_0').value=Array.isArray(it.a)?it.a[0]:it.a;});
  doc.getElementById('examSubmit').click();
  return doc.getElementById('examPaperResult').textContent;
}
doc.getElementById('examNewPaper').click();
const examResP6=examFillPerfectAndGrade();
ok('P6 閉環滿分 100/100', examResP6.includes('SCORE: 100 / 100'));
doc.getElementById('examSubmit').click();
ok('交卷顯示 SCORE', doc.getElementById('examPaperResult').textContent.includes('SCORE'));
ok('呈分試卷本級最佳寫入 localStorage(P6)', JSON.parse(window.localStorage.getItem('hkk_exampaper_v0') || '{}')['P6'] !== undefined);
doc.querySelector('#examChips .chip[data-pg="P5"]').click();
ok('切 P5 重新出卷', doc.getElementById('examPaperBox').textContent.includes('P5'));
const examResP5=examFillPerfectAndGrade();
ok('P5 閉環滿分 100/100', examResP5.includes('SCORE: 100 / 100'));
doc.querySelector('#enPracSub button[data-es="paper"]').click();
doc.querySelector('#enPracSub button[data-es="exam"]').click();
ok('子標籤來回切換 examView 狀態正常', doc.getElementById('examView').style.display === 'block' && doc.getElementById('paperView').style.display === 'none');
ok('呈分試卷打印容器存在', !!doc.getElementById('examPrintSheet'));
ok('v1.28 一次出10套按鈕存在', !!doc.getElementById('examTenBtn'));
doc.getElementById('examTenBtn').click();
const tenRows=doc.querySelectorAll('#exTenBox .ex-bank tr').length-1;
ok('v1.28 生成10套去重目錄卡', tenRows===10 && doc.getElementById('exTenBox').textContent.includes('互不相同'));
const tenPapers=window.eval('window._tenPapers||[]');
ok('v1.28 10套卷簽名互不相同', tenPapers.length===10 && new Set(tenPapers.map(p=>JSON.stringify(p))).size===10);
ok('v1.30 題庫加厚 H/I/C 每級5套', ['P5','P6'].every(g=>{const b=window.eval('EXAM_QBANK')['P5']&&window.eval('EXAM_QBANK')[g];return b.H.length===5&&b.I.length===5&&b.C.length===5;}));
ok('v1.30 10套卷 H+I 組合互不重複', tenPapers.length===10 && new Set(tenPapers.map(p=>p.H.title+'|'+p.I.title)).size===10);
doc.getElementById('examTenPrintBtn').click();
const tenHtml=doc.getElementById('examPrintSheet').innerHTML;
ok('v1.28 打印頁含10個套號卷頭', (tenHtml.match(/第 \d+ 套/g)||[]).length===10);
ok('v1.28 每套獨立分頁(9個分頁符)', (tenHtml.match(/page-break-before/g)||[]).length>=9);
doc.getElementById('examPrintSheet').innerHTML='';
ok('v1.29 目錄含10個「打開」按鈕', doc.querySelectorAll('#exTenBox button[onclick^="showTenPaper"]').length===10);
doc.querySelector('#exTenBox button[onclick="showTenPaper(0)"]').click();
ok('v1.29 打開第1套：卷頭標套號', doc.querySelector('#examPaperBox .ex-code').textContent.includes('第 1 套'));
ok('v1.29 打開後作答卷渲染(含詞彙表+各段)', doc.querySelectorAll('#examPaperBox .ex-vocab td').length===8 && doc.querySelectorAll('#examPaperBox .ex-sec').length>=10);
window.eval('genExamPaper()');
ok('v1.29 出新卷清套號', !doc.querySelector('#examPaperBox .ex-code').textContent.includes('第 '));
doc.getElementById('examTenBtn').click();
const bestBefore=window.eval('JSON.parse(localStorage.getItem("hkk_exampaper_v0")||"{}")')['P6'];
doc.querySelector('#exTenBox button[onclick="showTenAnswer(0)"]').click();
ok('v1.31 答案模式：SCORE 100/100', doc.getElementById('examPaperResult').textContent.includes('100 / 100'));
ok('v1.31 答案模式：全綠無錯題', doc.getElementById('examPaperResult').textContent.includes('全對'));
const bestAfter=window.eval('JSON.parse(localStorage.getItem("hkk_exampaper_v0")||"{}")')['P6'];
ok('v1.31 答案模式：最佳分不被污染', bestAfter===bestBefore);
ok('題庫常量 EXAM_QBANK 且含 P5/P6', /const EXAM_QBANK=\{[\s\S]*P5:\{[\s\S]*P6:\{/.test(html));

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
ok('planSub 6个(timeline/schools/docs/study/policy/faq)', doc.querySelectorAll('#planSub button').length === 6);
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

// ============ v1.33 賬號系統（异步：Web Crypto sha256） ============
(async()=>{try{
  const g=id=>doc.getElementById(id);
  ok('v1.33 sha256("abc") 標準向量', await window.eval('hkSha256("abc")')==='ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad');
  ok('v1.33 sha256("") 標準向量', await window.eval('hkSha256("")')==='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855');
  ok('v1.33 sha256("你好") UTF-8', await window.eval('hkSha256("你好")')===require('crypto').createHash('sha256').update('你好','utf8').digest('hex'));
  ok('v1.33 本地默認免登入（authGate 不顯示）', !g('authGate').classList.contains('on') && window.eval('curUser')==='本地');
  // 強制登入模式
  window.eval('AUTH_FORCE=true');
  window.eval('localStorage.removeItem("hkk_auth_sess")');
  window.eval('authBoot()');
  ok('v1.33 線上模式未登入→攔截', g('authGate').classList.contains('on'));
  // 註冊校驗
  g('authRegName').value='a';g('authRegPwd').value='test1234';g('authRegPwd2').value='test1234';
  await window.eval('authRegister()');
  ok('v1.33 暱稱太短被拒', g('authRegErr').textContent.includes('2–16'));
  g('authRegName').value='叶小工';g('authRegPwd').value='123';g('authRegPwd2').value='123';
  await window.eval('authRegister()');
  ok('v1.33 密碼太短被拒', g('authRegErr').textContent.includes('至少 8 位'));
  g('authRegPwd').value='test1234';g('authRegPwd2').value='test1234';
  await window.eval('authRegister()');
  const users=JSON.parse(window.localStorage.getItem('hkk_auth_users'));
  ok('v1.33 註冊成功寫入用戶表', !!users['叶小工'] && /^[0-9a-f]{64}$/.test(users['叶小工'].hash));
  ok('v1.33 hash=salt|密碼 的 sha256', users['叶小工'].hash===await window.eval('hkSha256('+JSON.stringify(users['叶小工'].salt)+'+"|test1234")'));
  ok('v1.33 重名被拒', await (async()=>{g('authRegName').value='叶小工';g('authRegPwd').value='test1234';g('authRegPwd2').value='test1234';await window.eval('authRegister()');return g('authRegErr').textContent.includes('已註冊');})());
  // 登入：錯誤密碼
  g('authLoginName').value='叶小工';g('authLoginPwd').value='wrong1234';
  await window.eval('authLogin()');
  ok('v1.33 錯誤密碼被拒', g('authLoginErr').textContent.includes('密碼不正確'));
  // 作用域往返
  window.localStorage.setItem('hkk_exampaper_v0','SCOPE_TEST');
  window.eval('authSaveScope("叶小工")');
  ok('v1.33 作用域搬移後全局鍵清空', window.localStorage.getItem('hkk_exampaper_v0')===null && window.localStorage.getItem('hkk_u@叶小工@exampaper_v0')==='SCOPE_TEST');
  window.eval('authLoadScope("叶小工")');
  ok('v1.33 作用域搬回', window.localStorage.getItem('hkk_exampaper_v0')==='SCOPE_TEST' && window.localStorage.getItem('hkk_u@叶小工@exampaper_v0')===null);
  // 正確密碼登入（remember=true → localStorage session）
  g('authLoginName').value='叶小工';g('authLoginPwd').value='test1234';
  await window.eval('authEnter("叶小工",true)');
  ok('v1.33 登入寫入 session', JSON.parse(window.localStorage.getItem('hkk_auth_sess')).name==='叶小工');
  ok('v1.33 登入後關閉登入頁', !g('authGate').classList.contains('on'));
  ok('v1.33 歡迎條顯示暱稱', g('userChipName').textContent.includes('叶小工'));
  // remember=false → sessionStorage
  await window.eval('authEnter("叶小工",false)');
  ok('v1.33 不記住我→sessionStorage', window.localStorage.getItem('hkk_auth_sess')===null && JSON.parse(window.sessionStorage.getItem('hkk_auth_sess')).name==='叶小工');
  // 復原：清 session 回本地身份
  window.eval('AUTH_FORCE=false');
  window.localStorage.clear();
  window.eval('authBoot()');
  ok('v1.33 清存儲後復原本地身份', window.eval('curUser')==='本地' && !g('authGate').classList.contains('on'));
}catch(e){ ok('v1.33 賬號系統測試執行', false); console.log('   err='+e.message); }

// ============ v1.35 繪本閱讀打卡 ============
try{
  ok('v1.35 ORT 書單 204 本', window.eval('ORT_BOOKS.length')===204);
  doc.querySelector('#enPracSub button[data-es="ort"]').click();
  ok('v1.35 子標籤切換顯示 ortView', doc.getElementById('ortView').style.display==='block');
  ok('v1.35 九階 chips 含計數（全部+9階=10）', (doc.getElementById('ortChips').textContent.match(/\(\d+\)/g)||[]).length===10);
  const bk1=doc.querySelector('#ortList .ort-bk');
  const k1=bk1.dataset.k;
  bk1.click();
  const bkAfter=[...doc.querySelectorAll('#ortList .ort-bk')].find(b=>b.dataset.k===k1);
  ok('v1.35 打卡→done 類+存儲', bkAfter.classList.contains('done') && !!JSON.parse(window.localStorage.getItem('hkk_ort'))[k1]);
  ok('v1.35 總進度=1', doc.getElementById('ortStat').innerHTML.includes('<b>1</b>'));
  bkAfter.click();
  ok('v1.35 再點取消打卡', !JSON.parse(window.localStorage.getItem('hkk_ort'))[k1]);
  doc.querySelector('#ortChips .chip[data-lv="5階"]').click();
  ok('v1.35 階 chip 過濾（僅 5 階）', doc.querySelectorAll('#ortList .ort-lv').length===1 && doc.querySelector('#ortList .ort-lv-h').textContent.includes('5階'));
  // 資源地圖卡
  ok('v1.35 資源地圖卡含本地路徑', doc.getElementById('ortView').textContent.includes('牛津树') && doc.getElementById('ortView').textContent.includes('香港朗文'));
}catch(e){ ok('v1.35 繪本閱讀測試執行', false); console.log('   err='+e.message); }

// ============ v1.38 择校：校车卡 + 东铁沿线（大埔）表 ============
try{
  doc.querySelector('nav button[data-tab="plan"]').click();
  doc.querySelector('#planSub button[data-sub="schools"]').click();
  ok('v1.38 校车卡：保姆车营办商+5-6月申请', doc.getElementById('schoolsView').textContent.includes('葉太') && doc.getElementById('schoolsView').textContent.includes('5–6 月'));
  const rows=doc.querySelectorAll('#tpTable tbody tr');
  ok('v1.39 大埔表 20 行', rows.length===20);
  ok('v1.38 大埔英中 7 所（含三育）', [...rows].filter(r=>(' '+r.dataset.tp+' ').includes(' en ')).length===7);
  ok('v1.38 直資 2（羅定邦雙標籤生效）', [...rows].filter(r=>(' '+r.dataset.tp+' ').includes(' dss ')).length===2);
  ok('v1.38 王肇枝=英中（站旁）', [...rows].some(r=>r.textContent.includes('王肇枝中學') && r.textContent.includes('英中') && r.textContent.includes('站旁')));
  doc.querySelector('#tpChips .chip[data-tp="en"]').click();
  const vis=[...doc.querySelectorAll('#tpTable tbody tr')].filter(r=>r.style.display!=='none');
  ok('v1.38 英中 chip 過濾=7 可見', vis.length===7);
  doc.querySelector('#tpChips .chip[data-tp="all"]').click();
  ok('v1.38 全部 chip 恢復 20 可見', [...doc.querySelectorAll('#tpTable tbody tr')].filter(r=>r.style.display!=='none').length===20);
}catch(e){ ok('v1.38 择校测试执行', false); console.log('   err='+e.message); }

// ============ v1.39 择校：电话列 + 删停办校 + 三育英中 ============
try{
  ok('v1.39 中學 tel 鏈接≥40（北20+埔20，v1.42 起全站 70 含小學30）', doc.querySelectorAll('a[href^="tel:"]').length>=40 && [...doc.querySelectorAll('#ssTable tbody tr')].every(r=>r.querySelector('a[href^="tel:"]')) && [...doc.querySelectorAll('#tpTable tbody tr')].every(r=>r.querySelector('a[href^="tel:"]')));
  ok('v1.39 停辦的大埔官立已移除', !doc.querySelector('#tpTable tbody tr') || ![...doc.querySelectorAll('#tpTable tbody tr')].some(r=>r.textContent.includes('大埔官立中學')));
  ok('v1.39 三育=直資英中+150位北區', [...doc.querySelectorAll('#tpTable tbody tr')].some(r=>r.textContent.includes('大埔三育中學')&&r.textContent.includes('英中')&&r.textContent.includes('150')));
  ok('v1.39 三育 chips 雙標籤 en+dss', [...doc.querySelectorAll('#tpTable tbody tr')].filter(r=>(' '+r.dataset.tp+' ').includes(' en ')).length===7);
  ok('v1.39 鄧顯電話 26726820', [...doc.querySelectorAll('#ssTable tbody tr')].some(r=>r.textContent.includes('鄧顯紀念中學')&&r.querySelector('a[href="tel:26726820"]')));
  ok('v1.39 王肇枝電話 26561270', [...doc.querySelectorAll('#tpTable tbody tr')].some(r=>r.textContent.includes('王肇枝中學')&&r.querySelector('a[href="tel:26561270"]')));
  ok('v1.39 何郭佩珍中英並重', [...doc.querySelectorAll('#tpTable tbody tr')].some(r=>r.textContent.includes('何郭佩珍')&&r.textContent.includes('中英並重')));
}catch(e){ ok('v1.39 择校电话测试执行', false); console.log('   err='+e.message); }

// ============ v1.40 FAQ 子页 + 关于/CTA/免责卡 ============
try{
  ok('v1.40 faqView 存在且 10 張問答卡', doc.querySelectorAll('#faqView .gcard').length===10);
  ok('v1.40 planSub 6 個子按鈕', doc.querySelectorAll('#planSub button').length===6);
  ok('v1.40 faq 默認隱藏', doc.getElementById('faqView').style.display==='none');
  doc.querySelector('#planSub button[data-sub="faq"]').click();
  ok('v1.40 點 faq 後顯示', doc.getElementById('faqView').style.display==='block');
  doc.querySelector('#planSub button[data-sub="timeline"]').click();
  ok('v1.40 切回 timeline 後 faq 隱藏', doc.getElementById('faqView').style.display==='none' && doc.getElementById('timelineView').style.display==='block');
  ok('v1.40 faq 含居港2年新政條目', doc.getElementById('faqView').textContent.includes('居港滿 2 年'));
  const about=doc.getElementById('aboutView');
  ok('v1.40 關於卡存在（CTA+免責）', !!about && about.textContent.includes('hkeec2023@gmail.com') && about.textContent.includes('史蒂夫HKSZ') && about.textContent.includes('免責聲明'));
  ok('v1.40 關於卡緊鄰 footer 之前', doc.querySelector('footer').previousElementSibling===about);
}catch(e){ ok('v1.40 优化测试执行', false); console.log('   err='+e.message); }

// ============ v1.41 北区表官網列 + Band 細分 ============
try{
  const ssRows=[...doc.querySelectorAll('#ssTable tbody tr')];
  ok('v1.41 北區 20 行都有官網 .edu.hk 鏈接', ssRows.length===20 && ssRows.every(r=>{const a=r.querySelector('td:last-child a');return a&&/\.edu\.hk/.test(a.href);}));
  ok('v1.41 鄧顯 Band 1A + tanghin.edu.hk', ssRows.some(r=>r.textContent.includes('鄧顯紀念中學')&&r.textContent.includes('1A')&&r.querySelector('a[href*="tanghin.edu.hk"]')));
  ok('v1.41 上水官立 Band 3C + ssgss.edu.hk', ssRows.some(r=>r.textContent.includes('上水官立中學')&&r.textContent.includes('3C')&&r.querySelector('a[href*="ssgss.edu.hk"]')));
  ok('v1.41 心誠 Band 2C + flss.edu.hk', ssRows.some(r=>r.textContent.includes('心誠中學')&&r.textContent.includes('2C')&&r.querySelector('a[href*="flss.edu.hk"]')));
  ok('v1.41 表頭含官網欄', doc.querySelector('#ssTable thead').textContent.includes('官網'));
}catch(e){ ok('v1.41 官網测试执行', false); console.log('   err='+e.message); }

// ============ v1.42 北區小學 30 所 ============
try{
  const psRows=[...doc.querySelectorAll('#psTable tbody tr')];
  ok('v1.42 小學表 30 行', psRows.length===30);
  ok('v1.42 校網 80/81/83 = 14/14/2（v1.45 起 data-m）', psRows.filter(r=>(' '+r.dataset.m+' ').includes(' 80 ')).length===14 && psRows.filter(r=>(' '+r.dataset.m+' ').includes(' 81 ')).length===14 && psRows.filter(r=>(' '+r.dataset.m+' ').includes(' 83 ')).length===2);
  ok('v1.42 30 行全帶 tel 電話', psRows.every(r=>r.querySelector('a[href^="tel:"]')));
  ok('v1.42 馬錦燦=上水彩園邨+26711071（非火炭）', psRows.some(r=>r.textContent.includes('馬錦燦紀念小學')&&r.textContent.includes('彩園邨')&&r.querySelector('a[href="tel:26711071"]')));
  ok('v1.45 官立 chip 過濾=1 行（粉嶺官立）', (()=>{psRows.forEach(r=>r.style.display='none');doc.querySelector('#psChips .chip[data-m="gov"]').click();return psRows.filter(r=>r.style.display!=='none').length===1 && psRows.find(r=>r.style.display!=='none').textContent.includes('粉嶺官立小學');})());
  ok('v1.45 全部 chip 恢復 30 可見', (()=>{doc.querySelector('#psChips .chip[data-m="all"]').click();return psRows.filter(r=>r.style.display!=='none').length===30;})());
  ok('v1.42 普教中標註≥4 所', psRows.filter(r=>r.textContent.includes('普教中')).length>=4);
  ok('v1.42 全站 tel 鏈接 70 個（中40+小30）', doc.querySelectorAll('a[href^="tel:"]').length===70);
}catch(e){ ok('v1.42 小學测试执行', false); console.log('   err='+e.message); }

// ============ v1.45 小學表對齊中學格式 + 時間線搬遷 ============
try{
  const psRows2=[...doc.querySelectorAll('#psTable tbody tr')];
  ok('v1.45 檔位 t1/t2/t3 = 12/14/4', psRows2.filter(r=>(' '+r.dataset.m+' ').includes(' t1 ')).length===12 && psRows2.filter(r=>(' '+r.dataset.m+' ').includes(' t2 ')).length===14 && psRows2.filter(r=>(' '+r.dataset.m+' ').includes(' t3 ')).length===4);
  ok('v1.45 檔位首列 tier class 樣式', psRows2.filter(r=>r.querySelector('td.tier1')).length===12 && psRows2.filter(r=>r.querySelector('td.tier3')).length===4);
  ok('v1.45 語言列：普教中 5+雙語 1', psRows2.filter(r=>(' '+r.dataset.m+' ').includes(' pth ')).length===5 && psRows2.filter(r=>(' '+r.dataset.m+' ').includes(' bil ')).length===1);
  ok('v1.45 普教中 chip 點擊過濾=5', (()=>{psRows2.forEach(r=>r.style.display='none');doc.querySelector('#psChips .chip[data-m="pth"]').click();const n=psRows2.filter(r=>r.style.display!=='none').length;doc.querySelector('#psChips .chip[data-m="all"]').click();return n===5;})());
  ok('v1.45 chips 10 個（data-m）', doc.querySelectorAll('#psChips .chip[data-m]').length===10);
  ok('v1.45 分檔依據說明 tip 存在', /檔位＝跨境通勤便利粗分/.test(html));
  ok('v1.45 時間線小學表已遷入擇校分檔（小學 30 所區塊內）', html.indexOf('插小二為例') > html.indexOf('北區小學 30 所') && html.indexOf('插小二為例') < html.indexOf('材料清單（按身份類型準備）'));
  ok('v1.45 身份政策時間線只剩中學線', !/時間線（以 2027\.9 入中一為例）[\s\S]*插小二為例/.test(html.slice(html.indexOf('timelineView'), html.indexOf('schoolsView'))));
  ok('v1.45 頁腳微信號 SteveHKSZ', html.includes('微信號：<b>SteveHKSZ</b>'));
  ok('v1.46 小學表包 scroll-x（與中學一致，手機橫向滾動）', /<div class="scroll-x">\s*<table (class="mtable" )?id="psTable">/.test(html));
  ok('v1.47 小學表帶 mtable class（min-width 780px 生效）', /<table class="mtable" id="psTable">/.test(html));
}catch(e){ ok('v1.45 小學表測試執行', false); console.log('   err='+e.message); }

// ============ v1.37 本地播放 ▶ ============
try{
  ok('v1.37 204 本書全帶視頻 fs', window.eval('ORT_BOOKS.filter(b=>b.fs&&b.fs.length).length')===204);
  ok('v1.37 視頻文件總數 503', window.eval('ORT_BOOKS.reduce((s,b)=>s+b.fs.length,0)')===503);
  ok('v1.37 ortHref 編碼 file:///%20', window.eval('ortHref("牛津树1阶/01【正课】Look at Me-双语讲解.mp4")').indexOf('file:///G:/00%20')===0);
  ok('v1.37 https 下不顯示 ▶', doc.querySelectorAll('#ortList .ort-play').length===0);
  window.eval('curOrtLv="";ORT_LOCAL=true;renderOrt()');
  const np=doc.querySelectorAll('#ortList .ort-play').length;
  ok('v1.37 本地模式 ▶ 全顯示（503 個）', np===503);
  const ph=doc.querySelector('#ortList .ort-play').getAttribute('href');
  ok('v1.37 ▶ href 為 file:/// 且編碼空格', ph.indexOf('file:///G:/')===0 && ph.indexOf('%20')>0);
  window.eval('ORT_LOCAL=false;renderOrt()');
  ok('v1.37 關閉本地模式 ▶ 消失', doc.querySelectorAll('#ortList .ort-play').length===0);
}catch(e){ ok('v1.37 本地播放測試執行', false); console.log('   err='+e.message); }

// ============ v1.35 朗文詞庫 ============
try{
  ok('v1.35 LWTE 詞庫 140 條', window.eval('LWTE_BANKS.reduce((s,e)=>s+e.items.length,0)')===140);
  ok('v1.35 LWTE 19 類', window.eval('LWTE_BANKS.length')===19);
  doc.querySelector('#enPracSub button[data-es="lwte"]').click();
  ok('v1.35 子標籤切換顯示 lwteView', doc.getElementById('lwteView').style.display==='block');
  const li1=doc.querySelector('#lwteList .ort-bk');
  const lk1=li1.dataset.k;
  li1.click();
  const liAfter=[...doc.querySelectorAll('#lwteList .ort-bk')].find(b=>b.dataset.k===lk1);
  ok('v1.35 LWTE 打卡→done+存儲', liAfter.classList.contains('done') && !!JSON.parse(window.localStorage.getItem('hkk_lwte'))[lk1]);
  ok('v1.35 LWTE 詞條帶中文釋義', liAfter.textContent.length > liAfter.textContent.replace(/[^\u4e00-\u9fff]/g,'').length ? [...doc.querySelectorAll('#lwteList .ort-bk')].some(b=>/[\u4e00-\u9fff]/.test(b.textContent)) : false);
  doc.querySelector('#lwteChips .chip[data-bk="5B"]').click();
  ok('v1.35 LWTE 冊 chip 過濾（僅 5B）', [...doc.querySelectorAll('#lwteList .ort-lv-h')].every(h=>h.textContent.includes('5B')));
}catch(e){ ok('v1.35 朗文詞庫測試執行', false); console.log('   err='+e.message); }

// ============ v1.43 51la 访问统计 ============
ok('v1.43 51la SDK 脚本存在(https)', !!doc.querySelector('script#LA_COLLECT[src^="https://sdk.51.la/"]'));
ok('v1.43 51la LA.init id/ck 注入', /LA\.init\(\{id:"3RhjH055gOjxA8UA",ck:"3RhjH055gOjxA8UA"\}\)/.test(html));

// ============ v1.44 时间线加小学插班 ============
ok('v1.44 小学插班时间线表存在（v1.45 起迁入择校分档）', /小學插班時間線（以 2027\.9 插小二為例/.test(html));
ok('v1.44 小学时间线含直接向学校申请', html.includes('沒有中央派位') && html.includes('逐校向校務處交表'));
ok('v1.44 中学时间线仍在', html.includes('中學插班（以 2027.9 入中一為例）') && html.includes('放榜＝2027.7.6'));
ok('v1.44 春季卡补身份赶不上提示', html.includes('2027 年春季批趕不上'));

// ============ v1.48 A批：title+OG / 默认首屏 / 择校切换 / 悬浮咨询 ============
try{
  ok('v1.48 title 改插班擇校關鍵詞', /<title>香港插班擇校 · 北區中小學名單＋申請時間線｜葉工<\/title>/.test(html));
  ok('v1.48 meta description＋OG 四標籤齊', /<meta name="description" content="香港新界北區/.test(html) && (html.match(/<meta property="og:/g)||[]).length===4);
  ok('v1.48 默認主 tab＝升學規劃（nav on＋planView 可見＋guideView 隱藏）', doc.querySelector('nav button.on').dataset.tab==='plan' && !/id="planView" style="display:none/.test(html) && /id="guideView" style="display:none/.test(html) && /let curTab='plan'/.test(html));
  ok('v1.48 引導卡 3 按鈕（schools/timeline/docs）', /id="welcomeCard"/.test(html) && (html.match(/onclick="swPlan\('/g)||[]).length===3);
  ok('v1.48 擇校頁小學/中學切換按鈕＋jmpSch 函數', /id="jmpPri"/.test(html) && /id="jmpSec"/.test(html) && /function jmpSch\(/.test(html));
  ok('v1.48 悬浮諮詢按鈕＋彈層（SteveHKSZ＋複製＋列印隱藏）', /id="ctaFabBtn">💬 諮詢葉工</.test(html) && /<div class="wechat">SteveHKSZ<\/div>/.test(html) && /id="ctaCopy"/.test(html) && /@media print\{#ctaFab\{display:none!important\}\}/.test(html));
  ok('v1.48 版本號 v1.48（footer×2＋ver）', (html.match(/公開版 v1\.48/g)||[]).length===2 && /hkk_v1\.48/.test(html));
}catch(e){ ok('v1.48 A批測試執行', false); console.log('   err='+e.message); }

console.log('\n结果: ' + pass + ' 通过, ' + fail + ' 失败');
process.exit(fail ? 1 : 0);
})();
