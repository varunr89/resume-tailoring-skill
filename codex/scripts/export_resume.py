#!/usr/bin/env python3
"""Export resume markdown to DOCX and/or PDF using local CLI tools.

Usage:
  python3 scripts/export_resume.py --input out/Resume.md --formats docx,pdf
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> tuple[int, str]:
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}"
    return result.returncode, (result.stdout or "").strip()


def has(binary: str) -> bool:
    return shutil.which(binary) is not None


def export_docx(input_md: Path, output_docx: Path) -> bool:
    if has("pandoc"):
        code, out = run(["pandoc", str(input_md), "-o", str(output_docx)])
        if code == 0 and output_docx.exists():
            print(f"[ok] DOCX via pandoc -> {output_docx}")
            return True
        print(f"[warn] pandoc DOCX export failed: {out}")

    # textutil fallback may lose markdown structure but still produces a DOCX.
    if has("textutil"):
        code, out = run(
            [
                "textutil",
                "-convert",
                "docx",
                str(input_md),
                "-output",
                str(output_docx),
            ]
        )
        if code == 0 and output_docx.exists():
            print(f"[ok] DOCX via textutil fallback -> {output_docx}")
            return True
        print(f"[warn] textutil DOCX export failed: {out}")

    print("[error] Could not generate DOCX (missing/failed converters).")
    return False


def export_pdf(input_md: Path, output_pdf: Path, docx_hint: Path | None) -> bool:
    if has("pandoc"):
        attempts = [
            ["pandoc", str(input_md), "-o", str(output_pdf)],
            ["pandoc", str(input_md), "-o", str(output_pdf), "--pdf-engine=xelatex"],
            ["pandoc", str(input_md), "-o", str(output_pdf), "--pdf-engine=pdflatex"],
            ["pandoc", str(input_md), "-o", str(output_pdf), "--pdf-engine=wkhtmltopdf"],
            ["pandoc", str(input_md), "-o", str(output_pdf), "--pdf-engine=weasyprint"],
        ]
        for cmd in attempts:
            code, out = run(cmd)
            if code == 0 and output_pdf.exists():
                print(f"[ok] PDF via {' '.join(cmd[:2])} -> {output_pdf}")
                return True
            if out:
                print(f"[warn] pandoc PDF attempt failed: {out}")

    if has("soffice") and docx_hint and docx_hint.exists():
        outdir = str(output_pdf.parent)
        code, out = run(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                outdir,
                str(docx_hint),
            ]
        )
        expected = output_pdf.parent / f"{docx_hint.stem}.pdf"
        if code == 0 and expected.exists():
            if expected != output_pdf:
                expected.replace(output_pdf)
            print(f"[ok] PDF via soffice from DOCX -> {output_pdf}")
            return True
        print(f"[warn] soffice PDF export failed: {out}")

    print("[error] Could not generate PDF (missing/failed converters).")
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export resume markdown to DOCX/PDF using local tools."
    )
    parser.add_argument("--input", required=True, help="Path to markdown resume")
    parser.add_argument(
        "--formats",
        default="docx,pdf",
        help="Comma-separated formats to generate (docx,pdf)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Optional output directory (default: input file directory)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_md = Path(args.input).expanduser().resolve()
    if not input_md.exists():
        print(f"[error] input file not found: {input_md}")
        return 1

    requested = {fmt.strip().lower() for fmt in args.formats.split(",") if fmt.strip()}
    unknown = requested - {"docx", "pdf"}
    if unknown:
        print(f"[error] unsupported formats: {', '.join(sorted(unknown))}")
        return 1

    outdir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else input_md.parent.resolve()
    )
    outdir.mkdir(parents=True, exist_ok=True)

    base = input_md.stem
    output_docx = outdir / f"{base}.docx"
    output_pdf = outdir / f"{base}.pdf"

    ok = True
    docx_generated = False
    if "docx" in requested:
        docx_generated = export_docx(input_md, output_docx)
        ok = ok and docx_generated

    if "pdf" in requested:
        docx_hint = output_docx if docx_generated or output_docx.exists() else None
        pdf_generated = export_pdf(input_md, output_pdf, docx_hint)
        ok = ok and pdf_generated

    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
