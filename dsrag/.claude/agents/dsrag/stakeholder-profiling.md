---
agent: stakeholder-profiling
type: lens
invoked-by: dsrag-ingest
description: Extract stakeholder profiles from transcripts. Identifies personas, roles, pain points, relationships, and organizational dynamics.
---

> **Internal Agent Template** — This file is read by `dsrag-ingest` at runtime. NOT a user-facing skill.

# DSRAG Stakeholder Profiling

Extract stakeholder information from transcripts into structured profiles.

## Invocation

Read by `dsrag-ingest` and passed as prompt to a Task agent.

## Prerequisites

- Project must be initialized with `dsrag-init-project`
- Transcript file must exist in `[projectid]/transcripts/`

## Operating Principle

**Two-stage extraction:**
1. Create processed analysis in `.dsrag/[projectid]/processed/transcripts/[filename]_stakeholder_analysis.md`
2. Extract structured profiles to `.dsrag/[projectid]/knowledge/stakeholders/`

**STRICT RULE:** Create individual profiles + stakeholder map. No auxiliary files.

## Required Output Structure

**Stage 1: Processed Analysis**
- File: `.dsrag/[projectid]/processed/transcripts/[filename]_stakeholder_analysis.md`
- Contains: Raw observations, quotes, organizational notes

**Stage 2: Structured Knowledge:**
1. `.dsrag/[projectid]/knowledge/stakeholders/profiles/[stakeholder-name].md` (one per person)
2. `.dsrag/[projectid]/knowledge/stakeholders/stakeholder_map.md` (relationships overview)

## Extraction Process

### Step 1: Read transcript file

Read line by line, tracking line numbers for citations.

### Step 2: Identify stakeholders

Extract mentions of:
- **Names:** Specific people mentioned (Alice, Frank, Sam, Karen, etc.)
- **Roles:** Titles or positions (Lead Architect, VP, etc.)
- **Organizations:** Company affiliations
- **Relationships:** Reports to, manages, dotted line, collaborates with

### Step 3: Capture stakeholder attributes

For each stakeholder, extract:
- **Role/Title:** Official position
- **Organization:** Company or department
- **Reporting structure:** Who they report to, who reports to them
- **Responsibilities:** What they're accountable for
- **Pain points:** Problems or challenges they face
- **Goals/Motivations:** What they want to achieve
- **Personality traits:** Communication style, approachability
- **Decision authority:** What they can decide or influence
- **Relationships:** Connections to other stakeholders
- **Evolution:** How their behavior/attitude changed over time

### Step 4: Create processed analysis

Write: `.dsrag/[projectid]/processed/transcripts/[filename]_stakeholder_analysis.md`

**Template:**
```markdown
# Stakeholder Analysis: [filename]

**Project:** [project_id]
**Source:** [projectid]/transcripts/[filename]
**Processed:** [timestamp]

## Stakeholders Identified

### [Stakeholder Name 1]
**Role:** [role/title]
**Organization:** [company/dept]
**Reports to:** [manager]
**Manages:** [direct reports]

**Attributes:**
- [Attribute 1 with line reference]
- [Attribute 2 with line reference]

**Relationships:**
- [Relationship description with line reference]

**Quotes:**
Line X: "[quote]"
Line Y: "[quote]"

---

### [Stakeholder Name 2]
[Similar structure]

## Organizational Structure Observed

[Hierarchy or relationships diagram in text]

## Dynamics & Patterns

[Cross-stakeholder observations]
- Power dynamics
- Communication patterns
- Influence relationships
```

### Step 5: Extract individual profiles

**Path:** `.dsrag/[projectid]/knowledge/stakeholders/profiles/[name].md`

**Naming convention:** Use lowercase with hyphens (e.g., `alice.md`, `bob.md`)

**Upsert behavior:**
- If profile exists: Read existing, append new information with source marker
- If new: Create profile
- Never delete existing information

**Profile Template:**
```markdown
# [Stakeholder Name]

## Role & Organization

**Title:** [role/title]
**Organization:** [company/department]
**Reports to:** [manager name]

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*

## Responsibilities

[What they're accountable for]

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*

## Reporting Structure

**Direct reports:**
- [Person 1]
- [Person 2]

**Dotted line reports (for engagement):**
- [Person 3]
- [Person 4]

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*

## Pain Points & Challenges

[Problems they face or express]

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*

## Goals & Motivations

[What they want to achieve]

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*

## Personality & Communication Style

[How they interact, approachability, communication preferences]

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*

## Decision Authority

[What they can decide or influence]

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*

## Relationships to Other Stakeholders

**[Other Stakeholder]:** [nature of relationship]

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*

## Evolution

[How their behavior/attitude changed over time, if mentioned]

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*

## Sources

- [List all transcripts this profile draws from]
```

**Example:**
```markdown
# Frank

## Role & Organization

**Title:** Lead Architect
**Organization:** ClientCorp
**Reports to:** Bob

*[Source: my-project/transcripts/interview-01.txt:7, Grace: "Frank, who is a direct report to Bob and he's our he's now like our lead architect from the client side, which they haven't had before"]*

## Responsibilities

Technical leadership for data platform engagement.

*[Source: my-project/transcripts/interview-02.txt:9, Grace: "folks like Team Member 1 or Jack as folks on the it side, Team Member 2, et cetera, they're not they're dotted line to him for the engagement"]*

## Reporting Structure

**Direct reports:** None mentioned

**Dotted line reports (for engagement):**
- Team Member 1 (IT side)
- Jack (IT side)
- Team Member 2

*[Source: my-project/transcripts/interview-02.txt:9, Grace: "they're dotted line to him for the engagement"]*

## Context

This is a new role at the client - they haven't had an architect in this capacity before.

*[Source: my-project/transcripts/interview-02.txt:7, Grace: "which they haven't had before"]*
```

