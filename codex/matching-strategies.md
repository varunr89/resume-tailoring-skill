# Content Matching Strategies

## Overview

Match experiences from library to template slots with transparent confidence scoring.

## Matching Criteria (Weighted)

**1. Direct Match (40%)**
- Keywords overlap with JD/success profile
- Same domain/technology mentioned
- Same type of outcome required
- Same scale or complexity level

**Scoring:**
- 90-100%: Exact match (same skill, domain, context)
- 70-89%: Strong match (same skill, different domain)
- 50-69%: Good match (overlapping keywords, similar outcomes)
- <50%: Weak direct match

**2. Transferable Skills (30%)**
- Same capability in different context
- Leadership in different domain
- Technical problem-solving in different stack
- Similar scale/complexity in different industry

**Scoring:**
- 90-100%: Directly transferable (process, skill generic)
- 70-89%: Mostly transferable (some domain translation needed)
- 50-69%: Partially transferable (analogy required)
- <50%: Stretch to call transferable

**3. Adjacent Experience (20%)**
- Touched on skill as secondary responsibility
- Used related tools/methodologies
- Worked in related problem space
- Supporting role in relevant area

**Scoring:**
- 90-100%: Closely adjacent (just different framing)
- 70-89%: Clearly adjacent (related but distinct)
- 50-69%: Somewhat adjacent (requires explanation)
- <50%: Loosely adjacent

**4. Impact Alignment (10%)**
- Achievement type matches what role values
- Quantitative metrics (if JD emphasizes data-driven)
- Team outcomes (if JD emphasizes collaboration)
- Innovation (if JD emphasizes creativity)
- Scale (if JD emphasizes hyperscale)

**Scoring:**
- 90-100%: Perfect impact alignment
- 70-89%: Strong impact alignment
- 50-69%: Moderate impact alignment
- <50%: Weak impact alignment

## Overall Confidence Score

```
Overall = (Direct × 0.4) + (Transferable × 0.3) + (Adjacent × 0.2) + (Impact × 0.1)
```

**Confidence Bands:**
- 90-100%: DIRECT - Use with confidence
- 75-89%: TRANSFERABLE - Strong candidate
- 60-74%: ADJACENT - Acceptable with reframing
- 45-59%: WEAK - Consider only if no better option
- <45%: GAP - Flag as unaddressed requirement

## Content Reframing Strategies

**When to reframe:** Good match (>60%) but language doesn't align with target terminology

**Strategy 1: Keyword Alignment**
```
Preserve meaning, adjust terminology

Before: "Led experimental design and data analysis programs"
After:  "Led data science programs combining experimental design and
         statistical analysis"
Reason: Target role uses "data science" terminology
```

**Strategy 2: Emphasis Shift**
```
Same facts, different focus

Before: "Designed statistical experiments... saving millions in recall costs"
After:  "Prevented millions in potential recall costs through predictive
         risk detection using statistical modeling"
Reason: Target role values business outcomes over technical methods
```

**Strategy 3: Abstraction Level**
```
Adjust technical specificity

Before: "Built MATLAB-based automated system for evaluation"
After:  "Developed automated evaluation system"
Reason: Target role is language-agnostic, emphasize outcome

OR

After:  "Built automated evaluation system (MATLAB, Python integration)"
Reason: Target role values technical specificity
```

**Strategy 4: Scale Emphasis**
```
Highlight relevant scale aspects

Before: "Managed project with 3 stakeholders"
After:  "Led cross-functional initiative coordinating 3 organizational units"
Reason: Emphasize cross-org complexity over headcount
```

## Gap Handling

**When match confidence < 60%:**

**Option 1: Reframe Adjacent Experience**
```
Present reframing option:

TEMPLATE SLOT: {Requirement}
BEST MATCH: {Experience} (Confidence: {score}%)

REFRAME OPPORTUNITY:
Original: "{bullet_text}"
Reframed: "{adjusted_text}"
Justification: {why this is truthful}

RECOMMENDATION: Use reframed version? Y/N
```

**Option 2: Flag as Gap**
```
GAP IDENTIFIED: {Requirement}

AVAILABLE OPTIONS:
None with confidence >60%

RECOMMENDATIONS:
1. Address in cover letter - emphasize learning ability
2. Omit bullet slot - reduce template allocation
3. Include best available match ({score}%) with disclosure
4. Discover new experience through brainstorming

User decides how to proceed.
```

**Option 3: Discover New Experience**
```
If Experience Discovery not yet run:

"This gap might be addressable through experience discovery.
Would you like to do a quick branching interview about {gap_area}?"

If already run:
Accept gap, move forward.
```
