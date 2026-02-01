from __future__ import annotations

from pathlib import Path

from delta_stats.analyzer import DeltaStatsAnalyzer
from graph_analysis.analyzer import GraphAnalysisAnalyzer
from mark_counts.analyzer import MarkCountsAnalyzer


def test_graph_analysis_even_odd(tmp_path: Path) -> None:
    a = GraphAnalysisAnalyzer([0.25])
    r_even = a.analyze(run_id=2, seed=1, data=None, output_dir=tmp_path)
    r_odd = a.analyze(run_id=1, seed=1, data=None, output_dir=tmp_path)

    assert "graph_analysis" in r_even
    assert "0.25" in r_even["graph_analysis"]
    assert r_even["graph_analysis"]["0.25"]["jaccard"] == 1.0
    assert 0.9 <= r_odd["graph_analysis"]["0.25"]["jaccard"] <= 1.0


def test_delta_stats(tmp_path: Path) -> None:
    a = DeltaStatsAnalyzer()
    r = a.analyze(run_id=1, seed=42, data=None, output_dir=tmp_path)
    assert "delta_stats" in r
    stats = r["delta_stats"]
    assert stats["n_deltas"] == 50
    assert stats["abs_p50"] <= stats["abs_p90"] <= stats["abs_p99"]
    assert (tmp_path / "delta_stats" / "stats.json").exists()


def test_mark_counts(tmp_path: Path) -> None:
    a = MarkCountsAnalyzer()
    r = a.analyze(run_id=1, seed=99, data=None, output_dir=tmp_path)
    assert "mark_counts" in r
    count = r["mark_counts"]["median_count"]
    assert 1 <= count <= 4
    assert (tmp_path / "mark_counts" / "count.txt").exists()
