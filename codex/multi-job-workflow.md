# Multi-Job Resume Tailoring Workflow

## Overview

Handles 3-5 similar jobs efficiently by consolidating experience discovery while maintaining per-job research depth.

**Architecture:** Shared Discovery + Per-Job Tailoring

**Target Use Case:**
- Small batches (3-5 jobs)
- Moderately similar roles (60%+ requirement overlap)
- Continuous workflow (add jobs incrementally)

## Phase 0: Job Intake & Batch Initialization

**Goal:** Collect all job descriptions and initialize batch structure

**User Interaction:**

```
SKILL: "Let's set up your multi-job batch. How would you like to provide
the job descriptions?

1. Paste them all now (recommended for efficiency)
2. Provide one at a time
3. Provide URLs to fetch

For each job, I need:
- Job description (text or URL)
- Company name (if not in JD)
- Role title (if not in JD)
- Optional: Priority (high/medium/low) or notes"
```

**Data Collection Loop:**

For each job (until user says "done"):
1. Collect JD text or URL
2. Collect company name (extract from JD if possible, else ask)
3. Collect role title (extract from JD if possible, else ask)
4. Ask: "Priority for this job? (high/medium/low, default: medium)"
5. Ask: "Any notes about this job? (optional, e.g., 'referral from X')"
6. Assign job_id: "job-1", "job-2", etc.
7. Set status: "pending"
8. Add to batch

**Quick JD Parsing:**

For each job, lightweight extraction (NOT full research yet):

```python
# Pseudo-code
def quick_parse_jd(jd_text):
    return {
        "requirements_must_have": extract_requirements(jd_text, required=True),
        "requirements_nice_to_have": extract_requirements(jd_text, required=False),
        "technical_skills": extract_technical_keywords(jd_text),
        "soft_skills": extract_soft_skills(jd_text),
        "domain_areas": identify_domains(jd_text)
    }
```

Purpose: Just enough to identify gaps for discovery phase. Full research happens per-job later.

**Batch Initialization:**

Create batch directory structure:

```
resumes/batches/batch-{YYYY-MM-DD}-{slug}/
├── _batch_state.json          # State tracking
├── _aggregate_gaps.md         # Gap analysis (created in Phase 1)
├── _discovered_experiences.md # Discovery output (created in Phase 2)
└── (job directories created during per-job processing)
```

Initialize _batch_state.json:

```json
{
  "batch_id": "batch-2025-11-04-job-search",
  "created": "2025-11-04T10:30:00Z",
  "current_phase": "intake",
  "processing_mode": "interactive",
  "jobs": [
    {
      "job_id": "job-1",
      "company": "Microsoft",
      "role": "Principal PM - 1ES",
      "jd_text": "...",
      "jd_url": "https://...",
      "priority": "high",
      "notes": "Internal referral from Alice",
      "status": "pending",
      "requirements": ["Kubernetes", "CI/CD", "Leadership"],
      "gaps": []
    }
  ],
  "discoveries": [],
  "aggregate_gaps": {}
}
```

**Library Initialization:**

Run standard Phase 0 from SKILL.md (library initialization) once for the entire batch.

**Output:**

```
"Batch initialized with {N} jobs:
- Job 1: {Company} - {Role} (priority: {priority})
- Job 2: {Company} - {Role}
...

Next: Aggregate gap analysis across all jobs.
Continue? (Y/N)"
```

**Checkpoint:** User confirms batch is complete before proceeding.

## Phase 1: Aggregate Gap Analysis

**Goal:** Build unified gap list across all jobs to guide single efficient discovery session

**Process:**

**1.1 Extract Requirements from All JDs:**

For each job:
- Parse requirements (already done in Phase 0 quick parse)
- Categorize: must-have vs nice-to-have
- Extract keywords and skill areas

Example output:
```
Job 1 (Microsoft 1ES): Kubernetes, CI/CD, cross-functional leadership, Azure
Job 2 (Google Cloud): Kubernetes, GCP, distributed systems, team management
Job 3 (AWS): Container orchestration, AWS services, program management
```

**1.2 Match Against Resume Library:**

For each requirement across ALL jobs:
1. Search library for matching experiences (using matching-strategies.md)
2. Score confidence (0-100%)
3. Flag as gap if confidence < 60%

```python
# Pseudo-code
for job in batch.jobs:
    for requirement in job.requirements:
        matches = search_library(requirement)
        best_score = max(match.score for match in matches)
        if best_score < 60:
            flag_as_gap(requirement, best_score, job.job_id)
```

**1.3 Build Aggregate Gap Map:**

Deduplicate gaps across jobs and prioritize:

