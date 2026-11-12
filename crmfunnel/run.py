"""Loads the CSVs into SQLite, runs every query in sql/ and renders the results
as a terminal report and a self-contained HTML dashboard. Standard library only."""

from __future__ import annotations

import csv
import html
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).parents[1]
Result = Tuple[List[str], List[tuple]]


def _typed(value: str):
    """CSV gives strings; store numbers as numbers so comparisons in SQL are numeric."""
    for cast in (int, float):
        try:
            return cast(value)
        except ValueError:
            pass
    return value


def load(data_dir: Path = ROOT / "data") -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    for csv_path in sorted(data_dir.glob("*.csv")):
        with csv_path.open(newline="") as f:
            rows = list(csv.reader(f))
        header, body = rows[0], [[_typed(v) for v in r] for r in rows[1:]]
        table = csv_path.stem
        con.execute(f"CREATE TABLE {table} ({', '.join(header)})")
        con.executemany(f"INSERT INTO {table} VALUES ({', '.join('?' * len(header))})", body)
    return con


def run_all(con: sqlite3.Connection, sql_dir: Path = ROOT / "sql") -> Dict[str, Result]:
    results: Dict[str, Result] = {}
    for path in sorted(sql_dir.glob("*.sql")):
        cur = con.execute(path.read_text())
        results[path.stem] = ([d[0] for d in cur.description], cur.fetchall())
    return results


def title(stem: str) -> str:
    return stem.split("_", 1)[1].replace("_", " ").capitalize()


def to_text(results: Dict[str, Result]) -> str:
    out = []
    for stem, (cols, rows) in results.items():
        widths = [max(len(str(c)), *(len(str(r[i])) for r in rows)) for i, c in enumerate(cols)]
        out.append(f"\n== {title(stem)} ==")
        out.append("  ".join(str(c).ljust(w) for c, w in zip(cols, widths)))
        out += ["  ".join(str(v).ljust(w) for v, w in zip(r, widths)) for r in rows]
    return "\n".join(out)


def to_html(results: Dict[str, Result], heading: str) -> str:
    sections = []
    for stem, (cols, rows) in results.items():
        # bar for the last numeric column, scaled to its max
        last = len(cols) - 1
        nums = [r[last] for r in rows if isinstance(r[last], (int, float))]
        top = max(nums) if nums else 0
        head = "".join(f"<th>{html.escape(c)}</th>" for c in cols) + "<th></th>"
        body = ""
        for r in rows:
            cells = "".join(f"<td>{html.escape(str(v))}</td>" for v in r)
            val = r[last] if isinstance(r[last], (int, float)) else 0
            width = 0 if not top or val < 0 else 100 * val / top
            body += f"<tr>{cells}<td class='bar'><span style='width:{width:.0f}%'></span></td></tr>"
        sections.append(f"<section><h2>{html.escape(title(stem))}</h2><table><tr>{head}</tr>{body}</table></section>")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(heading)}</title>
<style>body{{font-family:system-ui,sans-serif;margin:40px auto;max-width:960px;color:#1f2937}}
h1{{font-size:26px}}h2{{font-size:18px;margin-top:36px}}table{{border-collapse:collapse;width:100%;font-size:14px}}
th,td{{text-align:left;padding:6px 10px;border-bottom:1px solid #e5e7eb}}th{{background:#f3f4f6}}
.bar{{width:160px}}.bar span{{display:block;height:10px;background:#2563eb;border-radius:3px}}</style></head>
<body><h1>{html.escape(heading)}</h1><p>Generated from fictional data with plain SQL (SQLite).</p>{''.join(sections)}</body></html>"""
