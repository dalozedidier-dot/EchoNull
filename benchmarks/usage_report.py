from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd


def _clean_text(s: str) -> str:
    # Handles values like: ""'hosted"" or "".github/workflows/ci.yml""
    s = s.strip()
    s = re.sub(r'^"\'', "", s)
    s = re.sub(r'"$', "", s)
    s = s.replace("\\", "")
    return s.strip()


def _clean_columns(cols: list[str]) -> list[str]:
    out: list[str] = []
    for c in cols:
        c2 = c.strip()
        c2 = re.sub(r'^"\'', "", c2)
        c2 = re.sub(r'"$', "", c2)
        c2 = c2.replace("\\", "")
        out.append(c2.strip())
    return out


def load_usage_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = _clean_columns(list(df.columns))
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).map(_clean_text)
    return df


def summarize_usage(fixtures_dir: Path) -> dict[str, Any]:
    by_job = load_usage_csv(fixtures_dir / "by_job_failure_and_time.csv")
    by_workflow = load_usage_csv(fixtures_dir / "by_workflow_failure_and_time.csv")
    overall = load_usage_csv(fixtures_dir / "by_runner_type_usage.csv")

    # Convert ms to seconds where present
    if "Avg run time" in by_job.columns:
        by_job["avg_run_s"] = by_job["Avg run time"] / 1000.0
    if "Avg queue time" in by_job.columns:
        by_job["avg_queue_s"] = by_job["Avg queue time"] / 1000.0
    if "Avg run time" in by_workflow.columns:
        by_workflow["avg_run_s"] = by_workflow["Avg run time"] / 1000.0

    test_row = by_job.loc[by_job["Job"] == "test"].iloc[0].to_dict()
    ci_row = by_workflow.loc[by_workflow["Workflow"] == ".github/workflows/ci.yml"].iloc[0].to_dict()
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
