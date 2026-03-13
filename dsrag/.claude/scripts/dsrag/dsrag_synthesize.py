#!/usr/bin/env python3
"""
DSRAG Knowledge Synthesizer

Generates synthesis reports combining knowledge from multiple sources.
Identifies common themes, cross-references information, and preserves citations.
"""

import argparse
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict
from datetime import datetime


def extract_citations(content: str) -> List[Dict[str, str]]:
    """
    Extract all citations from markdown content.

    Citation format: *[Source: project/transcripts/file.txt:123, Speaker: "quote"]*
    """
    pattern = r'\*\[Source: ([^:]+):([^,]+), ([^:]+): "([^"]+)"\]\*'
    citations = []

    for match in re.finditer(pattern, content):
        citations.append({
            'file': match.group(1),
            'location': match.group(2),  # line number or section
            'speaker': match.group(3),
            'quote': match.group(4)
        })

    return citations


def extract_problems(file_path: Path) -> List[Dict[str, any]]:
    """Extract problem records from problem knowledge files."""
    if not file_path.exists():
        return []

    content = file_path.read_text()
    problems = []

    # Pattern: ### PROB-XXX: Title
    problem_pattern = r'### (PROB-\d+): (.+?)(?=###|$)'

    for match in re.finditer(problem_pattern, content, re.DOTALL):
        prob_id = match.group(1)
        problem_block = match.group(2)

        # Extract title (first line)
        lines = problem_block.strip().split('\n')
        title = lines[0].strip()

        # Extract severity
        severity_match = re.search(r'\*\*Severity:\*\* (.+)', problem_block)
        severity = severity_match.group(1).strip() if severity_match else "Unknown"

        # Extract citations
        citations = extract_citations(problem_block)

        problems.append({
            'id': prob_id,
            'title': title,
            'severity': severity,
            'citations': citations,
            'full_text': problem_block
        })

    return problems


def extract_stakeholder_profiles(profiles_dir: Path) -> List[Dict[str, any]]:
    """Extract stakeholder profiles from individual profile files."""
    if not profiles_dir.exists():
        return []

    profiles = []

    for profile_file in profiles_dir.glob('*.md'):
        content = profile_file.read_text()

        # Extract stakeholder name from first heading
        name_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        name = name_match.group(1).strip() if name_match else profile_file.stem

        # Extract citations
        citations = extract_citations(content)

        # Extract pain points section
        pain_points_match = re.search(
            r'## Pain Points & Challenges\s+(.+?)(?=##|$)',
            content,
            re.DOTALL
        )
        pain_points = pain_points_match.group(1).strip() if pain_points_match else ""

        profiles.append({
            'name': name,
            'citations': citations,
            'pain_points': pain_points,
            'full_text': content
        })

    return profiles


def synthesize_problems(project_id: str, project_path: Path) -> str:
    """Generate problem synthesis report."""
    problems_dir = project_path / "knowledge" / "problems"

    # Read all problem files
    all_problems = []
    for category_file in (problems_dir / "by_category").glob("*.md"):
        all_problems.extend(extract_problems(category_file))

    if not all_problems:
        return "No problems found to synthesize."

    # Group by severity
    by_severity = defaultdict(list)
    for problem in all_problems:
        by_severity[problem['severity']].append(problem)

    # Identify common themes (problems mentioned by multiple sources)
    themes = defaultdict(lambda: {'problems': [], 'sources': set()})

    for problem in all_problems:
        # Use problem title for theme grouping (simplified)
        theme_key = problem['title'][:30]  # First 30 chars as rough grouping
        themes[theme_key]['problems'].append(problem)
        for citation in problem['citations']:
            themes[theme_key]['sources'].add(citation['file'])

    # Generate synthesis markdown
    synthesis = f"""# Problem Synthesis

**Project:** {project_id}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Problems:** {len(all_problems)}

## Overview

This synthesis combines problem extractions from all processed transcripts.

## Problems by Severity

"""

    for severity in ['Critical', 'High', 'Medium']:
        problems = by_severity.get(severity, [])
        if problems:
            synthesis += f"### {severity} ({len(problems)} problems)\n\n"
            for prob in problems:
                synthesis += f"**{prob['id']}: {prob['title']}**\n\n"
                # Show unique sources
                sources = set(c['file'] for c in prob['citations'])
                synthesis += f"*Sources: {', '.join(sorted(sources))}*\n\n"

    # Multi-source themes
    synthesis += "\n## Themes Mentioned Across Multiple Sources\n\n"

    multi_source_themes = [(k, v) for k, v in themes.items() if len(v['sources']) > 1]
    multi_source_themes.sort(key=lambda x: len(x[1]['sources']), reverse=True)

    for theme_key, theme_data in multi_source_themes:
        sources_count = len(theme_data['sources'])
        synthesis += f"### {theme_data['problems'][0]['title']} ({sources_count} sources)\n\n"

        for problem in theme_data['problems']:
            synthesis += f"**{problem['id']}:**\n"
            for citation in problem['citations']:
                synthesis += f"- {citation['speaker']} ({citation['file']}): \"{citation['quote']}\"\n"
            synthesis += "\n"

    return synthesis


