# Expected Stakeholder Profiling Output

This document defines what `dsrag:stakeholder-profiling` should produce from `test-transcript.txt`

## Test Setup

**Project ID:** `test-project`
**Transcript:** `test-project/transcripts/test-transcript.txt`

## Expected Output Files

### 1. Individual Stakeholder Profiles

**Files in:** `.claude/.dsrag/test-project/knowledge/stakeholders/profiles/`

#### tom.md
- **Role:** Chief Information Officer (CIO)
- **Organization:** City Government, IT Department
- **Reports to:** Janet (City Manager)
- **Responsibilities:** Oversees all IT for the city (~30 people across infrastructure, applications, digital services)
- **Pain Points:** Lack of budget and organizational will to modernize permits/inspections; has been too hands-off with Linda's resistance
- **Personality:** Diplomatic, self-aware about his own shortcomings, avoids forcing change
- **Decision Authority:** Oversees IT strategy, manages Derek
- **Relationships:** Good relationship with Linda (built on trust); manages Derek; Linda sees Derek as Tom's proxy
- **Citations:** All facts cited to transcript lines

#### linda.md
- **Role:** Inspections Division Director
- **Organization:** City Government, Inspections Division
- **Characteristics:** Twenty years of institutional knowledge, knows every building code and process
- **Pain Points:** Distrust of technology based on past failed IT projects
- **Personality:** Resistant to change, highly capable, influential with her team
- **Decision Authority:** De facto veto on technology adoption in inspections (team follows her lead)
- **Relationships:** Good relationship with Tom (trusts him); defensive toward Derek; tension with Marcus over facilities/loading dock; coordinates with Rachel but processes are disconnected
- **Evolution:** Refused scheduling app rollout two years ago; skepticism rooted in experience with failed projects
- **Citations:** All facts cited to transcript lines

#### derek.md
- **Role:** Digital Services Coordinator
- **Organization:** City Government, IT Department
- **Reports to:** Tom
- **Background:** Hired 6 months ago from a tech startup
- **Characteristics:** Sharp, eager, moves fast, lacks institutional knowledge
- **Pain Points:** Getting frustrated; proposals shut down by old-timers; perceived as Tom's proxy by Linda
- **Goals:** Drive modernization, proposed online permit applications
- **Personality:** Enthusiastic but impatient; doesn't yet understand why things are the way they are
- **Citations:** All facts cited to transcript lines

#### rachel.md
- **Role:** Permits Director
- **Organization:** City Government, Permits Office
- **Responsibilities:** Manages 12 staff handling residential/commercial building permits and zoning variances
- **Pain Points:** Paper-based processes; has requested digital system for 3 years; staff turnover (newer people leave quickly); exhausted from fighting for change
- **Personality:** Pragmatic, patient, understands her team's limitations with change
- **Relationships:** Gets along with Marcus; coordinates with Linda but processes are disconnected; receptive to Derek but thinks he moves too fast
- **Citations:** All facts cited to transcript lines

#### marcus.md
- **Role:** Facilities Manager
- **Organization:** City Government, Facilities
- **Responsibilities:** Controls the Municipal Services Center (building where permits office operates); any physical changes to citizen-facing spaces go through him
- **Personality:** Territorial about his building but reasonable if brought in early
- **Relationships:** Gets along with Rachel; has butted heads with Linda over loading dock and vehicle parking (turf conflict)
- **Citations:** All facts cited to transcript lines

### 2. Stakeholder Map

**File:** `.claude/.dsrag/test-project/knowledge/stakeholders/stakeholder_map.md`

**Should contain:**
```markdown
# Stakeholder Map

## Organizational Structure

### Executive Leadership
- **Janet:** City Manager (Tom's boss, not interviewed)
- **Tom:** CIO, oversees all IT (~30 staff)

### IT / Digital Services
- **Derek:** Digital Services Coordinator (reports to Tom)
  - Hired 6 months ago, driving modernization

### Permits Office
- **Rachel:** Permits Director
  - Manages 12 staff (mix of senior and newer hires)

### Inspections Division
- **Linda:** Inspections Director
  - 20 years with the city, deep institutional knowledge

### Facilities
- **Marcus:** Facilities Manager
  - Controls Municipal Services Center

## Reporting Relationships

Janet (City Manager)
  └─ Tom (CIO)
      └─ Derek (Digital Services Coordinator)

Rachel (Permits Director)
  └─ 12 permits staff

Linda (Inspections Director)
  └─ Inspections team

Marcus (Facilities Manager)

## Key Relationships

### Tom <-> Linda
- Good relationship built on trust
- Tom has never forced technology on Linda's team
- Linda may see Derek as Tom's proxy, increasing defensiveness

### Rachel <-> Linda
- Must coordinate on permits-to-inspections handoff
- No shared system; paper copies walked down the hall
- Fine personally but processes are disconnected

### Rachel <-> Marcus
- Get along fine, no significant friction

### Linda <-> Marcus
- Tension over loading dock usage and inspector vehicle parking
- Turf-based conflict; don't naturally collaborate

### Derek <-> Linda / Permits Staff
- Derek's proposals met with resistance from long-tenured staff
- Lacks institutional knowledge to overcome pushback

## Power Dynamics
- Linda has de facto veto power on technology changes (team follows her lead)
- Tom has formal authority but has been too hands-off
- Rachel has been requesting change for 3 years without success
- Derek has the mandate but lacks the credibility and relationships
- Marcus is a gatekeeper for physical space changes
```

## Quality Checks

### MUST Have:
1. Individual profile for each stakeholder mentioned (Tom, Linda, Derek, Rachel, Marcus)
2. All facts cited with line numbers, speaker, quotes
3. Stakeholder map showing relationships
4. Organizational structure when mentioned
5. No speculation - only facts from transcript
6. Upsert behavior (append to existing profiles)

### MUST NOT Have:
1. Assumptions about roles not stated
2. Profiles without citations
3. Auxiliary files (drafts, notes)
4. Speculation about motivations not mentioned

## Citation Format

```markdown
*[Source: test-project/transcripts/test-transcript.txt:4, Tom: "I'm the CIO, I report directly to the city manager, Janet. I oversee all of IT for the city"]*
```

## Baseline Expectations (TDD)

Without the skill, expect:
- No structured profiles
- Missing stakeholder map
- No organizational relationships captured
- Inconsistent citation format
