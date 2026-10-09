# Quality Assurance (QA) Verification Protocol

This protocol defines the 10 quality gates required before publishing any bilingual chapter or volume. Automated checks are executed using `scripts/verify_qa.py`.

---

## The 10 Quality Gates

| # | Quality Gate | Scope | Automated Tool / Rule |
| :---: | :--- | :--- | :--- |
| **1** | **Bilingual Block Parity** | Structural | Count of `\en{...}` must strictly equal `\zh{...}`. Count of `\begin{enblock}` must strictly equal `\begin{zhblock}`. |
| **2** | **Mathematical Balance** | Syntactic | Inline math dollar signs (`$`) must be even in each file. `\[` and `\]` must balance. |
| **3** | **Environment Integrity** | Syntactic | Every `\begin{env}` (`theorem`, `proof`, `align`, `gather`) must have a matching `\end{env}`. |
| **4** | **Label Uniqueness** | References | No duplicate `\label{...}` entries across chapters. |
| **5** | **Original Page Tracking** | Fidelity | Every transition in original pagination must be marked with `\origpage{N}`. |
| **6** | **Reference Convergence** | Compilation | Zero `LaTeX Warning: Reference ... undefined` in `.log` file. |
| **7** | **Font Glyph Coverage** | Compilation | Zero `Missing character: There is no ...` in `.log` file. |
| **8** | **Term Database Parity** | Terminology | Every term invoked via `\term` or `\acnote` must exist in `glossary.json`. |
| **9** | **Margin Note Density** | Visual | Maximum 5 annotations per page to prevent margin overruns. |
| **10** | **Proof Completion Marks** | Semantics | Every mathematical proof must conclude with an appropriate Q.E.D. mark (`\qed` or `\square`). |

---

## Troubleshooting Common Issues

### 1. Parity Mismatch (`\en` vs `\zh`)
- **Cause**: An author translated multiple English paragraphs into a single Chinese block or omitted a translation block.
- **Fix**: Split the Chinese block so each `\en` block corresponds 1-to-1 with a `\zh` block.

### 2. Missing Glyph (`Missing character: There is no ... in font ...`)
- **Cause**: A special Unicode symbol (e.g. archaic script, specific Fraktur letter, or Chinese punctuation) is not supported by the primary font.
- **Fix**: Ensure `unicode-math` uses `texgyrepagella-math.otf`, and CJK fonts use `Songti SC` / `PingFang SC`. For exotic mathematical symbols, fallback to standard LaTeX command equivalents (e.g. `\mathbb{R}` instead of raw blackboard letters).

### 3. Margin Note Overlapping
- **Cause**: Too many `\term` or `\acnote` macros placed within a few lines.
- **Fix**: Distribute annotations throughout the section, or convert secondary terms to in-text mentions while reserving margin notes for the most essential terminology.
