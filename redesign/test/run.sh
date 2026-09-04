#!/bin/bash
# Rebuilds the mocked pages from playlist.html and runs both suites headless.
# Usage: test/run.sh [path-to-chrome]
set -e
cd "$(dirname "$0")"
CHROME="${1:-${CHROME:-/opt/pw-browsers/chromium}}"
[ -x "$CHROME" ] || { echo "no chrome at $CHROME - pass one as \$1"; exit 2; }
python3 build-test.py
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

run(){  # name, url
  "$CHROME" --headless=new --disable-gpu --no-sandbox \
    --user-data-dir="$TMP/$1" --virtual-time-budget=40000 \
    --dump-dom "$2" 2>/dev/null \
    | grep -o "<title>[^<]*</title>" | sed -e 's/<[^>]*>//g' -e 's/ | /\n  /g'
}

echo "== journey =="
run one   "file://$PWD/run.html"
echo
echo "== failure paths =="
run two   "file://$PWD/run2.html$(cat run2.hash)"
