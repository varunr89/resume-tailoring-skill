# Multi-Job Resume Tailoring - Design Document

**Date:** 2025-11-04
**Purpose:** Extend the resume-tailoring skill to handle multiple job applications efficiently while maintaining research depth and quality

## Overview

The current resume-tailoring skill produces high-quality, deeply researched resumes but processes one job at a time. This creates inefficiency when applying to multiple similar positions - the interactive experience discovery phase repeats similar questions for each job, and discovered experiences can't benefit other applications.

**Solution:** Shared Discovery + Per-Job Tailoring architecture that consolidates the most time-intensive interactive phase (experience discovery) across multiple jobs while maintaining full research depth for each individual application.

**Target Use Case:**
- Small batches (3-5 jobs at a time)
- Moderately similar roles (e.g., TPM, Senior PM, Principal Engineer - adjacent roles with overlapping skills)
- Continuous workflow (add jobs incrementally over days/weeks)
- Preserve depth in: role benchmarking, interactive discovery, content matching

## Architecture: Shared Discovery + Per-Job Tailoring

### High-Level Workflow

```
INTAKE PHASE
├─ User provides 3-5 job descriptions (text or URLs)
├─ Library initialization (existing Phase 0)
└─ Quick JD parsing for each job → extract requirements

AGGREGATE GAP ANALYSIS
├─ For each JD: identify required skills/experiences
├─ Cross-reference ALL requirements against library
├─ Build unified gap list across all jobs
└─ Deduplicate overlapping gaps (e.g., "Kubernetes" appears in 3 JDs)

SHARED EXPERIENCE DISCOVERY (Interactive)
├─ Present aggregate gaps to user
├─ Single branching interview session covering all gaps
├─ Captured experiences tagged with which jobs they address
└─ Enrich library with all discovered content

PER-JOB PROCESSING (Sequential with optional express mode)
├─ For each job independently:
│   ├─ Phase 1: Research (role benchmarking, company culture)
│   ├─ Phase 2: Template generation
│   ├─ Phase 3: Content matching (uses enriched library)
│   └─ Phase 4: Generation (MD + DOCX + Report)
└─ User reviews checkpoints (interactive) or auto-approves (express)

BATCH FINALIZATION
├─ User reviews all N resumes together
├─ Approve/revise individual resumes
└─ Optional: Update library with approved resumes
```

### Key Architectural Decision

**Why consolidate discovery but not research?**

The time profile of single-job workflow:
- Library Init: 1 min (one-time)
- Research: 3 min (per-job, varies by company)
- Template: 2 min (per-job, quick)
- **Discovery: 5-7 min (per-job, highly interactive)**
- Matching: 2 min (per-job, automated)
- Generation: 1 min (per-job, automated)

For 3 jobs with 60% overlapping requirements:
- **Sequential single-job:** 3 × 7 min = 21 minutes of discovery, asking similar questions repeatedly
- **Shared discovery:** 1 × 15 min = 15 minutes covering all gaps once

Discovery is:
1. Most time-intensive interactive phase
2. Most repetitive across similar jobs (same gaps appear multiple times)
3. Most beneficial when shared (one discovered experience helps multiple applications)

Research is:
1. Company-specific (not redundant across jobs)
2. Critical for quality differentiation (LinkedIn role benchmarking creates competitive advantage)
3. Fast enough that consolidation isn't worth complexity

**Result:** Consolidate discovery (high leverage), maintain per-job research (high value).

## Detailed Phase Specifications

### Phase 0: Intake & Job Management

**User Interaction:**

```
USER: "I want to apply for multiple jobs. Here are the JDs..."

SKILL: "I see you have multiple jobs. Let me set up multi-job mode.

How would you like to provide the job descriptions?
- Paste them all now (recommended for batch efficiency)
- Provide them one at a time

For each job, I need:
1. Job description (text or URL)
2. Company name (if not in JD)
3. Role title (if not in JD)
4. Optional: Priority/notes for this job"
```

**Data Structure:**

