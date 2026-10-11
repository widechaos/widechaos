"""Render contribution cards from public project records and current GitHub stars."""
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
    for state, url in re.findall(r'^\| \*\*([^*]+)\*\* \| .*?\]\((https://github.com/[^)]+)\)', text, re.M):
        number = re.search(r'/(?:pull|issues|discussions)/(\d+)', url)
        states.append(state + (f' #{number.group(1)}' if number else ''))
    if not states:
        raise ValueError(f'No contribution evidence: {path.name}')
    return dict(slug=path.stem, name=name, repo=repo, caption=captions.get(path.stem, 'Contribution details and upstream evidence'), statuses=states, details=f'contributions/projects/{path.name}')

def get_stars(p):
    result = subprocess.run(['gh', 'api', f'repos/{p["repo"]}'], check=True, text=True, capture_output=True)
    data = json.loads(result.stdout)
    if data['private']:
        raise ValueError('Only public repository metadata is allowed')
    p['stars'] = data['stargazers_count']
    return p

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
        projects = list(pool.map(get_stars, projects))
    OUT.mkdir(parents=True, exist_ok=True)
    for p in projects:
        for theme in PALETTES:
            (OUT / f'{p["slug"]}-{theme}.svg').write_text(render(p, theme))
    (OUT / 'stars.json').write_text(json.dumps({p['repo']: p['stars'] for p in projects}, indent=2) + '\n')
    print(f'Rendered {len(projects)} public contribution cards in both themes')

if __name__ == '__main__':
    main()
