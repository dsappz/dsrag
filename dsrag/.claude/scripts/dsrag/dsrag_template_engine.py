#!/usr/bin/env python3
"""
DSRAG Template Engine

Process templates with AI synthesis and knowledge base insertion.
"""

import re
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

class TemplateEngine:
    """Template processor with AI synthesis support."""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.kb_path = Path(f".dsrag/{project_id}/knowledge/")

    def load_template(self, template_path: str) -> str:
        """Load template file."""
        with open(template_path, 'r') as f:
            return f.read()

    def extract_placeholders(self, template: str) -> list:
        """
        Extract placeholders from template.

        Supported formats:
        - {{variable}} - Simple variable replacement
        - {{KNOWLEDGE_BASE: path}} - Insert from knowledge base
        - {{AI_SYNTHESIS}} ... {{/AI_SYNTHESIS}} - AI-generated content
        """
        placeholders = []

        # Simple variables
        for match in re.finditer(r'{{([A-Z_]+)}}', template):
            placeholders.append({
                "type": "variable",
                "name": match.group(1),
                "start": match.start(),
                "end": match.end()
            })

        # Knowledge base insertions
        for match in re.finditer(r'{{KNOWLEDGE_BASE:\s*([^}]+)}}', template):
            placeholders.append({
                "type": "knowledge_base",
                "path": match.group(1).strip(),
                "start": match.start(),
                "end": match.end()
            })

        # AI synthesis blocks
        for match in re.finditer(
            r'{{AI_SYNTHESIS}}(.*?){{/AI_SYNTHESIS}}',
            template,
            re.DOTALL
        ):
            placeholders.append({
                "type": "ai_synthesis",
                "prompt": match.group(1).strip(),
                "start": match.start(),
                "end": match.end()
            })

        return placeholders

    def resolve_variable(self, name: str, context: Dict) -> str:
        """Resolve simple variable from context."""
        return context.get(name.lower(), f"[{name} not provided]")

    def resolve_knowledge_base(self, path: str) -> str:
        """Load content from knowledge base."""
        full_path = self.kb_path / path

        if not full_path.exists():
            return f"[Knowledge base not found: {path}]"

        with open(full_path, 'r') as f:
            return f.read()

    def resolve_ai_synthesis(self, prompt: str) -> str:
        """
        Placeholder for AI synthesis.

        In actual implementation, this would:
        1. Load relevant knowledge into context
        2. Call Claude with synthesis prompt
        3. Return generated content

        For now, returns placeholder.
        """
        return f"[AI_SYNTHESIS: {prompt[:100]}...]"

    def process_template(self, template: str, context: Dict) -> str:
        """
        Process template with all placeholders.

        Args:
            template: Template string
            context: Variable context (version, project_id, etc.)

        Returns:
            Processed template
        """
        result = template
        placeholders = self.extract_placeholders(template)

        # Process in reverse order to maintain positions
        for ph in sorted(placeholders, key=lambda x: x["start"], reverse=True):
            if ph["type"] == "variable":
                replacement = self.resolve_variable(ph["name"], context)
            elif ph["type"] == "knowledge_base":
                replacement = self.resolve_knowledge_base(ph["path"])
            elif ph["type"] == "ai_synthesis":
                replacement = self.resolve_ai_synthesis(ph["prompt"])
            else:
                replacement = f"[Unknown placeholder type: {ph['type']}]"

            result = result[:ph["start"]] + replacement + result[ph["end"]:]

        return result

    def generate_deliverable(self, template_path: str, output_path: str,
                           context: Dict) -> str:
        """
        Generate deliverable from template.

        Args:
            template_path: Path to template file
            output_path: Path to output file
            context: Template context

        Returns:
            Output file path
        """
        # Load template
        template = self.load_template(template_path)

        # Add default context
        context.setdefault("project_id", self.project_id)
        context.setdefault("timestamp", datetime.now().isoformat())

        # Process template
        result = self.process_template(template, context)

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Write output
        with open(output_path, 'w') as f:
            f.write(result)

        return output_path

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python dsrag_template_engine.py <project_id> <template> <output>")
        sys.exit(1)

    project_id = sys.argv[1]
    template_path = sys.argv[2]
    output_path = sys.argv[3]

    # Parse context from remaining args (key=value format)
    context = {}
    for arg in sys.argv[4:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            context[key] = value

    engine = TemplateEngine(project_id)
    result = engine.generate_deliverable(template_path, output_path, context)

    print(f"✓ Generated: {result}")
