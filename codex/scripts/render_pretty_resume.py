#!/usr/bin/env python3
"""Render a styled resume HTML/PDF from a markdown resume draft.

This script is intentionally format-tolerant for markdown produced by this skill.
"""

from __future__ import annotations

import argparse
import html
from pathlib import Path


def parse_markdown(md_text: str) -> dict:
    lines = md_text.splitlines()
    data: dict = {
        "name": "",
        "role": "",
        "contacts": [],
        "summary": "",
        "skills": [],
        "experience": [],
        "projects": [],
        "fit": [],
        "image_from_md": "",
    }

    # Optional markdown image at top.
    for line in lines:
        s = line.strip()
        if s.startswith("![") and "](" in s and s.endswith(")"):
            data["image_from_md"] = s[s.find("(") + 1 : -1]
            break

    i = 0
    n = len(lines)
    current_section = ""
    while i < n:
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Ignore markdown image lines while parsing body content.
        if line.startswith("![") and "](" in line and line.endswith(")"):
            i += 1
            continue

        if line.startswith("# ") and not data["name"]:
            data["name"] = line[2:].strip()
            i += 1
            continue

        if line.startswith("**") and line.endswith("**") and not data["role"]:
            data["role"] = line.strip("*").strip()
            i += 1
            continue

        if line.startswith("## "):
            current_section = line[3:].strip().lower()
            i += 1
            continue

        if line.startswith("### "):
            title = line[4:].strip()
            meta = ""
            bullets: list[str] = []
            subtitle = ""
            i += 1
            while i < n and not lines[i].strip():
                i += 1
            if i < n and lines[i].strip().startswith("**"):
                meta = lines[i].strip().replace("**", "").strip()
                i += 1
            if i < n and lines[i].strip() and not lines[i].strip().startswith("-") and not lines[i].strip().startswith("## "):
                subtitle = lines[i].strip()
                i += 1
            while i < n:
                s = lines[i].strip()
                if not s:
                    i += 1
                    continue
                if s.startswith("## ") or s.startswith("### "):
                    break
                if s.startswith("- "):
                    bullets.append(s[2:].strip())
                i += 1
            item = {"title": title, "meta": meta, "subtitle": subtitle, "bullets": bullets}
            if "project" in current_section or "highlight" in current_section:
                data["projects"].append(item)
            else:
                data["experience"].append(item)
            continue

        # Section content collection.
        if current_section == "professional summary":
            parts = [line]
            i += 1
            while i < n and lines[i].strip() and not lines[i].strip().startswith("## "):
                parts.append(lines[i].strip())
                i += 1
            data["summary"] = " ".join(parts).strip()
            continue

        if current_section == "core skills" and line.startswith("- "):
            data["skills"].append(line[2:].strip())
            i += 1
            continue

        if "role alignment" in current_section and line.startswith("- "):
            data["fit"].append(line[2:].strip())
            i += 1
            continue

        # Contacts (lines between role and first section)
        if not current_section and line and not line.startswith("#"):
            if line not in data["contacts"]:
                data["contacts"].append(line.rstrip("\\"))
        i += 1

    return data


def _li(items: list[str]) -> str:
    return "".join(f"<li>{html.escape(x)}</li>" for x in items)


def _items(items: list[dict]) -> str:
    blocks: list[str] = []
    for item in items:
        blocks.append(
            f"""
            <div class="item">
              <div class="row">
                <div class="title">{html.escape(item.get('title',''))}</div>
                <div class="meta">{html.escape(item.get('meta',''))}</div>
              </div>
              {"<p class='sub'>" + html.escape(item.get('subtitle','')) + "</p>" if item.get("subtitle") else ""}
              <ul class="points">{_li(item.get("bullets", []))}</ul>
            </div>
            """
        )
    return "\n".join(blocks)


