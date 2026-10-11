"""Build the root Markdown book from the chapter sources (standard library only)."""
import posixpath
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = sorted((ROOT / 'chapters').glob('[0-9][0-9]-*.md'))
EXPECTED = [f'{number:02d}' for number in range(10)]


def build():
    if [path.name[:2] for path in CHAPTERS] != EXPECTED:
        raise SystemExit('Expected preface 00 and chapters 01–09, without gaps or duplicates.')
    anchors = {path.name: f'chapter-{path.name[:2]}' for path in CHAPTERS}
    titles = {path.name: path.read_text(encoding='utf-8').splitlines()[0].removeprefix('# ')
              for path in CHAPTERS}
    sections = ['# FDE 案例集：从业务问题到 AI 应用交付\n\n'
                '**Blueberry · 教育卷 0.1 · 审阅稿**\n\n'
                '由 `chapters/` 生成；请修改单章后重新构建。案例与数据为原创合成材料。\n\n'
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
