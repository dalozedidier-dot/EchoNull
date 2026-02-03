\
#!/usr/bin/env bash
set -euo pipefail

CI=".github/workflows/ci.yml"
if [[ ! -f "$CI" ]]; then
  echo "ERROR: missing $CI (run from repo root)" >&2
  exit 1
fi

cp "$CI" "$CI.bak"

# 1) Coverage target: src -> .
perl -0pi -e 's/--cov\s*=\s*src\b/--cov=./g' "$CI"

# 2) PYTHONPATH: src -> .
perl -0pi -e 's/\bPYTHONPATH:\s*src\b/PYTHONPATH: ./g' "$CI"

# 3) Remove 3.10 and 3.11 YAML block list items (python-version matrices).
perl -0pi -e 's/^\s*-\s*["'\''"]?3\.10[^0-9].*\n//mg' "$CI"
perl -0pi -e 's/^\s*-\s*["'\''"]?3\.11[^0-9].*\n//mg' "$CI"

# 4) Inline list matrices: python-version: ["3.10", "3.11", "3.12"] -> ["3.12"]
perl -0pi -e '
  s/(python-version:\s*\[)([^\]]*)(\])/
    my $pre=$1; my $mid=$2; my $post=$3;
    my @parts = split(/,/, $mid);
    @parts = grep { $_ !~ /3\.10/ && $_ !~ /3\.11/ } @parts;
    $pre . join(", ", map { my $x=$_; $x=~s/^\s+|\s+$//g; $x } @parts) . $post;
  /gex
' "$CI"

echo "OK: patched $CI"
echo "Backup: $CI.bak"
echo
echo "Next:"
echo "  git diff"
echo "  git commit -am \"ci: py312-only + fix coverage target\""
echo "  git push"