```json
{
  "batch_id": "batch-2025-11-04-job-search",
  "created": "2025-11-04T10:30:00Z",
  "jobs": [
    {
      "job_id": "job-1",
      "company": "Microsoft",
      "role": "Principal PM - 1ES",
      "jd_text": "...",
      "jd_url": "https://...",
      "priority": "high",
      "notes": "Internal referral from Alice",
      "status": "pending"
    },
    {
      "job_id": "job-2",
      "company": "Google",
      "role": "Senior TPM - Cloud Infrastructure",
      "jd_text": "...",
      "status": "pending"
    }
  ]
}
```

**Quick JD Parsing:**

For each job, lightweight extraction (NOT full research):
- Must-have requirements
- Nice-to-have requirements
- Key technical skills
- Soft skills
- Domain knowledge areas

Purpose: Just enough to identify gaps for discovery phase.

### Phase 1: Aggregate Gap Analysis

**Goal:** Build unified gap list across all jobs to guide one efficient discovery session.

**Process:**

1. **Extract requirements from all JDs:**
   ```
   Job 1 (Microsoft 1ES): Kubernetes, CI/CD, cross-functional leadership, Azure
   Job 2 (Google Cloud): Kubernetes, GCP, distributed systems, team management
   Job 3 (AWS): Container orchestration, AWS services, program management
   ```

2. **Match against current library:**
   - For each requirement across all jobs
   - Check library for matching experiences
   - Score confidence (using existing matching logic)
   - Flag as gap if confidence < 60%

3. **Build aggregate gap map:**

```markdown
## Aggregate Gap Analysis

### Critical Gaps (appear in 3+ jobs):
- **Kubernetes at scale**: Jobs 1, 2, 3 (current best match: 45%)

### Important Gaps (appear in 2 jobs):
- **CI/CD pipeline management**: Jobs 1, 2 (current best match: 58%)
- **Cloud-native architecture**: Jobs 2, 3 (current best match: 52%)

### Job-Specific Gaps:
- **Azure-specific experience**: Job 1 only (current best match: 40%)
- **GCP experience**: Job 2 only (current best match: 35%)
```

4. **Prioritize for discovery:**
   - Gaps appearing in multiple jobs first (highest leverage)
   - High-priority jobs get their specific gaps addressed
   - Critical gaps (confidence <45%) before weak gaps (45-60%)

**Output to User:**

```
"I've analyzed all 3 job descriptions against your resume library.

COVERAGE SUMMARY:
- Job 1 (Microsoft): 68% coverage, 5 gaps
- Job 2 (Google): 72% coverage, 4 gaps
- Job 3 (AWS): 65% coverage, 6 gaps

AGGREGATE GAPS (14 total, 8 unique after deduplication):
- 3 critical gaps (appear in all jobs)
- 4 important gaps (appear in 2 jobs)
- 1 job-specific gap

I recommend a 15-20 minute experience discovery session to address these gaps.
This will benefit all 3 applications. Ready to start?"
```

### Phase 2: Shared Experience Discovery

**Core Principle:** Same branching interview process from `branching-questions.md`, but with multi-job context.

**Single-Job Version:**
```
"I noticed the job requires Kubernetes experience. Have you worked with Kubernetes?"
```

**Multi-Job Version:**
```
"Kubernetes experience appears in 3 of your target jobs (Microsoft, Google, AWS).
This is a high-leverage gap - addressing it helps multiple applications.

Have you worked with Kubernetes or container orchestration?"
```

**Discovery Session Flow:**

1. **Start with highest-leverage gaps** (appear in most jobs)

2. **For each gap, conduct branching interview:**
   - Initial probe (contextualized with job relevance)
   - Branch based on answer (YES/INDIRECT/ADJACENT/PERSONAL/NO)
   - Drill into specifics (scale, metrics, challenges)
   - Capture immediately with job tags

3. **Tag discovered experiences with job relevance:**

```markdown
## Newly Discovered Experiences

### Experience 1: Kubernetes CI/CD for nonprofit project
- Context: Side project, 2023-2024, production deployment
- Scope: GitHub Actions pipeline, 3 nonprofits using it, pytest integration
- **Addresses gaps in:** Jobs 1, 2, 3 (Kubernetes), Jobs 1, 2 (CI/CD)
- Bullet draft: "Designed and implemented Kubernetes-based CI/CD pipeline
  using GitHub Actions and pytest, supporting production deployments for
  3 nonprofit organizations"
- Confidence improvement:
  - Kubernetes: 45% → 75%
  - CI/CD: 58% → 82%
```

