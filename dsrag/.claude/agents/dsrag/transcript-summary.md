---
agent: transcript-summary
type: lens
invoked-by: dsrag-ingest
description: Extract meeting intelligence from transcripts - participants, key topics, decisions (structured with rationale and dependencies), next steps, open questions, and sentiment analysis.
---

> **Internal Agent Template** — This file is read by `dsrag-ingest` at runtime. NOT a user-facing skill.

# DSRAG Transcript Summary

Extract high-level meeting intelligence and actionable insights from interview or meeting transcripts.

## Invocation

Read by `dsrag-ingest` and passed as prompt to a Task agent.

## Prerequisites

- Project must be initialized with `dsrag-init-project`
- Transcript file must exist in `[projectid]/transcripts/`

## Operating Principle

**Two-stage extraction:**
1. Create processed analysis in `.dsrag/[projectid]/processed/transcripts/[filename]_summary_analysis.md`
2. Extract structured summary to `.dsrag/[projectid]/knowledge/summaries/`

**STRICT RULE:** Output ONLY to defined structure. No auxiliary files.

## Required Output Structure

**Stage 1: Processed Analysis**
- File: `.dsrag/[projectid]/processed/transcripts/summary_[filename].md`
- Contains: Raw notes, speaker analysis, topic identification, quotes

**Stage 2: Structured Knowledge:**
- File: `.dsrag/[projectid]/knowledge/summaries/[filename]_summary.md`
- Contains: Executive summary, participants, topics, decisions, next steps, open questions, sentiment

## Extraction Process

### Step 1: Read transcript file

Read line by line, tracking line numbers for citations.

### Step 2: Identify participants

Extract:
- **Speaker names:** All unique speakers in transcript
- **Roles/titles:** If mentioned in conversation
- **Organizations:** Company affiliations
- **Viewpoints:** Each participant's perspective, concerns, priorities

### Step 3: Extract key topics

For each major topic discussed:
- **Topic title:** Clear, concise description
- **Lines:** Where this topic was discussed
- **Summary:** What was said about this topic
- **Who spoke:** Which participants contributed
- **Significance:** Why this topic matters

**Topic identification signals:**
- Extended discussion (multiple speaker turns on same subject)
- Problems or challenges mentioned
- Solutions or recommendations proposed
- Questions asked and answered (or left open)
- Strategic implications discussed

### Step 4: Identify decisions made

For each decision in the transcript:
- **Decision statement:** What was decided
- **Who decided:** Decision maker(s) — name and role
- **When:** Timestamp or context of when the decision was reached (line reference)
- **Rationale:** Why this decision was made (explicit reasoning or inferred from discussion)
- **Dependencies:** What this decision depends on (prior decisions, resources, approvals, information)
- **Impact:** What this decision affects (systems, people, timelines, other decisions)
- **Alternatives considered:** Other options discussed before deciding
- **Status:** Confirmed / Tentative / Conditional (on what condition)
- **Line references:** Where decision was made

**Decision indicators:**
- "We'll do X"
- "Let's go with Y"
- "Decision to..."
- "We've decided..."
- Approval or rejection of proposals
- Conditional decisions: "If X, then we'll Y"
- Deferred decisions: "We'll decide on X after Y"

**Decision classification:**
- **Strategic:** Affects project direction, scope, or approach
- **Technical:** Affects architecture, technology, or implementation
- **Operational:** Affects process, timeline, or resource allocation
- **Organizational:** Affects team structure, roles, or responsibilities

### Step 5: Extract next steps & action items

For each action item:
- **Action description:** What needs to be done
- **Owner:** Who is responsible (if mentioned)
- **Priority:** Urgency level (if indicated)
- **Context:** Why this action is needed
- **Line references:** Where action was identified

**Action indicators:**
- "Next step is..."
- "We need to..."
- "I'll follow up on..."
- "Action item: ..."
- Future-oriented language ("will", "should", "going to")

### Step 6: Capture open questions

For questions raised but not answered:
- **Question:** Exact question or topic needing resolution
- **Context:** Why this question matters
- **Who asked:** Questioner
- **Related topics:** Connection to other discussion areas
- **Line references:** Where question was raised

**Question indicators:**
- Explicit questions with no answers
- "We still need to figure out..."
- "Not sure about..."
- "Need to understand..."
- "Gap in knowledge..."

### Step 7: Analyze sentiment

Assess overall tone and stakeholder sentiment:
- **Overall sentiment:** Frustrated / Hopeful / Neutral / Excited / Concerned
- **Energy level:** High / Medium / Low
- **Tone indicators:** Specific language revealing emotion
- **Stakeholder dynamics:** Relationships, power dynamics, collaboration quality
- **Key emotional moments:** Line references to significant emotional shifts

**Sentiment indicators:**
- Word choice (positive, negative, neutral)
- Repetition (emphasis on certain points)
- Frustration language ("can't", "unable to", "struggle")
- Hope language ("excited", "looking forward", "opportunity")
- Urgency language ("critical", "must", "need to")

