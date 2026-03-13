#!/usr/bin/env python3
"""
DSRAG Citation Manager

Manages citations.jsonl file with CRUD operations.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime


def load_citations(citations_file):
    """Load all citations from JSONL file."""
    citations = []
    if Path(citations_file).exists():
        with open(citations_file, 'r') as f:
            for line in f:
                if line.strip():
                    citations.append(json.loads(line))
    return citations


def save_citation(citations_file, citation):
    """Append citation to JSONL file."""
    with open(citations_file, 'a') as f:
        f.write(json.dumps(citation) + '\n')


def add_citation(citations_file, source_file, line_num, snippet, referenced_in, processed_by):
    """Add new citation."""
    citations = load_citations(citations_file)

    # Generate ID
    cite_id = f"cite_{len(citations) + 1:03d}"

    # Determine source type
    source_type = "transcript" if "transcripts/" in source_file else "document"

    citation = {
        "id": cite_id,
        "source_type": source_type,
        "source_file": source_file,
        "line_number": line_num,
        "content_snippet": snippet,
        "referenced_in": [referenced_in] if isinstance(referenced_in, str) else referenced_in,
        "timestamp": datetime.now().isoformat(),
        "processed_by": processed_by
    }

    save_citation(citations_file, citation)
    print(f"✓ Added citation {cite_id}")
    return cite_id


def check_processed(citations_file, source_file):
    """Check if source file already processed."""
    citations = load_citations(citations_file)
    for cite in citations:
        if cite.get("source_file") == source_file:
            return True
    return False


def list_sources(citations_file):
    """List all unique source files."""
    citations = load_citations(citations_file)
    sources = set(cite.get("source_file") for cite in citations)
    return sorted(sources)


def main():
    parser = argparse.ArgumentParser(description="DSRAG citation manager")
    parser.add_argument("--project-id", required=True, help="Project ID")
    parser.add_argument("--add", action="store_true", help="Add new citation")
    parser.add_argument("--check-processed", help="Check if source file processed")
    parser.add_argument("--list-sources", action="store_true", help="List all sources")

    # For --add
    parser.add_argument("--source-file", help="Source file path")
    parser.add_argument("--line-num", type=int, help="Line number")
    parser.add_argument("--snippet", help="Content snippet")
    parser.add_argument("--referenced-in", help="Knowledge file reference")
    parser.add_argument("--processed-by", help="Skill that processed")

    args = parser.parse_args()

    # Build citations file path from project ID
    citations_file = f".dsrag/{args.project_id}/knowledge/_meta/citations.jsonl"

    if args.add:
        if not all([args.source_file, args.snippet, args.referenced_in, args.processed_by]):
            print("Error: --add requires --source-file, --snippet, --referenced-in, --processed-by")
            sys.exit(1)
        add_citation(
            citations_file,
            args.source_file,
            args.line_num or 0,
            args.snippet,
            args.referenced_in,
            args.processed_by
        )
    elif args.check_processed:
        if check_processed(citations_file, args.check_processed):
            print(f"✓ {args.check_processed} already processed")
            sys.exit(0)
        else:
            print(f"✗ {args.check_processed} not yet processed")
            sys.exit(1)
    elif args.list_sources:
        sources = list_sources(citations_file)
        print(f"Processed sources ({len(sources)}):")
        for source in sources:
            print(f"  - {source}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