```python
# Pseudo-code
def build_aggregate_gaps(all_gaps):
    gap_map = {}

    for gap in all_gaps:
        if gap.name not in gap_map:
            gap_map[gap.name] = {
                "appears_in_jobs": [],
                "best_match": gap.confidence,
                "priority": 0
            }
        gap_map[gap.name]["appears_in_jobs"].append(gap.job_id)

    # Prioritize
    for gap_name, gap_data in gap_map.items():
        job_count = len(gap_data["appears_in_jobs"])
        if job_count >= 3:
            gap_data["priority"] = 3  # Critical
        elif job_count == 2:
            gap_data["priority"] = 2  # Important
        else:
            gap_data["priority"] = 1  # Job-specific

    return gap_map
```

**1.4 Create Gap Analysis Report:**

Generate `_aggregate_gaps.md`:

```markdown
# Aggregate Gap Analysis
**Batch:** batch-2025-11-04-job-search
**Generated:** 2025-11-04T11:00:00Z

## Coverage Summary

- Job 1 (Microsoft): 68% coverage, 5 gaps
- Job 2 (Google): 72% coverage, 4 gaps
- Job 3 (AWS): 65% coverage, 6 gaps

## Critical Gaps (appear in 3+ jobs)

### Kubernetes at scale
- **Appears in:** Jobs 1, 2, 3
- **Current best match:** 45% confidence
- **Match source:** "Deployed containerized app for nonprofit" (2023)
- **Gap:** No production Kubernetes management at scale

### CI/CD pipeline management
- **Appears in:** Jobs 1, 2, 3
- **Current best match:** 58% confidence
- **Match source:** "Set up GitHub Actions workflow" (2024)
- **Gap:** Limited enterprise CI/CD experience

## Important Gaps (appear in 2 jobs)

### Cloud-native architecture
- **Appears in:** Jobs 2, 3
- **Current best match:** 52% confidence

### Cross-functional team leadership
- **Appears in:** Jobs 1, 2
- **Current best match:** 67% confidence (not a gap, but could improve)

## Job-Specific Gaps

### Azure-specific experience
- **Appears in:** Job 1 only
- **Current best match:** 40% confidence

### GCP experience
- **Appears in:** Job 2 only
- **Current best match:** 35% confidence

## Aggregate Statistics

- **Total gaps:** 14
- **Unique gaps:** 8 (after deduplication)
- **Critical gaps:** 3
- **Important gaps:** 4
- **Job-specific gaps:** 1

## Recommended Discovery Time

- Critical gaps (3 gaps × 5-7 min): 15-20 minutes
- Important gaps (4 gaps × 3-5 min): 12-20 minutes
- Job-specific gaps (1 gap × 2-3 min): 2-3 minutes

**Total estimated discovery time:** 30-40 minutes

For 3 similar jobs, this replaces 3 × 15 min = 45 min of sequential discovery.
```

**1.5 Update Batch State:**

```json
{
  "current_phase": "gap_analysis",
  "aggregate_gaps": {
    "critical_gaps": [
      {
        "gap_name": "Kubernetes at scale",
        "appears_in_jobs": ["job-1", "job-2", "job-3"],
        "current_best_match": 45,
        "priority": 3
      }
    ],
    "important_gaps": [...],
    "job_specific_gaps": [...]
  }
}
```

**Output to User:**

```
"Gap analysis complete! Here's what I found:

COVERAGE SUMMARY:
- Job 1 (Microsoft): 68% coverage, 5 gaps
- Job 2 (Google): 72% coverage, 4 gaps
- Job 3 (AWS): 65% coverage, 6 gaps

AGGREGATE GAPS (14 total, 8 unique after deduplication):
- 3 critical gaps (appear in all jobs) 🔴
- 4 important gaps (appear in 2 jobs) 🟡
- 1 job-specific gap 🔵

I recommend a 30-40 minute experience discovery session to address
these gaps. This will benefit all 3 applications.

Would you like to:
1. START DISCOVERY - Address gaps through conversational discovery
2. SKIP DISCOVERY - Proceed with current library (not recommended)
3. REVIEW GAPS - See detailed gap analysis first

Recommendation: Option 1 or 3 (review then start)"
```

**Checkpoint:** User chooses next action before proceeding.

## Phase 2: Shared Experience Discovery

**Goal:** Surface undocumented experiences across all gaps through single conversational session

**Core Principle:** Same branching interview from branching-questions.md, but with multi-job context for each question.

**Session Flow:**

**2.1 Start with Highest-Leverage Gaps:**

Process gaps in priority order:
1. Critical gaps (appear in 3+ jobs) - 5-7 min each
2. Important gaps (appear in 2 jobs) - 3-5 min each
3. Job-specific gaps - 2-3 min each

**2.2 Multi-Job Contextualized Questions:**

For each gap, provide multi-job context before branching interview:

**Single-Job Version (from branching-questions.md):**
```
"I noticed the job requires Kubernetes experience. Have you worked with Kubernetes?"
```

**Multi-Job Version (new):**
```
"Kubernetes experience appears in 3 of your target jobs (Microsoft, Google, AWS).

This is a HIGH-LEVERAGE gap - addressing it helps multiple applications.

Current best match: 45% confidence ('Deployed containerized app for nonprofit')

Have you worked with Kubernetes or container orchestration?"
```

