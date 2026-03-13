# Expected Problem Extraction Output

This document defines what `dsrag:problem-extraction` should produce from `test-transcript.txt`

## Test Setup

**Project ID:** `test-project`
**Transcript:** `test-project/transcripts/test-transcript.txt`

## Expected Problems Identified

### PROB-001: Process Workarounds (Client Solutions Bypass)
**Category:** Process
**Severity:** High
**Statement:** Client Solutions team bypasses established reporting process to contact developers directly
**Root Cause:** Lack of confidence in formal ticket system, personal relationships override process
**Impact:** Undermines reporting team role, creates chaos and constant firefighting
**Source:** Line 3, Speaker 2
**Citation:** "the client solutions team will just go around the reporting team direct to the developer because they all know each other"

### PROB-002: Backlog Mismanagement
**Category:** Process
**Severity:** High
**Statement:** Enhancements go into backlog that nobody pays attention to
**Root Cause:** Team focuses on immediate fixes rather than systemic improvements
**Impact:** Technical debt accumulates, root causes never addressed
**Source:** Line 5, Speaker 2
**Citation:** "it becomes an enhancement that ends up in the backlog that nobody really pays attention to"

### PROB-003: Report Quality Issues
**Category:** Data Quality
**Severity:** Critical
**Statement:** Reports are frequently wrong before clients see them
**Root Cause:** No validation before automatic upload to portal
**Impact:** Client trust erosion, account manager anxiety
**Source:** Line 6, Speaker 2
**Citation:** "considering how often they're wrong, they're worried a client is going to get a report that's wrong"

### PROB-004: Inter-Team Blame Game
**Category:** Organizational
**Severity:** High
**Statement:** Each team blames the team behind them in the value stream
**Root Cause:** Lack of shared ownership and accountability
**Impact:** No collaborative problem-solving, prevents root cause resolution
**Source:** Line 8, Speaker 2
**Citation:** "everyone on if you look at the process of, like, client data all the way through to reporting, every team that was one above would blame the team behind it"

### PROB-005: Data Ingestion Policy Contradiction
**Category:** Process / Data Quality
**Severity:** High
**Statement:** Policy says "accept any data format" but team can't actually process it
**Root Cause:** Misalignment between stated policy and technical capability
**Impact:** Data quality issues, processing failures
**Source:** Line 8, Speaker 2
**Citation:** "there's clearly a gap in send us whatever you want and we'll figure it out, because they're not figuring it out"

### PROB-006: Claims Sitting Idle
**Category:** Technology / Process
**Severity:** Critical
**Statement:** Files get ingested but don't move to processing, claims sit for 9 months
**Root Cause:** Technical issue in workflow (files don't get moved)
**Impact:** Revenue loss, unprocessed claims
**Source:** Line 9, Hank (quoting Frank)
**Citation:** "sometimes a file will get ingested, but it won't get moved. And so for, like, I think you said nine months, a claim would be sitting there"

## Expected Output Structure

### by_category/process_problems.md
- PROB-001: Process Workarounds
- PROB-002: Backlog Mismanagement
- PROB-005: Data Ingestion Policy Contradiction

### by_category/technology_problems.md
- PROB-006: Claims Sitting Idle (technical component)

### by_category/organizational_problems.md
- PROB-004: Inter-Team Blame Game

### by_category/data_quality_problems.md
- PROB-003: Report Quality Issues
- PROB-005: Data Ingestion Policy Contradiction (also in process)

### by_priority/critical.md
- PROB-003: Report Quality Issues
- PROB-006: Claims Sitting Idle

### by_priority/high.md
- PROB-001: Process Workarounds
- PROB-002: Backlog Mismanagement
- PROB-004: Inter-Team Blame Game
- PROB-005: Data Ingestion Policy Contradiction

### problem_index.md
Master list of all problems with ID, category, severity, one-line summary

## Quality Checks

### ✅ MUST Have:
1. Problem ID format: PROB-XXX
2. Each problem has: statement, category, severity, root cause, impact, citation
3. Problems appear in relevant category files
4. Problems appear in relevant priority files
5. problem_index.md cross-references all problems
6. All facts cited with line numbers

### ❌ MUST NOT Have:
1. Problems without citations
2. Speculative root causes not mentioned in transcript
3. Auxiliary files
4. Duplicate problem entries

## Problem Statement Template

```markdown
### PROB-XXX: [Problem Title]

**Category:** [Process|Technology|Organizational|Data Quality|Skills]
**Severity:** [Critical|High|Medium]

**Problem Statement:**
[Clear description of the problem]

**Root Cause:**
[Underlying cause if mentioned, otherwise "To be investigated"]

**Impact:**
[Business/operational impact]

**Who Mentioned:**
- [Speaker] (line X)

**Related Problems:**
- [PROB-YYY if related]

**Citations:**
*[Source: test-project/transcripts/test-transcript.txt:X, Speaker: "quote"]*
```
