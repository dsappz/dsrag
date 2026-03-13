# Deliverable Generation

## Overview

DSRAG generates formatted deliverables from consolidated knowledge using templates. Processing follows three stages:

1. **Variable replacement** -- Static template variables are substituted with project-specific values.
2. **Knowledge base insertion** -- Relevant knowledge base content is pulled into the template.
3. **AI synthesis** -- Claude generates narrative content based on surrounding context and inserted knowledge.

All deliverables include inline citations traced back to source materials.

## Available Templates

### Consulting Framework
- **Business Case** -- Strategic justification and cost-benefit analysis.
- **Stakeholder Analysis** -- Comprehensive stakeholder mapping and influence assessment.
- **RFI Documentation** -- Request for Information response documents.

### DAMA-DMBOK Framework
- **Data Quality Assessment** -- Assessment aligned with DAMA data management body of knowledge standards.

### Cloud Frameworks
- **AWS Well-Architected Review** -- Assessment against AWS Well-Architected Framework pillars.
- **GCP Well-Architected Review** -- Assessment against Google Cloud Architecture Framework.
- **Azure Well-Architected Review** -- Assessment against Azure Well-Architected Framework pillars.

## Usage

```bash
/dsrag-deliver --project-id my-project --framework consulting --template business-case --version 1.0.0
```

## Template Variables

| Variable | Description |
|---|---|
| `{{PROJECT_NAME}}` | Replaced with the project name. |
| `{{KNOWLEDGE_BASE: path}}` | Replaced with file contents from the knowledge base at the specified path. |
| `{{AI_SYNTHESIS}}...{{/AI_SYNTHESIS}}` | Claude generates content based on surrounding context and the knowledge base. |

## Versioning

Deliverables use semantic versioning: **vMAJOR.MINOR.PATCH**.

- **MAJOR** -- Structural or scope changes to the deliverable.
- **MINOR** -- Content additions or significant updates.
- **PATCH** -- Corrections, formatting, or minor refinements.

Use `--version auto` to auto-increment the version based on the last generated version. Each version is tracked with a changelog entry for auditability.