4. **Track coverage improvement in real-time:**

```
After discovering 3 experiences:

UPDATED COVERAGE:
- Job 1 (Microsoft): 68% → 85% (+17%)
- Job 2 (Google): 72% → 88% (+16%)
- Job 3 (AWS): 65% → 78% (+13%)

Remaining gaps: 5 (down from 14)
```

5. **Time-box intelligently:**
   - Critical gaps (3+ jobs): 5-7 minutes each
   - Important gaps (2 jobs): 3-5 minutes each
   - Job-specific gaps: 2-3 minutes each
   - Total: ~15-20 minutes for typical 3-job batch

**Integration Decision Per Experience:**

```
"Great! I captured 5 new experiences addressing gaps across your jobs.

For each experience, how should I integrate it?

Experience 1 (Kubernetes CI/CD):
└─ Addresses gaps in: Jobs 1, 2, 3
   Options: [Add to library for all jobs] [Add to library, use selectively] [Skip]

Experience 2 (Azure migration project):
└─ Addresses gap in: Job 1 only
   Options: [Add to library] [Skip]
```

**Result:** Enriched library ready for per-job processing.

### Phase 3: Per-Job Processing

**Key Insight:** Once discovery is complete, each job can be processed independently.

**For Each Job:**

**3.1 Research** (same depth as current single-job workflow)
- Company research via WebSearch (mission, values, culture, news)
- Role benchmarking via LinkedIn (find 3-5 similar role holders)
- Success profile synthesis
- **Checkpoint:** Present success profile to user

**3.2 Template Generation**
- Role consolidation decisions
- Title reframing options
- Bullet allocation
- **Checkpoint:** Approve template structure

**3.3 Content Matching**
- Match content using enriched library (includes discovered experiences)
- Confidence scoring (Direct/Transferable/Adjacent)
- Reframing suggestions
- Gap identification (should be minimal after discovery)
- **Checkpoint:** Approve content mapping

**3.4 Generation**
- Generate MD + DOCX + Report
- No checkpoint - just generate files

**Processing Modes:**

```
"Discovery complete! Now processing each job individually.

Processing mode:
1. INTERACTIVE (default): I'll show you checkpoints for each job
2. EXPRESS: Auto-approve templates/matching using best judgement,
   you review all final resumes together

Recommended: INTERACTIVE for first 1-2 jobs, then EXPRESS if you
like the pattern."
```

**Why Sequential Not Parallel:**
- User needs to review checkpoints (interactive mode)
- Express mode could theoretically parallelize, but adds complexity
- Sequential provides clear progress tracking
- 3 jobs × 8 min/job = 24 minutes is acceptable

### Phase 4: Batch Finalization

**Output to User:**

```
"All 3 resumes generated! Here's your batch summary:

JOB SUMMARIES:
┌─────────────────────────────────────────────────────────────┐
│ Job 1: Principal PM - Microsoft 1ES                         │
│ Coverage: 85% | Direct matches: 78% | Files: ✓ MD ✓ DOCX   │
│ Key strengths: Azure infra, cross-functional leadership     │
│ Remaining gaps: None critical                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Job 2: Senior TPM - Google Cloud Infrastructure            │
│ Coverage: 88% | Direct matches: 72% | Files: ✓ MD ✓ DOCX   │
│ Key strengths: K8s experience, distributed systems          │
│ Remaining gaps: GCP-specific (low priority)                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Job 3: Senior PM - AWS Container Services                  │
│ Coverage: 78% | Direct matches: 68% | Files: ✓ MD ✓ DOCX   │
│ Key strengths: Container orchestration, program mgmt        │
│ Remaining gaps: AWS-specific (addressed in cover letter)   │
└─────────────────────────────────────────────────────────────┘

BATCH STATISTICS:
- Total discovered experiences: 5
- Average coverage improvement: +16%
- Total files created: 9 (3 × MD + DOCX + Report)

FILES LOCATION:
resumes/batches/batch-2025-11-04-job-search/
├── job-1-microsoft/
│   ├── Varun_Ramesh_Microsoft_1ES_Principal_PM_Resume.md
│   ├── Varun_Ramesh_Microsoft_1ES_Principal_PM_Resume.docx
│   └── Varun_Ramesh_Microsoft_1ES_Principal_PM_Resume_Report.md
├── job-2-google/
│   └── ... (3 files)
├── job-3-aws/
│   └── ... (3 files)
├── _batch_summary.md
├── _aggregate_gaps.md
└── _discovered_experiences.md

Review options:
1. APPROVE ALL - Save all resumes to library
2. REVIEW INDIVIDUALLY - Approve/revise each resume separately
3. REVISE BATCH - Make changes across multiple resumes
4. SAVE BUT DON'T UPDATE LIBRARY - Keep files, don't enrich library
```