**2.3 Conduct Branching Interview:**

For each gap:
1. Initial probe with multi-job context (see above)
2. Branch based on answer using branching-questions.md patterns:
   - YES → Deep dive (scale, challenges, metrics)
   - INDIRECT → Explore role and transferability
   - ADJACENT → Explore related experience
   - PERSONAL → Assess recency and substance
   - NO → Try broader category or move on

3. Follow up systematically:
   - "What," "how," "why" questions
   - Quantify: "Any metrics?"
   - Contextualize: "Was this production?"
   - Validate: "This addresses {gap} for {jobs}"

4. Capture immediately with job tags:

**2.4 Capture Structure:**

As experiences are discovered, capture to `_discovered_experiences.md`:

```markdown
# Discovered Experiences
**Batch:** batch-2025-11-04-job-search
**Discovery Date:** 2025-11-04T11:30:00Z

## Experience 1: Kubernetes CI/CD for nonprofit project

**Context:** Side project, 2023-2024, production deployment

**Scope:**
- GitHub Actions pipeline with Kubernetes deployments
- 3 nonprofit organizations using it
- Integrated pytest for testing
- Managed scaling and monitoring

**Metrics:**
- 3 production deployments
- 99.9% uptime over 12 months
- Reduced deployment time from 2 hours to 15 minutes

**Addresses gaps in:**
- Jobs 1, 2, 3: Kubernetes at scale
- Jobs 1, 2: CI/CD pipeline management

**Confidence Improvement:**
- Kubernetes: 45% → 75% (+30%)
- CI/CD: 58% → 82% (+24%)

**Bullet Draft:**
"Designed and implemented Kubernetes-based CI/CD pipeline using GitHub Actions
and pytest, supporting production deployments for 3 nonprofit organizations with
99.9% uptime and 87% reduction in deployment time"

**Integration Decision:** [Pending user approval]

---

## Experience 2: Azure migration for university lab

**Context:** Graduate research, 2022-2023

**Scope:**
- Migrated on-premise compute to Azure VMs
- Set up Azure DevOps for lab
- Managed costs and resource allocation

**Metrics:**
- Migrated 15 TB of data
- Reduced compute costs by 40%
- Supported 25 researchers

**Addresses gaps in:**
- Job 1 only: Azure-specific experience

**Confidence Improvement:**
- Azure: 40% → 70% (+30%)

**Bullet Draft:**
"Led Azure cloud migration for university research lab, migrating 15 TB of data
and implementing Azure DevOps, reducing compute costs by 40% while supporting
25 researchers"

**Integration Decision:** [Pending user approval]
```

**2.5 Track Coverage Improvement in Real-Time:**

After each discovery, update user:

```
"Great! That addresses Kubernetes for all 3 jobs.

UPDATED COVERAGE:
- Job 1 (Microsoft): 68% → 78% (+10%)
- Job 2 (Google): 72% → 82% (+10%)
- Job 3 (AWS): 65% → 75% (+10%)

Remaining critical gaps: 2 (down from 3)

Continue with next gap? (Y/N)"
```

**2.6 Integration Decision Per Experience:**

After discovery session complete:

```
"Excellent! I captured 5 new experiences addressing gaps across your jobs.

For each experience, how should I integrate it?

---
EXPERIENCE 1: Kubernetes CI/CD for nonprofit project
├─ Addresses: Jobs 1, 2, 3
└─ Options:
   1. ADD TO LIBRARY FOR ALL JOBS - Integrate and use everywhere
   2. ADD TO LIBRARY, USE SELECTIVELY - User picks which jobs
   3. SKIP - Don't integrate

Your choice for Experience 1? (1/2/3)

---
EXPERIENCE 2: Azure migration for university lab
├─ Addresses: Job 1 only
└─ Options:
   1. ADD TO LIBRARY - Integrate for Job 1
   2. SKIP - Not needed

Your choice for Experience 2? (1/2)
```

**2.7 Enrich Library:**

For each approved experience:
1. Add to library database
2. Tag with metadata:
   - discovered_date
   - addressed_gaps
   - used_in_jobs
   - confidence_improvement

**2.8 Update Batch State:**

```json
{
  "current_phase": "discovery",
  "discoveries": [
    {
      "experience_id": "disc-1",
      "text": "Kubernetes CI/CD for nonprofit project",
      "context": "Side project, 2023-2024, production",
      "scope": "GitHub Actions, 3 nonprofits, pytest, monitoring",
      "addresses_jobs": ["job-1", "job-2", "job-3"],
      "addresses_gaps": ["Kubernetes", "CI/CD"],
      "confidence_improvement": {
        "Kubernetes": {"before": 45, "after": 75},
        "CI/CD": {"before": 58, "after": 82}
      },
      "integrated": true,
      "bullet_draft": "Designed and implemented..."
    }
  ]
}
```

**Output:**

