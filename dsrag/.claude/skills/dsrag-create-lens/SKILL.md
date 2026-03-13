---
name: dsrag-create-lens
description: Create a custom extraction lens — guides through lens design, writes agent template to .claude/agents/dsrag/custom/, registers in project config, and offers to backfill existing files.
---

# DSRAG Create Lens

Guided creation of custom extraction lenses for project-specific knowledge extraction needs.

## When to Use

- You need extraction patterns beyond the 4 core lenses (stakeholder, problem, VSM, summary)
- A project has domain-specific knowledge to extract (e.g., compliance requirements, risk factors, technology inventory)
- During `dsrag-init-project` when prompted to create custom lenses

## Usage

```bash
/dsrag-create-lens
/dsrag-create-lens --project-id [project-id]   # Also register in project
```

**Parameters:**
- `--project-id` (optional): If provided, auto-register the lens in this project's config after creation

## Output

- Agent template: `.claude/agents/dsrag/custom/[lens-name].md`
- Project config update: `.dsrag/[project-id]/config.json` (if project specified)

---

## Execution Process

### Step 1: Gather Lens Requirements

Use AskUserQuestion to collect information one question at a time:

**Question 1: Lens Name**
- "What should this lens be called? (lowercase-with-hyphens, e.g., 'compliance-extraction', 'risk-assessment')"
- Validate: lowercase, hyphens only, no spaces, no conflict with core lens names

**Question 2: Lens Purpose**
- "What knowledge should this lens extract? Describe in 1-2 sentences."
- Example: "Extract compliance requirements, regulatory references, and audit findings from transcripts"

**Question 3: Source Type**
- "What type of sources will this lens process?"
- Options: (a) Transcripts only, (b) Documents only, (c) Both
- Default: Transcripts only

**Question 4: Extraction Categories**
- "What categories of information should be extracted? List 3-7 categories."
- Example: "Regulatory requirements, Compliance gaps, Audit findings, Risk areas, Control descriptions"

**Question 5: Output Structure**
- "How should extracted knowledge be organized?"
- Options:
  - (a) Single file per source (like transcript-summary)
  - (b) Category-based files (like problem-extraction — one file per category)
  - (c) Entity-based files (like stakeholder-profiling — one file per entity)
- Recommend based on extraction categories count

**Question 6: Knowledge Folder**
- "What folder name for the knowledge output? (under .dsrag/[project-id]/knowledge/)"
- Suggest based on lens name (e.g., `compliance-extraction` → `compliance/`)

### Step 2: Generate Agent Template

Create `.claude/agents/dsrag/custom/[lens-name].md` following the core agent convention:

```markdown
---
agent: [lens-name]
type: lens
invoked-by: dsrag-ingest
description: [From Question 2]
---

> **Custom Agent Template** — Created via `/dsrag-create-lens`. Read by `dsrag-ingest` at runtime.

# DSRAG [Lens Title]

[Purpose description from Question 2]

## Invocation

Read by `dsrag-ingest` and passed as prompt to a Task agent.

## Prerequisites

- Project must be initialized with `dsrag-init-project`
- Source file must exist in `[projectid]/transcripts/` or `[projectid]/documents/`

## Operating Principle

**Two-stage extraction:**
1. Create processed analysis in `.dsrag/[projectid]/processed/[source-type]/[filename]_[lens-name]_analysis.md`
2. Extract structured knowledge to `.dsrag/[projectid]/knowledge/[knowledge-folder]/`

**STRICT RULE:** Output ONLY to defined structure. No auxiliary files.

## Required Output Structure

**Stage 1: Processed Analysis**
- File: `.dsrag/[projectid]/processed/[source-type]/[filename]_[lens-name]_analysis.md`
- Contains: Raw extraction notes, quotes, line references

**Stage 2: Structured Knowledge:**
[Generated based on Question 5 — single file, category-based, or entity-based]

## Extraction Process

### Step 1: Read source file

Read line by line, tracking line numbers for citations.

### Step 2: Extract by category

For each extraction category:
[Generated from Question 4 — one subsection per category with extraction guidance]

### Step 3: Create processed analysis

Write: `.dsrag/[projectid]/processed/[source-type]/[filename]_[lens-name]_analysis.md`

[Template generated based on categories]

### Step 4: Extract to structured knowledge

[Template generated based on output structure choice]

## Citation Format (STRICT)

Every fact MUST reference line numbers:

\`\`\`
**Quote:** *"[exact quote]"* (Line X)
\`\`\`

## Upsert Logic

When knowledge files already exist:
1. Read existing files
2. Append new extractions with source marker
3. Never delete existing content

## Error Prevention

**DO:**
- Cite every fact with line numbers
- Use project ID in all paths
- Follow upsert logic

**DON'T:**
- Create auxiliary files
- Skip citations
- Overwrite existing content
```

