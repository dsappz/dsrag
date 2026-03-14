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
- Lead time metrics (4-6 weeks current, 2 weeks target)

### 2. Knowledge Files (4 files only)

#### File: `.claude/.dsrag/test-project/knowledge/value_streams/current_state.md`

**Required content:**
- Process flow description (paper form, manual entry, zoning review, engineering review, inspection scheduling, payment)
- Lead time: 4-6 weeks best case, 6-8 weeks typical (cited to lines 7, 17)
- Bottleneck: Two zoning reviewers for entire city (cited to line 5)
- Wait times: 2 weeks zoning, 2 weeks engineering, 3-5 days payment (cited to lines 5, 7, 11)
- Sequential review process (cited to line 7)

**Citation format:**
```markdown
*[Source: test-project/transcripts/test-transcript.txt:7, Rachel: "So best case, you're looking at four to six weeks just to get through review"]*
```

#### File: `.claude/.dsrag/test-project/knowledge/value_streams/waste_analysis.md`

**Required content:**
- TIMWOODS category headers
- **Waiting (W):** Two-week zoning queue, two-week engineering queue, 3-5 day payment processing (cited to lines 5, 7, 11)
- **Transportation (T):** Citizens must physically come to city hall, return trips for forgotten documents (cited to line 1)
- **Over-processing (O):** Full restart required on rejection instead of fixing specific issues (cited to lines 5, 7)
- **Motion (M):** Manual data entry taking 20 minutes per application (cited to line 3)
- **Defects (D):** Double-booked inspections, missed appointments from paper calendars (cited to line 9)

**Example:**
```markdown
## Waiting (W)

**Zoning Review Queue**
Applications wait approximately two weeks in the zoning review queue due to only two reviewers serving the entire city.

*[Source: test-project/transcripts/test-transcript.txt:5, Rachel: "That queue is usually about two weeks because we only have two zoning reviewers for the whole city"]*
```

#### File: `.claude/.dsrag/test-project/knowledge/value_streams/future_state.md`

**Required content:**
- Online portal for application submission and document upload (cited to line 13)
- Automated routing to reviewers (cited to line 15)
- Digital payments (cited to line 17)
- Parallel review instead of sequential (cited to line 17)
- Expected lead time: 2 weeks total turnaround (cited to line 17)

#### File: `.claude/.dsrag/test-project/knowledge/value_streams/gap_analysis.md`

**Required content:**
- Current: 4-6 weeks best case, 6-8 weeks typical
- Future: 2 weeks total turnaround
- Improvement: approximately 70% reduction in lead time
- Key gaps: no online submission, no digital payments, sequential review process, manual data entry, paper-based inspection scheduling
- Citations to both current and future state lines

## Quality Checks

### MUST Have:
1. All 4 knowledge files created (no more, no less)
2. Every factual statement has inline citation
3. Citations include: source file, line number, speaker, quote
4. Waste mapped to TIMWOODS categories
5. Processed analysis preserved in `.dsrag/[projectid]/processed/`

### MUST NOT Have:
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
