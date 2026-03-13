# Consolidation

## What Consolidation Does

After ingesting multiple sources, consolidation performs cross-source synthesis. It identifies common themes, cross-references information, flags conflicts, and aggregates raw knowledge into versioned reference documents. The result is a unified, deduplicated knowledge base ready for deliverable generation.

## When to Run

Consolidation is **mandatory before generating deliverables**. It is also recommended after ingesting a batch of sources to keep the knowledge base current and internally consistent.

## Usage

```bash
/dsrag-consolidate --project-id my-project
```

## What It Produces

- **Aggregated stakeholder map** -- A unified view of all identified stakeholders, roles, and relationships across sources.
- **Consolidated problem index** -- A deduplicated, prioritized list of all extracted problems.
- **VSM overview** -- A combined view of value streams and process flows.
- **Synthesized themes and patterns** -- Recurring topics and insights that span multiple sources.
- **Conflict flags** -- Explicit markers where sources disagree, enabling informed resolution.

## Cross-Source Synthesis

Consolidation identifies patterns across multiple interviews and documents. It flags where different sources agree or disagree on the same topic, and produces a unified view that preserves the nuance of individual perspectives while surfacing the overall picture. When conflicts are detected, they are flagged rather than silently resolved, so that analysts can make informed decisions.
