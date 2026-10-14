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
if errors:
    raise SystemExit('\n'.join(errors))
print('Profile references, SVGs and sync boundaries are valid.')
