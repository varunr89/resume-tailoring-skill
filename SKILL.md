---
name: resume-tailoring
description: Use when creating tailored resumes for job applications - researches company/role, creates optimized templates, conducts branching experience discovery to surface undocumented skills, and generates professional multi-format resumes from user's resume library while maintaining factual integrity
---

# Resume Tailoring Skill

## Overview

Generates high-quality, tailored resumes optimized for specific job descriptions while maintaining factual integrity. Builds resumes around the holistic person by surfacing undocumented experiences through conversational discovery.

**Core Principle:** Truth-preserving optimization - maximize fit while maintaining factual integrity. Never fabricate experience, but intelligently reframe and emphasize relevant aspects.

**Mission:** A person's ability to get a job should be based on their experiences and capabilities, not on their resume writing skills.

## When to Use

Use this skill when:
- User provides a job description and wants a tailored resume
- User has multiple existing resumes in markdown format
- User wants to optimize their application for a specific role/company
- User needs help surfacing and articulating undocumented experiences

**DO NOT use for:**
- Generic resume writing from scratch (user needs existing resume library)
- Cover letters (different skill)
- LinkedIn profile optimization (different skill)

## Quick Start

**Required from user:**
1. Job description (text or URL)
2. Resume library location (defaults to `resumes/` in current directory)

**Workflow:**
1. Build library from existing resumes
2. Research company/role
3. Create template (with user checkpoint)
4. Optional: Branching experience discovery
5. Match content with confidence scoring
6. Generate MD + DOCX + PDF + Report
7. User review → Optional library update

## Implementation

See supporting files:
- `research-prompts.md` - Structured prompts for company/role research
- `matching-strategies.md` - Content matching algorithms and scoring
- `branching-questions.md` - Experience discovery conversation patterns

## Workflow Details

### Phase 0: Library Initialization

**Always runs first - builds fresh resume database**

**Process:**

1. **Locate resume directory:**
   ```
   User provides path OR default to ./resumes/
   Validate directory exists
   ```

2. **Scan for markdown files:**
   ```
   Use Glob tool: pattern="*.md" path={resume_directory}
   Count files found
   Announce: "Building resume library... found {N} resumes"
   ```

3. **Parse each resume:**
   For each resume file:
   - Use Read tool to load content
   - Extract sections: roles, bullets, skills, education
   - Identify patterns: bullet structure, length, formatting

4. **Build experience database structure:**
   ```json
   {
     "roles": [
       {
         "role_id": "company_title_year",
         "company": "Company Name",
         "title": "Job Title",
         "dates": "YYYY-YYYY",
         "description": "Role summary",
         "bullets": [
           {
             "text": "Full bullet text",
             "themes": ["leadership", "technical"],
             "metrics": ["17x improvement", "$3M revenue"],
             "keywords": ["cross-functional", "program"],
             "source_resumes": ["resume1.md"]
           }
         ]
       }
     ],
     "skills": {
       "technical": ["Python", "Kusto", "AI/ML"],
       "product": ["Roadmap", "Strategy"],
       "leadership": ["Stakeholder mgmt"]
     },
     "education": [...],
     "user_preferences": {
       "typical_length": "1-page|2-page",
       "section_order": ["summary", "experience", "education"],
       "bullet_style": "pattern"
     }
   }
   ```

5. **Tag content automatically:**
   - Themes: Scan for keywords (leadership, technical, analytics, etc.)
   - Metrics: Extract numbers, percentages, dollar amounts
   - Keywords: Frequent technical terms, action verbs

**Output:** In-memory database ready for matching

**Code pattern:**
```python
# Pseudo-code for reference
library = {
    "roles": [],
    "skills": {},
    "education": []
}

for resume_file in glob("resumes/*.md"):
    content = read(resume_file)
    roles = extract_roles(content)
    for role in roles:
        role["bullets"] = tag_bullets(role["bullets"])
        library["roles"].append(role)

return library
```

### Phase 1: Research Phase

**Goal:** Build comprehensive "success profile" beyond just the job description

**Inputs:**
- Job description (text or URL from user)
- Optional: Company name if not in JD

**Process:**

**1.1 Job Description Parsing:**
```
Use research-prompts.md JD parsing template
Extract: requirements, keywords, implicit preferences, red flags, role archetype
```

**1.2 Company Research:**
```
WebSearch queries:
- "{company} mission values culture"
- "{company} engineering blog"
- "{company} recent news"

Synthesize: mission, values, business model, stage
```

**1.3 Role Benchmarking:**
```
WebSearch: "site:linkedin.com {job_title} {company}"
WebFetch: Top 3-5 profiles
Analyze: common backgrounds, skills, terminology

If sparse results, try similar companies
```

