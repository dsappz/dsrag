#!/usr/bin/env python3
"""
DSRAG Project Initialization Script

Creates project-specific folder structure for DSRAG knowledge base.
Architecture:
- .dsrag/[projectid]/knowledge/ - Structured knowledge
- .dsrag/[projectid]/processed/ - Processed analysis
- [projectid]/transcripts/ - Raw interview transcripts
- [projectid]/documents/ - Raw documents
- [projectid]/deliverables/ - Project deliverables
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime


def sanitize_project_id(project_id):
    """Convert project ID to filesystem-safe format."""
    # Convert to lowercase, replace spaces/special chars with hyphens
    sanitized = re.sub(r'[^a-z0-9-]', '-', project_id.lower())
    # Remove multiple consecutive hyphens
    sanitized = re.sub(r'-+', '-', sanitized)
    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')
    return sanitized


def get_dsrag_folders(project_id):
    """Get list of DSRAG internal folders."""
    return [
        f".dsrag/{project_id}",
        f".dsrag/{project_id}/processed",
        f".dsrag/{project_id}/processed/transcripts",
        f".dsrag/{project_id}/processed/documents",
        f".dsrag/{project_id}/knowledge",
        f".dsrag/{project_id}/knowledge/_meta",
        f".dsrag/{project_id}/knowledge/value_streams",
        f".dsrag/{project_id}/knowledge/stakeholders",
        f".dsrag/{project_id}/knowledge/stakeholders/profiles",
        f".dsrag/{project_id}/knowledge/problems",
        f".dsrag/{project_id}/knowledge/requirements",
        f".dsrag/{project_id}/knowledge/capabilities",
        f".dsrag/{project_id}/knowledge/architecture",
        f".dsrag/{project_id}/knowledge/architecture/business",
        f".dsrag/{project_id}/knowledge/architecture/application",
        f".dsrag/{project_id}/knowledge/architecture/data",
        f".dsrag/{project_id}/knowledge/architecture/technology",
        f".dsrag/{project_id}/knowledge/architecture/security",
        f".dsrag/{project_id}/knowledge/decisions",
        f".dsrag/{project_id}/knowledge/risks",
    ]


def get_project_folders(project_id):
    """Get list of project data folders (outside .dsrag)."""
    return [
        f"{project_id}",
        f"{project_id}/transcripts",
        f"{project_id}/documents",
        f"{project_id}/deliverables",
    ]


def create_folder_structure(project_root, project_id):
    """Create all DSRAG and project folders."""
    created = []

    # Create DSRAG internal folders
    for folder in get_dsrag_folders(project_id):
        folder_path = Path(project_root) / folder
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            created.append(str(folder))

    # Create project data folders
    for folder in get_project_folders(project_id):
        folder_path = Path(project_root) / folder
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            created.append(str(folder))

    return created


def create_initial_files(project_root, project_id, project_name, client_name):
    """Create initial metadata files."""
    created_files = []

    # Create project_charter.md
    charter_path = Path(project_root) / f".dsrag/{project_id}/knowledge/_meta/project_charter.md"
    if not charter_path.exists():
        charter_content = f"""# Project Charter

**Project ID:** {project_id}
**Project Name:** {project_name}
**Client:** {client_name}
**Created:** {datetime.now().strftime('%Y-%m-%d')}

## Objectives
[To be filled in]

## Scope
[To be filled in]

## Key Deliverables
[To be filled in]

## Key Stakeholders
[To be filled in]
"""
        charter_path.write_text(charter_content)
        created_files.append(str(charter_path))

    # Create citations.jsonl
    citations_path = Path(project_root) / f".dsrag/{project_id}/knowledge/_meta/citations.jsonl"
    if not citations_path.exists():
        citations_path.write_text("")  # Empty file, will append JSONL lines
        created_files.append(str(citations_path))

    # Create knowledge_index.md
    index_path = Path(project_root) / f".dsrag/{project_id}/knowledge/_meta/knowledge_index.md"
    if not index_path.exists():
        index_content = f"""# Knowledge Index

