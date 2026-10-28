#!/usr/bin/env python3
"""Build static HTML, Markdown and SVG together. No network or third-party packages.

Run from any directory: python3 agent-learning-path/eli5/source/build.py
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from html import escape as esc
from content import CHAPTERS, GROUPS
from diagrams import render

ROOT = Path(__file__).resolve().parent.parent


def write(name, text):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def head(title, prefix=""):
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light"><meta name="description" content="用具体问题、机制图和可切换的教学演示理解 AI Agent。30 篇独立图解，可离线阅读。">
<title>{esc(title)} · AI Agent 图解书</title><link rel="stylesheet" href="{prefix}guide.css"><script src="{prefix}guide.js" defer></script></head>'''


def header(prefix="", current=None):
    right = f'<a href="{prefix}index.html#catalog">全部章节 <span aria-hidden="true">↗</span></a>' if current else '<a href="#catalog">打开目录 <span aria-hidden="true">↓</span></a>'
    return f'''<a class="skip" href="#main">跳到正文</a><header class="site-header">
<a class="brand" href="{prefix}index.html" aria-label="AI Agent 图解书首页"><span class="brand-mark" aria-hidden="true">a<span>·</span></span><span>AI AGENT<br><small>图解书 / VISUAL FIELDNOTES</small></span></a>
<nav aria-label="主导航">{('<span class="current-page">'+current+' / 30</span>') if current else ''}{right}</nav></header>'''


def zoom_dialog():
    return '''<dialog id="zoom" class="zoom-dialog" aria-labelledby="zoom-title"><div class="zoom-bar"><h2 id="zoom-title">图解大图</h2><button type="button" data-close-zoom aria-label="关闭大图">关闭 ×</button></div><p class="zoom-hint">可滚动查看完整图。按 Esc 或点击关闭返回。</p><div class="zoom-scroll"><img alt="" width="1000" height="540"></div></dialog>'''


def original_md(c):
    return "../" + c["source"]


def article(c):
    if c["id"] == "17":
        return (Path(__file__).resolve().parent / "redesign_17.html").read_text(encoding="utf-8")
    n, group = c["id"], GROUPS[c["group"]]
    theme = group[3]
    title = c["headline"].replace("\n", "<br>")
    tabs = ''.join(f'<button type="button" data-case="{i}" aria-pressed="{str(i==0).lower()}" aria-controls="case-{i}"><span>0{i+1}</span>{esc(s[0])}</button>' for i,s in enumerate(c["states"]))
    panels = ''.join(f'''<div class="case-panel" id="case-{i}" {'' if i==0 else 'hidden'}>
<div class="diagram-scroll"><button class="diagram-open" type="button" data-zoom="../diagrams/{n}-{i}.svg" data-alt="{esc(s[1])}" aria-label="放大机制图：{esc(s[0])}"><img src="../diagrams/{n}-{i}.svg" width="1000" height="540" alt="{esc(s[1])}" {'fetchpriority="high"' if i==0 else 'loading="eager"'}></button></div>
<div class="case-caption"><span class="state-tag">{esc(s[2])}</span><p>{esc(s[1])}</p><button class="zoom-button" type="button" data-zoom="../diagrams/{n}-{i}.svg" data-alt="{esc(s[1])}" aria-label="放大图解：{esc(s[0])}"><span aria-hidden="true">⤢</span> 放大</button></div></div>''' for i,s in enumerate(c["states"]))
    sections = ''.join(f'''<section class="explanation" id="read-{i}"><div class="section-rail"><span class="section-number">0{i+1}</span><span>{['把概念放回例子','看清关键关系','留意工程边界'][i]}</span></div><div class="section-copy"><h2>{esc(t)}</h2><p>{esc(p)}</p></div></section>''' for i,(t,p) in enumerate(c["sections"]))
    options = ''.join(f'<button type="button" class="quiz-choice" data-answer="{i}" aria-pressed="false"><span>{chr(65+i)}</span>{esc(o)}</button>' for i,o in enumerate(c["quiz"][1]))
    prev = CHAPTERS[int(n)-2] if int(n)>1 else None
    nxt = CHAPTERS[int(n)] if int(n)<30 else None
    def turn(item, label):
        return f'<a href="{item["id"]}.html"><small>{label} / {item["id"]}</small><span>{esc(item["title"])}</span><b aria-hidden="true">↗</b></a>' if item else '<a href="../index.html#catalog"><small>返回</small><span>全部图解</span><b aria-hidden="true">↗</b></a>'
    return head(c["title"], "../")+f'''<body class="article-page layout-{c['layout']}" style="--accent:{theme}" data-chapter="{n}">
<div class="reading-progress" aria-hidden="true"></div>{header('../',n)}
<main id="main"><article>
<header class="article-hero"><div class="hero-context"><span class="eyebrow">{n} / {esc(group[1])}</span><span class="figure-type">{esc(c['label'])}</span></div><div class="hero-columns"><h1>{title}</h1><div class="hero-intro"><p class="original-title">{esc(c['title'])}</p><p class="intro">{esc(c['intro'])}</p><a class="text-link" href="#explore">从图里看 <span aria-hidden="true">↓</span></a></div></div><div class="chapter-watermark" aria-hidden="true">{n}</div></header>
<section class="explorer" id="explore" aria-labelledby="explorer-title"><div class="explorer-heading"><h2 id="explorer-title">换一种情况，看看会怎样。</h2><span>本地教学演示 · 不连接真实服务</span></div><div class="case-controls" role="group" aria-label="选择演示情况">{tabs}</div><p class="mobile-diagram-hint">点按图解可放大阅读，拖动大图查看细节。</p>{panels}<p class="sr-only" id="case-announcement" aria-live="polite"></p><noscript><p class="noscript-note">切换演示需要 JavaScript；下方 Markdown 图文版包含全部三种情况。</p></noscript></section>
<div class="reading-body"><aside class="analogy"><span>先借一个熟悉的画面</span><p>{esc(c['analogy'])}</p></aside><div class="explanations">{sections}</div></div>
<aside class="boundary"><span class="boundary-mark" aria-hidden="true">↳</span><div><h2>{esc(c['boundary'][0])}</h2><p>{esc(c['boundary'][1])}</p></div></aside>
<section class="quiz" aria-labelledby="quiz-title" data-correct="{c['quiz'][2]}" data-reason="{esc(c['quiz'][3])}"><div class="quiz-heading"><span class="eyebrow">停一下，自己判断</span><h2 id="quiz-title">{esc(c['quiz'][0])}</h2></div><div class="quiz-options">{options}<p class="quiz-feedback" role="status" hidden></p></div><noscript><p>答案为 {chr(65+c['quiz'][2])}。{esc(c['quiz'][3])}</p></noscript></section>
<footer class="article-source"><div><span class="eyebrow">继续深入</span><p>到工程文章里看实现、异常处理和验收方法。</p></div><div><a href="{esc(original_md(c))}" download>下载工程原文 <span aria-hidden="true">↓</span></a><a href="../chapters/{n}.md" download>下载本篇图文版 <span aria-hidden="true">↓</span></a></div></footer>
<nav class="page-turn" aria-label="章节翻页">{turn(prev,'上一篇')}{turn(nxt,'下一篇')}</nav>
</article></main><footer class="site-footer"><span>AI 工程实践手册</span><a href="../index.html#catalog">回到 30 篇图解目录 ↑</a><span>读懂一件事，再往前一步。</span></footer>{zoom_dialog()}</body></html>'''


def index():
    features=[]
    for idx,tag in [(4,"通信 / 05"),(7,"记忆 / 08"),(18,"授权 / 19")]:
        c=CHAPTERS[idx]
        features.append(f'''<a class="featured-chapter" href="articles/{c['id']}.html" style="--accent:{GROUPS[c['group']][3]}"><div class="feature-art"><img src="diagrams/{c['id']}-0.svg" width="1000" height="540" alt="{esc(c['states'][0][1])}" loading="lazy"></div><div class="feature-info"><span class="eyebrow">{tag}</span><h3>{esc(c['headline'].replace(chr(10),''))}</h3><span class="feature-arrow" aria-hidden="true">↗</span></div></a>''')
    groups=[]
    for gi,g in enumerate(GROUPS):
        rows=[]
        for c in [x for x in CHAPTERS if x['group']==gi]:
            search=esc(c['title']+' '+c['headline'].replace('\n','')+' '+c['label'])
            rows.append(f'''<a id="t{c['id']}" class="chapter-row" href="articles/{c['id']}.html" data-search="{search}"><span class="row-number">{c['id']}</span><div><h3>{esc(c['title'])}</h3><p>{esc(c['headline'].replace(chr(10),''))}</p></div><span class="row-type">{esc(c['label'])}</span><span class="row-arrow" aria-hidden="true">↗</span></a>''')
        groups.append(f'''<section class="catalog-group" data-group="{gi}" style="--accent:{g[3]}"><header><span class="group-range">{g[2]}</span><div><h2>{g[0]}</h2><p>{g[1]}</p></div></header><div class="chapter-rows">{''.join(rows)}</div></section>''')
    filters=''.join(f'<button type="button" data-filter="{i}" aria-pressed="false">{g[1]}</button>' for i,g in enumerate(GROUPS))
    return head("把 Agent 拆开看")+f'''<body class="index-page">{header()}
<main id="main"><section class="book-cover"><div class="cover-copy"><span class="eyebrow">AI ENGINEERING HANDBOOK / 图解版</span><h1>把 Agent<br><em>拆开看。</em></h1><p>工具怎样被调用，记忆怎样被读写，<br>任务又怎样在出错以后继续。</p><a class="cover-cta" href="articles/01.html">从第一篇开始 <span aria-hidden="true">↗</span></a><div class="cover-meta"><span><b>28</b> 个主题</span><span><b>02</b> 篇架构补充</span><span>可离线阅读</span></div></div><div class="cover-visual"><div class="cover-caption"><span>打开一个 Agent，里面有什么？</span><span aria-hidden="true">↙</span></div><img src="diagrams/04-0.svg" width="1000" height="540" alt="Agent 根据观察选择行动；得到结果后再判断，证据充分时结束。"><div class="cover-note"><span class="cover-note-number">01</span><p>不只看结论。<br>把中间发生的事也看明白。</p></div><span class="cover-stamp">READ · TRY · UNDERSTAND</span></div></section>
<section class="featured"><div class="section-heading"><h2>从一个好问题开始。</h2><p>每一种机制，都用适合它的图来讲。</p></div><div class="featured-grid">{''.join(features)}</div></section>
<section class="catalog" id="catalog" aria-labelledby="catalog-title"><div class="catalog-intro"><div><span class="eyebrow">THE FIELD GUIDE / 全部章节</span><h2 id="catalog-title">沿着问题，<br>找到下一篇。</h2></div><div class="catalog-search"><label for="chapter-search">找一个主题</label><div class="search-box"><input id="chapter-search" type="search" placeholder="试试 MCP、记忆、恢复…" autocomplete="off"><span aria-hidden="true">⌕</span></div><p id="search-count" role="status">30 篇图解 · 每篇都有可切换的情况演示</p></div></div><div class="catalog-filters" role="group" aria-label="按学习阶段筛选"><button type="button" class="selected" data-filter="all" aria-pressed="true">全部</button>{filters}</div><p id="empty-search" hidden>没有找到这个主题。可以换个关键词，或切换到“全部”。</p>{''.join(groups)}</section>
<aside class="reading-note"><h2>图解之后，接着读工程文章。</h2><p>这里先用具体例子建立直觉，边界和失败情况也一起讲。每篇末尾保留对应工程原文的下载入口；在 GitHub 阅读时，可以使用同目录下的 Markdown 图文版。</p><a href="README.md" download>下载图文目录 ↓</a></aside></main>
<footer class="site-footer"><span>AI 工程实践手册</span><a href="#main">回到开头 ↑</a><span>图解 / 例子 / 边界</span></footer></body></html>'''


def markdown(c):
    n=c['id']
    parts=[f"# {c['title']}", f"[← 图解目录](../README.md#{n}) · [工程文章]({original_md(c)})", f"**{c['headline'].replace(chr(10),'')}**", c['intro'], f"> {c['analogy']}"]
    for i,(label,caption,status) in enumerate(c['states']):
        parts += [f"## {label}", f"![{caption}](../diagrams/{n}-{i}.svg)", f"**{status}**。{caption}"]
    for title,p in c['sections']:parts += [f"## {title}",p]
    parts += [f"## {c['boundary'][0]}",c['boundary'][1],"## 停一下，自己判断",c['quiz'][0]]
    parts += ["\n".join(f"- {chr(65+i)}. {x}" for i,x in enumerate(c['quiz'][1])),f"<details>\n<summary>查看解释</summary>\n\n答案为 {chr(65+c['quiz'][2])}。{c['quiz'][3]}\n\n</details>",f"[阅读工程文章]({original_md(c)}) · [返回图解目录](../README.md#{n})","> 图片、例子与结果均为教学示意，不代表真实服务运行或性能测试。"]
    return "\n\n".join(parts)


def readme():
    p=["# AI Agent 图解书", "[← AI Agent 学习路线](../README.md) · [离线 HTML 入口](index.html)", "从具体问题理解 Agent。28 个主题与 2 篇架构补充，每篇采用对应机制的图形，并比较三种不同情况。HTML 版可以切换演示、检查理解、搜索章节；下面的 Markdown 图文版可以直接在 GitHub 阅读。", "离线使用时，下载整个 `eli5` 目录并打开 `index.html`。HTML 无需联网或安装依赖。GitHub 仓库页面通常显示 HTML 源码，请使用下面的图文链接，或在本地浏览器打开。"]
    for i,g in enumerate(GROUPS):
        p.append(f"## {g[1]}")
        for c in [x for x in CHAPTERS if x['group']==i]:
            p.extend([f'<a id="{c["id"]}"></a>',f'**{c["id"]} [{c["title"]}](chapters/{c["id"]}.md)**',c['headline'].replace('\n','')+"　"+c['label']])
    p += ["## 维护图解", "讲解内容在 `source/content.py`，各主题的机制图在 `source/diagrams.py`，页面生成器在 `source/build.py`（第 17 篇使用 `source/redesign_17.html` 独立模板）。修改后执行 `python3 agent-learning-path/eli5/source/build.py`，同步生成 HTML、Markdown 和 SVG。页面样式与交互分别在 `guide.css`、`guide.js`。", "运行 `python3 agent-learning-path/eli5/source/check.py` 检查产物、链接与内容对应关系。浏览器验证方法见 [维护说明](source/README.md)。"]
    return "\n\n".join(p)


def main():
    for c in CHAPTERS:
        for i in range(len(c['states'])):
            write(f"diagrams/{c['id']}-{i}.svg",render(c,i,GROUPS[c['group']][3]))
        write(f"articles/{c['id']}.html",article(c))
        write(f"chapters/{c['id']}.md",markdown(c))
    write("index.html",index())
    write("README.md",readme())
    # Remove only retired generated assets from the previous card edition.
    # Keep unknown files and all engineering source articles untouched.
    for c in CHAPTERS:
        for suffix in ("-3.svg","-4.svg"):
            p=ROOT/"diagrams"/(c['id']+suffix)
            if p.exists():p.unlink()
        p=ROOT/"images"/(c['id']+".svg")
        if p.exists():p.unlink()
    images=ROOT/"images"
    if images.exists() and not any(images.iterdir()):images.rmdir()
    old_css=ROOT/"article.css"
    if old_css.exists():old_css.unlink()
    print("Built 30 HTML chapters, 30 Markdown chapters and 90 scenario diagrams.")


if __name__ == "__main__":main()
