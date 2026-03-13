---
name: dsrag-consolidate
description: Aggregate acquired knowledge into versioned, deliverable-ready reference documents with cross-source synthesis. Prerequisite for dsrag-deliver.
---

# DSRAG Consolidate

Aggregate knowledge from the DSRAG knowledge base and working documents into **topic-fragmented reference documents** (single source of truth per subject). Each fragment is independently versioned, and a deliverable composition map defines how fragments assemble into SOW deliverables. Includes cross-source synthesis (theme identification, consistency checks, multi-source validation), Mermaid diagrams, completeness scoring, and a mandatory People Perspective fragment.

> **Note:** As of v4.2, cross-source synthesis (previously `/dsrag-synthesize-knowledge`) is built into this skill. Theme extraction, conflict flagging, and multi-source validation happen automatically during fragment generation.

## When to Use

- Before running `/dsrag-deliver` (mandatory prerequisite)
- After processing new transcripts or documents
- When preparing for deliverable generation
- As part of daily workflow: ingest → consolidate → deliver

## Prerequisites

- Project must be initialized with `dsrag-init-project`
- At least one transcript or document must be processed
- Knowledge base must contain structured extractions

## Usage

```bash
/dsrag-consolidate [project-id]
/dsrag-consolidate [project-id] --category [category]
/dsrag-consolidate [project-id] --all
```

**Parameters:**
- `project_id`: Project identifier (e.g., `my-project`)
- `--category` (optional): Specific fragment to regenerate (e.g., `problems`, `stakeholders`, `architecture`)
- `--all` (default): Regenerate all affected fragments (selective — only those with newer sources)
- `--force` (optional): Regenerate ALL 10 fragments regardless of freshness

## Output Structure

### Two-Layer Architecture

Consolidation uses **topic fragments** (single source of truth per subject) with a **deliverable composition map** that tells `/dsrag-deliver` which fragments to assemble for each deliverable.

**Why:** Avoids content duplication across documents. Each piece of knowledge lives in exactly ONE fragment. Deliverables compose from fragments rather than duplicating content.

```
[project-id]/consolidation/
├── index.md                    # Master index + deliverable composition map
├── version_log.md              # Per-fragment version history
│
├── # Topic Fragments (single source of truth per subject)
├── problems.md                 # v[N] — ALL problems, severity, categories, cross-refs
├── stakeholders.md             # v[N] — ALL stakeholder profiles, dynamics, org structure
├── people_perspective.md       # v[N] — MANDATORY: per-person POV consolidation
├── architecture.md             # v[N] — Current state: systems, tech stack, C4 diagrams
├── processes.md                # v[N] — Value streams, waste (TIMWOODS), bottlenecks
├── capabilities.md             # v[N] — L1-L3 capability map, maturity, problem mapping
├── requirements.md             # v[N] — Functional + non-functional requirements
├── financial.md                # v[N] — TCO, costs, ROI indicators, investment areas
├── roadmap.md                  # v[N] — Future state, gap analysis, phases, migration
├── risks.md                    # v[N] — Risk register, mitigation, recommendations
│
└── archive/                    # Previous fragment versions
    ├── problems_v1_20260211.md
    ├── problems_v2_20260213.md
    └── ...
```

### Deliverable Composition Map (in `index.md`)

Instead of duplicating content into deliverable-aligned documents, the index defines which fragments compose each deliverable:

```markdown
## Deliverable Composition Map

| Deliverable | Primary Fragment | Supporting Fragments | Sections to Pull |
|---|---|---|---|
| DELIV-001 Business Case | problems.md | financial.md, capabilities.md, stakeholders.md | Strategic problems, investment themes, quantified impact |
| DELIV-002 Stakeholder Analysis | stakeholders.md | people_perspective.md | Power/interest grid, org dynamics, change readiness |
| DELIV-003 Current State Architecture | architecture.md | processes.md | C4 diagrams, tech stack, data flows, pain points |
| DELIV-004 Business Capability Catalog | capabilities.md | problems.md | L1-L3 map, maturity assessment, problem-to-capability mapping |
| DELIV-005/006 Platform Requirements & RFI | requirements.md | architecture.md | Prioritized FR/NFR, evaluation criteria, constraints |
| DELIV-007/008 TCO Framework & Budget | financial.md | requirements.md | Cost categories, hidden costs, ROI, budget recommendations |
| DELIV-009/010 Governance & Process Maps | processes.md | stakeholders.md | TIMWOODS, bottleneck inventory, governance gaps |
| DELIV-011/012 Roadmap & Migration | roadmap.md | capabilities.md, requirements.md | Future state, gap analysis, phase recommendations |
| DELIV-013 Change Management | stakeholders.md | people_perspective.md, risks.md | Change readiness, resistance factors, champion ID |
| DELIV-014/015 Risk & Recommendations | risks.md | problems.md, stakeholders.md | Risk register, mitigation strategies, prioritized actions |
```

### Anti-Duplication Rules

**CRITICAL: Every piece of knowledge lives in exactly ONE fragment.**

