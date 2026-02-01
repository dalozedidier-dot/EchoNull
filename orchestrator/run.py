from __future__ import annotations

import argparse
import json
import os
import zipfile
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from common.utils import compute_sha256, perf_timer
from delta_stats.analyzer import DeltaStatsAnalyzer
from graph_analysis.analyzer import GraphAnalysisAnalyzer
from mark_counts.analyzer import MarkCountsAnalyzer


@dataclass(frozen=True)
class Params:
    runs: int
    thresholds: list[float]
    out: Path
    seed_base: int
    workers: int
    zip_out: bool


def _generate_dataset_csv(path: Path, seed: int, rows: int = 256, cols: int = 8) -> None:
    rng = np.random.default_rng(seed)
    data = rng.normal(size=(rows, cols)).astype(np.float32)
    df = pd.DataFrame(data, columns=[f"c{i}" for i in range(cols)])
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


@perf_timer
def process_run(run_id: int, params: Params) -> dict[str, Any]:
    seed = params.seed_base + run_id
    run_dir = params.out / f"run_{run_id:04d}"
    run_dir.mkdir(parents=True, exist_ok=True)

    dataset_path = run_dir / "multi.csv"
    _generate_dataset_csv(dataset_path, seed=seed)

    analyzers = [
        GraphAnalysisAnalyzer(params.thresholds),
        DeltaStatsAnalyzer(),
        MarkCountsAnalyzer(),
    ]

    results: dict[str, Any] = {}
    for analyzer in analyzers:
        results.update(analyzer.analyze(run_id, seed, None, run_dir))

    hashes = {"multi.csv": compute_sha256(dataset_path)}
    return {"run_id": run_id, "results": results, "hashes": hashes}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="echonull-orchestrator", description="EchoNull sweep runner")
    p.add_argument("--runs", type=int, default=10)
    p.add_argument("--thresholds", type=str, default="0.25,0.5,0.7,0.8")
    p.add_argument("--out", type=str, default="_out")
    p.add_argument("--seed-base", type=int, default=1000)
    p.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    p.add_argument("--zip", dest="zip_out", action="store_true")
    return p


def _parse_thresholds(s: str) -> list[float]:
    parts = [x.strip() for x in s.split(",") if x.strip()]
    return [float(x) for x in parts]


@perf_timer
def run(params: Params) -> tuple[list[dict[str, Any]], Path | None]:
    params.out.mkdir(parents=True, exist_ok=True)

    with ProcessPoolExecutor(max_workers=params.workers) as pool:
        futures = [pool.submit(process_run, i, params) for i in range(1, params.runs + 1)]
        results = [f.result() for f in futures]

    overview_path = params.out / "overview.json"
    overview_path.write_text(
        json.dumps(results, separators=(",", ":"), ensure_ascii=False),
        encoding="utf-8",
    )

    manifest = {
        "name": "EchoNull",
        "runs": params.runs,
        "thresholds": params.thresholds,
        "seed_base": params.seed_base,
        "overview_sha256": compute_sha256(overview_path),
    }
    manifest_path = params.out / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, separators=(",", ":"), ensure_ascii=False),
        encoding="utf-8",
    )

    zip_path: Path | None = None
    if params.zip_out:
        zip_path = params.out.with_suffix(".zip")
        _zip_dir(params.out, zip_path)

    return results, zip_path


def _zip_dir(src_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in src_dir.rglob("*"):
            if p.is_file():
                zf.write(p, arcname=p.relative_to(src_dir))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    params = Params(
        runs=int(args.runs),
        thresholds=_parse_thresholds(args.thresholds),
        out=Path(args.out),
        seed_base=int(args.seed_base),
        workers=int(args.workers),
        zip_out=bool(args.zip_out),
    )
    run(params)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
