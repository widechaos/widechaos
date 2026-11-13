"""Approved light-strength, self-contained cold-blue surface treatment."""
import re


def apply_neon(svg, theme, kind='card'):
    if 'data-neon="light"' in svg:
        return svg
    opening = re.match(r'<svg\b[^>]*>', svg).group()
    view = re.search(r'viewBox="([^"]+)"', opening)
    x, y, width, height = map(float, view.group(1).split())
    # Reserve room inside the image canvas so GitHub cannot clip the outer glow.
    framed = opening.replace(view.group(), f'viewBox="{x-3:g} {y-3:g} {width+7:g} {height+7:g}"')
    framed = framed[:-1] + ' data-neon="light">'
    color = '#169fd8' if theme == 'light' else '#52d9ff'
    definitions = (f'<defs><filter id="surface-neon" x="-15%" y="-20%" width="140%" height="150%" color-interpolation-filters="sRGB">'
                   f'<feDropShadow dx="1" dy="1" stdDeviation="0" flood-color="{color}" flood-opacity=".22"/>'
                   f'<feDropShadow dx="0" dy="1" stdDeviation="1" flood-color="{color}" flood-opacity=".10"/>'
                   '</filter></defs>')
    body = svg[len(opening):svg.rfind('</svg>')]
    if kind == 'section':
        # Only the number frame and separator get light, never the heading text.
        body = re.sub(r'<path\b', '<path filter="url(#surface-neon)"', body)
    else:
        body = '<g filter="url(#surface-neon)">' + body + '</g>'
    return framed + definitions + body + '</svg>\n'
