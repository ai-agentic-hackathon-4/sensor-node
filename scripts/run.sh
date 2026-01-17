#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$DIR/.."
cd "$ROOT"

# PORT 環境変数でポート指定可能（デフォルト 8000）
uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"
