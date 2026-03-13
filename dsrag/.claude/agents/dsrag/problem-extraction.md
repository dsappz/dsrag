---
agent: problem-extraction
type: lens
invoked-by: dsrag-ingest
description: Extract and categorize problems/issues from transcripts. Categorizes by type (process, technology, organizational, data quality, skills) and severity (critical, high, medium).
---

> **Internal Agent Template** — This file is read by `dsrag-ingest` at runtime. NOT a user-facing skill.

# DSRAG Problem Extraction

Extract and categorize problems, issues, and pain points from transcripts into structured problem database.

## Invocation

Read by `dsrag-ingest` and passed as prompt to a Task agent.

## Prerequisites

- Project must be initialized with `dsrag-init-project`
- Transcript file must exist in `[projectid]/transcripts/`

## Operating Principle

**Two-stage extraction:**
1. Create processed analysis in `.dsrag/[projectid]/processed/transcripts/[filename]_problem_analysis.md`
2. Extract structured problems to `.dsrag/[projectid]/knowledge/problems/`

**STRICT RULE:** Output ONLY to defined structure. No auxiliary files.

## Required Output Structure

**Stage 1: Processed Analysis**
- File: `.dsrag/[projectid]/processed/transcripts/[filename]_problem_analysis.md`
- Contains: Raw problem notes, categorization notes, quotes

**Stage 2: Structured Knowledge:**
```
.dsrag/[projectid]/knowledge/problems/
├── by_category/
│   ├── process_problems.md
│   ├── technology_problems.md
│   ├── organizational_problems.md
│   ├── data_quality_problems.md
│   └── skills_problems.md
├── by_priority/
│   ├── critical.md
│   ├── high.md
│   └── medium.md
└── problem_index.md
```

## Problem Categories

### Process
- Workflow inefficiencies
- Workarounds or bypasses
- Manual processes that should be automated
- Lack of standard procedures
- Process adherence issues

### Technology
- System failures or bugs
- Integration issues
- Performance problems
- Technical debt
- Tool limitations

### Organizational
- Structural issues
- Role confusion
- Communication breakdowns
- Blame dynamics
- Lack of ownership
- Cross-team coordination failures

### Data Quality
- Inaccurate data
- Incomplete data
- Inconsistent data
- No validation
- Data format issues

### Skills / Capability
- Knowledge gaps
- Training needs
- Single points of failure
- Lack of expertise
- Strategic thinking deficits

## Severity Levels

### Critical
- Losing revenue
- Client churn risk
- Major compliance violations
- Complete process breakdown
- Frequent critical failures

**Examples:**
- "Claims sitting for 9 months unprocessed"
- "Reports frequently wrong when sent to clients"

### High
- Significant waste
- Poor quality affecting operations
- Major inefficiencies
- Team dysfunction
- Accumulated technical debt

**Examples:**
- "Teams bypassing established processes"
- "Backlog nobody manages"
- "Inter-team blame game"

### Medium
- Minor inefficiencies
- Annoyances
- Non-critical issues
- Room for optimization

**Examples:**
- "Could automate this manual step"
- "Tool is slow but functional"

## Extraction Process

### Step 1: Read transcript

Read line by line, tracking line numbers for citations.

### Step 2: Identify problems

Extract mentions of:
- Explicit complaints ("this doesn't work", "we're struggling with")
- Failure descriptions ("reports are wrong", "claims sit idle")
- Workarounds ("they just go around the process")
- Gaps ("there's no planning", "we don't have")
- Waste indicators (delays, rework, errors)
- Organizational issues (blame games, lack of coordination)

### Step 3: Analyze each problem

For each problem identified:
1. **Problem statement:** Clear description (what is the problem?)
2. **Category:** Process, Technology, Organizational, Data Quality, or Skills
3. **Severity:** Critical, High, or Medium
4. **Root cause:** If mentioned or inferable from context
5. **Impact:** Business/operational consequences
6. **Who mentioned:** Speaker and role
7. **Related problems:** Links to other problems if applicable

### Step 4: Generate problem ID

Format: `PROB-XXX` where XXX is a zero-padded sequential number

