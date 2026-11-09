"""Render the approved experiment catalog; publication evidence is supplied by its owner."""
from pathlib import Path
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
        key, target = item["id"], item["href"]
        if not re.fullmatch(r"[a-z][a-z0-9-]*", key) or key in ids:
            raise ValueError("Experiment ids must be unique stable work keys")
        if urlsplit(target).scheme != "https" or not urlsplit(target).netloc or target in targets:
            raise ValueError("Experiment links must be distinct public HTTPS targets")
        ids.add(key)
        targets.add(target)
        for field in ("name", "alt", "details"):
            if not item.get(field):
                raise ValueError("Missing experiment " + field)
        if "legacy_assets" not in item:
            if len(item["question"]) != 2 or len(item["limits"]) != 2:
                raise ValueError("Keep the approved two-line question and limits")
    return items


def render(item, theme, mobile=False):
    width, height = (300, 282) if mobile else (420, 258)
    dark = theme == "dark"
    bg, edge = ("#0d1117", "#39394f") if dark else ("#ffffff", "#d9cdee")
    ink, muted = ("#edf2f8", "#a5b0c0") if dark else ("#1f2328", "#59636e")
    accent, purple = ("#64d8d5", "#c3a7fa") if dark else ("#087e8b", "#7541c8")
    def text(value, y, size, color, family=SANS, weight=400):
        return (f'<text x="18" y="{y}" fill="{color}" font-family="{family}" '
                f'font-size="{size}" font-weight="{weight}">{html.escape(value)}</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" role="img"><title>{html.escape(item["alt"])}</title>'
           f'<path d="M12 1H{width-17}L{width-1} 17V{height-12}L{width-12} {height-1}H1V12Z" '
           f'fill="{bg}" stroke="{edge}"/>'
           f'<path d="M1 34V12L12 1H52" fill="none" stroke="{accent}" stroke-width="2"/>')
    svg += text(item["eyebrow"], 26, 10.5, purple, MONO)
    svg += text(item["headline"], 56, 16 if mobile else 18, ink, MONO, 700)
    for value, y in zip(item["question"], (82, 101)):
        svg += text(value, y, 13 if mobile else 14, muted)
    svg += text(item["result"], 140, 27, accent, MONO, 600)
    svg += text(item["result_label"], 161, 11.5, muted)
    for value, y in zip(item["limits"], (187, 204)):
        svg += text(value, y, 11.5, muted)
    svg += f'<path d="M18 {height-37}H{width-18}" stroke="{edge}"/>'
    svg += text(item["cta"], height-15, 11.5, purple, MONO)
    return svg + "</svg>"


def assets_for(item):
    if "legacy_assets" in item:
        return item["legacy_assets"], {}
    refs, payloads = {}, {}
    for theme in ("light", "dark"):
        for mobile in (False, True):
            svg = render(item, theme, mobile)
            suffix = "-mobile" if mobile else ""
            path = f'assets/experiments/{item["id"]}-{theme}{suffix}-{hashlib.sha256(svg.encode()).hexdigest()[:12]}.svg'
            refs[theme + ("_mobile" if mobile else "")] = path
            payloads[path] = svg
    return refs, payloads


def block(items, refs):
    cards = []
    for item, paths in zip(items, refs):
        esc = lambda s: html.escape(s, quote=True)
        cards.append(f'<a href="{esc(item["href"])}"><picture>'
                     f'<source media="(prefers-color-scheme: dark) and (max-width:520px)" srcset="{paths["dark_mobile"]}" width="300" height="282">'
                     f'<source media="(max-width:520px)" srcset="{paths["light_mobile"]}" width="300" height="282">'
                     f'<source media="(prefers-color-scheme: dark)" srcset="{paths["dark"]}">'
                     f'<img src="{paths["light"]}" width="49%" alt="{esc(item["alt"])}"></picture></a>')
    details = "\n".join(f'- **{item["name"]}:** {item["details"]}' for item in items)
    return ("<p>\n" + "\n".join(cards) + "\n</p>\n\n<details>\n"
            "<summary>Setup, limits &amp; reproduction</summary>\n\n" + details + "\n\n</details>")


def replace_block(readme, content):
    if readme.count(START) != 1 or readme.count(END) != 1 or readme.index(START) >= readme.index(END):
        raise ValueError("Missing or ambiguous experiment boundaries")
    before, rest = readme.split(START)
    _, after = rest.split(END)
    return before + START + "\n" + content + "\n" + END + after


def main():
    items = validate(json.loads((ROOT / "experiments.json").read_text())["items"])
    refs, payloads = [], {}
    for item in items:
        paths, generated = assets_for(item)
        refs.append(paths)
        payloads.update(generated)
        for path in paths.values():
            if not path.startswith("assets/experiments/") or ".." in Path(path).parts:
                raise ValueError("Experiment artwork must stay in its asset directory")
            if path not in generated and not (ROOT / path).is_file():
                raise ValueError("Missing preserved experiment artwork: " + path)
    readme = ROOT / "README.md"
    updated = replace_block(readme.read_text(), block(items, refs))
    for path, svg in payloads.items():
        (ROOT / path).write_text(svg)
    # Only replace old generated versions of catalog-owned cards. Legacy artwork is immutable here.
    for item in items:
        if "legacy_assets" not in item:
            for path in (ROOT / "assets/experiments").glob(item["id"] + "-*.svg"):
                if path.relative_to(ROOT).as_posix() not in payloads:
                    path.unlink()
    readme.write_text(updated)
    print(f'Rendered {len(items)} approved experiments; preserved other README sections.')


if __name__ == "__main__":
    main()
