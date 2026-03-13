---
name: dsrag-deliver
description: Generate versioned deliverables from templates (business cases, stakeholder analyses, DAMA-DMBOK assessments).
---

# DSRAG Deliver

Generate professional deliverables from templates using extracted knowledge.

## When to Use

- Create business case for platform investment
- Generate stakeholder analysis report
- Produce data quality assessment (DAMA-DMBOK)
- Document findings and recommendations
- Prepare client-ready deliverables

## Prerequisites

- Project initialized with knowledge bases populated
- At least one transcript processed
- **Consolidation documents generated** — run `/dsrag-consolidate [project-id]` first (mandatory)
- Template selected (consulting, DAMA-DMBOK, cloud)

**Automatic prerequisite check:** When invoked, this skill will:
1. Read `[project-id]/consolidation/index.md` for the Deliverable Composition Map
2. Look up the target deliverable to find its primary + supporting topic fragments
3. If any required fragment is missing or stale: run `/dsrag-consolidate [project-id]` first
4. Assemble deliverable by reading the primary fragment in full + relevant sections from supporting fragments (composition, not duplication)

## Usage

```bash
/dsrag-deliver \
    --project-id my-project \
    --framework consulting \
    --template business-case \
    --version 1.0.0
```

**Parameters:**
- `--project-id`: Project identifier
- `--framework`: Template framework (consulting, dama-dmbok, cloud)
- `--template`: Template name (business-case, stakeholder-analysis, etc.)
- `--version`: Semantic version (major.minor.patch) or "auto" to increment
- `--project-name`: (Optional) Project display name

## Execution Process

### Step 1: Validate inputs

Check:
- Project exists at `.dsrag/[project-id]/`
- Knowledge bases populated (at least one domain has content)
- Template exists at `.claude/skills/dsrag/deliver/templates/[framework]/[template].md.template`

### Step 2: Determine version

If `--version auto`:
```python
from dsrag_versioning import get_latest_version, increment_version

latest = get_latest_version(project_id)
if latest:
    version = increment_version(latest, "minor")
else:
    version = "v1.0.0"
```

If `--version` specified:
- Validate format (e.g., "1.0.0" or "v1.0.0")
- Normalize to "vX.Y.Z" format

### Step 3: Create version directory

```python
from dsrag_versioning import create_version_directory, update_current_symlink

version_dir = create_version_directory(project_id, version)
# .dsrag/[project-id]/deliverables/v1.0.0/
```

### Step 4: Prepare template context

```python
context = {
    "project_id": project_id,
    "project_name": project_name or project_id,
    "version": version,
    "timestamp": datetime.now().strftime("%Y-%m-%d"),
}
```

### Step 5: Process template

```python
from dsrag_template_engine import TemplateEngine

engine = TemplateEngine(project_id)

template_path = f".claude/skills/dsrag/deliver/templates/{framework}/{template}.md.template"
output_path = f".dsrag/{project_id}/deliverables/{version}/{template}.md"

engine.generate_deliverable(template_path, output_path, context)
```

**For each AI_SYNTHESIS placeholder:**
1. Load relevant knowledge from knowledge base
2. Construct synthesis prompt with context
3. Call Claude to generate content
4. Replace placeholder with generated content (includes citations)

### Step 6: Update changelog

```python
from dsrag_versioning import update_changelog

changes = {
    "added": [f"{template.replace('-', ' ').title()} ({framework})"],
    "changed": [],
    "removed": []
}

update_changelog(project_id, version, changes)
```

### Step 7: Update current symlink

```python
from dsrag_versioning import update_current_symlink

update_current_symlink(project_id, version)
# .dsrag/[project-id]/deliverables/current -> v1.0.0/
```

### Step 8: Report completion

```markdown
✓ Deliverable generated

**Output:**
.dsrag/[project-id]/deliverables/v1.0.0/[template].md

**Version:** v1.0.0
**Framework:** [framework]
**Template:** [template]

**Access:**
- Current version: .dsrag/[project-id]/deliverables/current/[template].md
- Specific version: .dsrag/[project-id]/deliverables/v1.0.0/[template].md

**Next steps:**
- Review deliverable for accuracy
- Update if needed: /dsrag-deliver ... --version 1.0.1
- Generate additional deliverables from other templates
```

## Available Templates

### Consulting Framework

**business-case** - Business case with ROI analysis
- Problem statement, solution, benefits, investment, recommendation

**stakeholder-analysis** - Stakeholder power/interest analysis
- Profiles, influence mapping, engagement strategy

**findings-recommendations** - Executive findings report
- Current state, issues identified, recommendations

