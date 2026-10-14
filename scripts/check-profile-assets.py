"""Check profile references and the boundaries used by automated synchronizers."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('src', 'srcset', 'href') and value:
                self.paths.add(value)

text = (ROOT / 'README.md').read_text()
refs = References()
refs.feed(text)
refs.paths.update(re.findall(r'\]\(([^)]+)\)', text))
errors = []
for boundary in ('COMMUNITY-BADGES', 'OPEN-SOURCE-CONTRIBUTIONS'):
    start, end = f'<!-- {boundary}:START -->', f'<!-- {boundary}:END -->'
    if text.count(start) != 1 or text.count(end) != 1 or text.find(start) > text.find(end):
        errors.append(f'Invalid sync boundary: {boundary}')
# Contribution cards must flow naturally when projects are inserted or reordered.
contributions = re.search(
    r'<!-- OPEN-SOURCE-CONTRIBUTIONS:START -->(.*?)<!-- OPEN-SOURCE-CONTRIBUTIONS:END -->',
    text, re.S,
)
if contributions:
    grid = contributions.group(1)
    if re.search(r'<br\s*/?>', grid, re.I):
        errors.append('Contribution cards must wrap naturally; remove hard-coded line breaks')
    if re.search(r'</a>[^<]*\n\s*\n\s*<a', grid):
        errors.append('Contribution cards must remain in one continuous paragraph')
collection = re.search(r'<!-- COMMUNITY-BADGES:START -->(.*?)<!-- COMMUNITY-BADGES:END -->', text, re.S)
if collection:
    block = collection.group(1)
    import json
    community = json.loads((ROOT / 'community-badges.json').read_text())
    reading = json.loads((ROOT / 'weread-badges.json').read_text())
    expected = sum(bool(b.get('displayed')) for b in community['known_badges']) + len(reading['selected']) + len(reading['known_badges'])
    if len(re.findall(r'<img src="assets/collection/', block)) != expected or '<kbd>' in block:
        errors.append('Collection styles out of sync: run python3 scripts/update-collection.py')
for value in sorted(refs.paths):
    url = urlsplit(value)
    if url.scheme or url.netloc or not url.path:
        continue
    path = (ROOT / unquote(url.path)).resolve()
    if not path.is_relative_to(ROOT) or not path.exists():
        errors.append(f'Missing local target: {value}')
    elif path.suffix == '.svg':
        try:
            ET.parse(path)
        except ET.ParseError as error:
            errors.append(f'Invalid SVG {value}: {error}')
# Guard the approved font hierarchy against older regenerators.
for pattern in ('assets/work-*.svg', 'assets/contact-*.svg', 'assets/section-*.svg', 'assets/motion/header-*.svg', 'assets/motion/identity-panel-*.svg'):
    for path in ROOT.glob(pattern):
        svg = path.read_text()
        if 'font-family="monospace"' in svg or 'font-family="sans-serif"' in svg or 'font-family="Arial,PingFang SC,sans-serif"' in svg:
            errors.append(f'Typography out of sync: {path.relative_to(ROOT)}; run scripts/update-typography.py')
if errors:
    raise SystemExit('\n'.join(errors))
print('Profile references, SVGs and sync boundaries are valid.')