### Step 6: Create/update stakeholder map

**Path:** `.dsrag/[projectid]/knowledge/stakeholders/stakeholder_map.md`

**Upsert behavior:** Append new relationships, don't overwrite existing

**Map Template:**
```markdown
# Stakeholder Map

**Last Updated:** [timestamp]
**Sources:** [list of transcripts]

## Organizational Structure

### Executive Leadership
- **[Name]:** [Role]
  - [Key attributes]

### [Department/Team 1]
- **[Name]:** [Role]
  - Reports to: [Manager]
  - Manages: [Direct reports]

### [Department/Team 2]
[Similar structure]

## Reporting Relationships

```
[ASCII diagram or bullet structure showing reporting lines]

Example:
Bob (Executive)
  └─ Frank (Lead Architect)
      ├─ Team Member 1 (dotted line)
      ├─ Jack (dotted line)
      └─ Team Member 2 (dotted line)
```

## Key Relationships

### [Stakeholder A] <-> [Stakeholder B]
[Nature of relationship]

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*

## Power & Influence Dynamics

[Who has decision authority, who influences whom]

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*

## Communication Patterns

[How stakeholders interact, formal/informal channels]

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*

## Engagement Health

[How stakeholders relate to consulting team, trust level, openness]

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*
```

## Citation Format (STRICT)

Every fact MUST have inline citation:

```markdown
Statement here.

*[Source: [projectid]/transcripts/[filename]:[line], [Speaker]: "[quote]"]*
```

**Examples:**
```markdown
*[Source: my-project/transcripts/interview-02.txt:15, Dana: "Sam is very friendly, outgoing"]*
*[Source: test-project/transcripts/interview.txt:42, Eric: "Karen is more reserved"]*
```

## Upsert Logic

When profiles already exist:

1. **Read existing profile**
2. **Check for new information not already present**
3. **If new:** Append section with source marker
4. **If duplicate:** Sam appending
5. **Never delete existing content**

**Example upsert:**
```markdown
# Alice

## Role & Organization
[Existing content from transcript A...]

---

## Additional Context (from [filename])
[New information from transcript B...]
```

## Conflict Detection

**Before appending new content, check for conflicts with existing knowledge.**

### When to Check for Conflicts

Run conflict detection when adding:
- Role/title information (different titles for same person)
- Organizational relationships (conflicting reporting structures)
- Personality traits (contradictory descriptions)
- Decision authority (inconsistent authority levels)

### How to Detect Conflicts

Use the conflict detector script:

```bash
python .claude/scripts/dsrag/dsrag_conflict_detector.py \
    --existing-file ".dsrag/$PROJECT_ID/knowledge/stakeholders/profiles/[stakeholder-name].md" \
    --new-assertion "$NEW_CONTENT" \
    --context "role information" \
    --existing-source "transcript A, line 15" \
    --new-source "transcript B, line 42"
```

**Exit codes:**
- `0` = No conflict detected, safe to append
- `1` = Conflict detected, user resolution required

### If Conflict Detected

Use AskUserQuestion to prompt user:

**Question:** "Conflicting information detected about [stakeholder]'s [context]. How should we resolve this?"

**Options:**
1. **"Keep existing"** - Preserve current knowledge, discard new assertion
   - Description: "Trust the existing source ([existing_source])"

2. **"Replace with new"** - Replace old with new assertion
   - Description: "Trust the new source ([new_source]) and update existing knowledge"

3. **"Keep both with note"** - Preserve both, add conflict marker
   - Description: "Document both perspectives with citations"

4. **"Manual resolution"** - User will edit manually
   - Description: "Sam automatic update, I'll resolve this manually"

**Apply user choice:**

- **Keep existing:** Sam appending new content
- **Replace with new:** Find and replace existing assertion with new
- **Keep both:** Append new content with conflict note:
  ```markdown
  **Note:** Conflicting information exists. See both sources:
  - [Existing source]: "Role X"
  - [New source]: "Role Y"
  ```
- **Manual resolution:** Sam automatic update, log conflict for user review

### Conflict Examples

**Role conflict:**
```
Existing: "Title: Lead Architect"
New:      "Title: Senior Architect"
-> Different title for same person
```

**Reporting conflict:**
```
Existing: "Reports to: Bob"
New:      "Reports to: Alice"
-> Different reporting structure
```

**Personality conflict:**
```
Existing: "Very friendly, outgoing"
New:      "Reserved, keeps distance"
-> Contradictory personality descriptions
```

## Error Prevention

**DO:**
- Create one profile per stakeholder
- Cite every fact with line numbers
- Capture organizational relationships
- Create stakeholder map showing connections
- Upsert to existing profiles
- Use project ID in all paths
- Only state facts from transcript (no speculation)

**DON'T:**
- Create auxiliary files (drafts, notes, temp)
- Speculate about roles/motivations not mentioned
- Sam citations
- Overwrite existing profiles
- Assume organizational structure not stated
- Forget to update stakeholder map

## Testing

**Test with:**
- `.claude/agents/dsrag/examples/stakeholder-profiling/test-transcript.txt`
- Project ID: `test-project`

**Expected output documented in:**
- `.claude/agents/dsrag/examples/stakeholder-profiling/expected-output.md`

## Implementation Notes

1. **Name normalization:** Convert names to lowercase with hyphens for filenames
   - "Frank" -> `frank.md`
   - "Alice" -> `alice.md`
2. **Incomplete information:** It's OK if some profile sections are empty (e.g., no pain points mentioned)
3. **Relationships:** Track both explicit (reports to) and implicit (works with) relationships
4. **Evolution:** Capture if stakeholder behavior changed over time
5. **Multiple mentions:** Consolidate all mentions of same person into single profile
