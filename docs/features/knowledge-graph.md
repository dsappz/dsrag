# Knowledge Graph

## What It Does

Scans the knowledge base and generates a Mermaid relationship diagram plus a tabular index showing how stakeholders, problems, decisions, and requirements connect. This provides a visual and structured view of the entire knowledge base at a glance.

## Usage

```bash
/dsrag-kg --project-id my-project
```

## Output

The command produces two artifacts:

- **Mermaid graph** -- A relationship diagram with entity nodes (stakeholders, problems, decisions, requirements) and edges representing their connections.
- **Tabular index** -- A structured table listing all entities, their types, and their relationships.

## Read-Only

This command does not modify the knowledge base. It can be re-run at any time after ingestion to reflect the current state of extracted knowledge.

## Use Cases

- **Visualize stakeholder-problem relationships** -- See which stakeholders are connected to which problems and decisions.
- **Identify orphaned entities** -- Find stakeholders, problems, or requirements that lack connections, indicating potential gaps in the analysis.
- **Validate knowledge completeness** -- Confirm that all expected relationships have been captured across sources.
