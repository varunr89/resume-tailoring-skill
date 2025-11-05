# Resume Tailoring Skill

> AI-powered resume generation that researches roles, surfaces undocumented experiences, and creates tailored resumes from your existing resume library.

**Mission:** Your ability to get a job should be based on your experiences and capabilities, not on your resume writing skills.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [License](#license)

## Overview

This Claude Code skill generates high-quality, tailored resumes optimized for specific job descriptions while maintaining factual integrity. It goes beyond simple keyword matching by:

- **Multi-Job Batch Processing:** Process 3-5 similar jobs efficiently with shared experience discovery (NEW!)
- **Deep Research:** Analyzes company culture, role requirements, and success profiles
- **Experience Discovery:** Surfaces undocumented experiences through conversational branching interviews
- **Smart Matching:** Uses confidence-scored content selection with transparent gap identification
- **Multi-Format Output:** Generates professional MD, DOCX, PDF, and interview prep reports
- **Self-Improving:** Library grows with each successful resume

## Installation

### Option 1: Install from GitHub (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/varunr89/resume-tailoring-skill.git ~/.claude/skills/resume-tailoring
   ```

2. **Verify installation:**
   ```bash
   ls ~/.claude/skills/resume-tailoring
   ```
   You should see: `SKILL.md`, `research-prompts.md`, `matching-strategies.md`, `branching-questions.md`, `README.md`

3. **Restart Claude Code** (if already running)

### Option 2: Manual Installation

1. **Create the skill directory:**
   ```bash
   mkdir -p ~/.claude/skills/resume-tailoring
   ```

2. **Download the files:**
   - Download all files from this repository
   - Place them in `~/.claude/skills/resume-tailoring/`

3. **Verify installation:**
   - Open Claude Code
   - Type `/skills` to see available skills
   - `resume-tailoring` should appear in the list

## Prerequisites

**Required:**
- Claude Code with skills enabled
- Existing resume library (at least 1-2 resumes in markdown format)

**Optional but Recommended:**
- WebSearch capability (for company research)
- `document-skills` plugin (for DOCX/PDF generation)
- 10+ resumes in your library for best results

**Resume Library Setup:**

Create a `resumes/` directory in your project:
```bash
mkdir -p ~/resumes
```

Add your existing resumes in markdown format:
```
~/resumes/
├── Resume_Company1_Role1.md
├── Resume_Company2_Role2.md
└── Resume_General_2024.md
```

## Quick Start

### Single Job Application
**1. Invoke the skill in Claude Code:**
```
"I want to apply for [Role] at [Company]. Here's the JD: [paste job description]"
```

**2. The skill will automatically:**
1. Build library from existing resumes
2. Research company and role
3. Create optimized template (with checkpoint)
4. Offer branching experience discovery
5. Match content with confidence scores (with checkpoint)
6. Generate MD + DOCX + PDF + Report
7. Optionally update library

**3. Review and approve:**
- Checkpoints at key decision points
- Full transparency on content matching
- Option to revise or approve at each stage

### Multiple Jobs (Batch Mode - NEW!)
**1. Provide multiple job descriptions:**
```
"I want to apply for these 3 roles:
1. [Company 1] - [Role]: [JD or URL]
2. [Company 2] - [Role]: [JD or URL]
3. [Company 3] - [Role]: [JD or URL]"
```

**2. The skill will:**
1. Detect multi-job intent and offer batch mode
2. Build library once (shared across all jobs)
3. Analyze gaps across ALL jobs (deduplicates common requirements)
4. Conduct single discovery session addressing all gaps
5. Process each job individually (research + tailoring)
6. Present all resumes for batch review

**3. Time savings:**
- Shared discovery session (ask once, not 3-5 times)
- 11-27% faster than processing jobs sequentially
- Same quality as single-job mode

## Files

### Core Implementation
- `SKILL.md` - Main skill implementation with single-job and multi-job workflows
- `multi-job-workflow.md` - Complete multi-job batch processing workflow
- `research-prompts.md` - Company/role research templates
- `matching-strategies.md` - Content scoring algorithms
- `branching-questions.md` - Experience discovery patterns

### Documentation
- `README.md` - This file
- `MARKETPLACE.md` - Marketplace listing information
- `SUBMISSION_GUIDE.md` - Skill submission guidelines

### Supporting Documentation (`docs/`)
- `docs/schemas/` - Data structure schemas for batch processing
  - `batch-state-schema.md` - Batch state tracking structure
  - `job-schema.md` - Job object schema
- `docs/plans/` - Design documents and implementation plans
  - `2025-11-04-multi-job-resume-tailoring-design.md` - Multi-job feature design
  - `2025-11-04-multi-job-implementation-summary.md` - Implementation summary
- `docs/testing/` - Testing checklists
  - `multi-job-test-checklist.md` - Comprehensive multi-job test cases

## Key Features

**🚀 Multi-Job Batch Processing (NEW!)**
- Process 3-5 similar jobs efficiently
- Shared experience discovery (ask once, apply to all)
- Aggregate gap analysis with deduplication
- Time savings: 11-27% faster than sequential processing
- Incremental batches (add more jobs later)

**🔍 Deep Research**
- Company culture and values
- Role benchmarking via LinkedIn
- Success profile synthesis

**💬 Branching Discovery**
- Conversational experience surfacing
- Dynamic follow-up questions
- Surfaces undocumented work
- Multi-job context awareness

**🎯 Smart Matching**
- Confidence-scored content selection
- Transparent gap identification
- Truth-preserving reframing

**📄 Multi-Format Output**
- Professional markdown
- ATS-friendly DOCX
- Print-ready PDF
- Interview prep report

**🔄 Self-Improving**
- Library grows with each resume
- Successful patterns reused
- New experiences captured

## Architecture

### Single-Job Workflow
```
Phase 0: Library Build (always first)
   ↓
Phase 1: Research (JD + Company + Role)
   ↓
Phase 2: Template (Structure + Titles)
   ↓  [CHECKPOINT]
Phase 2.5: Experience Discovery (Optional, Branching)
   ↓
Phase 3: Assembly (Matching + Scoring)
   ↓  [CHECKPOINT]
Phase 4: Generation (MD + DOCX + PDF + Report)
   ↓  [USER REVIEW]
Phase 5: Library Update (Conditional)
```

### Multi-Job Workflow (NEW!)
```
Phase 0: Intake & Batch Initialization
   ↓
Phase 1: Aggregate Gap Analysis (deduplicates across all jobs)
   ↓
Phase 2: Shared Experience Discovery (ask once, apply to all)
   ↓
Phase 3: Per-Job Processing (research + template + matching + generation for each)
   ↓
Phase 4: Batch Finalization (review all resumes, update library)
```

**Time Savings:**
- 3 jobs: ~40 min vs ~45 min sequential (11% savings)
- 5 jobs: ~55 min vs ~75 min sequential (27% savings)

See `multi-job-workflow.md` for complete details.

## Design Philosophy

**Truth-Preserving Optimization:**
- NEVER fabricate experience
- Intelligently reframe and emphasize
- Transparent about gaps

**Holistic Person Focus:**
- Surface undocumented experiences
- Value volunteer work, side projects
- Build around complete background

**User Control:**
- Checkpoints at key decisions
- Options, not mandates
- Can adjust or go back

## Usage Examples

### Example 1: Internal Role Transfer

```
USER: "I want to apply for Principal PM role in 1ES team at Microsoft.
      Here's the JD: [paste]"

RESULT:
- Found 29 existing resumes
- Researched Microsoft 1ES team culture
- Featured PM2 Azure Eng Systems experience
- Discovered: VS Code extension, AI side projects
- 92% JD coverage, 75% direct matches
- Generated tailored resume + interview prep report
```

### Example 2: Career Transition

```
USER: "I'm a TPM transitioning to ecology PM. JD: [paste]"

RESULT:
- Reframed "Technical Program Manager" → "Program Manager, Environmental Systems"
- Surfaced volunteer conservation work
- Identified graduate research in environmental modeling
- 65% JD coverage with clear gap analysis
- Cover letter recommendations provided
```

### Example 3: Career Gap Handling

```
USER: "I have a 2-year gap from starting a company. JD: [paste]"

RESULT:
- Included startup as legitimate role
- Surfaced: fundraising, product development, team building
- Framed gap as entrepreneurial experience
- Generated resume showing initiative and diverse skills
```

### Example 4: Multi-Job Batch (NEW!)

```
USER: "I want to apply for these 3 TPM roles:
      1. Microsoft 1ES Principal PM
      2. Google Cloud Senior TPM
      3. AWS Container Services Senior PM"

RESULT:
- Detected multi-job mode, user confirmed
- Built library once (29 resumes)
- Gap analysis: 14 total gaps, 8 unique after deduplication
- Shared discovery: 30-min session surfaced 5 new experiences
  * Kubernetes CI/CD for nonprofits
  * Azure migration for university lab
  * Cross-functional leadership examples
- Processed 3 jobs: 85%, 88%, 78% JD coverage
- Time: 40 minutes vs 45 minutes sequential (11% savings)
- All 3 resumes + batch summary generated
```

### Example 5: Incremental Batch Addition (NEW!)

```
WEEK 1: User processes 3 jobs (Microsoft, Google, AWS) in 40 minutes

WEEK 2:
USER: "I found 2 more jobs at Stripe and Meta. Add them to my batch?"

RESULT:
- Loaded existing batch with 5 previously discovered experiences
- Incremental gap analysis: only 3 new gaps (vs 14 original)
- Quick 10-min discovery session for new gaps only
- Processed 2 additional jobs: 82%, 76% coverage
- Time: 20 minutes (vs 30 if starting from scratch)
- Total: 5 jobs, 8 experiences discovered
```

## Usage Patterns

**Internal role (same company):**
- Features most relevant internal experience
- Uses internal terminology
- Leverages organizational knowledge

**External role (new company):**
- Deep company research
- Cultural fit emphasis
- Risk mitigation

**Career transition:**
- Title reframing
- Transferable skill emphasis
- Bridge domain gaps

**With career gaps:**
- Gaps as valuable experience
- Alternative activities highlighted
- Truthful, positive framing

## Testing

### Single-Job Tests
See Testing Guidelines section in SKILL.md (lines 1244-1320)

**Key test scenarios:**
- Happy path (full workflow)
- Minimal library (2 resumes)
- Research failures (obscure company)
- Experience discovery value
- Title reframing accuracy
- Multi-format generation

### Multi-Job Tests (NEW!)
See `docs/testing/multi-job-test-checklist.md` for comprehensive test cases

**Key multi-job scenarios:**
- Happy path (3 similar jobs)
- Diverse jobs (low overlap detection)
- Incremental batch addition
- Pause/resume functionality
- Individual vs batch review
- Express mode processing
- Error handling and graceful degradation

**Run tests:**
```bash
cd ~/.claude/skills/resume-tailoring
# Single-job: Follow test procedures in SKILL.md Testing Guidelines section
# Multi-job: Follow docs/testing/multi-job-test-checklist.md
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Make your changes:**
   - Update `SKILL.md` for implementation changes
   - Add tests if applicable
   - Update README if architecture changes
4. **Commit with descriptive messages:** `git commit -m "feat: add amazing feature"`
5. **Push to your fork:** `git push origin feature/amazing-feature`
6. **Open a Pull Request**

**Before submitting:**
- Run regression tests (see Testing section in SKILL.md)
- Ensure all phases work end-to-end
- Update documentation

## Troubleshooting

**Skill not appearing:**
- Verify files are in `~/.claude/skills/resume-tailoring/`
- Restart Claude Code
- Check SKILL.md has valid YAML frontmatter

**Research phase failing:**
- Check WebSearch capability is enabled
- Skill will gracefully fall back to JD-only analysis

**DOCX/PDF generation failing:**
- Ensure `document-skills` plugin is installed
- Skill will fall back to markdown-only output

**Low match confidence:**
- Try the Experience Discovery phase
- Consider adding more resumes to your library
- Review gap handling recommendations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for Claude Code skills framework
- Designed with truth-preserving optimization principles
- Inspired by the belief that job opportunities should be based on capabilities, not resume writing skills

## Support

- **Issues:** [GitHub Issues](https://github.com/varunr89/resume-tailoring-skill/issues)
- **Discussions:** [GitHub Discussions](https://github.com/varunr89/resume-tailoring-skill/discussions)

## Roadmap

- [ ] Cover letter generation integration
- [ ] LinkedIn profile optimization
- [ ] Interview preparation Q&A generation
- [ ] Multi-language resume support
- [ ] Custom industry templates
