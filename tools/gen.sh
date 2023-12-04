#!/usr/bin/env bash

set -Eeuo pipefail

ROOT=$(git rev-parse --show-toplevel)

cat <<EOF > "$ROOT/2023/day$1.py"
def main():
    with open("inputs/day$1.txt") as f:
        pass


if __name__ == "__main__":
    main()
EOF

touch "$ROOT/2023/inputs/day$1.txt"