**1.4 Success Profile Synthesis:**
```
Combine all research into structured profile (see research-prompts.md template)

Include:
- Core requirements (must-have)
- Valued capabilities (nice-to-have)
- Cultural fit signals
- Narrative themes
- Terminology map (user's background → their language)
- Risk factors + mitigations
```

**Checkpoint:**
```
Present success profile to user:

"Based on my research, here's what makes candidates successful for this role:

{SUCCESS_PROFILE_SUMMARY}

Key findings:
- {Finding 1}
- {Finding 2}
- {Finding 3}

Does this match your understanding? Any adjustments?"

Wait for user confirmation before proceeding.
```

**Output:** Validated success profile document

### Phase 2: Template Generation

**Goal:** Create resume structure optimized for this specific role

**Inputs:**
- Success profile (from Phase 1)
- User's resume library (from Phase 0)

**Process:**

**2.1 Analyze User's Resume Library:**
```
Extract from library:
- All roles, titles, companies, date ranges
- Role archetypes (technical contributor, manager, researcher, specialist)
- Experience clusters (what domains/skills appear frequently)
- Career progression and narrative
```

**2.2 Role Consolidation Decision:**

**When to consolidate:**
- Same company, similar responsibilities
- Target role values continuity over granular progression
- Combined narrative stronger than separate
- Page space constrained

**When to keep separate:**
- Different companies (ALWAYS separate)
- Dramatically different responsibilities that both matter
- Target role values specific progression story
- One position has significantly more relevant experience

**Decision template:**
```
For {Company} with {N} positions:

OPTION A (Consolidated):
Title: "{Combined_Title}"
Dates: "{First_Start} - {Last_End}"
Rationale: {Why consolidation makes sense}

OPTION B (Separate):
Position 1: "{Title}" ({Dates})
Position 2: "{Title}" ({Dates})
Rationale: {Why separate makes sense}

RECOMMENDED: Option {A/B} because {reasoning}
```

**2.3 Title Reframing Principles:**

**Core rule:** Stay truthful to what you did, emphasize aspect most relevant to target

**Strategies:**

1. **Emphasize different aspects:**
   - "Graduate Researcher" → "Research Software Engineer" (if coding-heavy)
   - "Data Science Lead" → "Technical Program Manager" (if leadership)

2. **Use industry-standard terminology:**
   - "Scientist III" → "Senior Research Scientist" (clearer seniority)
   - "Program Coordinator" → "Project Manager" (standard term)

3. **Add specialization when truthful:**
   - "Engineer" → "ML Engineer" (if ML work substantial)
   - "Researcher" → "Computational Ecologist" (if computational methods)

4. **Adjust seniority indicators:**
   - "Lead" vs "Senior" vs "Staff" based on scope

**Constraints:**
- NEVER claim work you didn't do
- NEVER inflate seniority beyond defensible
- Company name and dates MUST be exact
- Core responsibilities MUST be accurate

**2.4 Generate Template Structure:**

```markdown
## Professional Summary
[GUIDANCE: {X} sentences emphasizing {themes from success profile}]
[REQUIRED ELEMENTS: {keywords from JD}]

## Key Skills
[STRUCTURE: {2-4 categories based on JD structure}]
[SOURCE: Extract from library matching success profile]

## Professional Experience

### [ROLE 1 - Most Recent/Relevant]
[CONSOLIDATION: {merge X positions OR keep separate}]
[TITLE OPTIONS:
  A: {emphasize aspect 1}
  B: {emphasize aspect 2}
  Recommended: {option with rationale}]
[BULLET ALLOCATION: {N bullets based on relevance + recency}]
[GUIDANCE: Emphasize {themes}, look for {experience types}]

Bullet 1: [SEEKING: {requirement type}]
Bullet 2: [SEEKING: {requirement type}]
...

### [ROLE 2]
...

## Education
[PLACEMENT: {top if required/recent, bottom if experience-heavy}]

## [Optional Sections]
[INCLUDE IF: {criteria from success profile}]
```

**Checkpoint:**
```
Present template to user:

"Here's the optimized resume structure for this role:

STRUCTURE:
{Section order and rationale}

ROLE CONSOLIDATION:
{Decisions with options}

TITLE REFRAMING:
{Proposed titles with alternatives}

BULLET ALLOCATION:
Role 1: {N} bullets (most relevant)
Role 2: {N} bullets
...

Does this structure work? Any adjustments to:
- Role consolidation?
- Title reframing?
- Bullet allocation?"

Wait for user approval before proceeding.
```

**Output:** Approved template skeleton with guidance for each section
