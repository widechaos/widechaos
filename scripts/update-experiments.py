"""Render a bounded tool shelf and the complete, evidence-preserving experiment directory."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from profile_neon import apply_neon
import hashlib
import html
import json
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- EXPERIMENTS:START -->"
END = "<!-- EXPERIMENTS:END -->"
MONO = "SFMono-Regular,Consolas,Liberation Mono,monospace"
SANS = "Avenir Next,Segoe UI,Arial,sans-serif"


def validate(items):
    ids, targets = set(), set()
    for item in items:
        key, target = item['id'], item['href']
        if not re.fullmatch(r'[a-z][a-z0-9-]*', key) or key in ids:
            raise ValueError('Experiment ids must be unique stable work keys')
        if urlsplit(target).scheme != 'https' or not urlsplit(target).netloc or target in targets:
            raise ValueError('Experiment links must be distinct public HTTPS targets')
        ids.add(key)
        targets.add(target)
        for field in ('name', 'alt', 'details'):
            if not item.get(field):
                raise ValueError('Missing experiment ' + field)
    return items


def featured_items(catalog, items):
    keys = catalog['showcase']['featured']
    lookup = {i['id']: i for i in items}
    if not 1 <= len(keys) <= 3 or len(keys) != len(set(keys)) or any(k not in lookup for k in keys):
        raise ValueError('Curate at most three distinct existing tools; do not auto-promote new works')
    result = [lookup[k] for k in keys]
    for item in result:
        card = item['shelf_card']
        if len(card['lines']) != 2 or any(not card.get(k) for k in ('kind', 'title', 'note', 'glyph')):
            raise ValueError('Featured tools need a purpose, two description lines and a practical limit')
    return result


def render(item, theme, mobile=False):
    width, height = (300 if mobile else 270), 178
    dark = theme == 'dark'
    bg, edge, ink, muted, accent, purple = (
        ('#0d1117', '#34374f', '#edf2f8', '#adb6c6', '#64d8d5', '#c3a7fa') if dark else
        ('#fbfcff', '#d8ddeb', '#1f2328', '#536172', '#087e8b', '#7541c8'))
    card = item['shelf_card']
    label = f"{card['title']}. {item['summary']} {card['note']}"
    def text(value, x, y, size, color, family=SANS, weight=400):
        return f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" font-weight="{weight}">{html.escape(value)}</text>'
    glyphs = {
        'search': '<circle cx="0" cy="-2" r="5"/><path d="m4 2 5 5M-9 11H9"/>',
        'split': '<path d="M-9 0H0M0 0V-7H9M0 0V7H9"/><rect x="-13" y="-3" width="5" height="6"/><path d="M9-9v4M9 5v4"/>',
        'audit': '<path d="M-10 7V-5M-3 7V1M4 7V-9M11 7V-2M-12 11H13"/>'}
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{html.escape(label)}</title>
<defs><pattern id="grid" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M12 0H0V12" fill="none" stroke="{accent}" stroke-opacity=".035"/></pattern><linearGradient id="rail"><stop stop-color="{accent}"/><stop offset="1" stop-color="{purple}"/></linearGradient></defs>
<path d="M10 1H{width-13}L{width-1} 13V{height-10}L{width-10} {height-1}H1V10Z" fill="{bg}" stroke="{edge}"/>
<path d="M10 1H{width-13}L{width-1} 13V{height-10}L{width-10} {height-1}H1V10Z" fill="url(#grid)"/>
<path d="M1 32V10L10 1H56" fill="none" stroke="{accent}" stroke-width="2"/>
<path d="M16 36H{width-16}" stroke="{edge}"/>
<g transform="translate({width-28} 19)" fill="none" stroke="{accent}" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">{glyphs[card['glyph']]}</g>'''
    svg += text(card['kind'], 16, 24, 9.5, purple, MONO)
    svg += text(card['title'], 16, 61, 17, ink, SANS, 650)
    for line, y in zip(card['lines'], (84, 102)):
        svg += text(line, 16, y, 12.5, muted)
    svg += text(card['note'], 16, 125, 10.5, muted)
    svg += f'<path d="M16 139H{width-16}" stroke="url(#rail)" stroke-opacity=".45"/>'
    short_name = {'split-boundary-audit': 'Split Boundary Audit'}.get(item['id'], item['name'])
    svg += text(short_name, 16, 161, 10, purple, MONO)
    svg += text('↗', width-31, 162, 16, accent, SANS)
    return apply_neon(svg + '</svg>', theme)


def assets_for(item):
    refs, payloads = {}, {}
    for theme in ('light', 'dark'):
        for mobile in (False, True):
            svg = render(item, theme, mobile)
            suffix = '-mobile' if mobile else ''
            path = f"assets/experiments/shelf-{item['id']}-{theme}{suffix}-{hashlib.sha256(svg.encode()).hexdigest()[:12]}.svg"
            refs[theme + ('_mobile' if mobile else '')] = path
            payloads[path] = svg
    return refs, payloads


def block(items, featured, refs):
    cards = []
    for item, paths in zip(featured, refs):
        esc = lambda s: html.escape(s, quote=True)
        alt = item['shelf_card']['title'] + '. ' + item['summary'] + ' ' + item['shelf_card']['note']
        cards.append(f'<a href="{esc(item["href"])}"><picture>'
                     f'<source media="(prefers-color-scheme: dark) and (max-width:520px)" srcset="{paths["dark_mobile"]}" width="300" height="178">'
                     f'<source media="(max-width:520px)" srcset="{paths["light_mobile"]}" width="300" height="178">'
                     f'<source media="(prefers-color-scheme: dark)" srcset="{paths["dark"]}">'
                     f'<img src="{paths["light"]}" width="32%" alt="{esc(alt)}"></picture></a>')
    # New entries remain discoverable without growing the default front shelf.
    directory = '\n'.join(f'- [{i["name"]}]({i["href"]}) — {i.get("summary") or " ".join(i.get("question", ["Read the experiment and its limitations."]))}' for i in items)
    def result_summary(item):
        if 'legacy_assets' in item:
            return item['alt']
        return f"{item['result_label']}: {item['result']}. {'; '.join(item['limits'])}."
    details = '\n'.join(f'- **{i["name"]}:** {result_summary(i)} {i["details"]}' for i in items)
    return ('Small tools for inspecting text, datasets and model results. Pick a task to explore.\n\n<p>\n' + '\n'.join(cards) +
            '\n</p>\n\n<details>\n<summary>Explore all experiments</summary>\n\n' + directory +
            '\n\n<details>\n<summary>Methods, results &amp; limits</summary>\n\n' + details + '\n\n</details>\n\n</details>')


def replace_block(readme, content):
    if readme.count(START) != 1 or readme.count(END) != 1 or readme.index(START) >= readme.index(END):
        raise ValueError('Missing or ambiguous experiment boundaries')
    before, rest = readme.split(START)
    _, after = rest.split(END)
    return before + START + '\n' + content + '\n' + END + after


def main():
    catalog = json.loads((ROOT / 'experiments.json').read_text())
    items = validate(catalog['items'])
    featured = featured_items(catalog, items)
    refs, payloads = [], {}
    for item in featured:
        paths, generated = assets_for(item)
        refs.append(paths)
        payloads.update(generated)
    readme = ROOT / 'README.md'
    updated = replace_block(readme.read_text(), block(items, featured, refs))
    for path, svg in payloads.items():
        (ROOT / path).write_text(svg)
    # Retain source/legacy artwork; clean only obsolete front-shelf derivatives.
    for path in (ROOT / 'assets/experiments').glob('shelf-*.svg'):
        if path.relative_to(ROOT).as_posix() not in payloads:
            path.unlink()
    readme.write_text(updated)
    print(f'Rendered {len(featured)} curated tools; {len(items)} experiments retained in folded directory.')


if __name__ == '__main__':
    main()
