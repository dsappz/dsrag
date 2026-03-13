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
```markdown
# Functional Requirements

## REQ-F-001: Real-Time Data Processing
**Source:** Project Objectives (Section 1)
**Priority:** High (implied from "primary objective")

Enable real-time data processing capabilities for operational analytics.

*[Source: test-project/documents/test-sow.md:Section 1, "Real-time data processing capabilities"]*

## REQ-F-002: Self-Service Analytics
**Source:** Project Objectives (Section 1)
**Priority:** High

Enable business users to access and analyze data without IT dependency.

*[Source: test-project/documents/test-sow.md:Section 1, "Self-service analytics for business users"]*

## REQ-F-003: Data Governance Framework
**Source:** In Scope (Section 2)
**Priority:** High

Design comprehensive data governance framework.

*[Source: test-project/documents/test-sow.md:Section 2, "Data governance framework design"]*
```

#### non_functional_requirements.md
```markdown
# Non-Functional Requirements

## REQ-NF-001: Cost Reduction
**Source:** Project Objectives (Section 1)
**Priority:** High

Achieve cost reduction through cloud migration.

*[Source: test-project/documents/test-sow.md:Section 1, "Cost reduction through cloud migration"]*

## REQ-NF-002: Data Quality Improvement
**Source:** Project Objectives (Section 1)
**Priority:** High

Improve data quality across the platform.

*[Source: test-project/documents/test-sow.md:Section 1, "Improved data quality and governance"]*

## REQ-NF-003: Timeline Constraint
**Source:** Constraints (Section 6)
**Priority:** Critical

Project must complete within 12 weeks.

*[Source: test-project/documents/test-sow.md:Section 6, "Project duration: 12 weeks"]*

## REQ-NF-004: Budget Constraint
**Source:** Constraints (Section 6)
**Priority:** Critical

Project budget is $250,000.

*[Source: test-project/documents/test-sow.md:Section 6, "Budget: $250,000"]*
```

#### deliverables.md
```markdown
# Deliverables

## DELIV-001: Current State Assessment Report
**Due:** Week 4
**Type:** Analysis Document

Comprehensive analysis of existing data landscape including systems, processes, and pain points.

*[Source: test-project/documents/test-sow.md:Section 3.1]*

## DELIV-002: Future State Architecture Design
**Due:** Week 8
**Type:** Technical Design

Detailed technical architecture for target cloud data platform.

*[Source: test-project/documents/test-sow.md:Section 3.2]*

## DELIV-003: Platform Recommendation
**Due:** Week 10
**Type:** Decision Document

Evaluation of platform options (Cloud Data Warehouse A, Cloud Data Warehouse B, hybrid) with recommendation and justification.

*[Source: test-project/documents/test-sow.md:Section 3.3]*

## DELIV-004: Migration Roadmap
**Due:** Week 12
**Type:** Roadmap

Phased approach to migrating from current to future state with timeline and dependencies.

*[Source: test-project/documents/test-sow.md:Section 3.4]*
```

### 3. Decisions File

#### documented_decisions.md
```markdown
# Documented Decisions

## DEC-001: Platform Options
**Source:** In Scope (Section 2)
**Decision:** Platform options under consideration are Cloud Data Warehouse A, Cloud Data Warehouse B, or hybrid

*[Source: test-project/documents/test-sow.md:Section 2, "Platform selection recommendation (Cloud Data Warehouse A, Cloud Data Warehouse B, or hybrid)"]*

## DEC-002: Cloud Migration Approach
**Source:** Project Objectives (Section 1)
**Decision:** Platform will be cloud-based (migration from current state)

*[Source: test-project/documents/test-sow.md:Section 1, "cloud migration" + Section 2 "cloud-based data platform"]*

## DEC-003: Implementation Separate
**Source:** Out of Scope + Assumptions (Sections 2, 5)
**Decision:** Implementation phase will be separate engagement

*[Source: test-project/documents/test-sow.md:Section 2 "Out of Scope" and Section 5 "Implementation phase will be separate engagement"]*

## DEC-004: Assessment-First Approach
**Source:** In Scope (Section 2)
**Decision:** Start with current state assessment before designing future state

*[Source: test-project/documents/test-sow.md:Section 2, In Scope items listed sequentially starting with assessment]*
```

## Expected Processed Analysis Structure

```markdown
# Document Analysis: test-sow

**Project:** test-project
**Source:** test-project/documents/test-sow.md
**Document Type:** Statement of Work (SOW)
**Processed:** [timestamp]

## Document Overview
- **Title:** Statement of Work - Test Project
- **Sections:** 6 main sections
- **Length:** [lines/pages]

## Section-by-Section Analysis

### Section 1: Project Objectives
**Key objectives identified:**
- Real-time data processing
- Self-service analytics
- Improved data quality/governance
- Cost reduction via cloud

### Section 2: Scope
**In Scope:** 5 items
**Out of Scope:** 4 items

### Section 3: Deliverables
**Total:** 4 deliverables
**Timeline:** Week 4 → Week 12

### Section 4: Success Criteria
**Total:** 4 success criteria identified

### Section 5: Assumptions
**Total:** 4 assumptions

### Section 6: Constraints
**Total:** 4 constraints
- Time: 12 weeks
- Budget: $250K
- Team: 4 consultants
- Dependency: Q2 board presentation

## Extraction Summary
- **Functional Requirements:** 3
- **Non-Functional Requirements:** 4
- **Deliverables:** 4
- **Decisions:** 4
- **Assumptions:** 4
- **Constraints:** 4
```

## Quality Checks

### ✅ MUST Have:
1. Requirements with ID format (REQ-F-XXX, REQ-NF-XXX)
2. Deliverables with ID format (DELIV-XXX)
3. Decisions with ID format (DEC-XXX)
4. All facts cited to document sections
5. Separate functional and non-functional requirements
6. Priority/criticality indicators

### ❌ MUST NOT Have:
1. Requirements not stated in document
2. Speculation about intent
3. Auxiliary files
4. Missing citations

## Citation Format

```markdown
*[Source: test-project/documents/test-sow.md:Section X, "quote or reference"]*
```