**Project:** {project_name} ({project_id})
**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Files in Knowledge Base

This file tracks what structured knowledge exists and when it was last updated.

(Auto-updated by DSRAG commands)
"""
        index_path.write_text(index_content)
        created_files.append(str(index_path))

    # Create config.json
    config_path = Path(project_root) / f".dsrag/{project_id}/config.json"
    if not config_path.exists():
        config = {
            "project_id": project_id,
            "project_name": project_name,
            "client_name": client_name,
            "created": datetime.now().isoformat(),
            "version": "1.0"
        }
        config_path.write_text(json.dumps(config, indent=2))
        created_files.append(str(config_path))

    # Create project README.md
    readme_path = Path(project_root) / f"{project_id}/README.md"
    if not readme_path.exists():
        readme_content = f"""# {project_name}

**Project ID:** `{project_id}`
**Client:** {client_name}
**Created:** {datetime.now().strftime('%Y-%m-%d')}

## Folder Structure

- `transcripts/` - Raw interview transcripts
- `documents/` - Raw source documents (SOWs, diagrams, etc.)
- `deliverables/` - Project deliverables

## DSRAG Knowledge Base

Structured knowledge is maintained in `.dsrag/{project_id}/`

To process new content:
```bash
dsrag:add-transcript {project_id}/transcripts/[file]
```
"""
        readme_path.write_text(readme_content)
        created_files.append(str(readme_path))

    return created_files


def validate_structure(project_root, project_id, create_missing=False):
    """Validate folder structure, optionally create missing."""
    missing = []
    all_folders = get_dsrag_folders(project_id) + get_project_folders(project_id)

    for folder in all_folders:
        folder_path = Path(project_root) / folder
        if not folder_path.exists():
            missing.append(str(folder))
            if create_missing:
                folder_path.mkdir(parents=True, exist_ok=True)

    return missing


def main():
    parser = argparse.ArgumentParser(description="DSRAG project initialization")
    parser.add_argument("--init", action="store_true", help="Initialize fresh project structure")
    parser.add_argument("--validate", action="store_true", help="Validate existing project structure")
    parser.add_argument("--create-missing", action="store_true", help="Create missing folders during validation")
    parser.add_argument("--project-root", default=".", help="Project root directory (workspace root)")
    parser.add_argument("--project-id", required=True, help="Project ID (will be sanitized)")
    parser.add_argument("--project-name", default="", help="Project name (for init)")
    parser.add_argument("--client-name", default="", help="Client name (for init)")

    args = parser.parse_args()

    # Sanitize project ID
    project_id = sanitize_project_id(args.project_id)

    if project_id != args.project_id:
        print(f"ℹ Project ID sanitized: '{args.project_id}' → '{project_id}'")

    if args.init:
        print(f"Initializing DSRAG project: {project_id}")
        created_folders = create_folder_structure(args.project_root, project_id)
        print(f"✓ Created {len(created_folders)} folders")

        created_files = create_initial_files(
            args.project_root,
            project_id,
            args.project_name or args.project_id,
            args.client_name or "Unnamed Client"
        )
        print(f"✓ Created {len(created_files)} files")
        print(f"\n✓ Project initialized:")
        print(f"  - DSRAG artifacts: .dsrag/{project_id}/")
        print(f"  - Project data: {project_id}/")

    elif args.validate:
        print(f"Validating DSRAG project structure: {project_id}")
        missing = validate_structure(args.project_root, project_id, args.create_missing)

        if missing and not args.create_missing:
            print(f"⚠ Missing {len(missing)} folders:")
            for folder in missing:
                print(f"  - {folder}")
            print("\nRun with --create-missing to create them")
            sys.exit(1)
        elif missing and args.create_missing:
            print(f"✓ Created {len(missing)} missing folders")
        else:
            print("✓ Structure validated - all folders present")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
