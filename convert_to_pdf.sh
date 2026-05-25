#!/usr/bin/env bash
# Convert all CV markdown files in output/ to PDF using reportlab.
#
# Requirements (install once):
#   pip3 install reportlab
#
# Usage:
#   ./convert_to_pdf.sh       # convert all CVs

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if ! python3 -c "import reportlab" &>/dev/null; then
  echo "Error: reportlab not found. Install with: pip3 install reportlab"
  exit 1
fi

python3 "$SCRIPT_DIR/output/generate_pdfs.py"