**rfi-documentation** - Request for Information for vendor evaluation
- Problem-centric RFI with hybrid structure (narrative context + structured criteria)
- 7 capability themes, MUST-HAVE/NICE-TO-HAVE classification, scoring model
- Sanitized current state architecture (C1/C2/data flow from consolidation)
- Growth-aspiration framing (never deficit-framing)
- Prerequisite: `consolidation/architecture.md` for Section 3 diagrams
- Design principles: sensitivity guardrails, commercial separation, binary classification
- Feeds into vendor evaluation matrix (DELIV-012)

### DAMA-DMBOK Framework

**data-quality-assessment** - Data quality state assessment
- Quality dimensions, issues, root causes, framework recommendations

**data-governance-charter** - Governance structure proposal
- Roles, responsibilities, decision rights, processes

**data-architecture-blueprint** - Data architecture design
- Current/future state, gap analysis, migration approach

### Cloud Frameworks

**aws-well-architected** - AWS Well-Architected Review
- 6 pillars assessment, findings, recommendations

**gcp-adoption-framework** - GCP Cloud Adoption Framework
- Readiness assessment, migration strategy

**azure-waf** - Azure Well-Architected Framework
- 5 pillars review, workload analysis

## Versioning

**Semantic versioning:** vMAJOR.MINOR.PATCH

**When to bump:**
- **MAJOR (v2.0.0):** Fundamental approach change, new knowledge invalidates previous
- **MINOR (v1.1.0):** New sections added, additional templates generated
- **PATCH (v1.0.1):** Corrections, clarifications, formatting fixes

**Auto-increment:**
```bash
/dsrag-deliver ... --version auto
```
Automatically increments MINOR version from latest.

**Manual version:**
```bash
/dsrag-deliver ... --version 1.2.0
```
Use specific version (useful for MAJOR bumps or corrections).

## Example Workflows

### Workflow 1: Initial Business Case

```bash
# Generate business case
/dsrag-deliver \
    --project-id my-project \
    --framework consulting \
    --template business-case \
    --version 1.0.0 \
    --project-name "Client Data Platform"

# Review output
cat .dsrag/my-project/deliverables/current/business-case.md

# If corrections needed
/dsrag-deliver \
    --project-id my-project \
    --framework consulting \
    --template business-case \
    --version 1.0.1 \
    --project-name "Client Data Platform"
```

### Workflow 2: Full Deliverable Suite

```bash
# Business case
/dsrag-deliver --project-id my-project --framework consulting --template business-case --version 1.0.0

# Stakeholder analysis
/dsrag-deliver --project-id my-project --framework consulting --template stakeholder-analysis --version auto

# Data quality assessment
/dsrag-deliver --project-id my-project --framework dama-dmbok --template data-quality-assessment --version auto

# Result: All in .dsrag/my-project/deliverables/current/
```

### Workflow 3: Knowledge Base Update

```bash
# Process new transcripts
/dsrag-ingest --project-id my-project --transcript-file new-interview.txt

# Regenerate deliverables with updated knowledge
/dsrag-deliver --project-id my-project --framework consulting --template business-case --version 1.1.0
```

## Error Handling

**Project not found:**
```
Error: Project 'unknown' not found

Initialize project:
/dsrag-init-project --project-id unknown
```

**Empty knowledge base:**
```
Warning: Knowledge base appears empty

Process transcripts first:
/dsrag-ingest --project-id my-project --transcript-file transcripts/interview.txt
```

**Template not found:**
```
Error: Template not found: consulting/unknown-template

Available templates:
- consulting/business-case
- consulting/stakeholder-analysis
- dama-dmbok/data-quality-assessment

List all: ls .claude/skills/dsrag/deliver/templates/
```

**Invalid version format:**
```
Error: Invalid version format: "abc"

Use semantic versioning:
- "1.0.0" or "v1.0.0" (explicit)
- "auto" (auto-increment from latest)
```

## Template Customization

**To add a new template:**

1. Create template file:
   `.claude/skills/dsrag/deliver/templates/[framework]/[name].md.template`

2. Use placeholders:
   - `{{VARIABLE}}` - Simple variables (version, project_id, etc.)
   - `{{KNOWLEDGE_BASE: path}}` - Insert from knowledge base
   - `{{AI_SYNTHESIS}} ... {{/AI_SYNTHESIS}}` - AI-generated content

3. Test:
   ```bash
   /dsrag-deliver --project-id test --framework [framework] --template [name] --version 1.0.0
   ```

**See:** `.claude/docs/DEVELOPER_GUIDE.md` for template development guide
