# Research Phase Prompts

## Job Description Parsing

**Prompt template:**
```
Analyze this job description and extract:

1. EXPLICIT REQUIREMENTS (must-have vs nice-to-have)
2. TECHNICAL KEYWORDS and domain terminology
3. IMPLICIT PREFERENCES (cultural signals, hidden requirements)
4. RED FLAGS (overqualification risks, mismatches)
5. ROLE ARCHETYPE (IC technical / people leadership / cross-functional)

Job Description:
{JD_TEXT}

Output as structured sections.
```

## Company Research

**WebSearch queries:**
```
1. "{company_name} mission values culture"
2. "{company_name} engineering blog"
3. "{company_name} recent news product launches"
4. "{company_name} team structure engineering"
```

**Synthesis prompt:**
```
Based on these search results, summarize:

1. Company mission and values
2. Cultural priorities
3. Business model and customer base
4. Team structure (if available)
5. Company stage (startup/growth/mature) and implications

Search results:
{SEARCH_RESULTS}
```

## Role Benchmarking

**WebSearch + WebFetch strategy:**
```
1. Search: "site:linkedin.com {job_title} {company_name}"
2. Fetch: Top 3-5 profiles
3. Fallback: "site:linkedin.com {job_title} {similar_company}"
```

**Analysis prompt:**
```
Analyze these LinkedIn profiles for people in similar roles:

Extract patterns:
1. Common backgrounds and career paths
2. Emphasized skills and project types
3. Terminology they use to describe similar work
4. Notable accomplishments or themes

Profiles:
{PROFILE_DATA}
```

## Success Profile Synthesis

**Synthesis prompt:**
```
Combine job description analysis, company research, and role benchmarking into:

## Success Profile: {Role} at {Company}

### Core Requirements (Must-Have)
- {Requirement}: {Evidence from JD/research}

### Valued Capabilities (Nice-to-Have)
- {Capability}: {Why it matters in this context}

### Cultural Fit Signals
- {Value}: {How to demonstrate}

### Narrative Themes
- {Theme}: {Examples from similar role holders}

### Terminology Map
Standard term → Company-preferred term

### Risk Factors
- {Concern}: {Mitigation strategy}
```
