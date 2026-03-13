---
name: dsrag-init-project
description: Use when initializing DSRAG knowledge base for EA engagement. Creates project-scoped folder structure with project ID.
---

# DSRAG Init Project

Initialize or validate DSRAG knowledge base structure for an engagement.

## When to Use

- Starting new EA engagement
- Setting up DSRAG for first time in project
- Validating existing DSRAG project structure

## Architecture

**Project-scoped structure:**
- `.dsrag/[projectid]/knowledge/` - Structured knowledge
- `.dsrag/[projectid]/processed/` - Processed analysis
- `[projectid]/transcripts/` - Raw interview transcripts
- `[projectid]/documents/` - Raw source documents
- `[projectid]/deliverables/` - Project deliverables

## What It Does

**If project doesn't exist:**
1. Prompts for project ID, name, client
2. Creates complete folder structure (24+ folders)
3. Initializes metadata files (project_charter.md, citations.jsonl, config.json)
4. Creates project README.md

**If project exists (Upsert Mode):**
1. Validates all folders exist
2. Creates any missing folders
3. Creates missing metadata files (never overwrites existing)
4. Reports what was added

## Usage

User invokes: `dsrag-init-project`

## Implementation

**Step 1: Prompt for project info**

Use AskUserQuestion tool to collect:

**Question 1: Project ID**
- Header: "Project ID"
- Question: "Enter a project ID (will be used for folders, e.g., 'my-project'):"
- Type: Freeform text input
- Note: Will be sanitized to lowercase-with-hyphens

**Question 2: Project Name**
- Header: "Project Name"
- Question: "Enter the full project name:"
- Type: Freeform text input
- Example: "Client Data Platform - Discovery Phase"

**Question 3: Client Name**
- Header: "Client"
- Question: "Enter the client name:"
- Type: Freeform text input
- Example: "Client Services, Inc. (ClientCorp)"

**Step 2: Check if project already exists**

```bash
PROJECT_ID="[from user input, will be sanitized by script]"

if [ -d ".dsrag/$PROJECT_ID" ]; then
    MODE="validate"
    echo "ℹ Project '$PROJECT_ID' already exists. Validating structure..."
else
    MODE="init"
fi
```

**Step 3: Execute Python init script**

```bash
if [ "$MODE" = "init" ]; then
    python .claude/scripts/dsrag/dsrag_init_project.py \
        --init \
        --project-root "$PWD" \
        --project-id "$PROJECT_ID" \
        --project-name "$PROJECT_NAME" \
        --client-name "$CLIENT_NAME"
else
    python .claude/scripts/dsrag/dsrag_init_project.py \
        --validate \
        --create-missing \
        --project-root "$PWD" \
        --project-id "$PROJECT_ID"
fi
```

**Step 4: Custom Lens Configuration**

**4.1 Scan for available custom lenses:**

```bash
ls .claude/agents/dsrag/custom/*.md 2>/dev/null | grep -v README.md
```

**4.2 If custom lenses found:**

Display available lenses:

```markdown
## Custom Lenses Available

The following custom extraction lenses are installed:

| Lens | Description |
|------|-------------|
| [lens-name-1] | [from frontmatter description] |
| [lens-name-2] | [from frontmatter description] |
```

Use AskUserQuestion:
- "Which custom lenses would you like to include for this project? (comma-separated, or 'all', or 'none')"

Write selected lenses to `.dsrag/[project-id]/config.json`:

```json
{
  "include_lenses": ["lens-name-1", "lens-name-2"]
}
```

**4.3 If no custom lenses found:**

```markdown
ℹ️ No custom lenses installed.
   Core lenses (stakeholder, problem, VSM, summary, document-analyzer) will be used.
   Create custom lenses anytime with: /dsrag-create-lens
```

**4.4 Upsert mode (project already exists):**

Read existing `include_lenses` from config and display:

```markdown
## Current Custom Lens Configuration

| Lens | Status |
|------|--------|
| [lens-1] | ✅ Included |
| [lens-2] | ✅ Included |
| [lens-3] | Available (not included) |

Would you like to modify the lens selection?
```

If yes, update config. If no, keep existing.

**Step 5: Report results**

**Init mode:**
```
✓ Project initialized: my-project
✓ Created 24 folders
✓ DSRAG artifacts: .dsrag/my-project/
✓ Project data: my-project/
✓ Custom lenses: [N] included ([lens-names] or "none — core lenses only")

Next steps:
  1. Review: .dsrag/[project-id]/knowledge/_meta/project_charter.md
  2. Add transcripts to: [project-id]/transcripts/
  3. Create custom lenses: /dsrag-create-lens
  4. Run: /dsrag-ingest [project-id]
```

**Validate mode:**
```
✓ Project exists: my-project
✓ Validated structure
✓ Created 2 missing folders:
  - .dsrag/my-project/knowledge/decisions/
  - .dsrag/my-project/knowledge/risks/
✓ All required files present
✓ Custom lenses: [N] configured ([lens-names])

Ready to process. Run: /dsrag-ingest [project-id]
```

## Operating Principle

**NEVER delete existing data.** Only add missing pieces (upsert, not delete/insert).

**Project ID sanitization:** Script automatically converts project IDs to filesystem-safe format (lowercase, hyphens for special chars).

## Error Handling

**If Python script fails:**
Report error and suggest manual fix.

**If project ID invalid:**
Script will sanitize automatically and notify user of the change.