### Step 3: Present Template for Review

Display the generated agent template to the user:

```markdown
## Generated Lens Template

Here's the agent template I've created for **[lens-name]**:

[Show key sections: frontmatter, extraction categories, output structure]

Does this look right? Would you like to adjust anything before saving?
```

Wait for user confirmation or adjustments.

### Step 4: Write Agent Template

After user confirms:

```bash
# Write the template
Write: .claude/agents/dsrag/custom/[lens-name].md
```

Report:
```markdown
✅ Lens template created: `.claude/agents/dsrag/custom/[lens-name].md`
```

### Step 5: Register in Project (if applicable)

**If `--project-id` was provided OR user is in an active project:**

Ask: "Add this lens to project **[project-id]**?"

If yes:
1. Read `.dsrag/[project-id]/config.json`
2. Add lens name to `include_lenses` array (create array if missing)
3. Write updated config

```json
{
  "include_lenses": ["[lens-name]"]
}
```

Report:
```markdown
✅ Lens registered in project [project-id]
   Config: .dsrag/[project-id]/config.json → include_lenses: ["[lens-name]"]
```

**If no project specified:**

```markdown
ℹ️ Lens created but not registered to any project.
   To use it, either:
   - Run `/dsrag-init-project` (will prompt for lens selection)
   - Run `/dsrag-create-lens --project-id [project-id]` to register later
```

### Step 6: Offer Backfill

**Only if registered to a project in Step 5.**

Check for already-processed files:

```bash
# Count processed transcripts/documents
wc -l .dsrag/[project-id]/knowledge/_meta/citations.jsonl
```

If processed files exist:

```markdown
You have **[N]** already-processed files in project [project-id].

Would you like to run the **[lens-name]** lens against these existing files now?
This will only run the new lens — core lenses will NOT be re-run.

Estimated: [N] files × 1 agent = ~[time estimate]
```

If user says yes:
1. Read the new lens template
2. For each processed file, launch a Task agent with the new lens template
3. Batch in groups of 5
4. Report progress per batch

If user says no:
```markdown
ℹ️ Backfill skipped. The lens will be used for new files on the next `/dsrag-ingest` run.
```

### Step 7: Report Completion

```markdown
## Custom Lens Created

**Lens:** [lens-name]
**Template:** `.claude/agents/dsrag/custom/[lens-name].md`
**Registered:** [project-id] / Not registered
**Backfill:** [Completed (N files) / Skipped / N/A]

### Next Steps
- Run `/dsrag-ingest [project-id]` to use the lens on new files
- Run `/dsrag-create-lens` to create additional lenses
- Edit the template directly at `.claude/agents/dsrag/custom/[lens-name].md` for fine-tuning
```

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Convention-based discovery | Lenses in `.claude/agents/dsrag/custom/` are portable — copy `.claude/` to new project |
| Per-project `include_lenses` | Not all custom lenses apply to all projects |
| Backfill at creation time | One-time operation avoids complicating `dsrag-ingest` with per-lens tracking |
| Same agent template format | Custom lenses are first-class — same frontmatter, same two-stage output |

---

## Related Skills

- `dsrag-ingest` — Reads custom lenses from `include_lenses` config and runs alongside core lenses
- `dsrag-init-project` — Scans for available custom lenses and prompts for selection
