# Manuscript-area AGENTS.md template (generated with the work skeleton)

> The `手稿\` scaffold is generated together with the work skeleton: `AGENTS.md` (copy this template verbatim) + the empty `reference\` and `figures\` directories (each with a `.gitkeep` placeholder). The skeleton checklist lives in the openfoam-research-init skill (audit-and-tooling §6); once generated it is an instance — humans may extend freely. The symbol registry is **not** pre-built — it is created with the first manuscript via `symbol_audit.py --scaffold`, after which the pointer line below can become a real link.

# AGENTS.md

Manuscript format specification, math typesetting and the six-station processing pipeline (writing → markup processing → translation → citation numbering → clean copy → Word) all go through the `academic-manuscript` skill — load it before writing.

**Layout**: the .md canonical manuscripts live in this directory; `reference\` = the RIS/ENW citation pool (held per work; the resolution source of academic-markup `refs` — re-running `refs` requires this directory as the working directory, or `--root` pointing at it, otherwise volume/issue/pages fail to resolve and the reference list falls back to index-level metadata); `figures\` = manuscript figures (every figure source must be regenerable: derived data figures or vector-software png/tiff exports).

**Symbol registry**: `符号登记表.md` — the face registry of this work's manuscript symbols (register a new symbol before use; face rules live in the skill); created with the first manuscript, not pre-built at scaffolding.
