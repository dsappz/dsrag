# Extending DSRAG

How to add new extraction lenses and delivery templates.

## Overview

DSRAG's extensibility comes from the lens pattern. Each lens is an internal agent template that extracts a specific type of knowledge from source material. Lenses are NOT user-facing — they are invoked by the `/dsrag-ingest` orchestrator via the Task tool.

This guide walks through adding a new lens end-to-end, then covers adding delivery templates.

## Adding a New Extraction Lens

### Step 1: Create the Agent Template File

```bash
touch dsrag/.claude/agents/dsrag/custom/[lens-name].md
mkdir -p dsrag/.claude/agents/dsrag/examples/[lens-name]
```

Use kebab-case for the lens name (e.g., `decision-tracking`, `risk-identification`, `togaf-architecture`).

### Step 2: Write the Template

Structure the template according to the format defined in [content-guide.md](content-guide.md). At minimum, the file must include:

- YAML frontmatter with `agent`, `type`, `description`, and `invoked-by` fields.
- The internal agent header stating it is not user-facing.
- A complete extraction process with numbered steps.
- The strict citation format.
- Exact output file paths for both Stage 1 (processed) and Stage 2 (knowledge).
- A DO/DON'T error prevention list.

### Step 3: Define Knowledge Base Structure

Design the output structure for the `knowledge/` directory. Consider:

- **Discoverability** — Can users and delivery templates find the extracted knowledge by browsing the directory tree?
- **Queryability** — Is the structure suitable for Grep and Read operations during delivery?
- **Consistency** — Does the structure follow the same conventions as existing lenses (single-file, entity, or categorized patterns)?
- **Scalability** — Will the structure remain manageable as more sources are ingested?

### Step 4: Create Test Data and Expected Output

Create two files:

- `dsrag/.claude/agents/dsrag/examples/[lens-name]/test-input.txt` — A representative transcript or source document.
- `dsrag/.claude/agents/dsrag/examples/[lens-name]/expected-output.md` — The ideal extraction result from processing the test input.

See [content-guide.md](content-guide.md) for test data requirements.

### Step 5: Register in the Ingestion Orchestrator

Edit `dsrag/.claude/skills/dsrag-ingest/SKILL.md` to register the new lens:

1. Add a `Read` step for the new agent template file.
2. Add a `Task` launch alongside existing lenses in the parallel extraction section.
3. Update the lens count and performance estimates in the skill documentation.

## Example: Adding a TOGAF Architecture Lens

This walkthrough shows the complete process for adding a lens that extracts TOGAF architecture building blocks.

### Create the Agent Template

Create `dsrag/.claude/agents/dsrag/custom/togaf-architecture.md`:

```markdown
---
agent: togaf-architecture
type: lens
description: Extract TOGAF architecture building blocks (ABBs, SBBs, capabilities, gaps)
invoked-by: dsrag-ingest
---

# DSRAG TOGAF Architecture Extraction

This is an internal agent template. NOT a user-facing skill.

Extract architecture building blocks from transcripts using TOGAF ADM categories.

## Required Output Structure

**Stage 1: Processed Analysis**
- File: `.dsrag/[projectid]/processed/transcripts/togaf_[filename].md`

**Stage 2: Structured Knowledge:**
.dsrag/[projectid]/knowledge/architecture/
├── building_blocks/
├── capability_gaps.md
└── architecture_principles.md

## Extraction Process
1. Read source line by line, tracking line numbers
2. Identify architecture components (systems, platforms, integrations)
3. Classify as ABB (Abstract) or SBB (Solution Building Block)
4. Map to TOGAF domains: Business, Data, Application, Technology
5. Identify gaps between current and target state
6. Extract architecture principles and decisions

## Citation Format (STRICT)
*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*
```

### Create Test Data

Create `dsrag/.claude/agents/dsrag/examples/togaf-architecture/test-input.txt` with a representative transcript containing architecture discussions, and `expected-output.md` showing the ideal extraction.

### Create a Matching Delivery Template (Optional)

If the lens supports a specific deliverable, create a template at:

```
dsrag/.claude/skills/dsrag-deliver/templates/togaf/architecture-assessment.md.template
```

Use template variables to pull in the extracted knowledge base content.

## Adding a Delivery Template

Delivery templates render consolidated knowledge into formatted documents.

1. Create the template file at `dsrag/.claude/skills/dsrag-deliver/templates/[framework]/[name].md.template`.
2. Use template variables (`{{PROJECT_NAME}}`, `{{KNOWLEDGE_BASE: path}}`, `{{AI_SYNTHESIS}}...{{/AI_SYNTHESIS}}`) to reference knowledge base content.
3. Test the template with existing consolidated knowledge to verify rendering.

See [content-guide.md](content-guide.md) for the full template variable syntax.

## Contribution Checklist

Before submitting a PR for a new lens or template:

- [ ] Created agent template with YAML frontmatter
- [ ] Added "internal agent template" header
- [ ] Written complete extraction logic with numbered steps
- [ ] Defined knowledge base output structure for both stages
- [ ] Created test input data (400-500 lines max)
- [ ] Created expected output
- [ ] Tested via `/dsrag-ingest`
- [ ] PR linked to approved GitHub issue