```
"Discovery complete!

SUMMARY:
- New experiences captured: 5
- Experiences integrated: 5
- Average coverage improvement: +16%

FINAL COVERAGE:
- Job 1 (Microsoft): 68% → 85% (+17%)
- Job 2 (Google): 72% → 88% (+16%)
- Job 3 (AWS): 65% → 78% (+13%)

Remaining gaps: 5 (down from 14)
├─ 0 critical gaps ✓
├─ 2 important gaps
└─ 3 job-specific gaps

Ready to proceed with per-job processing? (Y/N)"
```

**Checkpoint:** User approves before moving to per-job processing.

## Phase 3: Per-Job Processing

**Goal:** Process each job independently through research/template/matching/generation

**Key Insight:** Once discovery is complete, each job can be processed independently using enriched library.

**Processing Modes:**

Before starting, ask user:

```
"Discovery complete! Now processing each job individually.

PROCESSING MODE:
1. INTERACTIVE (default) - I'll show you checkpoints for each job
   (template approval, content mapping approval)

2. EXPRESS - I'll auto-approve templates and matching using best judgment,
   you review all final resumes together

Recommendation: INTERACTIVE for first 1-2 jobs, then switch to EXPRESS
if you like the pattern.

Which mode for Job 1? (1/2)"
```

**3.1 Per-Job Loop:**

For each job in batch (job.status == "pending"):

1. Set job.status = "in_progress"
2. Set job.current_phase = "research"
3. Create job directory: `resumes/batches/{batch_id}/job-{N}-{company-slug}/`
4. Process through phases (see below)
5. Set job.status = "completed"
6. Set job.files_generated = true
7. Move to next job

**3.2 Phase 3A: Research (Per-Job)**

**Same depth as single-job workflow (SKILL.md Phase 1):**

```
Job {N}/{total}: {Company} - {Role}
├─ Company research via WebSearch (mission, values, culture, news)
├─ Role benchmarking via LinkedIn (find 3-5 similar role holders)
├─ Success profile synthesis
└─ Checkpoint (if INTERACTIVE mode): Present success profile to user
```

Save to: `job-{N}-{company-slug}/success_profile.md`

**INTERACTIVE Mode:**
```
"Job 1: Microsoft - Principal PM

Based on my research, here's what makes candidates successful for this role:

{SUCCESS_PROFILE_SUMMARY}

Key findings:
- {Finding 1}
- {Finding 2}
- {Finding 3}

Does this match your understanding? Any adjustments?

(Y to proceed / provide feedback)"
```

**EXPRESS Mode:**
- Generate success profile
- Save to file
- Proceed automatically (no checkpoint)

**3.3 Phase 3B: Template Generation (Per-Job)**

**Same process as single-job workflow (SKILL.md Phase 2):**

```
├─ Role consolidation decisions
├─ Title reframing options
├─ Bullet allocation
└─ Checkpoint (if INTERACTIVE): Approve template structure
```

Save to: `job-{N}-{company-slug}/template.md`

**INTERACTIVE Mode:**
```
"Here's the optimized resume structure for {Company} - {Role}:

STRUCTURE:
{Section order and rationale}

ROLE CONSOLIDATION:
{Decisions with options}

TITLE REFRAMING:
{Proposed titles with alternatives}

BULLET ALLOCATION:
{Allocation with rationale}

Approve? (Y/N/adjust)"
```

**EXPRESS Mode:**
- Generate template using best judgment
- Save to file
- Proceed automatically

**3.4 Phase 3C: Content Matching (Per-Job)**

**Same process as single-job workflow (SKILL.md Phase 3):**

Uses enriched library (includes discovered experiences from Phase 2)

```
├─ Match content to template slots
├─ Confidence scoring (Direct/Transferable/Adjacent)
├─ Reframing suggestions
├─ Gap identification (should be minimal after discovery)
└─ Checkpoint (if INTERACTIVE): Approve content mapping
```

Save to: `job-{N}-{company-slug}/content_mapping.md`

**INTERACTIVE Mode:**
```
"Content matched for {Company} - {Role}:

COVERAGE SUMMARY:
- Direct matches: {N} bullets ({%}%)
- Transferable: {N} bullets ({%}%)
- Adjacent: {N} bullets ({%}%)
- Gaps: {N} ({%}%)

OVERALL JD COVERAGE: {%}%

[Show detailed mapping]

Approve? (Y/N/adjust)"
```

**EXPRESS Mode:**
- Generate mapping automatically
- Use highest confidence matches
- Save to file
- Proceed automatically

**3.5 Phase 3D: Generation (Per-Job)**

**Same process as single-job workflow (SKILL.md Phase 4):**

```
├─ Generate Markdown resume
├─ Generate DOCX resume (using document-skills:docx)
├─ Generate Report
└─ No checkpoint - just generate files
```

Output files:
- `{Name}_{Company}_{Role}_Resume.md`
- `{Name}_{Company}_{Role}_Resume.docx`
- `{Name}_{Company}_{Role}_Resume_Report.md`

