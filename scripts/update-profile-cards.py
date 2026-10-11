"""Render contribution cards from public project records and current GitHub stars and PR states."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import html
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
            # Reports and discussions need human attribution; closure is not proof of a fix.
            continue
        repo, number = match.groups()
        if repo.lower() != p['repo'].lower():
            raise ValueError('PR evidence must belong to the recorded public repository')
        data = api(f'repos/{repo}/pulls/{number}')
        if data['user']['login'].lower() != 'widechaos':
            raise ValueError('PR author does not match the profile owner')
        item['status'] = pr_status(data)
        item['live_pr'] = True
    p['statuses'] = [item['status'] + (f" #{item['number']}" if item['number'] else '')
                     for item in p['evidence']]
    return p


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


def render(p, theme):
    bg, fg, muted, border, cyan, pink, purple = PALETTES[theme]
    esc = html.escape
    stars = str(p['stars']) if p['stars'] < 1000 else f'{p["stars"]/1000:.1f}k'
    states = p['statuses'][:2]
    if len(p['statuses']) > 2:
        states = [p['statuses'][0], f'+ {len(p["statuses"])-1} more · Details']
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="230" height="136" viewBox="0 0 230 136"><title>{esc(p["name"])} contribution details</title>',
        f'<path d="M1 1H215L229 15V135H15L1 121Z" fill="{bg}" stroke="{border}"/>',
        f'<path d="M1 29V1H31M201 1H215L229 15V29" fill="none" stroke="{cyan}" stroke-width="2"/>',
        f'<path d="M200 135H229V107" fill="none" stroke="{pink}" stroke-width="2"/>',
        f'<g font-family="Arial,sans-serif"><text x="13" y="27" fill="{fg}" font-size="16" font-weight="700">{esc(p["name"])}</text>',
        f'<text x="216" y="27" text-anchor="end" fill="{purple}" font-size="13">★ {stars}</text>']
    for j, line in enumerate(textwrap.wrap(p['caption'], width=29)):
        svg.append(f'<text x="13" y="{52+j*17}" fill="{muted}" font-size="13">{esc(line)}</text>')
    for j, state in enumerate(states):
        color = ('#1a7f37' if theme == 'light' else '#7ee787') if state.startswith('Merged') else ('#0969da' if theme == 'light' else '#79c0ff') if state.startswith('Resolved') else purple if state.startswith('Discussion') else ('#8b5b00' if theme == 'light' else '#e3b341') if state.startswith('Under review') else muted
        svg.append(f'<text x="13" y="{103+j*17}" fill="{color}" font-size="13">{esc(state)}</text>')
    return ''.join(svg) + '</g></svg>\n'

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
            (OUT / f'{p["slug"]}-{theme}.svg').write_text(render(p, theme))
    (OUT / 'stars.json').write_text(json.dumps({p['repo']: p['stars'] for p in projects}, indent=2) + '\n')
    snapshot = {p['repo']: p['evidence'] for p in projects}
    (OUT / 'status.json').write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + '\n')
    for path, text in updates.items():
        path.write_text(text)
    print(f'Rendered {len(projects)} public contribution cards in both themes')

if __name__ == '__main__':
    main()
