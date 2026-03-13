# Content Guide

This document defines the format specifications for contributing lenses and delivery templates to DSRAG.

## Lens Agent Template Format

### Required YAML Frontmatter

Every lens agent template must begin with the following YAML frontmatter:

```yaml
---
agent: [lens-name]
type: lens
description: [One-line description]
invoked-by: dsrag-ingest
---
```

### Required Sections

The agent template `.md` file must include all of the following sections:

1. **Internal agent header** — The first line after frontmatter must state: "This is an internal agent template. NOT a user-facing skill."
2. **Title and overview** — Name of the lens and a brief description of what it extracts.
3. **When to use (criteria)** — Conditions under which this lens should be applied (e.g., source type, content characteristics).
4. **Prerequisites** — Any files, tools, or context the lens requires before execution.
5. **Operating principle (two-stage extraction)** — Explain the two-stage process: Stage 1 produces processed analysis, Stage 2 produces structured knowledge.
6. **Required output structure (exact file paths)** — Specify the exact output paths for both stages.
7. **Invocation context** — State that the lens is invoked by `dsrag-ingest` via the Task tool. It does not run independently.
8. **Extraction process (step-by-step)** — Numbered steps describing how to read, identify, classify, and output extracted knowledge.
9. **Citation format** — The strict citation format (see Citation Format Rules below).
10. **Error prevention (DO/DON'T list)** — Explicit list of common mistakes and how to avoid them.
11. **Testing reference** — Pointer to the test data and expected output for this lens.

## Output Directory Conventions

### Stage 1: Processed Analysis

```
.dsrag/[project]/processed/[type]/[lens]_[filename].md
```

This stage contains per-source-file analysis with inline citations.

### Stage 2: Structured Knowledge

```
.dsrag/[project]/knowledge/[domain]/
```

This stage contains consolidated, queryable knowledge files. The structure depends on the lens pattern.

### Common Patterns

**Single file per source** — Used by summaries, VSM, and similar lenses that produce one output per input.

```
knowledge/[domain]/source1_[suffix].md
knowledge/[domain]/source2_[suffix].md
```

**Entity files (upsert)** — Used by stakeholders and similar lenses that maintain one file per entity, updated across multiple sources.

```
knowledge/[domain]/entity1.md
knowledge/[domain]/entity2.md
```

**Categorized + index** — Used by problems and similar lenses that organize extractions by category with a top-level index.

```
knowledge/[domain]/by_category/
knowledge/[domain]/by_priority/
knowledge/[domain]/index.md
```

## Citation Format Rules

All extracted facts must use the following strict citation format:

```markdown
*[Source: [projectid]/[type]/[filename]:[line], [Speaker]: "[quote]"]*
```

Rules:

- Every extracted fact MUST have an inline citation. No exceptions.
- Include speaker attribution for transcripts.
- Include exact line numbers from the source material.
- Quote the exact text from the source. Do not paraphrase within citations.

## Delivery Template Format

### Template Variable Syntax

Delivery templates use the following variable syntax:

- `{{PROJECT_NAME}}` — Replaced with the project name at render time.
- `{{KNOWLEDGE_BASE: path}}` — Replaced with the contents of a knowledge base file at the specified path.
- `{{AI_SYNTHESIS}}...{{/AI_SYNTHESIS}}` — Claude generates content based on the surrounding context and available knowledge.

### Template File Location

```
dsrag/.claude/skills/dsrag-deliver/templates/[framework]/[template-name].md.template
```

## Test Data Requirements

Every new lens must include test data:

- **Test input:** `dsrag/.claude/agents/dsrag/examples/[lens-name]/test-input.txt`
- **Expected output:** `dsrag/.claude/agents/dsrag/examples/[lens-name]/expected-output.md`

Requirements for test data:

- Representative of actual source material the lens will process.
- Contains extractable entities relevant to the lens.
- Varied enough to test edge cases (e.g., ambiguous speakers, overlapping topics, missing context).
- Not too long — 400 to 500 lines maximum.
