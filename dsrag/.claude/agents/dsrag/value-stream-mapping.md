---
agent: value-stream-mapping
type: lens
invoked-by: dsrag-ingest
description: Use when processing transcripts with business process discussions, bottlenecks, waste, or current/future state. Extracts VSM using Lean TIMWOODS framework.
---

> **Internal Agent Template** — This file is read by `dsrag-ingest` at runtime. NOT a user-facing skill.

# DSRAG Value Stream Mapping

Extract Value Stream Mapping insights from transcripts into structured knowledge.

## Invocation

Read by `dsrag-ingest` and passed as prompt to a Task agent.

## Prerequisites

- Project must be initialized with `dsrag-init-project`
- Transcript file must exist in `[projectid]/transcripts/`

## Operating Principle

**Two-stage extraction:**
1. Create processed analysis in `.dsrag/[projectid]/processed/transcripts/[filename]_vsm_analysis.md`
2. Extract structured knowledge to `.dsrag/[projectid]/knowledge/value_streams/*.md`

**STRICT RULE:** Output ONLY to defined structure. No auxiliary files in `.dsrag/[projectid]/knowledge/`.

## Required Output Structure

**Stage 1: Processed Analysis**
- File: `.dsrag/[projectid]/processed/transcripts/[filename]_vsm_analysis.md`
- Contains: Raw notes, observations, quotes with line numbers

**Stage 2: Structured Knowledge (ONLY these 4 files):**
1. `.dsrag/[projectid]/knowledge/value_streams/current_state.md`
2. `.dsrag/[projectid]/knowledge/value_streams/future_state.md`
3. `.dsrag/[projectid]/knowledge/value_streams/waste_analysis.md`
4. `.dsrag/[projectid]/knowledge/value_streams/gap_analysis.md`

## Extraction Process

### Step 1: Read transcript file

Read the transcript file line by line, tracking line numbers.

### Step 2: Identify VSM elements

As you read, extract:
- **Process steps:** Sequential activities mentioned
- **Lead times:** Time mentions (3-6 months, 4-6 weeks, etc.)
- **Wait times:** Waiting periods (weeks, months)
- **Pain points:** Problems, complaints, bottlenecks
- **Future improvements:** Proposed changes, automation
- **Waste indicators:** Delays, rework, duplication

### Step 3: Map waste to TIMWOODS

For each waste identified, categorize:
- **T**ransportation: Data moving between systems
- **I**nventory: Work queued/waiting
- **M**otion: Manual work that could be automated
- **W**aiting: Delays, queue time
- **O**verproduction: Unnecessary work
- **O**ver-processing: Redundant steps
- **D**efects: Errors, rework
- **S**kills: Knowledge gaps, single points of failure

### Step 4: Create processed analysis

Write: `.dsrag/[projectid]/processed/transcripts/[filename]_vsm_analysis.md`

**Template:**
```markdown
# VSM Analysis: [filename]

**Project:** [project_id]
**Source:** [projectid]/transcripts/[filename]
**Processed:** [timestamp]

## Current State Observations

[Process flow notes]
- Step 1: ...
- Step 2: ...

**Lead Times:**
- Total: X months
- Wait time: Y weeks

**Pain Points:**
- [List with line number references]

## Future State Observations

[Proposed improvements]

**Expected Improvements:**
- Lead time reduction: X -> Y

## TIMWOODS Waste Mapping

**Waiting (W):**
- Line X: [Description]

**Motion (M):**
- Line Y: [Description]

[etc.]

## Quotes for Knowledge Base

Line 2: "It can take three to six months..."
Line 7: "If we had automated validation..."

[All relevant quotes with line numbers]
```

### Step 5: Extract to current_state.md

**Path:** `.dsrag/[projectid]/knowledge/value_streams/current_state.md`

**Upsert behavior:**
- If file exists: Read existing content, append new sections with source marker
- If contradicts: Continue (conflict detection in Phase 2)
- If new: Create file

**Format:**
```markdown
# Current State Value Stream

## Process Flow

[Client onboarding process as described]

**Lead Time:** 3-6 months (client signs -> first accurate report)

*[Source: [projectid]/transcripts/[filename].txt:2, Dana: "It can take three to six months just to get the first accurate report out"]*

## Bottlenecks

**Reactive Field Mapping**
Clients send data in any format, team maps fields after the fact.

*[Source: [projectid]/transcripts/[filename].txt:1, Dana: "They just send us whatever random stuff they track"]*

## Wait Times

Weeks for initial data mapping, then additional weeks for error correction.

*[Source: [projectid]/transcripts/[filename].txt:10, Dana: "wait weeks for us to map it"]*
```

**Citation format (STRICT):**
```markdown
*[Source: [projectid]/transcripts/[filename].txt:[line], [Speaker]: "[quote]"]*
```

### Step 6: Extract to waste_analysis.md

**Path:** `.dsrag/[projectid]/knowledge/value_streams/waste_analysis.md`

**Format:**
```markdown
# Waste Analysis (TIMWOODS)

## Waiting (W)

**Client Data Mapping**
Clients wait weeks while team performs reactive field mapping.

*[Source: [projectid]/transcripts/[filename].txt:10, Dana: "wait weeks for us to map it"]*

**Error Correction Cycles**
Back-and-forth between client and team for data fixes.

*[Source: [projectid]/transcripts/[filename].txt:10, Dana: "It's just back and forth, back and forth"]*

## Motion (M)

**Manual Field Mapping**
Team manually maps data fields instead of automated metadata-driven process.

*[Source: [projectid]/transcripts/[filename].txt:2, Dana: "reactive field mapping"]*
```