| Content Type | Canonical Fragment | How Other Fragments Reference It |
|---|---|---|
| Problem statements | `problems.md` | By PROB-XXX ID only (e.g., "See PROB-006 in problems.md") |
| Stakeholder profiles | `stakeholders.md` | By name/role (e.g., "See Alice profile in stakeholders.md") |
| Process descriptions | `processes.md` | By process name (e.g., "See Client Onboarding in processes.md") |
| Architecture diagrams | `architecture.md` | By reference (e.g., "See C2 Container diagram in architecture.md") |
| Requirements | `requirements.md` | By FR-XXX/NFR-XXX ID |
| Risk statements | `risks.md` | By RISK-XXX ID |

**Fragments MAY include:**
- A 1-line summary when referencing content from another fragment (for context)
- Cross-reference links to the canonical fragment

**Fragments MUST NOT include:**
- Full problem descriptions that belong in `problems.md`
- Complete stakeholder profiles that belong in `stakeholders.md`
- Verbatim process flows that belong in `processes.md`

---

## Versioning Strategy

### Per-Fragment Independent Versioning

Each fragment has its OWN version number, incremented only when that fragment's content changes. This means:
- If a new transcript only affects `problems.md` and `stakeholders.md`, only those two fragments get new versions
- Other fragments retain their current version (status: "Unchanged" in the run log)
- This prevents unnecessary regeneration and makes change tracking precise

### Rules

1. **First run:** Creates `[fragment].md` as `v1`. No archive copy needed.
2. **Subsequent runs — fragment affected by new knowledge:**
   - Move current version to `archive/[fragment]_v[N]_[YYYYMMDD].md`
   - Generate new version as `[fragment].md` (always the latest)
   - Increment version in the fragment header
3. **Subsequent runs — fragment NOT affected:**
   - Skip regeneration. Keep existing file as-is.
   - Report as "Unchanged" in the run log.
4. **Determining which fragments are affected:**
   - Compare knowledge base files (by modification date) against the fragment's `Generated` timestamp
   - If any source file for a fragment is newer than the fragment, regenerate it
   - `--force` flag: Regenerate all fragments regardless
5. **Version log:** Append entry to `version_log.md` with per-fragment detail

### Fragment Header (Required)

Every fragment must include:

```markdown
# [Fragment Title]
**Project:** [project_id]
**Version:** v[N]
**Generated:** [YYYY-MM-DD HH:MM]
**Previous Version:** v[N-1] ([date]) → archived at `archive/[fragment]_v[N-1]_[date].md`
**Sources:** [count] knowledge files, [count] working documents
**Used by:** [DELIV-XXX list] (via composition map)
**Completeness:** [XX]% [GREEN/YELLOW/RED]
```

### Version Log Format (`version_log.md`)

```markdown
# Consolidation Version Log
**Project:** [project_id]

| Run | Date | Fragments Updated | Fragments Unchanged | Trigger | Key Changes |
|-----|------|-------------------|---------------------|---------|-------------|
| 3 | 2026-02-13 | problems(v4), stakeholders(v3) | 8 of 10 | New transcript (02122026-*) | Added interview data, 2 new PROB-XXX |
| 2 | 2026-02-11 | all 10 (v2) | 0 | Full regeneration (--force) | Complete rebuild with Mermaid diagrams |
| 1 | 2026-02-11 | all 10 (v1) | 0 | First run | Baseline generation |
```

---

## Visualization Standards

### MANDATORY: Mermaid Only

**All diagrams and illustrations MUST use Mermaid syntax.** No ASCII art permitted.

### Mermaid Styling: Muted Material Color Palette

Apply this consistent theme across all Mermaid diagrams:

```markdown
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#90A4AE',
  'primaryTextColor': '#263238',
  'primaryBorderColor': '#546E7A',
  'secondaryColor': '#B0BEC5',
  'tertiaryColor': '#CFD8DC',
  'lineColor': '#78909C',
  'textColor': '#37474F',
  'fontSize': '14px',
  'nodeBorder': '#546E7A',
  'mainBkg': '#ECEFF1',
  'clusterBkg': '#F5F5F5',
  'clusterBorder': '#B0BEC5'
}}}%%
```

### Color Assignments by Meaning

Use these style classes consistently:

```
classDef critical fill:#EF9A9A,stroke:#C62828,color:#B71C1C
classDef high fill:#FFCC80,stroke:#E65100,color:#BF360C
classDef medium fill:#FFF59D,stroke:#F9A825,color:#F57F17
classDef low fill:#A5D6A7,stroke:#2E7D32,color:#1B5E20
classDef neutral fill:#B0BEC5,stroke:#546E7A,color:#263238
classDef active fill:#81D4FA,stroke:#0277BD,color:#01579B
classDef legacy fill:#CE93D8,stroke:#6A1B9A,color:#4A148C
classDef external fill:#FFAB91,stroke:#BF360C,color:#3E2723
```

### Required Diagram Types

Each consolidation document should include at minimum:
- **Architecture docs:** C4 context/container diagrams (graph TD)
- **Process docs:** Flowcharts or sequence diagrams (graph LR or sequenceDiagram)
- **Stakeholder docs:** Quadrant charts or mindmaps
- **Risk docs:** Risk matrices (quadrantChart)
- **Capability docs:** Heat maps (graph TD with color classes)
- **People Perspective:** Relationship/influence diagrams (graph TD)