All saved to: `job-{N}-{company-slug}/`

**3.6 Progress Tracking:**

After each job completes:

```
"✓ Job {N}/{total} complete: {Company} - {Role}

QUALITY METRICS:
- JD Coverage: {%}%
- Direct Matches: {%}%
- Files: ✓ MD ✓ DOCX ✓ Report

Jobs remaining: {total - N}
Estimated time: ~{N * 8} minutes

Continue to Job {N+1}? (Y/N/pause)"
```

**3.7 Pause/Resume Support:**

If user says "pause":
```
"Progress saved!

CURRENT STATE:
- Jobs completed: {N}
- Jobs remaining: {total - N}
- Next: Job {N+1} - {Company} - {Role}

To resume later, say 'resume batch {batch_id}' or 'continue my batch'."
```

Save batch state with current progress.

## Phase 4: Batch Finalization

**Goal:** Present all resumes for review, handle batch-level actions, update library

**4.1 Generate Batch Summary:**

Create `_batch_summary.md`:

```markdown
# Batch Summary
**Batch ID:** batch-2025-11-04-job-search
**Created:** 2025-11-04T10:30:00Z
**Completed:** 2025-11-04T14:15:00Z
**Total Time:** 3 hours 45 minutes

## Job Summaries

### Job 1: Principal PM - Microsoft 1ES
- **Status:** Completed ✓
- **Coverage:** 85%
- **Direct Matches:** 78%
- **Key Strengths:** Azure infrastructure, cross-functional leadership, CI/CD
- **Remaining Gaps:** None critical
- **Files:**
  - Varun_Ramesh_Microsoft_1ES_Principal_PM_Resume.md
  - Varun_Ramesh_Microsoft_1ES_Principal_PM_Resume.docx
  - Varun_Ramesh_Microsoft_1ES_Principal_PM_Resume_Report.md

### Job 2: Senior TPM - Google Cloud Infrastructure
- **Status:** Completed ✓
- **Coverage:** 88%
- **Direct Matches:** 72%
- **Key Strengths:** Kubernetes experience, distributed systems, technical depth
- **Remaining Gaps:** GCP-specific (low priority, addressed in summary)
- **Files:**
  - Varun_Ramesh_Google_Cloud_Senior_TPM_Resume.md
  - Varun_Ramesh_Google_Cloud_Senior_TPM_Resume.docx
  - Varun_Ramesh_Google_Cloud_Senior_TPM_Resume_Report.md

### Job 3: Senior PM - AWS Container Services
- **Status:** Completed ✓
- **Coverage:** 78%
- **Direct Matches:** 68%
- **Key Strengths:** Container orchestration, program management, technical leadership
- **Remaining Gaps:** AWS-specific (noted in cover letter recommendations)
- **Files:**
  - Varun_Ramesh_AWS_Container_Senior_PM_Resume.md
  - Varun_Ramesh_AWS_Container_Senior_PM_Resume.docx
  - Varun_Ramesh_AWS_Container_Senior_PM_Resume_Report.md

## Batch Statistics

### Discovery Impact
- **New experiences discovered:** 5
- **Experiences integrated:** 5
- **Average coverage improvement:** +16%
- **Time saved vs sequential:** ~15 minutes (shared discovery)

### Coverage Metrics
- **Average JD coverage:** 84%
- **Average direct matches:** 73%
- **Total files created:** 9 (3 × MD + DOCX + Report)

### Gap Resolution
- **Starting gaps:** 14 unique gaps
- **Gaps resolved through discovery:** 9
- **Remaining gaps:** 5
  - 0 critical (100% critical gap resolution)
  - 2 important (50% important gap resolution)
  - 3 job-specific (handled in cover letters)

## Files Location

```
resumes/batches/batch-2025-11-04-job-search/
├── _batch_state.json
├── _aggregate_gaps.md
├── _discovered_experiences.md
├── _batch_summary.md (this file)
├── job-1-microsoft/
│   ├── success_profile.md
│   ├── template.md
│   ├── content_mapping.md
│   ├── Varun_Ramesh_Microsoft_1ES_Principal_PM_Resume.md
│   ├── Varun_Ramesh_Microsoft_1ES_Principal_PM_Resume.docx
│   └── Varun_Ramesh_Microsoft_1ES_Principal_PM_Resume_Report.md
├── job-2-google/
│   └── (same structure, 6 files)
└── job-3-aws/
    └── (same structure, 6 files)
```

## Recommendations

### Interview Prep
- Prepare Kubernetes stories (appears in all 3 jobs)
- Emphasize cross-functional leadership
- Practice articulating CI/CD experience with metrics

### Cover Letter Focus
- Job 1 (Microsoft): Emphasize internal Azure knowledge, 1ES mission alignment
- Job 2 (Google): Address GCP learning plan, highlight distributed systems thinking
- Job 3 (AWS): Address AWS learning plan, emphasize container orchestration transferability

### Application Priority
Based on coverage scores and fit:
1. **Job 2 (Google):** Highest coverage (88%), strong technical fit
2. **Job 1 (Microsoft):** Strong coverage (85%), internal opportunity
3. **Job 3 (AWS):** Good coverage (78%), but more gaps to address in materials
```

