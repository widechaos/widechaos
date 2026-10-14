"""Apply the approved font hierarchy to controllable SVG modules, preserving animation."""
from pathlib import Path
import re
import hashlib
R=Path(__file__).resolve().parents[1]
mono='SFMono-Regular,Consolas,Liberation Mono,monospace';sans='Avenir Next,Segoe UI,Arial,sans-serif'
paths=[]
for pattern in ['assets/work-*.svg','assets/contact-*.svg','assets/section-*.svg','assets/motion/header-*.svg','assets/motion/identity-panel-*.svg']:
 paths.extend(R.glob(pattern))
for p in paths:
 s=p.read_text().replace('font-family="monospace"',f'font-family="{mono}"').replace('font-family="sans-serif"',f'font-family="{sans}"')
 if p.name.startswith('work-'):
  s=re.sub(r'<text[^>]*font-weight="700"[^>]*>',lambda m:re.sub(r'font-family="[^"]+"',f'font-family="{mono}"',re.sub(r'font-size="(?:20|22)"','font-size="18"',m[0])),s)
 if p.name.startswith('identity-panel'):
  s=s.replace('Arial,PingFang SC,sans-serif','SFMono-Regular,Consolas,Liberation Mono,PingFang SC,Microsoft YaHei,monospace')
  s=s.replace('font-size="13"','font-size="12"')
 p.write_text(s)

print("Applied approved profile typography")

# Content-addressed image paths avoid GitHub raw/CDN serving older fonts.
readme=R/'README.md'
text=readme.read_text()
folder=R/'assets/typography'
folder.mkdir(exist_ok=True)
active=set()
for p in paths:
    data=p.read_bytes()
    name=p.stem+'-'+hashlib.sha256(data).hexdigest()[:12]+'.svg'
    target=folder/name
    target.write_bytes(data)
    active.add(name)
    source=p.relative_to(R).as_posix()
    text=text.replace(source, 'assets/typography/'+name)
    text=re.sub(r'assets/typography/'+re.escape(p.stem)+r'-[0-9a-f]{12}\.svg', 'assets/typography/'+name, text)
for old in folder.glob('*.svg'):
    if old.name not in active:
        old.unlink()
readme.write_text(text)
