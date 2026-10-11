/* Build an offline HTML reading edition. Rendering tools are build-time only. */
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');
const { chromium } = require('playwright');

async function main() {
  const root = path.resolve(__dirname, '..');
  const args = process.argv.slice(2);
  if (args.length !== 2 || args[0] !== '--mermaid') {
    throw new Error('Usage: node scripts/build_reading.cjs --mermaid /path/to/mermaid.min.js');
  }
  const library = fs.readFileSync(path.resolve(args[1]), 'utf8');
  const book = fs.readFileSync(path.join(root, 'education', 'BOOK.md'), 'utf8');
  const out = path.join(root, 'build');
  fs.mkdirSync(out, { recursive: true });
  const sources = [];
  const diagramBook = book.replace(/```mermaid\n([\s\S]*?)\n```/g, (_, definition) => {
    const index = sources.push(definition) - 1;
    return `<div class="diagram" data-diagram="${index}"></div>`;
  });
  let content = marked.parse(diagramBook);
  // Reading edition is in root/build; links resolve into the education directory.
  content = content.replace(/href="(?!#|[a-z]+:)([^"]+)"/gi, 'href="../education/$1"');
  const toc = [...book.matchAll(/^- \[([^\]]+)\]\(#(chapter-\d+)\)/gm)]
    .map((m) => `<a href="#${m[2]}">${m[1]}</a>`).join('');
  const html = `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>教育 AI 应用实践 · Blueberry</title><style>
:root{color-scheme:light;--ink:#243047;--muted:#637085;--accent:#6450c7;--line:#e4e6ef}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:28px}
body{margin:0;background:#f6f7fb;color:var(--ink);font:16px/1.95 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
aside{position:fixed;inset:0 auto 0 0;width:260px;padding:38px 24px;overflow:auto;background:#fafafe;border-right:1px solid var(--line)}
aside b{display:block;font-size:23px;line-height:1.4;letter-spacing:-.5px}aside p{font-size:13px;color:var(--muted);margin:10px 0 26px}
nav a{display:block;font-size:13px;line-height:1.6;padding:8px 0;border-bottom:1px solid var(--line)}
main{margin:32px 36px 56px 296px;padding:52px 62px;background:white;max-width:1080px;border:1px solid var(--line);border-radius:16px}
h1,h2,h3{line-height:1.5;color:#1e2940}h1{font-size:32px;letter-spacing:-.6px;margin:0 0 20px}h2{font-size:25px;margin:38px 0 20px}h3{font-size:20px;margin:30px 0 14px}
p{margin:16px 0}hr{border:0;border-top:1px solid var(--line);margin:52px 0}
code{font:13px/1.7 ui-monospace,SFMono-Regular,Consolas,monospace;background:#f1f2f8;padding:2px 5px;border-radius:4px;overflow-wrap:anywhere}
pre{background:#f1f2f8;padding:20px;border-radius:10px;overflow:auto;line-height:1.7}pre code{background:transparent;padding:0}
table{width:100%;border-collapse:collapse;display:block;overflow-x:auto;font-size:14px;line-height:1.7;margin:22px 0}
td,th{border:1px solid var(--line);padding:11px 13px;text-align:left;vertical-align:top}th{background:#f4f4fb;font-weight:600}
blockquote{border-left:3px solid #a99de5;padding-left:20px;color:var(--muted);margin:24px 0}
.diagram{padding:22px 8px;border:1px solid var(--line);border-radius:10px;background:#fcfcff;margin:26px 0;overflow:auto;text-align:center}
.diagram svg{max-width:100%;height:auto}.diagram-error{color:#ad253b}
@media(max-width:980px){aside{position:static;width:auto;padding:24px;border-bottom:1px solid var(--line)}nav{display:flex;gap:12px;flex-wrap:wrap}nav a{max-width:260px}main{margin:20px;padding:28px;max-width:none}}
@media(max-width:600px){body{font-size:15px}main{margin:12px;padding:22px 18px}h1{font-size:26px}h2{font-size:22px}.diagram svg{max-width:none}}
@media print{aside{display:none}main{margin:0;border:0;padding:0;max-width:none}pre,table,.diagram{break-inside:avoid}a{color:inherit}html{scroll-behavior:auto}}
</style></head><body><aside><b>教育 AI 应用实践</b><p>AI 应用工程案例集 · Blueberry<br>教育篇</p><nav>${toc}</nav></aside><main>${content}</main></body></html>`;
  const browser = await chromium.launch({ headless: true,
    executablePath: process.env.FDE_BROWSER_EXECUTABLE || chromium.executablePath() });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1050 }, deviceScaleFactor: 1 });
    await page.setContent(html);
    await page.addScriptTag({ content: library });
    const rendered = await page.evaluate(async (definitions) => {
      mermaid.initialize({startOnLoad:false,securityLevel:'strict',theme:'base',
        fontFamily:'PingFang SC, sans-serif', themeVariables:{primaryColor:'#eeebff',primaryTextColor:'#243047',
        primaryBorderColor:'#9b8cdd',lineColor:'#7d7795',secondaryColor:'#eaf4f7',tertiaryColor:'#f8f6ff'},
        flowchart:{htmlLabels:false}});
      const results = [];
      for (let index=0;index<definitions.length;index++) {
        const target = document.querySelector(`[data-diagram="${index}"]`);
        try {
          const {svg} = await mermaid.render(`diagram-${index}`,definitions[index]);
          target.innerHTML = svg;
          const graphic = target.querySelector('svg');
          graphic.style.width = `${graphic.viewBox.baseVal.width}px`;
          graphic.style.removeProperty('max-width');
          results.push({index,ok:true,svg});
        } catch (error) {
          target.textContent = String(error);
          target.classList.add('diagram-error');
          results.push({index,ok:false,error:String(error)});
        }
      }
      return results;
    }, sources);
    if (rendered.some((item)=>!item.ok)) throw new Error(JSON.stringify(rendered.filter((item)=>!item.ok)));
    for (const item of rendered) fs.writeFileSync(path.join(out, `diagram-${item.index+1}.svg`),item.svg);
    // Remove library and any rendering-only script nodes from the standalone output.
    await page.evaluate(()=>document.querySelectorAll('script').forEach((node)=>node.remove()));
    fs.writeFileSync(path.join(out,'reading.html'),await page.content());
    await page.screenshot({path:path.join(out,'reading-desktop.png')});
    for (let index=0;index<sources.length;index++) {
      await page.locator(`[data-diagram="${index}"]`).screenshot({path:path.join(out,`diagram-${index+1}.png`)});
    }
    await page.setViewportSize({width:430,height:932});
    await page.evaluate(()=>window.scrollTo(0,0));
    await page.screenshot({path:path.join(out,'reading-mobile.png')});
    fs.writeFileSync(path.join(out,'render-report.json'),JSON.stringify({diagrams:rendered.length,errors:0},null,2));
    console.log(`Built offline reading.html; rendered ${rendered.length} diagrams with zero errors.`);
  } finally { await browser.close(); }
}
main().catch((error)=>{console.error(error);process.exitCode=1;});
