const { JSDOM } = require('jsdom');
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf-8');
const data = JSON.parse(fs.readFileSync('build_data.json', 'utf-8'));
const N_POEMS = data.poems.length, N_VOCAB = data.vocab.length;
const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'http://localhost/' });
const w = dom.window, d = w.document;
function log(...a){ console.log(...a); }
let fail = 0;
function assert(cond, msg){ if(!cond){ log('  ✗ FAIL:', msg); fail++; } else { log('  ✓', msg); } }
try {
  log('期望 诗:', N_POEMS, '| 词:', N_VOCAB);
  const grid = d.getElementById('poemGrid');
  assert(grid.children.length === N_POEMS, `诗词卡片数=${grid.children.length} 应=${N_POEMS}`);
  const vlist = d.getElementById('vocabList');
  assert(vlist.children.length === N_VOCAB, `词表卡片数=${vlist.children.length} 应=${N_VOCAB}`);

  // 初中筛选
  const chips = [...d.querySelectorAll('.chip')];
  const chuzhong = chips.find(c => c.dataset.g === '初中');
  assert(!!chuzhong, '存在「初中」筛选 chip');
  chuzhong.click();
  const expectChu = data.poems.filter(p => p.grades.includes('初中')).length;
  assert(grid.children.length === expectChu, `初中筛选卡片数=${grid.children.length} 应=${expectChu}`);
  chips.find(c => c.dataset.g === 'all').click();
  assert(grid.children.length === N_POEMS, '还原全部筛选后卡片数恢复');

  // 打开第一首并查逐字
  grid.children[0].click();
  assert(d.getElementById('mask').classList.contains('show'), '点击卡片后详情弹窗 show');
  const mBody = d.getElementById('mBody');
  const chars = mBody.querySelectorAll('.ch').length;
  assert(chars > 0, `详情逐字块数=${chars} 应>0`);
  assert(mBody.querySelectorAll('.py').length === chars && mBody.querySelectorAll('.jy').length === chars,
         '拼音/粤拼块数与逐字一致');
  const jyText = [...mBody.querySelectorAll('.jy')].map(e=>e.textContent).join('');
  assert(!/\?/.test(jyText), '详情粤拼无 ? 未识别字符');

  // 背诵打卡写/取消
  w.toggleRecite();
  let saved = JSON.parse(w.localStorage.getItem('hkk_poem_v0'));
  assert(saved && Object.values(saved).some(x=>x.recite), 'localStorage 写入 recite 标记');
  w.toggleRecite();
  assert(!Object.values(JSON.parse(w.localStorage.getItem('hkk_poem_v0'))).some(x=>x.recite), '取消后 recite 清除');

  // 进度视图
  [...d.querySelectorAll('nav button')].find(b=>b.dataset.tab==='progress').click();
  assert(d.getElementById('progressView').style.display !== 'none', '进度视图显示');
  assert(d.getElementById('stRecite').textContent === '0', '进度统计 recite=0');

  // 词表单击隐藏中文
  const v0 = vlist.children[0]; v0.click();
  assert(v0.classList.contains('hidezh'), '词表单击后 hidezh 类生效');

  log(fail === 0 ? '\n=== 全部渲染验证通过 ✅ ===' : `\n=== 有 ${fail} 项失败 ===`);
  process.exit(fail === 0 ? 0 : 1);
} catch(e) {
  console.error('验证异常:', e.message);
  process.exit(1);
}
