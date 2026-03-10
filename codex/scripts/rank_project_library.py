#!/usr/bin/env python3
"""Rank project-catalog entries against a job description.

The goal is deterministic first-pass project selection before resume assembly.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+.#/\-]*")

SYNONYMS = {
    "bluetooth low energy": ["ble", "bluetooth"],
    "ci/cd": ["ci", "cd", "fastlane", "gitlab", "pipeline", "release"],
    "swift package manager": ["spm", "swift package manager"],
    "uikit": ["ui kit", "uikit"],
    "swiftui": ["swift ui", "swiftui"],
    "xctest": ["unit test", "tests", "testing", "xctest"],
    "consumer mobile": ["consumer", "mobile app", "ios app"],
    "medical devices": ["healthcare devices", "connected devices", "medical"],
    "cross-functional": ["product", "design", "qa", "backend", "android"],
    "release automation": ["testflight", "firebase distribution", "app store", "release", "deploy"],
}


def tokenize(text: str) -> set[str]:
    lowered = text.lower()
    tokens = set(TOKEN_RE.findall(lowered))
    for phrase, expansions in SYNONYMS.items():
        if phrase in lowered:
            tokens.update(expansions)
    return tokens


def flatten_strings(project: dict) -> dict[str, str]:
    return {
        "technologies": " ".join(project.get("technologies", [])),
        "domains": " ".join(project.get("domains", [])),
        "delivery_signals": " ".join(project.get("delivery_signals", [])),
        "best_used_for": " ".join(project.get("best_used_for", [])),
        "summary": project.get("summary", ""),
        "identity": " ".join(
            [
                project.get("name", ""),
                project.get("company", ""),
                project.get("role", ""),
                " ".join(project.get("repos", [])),
            ]
        ),
    }


def score_project(job_tokens: set[str], project: dict) -> dict:
    flattened = flatten_strings(project)
    field_weights = {
        "technologies": 5,
        "domains": 3,
        "delivery_signals": 2,
        "best_used_for": 2,
        "summary": 1,
        "identity": 1,
    }

    matches: dict[str, list[str]] = {}
    score = 0
    for field, weight in field_weights.items():
        field_tokens = tokenize(flattened[field])
        overlap = sorted(job_tokens & field_tokens)
        if overlap:
            matches[field] = overlap
            score += len(overlap) * weight

    if "ios" in job_tokens and "swift" in tokenize(flattened["technologies"]):
        score += 2
    if "lead" in job_tokens or "senior" in job_tokens:
        if "leadership" in tokenize(flattened["best_used_for"] + " " + flattened["delivery_signals"]):
            score += 2

    return {
        "slug": project.get("slug"),
        "name": project.get("name"),
        "company": project.get("company"),
        "role": project.get("role"),
        "period": project.get("period"),
        "score": score,
        "matches": matches,
        "summary": project.get("summary", ""),
        "technologies": project.get("technologies", []),
        "domains": project.get("domains", []),
        "best_used_for": project.get("best_used_for", []),
    }


def tier_for_score(score: int) -> str:
    if score >= 18:
        return "tier_1"
    if score >= 9:
        return "tier_2"
    return "tier_3"


def render_markdown(results: list[dict], top_n: int) -> str:
    lines = [
        "# Ranked Project Shortlist",
        "",
        f"Top results requested: {top_n}",
        "",
    ]
    for index, item in enumerate(results[:top_n], start=1):
        tier = tier_for_score(item["score"])
        lines.extend(
            [
                f"## {index}. {item['name']}",
                f"- Tier: {tier}",
                f"- Score: {item['score']}",
                f"- Role: {item['role']}",
                f"- Period: {item['period']}",
                f"- Technologies: {', '.join(item['technologies'])}",
                f"- Domains: {', '.join(item['domains'])}",
                f"- Best used for: {', '.join(item['best_used_for'])}",
                f"- Summary: {item['summary']}",
            ]
        )
        if item["matches"]:
            lines.append("- Match evidence:")
            for field, overlap in item["matches"].items():
                lines.append(f"  - {field}: {', '.join(overlap[:12])}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rank project catalog entries against a JD.")
    parser.add_argument("--catalog", required=True, help="Path to PROJECT_EXPERIENCE_LIBRARY.json")
    parser.add_argument("--job-file", help="Path to a text/markdown file containing job description")
    parser.add_argument("--job-text", help="Raw job description text")
    parser.add_argument("--top", type=int, default=6, help="Maximum number of projects to return")
    parser.add_argument("--output", help="Optional output markdown path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.job_file and not args.job_text:
        print("[error] provide --job-file or --job-text")
        return 1

    catalog_path = Path(args.catalog).expanduser().resolve()
    if not catalog_path.exists():
        print(f"[error] catalog not found: {catalog_path}")
        return 1

    if args.job_file:
        job_text = Path(args.job_file).expanduser().resolve().read_text(encoding="utf-8", errors="ignore")
    else:
        job_text = args.job_text or ""

    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    projects = payload.get("projects", [])
    job_tokens = tokenize(job_text)
    scored = [score_project(job_tokens, project) for project in projects]
    ranked = sorted(scored, key=lambda item: (-item["score"], item["name"]))

    text = render_markdown(ranked, args.top)
    if args.output:
        out = Path(args.output).expanduser().resolve()
        out.write_text(text, encoding="utf-8")
        print(f"[ok] wrote {out}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
