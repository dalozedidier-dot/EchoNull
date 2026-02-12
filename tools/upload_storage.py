from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="_ci_out", help="Directory or zip to upload.")
    ap.add_argument("--dest", required=True, help="Destination (ex: s3://bucket/path or ssh:user@host:/path).")
    ap.add_argument("--dry-run", action="store_true", help="Do not upload, only print.")
    args = ap.parse_args()

    src = Path(args.src)
    if not src.exists():
        raise SystemExit(f"Missing {src}")

    print(f"src={src}")
    print(f"dest={args.dest}")
    if args.dry_run:
        print("dry-run: no upload performed")
        return 0

    print("Upload is a skeleton. Implement the transport you want (S3, rsync, scp).")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
