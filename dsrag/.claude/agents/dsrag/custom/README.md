# Custom Lens Agents

Custom extraction lenses created via `/dsrag-create-lens`.

These agents are auto-discovered by `dsrag-init-project` and run alongside core lenses by `dsrag-ingest` when included in a project's `include_lenses` config.

## Convention

- One `.md` file per lens
- Same frontmatter format as core agents (`agent:`, `type: lens`, `invoked-by: dsrag-ingest`)
- Same two-stage output pattern (processed analysis → structured knowledge)
- Portable: copy `.claude/` to new project, custom lenses come along
