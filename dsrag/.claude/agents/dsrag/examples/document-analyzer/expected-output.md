# Expected Document Analyzer Output

This document defines what `dsrag:document-analyzer` should produce from `test-sow.md`

## Test Setup

**Project ID:** `test-project`
**Document:** `test-project/documents/test-sow.md`

## Expected Output Files

### 1. Processed Analysis

**File:** `.claude/.dsrag/test-project/processed/documents/test-sow_analysis.md`

**Should contain:**
- Document type: SOW
- Sections identified (Objectives, Scope, Deliverables, Success Criteria, Assumptions, Constraints)
- Key extractions per section
- All quotes with section references

### 2. Requirements Files

#### functional_requirements.md

**Expected IDs:** REQ-F-001 through REQ-F-004

| ID | Requirement | Source |
|---|---|---|
| REQ-F-001 | Reduce permit turnaround from 6-8 weeks to under 2 weeks | Section 1 |
| REQ-F-002 | Digital service delivery for improved citizen satisfaction | Section 1 |
| REQ-F-003 | Streamlined workflows for permit staff, reviewers, inspectors | Section 1 |
| REQ-F-004 | Eliminate paper-based processes across permitting/inspections | Section 1 |

All Priority: High (implied from "primary objective"). Each must include inline citation.

#### non_functional_requirements.md

**Expected IDs:** REQ-NF-001 through REQ-NF-004

| ID | Requirement | Priority | Source |
|---|---|---|---|
| REQ-NF-001 | Project must complete within 12 weeks | Critical | Section 6 |
| REQ-NF-002 | Budget: $180,000 | Critical | Section 6 |
| REQ-NF-003 | Team: 3 consultants (lead, process analyst, tech analyst) | High | Section 6 |
| REQ-NF-004 | Must align with next fiscal year planning cycle (October) | High | Section 6 |

Each must include inline citation.

#### deliverables.md

**Expected IDs:** DELIV-001 through DELIV-004

| ID | Deliverable | Due | Source |
|---|---|---|---|
| DELIV-001 | Current State Assessment Report | Week 4 | Section 3.1 |
| DELIV-002 | Future State Process Design | Week 8 | Section 3.2 |
| DELIV-003 | Vendor Recommendation | Week 10 | Section 3.3 |
| DELIV-004 | Implementation Roadmap | Week 12 | Section 3.4 |

Each must include description and inline citation to source section.

### 3. Decisions File

#### documented_decisions.md

**Expected IDs:** DEC-001 through DEC-004

| ID | Decision | Source |
|---|---|---|
| DEC-001 | Implementation separate, pending city council budget approval | Sections 2, 5 |
| DEC-002 | Scope limited to permits/inspections; non-permit services excluded | Section 2 |
| DEC-003 | City will assign internal project lead for logistics | Section 5 |
| DEC-004 | Assessment includes benchmarking against comparable municipalities | Section 2 |

Each must include inline citation.

## Quality Checks

### MUST Have:
1. Requirements with ID format (REQ-F-XXX, REQ-NF-XXX)
2. Deliverables with ID format (DELIV-XXX)
3. Decisions with ID format (DEC-XXX)
4. All facts cited to document sections
5. Separate functional and non-functional requirements
6. Priority/criticality indicators

### MUST NOT Have:
1. Requirements not stated in document
2. Speculation about intent
3. Auxiliary files
4. Missing citations
5. References to technology platforms, vendors, or implementation details not in the SOW

## Citation Format

```markdown
*[Source: test-project/documents/test-sow.md:Section X, "quote or reference"]*
```
