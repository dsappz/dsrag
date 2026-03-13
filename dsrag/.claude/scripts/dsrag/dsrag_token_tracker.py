#!/usr/bin/env python3
"""
DSRAG Token Usage Tracker

Parses agent output files to extract token usage and calculate costs.
"""

import re
import json
from pathlib import Path
from typing import Dict, List

# Sonnet 4.5 pricing (as of 2026-01-29)
INPUT_TOKEN_COST = 3.00 / 1_000_000   # $3 per million
OUTPUT_TOKEN_COST = 15.00 / 1_000_000  # $15 per million

def extract_token_usage(output_file: Path) -> Dict:
    """Extract token usage from agent output file."""
    if not output_file.exists():
        return {"input": 0, "output": 0, "total": 0}

    content = output_file.read_text()

    # Look for patterns like "Token usage: 5000 input, 2000 output"
    # or structured data in output
    input_tokens = 0
    output_tokens = 0

    # Pattern 1: "Token usage: X/Y"
    match = re.search(r'Token usage: (\d+)/(\d+)', content)
    if match:
        input_tokens = int(match.group(1))
        output_tokens = int(match.group(2))

    # Pattern 2: Look for usage stats
    input_match = re.search(r'(\d+) input tokens', content, re.IGNORECASE)
    output_match = re.search(r'(\d+) output tokens', content, re.IGNORECASE)

    if input_match:
        input_tokens = int(input_match.group(1))
    if output_match:
        output_tokens = int(output_match.group(1))

    return {
        "input": input_tokens,
        "output": output_tokens,
        "total": input_tokens + output_tokens
    }

def calculate_cost(token_usage: Dict) -> float:
    """Calculate cost in USD based on token usage."""
    input_cost = token_usage["input"] * INPUT_TOKEN_COST
    output_cost = token_usage["output"] * OUTPUT_TOKEN_COST
    return input_cost + output_cost

def aggregate_usage(lens_usages: List[Dict]) -> Dict:
    """Aggregate token usage across multiple lenses."""
    total = {"input": 0, "output": 0, "total": 0}

    for usage in lens_usages:
        total["input"] += usage["input"]
        total["output"] += usage["output"]
        total["total"] += usage["total"]

    return total

def format_usage_report(lens_usages: Dict[str, Dict], total: Dict) -> str:
    """Format token usage report."""
    report = []

    # Per-lens breakdown
    for lens_name, usage in lens_usages.items():
        cost = calculate_cost(usage)
        report.append(f"  - {lens_name:20s}: {usage['total']:7,} tokens (${cost:.2f})")

    # Total
    total_cost = calculate_cost(total)
    report.append(f"  - {'Total':20s}: {total['total']:7,} tokens (${total_cost:.2f})")

    return "\n".join(report)

if __name__ == "__main__":
    # Test with dummy data
    test_usage = {
        "stakeholder": {"input": 5000, "output": 1200, "total": 6200},
        "problem": {"input": 6500, "output": 1600, "total": 8100},
        "vsm": {"input": 6200, "output": 1600, "total": 7800},
        "summary": {"input": 5000, "output": 1350, "total": 6350}
    }

    total = aggregate_usage(list(test_usage.values()))
    print(format_usage_report(test_usage, total))
