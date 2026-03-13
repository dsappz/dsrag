---
name: dsrag-reset-project
description: Archive and reset a DSRAG project, clearing all accumulated knowledge and processing history for clean reprocessing.
---

# DSRAG Project Reset

Archive existing project data and reset to clean state for reprocessing with updated lenses or starting fresh.

## When to Use

- **Lens improvements:** Reprocess all sources with updated extraction logic
- **Data cleanup:** Remove accumulated test or incorrect extractions
- **Fresh start:** Clear everything and rebuild knowledge base
- **Migration:** Transition between DSRAG versions

## Prerequisites

- Project must exist at `.dsrag/[project-id]/`
- User must confirm reset action

## Reset Behavior

**Safe archive-then-delete:**
1. Archive existing project to `.dsrag/_archived/[project-id]-[timestamp]/`
2. Delete `.dsrag/[project-id]/`
3. Project directory removed, ready for re-initialization

**Preservation:**
- Source files (transcripts, documents) are NOT touched
- Archived data retained in `.dsrag/_archived/` for reference

## Usage

**Command:**
```bash
/dsrag-reset-project --project-id my-project
```

**With confirmation bypass (caution):**
```bash
/dsrag-reset-project --project-id my-project --confirm yes
```

## Execution Process

### Step 1: Validate project exists

Check that `.dsrag/[project-id]/` exists.

If not found:
```
Error: Project '[project-id]' not found at .dsrag/[project-id]/
Nothing to reset.
```

### Step 2: Show impact preview

**Display what will be affected:**

```markdown
Project Reset Preview
───────────────────────────────────────────────

Project: [project-id]
Location: .dsrag/[project-id]/

**What will be archived:**
- Knowledge bases:
  - Stakeholder profiles: X files
  - Problems: Y problems
  - VSM analyses: Z files
  - Summaries: W files
- Processed analyses: [count] files
- Citations: [count] processed sources

**Archive destination:**
.dsrag/_archived/[project-id]-[timestamp]/

**What will NOT be affected:**
- Source files: [project-id]/transcripts/*.txt (untouched)
- Tool configuration: .claude/ (untouched)

**After reset:**
- Project directory deleted: .dsrag/[project-id]/
- Ready for fresh initialization: /dsrag-init-project --project-id [project-id]
```

### Step 3: Confirm with user

**Use AskUserQuestion:**

```markdown
**Question:** "Reset project '[project-id]'? All knowledge will be archived then deleted."

**Options:**
1. **"Yes, archive and reset"** (Recommended)
   - Description: "Archive to .dsrag/_archived/ then delete .dsrag/[project-id]/"

2. **"No, cancel"**
   - Description: "Keep project as-is, no changes"

3. **"Archive only (no deletion)"**
   - Description: "Create backup but keep project intact"
```

If user selects "No, cancel":
```
Reset cancelled. No changes made.
```

If user selects "Archive only":
- Continue to Step 4 (archive)
- Skip Step 5 (deletion)

### Step 4: Create archive

**Archive path:**
```
.dsrag/_archived/[project-id]-[YYYYMMDD-HHMMSS]/
```

**Example:**
```
.dsrag/_archived/my-project-20260129-143000/
```

**Archive process:**
```bash
# Create archive directory
mkdir -p .dsrag/_archived

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Copy entire project
cp -r .dsrag/[project-id] .dsrag/_archived/[project-id]-$TIMESTAMP

# Verify copy
if [ $? -eq 0 ]; then
    echo "✓ Archived to .dsrag/_archived/[project-id]-$TIMESTAMP/"
else
    echo "✗ Archive failed, aborting reset"
    exit 1
fi
```

**Create archive manifest:**

Write `.dsrag/_archived/[project-id]-[timestamp]/ARCHIVE_INFO.md`:

```markdown
# Archive Information

**Project ID:** [project-id]
**Archived:** [timestamp]
**Reason:** Project reset
**Original Location:** .dsrag/[project-id]/

## Contents

**Knowledge Bases:**
- Stakeholder profiles: X files
- Problems: Y problems
- VSM analyses: Z files
- Summaries: W files

**Processed Analyses:** [count] files

**Citations:** [count] processed sources

## Restore Instructions

To restore this project:

```bash
# Copy archive back to active location
cp -r .dsrag/_archived/[project-id]-[timestamp] .dsrag/[project-id]

# Remove timestamp suffix
mv .dsrag/[project-id] .dsrag/[project-id]-restored

# Rename
mv .dsrag/[project-id]-restored .dsrag/[project-id]
```

## Sources Processed

[List of source files from citations.jsonl]

- [source1.txt]
- [source2.txt]
- ...
```

### Step 5: Delete project directory

