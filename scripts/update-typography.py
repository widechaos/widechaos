"""Apply the approved font hierarchy to controllable SVG modules, preserving animation."""
from pathlib import Path
import re
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
