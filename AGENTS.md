# Project documentation workflow

When the user says they are about to push or asks for a pre-push documentation update:

- Review the working tree changes and relevant commits. Include untracked source files; exclude virtual environments and generated files.
- Update `CHANGELOG.md` with concise, beginner-friendly notes about what changed, why, and what was actually verified. Do not invent test results.
- Update an existing entry for the same batch of work instead of duplicating it. Preserve earlier development history and use dated entries for new batches.
- Update `README.md` when setup, usage, or current behavior changes.
- Prepare documentation before the user commits and pushes. Do not commit or push unless requested. There is no automatic push hook configured for this workflow.

The project prioritizes the owner's learning of Python and ML while building toward an ASL learning app. Keep explanations approachable and changes easy to understand.
