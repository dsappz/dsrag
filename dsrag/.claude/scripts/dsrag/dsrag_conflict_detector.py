#!/usr/bin/env python3
"""
DSRAG Conflict Detector

Detects contradictions between existing knowledge and new assertions.
Used during upsert operations to prompt user for resolution.
"""

import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional


def extract_quantitative_values(text: str) -> List[Tuple[float, str]]:
    """Extract numbers with units from text (e.g., '3-6 months', '9 months', '67%')."""
    patterns = [
        r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(months?|weeks?|days?|years?|%)',
        r'(\d+(?:\.\d+)?)\s*(months?|weeks?|days?|years?|%)',
    ]

    values = []
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            if '-' in match.group(0):
                # Range: take midpoint
                val1 = float(match.group(1))
                val2 = float(match.group(2))
                unit = match.group(3)
                values.append(((val1 + val2) / 2, unit))
            else:
                val = float(match.group(1))
                unit = match.group(2)
                values.append((val, unit))

    return values


def normalize_unit(value: float, unit: str) -> Tuple[float, str]:
    """Normalize time units to a common base (days)."""
    unit_lower = unit.lower()

    # Time conversions
    if 'year' in unit_lower:
        return (value * 365, 'days')
    elif 'month' in unit_lower:
        return (value * 30, 'days')  # Approximate
    elif 'week' in unit_lower:
        return (value * 7, 'days')
    elif 'day' in unit_lower:
        return (value, 'days')
    elif '%' in unit_lower:
        return (value, '%')

    return (value, unit)


def detect_quantitative_conflict(existing_text: str, new_text: str, threshold: float = 0.3) -> Optional[Dict]:
    """
    Detect conflicts in quantitative values (times, percentages).

    Returns conflict dict if values differ by more than threshold (30% default).
    """
    existing_values = extract_quantitative_values(existing_text)
    new_values = extract_quantitative_values(new_text)

    if not existing_values or not new_values:
        return None

    # Compare values with same units
    for existing_val, existing_unit in existing_values:
        for new_val, new_unit in new_values:
            # Normalize to common units
            norm_existing_val, norm_unit_e = normalize_unit(existing_val, existing_unit)
            norm_new_val, norm_unit_n = normalize_unit(new_val, new_unit)

            # Only compare if units match after normalization
            if norm_unit_e == norm_unit_n:
                # Check if difference exceeds threshold
                if norm_existing_val > 0:
                    diff_pct = abs(norm_new_val - norm_existing_val) / norm_existing_val

                    if diff_pct > threshold:
                        return {
                            'type': 'quantitative',
                            'existing_value': f"{existing_val} {existing_unit}",
                            'new_value': f"{new_val} {new_unit}",
                            'difference_pct': round(diff_pct * 100, 1),
                            'threshold_pct': threshold * 100
                        }

    return None


def detect_categorical_conflict(existing_text: str, new_text: str, keywords: List[str]) -> Optional[Dict]:
    """
    Detect conflicts in categorical assertions (e.g., severity: critical vs. high).

    keywords: List of mutually exclusive terms to check for.
    """
    existing_lower = existing_text.lower()
    new_lower = new_text.lower()

    existing_match = None
    new_match = None

    for keyword in keywords:
        if keyword.lower() in existing_lower:
            existing_match = keyword
        if keyword.lower() in new_lower:
            new_match = keyword

    if existing_match and new_match and existing_match != new_match:
        return {
            'type': 'categorical',
            'existing_category': existing_match,
            'new_category': new_match,
            'keywords': keywords
        }

    return None


def detect_conflicts(existing_file: str, new_assertion: str, context: str = "") -> List[Dict]:
    """
    Main conflict detection function.

    Args:
        existing_file: Path to existing knowledge file
        new_assertion: New text being added
        context: Context about what's being compared (e.g., "lead time", "severity")

    Returns:
        List of conflict dicts (empty if no conflicts)
    """
    if not Path(existing_file).exists():
        return []  # No existing file, no conflict

    # Read existing content
    with open(existing_file, 'r') as f:
        existing_content = f.read()

    conflicts = []

    # Detect quantitative conflicts (times, percentages, numbers)
    quant_conflict = detect_quantitative_conflict(existing_content, new_assertion)
    if quant_conflict:
        quant_conflict['context'] = context
        conflicts.append(quant_conflict)

    # Detect categorical conflicts based on context
    if 'severity' in context.lower() or 'priority' in context.lower():
        severity_keywords = ['critical', 'high', 'medium', 'low']
        cat_conflict = detect_categorical_conflict(existing_content, new_assertion, severity_keywords)
        if cat_conflict:
            cat_conflict['context'] = context
            conflicts.append(cat_conflict)

    return conflicts


def format_conflict_report(conflicts: List[Dict], existing_source: str, new_source: str) -> str:
    """Format conflicts for user-friendly display."""
    if not conflicts:
        return ""

    report = "⚠️  CONFLICT DETECTED\n\n"

    for i, conflict in enumerate(conflicts, 1):
        report += f"Conflict #{i}: {conflict.get('context', 'Unknown context')}\n"
        report += f"{'=' * 60}\n"

        if conflict['type'] == 'quantitative':
            report += f"Existing: {conflict['existing_value']}\n"
            report += f"Source: {existing_source}\n\n"
            report += f"New: {conflict['new_value']}\n"
            report += f"Source: {new_source}\n\n"
            report += f"Difference: {conflict['difference_pct']}% (threshold: {conflict['threshold_pct']}%)\n"

        elif conflict['type'] == 'categorical':
            report += f"Existing: {conflict['existing_category']}\n"
            report += f"Source: {existing_source}\n\n"
            report += f"New: {conflict['new_category']}\n"
            report += f"Source: {new_source}\n\n"

        report += "\n"

    return report


def main():
    parser = argparse.ArgumentParser(description="DSRAG conflict detector")
    parser.add_argument("--existing-file", required=True, help="Path to existing knowledge file")
    parser.add_argument("--new-assertion", required=True, help="New text being added")
    parser.add_argument("--context", default="", help="Context for comparison (e.g., 'lead time', 'severity')")
    parser.add_argument("--existing-source", default="Existing knowledge", help="Source citation for existing")
    parser.add_argument("--new-source", default="New source", help="Source citation for new")
    parser.add_argument("--threshold", type=float, default=0.3, help="Conflict threshold (default 0.3 = 30%%)")

    args = parser.parse_args()

    conflicts = detect_conflicts(args.existing_file, args.new_assertion, args.context)

    if conflicts:
        print(format_conflict_report(conflicts, args.existing_source, args.new_source))
        exit(1)  # Exit code 1 indicates conflict detected
    else:
        print("✓ No conflicts detected")
        exit(0)  # Exit code 0 indicates no conflict


if __name__ == "__main__":
    main()
