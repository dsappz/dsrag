# Expected VSM Extraction

This document defines what `dsrag:value-stream-mapping` should produce from `test-transcript.txt`

## Test Setup

**Project ID:** `test-project`
**Transcript:** `test-project/transcripts/test-transcript.txt`

## Expected Output Files

### 1. Processed Analysis

**File:** `.claude/.dsrag/test-project/processed/transcripts/test-transcript_vsm_analysis.md`

**Should contain:**
- Current state process identification
- Future state improvements
- TIMWOODS waste mapping
- All quotes with line numbers
- Lead time metrics (3-6 months, 4-6 weeks)

### 2. Knowledge Files (4 files only)

#### File: `.claude/.dsrag/test-project/knowledge/value_streams/current_state.md`

**Required content:**
- Process flow description
- Lead time: 3-6 months (cited to line 2)
- Bottleneck: Reactive field mapping (cited to line 2)
- Wait times: weeks for mapping (cited to line 10)

**Citation format:**
```markdown
*[Source: test-project/transcripts/test-transcript.txt:2, Dana: "It can take three to six months just to get the first accurate report out"]*
```

#### File: `.claude/.dsrag/test-project/knowledge/value_streams/waste_analysis.md`

**Required content:**
- TIMWOODS category headers
- **Waiting (W):** Client data mapping delays (cited to line 10)
- **Motion (M):** Manual field mapping (cited to line 2)
- Each waste type linked to specific transcript quotes

**Example:**
```markdown
## Waiting (W)

**Client Data Mapping**
Clients wait weeks while team performs reactive field mapping.

*[Source: test-project/transcripts/test-transcript.txt:10, Dana: "Clients send data, then wait weeks for us to map it"]*
```

#### File: `.claude/.dsrag/test-project/knowledge/value_streams/future_state.md`

**Required content:**
- Automated validation (cited to line 7)
- Metadata-driven ingestion (cited to line 7)
- Expected lead time: 4-6 weeks (cited to line 7)

#### File: `.claude/.dsrag/test-project/knowledge/value_streams/gap_analysis.md`

**Required content:**
- Current: 3-6 months
- Future: 4-6 weeks
- Improvement: 67% reduction
- Citations to both current and future state lines

## Quality Checks

### ✅ MUST Have:
1. All 4 knowledge files created (no more, no less)
2. Every factual statement has inline citation
3. Citations include: source file, line number, speaker, quote
4. Waste mapped to TIMWOODS categories
5. Processed analysis preserved in `.dsrag/[projectid]/processed/`

### ❌ MUST NOT Have:
1. Additional files in `knowledge/value_streams/` (no drafts, notes, temp files)
2. Facts without citations
3. Generic waste categories without specific examples
4. Processed analysis without line numbers

## Baseline Test (RED Phase)

**Without the skill, expect these failures:**
1. No structured output to `.dsrag/` folders
2. No citation format with line numbers
3. No TIMWOODS waste categorization
4. No separation of processed analysis vs knowledge
5. May create auxiliary files (drafts, summaries, etc.)
6. May not upsert to existing files correctly
