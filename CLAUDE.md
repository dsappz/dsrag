# DSRAG — Public Repository

This repository is the community hub for DSRAG (Document-Source Retrieval Augmented Generation).

## Repository Structure

- `docs/` — Community documentation: guides, architecture, feature explanations
- `dsrag/` — The installable DSRAG system (copy into your project)
- `CONTRIBUTING.md` — How to contribute

## For Users

To use DSRAG, copy the `dsrag/` directory into your project root. See [Getting Started](docs/getting-started.md).

## For Contributors

1. Read [docs/content-guide.md](docs/content-guide.md) for format specifications
2. Read [docs/extending-dsrag.md](docs/extending-dsrag.md) for extension guides
3. Follow the issue-first workflow in [CONTRIBUTING.md](CONTRIBUTING.md)

## Conventions

- All documentation uses Markdown
- No emojis in documentation or code
- Lens agent templates use YAML frontmatter
- Citations follow strict format: `*[Source: project/type/file:line, Speaker: "quote"]*`
- Delivery templates use `{{VARIABLE}}` syntax

## License

[Business Source License 1.1](LICENSE)
