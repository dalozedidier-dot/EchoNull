\
#!/usr/bin/env bash
set -euo pipefail

CI=".github/workflows/ci.yml"
if [[ ! -f "$CI" ]]; then
  echo "ERROR: missing $CI (run from repo root)" >&2
  exit 1
fi

# Optional backup
cp "$CI" "$CI.bak"

# --- 1) Drop Python < 3.12 from matrices (block list items) ---
# Removes lines like: - "3.10" / - '3.10' / - 3.10  (same for 3.11)
perl -0pi -e 's/^\s*-\s*["'\'']?3\.10(?:\.\d+)?["'\'']?\s*\n//mg' "$CI"
perl -0pi -e 's/^\s*-\s*["'\'']?3\.11(?:\.\d+)?["'\'']?\s*\n//mg' "$CI"

# --- 2) Drop Python < 3.12 from inline lists ---
# python-version: ["3.10", "3.11", "3.12"] -> python-version: ["3.12"]
perl -0pi -e '
  s/(python-version:\s*\[)([^\]]*)(\])/
    my ($pre,$mid,$post)=($1,$2,$3);
    my @parts = split(/,/, $mid);
    @parts = grep { $_ !~ /3\.10/ && $_ !~ /3\.11/ } @parts;
    $pre . join(", ", map { my $x=$_; $x=~s/^\s+|\s+$//g; $x } @parts) . $post;
  /gex
' "$CI"

# --- 3) Fix coverage target (repo is not src/ layout) ---
# --cov=src -> --cov=.   and   --cov src -> --cov .
perl -0pi -e 's/--cov\s*=\s*src\b/--cov=./g' "$CI"
perl -0pi -e 's/--cov\s+src\b/--cov ./g' "$CI"

# --- 4) Fix PYTHONPATH if present ---
# PYTHONPATH: src -> PYTHONPATH: .
perl -0pi -e 's/\bPYTHONPATH:\s*src\b/PYTHONPATH: ./g' "$CI"

echo "OK: patched $CI"
echo "Backup written: $CI.bak"
echo
echo "Next:"
echo "  git diff"
echo "  # optionally: echo '.github/workflows/ci.yml.bak' >> .gitignore"
echo "  git commit -am \"ci: py312-only + fix coverage target\""
echo "  git push"
