from __future__ import annotations

from profile_config import CONTACT_ROWS, DISPLAY_NAME, INFO_ROWS, PROJECT_ROWS
from svg_utils import ROOT, esc, svg_header, write_text


def main() -> None:
    width = 560
    height = 330
    rows = INFO_ROWS + [("Projects", PROJECT_ROWS[0]), ("Links", CONTACT_ROWS[0][1])]
    row_markup = []
    y = 92
    for i, (key, value) in enumerate(rows):
        delay = 0.2 + i * 0.16
        row_markup.append(
            f'    <g opacity="0" transform="translate(0 8)">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.25s" begin="{delay:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 8" to="0 0" dur="0.25s" begin="{delay:.2f}s" fill="freeze"/>'
            f'<text x="34" y="{y}" fill="#39d353">{esc(key)}</text>'
            f'<text x="154" y="{y}" fill="#f0f6fc">{esc(value)}</text></g>'
        )
        y += 30

    svg = f"""{svg_header(width, height)}
  <rect width="100%" height="100%" rx="12" fill="#0d1117"/>
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="none" stroke="#30363d"/>
  <g font-family="Consolas, Monaco, 'Courier New', monospace">
    <text x="34" y="42" font-size="16" fill="#8b949e">bernardo@github</text>
    <text x="34" y="66" font-size="21" fill="#f0f6fc">{esc(DISPLAY_NAME)}</text>
{chr(10).join(row_markup)}
    <text x="34" y="304" font-size="13" fill="#8b949e">Edit scripts/profile_config.py to confirm stack, links, and projects.</text>
  </g>
</svg>
"""
    write_text(ROOT / "info-card.svg", svg)


if __name__ == "__main__":
    main()
