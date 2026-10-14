from __future__ import annotations

import json
import re
import sys
import time
from datetime import UTC, date, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from profile_config import USERNAME
from svg_utils import ROOT, write_text


class ContributionParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.days: list[dict[str, object]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: v for k, v in attrs if v is not None}
        if tag not in {"td", "tool-tip"}:
            return

        date_value = attr.get("data-date") or attr.get("for", "")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_value):
            return

        count = 0
        level = int(attr.get("data-level", "0") or 0)
        text = attr.get("aria-label") or attr.get("data-count") or ""
        count_match = re.search(r"(\d[\d,]*) contribution", text)
        if count_match:
            count = int(count_match.group(1).replace(",", ""))
        elif attr.get("data-count", "").isdigit():
            count = int(attr["data-count"])

        self.days.append({"date": date_value, "count": count, "level": max(0, min(level, 4))})


def fetch_html(username: str) -> str:
    url = f"https://github.com/users/{username}/contributions"
    req = Request(
        url,
        headers={
            "User-Agent": "Bernardo-Txa-profile-readme-generator",
            "Accept": "text/html",
        },
    )
    with urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def stats(days: list[dict[str, object]]) -> dict[str, object]:
    counts = [(datetime.fromisoformat(str(d["date"])).date(), int(d["count"])) for d in days]
    total = sum(count for _, count in counts)
    best = max(counts, key=lambda item: item[1], default=(date.today(), 0))
    current = 0
    for _, count in reversed(counts):
        if count <= 0:
            break
        current += 1
    longest = 0
    active = 0
    for _, count in counts:
        active = active + 1 if count > 0 else 0
        longest = max(longest, active)
    return {
        "total": total,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best[0].isoformat(), "count": best[1]},
    }


def main() -> None:
    try:
        html = fetch_html(USERNAME)
    except (HTTPError, URLError, TimeoutError) as exc:
        print(f"Could not fetch GitHub contributions for {USERNAME}: {exc}", file=sys.stderr)
        raise SystemExit(1)

    parser = ContributionParser()
    parser.feed(html)
    days = sorted({str(day["date"]): day for day in parser.days}.values(), key=lambda d: str(d["date"]))
    if not days:
        print("No contribution cells found. GitHub markup may have changed.", file=sys.stderr)
        raise SystemExit(1)

    payload = {
        "username": USERNAME,
        "fetched_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": f"https://github.com/users/{USERNAME}/contributions",
        "days": days[-371:],
        "stats": stats(days[-371:]),
    }
    write_text(ROOT / "data" / "contributions.json", json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"Fetched {len(payload['days'])} contribution days for {USERNAME}.")


if __name__ == "__main__":
    main()