**ID assignment:**
- Check existing problem_index.md for highest ID
- Increment by 1
- Example: If PROB-005 exists, next is PROB-006

### Step 5: Create processed analysis

Write: `.dsrag/[projectid]/processed/transcripts/[filename]_problem_analysis.md`

**Template:**
```markdown
# Problem Analysis: [filename]

**Project:** [project_id]
**Source:** [projectid]/transcripts/[filename]
**Processed:** [timestamp]

## Problems Identified

### PROB-XXX: [Problem Title]
**Line:** X
**Speaker:** [Name]
**Category:** [category]
**Severity:** [severity]

**Problem Statement:**
[Description]

**Root Cause:**
[Cause if mentioned]

**Impact:**
[Impact if mentioned]

**Quote:**
"[exact quote]"

---

[Repeat for each problem]

## Problem Summary

**Total problems:** X
**By Category:**
- Process: X
- Technology: X
- Organizational: X
- Data Quality: X
- Skills: X

**By Severity:**
- Critical: X
- High: X
- Medium: X
```

### Step 6: Extract to category files

Create/update files in `.dsrag/[projectid]/knowledge/problems/by_category/`

**Upsert behavior:** Append new problems, don't overwrite existing

**Template for each category file:**
```markdown
# [Category] Problems

## Problem List

### PROB-XXX: [Problem Title]

**Severity:** [Critical|High|Medium]

**Problem Statement:**
[Clear description]

**Root Cause:**
[Cause if known, otherwise "To be investigated"]

**Impact:**
[Business/operational impact]

**Who Mentioned:**
- [Speaker] (line X from [filename])

**Related Problems:**
- [PROB-YYY if applicable]

**Citations:**
*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*

---

[Next problem]
```

**Example:**
```markdown
# Process Problems

## Problem List

### PROB-001: Process Workarounds (Client Solutions Bypass)

**Severity:** High

**Problem Statement:**
Client Solutions team bypasses established reporting process to contact developers directly, undermining the formal ticket system.

**Root Cause:**
Lack of confidence in formal process; personal relationships override established workflow.

**Impact:**
Undermines reporting team's project management role, creates constant firefighting, prevents systematic issue tracking.

**Who Mentioned:**
- Dana (line 89 from interview-dana.txt)

**Related Problems:**
- PROB-004 (Inter-team blame game)

**Citations:**
*[Source: my-project/transcripts/interview-dana.txt:89, Dana: "the client solutions team will just go around the reporting team direct to the developer because they all know each other"]*
```

### Step 7: Extract to priority files

Create/update files in `.dsrag/[projectid]/knowledge/problems/by_priority/`

**Structure:** Same as category files, but grouped by severity

**Files:**
- `critical.md` - All critical problems
- `high.md` - All high severity problems
- `medium.md` - All medium severity problems

### Step 8: Update problem index

Create/update: `.dsrag/[projectid]/knowledge/problems/problem_index.md`

**Template:**
```markdown
# Problem Index

**Last Updated:** [timestamp]
**Total Problems:** X

## All Problems

| ID | Title | Category | Severity | Source |
|----|-------|----------|----------|--------|
| PROB-001 | Process Workarounds | Process | High | interview-02.txt:89 |
| PROB-002 | Backlog Mismanagement | Process | High | interview-02.txt:95 |
| PROB-003 | Report Quality Issues | Data Quality | Critical | interview-02.txt:160 |
| ... | ... | ... | ... | ... |

## By Category

### Process (X problems)
- PROB-001: Process Workarounds (High)
- PROB-002: Backlog Mismanagement (High)
- ...

### Technology (X problems)
- PROB-006: Claims Sitting Idle (Critical)
- ...

### Organizational (X problems)
- PROB-004: Inter-Team Blame Game (High)
- ...

### Data Quality (X problems)
- PROB-003: Report Quality Issues (Critical)
- ...

### Skills (X problems)
- ...

## By Severity

### Critical (X problems)
- PROB-003: Report Quality Issues
- PROB-006: Claims Sitting Idle

### High (X problems)
- PROB-001: Process Workarounds
- PROB-002: Backlog Mismanagement
- PROB-004: Inter-Team Blame Game

### Medium (X problems)
- ...

## Sources

- interview-dana.txt: PROB-001, PROB-002, PROB-003, PROB-004, PROB-005, PROB-006
- [other-transcript].txt: PROB-007, PROB-008
```