---

## People Perspective Document (MANDATORY)

### Purpose

A deliverable-independent consolidation of **every individual's point of view**. This is NOT a stakeholder analysis for a deliverable — it is a true consolidation of everything each person has said, their problems, their aspirations, their concerns, and their relationships.

### When Generated

**Always.** Every run of `/dsrag-consolidate` must generate or update the People Perspective document. It is not optional and not tied to any specific DELIV-XXX.

### Sources

- `.dsrag/[pid]/knowledge/stakeholders/profiles/` — All individual profiles
- `.dsrag/[pid]/knowledge/stakeholders/stakeholder_map.md` — Relationship map
- `.dsrag/[pid]/processed/transcripts/*_stakeholder_analysis.md` — All stakeholder analyses
- `.dsrag/[pid]/knowledge/summaries/` — Meeting summaries (for who said what)
- `.dsrag/[pid]/knowledge/problems/problem_index.md` — Problems attributed to individuals

### Content Structure

```markdown
# People Perspective Reference
**Project:** [project_id]
**Version:** v[N]
**Generated:** [timestamp]
**Completeness:** [XX]%
**Individuals Profiled:** [count]

## How to Read This Document
This document consolidates every individual's expressed views, concerns,
and problem statements from all processed transcripts. It is organized
per-person, not per-deliverable. Use this to understand "what does [person]
actually think and want?"

## Stakeholder Landscape
[Mermaid diagram: influence/relationship map showing all stakeholders and connections]

## Individual Perspectives

### [Person Name] — [Role/Title]
**Interviews/Meetings Referenced:** [list of transcript sources]
**Overall Stance:** [1-2 sentence summary of their position]

#### Their Problem Statements
[Problems this person has explicitly raised, with citations]

#### Their Aspirations & Vision
[What they want the future to look like]

#### Their Concerns & Fears
[What they're worried about — stated or inferred]

#### Their Constraints
[What limits their ability to act]

#### Key Quotes
[Top 5 most revealing quotes from this person]

#### Relationships & Dynamics
[How they relate to other stakeholders — allies, tensions, dependencies]

#### Platform/Technology Preferences
[Any stated preferences with rationale]

#### Credibility Assessment
[How reliable is this person's information? Any known biases?]

---
[Repeat for each individual]
---

## Cross-Cutting Themes
[Themes that emerge across multiple people]

### Areas of Agreement
[What most/all stakeholders agree on]

### Areas of Conflict
[Where stakeholders fundamentally disagree]
[Mermaid diagram: conflict map showing disagreement axes]

### Information Asymmetry
[What some people know that others don't]

### Power Dynamics
[Mermaid diagram: power/influence quadrant chart]

## Completeness Assessment
[Per-person completeness — who do we know well vs. who is still opaque]

## Missing Perspectives
[People we haven't interviewed or have insufficient data on]
```

---

## Topic Fragment Definitions (10 Fragments)

Each fragment is the **single source of truth** for its subject. Fragments are topic-aligned, not deliverable-aligned. The Deliverable Composition Map in `index.md` defines which fragments compose each deliverable.

