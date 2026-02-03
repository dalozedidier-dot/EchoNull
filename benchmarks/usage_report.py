from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from pandas.api.types import is_string_dtype


def _clean_text(value: str) -> str:
    s = value.strip()

    # Some GitHub Actions usage CSV exports contain extra quotes and backslashes.
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        s = s[1:-1]

    s = s.replace("\\", "")

    if s.startswith("'"):
        s = s[1:]

    return s.strip()


def load_usage_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [_clean_text(str(c)) for c in df.columns]

    # Pandas 3.0 may default to dedicated string dtypes instead of plain object.
    # We want to normalize *all* string-like columns (headers already cleaned above).
    for col in df.columns:
        if is_string_dtype(df[col]):
            df[col] = df[col].astype(str).map(_clean_text)

    return df


def summarize_usage(fixtures_dir: Path) -> dict[str, Any]:
    by_job = load_usage_csv(fixtures_dir / "by_job_failure_and_time.csv")
    by_workflow = load_usage_csv(fixtures_dir / "by_workflow_failure_and_time.csv")
    overall = load_usage_csv(fixtures_dir / "by_runner_type_usage.csv")

    if "Avg run time" in by_job.columns:
        by_job["avg_run_s"] = by_job["Avg run time"] / 1000.0
    if "Avg queue time" in by_job.columns:
        by_job["avg_queue_s"] = by_job["Avg queue time"] / 1000.0
    if "Avg run time" in by_workflow.columns:
        by_workflow["avg_run_s"] = by_workflow["Avg run time"] / 1000.0

    test_row = by_job.loc[by_job["Job"] == "test"].iloc[0].to_dict()
    ci_row = (
        by_workflow.loc[by_workflow["Workflow"] == ".github/workflows/ci.yml"].iloc[0].to_dict()
    )
    overall_row = overall.iloc[0].to_dict()

    return {
        "total_minutes": int(overall_row["Total minutes"]),
        "workflow_runs_total": int(overall_row["Workflow runs"]),
        "workflows_total": int(overall_row["Workflows"]),
        "test_job_failure_rate": float(test_row["Failure rate"]),
        "test_job_avg_run_s": float(test_row.get("avg_run_s", 0.0)),
        "ci_workflow_has_failures_rate": float(ci_row["Has job failures"]),
        "ci_workflow_avg_run_s": float(ci_row.get("avg_run_s", 0.0)),
    }
