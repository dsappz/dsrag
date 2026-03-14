# Expected Problem Extraction Output

This document defines what `dsrag:problem-extraction` should produce from `test-transcript.txt`

## Test Setup

**Project ID:** `test-project`
**Transcript:** `test-project/transcripts/test-transcript.txt`

## Expected Problems Identified

### PROB-001: Paper Permit Processing Delays
**Category:** Process
**Severity:** Critical
**Statement:** Paper-based permit applications take 6-8 weeks to process when the target should be 2 weeks
**Root Cause:** Manual paper-based workflow requiring physical routing between departments for sign-off
**Impact:** Citizen frustration, loss of faith in city services
**Source:** Line 1, Rachel
**Citation:** "we're looking at six to eight weeks on average. It should be two weeks, max. People are furious"

### PROB-002: No Permit Status Tracking for Citizens
**Category:** Technology
**Severity:** Critical
**Statement:** No system exists for citizens to check permit status, resulting in staff spending hours on phone calls
**Root Cause:** No tracking system in place
**Impact:** Staff time wasted on phone inquiries, poor citizen experience (one citizen called 17 times in 3 weeks)
**Source:** Line 3, Tom
**Citation:** "There's no tracking system. So what happens is the homeowner calls us, and my front desk staff spend hours every day just answering the phone"

### PROB-003: Inspection Scheduling via Whiteboard
**Category:** Process / Technology
**Severity:** Critical
**Statement:** Inspection scheduling is done on a physical whiteboard, leading to errors where inspectors show up at wrong addresses
**Root Cause:** No digital scheduling system; information easily erased or incorrectly recorded
**Impact:** Inspectors dispatched to wrong addresses (3 incidents last month), homeowners left waiting
**Source:** Line 7, Rachel
**Citation:** "Linda's team uses a whiteboard in their office to schedule inspections. A literal whiteboard. So if someone erases something or writes the wrong address, the inspector shows up at the wrong house"

### PROB-004: Disconnected Systems (Permits, Inspections, Payments)
**Category:** Technology
**Severity:** High
**Statement:** Three separate systems (paper permits, inspections spreadsheet, city financial system) do not integrate with each other
**Root Cause:** Organically developed independent tracking methods with no integration layer
**Impact:** Manual reconciliation required; missed payment updates cause false delinquency notices to citizens who already paid
**Source:** Line 9, Tom
**Citation:** "we have three completely separate systems that don't talk to each other"

### PROB-005: Permits Staff Turnover
**Category:** Organizational
**Severity:** High
**Statement:** 40% staff turnover in the permits office over 2 years (5 out of 12 staff), driven by frustration
**Root Cause:** Staff feel set up to fail; they absorb citizen anger over systemic problems they cannot fix
**Impact:** Institutional knowledge loss, slower processing, vicious cycle of worsening service and further turnover
**Source:** Line 5, Rachel
**Citation:** "I've lost five people in the last two years out of a team of twelve. That's almost half. And when I do exit interviews, every single one of them says the same thing"

### PROB-006: IT Budget Requests Rejected by City Council
**Category:** Organizational
**Severity:** High
**Statement:** Budget requests for a unified permits and inspections system have been rejected by the city council three years running
**Root Cause:** City council does not perceive technology modernization as a priority; they see line item cost but not hidden costs of inefficiency
**Impact:** Modernization stalled, no path to systemic improvement, staff and citizen problems persist
**Source:** Line 13, Tom
**Citation:** "I've put in budget requests for a unified permits and inspections system three years in a row now. Three years. And the city council has rejected it every single time"

### PROB-007: Failed Scheduling App Rollout (Change Management)
**Category:** Organizational / Skills
**Severity:** Medium
**Statement:** A previous attempt to deploy a scheduling app for inspections failed because it was dropped on staff with no training or input
**Root Cause:** No change management strategy; no user input gathered before deployment; no training provided
**Impact:** Burned goodwill, created institutional skepticism toward technology projects ("proof that technology doesn't work here")
**Source:** Line 17, Tom
**Citation:** "We bought the tool, dropped it on Linda's desk, and said here you go. No training, no input from her team on what they needed"

### PROB-008: Paper Records at Risk of Loss
**Category:** Process
**Severity:** High
**Statement:** Decades of paper permit records stored in filing cabinets with no digital backup, in a room with no sprinkler system
**Root Cause:** No digitization effort undertaken; facilities improvements not prioritized
**Impact:** Catastrophic data loss risk (fire or flood would destroy 40+ years of city permit records)
**Source:** Line 19, Rachel
**Citation:** "If there's a fire or a flood in that office, we lose everything. There's no backup. No digital copies"

## Expected Output Structure

### by_category/process_problems.md
- PROB-001: Paper Permit Processing Delays
- PROB-003: Inspection Scheduling via Whiteboard
- PROB-008: Paper Records at Risk of Loss

### by_category/technology_problems.md
- PROB-002: No Permit Status Tracking for Citizens
- PROB-003: Inspection Scheduling via Whiteboard (also in process)
- PROB-004: Disconnected Systems

### by_category/organizational_problems.md
- PROB-005: Permits Staff Turnover
- PROB-006: IT Budget Requests Rejected by City Council
- PROB-007: Failed Scheduling App Rollout

### by_category/skills_problems.md
- PROB-007: Failed Scheduling App Rollout (also in organizational)

### by_category/data_quality_problems.md
- (none identified in this transcript)

### by_priority/critical.md
- PROB-001: Paper Permit Processing Delays
- PROB-002: No Permit Status Tracking for Citizens
- PROB-003: Inspection Scheduling via Whiteboard

### by_priority/high.md
- PROB-004: Disconnected Systems
- PROB-005: Permits Staff Turnover
- PROB-006: IT Budget Requests Rejected by City Council
- PROB-008: Paper Records at Risk of Loss

### by_priority/medium.md
- PROB-007: Failed Scheduling App Rollout

### problem_index.md
Master list of all problems with ID, category, severity, one-line summary

## Quality Checks

### MUST Have:
1. Problem ID format: PROB-XXX
2. Each problem has: statement, category, severity, root cause, impact, citation
3. Problems appear in relevant category files
4. Problems appear in relevant priority files
5. problem_index.md cross-references all problems
6. All facts cited with line numbers

### MUST NOT Have:
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

## Citation Format

```markdown
*[Source: test-project/transcripts/test-transcript.txt:1, Rachel: "we're looking at six to eight weeks on average. It should be two weeks, max"]*
```