**Individual Review Flow** (Option 2):
- For each resume: show JD requirements vs. resume coverage
- Highlight newly discovered experiences used
- Allow revisions
- Approve/reject for library individually

**Batch Revision Flow** (Option 3):
```
"What would you like to change across the batch?"

Common batch revisions:
- "Make all summaries shorter"
- "Emphasize leadership more in all resumes"
- "Remove mentions of X technology from all"
- "Use title 'Senior Technical Program Manager' consistently"

System reruns matching/generation for affected resumes.
```

**Library Update:**
```
If approved:
- Add all N resumes to library
- Add discovered experiences to database (tagged with: discovered_date,
  addressed_gaps, used_in_jobs)
- Rebuild library indices

Result:
"Library updated!
- New resumes: 3
- New experiences: 5
- Your library now has 32 resumes total

These experiences are now available for future applications."
```

## Continuous Workflow Support

### Adding Jobs to Existing Batch

**Scenario:** User processes 3 jobs today, finds 2 more jobs next week.

```
USER: "I found 2 more jobs I want to apply for. Can you add them to my batch?"

SKILL: "Sure! I'll add them to your existing batch.

Current batch: 3 jobs (completed)
New jobs: 2

I'll do an incremental gap analysis:
- Check new JDs against your enriched library (includes the 5 experiences
  we discovered last week)
- Identify only NEW gaps not covered by existing discoveries
- Run discovery session ONLY for new gaps (not re-asking old questions)

This should be much faster than the first session."
```

### Incremental Gap Analysis

```
NEW GAP ANALYSIS:
- Job 4 (Stripe): 82% coverage with existing library
- Job 5 (Meta): 75% coverage with existing library

NEW GAPS (3 total):
- Payment systems experience (Job 4 only)
- Large-scale social networking (Job 5 only)
- React/frontend (Jobs 4, 5)

Previous discoveries already cover:
- Kubernetes ✓ (from first batch)
- CI/CD ✓ (from first batch)
- Cross-functional leadership ✓ (from first batch)

Estimated discovery time: 5-10 minutes (vs 20 minutes for first batch)

Ready for incremental discovery?
```

**Smart Reuse:** System remembers what's been asked, doesn't repeat questions, only explores genuinely new gaps.

## Data Persistence

### File Structure

```
resumes/batches/
└── batch-2025-11-04-job-search/
    ├── _batch_state.json          # Workflow state
    ├── _aggregate_gaps.md         # Gap analysis results
    ├── _discovered_experiences.md # Discovery session output
    ├── _batch_summary.md          # Final summary
    ├── job-1-microsoft/
    │   ├── success_profile.md
    │   ├── template.md
    │   ├── content_mapping.md
    │   ├── Varun_Ramesh_Microsoft_1ES_Resume.md
    │   ├── Varun_Ramesh_Microsoft_1ES_Resume.docx
    │   └── Varun_Ramesh_Microsoft_1ES_Resume_Report.md
    ├── job-2-google/
    │   └── ... (same structure)
    └── job-3-aws/
        └── ... (same structure)
```

### State Tracking

**`_batch_state.json`:**