### 1. Problems Fragment (`problems.md`)
**Owns:** ALL problem statements, severity, categories, root causes, impact
**Used by:** DELIV-001, DELIV-004, DELIV-014/015 (via composition map)
**Sources:**
- `.dsrag/[pid]/knowledge/problems/` — All problem files (index, by_priority/*, by_category/*)
- `working_folder/problem_reconciliation_analysis.md` — Reconciled problem statements
- `[pid]/deliverables/Current_State_Value_Stream_Strategic_Problems.md` — Strategic problems
- `[pid]/deliverables/Strategic_Problems_Executive_Summary.md` — Executive summary

**Content structure:**
```markdown
# Problems
## Summary Statistics
[Mermaid severity distribution chart + category breakdown]
## Top Strategic Problems (Ranked by Business Impact)
## All Problems by Category
### Process Problems
### Technology Problems
### Organizational Problems
### Data Quality Problems
### Skills Problems
## Problem-to-Capability Mapping (summary IDs only — detail in capabilities.md)
## Problem-to-Stakeholder Attribution (summary — detail in stakeholders.md)
## Completeness Assessment
## Missing Information
```

**Anti-duplication:** Other fragments reference by `PROB-XXX` ID + 1-line summary only.

### 2. Stakeholders Fragment (`stakeholders.md`)
**Owns:** ALL stakeholder profiles, org structure, power dynamics, change readiness
**Used by:** DELIV-002, DELIV-013, DELIV-009 (via composition map)
**Sources:**
- `.dsrag/[pid]/knowledge/stakeholders/profiles/` — All profiles
- `.dsrag/[pid]/knowledge/stakeholders/stakeholder_map.md` — Relationship map
- `.dsrag/[pid]/knowledge/problems/by_category/organizational_problems.md`
- `.dsrag/[pid]/knowledge/problems/by_category/skills_problems.md`
- `working_folder/stakeholder_interviews/` — Interview analyses

**Content structure:**
```markdown
# Stakeholders
## Stakeholder Landscape
[Mermaid power/interest quadrant chart]
## Key Decision Makers
## Organizational Dynamics & Team Structure
## Skills Gaps
## Change Readiness Assessment
## Resistance Factors & Champions
## Key Quotes by Stakeholder (top 3 per person)
## Completeness Assessment
## Missing Information
```

**Anti-duplication:** Other fragments reference by name/role only. Full profiles live here.

### 3. People Perspective Fragment (`people_perspective.md`)
**Owns:** Per-person consolidated POV — what each individual thinks, wants, fears
**Used by:** DELIV-002, DELIV-013 (via composition map)
**See:** [People Perspective Document (MANDATORY)](#people-perspective-document-mandatory) section above for full specification.

### 4. Architecture Fragment (`architecture.md`)
**Owns:** Current state systems, tech stack, C4 diagrams, data flows, technical debt
**Used by:** DELIV-003, DELIV-005/006 (via composition map)
**Sources:**
- `.dsrag/[pid]/knowledge/value_streams/current_state.md` — Process flows
- `.dsrag/[pid]/knowledge/problems/by_category/technology_problems.md` — Referenced by PROB-XXX
- `.dsrag/[pid]/knowledge/problems/by_category/data_quality_problems.md` — Referenced by PROB-XXX
- `.dsrag/[pid]/knowledge/requirements/` — Referenced by FR/NFR-XXX
- `working_folder/architecture_strategy/` — Architecture documents
- `working_folder/process_maps/` — Process maps

**Content structure:**
```markdown
# Architecture (Current State)
## System Landscape (C1 Context)
[Mermaid C4 context diagram]
## Container Architecture (C2)
[Mermaid C4 container diagram]
## Data Flow & Integration Points
[Mermaid sequence/flow diagram]
## Technology Stack
## Technical Debt Inventory
## Key Technology Problems (PROB-XXX references — detail in problems.md)
## Data Quality Issues (PROB-XXX references — detail in problems.md)
## Completeness Assessment
## Missing Information
```

**Anti-duplication:** References problems by PROB-XXX ID. Does NOT duplicate problem descriptions from `problems.md`.

### 5. Processes Fragment (`processes.md`)
**Owns:** Value streams, waste (TIMWOODS), bottlenecks, lead times, process maps
**Used by:** DELIV-009, DELIV-010, DELIV-003 (via composition map)
**Sources:**
- `.dsrag/[pid]/knowledge/value_streams/` — All VSM files (current_state, waste_analysis, future_state, gap_analysis)
- `working_folder/process_maps/` — BPMN diagrams
- `.dsrag/[pid]/knowledge/problems/by_category/process_problems.md` — Referenced by PROB-XXX

**Content structure:**
```markdown
# Processes & Value Streams
## Business Process Maps
[Mermaid flowchart/sequence diagrams]
## Value Stream Current State
[Mermaid value stream flow]
## TIMWOODS Waste Analysis
## Lead Time Analysis
## Bottleneck Inventory
## Data Governance Gaps
## Process Problems (PROB-XXX references — detail in problems.md)
## Process Improvement Opportunities
## Completeness Assessment
## Missing Information
```

**Anti-duplication:** Owns process descriptions and waste analysis. References problems by PROB-XXX. References stakeholders by name only.

### 6. Capabilities Fragment (`capabilities.md`)
**Owns:** L1-L3 capability map, maturity assessment, problem-to-capability mapping
**Used by:** DELIV-004, DELIV-001, DELIV-011/012 (via composition map)
**Sources:**
- `[pid]/deliverables/CAPABILITY_CATALOG_V2.md` — L1-L3 capability map
- `.dsrag/[pid]/knowledge/problems/` — Referenced by PROB-XXX
- `working_folder/problem_to_capability_impact_map.md`

**Content structure:**
```markdown
# Business Capabilities
## L1 Capabilities Overview
[Mermaid capability tree diagram]
## L2-L3 Capability Detail
## Problem-to-Capability Impact Map
[Mermaid heat map: capabilities × PROB-XXX severity, using color classes]
## Capability Maturity Assessment
## Priority Capabilities for Investment
## Completeness Assessment
## Missing Information
```

**Anti-duplication:** Maps PROB-XXX IDs to capabilities but does NOT include full problem descriptions. References requirements by FR/NFR-XXX.

### 7. Requirements Fragment (`requirements.md`)
**Owns:** ALL functional + non-functional requirements, RFI criteria, constraints
**Used by:** DELIV-005, DELIV-006, DELIV-011/012 (via composition map)
**Sources:**
- `.dsrag/[pid]/knowledge/requirements/functional_requirements.md`
- `.dsrag/[pid]/knowledge/requirements/non_functional_requirements.md`
- `.dsrag/[pid]/knowledge/value_streams/future_state.md` — Future state needs
- `working_folder/architecture_strategy/` — Architecture decisions

**Content structure:**
```markdown
# Requirements
## Functional Requirements (Prioritized)
## Non-Functional Requirements (Prioritized)
## RFI Evaluation Criteria (Draft)
## Platform Capability Mapping
[Mermaid comparison diagram]
## Integration Requirements
[Mermaid integration flow diagram]
## Data Requirements
## Key Constraints
## Completeness Assessment
## Missing Information
```

**Anti-duplication:** Owns requirement definitions (FR-XXX, NFR-XXX). Other fragments reference by ID only.

### 8. Financial Fragment (`financial.md`)
**Owns:** TCO analysis, cost categories, hidden costs, ROI indicators, budget themes
**Used by:** DELIV-007, DELIV-008, DELIV-001 (via composition map)
**Sources:**
- `.dsrag/[pid]/knowledge/summaries/` — TCO-related meeting summaries
- `.dsrag/[pid]/knowledge/value_streams/gap_analysis.md` — Quantified gaps
- `.dsrag/[pid]/knowledge/decisions/documented_decisions.md`

**Content structure:**
```markdown
# Financial & TCO
## Cost Categories Identified
[Mermaid cost breakdown diagram]
## Current State Cost Drivers
## Hidden Costs (Operational, Skills, Migration)
## Investment Areas
## ROI Indicators
## Budget Discussion Points
## Financial Decision Log
## Completeness Assessment
## Missing Information
```

**Anti-duplication:** Owns financial data. References problems by PROB-XXX when discussing cost impact. Does NOT duplicate problem descriptions.

### 9. Roadmap Fragment (`roadmap.md`)
**Owns:** Future state vision, gap analysis, phases, migration considerations, dependencies
**Used by:** DELIV-011, DELIV-012, DELIV-001 (via composition map)
**Sources:**
- `.dsrag/[pid]/knowledge/value_streams/future_state.md`
- `.dsrag/[pid]/knowledge/value_streams/gap_analysis.md`
- `.dsrag/[pid]/knowledge/decisions/documented_decisions.md`
- `.dsrag/[pid]/knowledge/requirements/` — Referenced by FR/NFR-XXX

**Content structure:**
```markdown
# Roadmap & Future State
## Future State Vision
[Mermaid target architecture diagram]
## Gap Analysis (Current → Future)
## Quick Wins Identified
## Phase Recommendations
[Mermaid Gantt chart or timeline]
## Migration Considerations
## Dependency Map
[Mermaid dependency graph]
## Completeness Assessment
## Missing Information
```

**Anti-duplication:** References requirements by FR/NFR-XXX. References problems by PROB-XXX. References capabilities by name. Does NOT duplicate content from those fragments.

### 10. Risks Fragment (`risks.md`)
**Owns:** Risk register (RISK-XXX), mitigation strategies, recommendations
**Used by:** DELIV-014, DELIV-015, DELIV-013 (via composition map)
**Sources:**
- `.dsrag/[pid]/knowledge/problems/by_priority/critical.md` — Referenced by PROB-XXX
- `.dsrag/[pid]/knowledge/problems/by_priority/high.md` — Referenced by PROB-XXX
- `.dsrag/[pid]/knowledge/value_streams/waste_analysis.md`
- `.dsrag/[pid]/knowledge/stakeholders/stakeholder_map.md`
- `.dsrag/[pid]/knowledge/decisions/documented_decisions.md`

**Content structure:**
```markdown
# Risks & Recommendations
## Risk Register
[Mermaid risk matrix quadrant chart]
### Critical Risks (RISK-001, RISK-002, ...)
### High Risks
### Medium Risks
## Organizational Risks
## Technical Risks
## Process Risks
## Risk Mitigation Strategies
## Top Recommendations (Prioritized)
## Quick Wins vs Strategic Investments
[Mermaid effort/impact quadrant]
## Completeness Assessment
## Missing Information
```

**Anti-duplication:** Derives risks FROM problems but owns RISK-XXX statements independently. References source problems by PROB-XXX. Does NOT duplicate problem descriptions.

---

## Execution Process

### Step 1: Validate inputs

Check:
- Project exists at `.dsrag/[project_id]/`
- Knowledge base has content (at least one knowledge directory has files)
- Consolidation output directory exists or can be created at `[project-id]/consolidation/`
- Check for existing consolidation documents (for versioning)

### Step 2: Inventory available knowledge

Scan all knowledge sources and create an inventory:
```markdown
Knowledge Inventory:
- Value Streams: [X] files, [Y] total lines
- Problems: [X] files, [Y] total lines
- Stakeholders: [X] profiles, [Y] total lines
- Summaries: [X] summaries, [Y] total lines
- Requirements: [X] files, [Y] total lines
- Decisions: [X] files, [Y] total lines
- Working Folder: [X] documents
- Existing Deliverables: [X] documents
```

### Step 3: Determine versioning

For each document to be generated:
1. Check if `[project-id]/consolidation/[document].md` exists
2. If yes: read version header, determine next version number
3. Archive existing version to `[project-id]/consolidation/archive/[document]_v[N]_[YYYYMMDD].md`
4. If no: this will be v1

### Step 4: Create consolidation directory and snapshot knowledge artifacts

```bash
mkdir -p [project-id]/consolidation
mkdir -p [project-id]/consolidation/archive
```

**MANDATORY: The `problems.md` fragment serves as the canonical problem inventory.**

The problems fragment is the **single source of truth** for all PROB-XXX statements. Other fragments reference problems by ID only. The purposes:

1. **Self-contained reference** — all PROB-XXX IDs resolve within `problems.md`; no need to scan the raw knowledge base
2. **Audit trail** — when versioned and archived, shows how the problem landscape evolved between consolidation runs
3. **Deduplication** — the knowledge base accumulates problems per-transcript which may overlap; `problems.md` is the deduplicated, authoritative list

The problems fragment agent (Agent 1 in Step 5) handles this automatically. It reads all files in `.dsrag/[pid]/knowledge/problems/` and produces a clean, organized, deduplicated fragment with cross-references.

### Step 5: Launch parallel agents for fragment generation

**MANDATORY: Use Task tool to generate fragments in parallel.**

Each topic fragment is independent and MUST be generated concurrently:

```
Launch 10 parallel Task agents (one per fragment):
  Agent 1:  problems.md      — ALL problems, deduplicated, with PROB-XXX IDs
  Agent 2:  stakeholders.md  — ALL stakeholder profiles, org structure, dynamics
  Agent 3:  people_perspective.md — MANDATORY: per-person POV consolidation
  Agent 4:  architecture.md  — Current state systems, C4 diagrams, tech stack
  Agent 5:  processes.md     — Value streams, TIMWOODS waste, bottlenecks
  Agent 6:  capabilities.md  — L1-L3 map, maturity, problem-capability mapping
  Agent 7:  requirements.md  — FR + NFR, RFI criteria, constraints
  Agent 8:  financial.md     — TCO, costs, ROI, budget themes
  Agent 9:  roadmap.md       — Future state, gaps, phases, migration
  Agent 10: risks.md         — Risk register (RISK-XXX), mitigation, recommendations
```

Each agent receives:
- The source file list for its fragment (see Topic Fragment Definitions)
- The version number to use
- The Mermaid styling standards (see Visualization Standards)
- The content structure template for its fragment
- The anti-duplication rules: what it OWNS vs. what it REFERENCES by ID
- Instructions to write directly to `[project-id]/consolidation/[fragment].md`

**If `--category` specified:** Only launch the relevant agent(s). The `problems.md` and `people_perspective.md` agents always run (they are referenced by most other fragments).

### Fragment Agent Anti-Duplication Instructions

Every fragment agent MUST be given these rules in its prompt:

```
ANTI-DUPLICATION RULES:
1. You OWN [list of content types for this fragment]. Write full detail for these.
2. You REFERENCE [list of content from other fragments]. Use ID + 1-line summary ONLY.
   Example: "PROB-006: Claims sitting idle for 9 months (see problems.md for detail)"
3. NEVER copy full problem descriptions, stakeholder profiles, or process flows
   that belong to another fragment.
4. Cross-reference format: "(see [fragment_name].md)" or "(PROB-XXX in problems.md)"
```

### Step 5.1: Agent instructions for each fragment

Each parallel agent must:

**5.1.1 Read all source files for this fragment**
- Read knowledge base files listed in the fragment's Sources (sample if >2000 lines)
- Read working folder documents relevant to this topic
- Read existing deliverables for context

**5.1.2 Synthesize into topic fragment**
- Include fragment header (see Versioning Strategy → Fragment Header)
- Extract key themes, findings, and insights **for this topic only**
- Preserve critical citations (top 10-20 most impactful quotes per section)
- Cross-reference other fragments by ID only (PROB-XXX, FR-XXX, RISK-XXX) — do NOT duplicate their content
- Flag contradictions or inconsistencies
- Quantify where possible
- **Use Mermaid diagrams** with the standard material palette (no ASCII art)

**5.1.3 Assess completeness**
For each section, rate:
- **GREEN** (80%+): Sufficient information for deliverable generation
- **YELLOW** (40-79%): Partial information, deliverable possible but gaps exist
- **RED** (<40%): Critical gaps, additional data collection needed

Calculate overall fragment completeness as weighted average of section scores.

**5.1.4 Identify missing information**
List specific data points, interviews, or documents still needed for this topic.

### Step 6: Generate master index and version log

After all agents complete, create/update `[project-id]/consolidation/index.md`:

```markdown
# Consolidation Index

**Project:** [project_id]
**Consolidation Run:** #[N]
**Generated:** [timestamp]
**Knowledge Sources:** [count] transcripts, [count] documents, [total] knowledge files

## Topic Fragments

| # | Fragment | Version | Completeness | Status |
|---|----------|---------|--------------|--------|
| 1 | problems.md | v[N] | [XX]% [COLOR] | [New/Updated/Unchanged] |
| 2 | stakeholders.md | v[N] | [XX]% [COLOR] | [New/Updated/Unchanged] |
| 3 | people_perspective.md | v[N] | [XX]% [COLOR] | [New/Updated/Unchanged] |
| 4 | architecture.md | v[N] | [XX]% [COLOR] | [New/Updated/Unchanged] |
| 5 | processes.md | v[N] | [XX]% [COLOR] | [New/Updated/Unchanged] |
| 6 | capabilities.md | v[N] | [XX]% [COLOR] | [New/Updated/Unchanged] |
| 7 | requirements.md | v[N] | [XX]% [COLOR] | [New/Updated/Unchanged] |
| 8 | financial.md | v[N] | [XX]% [COLOR] | [New/Updated/Unchanged] |
| 9 | roadmap.md | v[N] | [XX]% [COLOR] | [New/Updated/Unchanged] |
| 10 | risks.md | v[N] | [XX]% [COLOR] | [New/Updated/Unchanged] |

## Deliverable Composition Map

| Deliverable | Primary Fragment | Supporting Fragments |
|---|---|---|
| DELIV-001 Business Case | problems.md | financial.md, capabilities.md, stakeholders.md |
| DELIV-002 Stakeholder Analysis | stakeholders.md | people_perspective.md |
| DELIV-003 Current State Architecture | architecture.md | processes.md |
| DELIV-004 Business Capability Catalog | capabilities.md | problems.md |
| DELIV-005/006 Platform Req & RFI | requirements.md | architecture.md |
| DELIV-007/008 TCO & Budget | financial.md | requirements.md |
| DELIV-009/010 Governance & Process | processes.md | stakeholders.md |
| DELIV-011/012 Roadmap & Migration | roadmap.md | capabilities.md, requirements.md |
| DELIV-013 Change Management | stakeholders.md | people_perspective.md, risks.md |
| DELIV-014/015 Risk & Recommendations | risks.md | problems.md, stakeholders.md |

## Overall Readiness: [X]% ([Y] of 10 fragments GREEN)

## Key Insights from This Consolidation
1. [Insight 1 — most significant finding or change since last run]
2. [Insight 2]
3. [Insight 3]

## Critical Gaps (Blocking Deliverable Generation)
- [Gap 1] — blocks [DELIV-XXX]
- [Gap 2] — blocks [DELIV-XXX]

## Recommended Next Steps
1. [Action 1]
2. [Action 2]
3. [Action 3]
```

Update `[project-id]/consolidation/version_log.md` with the run entry.

**IMPORTANT:** Fragments have independent version numbers. If only `problems.md` and `risks.md` changed in this run, only those get version increments. Others retain their current version with status "Unchanged".

### Step 7: Report completion

Display to user:

```markdown
## Consolidation Complete: [project_id]

**Run:** #[N] | **Date:** [timestamp]

### Fragment Status

| Fragment | Version | Completeness | Status |
|----------|---------|-------------|--------|
| problems.md | v[N] | [XX]% [COLOR] | [Created/Updated/Unchanged] |
| stakeholders.md | v[N] | [XX]% [COLOR] | [Created/Updated/Unchanged] |
| people_perspective.md | v[N] | [XX]% [COLOR] | [Created/Updated/Unchanged] |
| architecture.md | v[N] | [XX]% [COLOR] | [Created/Updated/Unchanged] |
| processes.md | v[N] | [XX]% [COLOR] | [Created/Updated/Unchanged] |
| capabilities.md | v[N] | [XX]% [COLOR] | [Created/Updated/Unchanged] |
| requirements.md | v[N] | [XX]% [COLOR] | [Created/Updated/Unchanged] |
| financial.md | v[N] | [XX]% [COLOR] | [Created/Updated/Unchanged] |
| roadmap.md | v[N] | [XX]% [COLOR] | [Created/Updated/Unchanged] |
| risks.md | v[N] | [XX]% [COLOR] | [Created/Updated/Unchanged] |

**Fragments regenerated:** [X] of 10 | **Unchanged:** [Y] of 10

### Overall Project Readiness: [XX]%
- GREEN: [count] fragments ready for deliverable generation
- YELLOW: [count] fragments have gaps
- RED: [count] fragments need additional data collection

### Key Insights
1. [Most important insight]
2. [Second insight]
3. [Third insight]

### What Changed (vs. Previous Run)
- [Delta 1]
- [Delta 2]

### Output Location
`[project-id]/consolidation/`

### Next Steps
- Run `/dsrag-deliver` for deliverables where all required fragments are GREEN
- Address RED fragment gaps before generating dependent deliverables
- See composition map in `index.md` for fragment → deliverable mapping
```

---

## Upsert Behavior (Per-Fragment Intelligent Regeneration)

When consolidation fragments already exist:

### Fragment-Level Freshness Check

For each fragment independently:
1. **Read existing fragment** header to get `Generated` timestamp
2. **Check source files** for that fragment (see Topic Fragment Definitions → Sources)
3. **Compare timestamps:** Are any source files newer than the fragment's `Generated` date?
4. **Decision:**
   - **No newer sources:** Skip this fragment. Report as "Unchanged" in run log.
   - **Newer sources exist:** Archive current version, regenerate, increment version.
   - **`--force` flag:** Regenerate regardless of freshness.

### Selective Regeneration Example

```
Run #3 — 2 new transcripts added since last consolidation

Fragment freshness check:
  problems.md:          Sources NEWER → Regenerate (v2 → v3)
  stakeholders.md:      Sources NEWER → Regenerate (v2 → v3)
  people_perspective.md: Sources NEWER → Regenerate (v2 → v3)
  architecture.md:      No changes   → Skip (stays v2)
  processes.md:         Sources NEWER → Regenerate (v2 → v3)
  capabilities.md:      No changes   → Skip (stays v2)
  requirements.md:      No changes   → Skip (stays v2)
  financial.md:         No changes   → Skip (stays v2)
  roadmap.md:           No changes   → Skip (stays v2)
  risks.md:             Sources NEWER → Regenerate (v2 → v3)

Result: 5 fragments regenerated, 5 unchanged
Agents launched: 5 (not 10) — saves time and cost
```

### Manual Edit Preservation

Fragments MAY contain manual edits marked with `<!-- MANUAL -->` tags:
```markdown
<!-- MANUAL -->
**Note:** Per client discussion on 02/10, the actual onboarding time
is closer to 8 months, not 3-6 months as stated in transcripts.
<!-- /MANUAL -->
```

When regenerating a fragment, **carry forward all `<!-- MANUAL -->` blocks** into the new version unchanged.

---

## Large File Handling

Knowledge files can be very large (5000+ lines). Strategy:
- **For files >2000 lines:** Read in sections, extract key themes and top citations
- **For stakeholder profiles:** Read all profiles but summarize each to key attributes
- **For problem registries:** Group by category/priority, extract top items per group
- **For VSM files:** Extract process flow summary, top bottlenecks, quantified metrics

---

## Integration with /dsrag-deliver

When `/dsrag-deliver` is invoked for a specific deliverable (e.g., DELIV-001):

1. **Read `[project-id]/consolidation/index.md`** to get the Deliverable Composition Map
2. **Look up the target deliverable** to find its primary + supporting fragments
3. **Check fragment freshness** — if any required fragment is stale (>24h or sources changed), re-run `/dsrag-consolidate [project-id] --category [affected-fragments]`
4. **If no consolidation folder exists:** Run `/dsrag-consolidate [project-id]` first
5. **Assemble deliverable** by reading the primary fragment in full + relevant sections from supporting fragments

**Example:** Generating DELIV-001 (Business Case):
- Read `problems.md` (primary) — full document
- Read `financial.md` (supporting) — investment themes, ROI indicators sections
- Read `capabilities.md` (supporting) — priority capabilities section
- Read `stakeholders.md` (supporting) — key quotes, champion identification
- Compose into the business case deliverable template

This means `/dsrag-deliver` reads from topic fragments in `[project-id]/consolidation/` and never duplicates content — it composes from single-source-of-truth fragments.

---

## Error Handling

### No knowledge found
```
Error: Knowledge base is empty for project '[project_id]'

Process transcripts first:
  /dsrag-ingest [project_id]
```

### Partial knowledge
```
Warning: Some knowledge categories are empty

Available:
  - value_streams: 4 files
  - problems: 10 files

Missing:
  - requirements: No files found
  - decisions: No files found

Proceeding with available knowledge...
```

---

## Performance Notes

- **First run:** 5-15 minutes depending on knowledge base size (10 parallel agents)
- **Subsequent runs:** Faster due to selective regeneration — only affected fragments are regenerated (e.g., 3 of 10 fragments → 3 agents, not 10)
- **Large knowledge bases (>50K lines):** Uses sampling strategy for very large files
- **Parallel execution:** Affected fragments generated concurrently via Task agents
- **Cost savings:** Selective regeneration reduces token usage by 50-70% on incremental runs

---

## Daily Workflow Integration

```
Morning workflow (recommended):
1. /dsrag-ingest my-project --consolidate    # Ingest + consolidate in one command

Or step by step:
1. /dsrag-ingest my-project                   # Auto-discover and ingest new files
2. /dsrag-consolidate my-project                         # Aggregate knowledge (parallel)
3. /dsrag-deliver my-project business-case               # Generate outputs

The consolidation step ensures deliverables always reflect the latest knowledge
without re-scanning the entire (potentially 50K+ line) knowledge base each time.
```

---

## Related Skills

- `dsrag-ingest` — Unified ingestion command (primary upstream entry point)
- ~~`dsrag-synthesize-knowledge`~~ — Deprecated in v4.2; synthesis is now built into this skill
- `dsrag-deliver` — Generates deliverables from consolidation documents (downstream)

**Agent templates** (in `.claude/agents/dsrag/`, used internally by `dsrag-ingest`):
- `stakeholder-profiling.md`, `problem-extraction.md`, `value-stream-mapping.md`, `transcript-summary.md`, `document-analyzer.md` — Lens agents

---

## Testing

**Test with:**
1. Ensure `my-project` project has processed transcripts
2. Run: `/dsrag-consolidate my-project`
3. Verify 10 topic fragments + index.md + version_log.md created in `my-project/consolidation/`
4. Verify all diagrams are Mermaid (no ASCII art)
5. Check completeness scores are reasonable
6. Verify `people_perspective.md` has per-person sections
7. **Anti-duplication check:** Verify PROB-XXX descriptions only appear in `problems.md`, other fragments reference by ID only
8. **Cross-reference check:** Verify `index.md` has a complete Deliverable Composition Map
9. Run again to test selective versioning — only add 1 new transcript, verify only affected fragments regenerated (not all 10)
10. Run: `/dsrag-deliver my-project --framework consulting --template business-case`
11. Verify deliver reads primary fragment (`problems.md`) + supporting fragments from composition map
