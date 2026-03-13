# DSRAG Internal Agent Templates

## What Are Agents?

Agents are **internal processing units** (prompt templates) read by orchestrating
skills at runtime. They are NOT user-facing commands.

| Concept | Skills | Agents |
|---------|--------|--------|
| Location | `.claude/skills/` | `.claude/agents/dsrag/` |
| Invoked by | User via `/skill-name` | Orchestrating skill via Task tool |
| Frontmatter | `name:` | `agent:`, `type:`, `invoked-by:` |
| Discoverable | Yes (shows in skill list) | No (internal only) |
| Role | Brain / Orchestrator | Doer / Executor |
| Count | 9 user-facing skills | 5 core lens agents + custom lenses |

## Agent File Format

YAML frontmatter + markdown prompt specification:

```yaml
---
agent: stakeholder-profiling
type: lens          # lens | synthesis
description: ...
invoked-by: dsrag-ingest
---
```

## Agent Types

- **lens** — Extraction agents (read source → write knowledge)
  - `stakeholder-profiling.md` — Extract personas, roles, relationships, pain points
  - `problem-extraction.md` — Identify and categorize problems by type and severity
  - `value-stream-mapping.md` — Extract processes, waste (TIMWOODS), bottlenecks
  - `transcript-summary.md` — Executive summary, decisions, action items, sentiment
  - `document-analyzer.md` — Extract requirements, deliverables, decisions from documents

## How Orchestrators Reference Agents

`dsrag-ingest` reads agent `.md` files at runtime using the Read tool, then
passes the content as the prompt to a Task agent:

```
Step 6.1 (transcripts):
  Read .claude/agents/dsrag/stakeholder-profiling.md → Task agent prompt
  Read .claude/agents/dsrag/problem-extraction.md    → Task agent prompt
  Read .claude/agents/dsrag/value-stream-mapping.md  → Task agent prompt
  Read .claude/agents/dsrag/transcript-summary.md    → Task agent prompt

Step 6.2 (documents):
  Read .claude/agents/dsrag/document-analyzer.md     → Task agent prompt

Step 6.3 (custom lenses, if include_lenses configured):
  Read .claude/agents/dsrag/custom/[lens-name].md → Task agent prompt
```

## Directory Structure

```
.claude/agents/dsrag/
├── README.md                          # This file
├── stakeholder-profiling.md           # Lens: stakeholder extraction
├── problem-extraction.md              # Lens: problem extraction
├── value-stream-mapping.md            # Lens: VSM extraction
├── transcript-summary.md              # Lens: meeting summary
├── document-analyzer.md               # Lens: document analysis
├── examples/                          # Test data per agent
│   ├── stakeholder-profiling/
│   ├── problem-extraction/
│   ├── value-stream-mapping/
│   ├── transcript-summary/
│   └── document-analyzer/
└── custom/                            # Custom lens agents (via /dsrag-create-lens)
    ├── README.md                      # Custom lens conventions
    └── [user-created-lenses].md       # Created by /dsrag-create-lens
```

## Adding a New Agent

1. Create `[agent-name].md` in this directory
2. Add YAML frontmatter with `agent:`, `type:`, `description:`, `invoked-by:`
3. Add header: "This is an internal agent template. NOT a user-facing skill."
4. Write the extraction/processing logic
5. Create test data in `examples/[agent-name]/`
6. Update the orchestrating skill to read and use the new agent template
7. Update this README

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-02 | Initial creation — 5 lens agents migrated from skills |
| 1.1 | 2026-03-02 | Removed utility agents (infra.md, embed.md) — embedding discontinued. File-based approach is the complete knowledge management system. |
| 1.2 | 2026-03-06 | Added custom/ directory for user-created lenses via /dsrag-create-lens. Updated skill count to 9. |
