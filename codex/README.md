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
- `scripts/export_resume.py` - local DOCX/PDF export helper
