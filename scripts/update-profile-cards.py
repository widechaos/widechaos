"""Render contribution cards from public project records and current GitHub stars and PR states."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import html
from datetime import datetime
import hashlib
import json
import re
import subprocess
import textwrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/profile/contributions'
PALETTES = {
    'light': ('#fbfaff', '#1f2328', '#59636e', '#d9d1e8', '#087e8b', '#b32c83', '#7541c8'),
    'dark': ('#11131e', '#f0f6fc', '#aab4c2', '#37354f', '#4ee5dd', '#f66eb9', '#bb9aff'),
}

def project(path, captions):
    text = path.read_text()
    name = re.search(r'^# (.+)$', text, re.M).group(1)
    repo = re.search(r'\[Upstream repository\]\(https://github.com/([^/)]+/[^/)]+)\)', text).group(1)
    if 'estidama' in repo.lower():
        raise ValueError('Employer repositories are excluded')
    states = []
    evidence = []
    for state, url in re.findall(r'^\| \*\*([^*]+)\*\* \| .*?\]\((https://github.com/[^)]+)\)', text, re.M):
        number = re.search(r'/(?:pull|issues|discussions)/(\d+)', url)
        evidence.append(dict(status=state, url=url, number=number.group(1) if number else None))
        states.append(state + (f' #{number.group(1)}' if number else ''))
    if not states:
        raise ValueError(f'No contribution evidence: {path.name}')
    return dict(slug=path.stem, name=name, repo=repo, caption=captions.get(path.stem, 'Contribution details and upstream evidence'), statuses=states, evidence=evidence, details=f'contributions/projects/{path.name}')

def api(endpoint):
    result = subprocess.run(['gh', 'api', endpoint], check=True, text=True,
                            capture_output=True, timeout=45)
    return json.loads(result.stdout)


def pr_status(data):
    if data.get('merged'):
        return 'Merged'
    if data['state'] == 'closed':
        return 'Closed · unmerged'
    if data['state'] == 'open':
        return 'Draft' if data.get('draft') else 'Under review'
    raise ValueError('Unrecognized PR state')


def get_metadata(p):
    data = api(f'repos/{p["repo"]}')
    if data['private']:
        raise ValueError('Only public repository metadata is allowed')
    p['stars'] = data['stargazers_count']
    for item in p['evidence']:
        match = re.fullmatch(r'https://github.com/([^/]+/[^/]+)/pull/(\d+)', item['url'])
        if not match:
            # Fetch dates only: human-verified report attribution stays unchanged.
            other = re.fullmatch(r'https://github.com/([^/]+/[^/]+)/(issues|discussions)/(\d+)', item['url'])
            if not other or other[1].lower() != p['repo'].lower():
                raise ValueError('Unrecognized contribution evidence URL')
            repo, kind, number = other.groups()
            if kind == 'issues':
                data = api(f'repos/{repo}/issues/{number}')
                item['sort_date'] = (data.get('closed_at') if item['status'].startswith('Resolved') else None) or data['created_at']
            else:
                owner, name = repo.split('/')
                query = 'query { repository(owner: "' + owner + '", name: "' + name + '") { discussion(number: ' + number + ') { createdAt } } }'
                result = subprocess.run(['gh', 'api', 'graphql', '-f', 'query=' + query], check=True, capture_output=True, text=True, timeout=45)
                item['sort_date'] = json.loads(result.stdout)['data']['repository']['discussion']['createdAt']
            continue
        repo, number = match.groups()
        if repo.lower() != p['repo'].lower():
            raise ValueError('PR evidence must belong to the recorded public repository')
        data = api(f'repos/{repo}/pulls/{number}')
        if data['user']['login'].lower() != 'widechaos':
            raise ValueError('PR author does not match the profile owner')
        item['status'] = pr_status(data)
        item['live_pr'] = True
        item['sort_date'] = data.get('merged_at') or data.get('closed_at') or data['created_at']
    p['evidence'].sort(key=evidence_order)
    p['statuses'] = [item['status'] + (f" #{item['number']}" if item['number'] else '')
                     for item in p['evidence']]
    return p


def status_rank(status):
    for prefix, rank in [('Merged', 0), ('Resolved', 1), ('Under review', 2), ('Draft', 2), ('Discussion', 3), ('Closed', 4)]:
        if status.startswith(prefix):
            return rank
    raise ValueError('Unrecognized contribution status: ' + status)


def evidence_order(item):
    # Status milestones or original submission dates, never comment/repository activity.
    date = item.get('sort_date')
    timestamp = datetime.fromisoformat(date.replace('Z', '+00:00')).timestamp() if date else 0
    return status_rank(item['status']), -timestamp, item['url']


def project_order(p):
    if not p.get('evidence'):
        raise ValueError('Missing contribution sorting evidence')
    rank = min(status_rank(i['status']) for i in p['evidence'])
    relevant = [i for i in p['evidence'] if status_rank(i['status']) == rank]
    return min(evidence_order(i)[:2] for i in relevant) + (p['slug'],)


def sync_status_text(text, projects):
    # Replace only the label paired with the exact previously verified PR URL.
    for p in projects:
        for item in p['evidence']:
            if not item.get('live_pr'):
                continue
            url = re.escape(item['url'])
            row = re.compile(r'(^\| \*\*)[^*]+(\*\* \| .*?\]\(' + url + r'\))', re.M)
            text = row.sub(lambda m: m[1] + item['status'] + m[2], text)
            index = re.compile(r'\*\*[^*]+\*\*( · \[#\d+\]\(' + url + r'\))')
            text = index.sub(lambda m: '**' + item['status'] + '**' + m[1], text)
    return text


def status_visual(state, theme):
    light = theme == 'light'
    if state.startswith('Merged'):
        return ('#7541c8' if light else '#c9a0ff', 'Merged', 'M4 3v10m0-7c7 0 7 5 7 7M8 10l3 3 3-3', [(4, 2), (4, 14)])
    if state.startswith('Under review'):
        return ('#916300' if light else '#f2cc60', 'Review', 'M4 4v9M12 13V6c0-3-4-3-4-3m0 0 2-2M8 3l2 2', [(4, 2), (4, 14), (12, 14)])
    if state.startswith('Discussion'):
        return ('#087e8b' if light else '#65dfeb', 'Discussion', 'M2 2h12v9H7l-4 3v-3H2ZM5 5h6M5 8h4', [])
    if state.startswith('Resolved'):
        return ('#16734c' if light else '#7ee7b3', 'Report resolved', 'M4 8l3 3 5-6', [(8, 8, 7)])
    if state.startswith('Closed'):
        return ('#656d76' if light else '#aab4c2', 'Unmerged', 'M4 4l8 8M12 4l-8 8', [(8, 8, 7)])
    return ('#656d76' if light else '#aab4c2', state.split(' #')[0], 'M3 8h10M9 4l4 4-4 4', [])


def render(p, theme):
    bg, fg, muted, border, cyan, pink, purple = PALETTES[theme]
    esc = html.escape
    light = theme == 'light'
    stars = str(p['stars']) if p['stars'] < 1000 else f'{p["stars"]/1000:.1f}k'
    states = p['statuses'][:2]
    if len(p['statuses']) > 2:
        states = [p['statuses'][0], f'+{len(p["statuses"])-1} · Details →']
    bg = '#eaf0f6' if light else bg
    shine = '#ffffff' if light else '#c7f8ff'
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="230" height="136" viewBox="0 0 230 136"><title>{esc(p["name"])} contribution details: {esc("; ".join(p["statuses"]))}</title>',
        f'<defs><linearGradient id="badge-sheen"><stop stop-color="{shine}" stop-opacity="0"/><stop offset=".48" stop-color="{shine}" stop-opacity=".15"/><stop offset=".6" stop-color="{shine}" stop-opacity=".9"/><stop offset="1" stop-color="{shine}" stop-opacity="0"/></linearGradient></defs>',
        '<style>@media(prefers-reduced-motion:reduce){.sheen{display:none}}</style>',
        f'<path d="M1 1H215L229 15V135H15L1 121Z" fill="{bg}" fill-opacity="{.8 if light else .64}" stroke="{border}"/>',
        (f'<path d="M3 32V3H213L227 17" fill="none" stroke="#8192a5" stroke-opacity=".16" stroke-width="2"/>' if light else ''),
        f'<path d="M1 29V1H31M201 1H215L229 15V29" fill="none" stroke="{cyan}" stroke-width="2"/>',
        f'<path d="M200 135H229V107" fill="none" stroke="{pink}" stroke-width="2"/>',
        f'<g font-family="Avenir Next,Segoe UI,Arial,sans-serif"><text x="13" y="27" fill="{fg}" font-family="SFMono-Regular,Consolas,Liberation Mono,monospace" font-size="14" font-weight="700" letter-spacing="-.35">{esc(p["name"])}</text>',
        f'<text x="216" y="27" text-anchor="end" fill="{purple}" font-family="SFMono-Regular,Consolas,Liberation Mono,monospace" font-size="11.5">★ {stars}</text>']
    for j, line in enumerate(textwrap.wrap(p['caption'], width=29)[:2]):
        svg.append(f'<text x="13" y="{49+j*16}" fill="{muted}" font-size="12.5">{esc(line)}</text>')
    for j, state in enumerate(states):
        y = 100+j*19
        if state.startswith('+'):
            svg.append(f'<text x="14" y="{y}" fill="{muted}" font-family="SFMono-Regular,Consolas,Liberation Mono,monospace" font-size="11">{esc(state)}</text>')
            continue
        color, label, path, circles = status_visual(state, theme)
        number = re.search(r'#(\d+)', state)
        label += f' #{number.group(1)}' if number else ''
        badge_width = min(202, 29 + len(label) * 6.6)
        svg.append(f'<defs><clipPath id="badge-{j}"><rect x="10" y="{y-14}" width="{badge_width}" height="18" rx="4"/></clipPath></defs>')
        svg.append(f'<rect x="10" y="{y-14}" width="{badge_width}" height="18" rx="4" fill="{color}" fill-opacity=".07" stroke="{color}" stroke-opacity=".18" stroke-width=".6"/>')
        timing = int.from_bytes(hashlib.sha256(f"{p['slug']}:{state}:{j}".encode()).digest()[:4], 'big')
        duration = 7 + (timing % 6001) / 1000
        offset = ((timing >> 12) % 10000) / 10000 * duration
        sweep_end = round(2.25 / duration, 4)
        svg.append(f'<g clip-path="url(#badge-{j})"><g class="sheen" opacity=".85"><animateTransform attributeName="transform" type="translate" values="-55 {y-42};{badge_width+35} {y+8};{badge_width+35} {y+8}" keyTimes="0;{sweep_end};1" dur="{duration:.3f}s" begin="-{offset:.3f}s" repeatCount="indefinite"/><rect x="-24" y="-35" width="48" height="70" transform="rotate(-25)" fill="url(#badge-sheen)"/></g></g>')
        svg.append(f'<g transform="translate(13 {y-12})" fill="none" stroke="{color}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="{path}"/>')
        for circle in circles:
            x, cy, *radius = circle
            svg.append(f'<circle cx="{x}" cy="{cy}" r="{radius[0] if radius else 1.7}"/>')
        svg.append(f'</g><text x="35" y="{y}" fill="{color}" font-family="SFMono-Regular,Consolas,Liberation Mono,monospace" font-size="11">{esc(label)}</text>')
    return ''.join(svg) + '</g></svg>\n'

def sync_grid(text, projects):
    start = '<!-- OPEN-SOURCE-CONTRIBUTIONS:START -->'
    end = '<!-- OPEN-SOURCE-CONTRIBUTIONS:END -->'
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError('Invalid contribution grid boundaries')
    a = text.index(start) + len(start)
    b = text.index(end)
    known = {p['slug']: p for p in projects}
    existing = re.findall(r'href="contributions/projects/([^"/]+)\.md"', text[a:b])
    missing = set(existing) - set(known)
    if missing:
        raise ValueError('Missing contribution evidence: ' + ', '.join(sorted(missing)))
    order = [p['slug'] for p in sorted(projects, key=project_order)]
    links = []
    for slug in order:
        if slug not in known:
            raise ValueError('Missing contribution evidence: ' + slug)
        p = known[slug]
        base = 'assets/profile/contributions/' + slug
        light = base + '-light-' + hashlib.sha256(render(p, 'light').encode()).hexdigest()[:12] + '.svg'
        dark = base + '-dark-' + hashlib.sha256(render(p, 'dark').encode()).hexdigest()[:12] + '.svg'
        alt = html.escape(p['name'] + ' — ' + p['caption'], quote=True)
        links.append(f'<a href="contributions/projects/{slug}.md"><picture><source media="(prefers-color-scheme: dark) and (max-width:520px)" srcset="{dark}" width="300" height="177"><source media="(max-width:520px)" srcset="{light}" width="300" height="177"><source media="(prefers-color-scheme: dark)" srcset="{dark}"><img src="{light}" width="205" alt="{alt}"></picture></a>')
    block = '\n<p>\n' + '\n'.join(links) + '\n</p>\n\n[Contribution details →](contributions/README.md)\n\n'
    return text[:a] + block + text[b:]


def main():
    captions = json.loads((ROOT / 'profile-card-captions.json').read_text())
    paths = sorted((ROOT / 'contributions/projects').glob('*.md'))
    # Complete fetching before replacing any last-known-good output.
    projects = [project(p, captions) for p in paths]
    with ThreadPoolExecutor(max_workers=4) as pool:
        projects = list(pool.map(get_metadata, projects))
    updates = {}
    for path in (ROOT / 'contributions').rglob('*.md'):
        before = path.read_text()
        after = sync_status_text(before, projects)
        if after != before:
            updates[path] = after
    OUT.mkdir(parents=True, exist_ok=True)
    for p in projects:
        for theme in PALETTES:
            svg = render(p, theme)
            (OUT / f'{p["slug"]}-{theme}.svg').write_text(svg)
            digest = hashlib.sha256(svg.encode()).hexdigest()[:12]
            filename = f'{p["slug"]}-{theme}-{digest}.svg'
            (OUT / filename).write_text(svg)
            for old in OUT.glob(f'{p["slug"]}-{theme}-*.svg'):
                if re.fullmatch(re.escape(p['slug'] + '-' + theme) + r'-[0-9a-f]{12}\.svg', old.name) and old.name != filename:
                    old.unlink()
    (OUT / 'stars.json').write_text(json.dumps({p['repo']: p['stars'] for p in projects}, indent=2) + '\n')
    snapshot = {p['repo']: p['evidence'] for p in projects}
    (OUT / 'status.json').write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + '\n')
    for path, text in updates.items():
        path.write_text(text)
    readme = ROOT / 'README.md'
    readme.write_text(sync_grid(readme.read_text(), projects))
    print(f'Rendered {len(projects)} public contribution cards in both themes')

if __name__ == '__main__':
    main()
