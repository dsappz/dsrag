#!/usr/bin/env python3
"""
DSRAG Deliverable Versioning

Semantic versioning for deliverables (major.minor.patch).
"""

import json
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime

def parse_version(version_str: str) -> tuple:
    """Parse version string to tuple (major, minor, patch)."""
    parts = version_str.lstrip('v').split('.')
    return tuple(int(p) for p in parts)

def version_to_string(version_tuple: tuple) -> str:
    """Convert version tuple to string."""
    return f"v{version_tuple[0]}.{version_tuple[1]}.{version_tuple[2]}"

def get_latest_version(project_id: str) -> Optional[str]:
    """Get latest version from deliverables directory."""
    deliverables_path = Path(f".dsrag/{project_id}/deliverables/")

    if not deliverables_path.exists():
        return None

    # Find all version directories
    version_dirs = [
        d.name for d in deliverables_path.iterdir()
        if d.is_dir() and d.name.startswith('v') and d.name != 'current'
    ]

    if not version_dirs:
        return None

    # Parse and sort versions
    versions = [parse_version(v) for v in version_dirs]
    latest = max(versions)

    return version_to_string(latest)

def increment_version(current: str, bump: str = "minor") -> str:
    """
    Increment version.

    Args:
        current: Current version (e.g., "v1.2.3")
        bump: "major", "minor", or "patch"

    Returns:
        New version string
    """
    major, minor, patch = parse_version(current)

    if bump == "major":
        return version_to_string((major + 1, 0, 0))
    elif bump == "minor":
        return version_to_string((major, minor + 1, 0))
    elif bump == "patch":
        return version_to_string((major, minor, patch + 1))
    else:
        raise ValueError(f"Invalid bump type: {bump}")

def create_version_directory(project_id: str, version: str):
    """Create directory for version."""
    version_path = Path(f".dsrag/{project_id}/deliverables/{version}")
    version_path.mkdir(parents=True, exist_ok=True)
    return version_path

def update_current_symlink(project_id: str, version: str):
    """Update 'current' symlink to point to version."""
    deliverables_path = Path(f".dsrag/{project_id}/deliverables/")
    current_link = deliverables_path / "current"

    # Remove existing symlink
    if current_link.exists() or current_link.is_symlink():
        current_link.unlink()

    # Create new symlink
    current_link.symlink_to(version)

def load_changelog(project_id: str) -> list:
    """Load changelog entries."""
    changelog_path = Path(f".dsrag/{project_id}/deliverables/CHANGELOG.md")

    if not changelog_path.exists():
        return []

    # Parse changelog (simplified - just return file content)
    with open(changelog_path, 'r') as f:
        return f.readlines()

def update_changelog(project_id: str, version: str, changes: Dict):
    """
    Update changelog with new version.

    Args:
        project_id: Project identifier
        version: Version string
        changes: Dict with "added", "changed", "removed" lists
    """
    changelog_path = Path(f".dsrag/{project_id}/deliverables/CHANGELOG.md")

    # Load existing or create header
    if changelog_path.exists():
        with open(changelog_path, 'r') as f:
            existing = f.read()
    else:
        existing = "# Deliverable Changelog\n\n"

    # Build new entry
    entry = f"\n## {version} ({datetime.now().strftime('%Y-%m-%d')})\n\n"

    if changes.get("added"):
        entry += "### Added\n"
        for item in changes["added"]:
            entry += f"- {item}\n"
        entry += "\n"

    if changes.get("changed"):
        entry += "### Changed\n"
        for item in changes["changed"]:
            entry += f"- {item}\n"
        entry += "\n"

    if changes.get("removed"):
        entry += "### Removed\n"
        for item in changes["removed"]:
            entry += f"- {item}\n"
        entry += "\n"

    # Insert after header
    parts = existing.split('\n', 2)
    if len(parts) >= 2:
        new_content = parts[0] + '\n' + parts[1] + entry + (parts[2] if len(parts) > 2 else '')
    else:
        new_content = existing + entry

    # Write
    with open(changelog_path, 'w') as f:
        f.write(new_content)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python dsrag_versioning.py <command> [args]")
        print("Commands: latest, increment, create")
        sys.exit(1)

    command = sys.argv[1]

    if command == "latest":
        project_id = sys.argv[2]
        version = get_latest_version(project_id)
        print(version if version else "No versions")

    elif command == "increment":
        current = sys.argv[2]
        bump = sys.argv[3] if len(sys.argv) > 3 else "minor"
        print(increment_version(current, bump))

    elif command == "create":
        project_id = sys.argv[2]
        version = sys.argv[3]
        create_version_directory(project_id, version)
        update_current_symlink(project_id, version)
        print(f"✓ Created {version}, updated 'current' symlink")
