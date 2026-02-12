from __future__ import annotations

from echonull.orchestrator.run import build_parser, main

if __name__ == "__main__":
    # Default behavior: run the orchestrator CLI.
    parser = build_parser()
    args = parser.parse_args()
    argv: list[str] = []
    if args.runs is not None:
        argv += ["--runs", str(args.runs)]
    argv += ["--thresholds", str(args.thresholds)]
    argv += ["--out", str(args.out)]
    argv += ["--seed-base", str(args.seed_base)]
    argv += ["--workers", str(args.workers)]
    if args.zip_out:
        argv += ["--zip"]
    raise SystemExit(main(argv))