## Citation Format (STRICT)

Every problem MUST have inline citation:

```markdown
*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*
```

## Upsert Logic

When problem files already exist:

1. **Read existing files**
2. **Check highest PROB-XXX ID**
3. **Assign new IDs sequentially**
4. **Append new problems to category files**
5. **Append new problems to priority files**
6. **Regenerate problem_index.md** (rewrite entire file with all problems)

## Conflict Detection

**Before appending new problems, check for conflicts with existing problem definitions.**

### When to Check for Conflicts

Run conflict detection when adding:
- Severity assessments (same problem, different severity levels)
- Problem categorization (same problem, different categories)
- Impact descriptions (contradictory business impact statements)
- Root cause analysis (conflicting root cause theories)

### How to Detect Conflicts

Use the conflict detector script:

```bash
python .claude/scripts/dsrag/dsrag_conflict_detector.py \
    --existing-file ".dsrag/$PROJECT_ID/knowledge/problems/by_category/[category]_problems.md" \
    --new-assertion "$NEW_PROBLEM_DESCRIPTION" \
    --context "severity" \
    --existing-source "transcript A, line 15" \
    --new-source "transcript B, line 42"
```

**Exit codes:**
- `0` = No conflict detected, safe to append
- `1` = Conflict detected, user resolution required

### If Conflict Detected

Use AskUserQuestion to prompt user:

**Question:** "Conflicting information detected about [problem]. How should we resolve this?"

**Options:**
1. **"Keep existing"** - Preserve current problem definition, discard new assertion
   - Description: "Trust the existing source ([existing_source])"

2. **"Replace with new"** - Replace old with new assertion
   - Description: "Trust the new source ([new_source]) and update existing knowledge"

3. **"Keep both with note"** - Preserve both, add conflict marker
   - Description: "Document both perspectives with citations"

4. **"Manual resolution"** - User will edit manually
   - Description: "Skip automatic update, I'll resolve this manually"

**Apply user choice:**

- **Keep existing:** Skip appending new content
- **Replace with new:** Find and replace existing assertion with new
- **Keep both:** Append new content with conflict note:
  ```markdown
  **Note:** Conflicting severity assessments exist:
  - [Existing source]: "Severity: High"
  - [New source]: "Severity: Critical"
  ```
- **Manual resolution:** Skip automatic update, log conflict for user review

### Conflict Examples

**Severity conflict:**
```
Existing: "Severity: High"
New:      "Severity: Critical"
-> Different severity levels for same problem
```

**Category conflict:**
```
Existing: "Category: Process"
New:      "Category: Technology"
-> Different categorization (Note: problems CAN span multiple categories legitimately)
```

**Impact conflict:**
```
Existing: "Impact: Minor delays in reporting"
New:      "Impact: Losing revenue, client churn risk"
-> Significantly different impact assessments
```

## Error Prevention

**DO:**
- Assign unique PROB-XXX IDs
- Categorize each problem
- Assign severity based on business impact
- Cite every problem to source
- Update problem_index.md
- Create both category and priority views
- Identify root cause if mentioned

**DON'T:**
- Speculate on root causes not mentioned
- Create auxiliary files
- Skip citations
- Assign duplicate IDs
- Overwrite existing problems
- Forget to update index

## Testing

**Test with:**
- `.claude/agents/dsrag/examples/problem-extraction/test-transcript.txt`
- Project ID: `test-project`

**Expected output documented in:**
- `.claude/agents/dsrag/examples/problem-extraction/expected-output.md`

## Implementation Notes

1. **Problem identification:** Look for negative language, complaints, "doesn't work", "problem with", "issue is"
2. **Categorization:** A problem can belong to multiple categories (e.g., process AND data quality)
3. **Severity assignment:** Focus on business impact, not just technical severity
4. **Root cause:** Only state if explicitly mentioned; otherwise say "To be investigated"
5. **Related problems:** Link problems that are connected or caused by each other
6. **Multi-source:** Same problem from multiple transcripts? Add additional citations to existing problem
