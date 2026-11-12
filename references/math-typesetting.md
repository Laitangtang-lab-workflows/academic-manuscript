# Math typesetting standard (manuscript domain)

> Merged from the former standalone "Math Format Spec v2" (established 2026-09-09; merged into the academic-manuscript skill, generically reworded, 2026-10-16).
> Rendering environment: Markdown inline `$…$`, display `$$…$$` (MathJax/KaTeX-compatible syntax).
> Nature: a **formal-layer convention** — it fixes the *face* of notation, never the content or values of formulas; **mandatory in the manuscript domain only**, advisory for research-document derivations.
> Division of labor: Chinese terminology goes to the glossary; this standard governs math faces.

## 1. Six base rules

| # | Object | Face | LaTeX |
|---|---|---|---|
| R1 | scalars (1-D variables) | italic | bare letters, no `\mathrm`: `$p$`, `$\rho$`, `$\theta$`, `$\dot\gamma$`, `$l$`, `$V$`, `$H$` |
| R2 | vectors | bold italic | `\boldsymbol{}`: `$\boldsymbol{u}$`, `$\boldsymbol{g}$`, `$\boldsymbol{n}$`, `$\boldsymbol{U}$` |
| R3 | tensors | bold upright | Latin `\mathbf{}`: `$\mathbf{D}$`, `$\mathbf{A}$`, `$\mathbf{R}$`; Greek `\boldsymbol{\mathrm{}}`: `$\boldsymbol{\mathrm{\tau}}$`, `$\boldsymbol{\mathrm{\Theta}}$`, `$\boldsymbol{\mathrm{\Lambda}}$` |
| R4 | subscripts | face follows the subscripted object's category (see §2) | below |
| R5 | dimensionless numbers | upright (ISO 80000) | `\mathrm{Re}`, `\mathrm{Wi}`, `\mathrm{We}`, `\mathrm{Fr}`, `\mathrm{Ca}`, `\mathrm{De}` |
| R6 | 1-D differentials, material derivatives | upright (ISO 80000) | `$\mathrm{d}t$`, `$\mathrm{d}\gamma$`, material derivative `$\dfrac{\mathrm{D}\boldsymbol{\tau}_\mathrm{p}}{\mathrm{D}t}$` |

## 2. R4 in detail — subscript face follows what the subscript denotes

| Subscript denotes | Face | Example |
|---|---|---|
| descriptive words/abbreviations (e.g. n nozzle, e extrudate, i inlet, s substrate, p polymer, w wall, r ratio; air, ink, exact, sim; components xx, yy, xy, nn, nt) | upright `\mathrm{}` | `$d_\mathrm{n}$`, `$u_\mathrm{i}$`, `$\tau_\mathrm{w}$`, `$W_\mathrm{s}$`, `$A_{\mathrm{exact}}$`, `$\rho_\mathrm{r}$` |
| scalar variables (incl. running indices) | italic | `$\dot\gamma_i$`, `$E_{a,b}$` |
| vectors | bold italic | `$F_{\boldsymbol{u}}$` (reserved) |
| tensors | bold upright | `$c_{\mathbf{A}}$` (reserved) |
| dimensionless numbers | upright | `$X_{\mathrm{Re}}$` (reserved) |

**Superscripts**: exponents keep defaults (digits or italic variables); transpose `$\mathrm{T}$`; phase labels `$\mathrm{ink}$`, `$\mathrm{air}$`; dimensionless-prime `$'$`.

## 3. Functions, operators, units

- Function and operator names are always upright: `\sin`, `\exp`, `\ln`, `\Gamma`, `\mathrm{tr}`, `\partial`, `\nabla`.
- Numbers and units: upright, with `\;` or `\,` between value and unit: `$0.26\;\mathrm{mm}$`, `$2\times10^{-3}\;\mathrm{g\,mm^{-3}}$`.
- Display equations carry right-aligned numbers via `\tag{n}` (the `\tag{}` pitfall at docx conversion is word-standards' business); when `\text{}` and `\mathrm{}` conflict, use `\mathrm{}` uniformly.
- Dimensionless-number groups: `$(\mathrm{Re},\mathrm{Wi},\mathrm{We})$`; ratios and powers as `$\frac{1}{\mathrm{Re}}$`.

## 4. Settled edge cases

| Case | Treatment | Basis |
|---|---|---|
| a, b in `E_{a,b}` | stay italic | R4: variable-like subscripts |
| i in `\dot\gamma_i` | stays italic | R4: a running index is a variable |
| scalar variables named in prose ("parameters `$a = b = 1$`") | italic | R1: not a subscript context |
| `\mathrm{Ca}_\mathrm{e}` | Ca upright (R5) + subscript e upright (R4 word abbreviation) | — |
| `\text{}` vs `\mathrm{}` | use `\mathrm{}` uniformly | §3 |

## 5. Examples (legal forms)

Inline: $l = a\,d_\mathrm{e}\sqrt{v_\mathrm{e}/v_\mathrm{n}}$; $\mathrm{Ca}_\mathrm{e}=\eta_0 u_\mathrm{e}/\sigma$; running indices stay italic: $\eta_{\mathrm{fit}}(\dot\gamma_i)$.

$$
f\,\boldsymbol{\mathrm{\tau}}' + \mathrm{Wi}\,\overset{\square}{\boldsymbol{\mathrm{\tau}}'} = \alpha\!\left(\nabla'\boldsymbol{U}+\nabla'\boldsymbol{U}^{\mathrm T}\right), \tag{9}
$$

## 6. Maintenance

1. Register a new symbol's face in that manuscript's **symbol registry** before using it;
2. rule changes require user confirmation and a version-line entry here recording what changed and when;
3. after a batch face-unification pass, mark "applied (date)" in that manuscript's symbol registry.
