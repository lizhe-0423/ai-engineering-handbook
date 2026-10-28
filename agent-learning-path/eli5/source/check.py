#!/usr/bin/env python3
"""Validate the published guide without requiring a browser or network."""
import sys
sys.dont_write_bytecode = True
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import re
import xml.etree.ElementTree as ET
from content import CHAPTERS, GROUPS
from build import article, index, markdown, readme
from diagrams import render, RENDERERS

ROOT = Path(__file__).resolve().parent.parent
errors = []
links = 0


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.refs = []
        self.images = 0
        self.cases = 0
        self.h1s = 0
        self.downloads = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids: errors.append(f"Duplicate ID {a['id']}")
            self.ids.add(a['id'])
        if 'data-case' in a:self.cases += 1
        if tag == 'h1':self.h1s += 1
        if tag == 'img':
            self.images += 1
            if not a.get('alt') and 'zoom-dialog' not in str(a):
                # The empty modal image gets its alt and src when opened.
                if a.get('src'):errors.append('Image missing text alternative')
        for key in ('href', 'src', 'data-zoom'):
            if a.get(key):self.refs.append(a[key])
        if tag == 'a' and a.get('href','').endswith('.md'):
            self.downloads.append('download' in a)


def same(path, expected):
    actual = path.read_text(encoding='utf-8')
    if actual != expected.rstrip()+'\n':errors.append(f'Stale generated file: {path.relative_to(ROOT)}')


def ref_exists(path, ref):
    global links
    u = urlsplit(ref)
    if u.scheme or u.netloc:
        errors.append(f'Unexpected external dependency/link: {path.name} {ref}')
        return
    target = (path.parent / unquote(u.path)).resolve() if u.path else path.resolve()
    if not target.is_file():errors.append(f'Broken reference: {path.relative_to(ROOT)} -> {ref}')
    elif u.fragment and target.suffix == '.html':
        if u.fragment not in Page(target.read_text()).ids:errors.append(f'Missing HTML anchor: {ref}')
    elif u.fragment and target.suffix == '.md':
        text = target.read_text()
        if f'id="{u.fragment}"' not in text:errors.append(f'Missing Markdown anchor: {ref}')
    links += 1


assert len(CHAPTERS) == 30 and len(RENDERERS) == 30
assert len(set(RENDERERS.values())) == 30, 'Each topic must have its own diagram composition'
assert len(list((ROOT/'diagrams').glob('*.svg'))) == 90
route = (ROOT.parent/'README.md').read_text()
for c in CHAPTERS:
    n=c['id']
    assert f'[图解](eli5/chapters/{n}.md)' in route
    assert (ROOT/c['source']).resolve().is_file(), c['source']
    same(ROOT/f'articles/{n}.html',article(c))
    same(ROOT/f'chapters/{n}.md',markdown(c))
    digests=[]
    for i in range(3):
        p=ROOT/f'diagrams/{n}-{i}.svg'
        same(p,render(c,i,GROUPS[c['group']][3]))
        r=ET.parse(p).getroot()
        ns='{http://www.w3.org/2000/svg}'
        assert r.find(ns+'title') is not None and r.find(ns+'desc') is not None
        assert r.attrib['viewBox'] == '0 0 1000 540'
        assert r.find('.//'+ns+'script') is None
        # Discard accessibility description before comparing visible diagram output.
        visible=re.sub(r'<(?:title|desc)\b[^>]*>.*?</(?:title|desc)>','',p.read_text())
        digests.append(hashlib.sha256(visible.encode()).hexdigest())
    assert len(set(digests)) == 3, f'Cases should visibly differ: {n}'
same(ROOT/'index.html',index())
same(ROOT/'README.md',readme())
for p in [ROOT/'index.html',*sorted((ROOT/'articles').glob('*.html'))]:
    page=Page(p.read_text())
    if page.h1s != 1:errors.append(f'Expected one h1: {p.name}')
    if p.parent.name=='articles':
        if page.cases!=3:errors.append(f'Missing scenario controls: {p.name}')
        if not all(page.downloads):errors.append(f'Raw Markdown navigation: {p.name}')
    for ref in page.refs:ref_exists(p,ref)
for p in [ROOT/'README.md',*sorted((ROOT/'chapters').glob('*.md'))]:
    for ref in re.findall(r'\]\(([^)]+)\)',p.read_text()):ref_exists(p,ref)
if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'PASS: 30 chapters, 90 distinct scenario SVGs, {links} local references, HTML/Markdown/source parity.')
