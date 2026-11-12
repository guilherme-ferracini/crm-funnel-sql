"""python -m crmfunnel [--html out/dashboard.html]"""

from __future__ import annotations

import argparse
from pathlib import Path

from .run import load, run_all, to_html, to_text


def main() -> None:
    p = argparse.ArgumentParser(description="CRM funnel analytics in SQL")
    p.add_argument("--html", type=Path, default=None, help="also write an HTML dashboard")
    a = p.parse_args()
    results = run_all(load())
    print(to_text(results))
    if a.html:
        a.html.parent.mkdir(parents=True, exist_ok=True)
        a.html.write_text(to_html(results, "Advisory office CRM funnel"), encoding="utf-8")
        print(f"\nDashboard written to {a.html}")


if __name__ == "__main__":
    main()