def synthesize_stakeholders(project_id: str, project_path: Path) -> str:
    """Generate stakeholder synthesis report."""
    stakeholders_dir = project_path / "knowledge" / "stakeholders" / "profiles"

    profiles = extract_stakeholder_profiles(stakeholders_dir)

    if not profiles:
        return "No stakeholder profiles found to synthesize."

    # Identify common pain points mentioned by multiple stakeholders
    pain_point_themes = defaultdict(lambda: {'stakeholders': [], 'details': []})

    for profile in profiles:
        if profile['pain_points']:
            # Simplified theme extraction (in production, use NLP)
            if 'strategic' in profile['pain_points'].lower():
                pain_point_themes['Lack of Strategic Planning']['stakeholders'].append(profile['name'])
                pain_point_themes['Lack of Strategic Planning']['details'].append(
                    profile['pain_points'][:200]
                )

    # Generate synthesis
    synthesis = f"""# Stakeholder Synthesis

**Project:** {project_id}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Stakeholders:** {len(profiles)}

## Overview

This synthesis combines stakeholder profiles from all processed transcripts.

## Stakeholder Overview

"""

    for profile in profiles:
        sources = set(c['file'] for c in profile['citations'])
        synthesis += f"**{profile['name']}** - Mentioned in {len(sources)} source(s)\n"

    synthesis += "\n## Common Themes Across Stakeholders\n\n"

    for theme, data in pain_point_themes.items():
        if len(data['stakeholders']) > 1:
            synthesis += f"### {theme}\n\n"
            synthesis += f"Mentioned by {len(data['stakeholders'])} stakeholders: "
            synthesis += ", ".join(data['stakeholders']) + "\n\n"

    synthesis += "\n## Cross-References\n\n"
    synthesis += "See individual stakeholder profiles for detailed citations and quotes.\n"

    return synthesis


def synthesize_vsm(project_id: str, project_path: Path) -> str:
    """Generate value stream synthesis report."""
    vsm_dir = project_path / "knowledge" / "value_streams"

    if not vsm_dir.exists():
        return "No value stream data found to synthesize."

    # Read VSM files
    current_state = ""
    future_state = ""
    waste_analysis = ""

    if (vsm_dir / "current_state.md").exists():
        current_state = (vsm_dir / "current_state.md").read_text()

    if (vsm_dir / "future_state.md").exists():
        future_state = (vsm_dir / "future_state.md").read_text()

    if (vsm_dir / "waste_analysis.md").exists():
        waste_analysis = (vsm_dir / "waste_analysis.md").read_text()

    # Extract citations
    current_citations = extract_citations(current_state)
    future_citations = extract_citations(future_state)
    waste_citations = extract_citations(waste_analysis)

    # Generate synthesis
    synthesis = f"""# Value Stream Synthesis

**Project:** {project_id}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This synthesis combines value stream mapping insights from all processed transcripts.

## Data Sources

**Current State:** {len(current_citations)} citation(s)
**Future State:** {len(future_citations)} citation(s)
**Waste Analysis:** {len(waste_citations)} citation(s)

## Key Insights

### Current State Summary

{current_state[:500] if current_state else "No current state data"}

### Future State Summary

{future_state[:500] if future_state else "No future state data"}

### Waste Analysis Summary

{waste_analysis[:500] if waste_analysis else "No waste analysis data"}

## Multi-Source Validation

"""

    # Check if current state mentions are from multiple sources
    current_sources = set(c['file'] for c in current_citations)
    if len(current_sources) > 1:
        synthesis += f"Current state validated across {len(current_sources)} sources:\n"
        for source in sorted(current_sources):
            synthesis += f"- {source}\n"

    return synthesis


def main():
    parser = argparse.ArgumentParser(description="DSRAG Knowledge Synthesizer")
    parser.add_argument("--project-id", required=True, help="Project identifier")
    parser.add_argument("--category", required=True,
                       choices=['stakeholders', 'problems', 'value_streams', 'requirements'],
                       help="Knowledge category to synthesize")
    parser.add_argument("--output", help="Output file path (optional, prints to stdout if not provided)")

    args = parser.parse_args()

    # Find project directory
    project_path = Path(f".dsrag/{args.project_id}")

    if not project_path.exists():
        print(f"❌ Error: Project '{args.project_id}' not found at {project_path}")
        exit(1)

    # Generate synthesis based on category
    if args.category == 'problems':
        synthesis_content = synthesize_problems(args.project_id, project_path)
    elif args.category == 'stakeholders':
        synthesis_content = synthesize_stakeholders(args.project_id, project_path)
    elif args.category == 'value_streams':
        synthesis_content = synthesize_vsm(args.project_id, project_path)
    elif args.category == 'requirements':
        synthesis_content = "Requirements synthesis not yet implemented."
    else:
        print(f"❌ Unknown category: {args.category}")
        exit(1)

    # Output synthesis
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(synthesis_content)
        print(f"✓ Synthesis written to: {output_path}")
    else:
        print(synthesis_content)


if __name__ == "__main__":
    main()