### Step 8: Write executive summary

Create 2-3 paragraph summary capturing:
1. **Paragraph 1:** Main topic of meeting, primary findings or revelations
2. **Paragraph 2:** Key problems, challenges, or opportunities discussed
3. **Paragraph 3:** Strategic implications, decisions, and next steps

**Executive summary principles:**
- Lead with most important information
- Focus on "so what?" (implications, not just facts)
- Highlight surprises or critical discoveries
- Connect to strategic context
- Quantify where possible

### Step 9: Create processed analysis

Write: `.dsrag/[projectid]/processed/transcripts/summary_[filename].md`

**Template:**
```markdown
# Summary Analysis: [filename]

**Project:** [project_id]
**Source:** [projectid]/transcripts/[filename]
**Processed:** [timestamp]

## Participants Identified

### [Participant Name 1]
**Role:** [role/title if mentioned]
**Organization:** [company/dept if mentioned]
**Key Contributions:** [topics they spoke about]
**Viewpoint:** [their perspective, concerns, priorities]

**Lines:** X, Y, Z

---

### [Participant Name 2]
[Similar structure]

## Topics Discussed

### Topic 1: [Topic Title]
**Lines:** X-Y

**Summary:**
[What was discussed]

**Who Spoke:**
- [Participant A]: [their contribution]
- [Participant B]: [their contribution]

**Significance:**
[Why this matters]

**Quotes:**
Line X: "[quote]"

---

### Topic 2: [Topic Title]
[Similar structure]

## Decisions Identified

**Decision 1:** [Decision statement]
- **Classification:** [Strategic|Technical|Operational|Organizational]
- **Who Decided:** [Name (Role)]
- **When:** Line X — [context]
- **Rationale:** [Why — explicit or inferred]
- **Dependencies:** [What this depends on]
- **Impact:** [What this affects]
- **Alternatives:** [What else was considered]
- **Status:** [Confirmed|Tentative|Conditional]
- **Lines:** X-Y

---

## Next Steps Identified

**Action 1:** [Action description]
- **Owner:** [Name if mentioned]
- **Priority:** [High/Medium/Low if indicated]
- **Context:** [Why needed]
- **Lines:** X-Y

---

## Open Questions

**Question 1:** [Question]
- **Context:** [Why this matters]
- **Asked By:** [Name]
- **Related Topics:** [Connections]
- **Lines:** X-Y

---

## Sentiment Observations

**Overall:** [Sentiment]
**Energy:** [Level]

**Key Observations:**
- [Observation 1 with line reference]
- [Observation 2 with line reference]

**Emotional Moments:**
Line X: "[quote showing emotion]" - [Analysis]
```

### Step 10: Extract to structured summary

**Path:** `.dsrag/[projectid]/knowledge/summaries/[filename]_summary.md`

**Naming convention:** Use transcript filename (e.g., `interview-03-part-1_summary.md`)

