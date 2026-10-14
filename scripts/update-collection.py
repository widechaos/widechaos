"""Render verified collection artwork into themed frames and replace only its README block.

Catalogs are evidence, not discoveries: this renderer never awards or infers badges.
Original artwork is embedded unchanged; no external image requests run inside SVGs.
"""

from pathlib import Path
import base64
import hashlib
import html
import json
import mimetypes
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/collection"
START = "<!-- COMMUNITY-BADGES:START -->"
END = "<!-- COMMUNITY-BADGES:END -->"


def render(src, alt, kind, url, theme):
    dark = theme == "dark"
    bg = "#161b22" if dark else "#f1f4f8"
    edge = "#394650" if dark else "#cbd5df"
    shine = "#e0fbff" if dark else "#fff"
    accent = "#53dce7" if dark else "#087e8b"
    w = 72 if kind == 0 else 56
    seed = int(hashlib.sha256(src.encode()).hexdigest()[:8], 16)
    dur = 11 + (seed % 9000) / 1000
    phase = (seed >> 12) % 1000 / 1000 * dur
    shape = f'<rect x="1" y="1" width="{w - 2}" height="56" rx="5"/>'
    defs = f'<defs><clipPath id="clip">{shape}</clipPath><linearGradient id="reflection"><stop stop-color="{shine}" stop-opacity="0"/><stop offset=".25" stop-color="{shine}" stop-opacity=".04"/><stop offset=".5" stop-color="{shine}" stop-opacity=".5"/><stop offset=".75" stop-color="{shine}" stop-opacity=".04"/><stop offset="1" stop-color="{shine}" stop-opacity="0"/></linearGradient><filter id="soft-reflection" x="-100%" y="-10%" width="300%" height="120%"><feGaussianBlur stdDeviation="2"/></filter><linearGradient id="neon" x2="1" y2="1"><stop stop-color="{"#30e4f0" if dark else "#087e8b"}"/><stop offset=".5" stop-color="{"#a778ff" if dark else "#7541c8"}"/><stop offset="1" stop-color="{"#ff49c8" if dark else "#c0268c"}"/></linearGradient><filter id="neon-glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.5"/></filter></defs>'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="58" viewBox="0 0 {w} 58"><title>{html.escape(alt)}</title>{defs}<style>@media(prefers-reduced-motion:reduce){{.fx{{display:none}}}}</style><rect x="1" y="1" width="{w - 2}" height="56" rx="5" fill="{bg}" fill-opacity=".65" stroke="{edge}"/><path d="M5 2H{w - 5}" stroke="{shine}" stroke-opacity=".32"/>'
    if kind == 0:
        svg += f'<rect x="4" y="5" width="{w - 8}" height="48" rx="1" fill="#000" opacity=".12"/><image href="{url}" x="5" y="4" width="{w - 10}" height="48" preserveAspectRatio="xMidYMid meet"/>'
    else:
        svg += f'<image href="{url}" x="6" y="7" width="44" height="44"/>'
    if kind == 1:
        svg += f'<g clip-path="url(#clip)"><g class="fx"><animateTransform attributeName="transform" type="translate" values="-50 -30;100 70;100 70" keyTimes="0;{2.5 / dur:.4f};1" dur="{dur:.3f}s" begin="-{phase:.3f}s" repeatCount="indefinite"/><rect x="-9" y="-60" width="18" height="120" transform="rotate(-30)" fill="url(#reflection)" filter="url(#soft-reflection)" opacity=".6"/></g></g>'
    if kind == 2:
        svg += f'<g class="fx" opacity="0"><animate attributeName="opacity" values="0;.9;0;0" keyTimes="0;.1;.3;1" dur="{dur:.3f}s" begin="-{phase:.3f}s" repeatCount="indefinite"/><rect x="2" y="2" width="{w - 4}" height="54" rx="5" fill="none" stroke="url(#neon)" stroke-width="2.5" filter="url(#neon-glow)" opacity=".8"/><rect x="2" y="2" width="{w - 4}" height="54" rx="5" fill="none" stroke="url(#neon)" stroke-width="1.2"/></g>'
    return svg + "</svg>\n"