```json
{
  "batch_id": "batch-2025-11-04-job-search",
  "created": "2025-11-04T10:30:00Z",
  "current_phase": "per_job_processing",
  "jobs": [
    {
      "job_id": "job-1",
      "company": "Microsoft",
      "role": "Principal PM - 1ES",
      "status": "completed",
      "coverage": 85,
      "files_generated": true
    },
    {
      "job_id": "job-2",
      "company": "Google",
      "status": "in_progress",
      "current_phase": "template_generation"
    },
    {
      "job_id": "job-3",
      "status": "pending"
    }
  ],
  "discoveries": [
    {
      "experience_id": "disc-1",
      "text": "Designed and implemented Kubernetes-based CI/CD pipeline...",
      "addresses_jobs": ["job-1", "job-2", "job-3"],
      "addresses_gaps": ["Kubernetes", "CI/CD"],
      "confidence_improvement": {
        "Kubernetes": {"before": 45, "after": 75},
        "CI/CD": {"before": 58, "after": 82}
      },
      "integrated": true
    }
  ]
}
```

### Resume Capability

```
USER: "I need to stop. Can I continue later?"

SKILL: "Absolutely! I've saved all progress.

Current state:
- Library: Initialized ✓
- Gap analysis: Complete ✓
- Discovery: Complete (5 experiences) ✓
- Job 1: Complete ✓
- Job 2: In progress (template approved, matching pending)
- Job 3: Pending

When you return, just say 'resume my batch' and I'll pick up
from Job 2 content matching."
```

## Error Handling & Edge Cases

### Edge Case 1: Jobs Are More Diverse Than Expected

```
SCENARIO: User provides 5 jobs, but they're quite different
(TPM, Data Scientist, Product Marketing Manager)

DETECTION: During gap analysis, <40% gap overlap between jobs

HANDLING:
"⚠️ I notice these jobs are quite diverse:
- Jobs 1, 2 (TPM roles): 85% requirement overlap
- Jobs 3, 4 (Data Science): 80% requirement overlap
- Job 5 (Marketing): Only 20% overlap with others

RECOMMENDATION:
Split into 2 batches for better efficiency:
- Batch A: Jobs 1, 2 (TPM-focused discovery)
- Batch B: Jobs 3, 4 (Data Science-focused discovery)
- Job 5: Process separately

OR proceed with unified discovery (will take longer, ~30 minutes)

Your preference?"
```

### Edge Case 2: Discovery Reveals Experience Relevant to Only 1 Job

```
SCENARIO: During discovery for "multi-job gap," user's answer only
addresses one job

EXAMPLE:
SKILL: "Kubernetes appears in all 3 jobs. Have you worked with it?"
USER: "Only in Azure (AKS), not GCP or AWS"

HANDLING:
"Got it - this addresses the Microsoft job (AKS) but not Google (GKE)
or AWS (EKS). I'll tag this as Microsoft-specific.

Should I still explore Kubernetes more broadly? You might have
experience with container orchestration concepts that transfer."

[Branch to adjacent probe for GKE/EKS]
```

### Edge Case 3: One Job's Research Fails

```
SCENARIO: Company is obscure startup, minimal online presence

HANDLING:
"⚠️ Limited research for Job 3 (StartupXYZ):
- No company info found
- No LinkedIn profiles for similar roles

Falling back to JD-only analysis for this job.

Options:
1. Continue with JD-only (recommended)
2. Skip Job 3 for now, process others
3. You provide company context manually

Other jobs (1, 2) have sufficient research data."

[Don't let one failure block the batch]
```

### Edge Case 4: User Wants to Add/Remove Jobs Mid-Process

**Add Job:**
```
"I'll add Job 4 to the batch. Since discovery is already complete:
- If Job 4 has new gaps: We'll do incremental discovery
- If existing discoveries cover it: Proceed directly to processing"
```

**Remove Job:**
```
"Removing Job 2 from batch. Already-discovered experiences are still
in the library and available for remaining jobs."
```

### Edge Case 5: Library Update Conflicts

```
SCENARIO: User approves Job 1 resume, rejects Job 2, wants to revise Job 3

HANDLING:
"Library update options:

INDIVIDUAL APPROVAL (recommended):
- Add Job 1 to library now ✓
- Job 2 won't be added ✗
- Job 3 pending revision (decide after changes)

BATCH APPROVAL (wait):
- Update library only when all jobs finalized
- Ensures consistency

Your preference?"
```

## Success Criteria

The multi-job extension is successful if:

1. **Efficiency Gain:** Processing N jobs takes < (N × single-job time)
   - **Target:** 3 jobs in ~40 minutes vs 3 × 15 min = 45 min sequential
   - **Primary saving:** Shared discovery (20 min vs 60 min for 3× sequential)
   - **Scale:** 5 jobs in ~55 min vs 75 min sequential (~25% time savings)

2. **Quality Maintained:** Each resume has same quality as single-job workflow
   - ≥70% JD coverage per job
   - Full depth research per job (role benchmarking, company culture)
   - Transparent gap identification and confidence scoring

3. **User Experience:** Clear and manageable
   - Batch status visible at all times
   - Can pause/resume between sessions
   - Can add jobs incrementally
   - Individual job control (approve/revise independently)

4. **Library Enrichment:** Discoveries benefit all jobs
   - Experiences tagged with multi-job relevance
   - Reusable for future batches
   - Clear provenance (which batch, which gaps addressed)

5. **Continuous Workflow Support:**
   - Can process initial batch, add more jobs later
   - Incremental discovery only asks new questions
   - State persists between sessions

## Time Comparison: Single-Job vs Multi-Job

### Single-Job Workflow (Current)

```
1 job → ~15 minutes

Library Init (1 min)
Research (3 min)
Template (2 min)
Discovery (5-7 min)
Matching (2 min)
Generation (1 min)
Review (1 min)

3 jobs sequentially: 45 minutes
- Discovery happens 3 times
- Overlapping questions asked repeatedly
- Each job processed in isolation
```

### Multi-Job Workflow (Proposed)

```
3 jobs → ~40 minutes

Library Init (1 min)
Aggregate Gap Analysis (2 min)
Shared Discovery (15-20 min)     ← Once for all jobs

Per-Job (×3):
 ├─ Research (3 min each)
 ├─ Template (2 min each)
 ├─ Matching (2 min each)
 └─ Generation (1 min each)

Batch Review (3 min)

Time saved: ~25-30% for 3 jobs
- Shared discovery eliminates redundancy
- Batch review more efficient than sequential
- Scales better: 5 jobs ~55 min (vs 75 min sequential)
```

## Implementation Notes

### Changes to Existing Skill Structure

**Current Structure:**
```
~/.claude/skills/resume-tailoring/
├── SKILL.md
├── research-prompts.md
├── matching-strategies.md
└── branching-questions.md
```

**Proposed Additions:**
```
~/.claude/skills/resume-tailoring/
├── SKILL.md                      # Modified: Add multi-job mode detection
├── research-prompts.md           # Unchanged
├── matching-strategies.md        # Unchanged
├── branching-questions.md        # Modified: Add multi-job context
└── multi-job-workflow.md         # NEW: Multi-job orchestration logic
```

### Backward Compatibility

**Single-job invocations still work:**
```
USER: "Create a resume for Microsoft 1ES Principal PM role"

SKILL: Detects single job → Uses existing single-job workflow
```

**Multi-job detection:**
```
Triggers when user provides:
- Multiple JD URLs
- Phrase like "multiple jobs" or "several positions"
- List of companies/roles

Asks for confirmation: "I see multiple jobs. Use multi-job mode? (Y/N)"
```

### Migration Strategy

**Phase 1:** Implement multi-job workflow as separate mode (preserves existing single-job)

**Phase 2:** Test with real job search batches

**Phase 3:** Optimize based on usage patterns (potentially make multi-job the default)

## Future Enhancements

**Potential improvements beyond initial implementation:**

1. **Smart Batching:** Automatically cluster jobs by similarity
2. **Cross-Resume Optimization:** Suggest which resume to submit based on coverage scores
3. **Application Tracking:** Track which resumes sent, responses received
4. **A/B Testing:** Compare success rates of different approaches
5. **Cover Letter Generation:** Extend multi-job approach to cover letters
6. **Interview Prep:** Generate interview prep guides based on gaps and strengths

## References

**Related Documents:**
- `2025-10-31-resume-tailoring-skill-design.md` - Original single-job design
- `2025-10-31-resume-tailoring-skill-implementation.md` - Implementation plan

**Design Process:**
- Developed using superpowers:brainstorming skill
- Validated constraints: 3-5 jobs, moderately similar, continuous workflow
- Evaluated 3 approaches, selected Shared Discovery + Per-Job Tailoring
