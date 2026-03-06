#!/usr/bin/env python3
"""Prepare a resume library from source files (PDF/MD/TXT).

Primary use case:
- User provides existing resume PDFs in resumes/source/
- Script extracts text into resumes/library/*.md
- Script extracts embedded images into resumes/assets/
- Script emits a generated master library file for fallback/reference
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def safe_stem(path: Path) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in path.stem).strip("_")


def strip_resume_source_header(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# Resume Source:"):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    return "\n".join(lines).strip()


def extract_pdf(pdf_path: Path, library_dir: Path, assets_dir: Path) -> tuple[Path | None, list[Path]]:
    try:
        from pypdf import PdfReader
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("pypdf is required for PDF extraction") from exc

    reader = PdfReader(str(pdf_path))
    text_parts: list[str] = []
    image_outputs: list[Path] = []
    largest_img: tuple[int, Path] | None = None

    for page_index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            text_parts.append(f"\n\n--- PAGE {page_index} ---\n{text}")

        for image_index, image in enumerate(page.images, start=1):
            name = image.name or f"img_p{page_index}_{image_index}"
            ext = name.split(".")[-1].lower() if "." in name else "bin"
            if ext == "jpx":
                ext = "jp2"
            if ext not in {"jpg", "jpeg", "png", "jp2"}:
                ext = "bin"

            out_name = f"{safe_stem(pdf_path)}_p{page_index}_{image_index}.{ext}"
            out_path = assets_dir / out_name
            out_path.write_bytes(image.data)
            image_outputs.append(out_path)

            img_size = len(image.data)
            if largest_img is None or img_size > largest_img[0]:
                largest_img = (img_size, out_path)

    full_text = "\n".join(text_parts).strip()
    if not full_text:
        return None, image_outputs

    md_out = library_dir / f"{safe_stem(pdf_path)}.md"
    md_out.write_text(
        f"# Resume Source: {pdf_path.name}\n\n{full_text}\n",
        encoding="utf-8",
    )

    if largest_img is not None:
        profile_candidate = assets_dir / "profile_candidate.jpg"
        shutil.copyfile(largest_img[1], profile_candidate)

    return md_out, image_outputs


def process_text_like(src: Path, library_dir: Path) -> Path:
    out = library_dir / f"{safe_stem(src)}.md"
    raw = src.read_text(encoding="utf-8", errors="ignore")
    out.write_text(f"# Resume Source: {src.name}\n\n{raw}\n", encoding="utf-8")
    return out


def build_generated_master(
    prepared: list[Path], source_dir: Path, master_library: Path
) -> None:
    timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    parts: list[str] = [
        "# MASTER EXPERIENCE LIBRARY (Generated)",
        "",
        "This file is generated from the normalized resume sources in this workspace.",
        "If a hand-maintained `MASTER_EXPERIENCE_LIBRARY.md` exists, prefer that file for tailoring and update it with new discoveries.",
        "",
        f"Generated: {timestamp}",
        f"Source directory: `{source_dir}`",
        "",
        "## Source Inventory",
        "",
    ]

    for item in prepared:
        parts.append(f"- `{item.name}`")

    parts.extend(
        [
            "",
            "## Normalized Source Content",
            "",
        ]
    )

    for item in prepared:
        body = strip_resume_source_header(item.read_text(encoding="utf-8", errors="ignore"))
        parts.extend(
            [
                f"### {item.name}",
                "",
                body or "_No extractable content._",
                "",
            ]
        )

    master_library.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare resume sources for tailoring.")
    parser.add_argument("--source-dir", required=True, help="Directory with source resumes")
    parser.add_argument("--library-dir", required=True, help="Directory for normalized markdown resumes")
    parser.add_argument("--assets-dir", required=True, help="Directory for extracted assets (images)")
    parser.add_argument(
        "--master-library",
        default=None,
        help="Optional output path for generated master library markdown",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_dir = Path(args.source_dir).expanduser().resolve()
    library_dir = Path(args.library_dir).expanduser().resolve()
    assets_dir = Path(args.assets_dir).expanduser().resolve()
    master_library = (
        Path(args.master_library).expanduser().resolve()
        if args.master_library
        else library_dir / "MASTER_EXPERIENCE_LIBRARY.generated.md"
    )

    if not source_dir.exists():
        print(f"[error] source dir not found: {source_dir}")
        return 1

    ensure_dir(library_dir)
    ensure_dir(assets_dir)

    prepared: list[Path] = []
    extracted_images = 0

    for src in sorted(source_dir.iterdir()):
        if not src.is_file():
            continue
        suffix = src.suffix.lower()
        try:
            if suffix == ".pdf":
                md_out, imgs = extract_pdf(src, library_dir, assets_dir)
                extracted_images += len(imgs)
                if md_out:
                    prepared.append(md_out)
            elif suffix in {".md", ".txt"}:
                prepared.append(process_text_like(src, library_dir))
        except Exception as exc:
            print(f"[warn] failed to process {src.name}: {exc}")

    if prepared:
        build_generated_master(prepared, source_dir, master_library)

    print(f"[ok] prepared_markdown={len(prepared)} extracted_images={extracted_images}")
    for item in prepared:
        print(f" - {item}")
    if prepared:
        print(f"[ok] generated_master={master_library}")
    profile_candidate = assets_dir / "profile_candidate.jpg"
    if profile_candidate.exists():
        print(f"[ok] profile_candidate={profile_candidate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