def artwork(src):
    if not src.startswith("https://"):
        path = (ROOT / src).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError("Artwork escapes the repository")
        data = path.read_bytes()
        mime = mimetypes.guess_type(src)[0]
    else:
        cache = OUT / "source" / hashlib.sha256(src.encode()).hexdigest()
        if cache.exists():
            data = cache.read_bytes()
        else:
            data = urllib.request.urlopen(src, timeout=30).read()
            if len(data) > 5_000_000:
                raise ValueError("Artwork too large")
        if b"<svg" in data[:500]:
            ET.fromstring(data)
            mime = "image/svg+xml"
        elif data.startswith(b"\x89PNG"):
            mime = "image/png"
        elif data[8:12] == b"WEBP":
            mime = "image/webp"
        elif data.startswith(b"\xff\xd8"):
            mime = "image/jpeg"
        else:
            raise ValueError("Unsupported official artwork")
        cache.parent.mkdir(parents=True, exist_ok=True)
        if not cache.exists():
            cache.write_bytes(data)
    return "data:" + mime + ";base64," + base64.b64encode(data).decode()


def collect():
    catalog = json.loads((ROOT / "community-badges.json").read_text())
    reading = json.loads((ROOT / "weread-badges.json").read_text())
    groups = [[], [], [], []]
    for b in sorted(
        catalog["known_badges"], key=lambda b: b.get("display_order", 10000)
    ):
        if not b.get("displayed"):
            continue
        src = b.get("image_url")
        link = b.get("credential_url")
        if not src or not link:
            raise ValueError(
                "Displayed badge needs verified image and credential: " + b["name"]
            )
        kind = (
            0
            if b.get("display_group") == "certificate"
            or src.startswith("assets/certificates/")
            else 1
        )
        groups[kind].append(
            dict(
                src=src,
                alt=b.get("display_alt", b["platform"] + " · " + b["name"]),
                link=b.get("artwork_link", link),
                verify=link,
                kind=kind,
            )
        )
    for index, key in [(2, "selected"), (3, "known_badges")]:
        for b in reading[key]:
            groups[index].append(
                dict(
                    src=b.get("display_asset_path", b["asset_path"]),
                    alt=b["display_name_en"],
                    link="https://weread.qq.com/",
                    kind=2,
                )
            )
    return groups


def generate(groups):
    assets = {}

    def tag(item):
        slug = hashlib.sha256(
            (str(item["kind"]) + ":" + item["src"]).encode()
        ).hexdigest()[:20]
        uri = artwork(item["src"])
        for theme in ("light", "dark"):
            svg = render(item["src"], item["alt"], item["kind"], uri, theme)
            ET.fromstring(svg)
            assets[OUT / (slug + "-" + theme + ".svg")] = svg
        width = 72 if item["kind"] == 0 else 56
        return (
            '<a href="'
            + html.escape(item["link"], quote=True)
            + '"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/collection/'
            + slug
            + '-dark.svg"><img src="assets/collection/'
            + slug
            + '-light.svg" width="'
            + str(width)
            + '" height="58" alt="'
            + html.escape(item["alt"], quote=True)
            + '"></picture></a>'
        )

    rows = []
    for group in groups:
        rows.append(" ".join(tag(item) for item in group))
    verify = (
        "<details>\n<summary>Verify learning credentials</summary>\n\n"
        + "\n".join(
            "- [" + html.escape(i["alt"]) + "](" + i["verify"] + ")" for i in groups[0]
        )
        + "\n\n</details>"
    )
    block = (
        "\n\n<p>"
        + rows[0]
        + "</p>\n\n"
        + verify
        + "\n\n<p>"
        + rows[1]
        + "<br>\n<sub>Kaggle · DEV</sub></p>\n\n<p>"
        + rows[2]
        + "<br>\n<sub>WeRead · Reading milestones</sub></p>\n\n<details><summary>More reading badges</summary>\n\n<p>"
        + rows[3]
        + "</p>\n\n</details>\n\n"
    )
    return assets, block


def main():
    text = (ROOT / "README.md").read_text()
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError("Invalid collection boundaries")
    # Prepare every image before updating the README, so download failures keep it intact.
    assets, block = generate(collect())
    for path, svg in assets.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(svg)
    a = text.index(START) + len(START)
    b = text.index(END)
    (ROOT / "README.md").write_text(text[:a] + block + text[b:])
    print(
        "Rendered themed collection frames; preserved original artwork and evidence links."
    )


if __name__ == "__main__":
    main()
