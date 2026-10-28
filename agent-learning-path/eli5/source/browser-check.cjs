/* Local visual/interaction audit. Uses an installed Playwright and browser.
 * See README.md for environment variables. No browser downloads or network.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.env.AGENT_GUIDE_PLAYWRIGHT || 'playwright');
const root = path.resolve(__dirname, '..');
const out = process.env.AGENT_GUIDE_SCREENSHOTS || fs.mkdtempSync(path.join(os.tmpdir(), 'agent-guide-review-'));
fs.mkdirSync(out, {recursive:true});
const file = relative => pathToFileURL(path.join(root, relative)).href;

(async () => {
  const browser = await chromium.launch({headless:true, ...(process.env.AGENT_GUIDE_CHROME ? {executablePath:process.env.AGENT_GUIDE_CHROME} : {})});
  const errors = [], network = [], overflow = [], collisions = [];
  try {
    const p = await browser.newPage({viewport:{width:1440,height:1050},deviceScaleFactor:1,reducedMotion:'reduce'});
    p.on('pageerror', e => errors.push(e.message));
    p.on('request', r => {if (/^https?:/.test(r.url())) network.push(r.url());});
    await p.goto(file('index.html'));
    assert.equal(await p.locator('.chapter-row:visible').count(),30);
    await p.locator('#chapter-search').fill('MCP');
    assert.equal(await p.locator('.chapter-row:visible').count(),1);
    await p.locator('.chapter-row:visible').click();
    assert(p.url().endsWith('/05.html'));
    await p.goto(file('index.html'));
    await p.locator('[data-filter="2"]').click();
    assert.equal(await p.locator('.chapter-row:visible').count(),3);
    await p.locator('#chapter-search').fill('不存在的词');
    assert(await p.locator('#empty-search').isVisible());
    await p.locator('#chapter-search').fill('');
    await p.locator('[data-filter="all"]').click();
    await p.screenshot({path:path.join(out,'index-desktop.png')});
    for(let n=1;n<=30;n++) {
      const id=String(n).padStart(2,'0');
      await p.setViewportSize({width:1440,height:1050});
      await p.goto(file(`articles/${id}.html`));
      assert.equal(await p.locator('h1').count(),1);
      if (id === '17') {
        // Custom ledger page: three recovery scenarios and its own step/query controls.
        for (const key of ['rebuild','checkpoint','unknown']) {
          await p.locator(`[data-scenario="${key}"]`).click();
          assert.equal(await p.locator(`[data-scenario="${key}"]`).getAttribute('aria-pressed'),'true');
        }
        await p.locator('[data-scenario="checkpoint"]').click();
        assert.equal(await p.locator('#f-checkpoint').textContent(),'#3');
        await p.locator('#step').click();
        assert.equal(await p.locator('#f-task').textContent(),'已完成');
        await p.locator('[data-scenario="unknown"]').click();
        for(let i=0;i<4;i++) await p.locator('#step').click();
        await p.locator('#query').click();
        assert.equal(await p.locator('#f-task').textContent(),'已完成');
        await p.locator('[data-answer="0"]').click();
        assert.equal(await p.locator('[data-answer="0"]').getAttribute('data-state'),'wrong');
        await p.locator('[data-answer="1"]').click();
        assert.equal(await p.locator('[data-answer="1"]').getAttribute('data-state'),'correct');
        assert(await p.locator('.quiz-feedback').isVisible());
        assert(!(await p.evaluate(()=>document.documentElement.scrollWidth > innerWidth + 1)),'17: desktop overflow');
        await p.evaluate(()=>scrollTo(0,0));
        await p.screenshot({path:path.join(out,'17-desktop.png')});
        for(const width of [390,768]) {
          await p.setViewportSize({width,height:844});
          assert(!(await p.evaluate(()=>document.documentElement.scrollWidth > innerWidth + 1)),`17: ${width}px overflow`);
        }
        continue;
      }
      for(let i=0;i<3;i++) {
        await p.locator(`[data-case="${i}"]`).click();
        assert.equal(await p.locator('.case-panel:visible').count(),1);
        assert(await p.locator(`#case-${i}`).isVisible());
        await p.locator(`#case-${i} img`).evaluate(img=>img.decode());
        assert(await p.locator(`#case-${i} img`).evaluate(img=>img.complete && img.naturalWidth>0));
      }
      await p.locator('[data-case="0"]').focus();
      await p.keyboard.press('ArrowRight');
      assert.equal(await p.locator('[data-case="1"]').getAttribute('aria-pressed'),'true');
      await p.locator('#case-1 .zoom-button').click();
      assert(await p.locator('#zoom').isVisible());
      await p.keyboard.press('Escape');
      assert(!(await p.locator('#zoom').isVisible()));
      assert.equal(await p.evaluate(()=>document.activeElement.className),'zoom-button');
      const correct=Number(await p.locator('.quiz').getAttribute('data-correct'));
      await p.locator(`[data-answer="${1-correct}"]`).click();
      assert(await p.locator('.quiz-choice.incorrect').isVisible());
      await p.locator(`[data-answer="${correct}"]`).click();
      assert(await p.locator('.quiz-choice.correct').isVisible());
      assert(await p.locator('.quiz-feedback').isVisible());
      assert(!(await p.evaluate(()=>document.documentElement.scrollWidth > innerWidth + 1)),`${id}: desktop overflow`);
      await p.locator('[data-case="0"]').click();
      await p.evaluate(()=>scrollTo(0,0));
      await p.screenshot({path:path.join(out,`${id}-desktop.png`)});
      for(const width of [390,768]) {
        await p.setViewportSize({width,height:844});
        assert(!(await p.evaluate(()=>document.documentElement.scrollWidth > innerWidth + 1)),`${id}: ${width}px overflow`);
        await p.locator('[data-case="2"]').click();
        assert(await p.locator('#case-2').isVisible());
        if(width===390) {
          await p.locator('#case-2 .diagram-open').click();
          assert(await p.locator('#zoom').isVisible());
          await p.locator('[data-close-zoom]').click();
          await p.evaluate(()=>scrollTo(0,0));
          if([1,5,8,19,22,26,28].includes(n)) await p.screenshot({path:path.join(out,`${id}-mobile.png`),fullPage:true});
        }
      }
    }
    await p.setViewportSize({width:1000,height:540});
    // Check intrinsic SVG bounds and visible text intersections.
    for (const svg of fs.readdirSync(path.join(root,'diagrams')).filter(f=>f.endsWith('.svg')).sort()) {
      await p.goto(file('diagrams/'+svg));
      const issues=await p.evaluate(()=>{
        const texts=[...document.querySelectorAll('text')].map(t=>({t:t.textContent,el:t,b:t.getBoundingClientRect()}));
        const outside=texts.filter(({b})=>b.left < -1 || b.right > 1001 || b.top < -1 || b.bottom > 541).map(x=>x.t);
        const overlaps=[];
        // A later rectangle can intentionally replace text (e.g. a corrected record).
        const visible=texts.filter(({el,b})=>{
          const hit=document.elementFromPoint((b.left+b.right)/2,(b.top+b.bottom)/2);
          return hit===el;
        });
        for(let i=0;i<visible.length;i++)for(let j=i+1;j<visible.length;j++){
          const a=visible[i],b=visible[j];
          const w=Math.min(a.b.right,b.b.right)-Math.max(a.b.left,b.b.left);
          const h=Math.min(a.b.bottom,b.b.bottom)-Math.max(a.b.top,b.b.top);
          if(w>3&&h>3)overlaps.push([a.t,b.t]);
        }
        return {outside,overlaps};
      });
      if(issues.outside.length)overflow.push({svg,text:issues.outside});
      if(issues.overlaps.length)collisions.push({svg,pairs:issues.overlaps});
      await p.screenshot({path:path.join(out,svg.replace('.svg','.png'))});
    }
    // Five contact sheets, six topics per sheet, three cases per row.
    fs.writeFileSync(path.join(out,'diagram-review.json'),JSON.stringify({overflow,collisions},null,2));
    await p.goto(file('index.html'));
    for(let batch=0;batch<5;batch++) {
      let items='';
      for(let n=batch*6+1;n<=batch*6+6;n++) for(let s=0;s<3;s++) {
        const id=String(n).padStart(2,'0');
        items+=`<figure><figcaption>${id} / ${s+1}</figcaption><img src="${file(`diagrams/${id}-${s}.svg`)}"></figure>`;
      }
      await p.setViewportSize({width:1800,height:2050});
      await p.setContent(`<html lang="zh-CN"><style>body{margin:0;background:#fff;display:grid;grid-template-columns:repeat(3,1fr);gap:8px;font:16px sans-serif}figure{margin:0;border:1px solid #ddd}figcaption{padding:6px}img{width:100%;display:block}</style>${items}</html>`);
      await p.locator('img').evaluateAll(async imgs=>{await Promise.all(imgs.map(i=>i.decode()))});
      await p.screenshot({path:path.join(out,`contact-${batch+1}.png`),fullPage:true});
    }
    assert.deepEqual(errors,[],'JavaScript errors');
    assert.deepEqual(network,[],'Unexpected network requests');
    const report={chapters:30,caseSwitches:90,diagramBounds:90,viewports:[1440,768,390],search:true,quiz:true,keyboard:true,zoom:true,network:0,errors,overflow,collisions,screenshots:out};
    fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));
    console.log(JSON.stringify(report,null,2));
    assert.deepEqual(overflow,[],'SVG text overflow');
    assert.deepEqual(collisions,[],'SVG visible text overlap');
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exit(1)});
