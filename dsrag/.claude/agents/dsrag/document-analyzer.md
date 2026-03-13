---
agent: document-analyzer
type: lens
invoked-by: dsrag-ingest
description: Extract structured knowledge from documents (SOWs, specs, diagrams, policies) and embedded images (architecture diagrams, whiteboard photos, screenshots). Outputs requirements, deliverables, decisions, assumptions, constraints.
---

> **Internal Agent Template** — This file is read by `dsrag-ingest` at runtime. NOT a user-facing skill.

# DSRAG Document Analyzer

Extract structured knowledge from documents into requirements, deliverables, and decisions.

## Invocation

Read by `dsrag-ingest` and passed as prompt to a Task agent.

## Prerequisites

- Project must be initialized with `dsrag-init-project`
- Document file must exist in `[projectid]/documents/`

## Operating Principle

**Two-stage extraction:**
1. Create processed analysis in `.dsrag/[projectid]/processed/documents/[filename]_analysis.md`
2. Extract structured knowledge to requirements/, deliverables/, decisions/ folders

**STRICT RULE:** Output ONLY to defined structure. No auxiliary files.

## Required Output Structure

**Stage 1: Processed Analysis**
- File: `.dsrag/[projectid]/processed/documents/[filename]_analysis.md`
- Contains: Section-by-section breakdown, extraction notes, quotes

**Stage 2: Structured Knowledge:**
```
.dsrag/[projectid]/knowledge/
├── requirements/
│   ├── functional_requirements.md
│   ├── non_functional_requirements.md
│   └── deliverables.md
└── decisions/
    └── documented_decisions.md
```

## Supported Document Types

### Statement of Work (SOW)
- Objectives
- Scope (in/out)
- Deliverables
- Success criteria
- Assumptions
- Constraints
- Timeline

### Technical Specification
- Requirements (functional/non-functional)
- Architecture decisions
- Technical constraints
- Dependencies
- Success metrics

### Business Requirements Document (BRD)
- Business objectives
- Functional requirements
- User stories
- Acceptance criteria
- Constraints

### Architecture Diagram (Text)
- Component descriptions
- Integration points
- Technology decisions
- Design rationale

### Image-Containing Documents
Documents may contain embedded images (diagrams, architecture screenshots, whiteboard photos, process flows). When encountering images:

**What to extract from images:**
- **Architecture diagrams:** Components, connections, technology labels, data flows
- **Whiteboard photos:** Key concepts, relationships, decisions captured visually
- **Process flow diagrams:** Steps, decision points, actors, swim lanes
- **Screenshots:** System names, UI elements, configuration details, error states
- **Org charts:** Reporting structures, team boundaries, role assignments

**How to handle images:**
1. Describe what the image shows (components, relationships, labels)
2. Extract any text visible in the image (labels, annotations, titles)
3. Map image content to appropriate extraction categories (requirements, decisions, architecture)
4. Cite as: `*[Source: [projectid]/documents/[filename]:Image on Page X, "description"]*`

**Image extraction principles:**
- Treat image content as equal to text content for extraction purposes
- Cross-reference image content with surrounding text for context
- If image contradicts text, note the discrepancy in processed analysis
- If image is unreadable or low quality, note as: `[Image on Page X: unreadable/low quality — skipping]`

## Extraction Process

### Step 1: Read document

Read entire document, tracking section headers and line/page numbers.

### Step 2: Identify document type

Determine document type from:
- Title/heading
- Section structure
- Content patterns

### Step 3: Extract by section

For each section, identify:
- **Objectives:** What the project aims to achieve
- **Requirements:** What must be delivered (functional/non-functional)
- **Deliverables:** Specific artifacts to produce
- **Decisions:** Choices already made
- **Assumptions:** What is assumed to be true
- **Constraints:** Limitations (time, budget, scope, technical)
- **Success criteria:** How success is measured

### Step 4: Create processed analysis

Write: `.dsrag/[projectid]/processed/documents/[filename]_analysis.md`

**Template:**
```markdown
# Document Analysis: [filename]

**Project:** [project_id]
**Source:** [projectid]/documents/[filename]
**Document Type:** [SOW|Spec|BRD|Architecture|Policy]
**Processed:** [timestamp]

## Document Overview
- **Title:** [document title]
- **Sections:** [number] main sections
- **Length:** [pages/lines]

## Section-by-Section Analysis

### Section [X]: [Section Name]
**Key points:**
- [Point 1]
- [Point 2]

**Extractions:**
- Requirements: [count]
- Deliverables: [count]
- Decisions: [count]

---

[Repeat for each section]

## Extraction Summary
- **Functional Requirements:** [count]
- **Non-Functional Requirements:** [count]
- **Deliverables:** [count]
- **Decisions:** [count]
- **Assumptions:** [count]
- **Constraints:** [count]
```

### Step 5: Extract functional requirements

**Path:** `.dsrag/[projectid]/knowledge/requirements/functional_requirements.md`

**ID Format:** REQ-F-XXX (zero-padded sequential)

**Template:**
```markdown
# Functional Requirements

## REQ-F-001: [Requirement Title]

**Source:** [Section name]
**Priority:** [Critical|High|Medium|Low]

[Requirement description]

*[Source: [projectid]/documents/[filename]:Section X, "quote or reference"]*

---

[Next requirement]
```