def build_html(data: dict, profile_image: str, target_label: str) -> str:
    fit_boxes = "".join(
        f"<div class='fit'><strong>Fit</strong>{html.escape(point)}</div>" for point in data.get("fit", [])[:4]
    )
    headline_right = f"<p class='target'>{html.escape(target_label)}</p>" if target_label else ""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(data.get("name","Resume"))} - Resume</title>
  <style>
    @page {{ size: A4; margin: 0; }}
    :root {{
      --ink: #132033; --muted: #5a6a7d; --line: #d8e0ea; --panel: #edf3fb;
      --accent: #0f4c81;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: "Avenir Next", "Segoe UI", "Trebuchet MS", sans-serif; color: var(--ink); }}
    .page {{ width: 210mm; min-height: 297mm; display: grid; grid-template-columns: 68mm 1fr; }}
    .left {{ background: linear-gradient(180deg, #0f4c81 0%, #0e3e67 55%, #102f4d 100%); color: #f6f9fd; padding: 14mm 8mm 12mm; }}
    .right {{ padding: 13mm 12mm 12mm; }}
    .photo {{ width: 36mm; height: 36mm; margin: 0 auto 6mm; border-radius: 50%; overflow: hidden; border: 2.5mm solid rgba(255,255,255,0.25); background: #fff; }}
    .photo img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .name {{ text-align: center; margin: 0; font-size: 20px; line-height: 1.15; font-weight: 700; }}
    .role {{ text-align: center; margin: 2.5mm 0 8mm; font-size: 10.5px; line-height: 1.35; color: #dce8f6; font-weight: 600; }}
    .left h3 {{ margin: 8mm 0 3mm; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: #b9d7f3; border-top: 0.3mm solid rgba(255,255,255,0.2); padding-top: 2.3mm; }}
    .left p, .left li, .left a {{ font-size: 9.2px; line-height: 1.45; margin: 0; color: #f2f7fc; text-decoration: none; word-break: break-word; }}
    .contact-list {{ display: grid; gap: 2.2mm; }}
    .left ul {{ margin: 1mm 0 0; padding-left: 3.8mm; }}
    .skills-list {{ margin-top: 1.6mm; display: grid; gap: 1.6mm; }}
    .skills-list li {{ font-size: 8.8px; line-height: 1.25; }}
    .headline {{ display: flex; justify-content: space-between; align-items: baseline; gap: 5mm; margin-bottom: 4mm; }}
    .headline h1 {{ margin: 0; font-size: 25px; line-height: 1.05; color: var(--accent); }}
    .headline .target {{ margin: 0; font-size: 10px; color: var(--muted); text-align: right; font-weight: 600; }}
    .summary {{ background: var(--panel); border-left: 1.2mm solid var(--accent); border-radius: 1.2mm; padding: 3.3mm 3.6mm; font-size: 10.2px; line-height: 1.5; margin-bottom: 5.4mm; }}
    .section {{ margin-bottom: 5.2mm; }}
    .section h2 {{ margin: 0 0 2.8mm; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: var(--accent); border-bottom: 0.35mm solid var(--line); padding-bottom: 1.5mm; }}
    .item {{ margin-bottom: 3.1mm; }}
    .row {{ display: flex; justify-content: space-between; align-items: baseline; gap: 4mm; }}
    .row .title {{ font-size: 11px; font-weight: 700; color: #10253a; }}
    .row .meta {{ font-size: 9px; color: var(--muted); white-space: nowrap; font-weight: 600; }}
    .sub {{ margin-top: 0.7mm; font-size: 9.6px; color: #30435a; font-weight: 600; }}
    ul.points {{ margin: 1.4mm 0 0; padding-left: 4.3mm; }}
    ul.points li {{ font-size: 9.5px; line-height: 1.45; margin-bottom: 1.2mm; }}
    .fit-box {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2.2mm; }}
    .fit {{ background: #f8fbff; border: 0.3mm solid var(--line); border-radius: 1.2mm; padding: 2.4mm 2.8mm; font-size: 9.2px; line-height: 1.4; }}
    .fit strong {{ display: block; color: var(--accent); margin-bottom: 0.7mm; font-size: 9.3px; text-transform: uppercase; letter-spacing: 0.4px; }}
  </style>
</head>
<body>
  <main class="page">
    <aside class="left">
      <div class="photo"><img src="{html.escape(profile_image)}" alt="{html.escape(data.get("name","Profile"))}" /></div>
      <h2 class="name">{html.escape(data.get("name",""))}</h2>
      <p class="role">{html.escape(data.get("role",""))}</p>
      <h3>Contact</h3>
      <div class="contact-list">{"".join(f"<p>{html.escape(c)}</p>" for c in data.get("contacts",[])[:4])}</div>
      <h3>Core Skills</h3>
      <ul class="skills-list">{_li(data.get("skills", [])[:12])}</ul>
    </aside>
    <section class="right">
      <div class="headline">
        <h1>iOS Engineer Resume</h1>
        {headline_right}
      </div>
      <div class="summary">{html.escape(data.get("summary",""))}</div>
      <div class="section"><h2>Professional Experience</h2>{_items(data.get("experience", []))}</div>
      <div class="section"><h2>Selected Project Highlights</h2>{_items(data.get("projects", []))}</div>
      <div class="section"><h2>Role Fit</h2><div class="fit-box">{fit_boxes}</div></div>
    </section>
  </main>
</body>
</html>"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a styled resume PDF from markdown.")
    parser.add_argument("--input-md", required=True, help="Input markdown resume")
    parser.add_argument("--output-html", help="Output HTML path (default: <stem>.html)")
    parser.add_argument("--output-pdf", help="Output PDF path (default: <stem>.pdf)")
    parser.add_argument("--profile-image", help="Path/URL to profile image")
    parser.add_argument("--target-label", default="", help="Optional small right-side label in header")
    parser.add_argument("--no-pdf", action="store_true", help="Generate only HTML")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_md = Path(args.input_md).expanduser().resolve()
    if not input_md.exists():
        print(f"[error] input not found: {input_md}")
        return 1

    out_html = (
        Path(args.output_html).expanduser().resolve()
        if args.output_html
        else input_md.with_suffix(".html")
    )
    out_pdf = (
        Path(args.output_pdf).expanduser().resolve()
        if args.output_pdf
        else input_md.with_suffix(".pdf")
    )

    md_text = input_md.read_text(encoding="utf-8", errors="ignore")
    parsed = parse_markdown(md_text)

    profile_image = args.profile_image or parsed.get("image_from_md") or ""
    if not profile_image:
        profile_image = "https://dummyimage.com/400x400/e6eef7/7f8fa3.jpg&text=Profile"

    html_text = build_html(parsed, profile_image, args.target_label)
    out_html.write_text(html_text, encoding="utf-8")
    print(f"[ok] html={out_html}")

    if args.no_pdf:
        return 0

    try:
        from weasyprint import HTML
    except Exception:
        print("[error] weasyprint is required for PDF rendering")
        return 2

    HTML(string=html_text, base_url=str(out_html.parent)).write_pdf(str(out_pdf))
    print(f"[ok] pdf={out_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
