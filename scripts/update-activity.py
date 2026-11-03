"""Render the public GitHub contribution calendar without account credentials."""
from datetime import date, datetime, timedelta
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/profile/activity'
START, END = '<!-- GITHUB-ACTIVITY:START -->', '<!-- GITHUB-ACTIVITY:END -->'
MONO = 'SFMono-Regular,Consolas,Liberation Mono,monospace'
SANS = 'Avenir Next,Segoe UI,Arial,sans-serif'

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells, self.tips = {}, {}
        self.target = None
        self.heading = ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'td' and 'data-date' in a:
            day = a['data-date']
            if day in self.cells:
                raise ValueError('Duplicate calendar day')
            self.cells[day] = a['id']
        if tag == 'tool-tip' and a.get('for'):
            self.target = a['for']
            self.tips[self.target] = ''
        if tag == 'h2' and a.get('id') == 'js-contribution-activity-description':
            self.target = 'heading'

    def handle_data(self, data):
        if self.target == 'heading':
            self.heading += data
        elif self.target is not None:
            self.tips[self.target] += data

    def handle_endtag(self, tag):
        if tag in ('tool-tip', 'h2'):
            self.target = None

def parse_calendar(html, year):
    parser = Calendar()
    parser.feed(html)
    header = re.fullmatch(r'\s*([\d,]+)\s+contributions?\s+in\s+(\d{4})\s*', parser.heading)
    if not header or int(header[2]) != year:
        raise ValueError('Missing or wrong-year GitHub calendar heading')
    total = int(header[1].replace(',', ''))
    days = []
    for day, cell in sorted(parser.cells.items()):
        d = date.fromisoformat(day)
        if d.year != year:
            continue
        tip = parser.tips.get(cell, '').strip()
        count = re.match(r'(No|[\d,]+) contributions? on ', tip)
        if not count:
            raise ValueError('Missing contribution count for ' + day)
        days.append({'date': day, 'count': 0 if count[1] == 'No' else int(count[1].replace(',', ''))})
    expected = (date(year + 1, 1, 1) - date(year, 1, 1)).days
    if len(days) != expected or sum(d['count'] for d in days) != total:
        raise ValueError('Incomplete calendar or annual/daily count mismatch')
    return total, days

def render(data, dark):
    year, total = data['year'], data['total']
    ink, muted, border = ('#e6edf3', '#9da7b3', '#424a62') if dark else ('#1f2328', '#68717e', '#d7dbe8')
    accent = '#b69aff' if dark else '#7541c8'
    palette = ['#252d3c', '#17484b', '#17696d', '#20979b', '#50d4ca'] if dark else ['#edf0f5', '#c8efeb', '#83d7d0', '#3cb3ae', '#087e8b']
    maximum = max(d['count'] for d in data['days']) or 1
    first = date(year, 1, 1)
    origin = first - timedelta(days=(first.weekday() + 1) % 7)
    cells = []
    for d in data['days']:
        day = date.fromisoformat(d['date'])
        offset = (day - origin).days
        level = 0 if d['count'] == 0 else min(4, 1 + (d['count'] * 3 - 1) // maximum)
        cells.append(f'<rect x="{22 + offset // 7 * 8}" y="{116 + offset % 7 * 8}" width="6" height="6" rx="1" fill="{palette[level]}"><title>{d["date"]}: {d["count"]} contributions</title></rect>')
    desc = f'{total:,} contributions in {year}, from the GitHub contribution calendar. Includes commits, pull requests, issues and reviews; not a commit total.'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="467" height="212" viewBox="0 0 467 212" role="img" aria-labelledby="title desc">
<title id="title">{escape(desc)}</title><desc id="desc">Source: public GitHub profile. Updated {data['updated_on']}.</desc>
<path d="M10 .5H456.5L466.5 10V201L456 211.5H.5V10Z" fill="none" stroke="{border}"/>
<path d="M22 20h24" stroke="{accent}" stroke-width="2"/>
<text x="54" y="24" font-family="{MONO}" font-size="12" fill="{accent}">{year} / GITHUB CONTRIBUTIONS</text>
<text x="22" y="72" font-family="{MONO}" font-size="38" font-weight="700" fill="{ink}">{total:,}</text>
<text x="22" y="96" font-family="{SANS}" font-size="12" fill="{muted}">Commits · pull requests · issues · reviews</text>
{''.join(cells)}
<text x="22" y="192" font-family="{MONO}" font-size="10" fill="{muted}">GITHUB CALENDAR / UPDATED {data['updated_on']}</text>
</svg>'''

def main():
    now = datetime.now(ZoneInfo('Asia/Muscat'))
    year = now.year
    source = f'https://github.com/users/widechaos/contributions?from={year}-01-01&to={year}-12-31'
    with urlopen(Request(source, headers={'User-Agent': 'widechaos-profile-calendar'}), timeout=30) as response:
        total, days = parse_calendar(response.read().decode(), year)
    data = {'year': year, 'total': total, 'updated_on': now.date().isoformat(), 'source': source, 'days': days}
    readme = (ROOT / 'README.md').read_text()
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError('Missing or duplicate activity boundaries')
    assets = {}
    for theme in ('light', 'dark'):
        svg = render(data, theme == 'dark')
        name = f'calendar-{theme}-{hashlib.sha256(svg.encode()).hexdigest()[:12]}.svg'
        assets[name] = svg
    light, dark = assets.keys()
    link = f'https://github.com/widechaos?tab=overview&amp;from={year}-01-01&amp;to={year}-12-31'
    block = f'\n<p><a href="{link}"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/profile/activity/{dark}"><img src="assets/profile/activity/{light}" width="467" alt="{year} GitHub contributions: {total:,}. Includes commits, pull requests, issues and reviews."></picture></a></p>\n'
    updated = readme[:readme.index(START) + len(START)] + block + readme[readme.index(END):]
    # Fetch and validate before touching any current output; a failed run keeps the last snapshot.
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg in assets.items():
        (OUT / name).write_text(svg)
    (OUT / 'calendar.json').write_text(json.dumps(data, indent=2) + '\n')
    (ROOT / 'README.md').write_text(updated)
    for old in OUT.glob('calendar-*.svg'):
        if old.name not in assets:
            old.unlink()
    print(f'{year}: {total:,} GitHub contributions; annual/daily totals agree.')

if __name__ == '__main__':
    main()
