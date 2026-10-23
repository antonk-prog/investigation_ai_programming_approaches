#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
impl="${1:?usage: ./check.sh approaches/NN-name/impl}"
bin="$impl/build/logstat"

if [[ ! -x "$bin" ]]; then
  echo "error: binary not found: $bin" >&2
  echo "build it with:" >&2
  echo "  cmake -S \"$impl\" -B \"$impl/build\" -G Ninja && cmake --build \"$impl/build\"" >&2
  exit 2
fi

exec python3 "$root/shared/acceptance/check.py" --bin "$bin"
