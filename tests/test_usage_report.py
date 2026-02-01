from __future__ import annotations

from pathlib import Path

from benchmarks.usage_report import summarize_usage


def test_usage_report_summary_contract() -> None:
    fixtures = Path("benchmarks/fixtures/github_actions_usage")
    s = summarize_usage(fixtures)

    assert s["total_minutes"] == 54
    assert s["workflow_runs_total"] == 54
    assert s["workflows_total"] == 3

    # This reflects your exported snapshot
    assert round(s["test_job_failure_rate"], 2) == 45.71
    assert 20.0 <= s["test_job_avg_run_s"] <= 60.0

    assert round(s["ci_workflow_has_failures_rate"], 2) == 47.06
    assert 20.0 <= s["ci_workflow_avg_run_s"] <= 60.0