**Priority assignment:**
- **Critical:** Explicitly called out as must-have, primary objective, or success criteria
- **High:** Core functionality, explicitly in scope
- **Medium:** Nice-to-have, implied importance
- **Low:** Optional, edge cases

### Step 6: Extract non-functional requirements

**Path:** `.dsrag/[projectid]/knowledge/requirements/non_functional_requirements.md`

**ID Format:** REQ-NF-XXX

**Categories:**
- Performance (speed, scalability)
- Quality (accuracy, completeness)
- Cost (budget, TCO)
- Timeline (schedule, deadlines)
- Security (compliance, access control)
- Usability (user experience, accessibility)
- Reliability (uptime, availability)

**Template:** Same as functional requirements

### Step 7: Extract deliverables

**Path:** `.dsrag/[projectid]/knowledge/requirements/deliverables.md`

**ID Format:** DELIV-XXX

**Template:**
```markdown
# Deliverables

## DELIV-001: [Deliverable Name]

**Due:** [Date/milestone]
**Type:** [Document|Design|Code|Report|Roadmap|Presentation]

[Deliverable description]

*[Source: [projectid]/documents/[filename]:Section X]*

---

[Next deliverable]
```

### Step 8: Extract documented decisions

**Path:** `.dsrag/[projectid]/knowledge/decisions/documented_decisions.md`

**ID Format:** DEC-XXX

**Template:**
```markdown
# Documented Decisions

## DEC-001: [Decision Title]

**Source:** [Section name]
**Decision:** [What was decided]

[Additional context or rationale if provided]

*[Source: [projectid]/documents/[filename]:Section X, "quote"]*

---

[Next decision]
```

## Citation Format (STRICT)

Every extraction MUST have inline citation:

```markdown
*[Source: [projectid]/documents/[filename]:Section X, "quote or reference"]*
```

**Section reference formats:**
- By section number: `Section 3.2`
- By section name: `Section "Project Objectives"`
- By page: `Page 5`
- By line range: `Lines 45-50`

**Examples:**
```markdown
*[Source: my-project/documents/sow-03.md:Section 2.1, "Platform selection recommendation"]*
*[Source: test-project/documents/requirements.md:Section "Success Criteria"]*
```

**For image-based extractions:**
```markdown
*[Source: my-project/documents/architecture-overview.pdf:Image on Page 3, "System architecture diagram showing 4 microservices"]*
*[Source: my-project/documents/whiteboard-session.pdf:Image on Page 1, "Whiteboard capture of data flow"]*
```

## Upsert Logic

When knowledge files already exist:

1. **Read existing files**
2. **Check highest ID** (REQ-F-XXX, REQ-NF-XXX, DELIV-XXX, DEC-XXX)
3. **Assign new IDs sequentially**
4. **Append new extractions** with source marker
5. **Never delete existing content**

**Example upsert:**
```markdown
# Functional Requirements

[Existing requirements from previous documents...]

---

## Requirements from [filename]

### REQ-F-008: [New Requirement]
[Details...]

*[Source: [projectid]/documents/[filename]:Section X]*
```

## Special Handling

### Assumptions
If document contains assumptions section, create note in processed analysis but extract as requirements with [ASSUMPTION] tag:

```markdown
## REQ-NF-005: Stakeholder Access [ASSUMPTION]
**Source:** Assumptions (Section 5)
**Priority:** Critical

Assumes client will provide timely access to stakeholders for interviews.

*[Source: test-project/documents/test-sow.md:Section 5]*
```

### Constraints
Extract as non-functional requirements with [CONSTRAINT] tag:

```markdown
## REQ-NF-006: Timeline [CONSTRAINT]
**Source:** Constraints (Section 6)
**Priority:** Critical

Project must complete within 12 weeks.

*[Source: test-project/documents/test-sow.md:Section 6]*
```

### Out of Scope
Document in processed analysis but don't create requirement records. Can reference in decisions:

```markdown
## DEC-002: Implementation Out of Scope
**Source:** Section 2 (Out of Scope)
**Decision:** Implementation and migration execution will be separate engagement

*[Source: test-project/documents/test-sow.md:Section 2]*
```

## Error Prevention

**DO:**
- Assign unique IDs (REQ-F-XXX, etc.)
- Distinguish functional vs non-functional
- Extract ALL deliverables listed
- Capture documented decisions
- Cite every extraction to section
- Use priority levels
- Update all relevant files

**DON'T:**
- Infer requirements not stated
- Skip deliverables
- Create auxiliary files
- Assign duplicate IDs
- Forget citations
- Mix functional and non-functional

## Testing

**Test with:**
- `.claude/agents/dsrag/examples/document-analyzer/test-sow.md`
- Project ID: `test-project`

**Expected output documented in:**
- `.claude/agents/dsrag/examples/document-analyzer/expected-output.md`

## Implementation Notes

1. **ID sequencing:** Always check existing files for highest ID before assigning new
2. **Section parsing:** Look for markdown headers (#, ##, ###) or numbered sections (1., 2., etc.)
3. **Priority inference:** If not stated, use position in document (early = higher priority)
4. **Multiple categories:** A requirement can be both functional and appear in constraints
5. **Deliverable timeline:** Extract due dates/milestones if specified
6. **Decision context:** Include rationale if provided in document
