# Extraction Lenses

## What Are Lenses

Lenses are specialized extraction agents that analyze the same source from different analytical perspectives simultaneously. Each lens looks for a specific type of knowledge, allowing a single document or transcript to yield multiple layers of structured insight in one pass.

## Built-in Lenses

### Stakeholder Profiling

**Lens ID:** `stakeholder-profiling`

Extracts people, roles, relationships, motivations, pain points, and organizational dynamics from source materials.

**Output:**
- Individual profiles in `knowledge/stakeholders/profiles/[name].md`
- Relationship map in `knowledge/stakeholders/stakeholder_map.md`

**Use for:** Understanding who's who, power dynamics, and decision authority within an organization.

---

### Problem Extraction

**Lens ID:** `problem-extraction`

Extracts issues, pain points, failures, gaps, and waste indicators. Categorizes each problem by type (Process, Technology, Organizational, Data Quality, Skills) and severity (Critical, High, Medium).

**Output:**
- `knowledge/problems/by_category/`
- `knowledge/problems/by_priority/`
- `knowledge/problems/problem_index.md`

**Use for:** Issue tracking, root cause analysis, and prioritization.

---

### Value Stream Mapping

**Lens ID:** `value-stream-mapping`

Extracts processes, workflows, value streams, waste, and improvement opportunities from source materials.

**Output:**
- `knowledge/vsm/[filename]_vsm.md`

**Use for:** Process improvement, efficiency analysis, and workflow optimization.

---

### Transcript Summary

**Lens ID:** `transcript-summary`

Extracts meeting intelligence including executive summary, decisions, action items, and sentiment analysis.

**Output:**
- `knowledge/summaries/[filename]_summary.md`

**Use for:** Meeting follow-up, decision tracking, and action item management.

---

### Document Analyzer

**Lens ID:** `document-analyzer`

Extracts document-specific analysis tailored to the document type, such as SOWs, specifications, and contracts.

**Output:**
- Structured analysis in processed and knowledge directories.

**Use for:** Non-transcript document analysis.

## How Lenses Work

Lenses use a two-stage extraction process. Stage 1 creates a processed analysis file from the raw source. Stage 2 extracts structured knowledge with citations, organizing it into the appropriate knowledge base directories.

## Custom Lenses

You can create custom lenses for project-specific frameworks. See [Extending DSRAG](../extending-dsrag.md) for details on building and registering your own lenses.