**4.2 Present to User:**

```
"All 3 resumes generated! 🎉

JOB SUMMARIES:
┌─────────────────────────────────────────────────────────────┐
│ Job 1: Principal PM - Microsoft 1ES                         │
│ Coverage: 85% | Direct: 78% | Files: ✓ MD ✓ DOCX ✓ Report │
│ Key strengths: Azure infra, cross-functional leadership     │
│ Remaining gaps: None critical                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Job 2: Senior TPM - Google Cloud Infrastructure            │
│ Coverage: 88% | Direct: 72% | Files: ✓ MD ✓ DOCX ✓ Report │
│ Key strengths: Kubernetes, distributed systems             │
│ Remaining gaps: GCP-specific (low priority)                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Job 3: Senior PM - AWS Container Services                  │
│ Coverage: 78% | Direct: 68% | Files: ✓ MD ✓ DOCX ✓ Report │
│ Key strengths: Container orchestration, program mgmt        │
│ Remaining gaps: AWS-specific (cover letter)                │
└─────────────────────────────────────────────────────────────┘

BATCH STATISTICS:
- New experiences discovered: 5
- Average coverage improvement: +16%
- Total files: 9 (3 jobs × MD + DOCX + Report)
- Time saved vs sequential: ~15 minutes

FILES: resumes/batches/batch-2025-11-04-job-search/

REVIEW OPTIONS:
1. APPROVE ALL - Save all resumes to library
2. REVIEW INDIVIDUALLY - Approve/revise each resume separately
3. REVISE BATCH - Make changes across multiple resumes
4. SAVE BUT DON'T UPDATE LIBRARY - Keep files, don't enrich library

Which option? (1/2/3/4)"
```

**4.3 Handle Review Option 1 (APPROVE ALL):**

```
User chooses: 1

Process:
1. Copy all resume files to library directory
2. Add all discovered experiences to library database
3. Tag with metadata (batch_id, target_company, target_role, etc.)
4. Rebuild library indices
5. Update batch state to "completed"

Output:
"✓ All resumes saved to library!

LIBRARY UPDATED:
- New resumes: 3
- New experiences: 5
- Total resumes in library: 32

These experiences are now available for future applications.

Good luck with your applications! 🚀"
```

**4.4 Handle Review Option 2 (REVIEW INDIVIDUALLY):**

```
User chooses: 2

For each job:
  Show JD requirements vs resume coverage
  Highlight newly discovered experiences used
  Ask: "Approve Job {N}? (Y/N/revise)"

  If Y: Add to library
  If N: Don't add to library
  If revise: Collect feedback, make changes, re-ask

After all reviewed:
"Review complete!

LIBRARY UPDATED:
- Approved resumes: {N}
- Skipped resumes: {M}
- Revised resumes: {K}

Total resumes in library: {count}"
```

**4.5 Handle Review Option 3 (REVISE BATCH):**

```
User chooses: 3

Prompt:
"What would you like to change across the batch?

COMMON BATCH REVISIONS:
- 'Make all summaries shorter'
- 'Emphasize leadership more in all resumes'
- 'Remove mentions of X technology from all'
- 'Use title \"Senior Technical Program Manager\" consistently'
- 'Add bullets about Y experience to all resumes'

Your revision request:"

Process:
1. Collect revision request
2. Determine which jobs affected
3. Re-run matching/generation for affected jobs
4. Present revised resumes
5. Ask for approval again

Loop until user approves or cancels.
```

