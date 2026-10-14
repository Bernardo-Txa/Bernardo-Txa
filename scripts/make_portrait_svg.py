from __future__ import annotations

import argparse
from pathlib import Path

from profile_config import INITIALS
from svg_utils import ROOT, esc, svg_header, write_text


GLYPHS = [
    "        ########        ",
    "     ################     ",
    "   ####################   ",
    "  #######  ####  #######  ",
    " ######    ####    ###### ",
    " ######  ########  ###### ",
    " ######  ########  ###### ",
    " ######    ####    ###### ",
    "  #######  ####  #######  ",
    "   ####################   ",
    "     ################     ",
    "        ########        ",
]


def image_to_ascii(image_path: Path, width: int = 46) -> list[str]:
    try:
        from PIL import Image, ImageOps
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Pillow is required to convert a photo. Run: python -m pip install -r scripts/requirements.txt"
        ) from exc

    ramp = " .:-=+*#%@"
    image = Image.open(image_path).convert("L")
    image = ImageOps.autocontrast(image)
    aspect = image.height / image.width
    height = max(16, int(width * aspect * 0.46))
    image = image.resize((width, height))
    rows: list[str] = []
    for y in range(height):
        row = ""
        for x in range(width):
            pixel = image.getpixel((x, y))
            row += ramp[pixel * (len(ramp) - 1) // 255]
        rows.append(row)
    return rows


def initials_ascii() -> list[str]:
    rows = [line.replace("#", "@") for line in GLYPHS]
    center = len(rows) // 2
    chars = list(rows[center])
    start = max(0, (len(chars) - len(INITIALS)) // 2)
    for idx, char in enumerate(INITIALS):
        chars[start + idx] = char
    rows[center] = "".join(chars)
    return rows


def render(rows: list[str]) -> str:
    char_w = 9
    line_h = 15
    pad_x = 24
    pad_y = 28
    width = max(len(row) for row in rows) * char_w + pad_x * 2
    height = len(rows) * line_h + pad_y * 2
    lines = []
    for i, row in enumerate(rows):
        y = pad_y + i * line_h
        delay = i * 0.055
        lines.append(
            f'    <text x="{pad_x}" y="{y}" opacity="0">{esc(row)}'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.18s" begin="{delay:.2f}s" fill="freeze"/></text>'
        )

    return f"""{svg_header(width, height)}
  <rect width="100%" height="100%" rx="12" fill="#0d1117"/>
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="none" stroke="#30363d"/>
  <g font-family="Consolas, Monaco, 'Courier New', monospace" font-size="14" fill="#c9d1d9" xml:space="preserve">
{chr(10).join(lines)}
  </g>
</svg>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="Approved source photo to convert into ASCII.")
    args = parser.parse_args()
    rows = image_to_ascii(args.source) if args.source else initials_ascii()
    write_text(ROOT / "portrait.svg", render(rows))


if __name__ == "__main__":
    main()