**If user confirmed deletion:**

```bash
# Delete project directory
rm -rf .dsrag/[project-id]

# Verify deletion
if [ ! -d .dsrag/[project-id] ]; then
    echo "✓ Project directory deleted: .dsrag/[project-id]/"
else
    echo "✗ Deletion failed"
    exit 1
fi
```

### Step 6: Report completion

**Success message:**

```markdown
✓ Project reset complete

**Archive location:**
.dsrag/_archived/[project-id]-[timestamp]/

**Archived contents:**
- Knowledge bases: X stakeholders, Y problems, Z VSM, W summaries
- Processed analyses: [count] files
- Citations: [count] sources

**Project directory deleted:**
.dsrag/[project-id]/ (removed)

**Next steps:**

1. **Re-initialize project:**
   /dsrag-init-project --project-id [project-id]

2. **Reprocess sources:**
   /dsrag-ingest --project-id [project-id] --folder [project-id]/transcripts/

3. **Or restore from archive:**
   cp -r .dsrag/_archived/[project-id]-[timestamp] .dsrag/[project-id]

**Source files preserved:**
[project-id]/transcripts/ (unchanged)
[project-id]/documents/ (unchanged)
```

## Archive Management

### List all archives

```bash
ls -lt .dsrag/_archived/

# Output:
# my-project-20260129-143000/
# my-project-20260128-090000/
# other-project-20260115-120000/
```

### Remove old archives

```bash
# Remove specific archive
rm -rf .dsrag/_archived/[project-id]-[timestamp]/

# Remove all archives older than 30 days
find .dsrag/_archived/ -type d -mtime +30 -exec rm -rf {} \;
```

### Restore from archive

```bash
# Restore most recent archive
LATEST=$(ls -t .dsrag/_archived/ | grep "^[project-id]-" | head -1)
cp -r .dsrag/_archived/$LATEST .dsrag/[project-id]
```

## Safety Features

**Archive-first design:**
- Always archive before delete
- Archives timestamped for multiple backups
- Archive includes manifest for documentation

**Confirmation required:**
- User must explicitly approve deletion
- Preview shows what will be affected
- Option to archive-only without deletion

**Source preservation:**
- Transcript and document files never touched
- Only `.dsrag/[project-id]/` affected

**Reversible:**
- Archive contains complete project state
- Restore instructions included in archive
- Multiple restore points if reset multiple times

## Error Handling

**Project not found:**
```
Error: Project '[project-id]' does not exist at .dsrag/[project-id]/
Nothing to reset.
```

**Archive creation fails:**
```
Error: Failed to create archive at .dsrag/_archived/[project-id]-[timestamp]/
Reason: [error details]

Reset aborted. No changes made.
```

**Deletion fails:**
```
Warning: Project archived successfully but deletion failed.
Archive location: .dsrag/_archived/[project-id]-[timestamp]/
Manual deletion required: rm -rf .dsrag/[project-id]
```

## Use Cases

### Use Case 1: Lens Improvement

**Scenario:** Updated stakeholder-profiling agent template (`.claude/agents/dsrag/stakeholder-profiling.md`) to extract more details.

**Workflow:**
```bash
# Reset project
/dsrag-reset-project --project-id my-project

# Re-initialize
/dsrag-init-project --project-id my-project

# Reprocess with improved lens
/dsrag-ingest --project-id my-project --folder my-project/transcripts/

# Result: New knowledge bases with improved extractions
```

---

### Use Case 2: Clean Test Data

**Scenario:** Tested DSRAG with sample files, now ready for production.

**Workflow:**
```bash
# Reset test project
/dsrag-reset-project --project-id test-project

# Remove archive (don't need test data backup)
rm -rf .dsrag/_archived/test-project-*

# Ready for real data
/dsrag-init-project --project-id production
```

---

### Use Case 3: Version Migration

**Scenario:** Migrating from DSRAG 2.0 to 3.0 with new file structure.

**Workflow:**
```bash
# Archive old version
/dsrag-reset-project --project-id legacy-project

# Archive preserved at .dsrag/_archived/legacy-project-[timestamp]/

# Initialize with new version
/dsrag-init-project --project-id legacy-project

# Reprocess with v3.0 structure
/dsrag-ingest --project-id legacy-project --folder legacy-project/transcripts/
```

## Related Commands

**Initialize project after reset:**
```bash
/dsrag-init-project --project-id [project-id]
```

**Reprocess sources:**
```bash
/dsrag-ingest --project-id [project-id] --folder [project-id]/transcripts/
```

**Check archived projects:**
```bash
ls -lt .dsrag/_archived/
```

---

**Last Updated:** 2026-01-29
**Version:** 3.0.0
