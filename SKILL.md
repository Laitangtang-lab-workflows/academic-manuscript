---
name: academic-manuscript
description: >-
  Academic manuscript processing pipeline and .md manuscript format specification (the pipeline front door): a six-station pipeline writing → markup processing → translation → citation numbering → clean copy → Word export, an eight-part manuscript format spec, and a math typesetting standard (italic scalars, bold-italic vectors, bold-upright tensors, upright dimensionless numbers and differentials, category-driven subscripts — the former "Math Format Spec v2" merged in). Use when writing or revising an academic manuscript, defining the .md manuscript format, typesetting math, running the gg/rr/tt/vv marker pipeline, translating Chinese→English, generating citation numbers and reference lists, stripping markers for the clean copy, or exporting to Word. This skill registers interfaces only: marker implementation in academic-markup, document layout in word-standards; math typesetting is mandatory only in the manuscript domain, advisory in research documents. Chinese companion: SKILL.zh-CN.md.
---

# Academic Manuscript — the manuscript pipeline and format specification

The **pipeline front door and format source of truth** for academic manuscripts (the .md file is the single canonical copy). Read this skill before drafting, processing, translating or exporting; it registers interfaces and formats only — implementations live in the companion skills (§4).

## 0. Iron rules

1. **Zero markers in the final copy**: before delivery or Word export, scan the whole text for leftover `gg/rr/tt/vv/ee/cc` and `[['']]` markers — **a leftover is an incident; do not ship**.
2. **The .md manuscript is the only canonical copy** (version-controlled); the clean copy and the docx are pipeline products — regenerable, never committed.
3. **The math typesetting standard is mandatory only in the manuscript domain**; derivations in research documents follow it as advice, never as a health-check item.
4. **Before any symbol or numerical value from the literature enters a manuscript**, pass it through `lit-symbol-translation` (explicit mapping + numerical recomputation).

## 1. The six-station pipeline

| Station | Action | Carried by | Key points |
|---|---|---|---|
| 1 Writing | draft in the working language | the .md manuscript | follow §2 format + §3 math rules |
| 2 Markup processing | gg generate / rr rewrite / ee expand / cc condense / vv fact-check | academic-markup | markers close in pairs, never nested across sections |
| 3 Translation | tt markers + the three-pass method | this skill (method below) | produces the `_en` draft; glossary maintained alongside |
| 4 Citations | `[['…']]` insert → refs numbering + reference list | academic-markup `refs` | RIS pool, see §2⑥ |
| 5 Clean copy | strip every marker | academic-markup | iron rule 1 scan |
| 6 Export | pandoc → docx | word-standards | caption/equation-number formatting is its job |

**The three-pass translation method** (station 3): pass 1 — understand and restructure (read the source, rebuild the paragraph's logical skeleton, do not translate sentence-by-sentence); pass 2 — draft the translation (render meaning, not words; keep terminology consistent with the glossary); pass 3 — polish as a reviewer (read aloud mentally, remove translationese, tighten connectives, verify every number and symbol against the source). Register a term in the glossary at its first occurrence.

## 2. Manuscript .md format specification

① **Files and naming**: manuscripts live in the project's manuscript area (e.g. `手稿\`); language suffixes `_zh` / `_en`; evolution happens on the canonical file (version history is the version log), final snapshots may take `_vN`; retired files carry `(过时)` (outdated) or `(失败)` (failed) suffixes.
② **Header block**: a single H1 title + a blockquote metadata line (status / purpose, e.g. target journal / glossary pointer); no "when was what done" time notes (dates only in ledger-type material).
③ **Sections and figures**: top-level structure Abstract → Introduction → Methods → Results → Discussion → Conclusions (merge as needed); body headings go down to `####`; `#####` and deeper are author-only writing hints — the word-standards pipeline strips those lines entirely at Word export (not shown, no blank line) while the .md keeps them; figures use relative paths and **every figure source must be regenerable** (derived data figures or vector-software exports); caption numbering and formats are word-standards' interface.
④ **Math**: see §3 and the full [references/math-typesetting.md](references/math-typesetting.md).
⑤ **Marker syntax registry** (the implementation truth is in academic-markup; on conflict, it wins):

| Marker | Meaning |
|---|---|
| `gg'…'gg` | generate a passage |
| `rr'…'rr` | rewrite |
| `tt'…'tt` | translate Chinese → English |
| `vv'…'vv` | fact-check |
| `ee'…'ee` / `cc'…'cc` | expand / condense |
| `[['…']]` | insert citation (key = a library entry) |
| `/refs` | regenerate citation numbers + reference list |

⑥ **Citation system**: the `[['key']]` key maps one-to-one onto a library entry; the RIS/ENW pool lives in each manuscript area's `reference\` (**held per manuscript**); running `refs` requires the manuscript directory as the working directory (or `--root` pointing at it), otherwise volume/issue/pages fail to resolve and the reference list falls back to index-level metadata. The manuscript-area scaffold (`AGENTS.md` + `reference\` + `figures\`, generated with the work skeleton) is templated in [references/manuscript-dir-agents.md](references/manuscript-dir-agents.md).
⑦ **Language flow**: draft in the working language → tt/three-pass → `_en` draft; register a term in the glossary at its first occurrence.
⑧ **Artifact chain and versioning**: .md canonical (committed) → clean copy → docx (an export, never committed).
⑨ **Punctuation and style**: AI-generated and AI-rewritten text should **favor short sentences ended by periods over dashes, colons and semicolons**; keep the latter only where an enumeration genuinely needs them.

## 3. Math typesetting (quick reference)

R1 scalars italic ｜ R2 vectors `\boldsymbol{}` ｜ R3 tensors: Latin `\mathbf{}`, Greek `\boldsymbol{\mathrm{}}` ｜ R4 subscript face follows the subscripted object's category (word abbreviations upright, variables italic) ｜ R5 dimensionless numbers upright (`\mathrm{Re}`) ｜ R6 differentials and material derivatives upright (`\mathrm{d}t`).
Full text (details, edge cases, examples, maintenance rules): [references/math-typesetting.md](references/math-typesetting.md); every symbol's face in a concrete manuscript must be **registered in that manuscript's symbol registry before use**.

**Registry audit**: `python scripts/symbol_audit.py <manuscript.md>…` (defaults to `符号登记表.md` beside the manuscript) — reports unregistered symbols, face mismatches against the registry, and `\text` leftovers; **reports, never edits**; unregistered items are entered by human/AI with a trail in the registry's "application and amendment record". Exit 1 = findings (usable as a pre-delivery gate). If the registry is lost or new: `--scaffold [--out new.md]` regenerates a **skeleton** from the manuscript (form and frequency automatic; semantics and canonical faces still need a human/AI ruling); a committed registry is best recovered from git history — its semantics column is a ruling asset that cannot be fully auto-regenerated.

## 4. Companion skills

| Skill | Owns |
|---|---|
| academic-markup | marker pipeline implementation (scan/recall/process/assemble/refs) |
| word-standards | md→pandoc→docx layout and conversion scripts |
| lit-symbol-translation | translating and recomputing literature symbols/values before they enter a draft |
| note-gen | maintaining the reference library (the source of citation keys) |

(The three-pass translation method is inlined in §1 and §2 — station 3 does not depend on a separate skill.)
