# Getting Started

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed and configured
- Python 3.x (for utility scripts)

## Installation

Copy the `dsrag/` directory from this repository into the root of your project:

```bash
cp -r dsrag/ /path/to/your-project/
```

This places the DSRAG skills, agents, and scripts into your project's `.claude/` directory.

## Initialize Your Project

```bash
/dsrag-init-project --project-id my-project
```

This creates the following directory structure:

```
.dsrag/my-project/
├── config.json
├── knowledge/
│   ├── stakeholders/profiles/
│   ├── problems/by_category/ and by_priority/
│   ├── vsm/
│   ├── summaries/
│   └── _meta/citations.jsonl
└── processed/
```

- **config.json** -- project-level settings and metadata.
- **knowledge/** -- extracted insights organized by analytical lens.
- **processed/** -- tracking state so files are not re-processed.

## Add Source Files

Place transcripts in `my-project/transcripts/` and documents in `my-project/documents/`.

Supported formats: `.txt`, `.md`

Transcripts should follow this format:

```
Speaker Name | Timestamp
What they said goes here...
```

## Ingest and Extract Knowledge

```bash
/dsrag-ingest --project-id my-project
```

The ingest skill auto-discovers new files, processes each source through five analytical lenses in parallel, and skips files that have already been processed. Expect roughly 2--3 minutes per transcript at an estimated cost of $0.40--0.64 per transcript.

## Explore Your Knowledge

After ingestion, browse the extracted knowledge directly:

```bash
cat .dsrag/my-project/knowledge/stakeholders/stakeholder_map.md
cat .dsrag/my-project/knowledge/problems/problem_index.md
cat .dsrag/my-project/knowledge/summaries/interview-1_summary.md
```

Every extracted fact includes a citation back to its source. For example:

```markdown
**Title:** VP of Data
*[Source: my-project/transcripts/interview.txt:42, Grace: "Alice is our VP of Data"]*
```

## Consolidate and Generate Deliverables

Once ingestion is complete, consolidate knowledge across all sources and then generate formatted deliverables:

```bash
/dsrag-consolidate --project-id my-project
/dsrag-deliver --project-id my-project --framework consulting --template business-case --version 1.0.0
```

Consolidation aggregates individual extractions into unified reference documents. Delivery formats the consolidated knowledge into a structured output appropriate for the chosen framework and template.

## Common Workflows

- **Weekly ingestion:** Add new transcript or document files, then run `/dsrag-ingest`. Only new files are processed; previously ingested sources are skipped automatically.
- **Dry run:** Preview what would be processed without actually running extraction:
  ```bash
  /dsrag-ingest --project-id my-project --dry-run
  ```
- **Force reprocess:** Re-run extraction on all files, including those already processed:
  ```bash
  /dsrag-ingest --project-id my-project --force
  ```

## Cost and Performance

| Scenario | Time | Estimated Cost |
|---|---|---|
| Single transcript (parallel) | ~2-3 min | ~$0.40-0.64 |
| 10 transcripts (batched) | ~30-40 min | ~$4.00-6.40 |

Costs are based on Claude Sonnet pricing. Incremental processing means you only pay for new sources.

## Skill Reference

| Command | What It Does |
|---|---|
| `/dsrag-init-project` | Initialize project structure |
| `/dsrag-ingest` | Process sources through analytical lenses |
| `/dsrag-consolidate` | Aggregate knowledge into reference docs |
| `/dsrag-deliver` | Generate formatted deliverables |
| `/dsrag-kg` | Visualize entity relationships |
| `/dsrag-create-lens` | Create a custom extraction lens |
| `/dsrag-pm-update` | Generate PM status report |
| `/dsrag-visualize` | Visual validation of consolidated knowledge |
| `/dsrag-reset-project` | Archive and reset project data |