### Step 7: Extract to future_state.md

**Path:** `.dsrag/[projectid]/knowledge/value_streams/future_state.md`

**Format:**
```markdown
# Future State Value Stream

## Process Improvements

**Automated Validation**
Validate data at ingestion point, catch errors in days instead of months.

*[Source: [projectid]/transcripts/[filename].txt:7, Dana: "If we had automated validation upfront, we could catch these issues in days"]*

**Metadata-Driven Ingestion**
Use metadata to automate field mapping, reducing manual intervention.

*[Source: [projectid]/transcripts/[filename].txt:7, Dana: "metadata-driven ingestion process"]*

## Expected Lead Time

4-6 weeks (from contract -> first accurate report)

*[Source: [projectid]/transcripts/[filename].txt:7, Dana: "4-6 weeks"]*
```

### Step 8: Extract to gap_analysis.md

**Path:** `.dsrag/[projectid]/knowledge/value_streams/gap_analysis.md`

**Format:**
```markdown
# Gap Analysis: Current -> Future State

## Lead Time Reduction

**Current:** 3-6 months
**Future:** 4-6 weeks
**Improvement:** 67% reduction in onboarding time

*[Source: [projectid]/transcripts/[filename].txt:2,7, Dana describing current (3-6 months) and future state (4-6 weeks)]*

## Waste Elimination

**Waiting:** Reduced from weeks to days through automated validation

*[Source: [projectid]/transcripts/[filename].txt:7, Dana: "catch these issues in days instead of months"]*
```

## Citation Format (STRICT)

Every factual statement MUST have inline citation:

```markdown
Statement here.

*[Source: [projectid]/transcripts/[filename].txt:[line], [Speaker]: "[quote]"]*
```

**Examples:**
```markdown
*[Source: my-project/transcripts/interview-01.txt:15, Dana: "It can take three to six months"]*
*[Source: test-project/transcripts/test-transcript.txt:7, Dana: "We're struggling with integration"]*
```

## Upsert Logic

When knowledge files already exist:

1. **Read existing content**
2. **Check for duplicate information** (same quote/line already cited)
3. **If duplicate:** Skip appending
4. **If new information:** Append new section with clear source marker
5. **Never delete existing content**

**Example upsert:**
```markdown
# Current State Value Stream

## Process Flow

[Existing content from previous transcript...]

---

## Process Flow (Additional from [filename])

[New content with new citations...]
```

## Conflict Detection

**Before appending new content, check for conflicts with existing knowledge.**

### When to Check for Conflicts

Run conflict detection when adding:
- Quantitative values (lead times, percentages, counts)
- Categorical assertions (severity levels, priority)
- Mutually exclusive statements

### How to Detect Conflicts

Use the conflict detector script:

```bash
python .claude/scripts/dsrag/dsrag_conflict_detector.py \
    --existing-file ".dsrag/$PROJECT_ID/knowledge/value_streams/current_state.md" \
    --new-assertion "$NEW_CONTENT" \
    --context "lead time" \
    --existing-source "transcript A, line 15" \
    --new-source "transcript B, line 42"
```

**Exit codes:**
- `0` = No conflict detected, safe to append
- `1` = Conflict detected, user resolution required

### If Conflict Detected

Use AskUserQuestion to prompt user:

**Question:** "Conflicting information detected about [context]. How should we resolve this?"

**Options:**
1. **"Keep existing"** - Preserve current knowledge, discard new assertion
   - Description: "Trust the existing source ([existing_source])"

2. **"Replace with new"** - Replace old with new assertion
   - Description: "Trust the new source ([new_source]) and update existing knowledge"

3. **"Keep both with note"** - Preserve both, add conflict marker
   - Description: "Document both perspectives with citations"

4. **"Manual resolution"** - User will edit manually
   - Description: "Skip automatic update, I'll resolve this manually"

**Apply user choice:**

- **Keep existing:** Skip appending new content
- **Replace with new:** Find and replace existing assertion with new
- **Keep both:** Append new content with conflict note:
  ```markdown
  **Note:** Conflicting information exists. See both sources:
  - [Existing source]: "X months"
  - [New source]: "Y months"
  ```
- **Manual resolution:** Skip automatic update, log conflict for user review

### Conflict Examples

**Quantitative conflict:**
```
Existing: "Lead time is 3-6 months"
New:      "Lead time is 9 months"
-> 50% difference detected
```

**Categorical conflict:**
```
Existing: "Severity: High"
New:      "Severity: Critical"
-> Different severity levels
```

## Error Prevention

**DO:**
- Create processed analysis first, then extract
- Cite every fact with line numbers
- Map waste to TIMWOODS categories
- Upsert to existing files (don't overwrite)
- Output ONLY to 4 defined knowledge files
- Use project ID in all paths

**DON'T:**
- Create additional files in `.dsrag/[projectid]/knowledge/value_streams/`
- Summarize without citations
- Skip the processed analysis stage
- Ignore TIMWOODS framework
- Delete existing knowledge during upsert
- Forget to include project ID in paths

## Testing

**Test with:**
- `.claude/agents/dsrag/examples/value-stream-mapping/test-transcript.txt`
- Project ID: `test-project`

**Expected output documented in:**
- `.claude/agents/dsrag/examples/value-stream-mapping/expected-output.md`

## Implementation Notes

1. **Always ask for project ID first** if not provided
2. **Validate project exists** (`.dsrag/[projectid]/` folder exists)
3. **Track line numbers** as you read transcript
4. **Parse speaker format:** `Speaker | timestamp`
5. **Preserve exact quotes** for citations
6. **Use TIMWOODS explicitly** in waste_analysis.md headers
