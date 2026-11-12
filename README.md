# academic-manuscript

**The front door of an AI-assisted manuscript pipeline: a six-station process (write → markup → translate → cite → clean → export) plus a measured .md manuscript format spec and an ISO-aligned math typesetting standard, with a symbol-registry audit script.**

> [!NOTE]
> This repository is **written and maintained entirely by AI agents** under human direction — see [AI-maintained](#ai-maintained).
> Documentation is English-first; a Chinese README is available ([README.zh-CN.md](README.zh-CN.md)), and a Chinese SKILL companion ([SKILL.zh-CN.md](SKILL.zh-CN.md)).

## Why

An AI in the loop makes manuscript chaos easy: markers left in the delivered file, inconsistent symbol faces across sections, citations keyed to nothing, three versions of the "final" draft. This skill is the single entry point that keeps the pipeline honest:

- **Six stations, one canonical copy**: draft in the working language → marker processing (generate/rewrite/expand/condense/fact-check) → three-pass translation → citation numbering with a generated reference list → marker-stripped clean copy → Word export. The .md file is the only committed artifact; everything downstream is regenerable.
- **Zero-marker delivery gate**: an iron rule that the final copy must scan clean of every marker — a leftover is an incident, not a warning.
- **An ISO 80000-aligned math typesetting standard**: italic scalars, bold-italic vectors, bold-upright tensors, upright dimensionless numbers and differentials, category-driven subscript faces — with settled edge cases and legal examples.
- **A symbol registry with an audit script**: every symbol's face is registered before use; `symbol_audit.py` reports unregistered symbols, face mismatches and `\text` leftovers (reports, never edits), and can scaffold a registry from an existing manuscript.
- **A format spec for the .md manuscript itself**: header block, section structure, author-only hint headings stripped at export, regenerable figure sources, per-manuscript RIS citation pools.

This skill registers interfaces; the implementations live in its companion skills (academic-markup for the marker pipeline, word-standards for the docx layout, lit-symbol-translation for literature symbols, note-gen for the reference library).

## Install as a skill

```
git clone https://github.com/Laitangtang-lab-workflows/academic-manuscript ~/.agents/skills/academic-manuscript
```

Works with any agent harness supporting the SKILL.md convention (Claude Code, DeepSeek Harness, …); the audit script needs Python 3.

## Repository layout

| Path | Content |
|---|---|
| `SKILL.md` | Skill entry point: iron rules, six stations, format spec, math quick reference |
| `references/math-typesetting.md` | The full math typesetting standard |
| `references/manuscript-dir-agents.md` | Manuscript-area AGENTS.md template |
| `scripts/symbol_audit.py` | Symbol-registry audit (report-only) and registry scaffolder |

## AI-maintained

Every file in this repository — code, documentation, this README — is written and updated by AI agents under human supervision. The pipeline exists because AI sessions are the primary writers of these manuscripts; the rules are the guardrails they wrote for themselves. Expect commits to be machine-authored; humans review direction and decisions, not lines.

## License

[CC0-1.0](LICENSE) — released to the public domain. Use, fork and vendor it into anything, no attribution required (a nod is always appreciated).

By submitting a pull request you agree that your contributions are dedicated under CC0 as well.
