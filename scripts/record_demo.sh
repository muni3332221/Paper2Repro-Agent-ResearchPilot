#!/usr/bin/env bash
set -euo pipefail

# Demo script for README screenshots or terminal recording tools such as asciinema.
# Usage:
#   bash scripts/record_demo.sh path/to/paper.pdf

PDF_PATH="${1:-examples/paper.pdf}"
OUTPUT_DIR="outputs/demo"

paper2repro run "$PDF_PATH" --no-llm -o "$OUTPUT_DIR"

echo ""
echo "Generated files:"
find "$OUTPUT_DIR" -maxdepth 3 -type f | sort

echo ""
echo "Preview:"
sed -n '1,80p' "$OUTPUT_DIR/repro_plan.md"
