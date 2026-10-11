"""Check chapter completeness, local links, JSON blocks and basic publication hygiene."""
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main():
    issues = []
    files = [path for path in ROOT.rglob('*.md') if not ({'.git', 'build'} & set(path.parts))]
    for path in files:
        text = path.read_text(encoding='utf-8')
        name = str(path.relative_to(ROOT))
        if sum(line.startswith('```') for line in text.splitlines()) % 2:
            issues.append(f'{name}: unmatched code fence')
        prose = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', prose):
            if re.match(r'^[a-zA-Z][\w+.-]*:', target) or target.startswith('#'):
                continue
            local = unquote(urlsplit(target).path)
            if not (path.parent / local).exists():
                issues.append(f'{name}: missing local target {target}')
        for block in re.findall(r'^```json\n(.*?)^```', text, re.M | re.S):
            try:
                json.loads(block)
            except ValueError as exc:
                issues.append(f'{name}: invalid JSON block: {exc}')
        patterns = [r'https?://[^\s)]+feishu[^\s)]+', r'AKIA[0-9A-Z]{16}',
                    r'gh[pousr]_[A-Za-z0-9]{20,}', r'/Users/',
                    r'-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----']
        for pattern in patterns:
            if re.search(pattern, text):
                issues.append(f'{name}: publication-hygiene pattern needs review')
    fixtures = sorted((ROOT / 'examples/education/data').glob('*.json'))
    for path in fixtures:
        try:
            json.loads(path.read_text(encoding='utf-8'))
        except ValueError as exc:
            issues.append(f'{path.name}: invalid fixture: {exc}')
    chapters = sorted((ROOT / 'chapters').glob('[0-9][0-9]-*.md'))
    if [path.name[:2] for path in chapters] != [f'{n:02d}' for n in range(10)]:
        issues.append('Expected preface 00 and chapters 01–09')
    book = (ROOT / 'BOOK.md').read_text(encoding='utf-8')
    anchors = set(re.findall(r'<a id="([^"]+)">', book))
    for target in re.findall(r'\]\(#(chapter-\d+)\)', book):
        if target not in anchors:
            issues.append(f'BOOK.md: missing chapter anchor {target}')
    if len(anchors) != 10:
        issues.append('BOOK.md: expected ten chapter anchors')
    for path in chapters[1:]:
        if path.read_text(encoding='utf-8').count('```mermaid') != 1:
            issues.append(f'{path.name}: expected one Mermaid mechanism diagram')
    print(json.dumps({'markdown_files': len(files), 'json_fixtures': len(fixtures),
                      'chapter_sources': len(chapters), 'chapter_anchors': len(anchors),
                      'issues': issues}, ensure_ascii=False, indent=2))
    return int(bool(issues))


if __name__ == '__main__':
    raise SystemExit(main())
