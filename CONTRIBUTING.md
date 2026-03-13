# Contributing to DSRAG

Thank you for your interest in contributing to DSRAG. We welcome contributions of new extraction lenses, delivery templates, bug fixes, and documentation improvements.

## Issue-First Workflow

All contributions start with a GitHub issue. This ensures alignment before you invest time writing code.

1. **Create a GitHub issue** describing your proposed contribution and its motivation.
2. **Wait for maintainer feedback** -- the maintainer will approve, suggest changes, or discuss the approach.
3. **Create a branch** and implement your change following the [Content Guide](docs/content-guide.md).
4. **Submit a Pull Request** linked to the approved issue.
5. **Review cycle** -- the maintainer reviews your PR, may request changes, then merges.

## What You Can Contribute

- **New extraction lenses** -- agent templates in `dsrag/.claude/agents/dsrag/custom/`
- **New delivery templates** -- in `dsrag/.claude/skills/dsrag-deliver/templates/`
- **Bug fixes and improvements** -- to existing lenses, skills, or Python scripts
- **Documentation** -- improvements to `docs/`, tutorials, examples

## Contribution Requirements

- Must include example test data and expected output, following the pattern in `dsrag/.claude/agents/dsrag/examples/`.
- Must follow citation format and output directory conventions from the [Content Guide](docs/content-guide.md).
- PR description must reference the approved issue number (e.g., "Closes #12").
- New lenses must include YAML frontmatter with required fields.

## Code of Conduct

We are committed to providing a welcoming and respectful environment for everyone. Be constructive, be kind, be patient.

## License

By submitting a contribution, you agree that your contribution will be licensed under the same [Business Source License 1.1](LICENSE) that covers the project.
