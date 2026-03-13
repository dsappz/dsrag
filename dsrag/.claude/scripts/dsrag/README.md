# DSRAG Python Scripts

Helper scripts for DSRAG knowledge base management.

## Scripts

### dsrag_init_project.py

Creates/validates project-specific folder structure.

**Architecture:**
- `.claude/.dsrag/[projectid]/knowledge/` - Structured knowledge
- `.claude/.dsrag/[projectid]/processed/` - Processed analysis
- `[projectid]/transcripts/` - Raw interview transcripts
- `[projectid]/documents/` - Raw documents
- `[projectid]/deliverables/` - Project deliverables

**Initialize fresh project:**
```bash
python .claude/scripts/dsrag/dsrag_init_project.py --init \
  --project-id "my-project" \
  --project-name "Client Data Platform" \
  --client-name "ClientCorp"
```

**Validate existing project:**
```bash
python .claude/scripts/dsrag/dsrag_init_project.py --validate --project-id "my-project"
```

**Validate and create missing:**
```bash
python .claude/scripts/dsrag/dsrag_init_project.py --validate --create-missing --project-id "my-project"
```

### dsrag_citation_manager.py

Manages citations.jsonl file for a project.

**Add citation:**
```bash
python .claude/scripts/dsrag/dsrag_citation_manager.py --project-id "my-project" --add \
  --source-file "my-project/transcripts/file.txt" \
  --line-num 123 \
  --snippet "Quote from transcript" \
  --referenced-in ".claude/.dsrag/my-project/knowledge/value_streams/current_state.md:45" \
  --processed-by "dsrag:value-stream-mapping"
```

**Check if source processed:**
```bash
python .claude/scripts/dsrag/dsrag_citation_manager.py --project-id "my-project" \
  --check-processed "my-project/transcripts/file.txt"
```

**List all sources:**
```bash
python .claude/scripts/dsrag/dsrag_citation_manager.py --project-id "my-project" --list-sources
```

## Dependencies

None - uses Python 3.x standard library only.
