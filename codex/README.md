# Resume Tailoring Skill (Codex Variant)

This folder contains the Codex-specific version of the resume tailoring skill.

- Root `SKILL.md` is kept for Claude Code.
- `codex/SKILL.md` is for Codex.

## Install in Codex

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo varunr89/resume-tailoring-skill \
  --ref master \
  --path codex \
  --name resume-tailoring
```

Restart Codex after installation.

## Files

- `SKILL.md` - Codex-only workflow
- `research-prompts.md` - company and role research templates
- `matching-strategies.md` - confidence scoring and mapping logic
- `branching-questions.md` - experience discovery patterns
- `multi-job-workflow.md` - batch workflow details
- `scripts/prepare_resume_sources.py` - normalize source resumes and emit a generated master library
- `scripts/rank_project_library.py` - rank structured project catalog entries against a job description
- `scripts/export_resume.py` - local DOCX/PDF export helper
- `scripts/render_pretty_resume.py` - styled one-page HTML/PDF renderer from resume markdown

## Recommended Resume Library Layout

```text
resumes/
├── source/
├── library/
│   ├── MASTER_EXPERIENCE_LIBRARY.md
│   ├── PROJECT_EXPERIENCE_LIBRARY.json
│   ├── PROJECT_EXPERIENCE_LIBRARY.md
│   └── MASTER_EXPERIENCE_LIBRARY.generated.md
└── assets/
```

Use `MASTER_EXPERIENCE_LIBRARY.md` as the canonical, hand-maintained source for past experience. Use the generated file as fallback/reference after running `scripts/prepare_resume_sources.py`.
Use `PROJECT_EXPERIENCE_LIBRARY.json` as the primary structured catalog for deterministic job-to-project matching.
Use `PROJECT_EXPERIENCE_LIBRARY.md` as the human-readable companion index.