**4.6 Handle Review Option 4 (SAVE BUT DON'T UPDATE LIBRARY):**

```
User chooses: 4

Output:
"✓ Files saved to: resumes/batches/batch-2025-11-04-job-search/

Not added to library. You can manually move them later if desired.

Batch state preserved for future reference."
```

**4.7 Update Final Batch State:**

```json
{
  "batch_id": "batch-2025-11-04-job-search",
  "current_phase": "completed",
  "completed_at": "2025-11-04T14:15:00Z",
  "jobs": [
    {
      "job_id": "job-1",
      "status": "completed",
      "files_generated": true,
      "added_to_library": true
    }
  ],
  "statistics": {
    "total_jobs": 3,
    "completed_jobs": 3,
    "new_experiences": 5,
    "average_coverage": 84,
    "total_time_minutes": 225
  }
}
```

## Incremental Batch Support

**Goal:** Add new jobs to existing batches without re-doing completed work

**Scenario:** User processes 3 jobs today, finds 2 more jobs next week

**8.1 Detect Add Request:**

User says:
- "Add another job to my batch"
- "I found 2 more jobs"
- "Resume batch {batch_id} and add jobs"

**8.2 Load Existing Batch:**

```python
# Pseudo-code
batch = load_batch_state(batch_id)

if batch.current_phase == "completed":
    print("Batch already completed. Creating extension...")
    batch.current_phase = "intake"  # Reopen for new jobs
```

**8.3 Intake New Jobs:**

Same process as Phase 0, but:
- Append to existing batch.jobs list
- Assign new job_ids (continue numbering: job-4, job-5, etc.)

```
"Adding jobs to existing batch: {batch_id}

CURRENT BATCH:
- Job 1: Microsoft - Principal PM (completed ✓)
- Job 2: Google - Senior TPM (completed ✓)
- Job 3: AWS - Senior PM (completed ✓)

NEW JOBS TO ADD:

Provide job description for Job 4: [user input]
[... collect JD, company, role, priority, notes ...]

Add another job? (Y/N)
```

**8.4 Incremental Gap Analysis:**

```
"Running incremental gap analysis for new jobs...

NEW JOBS:
- Job 4 (Stripe): Payment Systems Engineer
- Job 5 (Meta): Senior TPM

COVERAGE WITH EXISTING LIBRARY:
(Library now includes 5 experiences discovered in previous session)

- Job 4 (Stripe): 82% coverage
- Job 5 (Meta): 75% coverage

NEW GAPS (not covered by previous discoveries):
- Payment systems experience (Job 4 only) 🔵
- Large-scale social networking (Job 5 only) 🔵
- React/frontend (Jobs 4, 5) 🟡

ALREADY COVERED FROM PREVIOUS BATCH:
✓ Kubernetes (from previous batch)
✓ CI/CD (from previous batch)
✓ Cross-functional leadership (from previous batch)

NEW GAP COUNT: 3 (vs 14 in original batch)
Estimated discovery time: 5-10 minutes (vs 30-40 for original batch)

Ready for incremental discovery? (Y/N)"
```

**8.5 Incremental Discovery:**

Only ask about NEW gaps:

```python
# Pseudo-code
previous_gaps = set(batch.aggregate_gaps.all_gap_names())
new_gaps = []

for job in new_jobs:
    for gap in job.gaps:
        if gap.name not in previous_gaps:
            new_gaps.append(gap)

# Run discovery ONLY for new_gaps
conduct_discovery(new_gaps)
```

**Important:** Don't re-ask questions already answered in previous session.

**8.6 Process New Jobs:**

Run Phase 3 (per-job processing) for new jobs only:
- Job 4: Research → Template → Matching → Generation
- Job 5: Research → Template → Matching → Generation

**8.7 Update Batch Summary:**

Add new jobs to `_batch_summary.md`:

```markdown
## Incremental Addition (2025-11-11)

Added 2 new jobs to batch after initial completion.

### Job 4: Payment Systems Engineer - Stripe
... [same format as original jobs]

### Job 5: Senior TPM - Meta
... [same format as original jobs]

## Updated Statistics
- Total jobs: 5 (original 3 + added 2)
- New experiences discovered (incremental): 3
- Total experiences discovered: 8
```

**8.8 Final Output:**

```
"Incremental batch processing complete!

ORIGINAL BATCH (2025-11-04):
✓ Job 1: Microsoft
✓ Job 2: Google
✓ Job 3: AWS

NEW JOBS (2025-11-11):
✓ Job 4: Stripe
✓ Job 5: Meta

NEW DISCOVERIES: 3
TIME SAVED: ~25 minutes (avoided re-asking 8 previous gaps)

All 5 resumes available in: resumes/batches/{batch_id}/

Add to library? (Y/N)"
```

## Error Handling & Edge Cases

### Edge Case 1: Jobs Are More Diverse Than Expected

**Detection:** During gap analysis, <40% gap overlap between jobs

**Scenario:** User provides 5 jobs, but they're quite different (TPM, Data Scientist, Product Marketing Manager)

**Handling:**

```
"⚠️ I notice these jobs are quite diverse:

JOB SIMILARITY ANALYSIS:
- Jobs 1, 2 (TPM roles): 85% requirement overlap ✓
- Jobs 3, 4 (Data Science): 80% requirement overlap ✓
- Job 5 (Marketing): Only 20% overlap with others ⚠️

RECOMMENDATION:
Split into batches for better efficiency:
- Batch A: Jobs 1, 2 (TPM-focused discovery)
- Batch B: Jobs 3, 4 (Data Science-focused discovery)
- Job 5: Process separately (single-job mode)

OR proceed with unified discovery (will take longer, ~50 minutes)

Your preference:
1. Split into batches (recommended)
2. Continue with unified discovery
3. Remove dissimilar jobs"
```

### Edge Case 2: Discovery Reveals Experience Relevant to Only 1 Job

**Scenario:** During discovery for "multi-job gap," user's answer only addresses one job

**Example:**

```
SKILL: "Kubernetes appears in all 3 jobs. Have you worked with it?"
USER: "Only in Azure (AKS), not GCP or AWS"

HANDLING:
"Got it - this addresses the Microsoft job (Azure AKS) but not Google (GKE)
or AWS (EKS).

I'll tag this as Microsoft-specific.

Should I still explore Kubernetes more broadly? You might have experience
with container orchestration concepts that transfer across cloud providers.

Options:
1. YES - Explore general container orchestration
2. NO - Move to next gap

Your choice? (1/2)"

[If 1, branch to adjacent probe for container orchestration concepts]
```

### Edge Case 3: One Job's Research Fails

**Scenario:** Company is obscure startup, minimal online presence

**Handling:**

```
"⚠️ Limited research data for Job 3 (StartupXYZ):
- No company website or information found
- No LinkedIn profiles for similar roles
- No news or press coverage

FALLBACK: JD-only analysis for this job

OPTIONS:
1. CONTINUE - Proceed with JD-only (recommended)
2. SKIP JOB 3 - Process others, come back later
3. PROVIDE CONTEXT - You share company info manually
4. REMOVE JOB 3 - Remove from batch entirely

Other jobs (1, 2) have sufficient research data.

Your preference? (1/2/3/4)"

[Don't let one failure block the entire batch]
```

### Edge Case 4: User Wants to Add/Remove Jobs Mid-Process

**Add Job Mid-Process:**

```
USER: "I want to add another job to the batch"

SKILL: "Adding Job {N+1} to batch.

CURRENT PHASE: {current_phase}

Since we've already completed discovery:
- If Job {N+1} has NEW gaps: We'll do quick incremental discovery
- If existing discoveries cover it: Proceed directly to processing

Let me collect the job details..."

[Run quick gap check, incremental discovery if needed, then process]
```

**Remove Job Mid-Process:**

```
USER: "Remove Job 2 from the batch"

SKILL: "Removing Job 2 from batch.

ALREADY-DISCOVERED EXPERIENCES:
- Will remain in library
- Still available for other jobs in batch
- Available for future batches

BATCH UPDATED:
- Jobs remaining: {N-1}
- Job 2 files will be moved to archive (not deleted)

Continue with remaining jobs? (Y/N)"
```

### Edge Case 5: Library Update Conflicts

**Scenario:** User approves Job 1 resume, rejects Job 2, wants to revise Job 3

**Handling:**

```
"You've approved some jobs but not others.

LIBRARY UPDATE OPTIONS:

1. INDIVIDUAL APPROVAL (recommended)
   - Add Job 1 to library now ✓
   - Job 2 won't be added ✗
   - Job 3 pending revision (decide after changes)

2. BATCH APPROVAL (wait)
   - Update library only when all jobs finalized
   - Ensures consistency across batch

3. SELECTIVE APPROVAL
   - Choose which jobs to add now
   - Which experiences to integrate

Recommendation: Option 1 (individual approval)

Your preference? (1/2/3)"
```

### Edge Case 6: Batch Processing Interrupted

**Scenario:** User stops mid-batch, connection drops, or session ends

**Auto-Save Behavior:**

After each major milestone, auto-save batch state:
- After each job completes
- After discovery phase
- After gap analysis
- After user checkpoints

**Resume Instructions:**

```
"Your batch processing was interrupted.

SAVED STATE:
- Batch ID: {batch_id}
- Completed: Jobs 1, 2
- In Progress: Job 3 (template approved, matching not started)
- Pending: Jobs 4, 5

To resume:
- Say 'resume batch {batch_id}'
- Or 'continue my batch'
- Or provide batch ID when asked

I'll pick up exactly where we left off."
```

### Edge Case 7: No Gaps Found

**Scenario:** All jobs are well-covered by existing library (rare but possible)

**Handling:**

```
"Gap analysis complete!

COVERAGE SUMMARY:
- Job 1: 92% coverage
- Job 2: 89% coverage
- Job 3: 87% coverage

ALL GAPS ADDRESSABLE WITH EXISTING LIBRARY ✓

No experience discovery needed - your library already covers these roles well.

OPTIONS:
1. SKIP DISCOVERY - Proceed directly to per-job processing (recommended)
2. OPTIONAL DISCOVERY - Surface any additional experiences anyway
3. REVIEW GAPS - See what small gaps exist

Your preference? (1/2/3)"
```

### Error Recovery Principles

1. **Never lose progress:** Auto-save batch state frequently
2. **Partial success is success:** Some jobs completing is better than none
3. **Transparent failures:** Always explain what went wrong and options
4. **Graceful degradation:** Fall back to JD-only, single-job mode, or skip if needed
5. **User control:** Always provide options, never force a path

### Graceful Degradation Paths

```
Research fails → Fall back to JD-only analysis
Library too small → Emphasize discovery phase
WebSearch unavailable → Use cached data or skip research
DOCX generation fails → Provide markdown only
One job fails → Continue with others, revisit failed job later
```