**Upsert behavior:**
- If summary exists: Error (summaries are snapshot of single meeting, don't append)
- If new: Create summary
- To update existing summary: Reprocess and overwrite

**Summary Template:**
```markdown
# Transcript Summary: [Title/Description]

**Project:** [project_id]
**Source:** [projectid]/transcripts/[filename]
**Processed:** [timestamp]

---

## Executive Summary

[2-3 paragraph summary capturing main findings, problems, and strategic implications]

Paragraph 1: Main topic and primary findings

Paragraph 2: Key problems, challenges, or opportunities

Paragraph 3: Strategic implications and next steps

---

## Participants & Viewpoints

### [Participant Name 1] ([Role])
**Organization:** [Company/Department]
**Responsibilities:** [If mentioned]

**Key Viewpoints:**
- **[Topic Area]:** [Their perspective]
- **[Pain Points]:** [Their concerns]
- **[Priorities]:** [What they care about]

**Quote:** *"[Most impactful quote]"* (Line X)

---

### [Participant Name 2]
[Similar structure]

---

## Key Topics Discussed

### 1. [Topic Title]
**Lines: X-Y**

**Description:**
[What was discussed about this topic]

**Key Points:**
- [Point 1]
- [Point 2]

**Business Impact:**
[Why this matters]

**Quote:** *"[Relevant quote]"* (Line X)

---

### 2. [Topic Title]
[Similar structure]

---

## Decisions Made

### Decision 1: [Decision Title]
**Classification:** [Strategic|Technical|Operational|Organizational]
**Decision:** [What was decided]
**Who Decided:** [Decision maker (Role)]
**Rationale:** [Why this decision was made]
**Dependencies:** [Prior decisions, resources, approvals needed]
**Impact:** [Systems, people, timelines affected]
**Alternatives Considered:** [Other options discussed]
**Status:** [Confirmed|Tentative|Conditional — condition]
**Lines:** X-Y

---

## Next Steps & Action Items

### For [Team/Person A]

**Action Item 1: [Action Title]**
- **Owner:** [Name]
- **Priority:** [High/Medium/Low]
- **Context:** [Why this action is needed]
- **Lines:** X-Y

---

### For [Team/Person B]
[Similar structure]

---

## Open Questions

### Strategic Questions

**Question 1: [Question Topic]**
- [Detailed question]
- **Context:** [Why this matters]
- **Status:** [Unanswered/Partially answered]
- **Related Lines:** X-Y

---

### Technical Questions

**Question 2: [Question Topic]**
[Similar structure]

---

### Operational Questions
[Similar structure]

---

## Sentiment Analysis

### Overall Sentiment: **[Sentiment]**

**[Sentiment Category] Indicators:**
- [Indicator 1 with line reference]
- [Indicator 2 with line reference]

**Energy Level: [High/Medium/Low]**
- [Supporting evidence]

**Tone Indicators:**
- **[Tone Type]:** [Description with examples]

**Stakeholder Dynamics:**
- [Relationship observation 1]
- [Power dynamic observation 2]

**Key Emotional Moments:**

1. **Line X:** *"[Quote]"*
   - **Emotion:** [Analysis of emotional content]

---

## Processing Metadata

**Transcript File:** [projectid]/transcripts/[filename]
**Processing Skill:** dsrag:transcript-summary
**Total Lines:** [count]
**Total Speakers:** [count] ([names])
**Duration:** [if determinable from timestamps]
**Meeting Type:** [Stakeholder interview / Team meeting / Discovery session / etc.]
**Recording:** [Yes/No if mentioned]
**Processed By:** dsrag:transcript-summary v1.0
**Processed Date:** [timestamp]
```

## Citation Format (STRICT)

Every fact MUST reference line numbers:

```markdown
**Quote:** *"[exact quote]"* (Line X)
```

For ranges:
```markdown
**Lines:** X-Y
```

For multiple references:
```markdown
**Lines:** X, Y, Z
```

## Conflict Detection

**Summaries are single-meeting snapshots - no conflict detection needed.**

If reprocessing an existing summary:
- Overwrite previous version
- Update timestamp in metadata
- No upsert/append behavior

## Error Prevention

**DO:**
- Identify all participants (even if brief contribution)
- Cite every fact with line numbers
- Capture all decisions and action items
- Track open questions for follow-up
- Analyze sentiment objectively
- Write executive summary focused on "so what?"
- Use project ID in all paths

**DON'T:**
- Create auxiliary files (drafts, notes)
- Speculate on topics not discussed
- Skip line number citations
- Miss action items or open questions
- Overlook sentiment signals
- Write generic summary (make it specific to this meeting)

## Testing

**Test with:**
- `.claude/agents/dsrag/examples/transcript-summary/test-transcript.txt` (use existing test transcript)
- Project ID: `test-project`

**Expected output documented in:**
- `.claude/agents/dsrag/examples/transcript-summary/expected-output.md`

## Implementation Notes

1. **Participant identification:** Track all speakers even if minimal contribution
2. **Topic boundaries:** Topics can overlap; same line can appear in multiple topics
3. **Decision vs. Discussion:** Distinguish between "we should" (discussion) and "we will" (decision)
4. **Action items:** Explicit actions ("I'll do X") AND implicit actions ("we need to find out Y")
5. **Open questions:** Capture both explicit questions and implied knowledge gaps
6. **Sentiment:** Focus on tone, energy, stakeholder relationships - not just positive/negative
7. **Executive summary:** Lead with most important information; quantify when possible
8. **Line references:** Be precise - help reader find exact location in transcript

## Integration with Other Lenses

**Transcript summaries complement:**
- **Stakeholder profiling** - Participants section feeds into individual profiles
- **Problem extraction** - Topics may reveal problems for separate extraction
- **VSM analysis** - Process discussions may feed value stream mapping

**Summary is the "meeting intelligence" lens** - focuses on:
- What happened in this meeting
- What decisions were made
- What actions are needed
- What questions remain

Other lenses extract domain-specific knowledge (stakeholders, problems, processes).

**Decision tracking enrichment (v4.3):** This lens now captures structured decision records with rationale, dependencies, and impact. This complements:
- **Document analyzer** — captures decisions from formal documents (SOWs, specs)
- **Transcript summary** — captures decisions from verbal discussions (meetings, interviews)
Together, both lenses provide a complete decision trail across all source types.

## Output File Naming

**Processed analysis:** `summary_[original-filename].md`
- Example: `summary_interview-03-part-1.md`

**Structured summary:** `[original-filename]_summary.md`
- Example: `interview-03-part-1_summary.md`

**Rationale:** Subject-prefix naming for processed files (alphabetical grouping by analysis type), filename-suffix naming for knowledge files (grouping by source).
