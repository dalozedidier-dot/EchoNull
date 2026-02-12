from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="_ci_out", help="Run output directory.")
    ap.add_argument("--html", default="dashboard.html", help="Output HTML file.")
    args = ap.parse_args()

    out = Path(args.out)
    manifest = _load_json(out / "manifest.json")
    overview = _load_json(out / "overview.json")

    rows = []
    for i, run_item in enumerate(overview, start=1):
        ds = run_item.get("delta_stats", {})
        mc = run_item.get("mark_counts", {})
        ga = run_item.get("graph_analysis", {})
        j_min = None
        for thr, rep in ga.items():
            j = rep.get("jaccard")
            if isinstance(j, (int, float)):
                j_min = j if j_min is None else min(j_min, j)
        rows.append(
            {
                "run": i,
                "abs_p99": ds.get("abs_p99"),
                "max": ds.get("max"),
                "count": mc.get("count"),
                "jaccard_min": j_min,
            }
        )

    def td(x: Any) -> str:
        return f"<td>{html.escape(str(x))}</td>"

    table_rows = "\n".join(
        "<tr>" + "".join(td(r[k]) for k in ["run", "abs_p99", "max", "count", "jaccard_min"]) + "</tr>"
        for r in rows
    )

    html_doc = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>EchoNull dashboard</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 24px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; }}
    th {{ background: #f5f5f5; text-align: left; }}
    code {{ background: #f2f2f2; padding: 2px 4px; }}
  </style>
</head>
<body>
  <h1>EchoNull dashboard</h1>
  <p><b>run_id</b>: <code>{html.escape(str(manifest.get("run_id")))}</code></p>
  <p><b>runs</b>: {manifest.get("runs")} | <b>thresholds</b>: {html.escape(str(manifest.get("thresholds")))}</p>

  <h2>Overview</h2>
  <table>
    <thead>
      <tr>
        <th>run</th>
        <th>abs_p99</th>
        <th>max</th>
        <th>count</th>
        <th>jaccard_min</th>
      </tr>
    </thead>
    <tbody>
      {table_rows}
    </tbody>
  </table>
</body>
</html>
"""

    Path(args.html).write_text(html_doc, encoding="utf-8")
    print(args.html)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
