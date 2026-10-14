from __future__ import annotations

import json
from datetime import UTC, date, datetime, timedelta

from profile_config import USERNAME
from svg_utils import ROOT, esc, svg_header, write_text


PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def load_payload() -> dict:
    path = ROOT / "data" / "contributions.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    today = date.today()
    days = []
    start = today - timedelta(days=370)
    for i in range(371):
        d = start + timedelta(days=i)
        days.append({"date": d.isoformat(), "count": 0, "level": 0})
    return {
        "username": USERNAME,
        "fetched_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": "local placeholder",
        "days": days,
        "stats": {"total": 0, "current_streak": 0, "longest_streak": 0, "best_day": {"date": today.isoformat(), "count": 0}},
    }


def main() -> None:
    payload = load_payload()
    by_date = {item["date"]: item for item in payload["days"]}
    dates = [datetime.fromisoformat(str(d)).date() for d in by_date]
    end = max(dates) if dates else date.today()
    start = end - timedelta(days=370)
    start -= timedelta(days=(start.weekday() + 1) % 7)

    cell = 12
    gap = 4
    left = 44
    top = 70
    width = left + 53 * (cell + gap) + 34
    height = 205
    cells = []
    for week in range(53):
        for weekday in range(7):
            day = start + timedelta(days=week * 7 + weekday)
            data = by_date.get(day.isoformat(), {"count": 0, "level": 0})
            level = max(0, min(int(data.get("level", 0)), 4))
            count = int(data.get("count", 0))
            x = left + week * (cell + gap)
            y = top + weekday * (cell + gap)
            delay = (week * 7 + weekday) * 0.006
            cells.append(
                f'    <rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{PALETTE[level]}" opacity="0">'
                f'<title>{esc(day.isoformat())}: {count} contributions</title>'
                f'<animate attributeName="opacity" from="0" to="1" dur="0.18s" begin="{delay:.3f}s" fill="freeze"/></rect>'
            )

    stats = payload.get("stats", {})
    total = int(stats.get("total", 0) or 0)
    footer = f"{total:,} public contributions in the available GitHub window".replace(",", ".")
    legend = []
    lx = width - 170
    for idx, color in enumerate(PALETTE):
        legend.append(f'<rect x="{lx + idx * 18}" y="170" width="12" height="12" rx="3" fill="{color}"/>')

    svg = f"""{svg_header(width, height)}
  <rect width="100%" height="100%" rx="12" fill="#0d1117"/>
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="none" stroke="#30363d"/>
  <g font-family="Consolas, Monaco, 'Courier New', monospace">
    <text x="30" y="36" font-size="18" fill="#f0f6fc">{esc(USERNAME)} contribution activity</text>
    <text x="30" y="56" font-size="12" fill="#8b949e">Source: {esc(payload.get("source", "GitHub public contribution endpoint"))}</text>
{chr(10).join(cells)}
    <text x="30" y="180" font-size="13" fill="#8b949e">{esc(footer)}</text>
    <text x="{lx - 36}" y="180" font-size="12" fill="#8b949e">Less</text>
    {''.join(legend)}
    <text x="{lx + 96}" y="180" font-size="12" fill="#8b949e">More</text>
  </g>
</svg>
"""
    write_text(ROOT / "contrib-heatmap.svg", svg)


if __name__ == "__main__":
    main()
