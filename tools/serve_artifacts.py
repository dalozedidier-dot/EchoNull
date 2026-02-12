from __future__ import annotations

import argparse
import http.server
import os
import socketserver
from pathlib import Path


class RootHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, root: Path, **kwargs):
        self._root = root
        super().__init__(*args, directory=str(root), **kwargs)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="_ci_out", help="Directory to serve.")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"Missing {root}")

    os.chdir(root)
    with socketserver.TCPServer(("", args.port), lambda *a, **k: RootHandler(*a, root=root, **k)) as httpd:
        print(f"Serving {root} on http://127.0.0.1:{args.port}")
        httpd.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
