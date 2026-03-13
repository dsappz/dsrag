# Expected Stakeholder Profiling Output

This document defines what `dsrag:stakeholder-profiling` should produce from `test-transcript.txt`

## Test Setup

**Project ID:** `test-project`
**Transcript:** `test-project/transcripts/test-transcript.txt`

## Expected Output Files

### 1. Individual Stakeholder Profiles

**Files in:** `.claude/.dsrag/test-project/knowledge/stakeholders/profiles/`

#### alice.md
- **Role:** Executive / Leadership
- **Organization:** ClientCorp
- **Characteristics:** "always right", decisive
- **Focus Areas:** Client onboarding, ingestion process
- **Influence:** Only person who wanted to tackle client onboarding
- **Citations:** All facts cited to transcript lines

#### frank.md
- **Role:** Lead Architect (new role)
- **Organization:** ClientCorp
- **Reports to:** Bob
- **Responsibilities:** Technical leadership for engagement
- **Team:** Team Member 1, Jack, Team Member 2 (dotted line reporting)
- **Context:** First architect role at ClientCorp
- **Citations:** All facts cited to transcript lines

#### sam.md
- **Role:** Client Solutions (implied)
- **Personality:** Friendly, outgoing, helpful
- **Communication style:** Will text randomly, very approachable
- **Relationship to consultants:** Likes team, wants to help
- **Citations:** All facts cited to transcript lines

#### karen.md
- **Role:** Client Solutions (implied)
- **Personality:** Nice but reserved
- **Background:** Not accustomed to strategic thinking about business
- **Evolution:** Initially touchy when poked about strategy, became more open over time
- **Relationship to consultants:** Likes team, more open to sharing ideas now
- **Citations:** All facts cited to transcript lines

#### bob.md
- **Role:** Executive / Management (Frank's manager)
- **Organization:** ClientCorp
- **Reports:** Frank (direct report)
- **Citations:** All facts cited to transcript lines

### 2. Stakeholder Map

**File:** `.claude/.dsrag/test-project/knowledge/stakeholders/stakeholder_map.md`

**Should contain:**
```markdown
# Stakeholder Map

## Organizational Structure

### Leadership
- **Alice:** Executive, focus on ingestion/onboarding
- **Bob:** Executive, manages Frank

### Technical Team
- **Frank:** Lead Architect (reports to Bob)
  - Dotted line: Team Member 1, Jack, Team Member 2

### Client Solutions
- **Sam:** Friendly, outgoing
- **Karen:** Reserved, growing strategic capability

## Relationships

### Alice ↔ Other Stakeholders
- Championed client onboarding focus
- Others initially resisted discussing ingestion issues

### Sam & Karen ↔ Consulting Team
- Both like the team
- Sam: Very open, friendly
- Karen: Initially guarded, now more open

## Power Dynamics
- Alice has influence to shift focus (only person who pushed onboarding)
- Blame game exists across teams (reported indirectly)
```

## Quality Checks

### ✅ MUST Have:
1. Individual profile for each stakeholder mentioned
2. All facts cited with line numbers, speaker, quotes
3. Stakeholder map showing relationships
4. Organizational structure when mentioned
5. No speculation - only facts from transcript
6. Upsert behavior (append to existing profiles)

### ❌ MUST NOT Have:
1. Assumptions about roles not stated
2. Profiles without citations
3. Auxiliary files (drafts, notes)
4. Speculation about motivations not mentioned

## Citation Format

```markdown
*[Source: test-project/transcripts/test-transcript.txt:7, Grace: "he's now like our lead architect from the ClientCorp side, which they haven't had before"]*
```

## Baseline Expectations (TDD)

Without the skill, expect:
- No structured profiles
- Missing stakeholder map
- No organizational relationships captured
- Inconsistent citation format
