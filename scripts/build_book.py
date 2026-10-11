"""Build the education Markdown book from the chapter sources (standard library only)."""
import posixpath
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'education'
CHAPTERS = sorted((ROOT / 'chapters').glob('[0-9][0-9]-*.md'))
EXPECTED = [f'{number:02d}' for number in range(10)]


def build():
    if [path.name[:2] for path in CHAPTERS] != EXPECTED:
        raise SystemExit('Expected preface 00 and chapters 01–09, without gaps or duplicates.')
    anchors = {path.name: f'chapter-{path.name[:2]}' for path in CHAPTERS}
    titles = {path.name: path.read_text(encoding='utf-8').splitlines()[0].removeprefix('# ')
              for path in CHAPTERS}
    sections = ['# 教育 AI 应用实践\n\n'
                '**Blueberry · AI 应用工程案例集 · 教育**\n\n'
                '按章节连续阅读。单章目录与运行说明见 [教育首页](README.md)。\n\n'
                '## 目录\n\n' + '\n'.join(
                    f'- [{titles[path.name]}](#{anchors[path.name]})' for path in CHAPTERS)]
    for path in CHAPTERS:
        text = path.read_text(encoding='utf-8')
        blocks = re.split(r'(^```[^\n]*\n.*?^```\s*$)', text, flags=re.M | re.S)
        for index in range(0, len(blocks), 2):
            prose = blocks[index]
            prose = re.sub(r'^(#{1,5}) ', r'#\1 ', prose, flags=re.M)

            def relocate(match):
                label, target = match.groups()
                if re.match(r'^[a-zA-Z][\w+.-]*:', target) or target.startswith('#'):
                    return match.group(0)
                if target in anchors:
                    return f'[{label}](#{anchors[target]})'
                return f'[{label}]({posixpath.normpath(posixpath.join("chapters", target))})'

            blocks[index] = re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)', relocate, prose)
        sections.append(f'<a id="{anchors[path.name]}"></a>\n\n' + ''.join(blocks).strip())
    output = ROOT / 'BOOK.md'
    output.write_text('\n\n---\n\n'.join(sections) + '\n', encoding='utf-8')
    print(f'Built BOOK.md from {len(CHAPTERS)} source files.')


if __name__ == '__main__':
    build()
