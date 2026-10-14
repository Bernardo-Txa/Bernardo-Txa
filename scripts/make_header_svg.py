from __future__ import annotations

from profile_config import DISPLAY_NAME, TAGLINE
from svg_utils import ROOT, esc, svg_header, write_text


def main() -> None:
    command = "bernardo@github:~$ whoami"
    answer = f"{DISPLAY_NAME} - {TAGLINE}"
    width = 980
    height = 230
    char_w = 15
    command_w = len(command) * char_w
    answer_w = min(len(answer) * 10, 850)

    svg = f"""{svg_header(width, height)}
  <defs>
    <filter id="terminalGlow" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="chrome" x1="0" x2="1">
      <stop offset="0" stop-color="#30363d"/>
      <stop offset="1" stop-color="#161b22"/>
    </linearGradient>
    <clipPath id="typeCommand">
      <rect x="34" y="76" width="0" height="34">
        <animate attributeName="width" from="0" to="{command_w}" dur="2.2s" fill="freeze"/>
      </rect>
    </clipPath>
    <clipPath id="typeAnswer">
      <rect x="34" y="132" width="0" height="36">
        <animate attributeName="width" from="0" to="{answer_w}" dur="2.6s" begin="2.35s" fill="freeze"/>
      </rect>
    </clipPath>
  </defs>
  <rect width="100%" height="100%" rx="14" fill="#0d1117"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" fill="none" stroke="#30363d"/>
  <rect x="1" y="1" width="{width - 2}" height="44" rx="14" fill="url(#chrome)"/>
  <circle cx="25" cy="23" r="6" fill="#ff5f56"/>
  <circle cx="47" cy="23" r="6" fill="#ffbd2e"/>
  <circle cx="69" cy="23" r="6" fill="#27c93f"/>
  <text x="490" y="28" text-anchor="middle" font-family="Consolas, Monaco, 'Courier New', monospace" font-size="13" fill="#8b949e">profile.sh</text>
  <g font-family="Consolas, Monaco, 'Courier New', monospace">
    <text x="34" y="101" font-size="25" fill="#39d353" filter="url(#terminalGlow)" clip-path="url(#typeCommand)">{esc(command)}</text>
    <rect x="{34 + command_w + 8}" y="78" width="12" height="27" fill="#39d353" opacity="0">
      <animate attributeName="opacity" values="0;1;0;1;0" dur="1.1s" repeatCount="3"/>
    </rect>
    <text x="34" y="160" font-size="20" fill="#f0f6fc" clip-path="url(#typeAnswer)">{esc(answer)}</text>
    <text x="34" y="199" font-size="14" fill="#8b949e">No external services. No JavaScript. Self-contained SVG animations.</text>
  </g>
</svg>
"""
    write_text(ROOT / "header.svg", svg)


if __name__ == "__main__":
    main()
